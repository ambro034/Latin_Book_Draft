"""Index BeOps `_posts/*.md` into pgvector.

Idempotent + incremental:
  - posts.body_hash skips unchanged posts in O(1)
  - chunks deleted-then-reinserted only for posts whose hash changed
  - posts present in DB but missing from disk are deleted (rename / un-publish)
  - serialized via pg_try_advisory_lock so concurrent workflow runs don't race
"""
from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path

import psycopg
from psycopg.types.json import Json  # noqa: F401  (kept for future use)

from . import EMBEDDING_DIM
from .chunker import body_hash, chunk_markdown, parse_front_matter
from .db import acquire_index_lock, assert_meta_matches, init_schema
from .embedder import embed

log = logging.getLogger(__name__)

JEKYLL_URL_BASE = "https://neverthesame.github.io/BeOps"


@dataclass(frozen=True)
class IndexStats:
    scanned: int = 0
    inserted: int = 0
    updated: int = 0
    unchanged: int = 0
    deleted: int = 0
    chunks_written: int = 0

    def merged(self, **kw: int) -> "IndexStats":
        return IndexStats(
            scanned=kw.get("scanned", self.scanned),
            inserted=kw.get("inserted", self.inserted),
            updated=kw.get("updated", self.updated),
            unchanged=kw.get("unchanged", self.unchanged),
            deleted=kw.get("deleted", self.deleted),
            chunks_written=kw.get("chunks_written", self.chunks_written),
        )


def _post_url(category: str, slug: str) -> str:
    return f"{JEKYLL_URL_BASE}/{category}/{slug}.html"


def _load_post(path: Path) -> tuple[str, str, str, str, str] | None:
    """Return (slug, title, category, url, body) or None if frontmatter incomplete."""
    text = path.read_text(encoding="utf-8")
    fm, _ = parse_front_matter(text)
    title = (fm.get("title") or "").strip()
    category = (fm.get("category") or "").strip()
    if not title or not category:
        log.warning("skipping %s: missing title/category", path.name)
        return None
    slug = path.stem
    return slug, title, category, _post_url(category, slug), text


def index(
    conn: psycopg.Connection,
    posts_dir: Path,
    *,
    force: bool = False,
) -> IndexStats:
    """Index every Markdown post under `posts_dir`."""
    assert_meta_matches(conn)
    init_schema(conn)  # idempotent; creates tables if missing and pins meta

    if not acquire_index_lock(conn):
        raise RuntimeError(
            "another indexer holds the advisory lock — refusing to run"
        )

    stats = IndexStats()

    # 1) reconcile filesystem vs DB by slug ----------------------------------
    fs_slugs: set[str] = set()
    posts_to_process: list[tuple[str, str, str, str, str, str]] = []
    for md in sorted(posts_dir.glob("*.md")):
        loaded = _load_post(md)
        if loaded is None:
            continue
        slug, title, category, url, text = loaded
        fs_slugs.add(slug)
        posts_to_process.append((slug, title, category, url, text, body_hash(text)))
        stats = stats.merged(scanned=stats.scanned + 1)

    with conn.cursor() as cur:
        cur.execute("select slug, body_hash from posts")
        existing = {s: h for s, h in cur.fetchall()}

    # 2) delete posts no longer on disk -------------------------------------
    orphan_slugs = [s for s in existing if s not in fs_slugs]
    if orphan_slugs:
        with conn.cursor() as cur:
            cur.execute("delete from posts where slug = any(%s)", (orphan_slugs,))
        stats = stats.merged(deleted=len(orphan_slugs))
        log.info("deleted %d orphan posts: %s", len(orphan_slugs), orphan_slugs)

    # 3) upsert posts; re-chunk + re-embed only those whose hash changed -----
    to_embed: list[tuple[str, str, str, str, str, str]] = []
    for slug, title, category, url, text, h in posts_to_process:
        prev = existing.get(slug)
        if prev == h and not force:
            stats = stats.merged(unchanged=stats.unchanged + 1)
            # still upsert metadata so title/category edits propagate cheaply
            with conn.cursor() as cur:
                cur.execute(
                    """
                    update posts
                       set title = %s, category = %s, url = %s, updated_at = now()
                     where slug = %s
                    """,
                    (title, category, url, slug),
                )
            continue
        to_embed.append((slug, title, category, url, text, h))
        if prev is None:
            stats = stats.merged(inserted=stats.inserted + 1)
        else:
            stats = stats.merged(updated=stats.updated + 1)

    # 4) re-chunk + embed in one batch (huge speedup for sentence-transformers)
    chunk_payload: list[tuple[str, int, str]] = []  # (slug, ord, text)
    for slug, _, _, _, text, _ in to_embed:
        for c in chunk_markdown(text):
            chunk_payload.append((slug, c.ord, c.text))

    if to_embed:
        log.info(
            "embedding %d chunks across %d changed posts",
            len(chunk_payload), len(to_embed),
        )
        vecs = embed([t for _, _, t in chunk_payload]) if chunk_payload else None

        with conn.cursor() as cur:
            # delete old chunks for changed posts in one shot
            cur.execute(
                "delete from chunks where slug = any(%s)",
                ([s for s, *_ in to_embed],),
            )
            # upsert posts
            for slug, title, category, url, text, h in to_embed:
                cur.execute(
                    """
                    insert into posts(slug, title, category, url, body_hash, body)
                    values (%s, %s, %s, %s, %s, %s)
                    on conflict (slug) do update set
                      title = excluded.title,
                      category = excluded.category,
                      url = excluded.url,
                      body_hash = excluded.body_hash,
                      body = excluded.body,
                      updated_at = now()
                    """,
                    (slug, title, category, url, h, text),
                )
            # insert chunks
            for (slug, ord_, text), vec in zip(chunk_payload, vecs):
                cur.execute(
                    "insert into chunks(slug, ord, text, embedding) "
                    "values (%s, %s, %s, %s::vector)",
                    (slug, ord_, text, vec.tolist()),
                )
        stats = stats.merged(chunks_written=len(chunk_payload))

    conn.commit()
    log.info("index done: %s", stats)
    return stats


def reset(conn: psycopg.Connection) -> None:
    """Drop and recreate everything. Used by CLI `reset` for schema/model bumps."""
    with conn.cursor() as cur:
        cur.execute("drop table if exists chunks cascade")
        cur.execute("drop table if exists posts cascade")
        cur.execute("drop table if exists rag_meta cascade")
        cur.execute("drop function if exists search_chunks(text, vector, int, int)")
    conn.commit()
    init_schema(conn)
    log.info("schema reset complete")

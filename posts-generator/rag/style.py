"""Style corpus: index the author's own Telegram posts and retrieve voice
exemplars for drafting new Telegram posts.

Kept deliberately separate from the blog RAG (rag.indexer / rag.retriever):
different tables (style_posts/style_chunks), different FTS config ('simple'
for mixed RU/EN), and a different SQL search function (search_style_chunks).
This guarantees the blog anti-rehash retrieval is never polluted by channel
posts.

Reuses the shared embedder (MiniLM-L6-v2, 384-d) and DB connection helpers.

CLI:
    python -m rag.style init
    python -m rag.style index [style_corpus/telegram_posts.jsonl]
    python -m rag.style reset
    python -m rag.style examples "topic / seed text" [-k 6]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import logging
from dataclasses import dataclass
from pathlib import Path

import psycopg

from . import CHUNKER_VERSION, EMBEDDING_DIM, EMBEDDING_MODEL, SCHEMA_VERSION
from .chunker import chunk_markdown
from .db import acquire_index_lock, connect
from .embedder import embed, embed_one

log = logging.getLogger(__name__)

# Drop obvious service/empty messages (e.g. "Channel created").
_MIN_TEXT_LEN = 20

# Distinct advisory-lock key from the blog indexer (7142001) so the two
# indexers never collide when triggered concurrently.
_STYLE_LOCK_KEY = 7142002


def _schema_path() -> Path:
    return Path(__file__).with_name("style_schema.sql")


def _default_corpus() -> Path:
    # posts-generator/rag/style.py -> ../style_corpus/telegram_posts.jsonl
    return Path(__file__).resolve().parents[1] / "style_corpus" / "telegram_posts.jsonl"


def _expected_meta() -> dict[str, str]:
    return {
        "schema_version": SCHEMA_VERSION,
        "embedding_model": EMBEDDING_MODEL,
        "embedding_dim": str(EMBEDDING_DIM),
        "chunker_version": CHUNKER_VERSION,
    }


def assert_meta_matches(conn: psycopg.Connection) -> None:
    """Abort if the style DB was indexed with a different model/chunker/schema.

    Prevents silent retrieval drift (unchanged posts keep old embeddings while
    a new model is in use). Recover with `python -m rag.style reset` then `index`.
    """
    with conn.cursor() as cur:
        cur.execute("select key, value from style_meta")
        meta = {k: v for k, v in cur.fetchall()}
    if not meta:
        return
    mismatches = {
        k: (meta.get(k), v) for k, v in _expected_meta().items() if meta.get(k) != v
    }
    if mismatches:
        raise RuntimeError(
            "style_meta mismatch — DB indexed with different params. "
            f"got/want: {mismatches}. Run `python -m rag.style reset` then `index`."
        )


def init_schema(conn: psycopg.Connection) -> None:
    """Create style tables + function. Idempotent."""
    conn.execute(_schema_path().read_text(encoding="utf-8"))
    for k, v in _expected_meta().items():
        conn.execute(
            "insert into style_meta(key, value) values (%s, %s) "
            "on conflict (key) do update set value = excluded.value, "
            "updated_at = now()",
            (k, v),
        )
    conn.commit()


def reset(conn: psycopg.Connection) -> None:
    conn.execute("drop table if exists style_chunks cascade")
    conn.execute("drop table if exists style_posts cascade")
    conn.execute("drop table if exists style_meta cascade")
    conn.execute("drop function if exists search_style_chunks(text, vector, int, int)")
    conn.commit()
    init_schema(conn)
    log.info("style schema reset complete")


def _body_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_corpus(path: Path) -> list[dict]:
    """Read the JSONL corpus, dropping empty/service messages."""
    rows: list[dict] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        rec = json.loads(line)
        text = (rec.get("text") or "").strip()
        if len(text) < _MIN_TEXT_LEN:
            continue
        rows.append(
            {
                "id": int(rec["id"]),
                "channel": rec.get("channel", ""),
                "date": rec.get("date") or None,
                "text": text,
            }
        )
    return rows


@dataclass(frozen=True)
class StyleStats:
    scanned: int = 0
    inserted: int = 0
    updated: int = 0
    unchanged: int = 0
    deleted: int = 0
    chunks_written: int = 0


def index(conn: psycopg.Connection, corpus_path: Path, *, force: bool = False) -> StyleStats:
    """Index the Telegram style corpus. Idempotent + incremental by body_hash."""
    # Drift guard: compare against existing meta BEFORE init_schema rewrites it.
    try:
        assert_meta_matches(conn)
    except psycopg.errors.UndefinedTable:
        conn.rollback()  # fresh DB, no style_meta table yet
    init_schema(conn)
    if not acquire_index_lock(conn, _STYLE_LOCK_KEY):
        raise RuntimeError("another style indexer holds the advisory lock — refusing to run")

    rows = load_corpus(corpus_path)
    fs_ids = {r["id"] for r in rows}

    with conn.cursor() as cur:
        cur.execute("select tg_id, body_hash from style_posts")
        existing = {i: h for i, h in cur.fetchall()}

    # delete posts no longer present in the corpus
    orphans = [i for i in existing if i not in fs_ids]
    deleted = 0
    if orphans:
        with conn.cursor() as cur:
            cur.execute("delete from style_posts where tg_id = any(%s)", (orphans,))
        deleted = len(orphans)

    to_embed: list[dict] = []
    inserted = updated = unchanged = 0
    for r in rows:
        h = _body_hash(r["text"])
        prev = existing.get(r["id"])
        if prev == h and not force:
            unchanged += 1
            with conn.cursor() as cur:
                cur.execute(
                    "update style_posts set channel = %s, posted_at = %s, "
                    "updated_at = now() where tg_id = %s",
                    (r["channel"], r["date"], r["id"]),
                )
            continue
        r["_hash"] = h
        to_embed.append(r)
        if prev is None:
            inserted += 1
        else:
            updated += 1

    chunk_payload: list[tuple[int, int, str]] = []
    for r in to_embed:
        for c in chunk_markdown(r["text"]):
            chunk_payload.append((r["id"], c.ord, c.text))

    chunks_written = 0
    if to_embed:
        vecs = embed([t for _, _, t in chunk_payload]) if chunk_payload else []
        with conn.cursor() as cur:
            cur.execute(
                "delete from style_chunks where tg_id = any(%s)",
                ([r["id"] for r in to_embed],),
            )
            for r in to_embed:
                cur.execute(
                    "insert into style_posts(tg_id, channel, posted_at, body_hash, body) "
                    "values (%s, %s, %s, %s, %s) "
                    "on conflict (tg_id) do update set "
                    "channel = excluded.channel, posted_at = excluded.posted_at, "
                    "body_hash = excluded.body_hash, body = excluded.body, "
                    "updated_at = now()",
                    (r["id"], r["channel"], r["date"], r["_hash"], r["text"]),
                )
            for (tg_id, ord_, text), vec in zip(chunk_payload, vecs):
                cur.execute(
                    "insert into style_chunks(tg_id, ord, text, embedding) "
                    "values (%s, %s, %s, %s::vector)",
                    (tg_id, ord_, text, vec.tolist()),
                )
        chunks_written = len(chunk_payload)

    conn.commit()
    stats = StyleStats(
        scanned=len(rows),
        inserted=inserted,
        updated=updated,
        unchanged=unchanged,
        deleted=deleted,
        chunks_written=chunks_written,
    )
    log.info("style index done: %s", stats)
    return stats


@dataclass(frozen=True)
class StyleExample:
    tg_id: int
    text: str
    score: float


def style_examples(
    conn: psycopg.Connection, seed: str, k: int = 6, pool: int = 40
) -> list[StyleExample]:
    """Return up to k of the author's own posts most similar to `seed`.

    Searches chunks for recall, then returns the FULL post body per distinct
    tg_id (we want whole-voice exemplars, not fragments), best-ranked first.
    """
    q_emb = embed_one(seed).tolist()
    with conn.cursor() as cur:
        cur.execute(
            "select tg_id, ord, text, rrf from search_style_chunks(%s, %s::vector, %s, %s)",
            (seed, q_emb, k * 3, pool),
        )
        hits = cur.fetchall()

    best: dict[int, float] = {}
    order: list[int] = []
    for tg_id, _ord, _text, rrf in hits:
        if tg_id not in best:
            order.append(tg_id)
        best[tg_id] = max(best.get(tg_id, 0.0), float(rrf))
    top_ids = sorted(order, key=lambda i: best[i], reverse=True)[:k]
    if not top_ids:
        return []

    with conn.cursor() as cur:
        cur.execute("select tg_id, body from style_posts where tg_id = any(%s)", (top_ids,))
        bodies = {i: b for i, b in cur.fetchall()}

    return [
        StyleExample(tg_id=i, text=bodies.get(i, ""), score=best[i])
        for i in top_ids
        if bodies.get(i)
    ]


def examples_block(conn: psycopg.Connection, seed: str, k: int = 6) -> str:
    """Format style exemplars as a prompt block for the drafter."""
    ex = style_examples(conn, seed, k=k)
    if not ex:
        return ""
    parts = [
        "REAL EXAMPLES OF HOW THE AUTHOR WRITES TELEGRAM POSTS "
        "(study the voice, tone, length, emoji use, lowercase habits — then "
        "imitate the STYLE, not the content):",
        "",
    ]
    for i, e in enumerate(ex, 1):
        parts.append(f"--- example {i} ---\n{e.text.strip()}")
    return "\n".join(parts)


def main(argv: list[str] | None = None) -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s %(message)s")
    p = argparse.ArgumentParser(prog="rag.style")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("init", help="create style schema (idempotent)")
    pi = sub.add_parser("index", help="index the telegram style corpus")
    pi.add_argument("path", nargs="?", default=None)
    pi.add_argument("--force", action="store_true")
    sub.add_parser("reset", help="drop + recreate style schema (destructive)")
    pe = sub.add_parser("examples", help="print voice exemplars for a seed")
    pe.add_argument("seed")
    pe.add_argument("-k", type=int, default=6)
    args = p.parse_args(argv)

    if args.cmd == "init":
        with connect() as conn:
            init_schema(conn)
        print("style schema ready")
        return 0
    if args.cmd == "reset":
        with connect() as conn:
            reset(conn)
        print("style schema reset")
        return 0
    if args.cmd == "index":
        path = Path(args.path) if args.path else _default_corpus()
        with connect() as conn:
            print(index(conn, path, force=args.force))
        return 0
    if args.cmd == "examples":
        with connect() as conn:
            print(examples_block(conn, args.seed, k=args.k))
        return 0
    return 2


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())

"""Retrieval helpers.

The actual hybrid search runs inside Postgres (see schema.sql ::
search_chunks()). This module provides:
  - rrf_fuse(): pure-Python RRF for unit-testing the math
  - search(): thin Python wrapper around the SQL function
  - context_for(): formatted string ready to drop into an LLM prompt
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import psycopg

from .embedder import embed_one

RRF_K = 60  # Cormack et al. 2009 default


@dataclass(frozen=True)
class Hit:
    slug: str
    ord: int
    text: str
    score: float


def rrf_fuse(
    rankings: Sequence[Sequence[str]],
    k: int = RRF_K,
) -> list[tuple[str, float]]:
    """Reciprocal Rank Fusion.

    Each ranking is a sequence of ids in best-first order. Returns
    (id, score) pairs sorted by descending score. Items missing from a
    ranking contribute 0 for that ranking.
    """
    scores: dict[str, float] = {}
    for ranking in rankings:
        for rank, item in enumerate(ranking, start=1):
            scores[item] = scores.get(item, 0.0) + 1.0 / (k + rank)
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)


def search(
    conn: psycopg.Connection,
    query: str,
    k: int = 8,
    pool: int = 50,
) -> list[Hit]:
    """Hybrid search via the in-DB `search_chunks` function."""
    q_emb = embed_one(query).tolist()
    with conn.cursor() as cur:
        cur.execute(
            "select slug, ord, text, rrf from search_chunks(%s, %s::vector, %s, %s)",
            (query, q_emb, k, pool),
        )
        rows = cur.fetchall()
    return [Hit(slug=s, ord=o, text=t, score=float(r)) for s, o, t, r in rows]


def context_for(
    conn: psycopg.Connection,
    seed: str,
    k: int = 8,
    base_url: str = "https://neverthesame.github.io/BeOps",
) -> str:
    """Return a prompt-ready 'prior work' block. Empty string if no hits."""
    hits = search(conn, seed, k=k)
    if not hits:
        return ""
    # Resolve URLs (one query, in-clause)
    slugs = list({h.slug for h in hits})
    with conn.cursor() as cur:
        cur.execute(
            "select slug, url, title from posts where slug = any(%s)", (slugs,)
        )
        meta = {s: (u, t) for s, u, t in cur.fetchall()}

    lines = ["PRIOR POSTS YOU HAVE ALREADY WRITTEN (cite the URL inline when "
             "you build on them; do NOT rehash them):", ""]
    for h in hits:
        url, title = meta.get(h.slug, (f"{base_url}/?{h.slug}", h.slug))
        snippet = h.text.strip().replace("\n", " ")
        if len(snippet) > 600:
            snippet = snippet[:600].rsplit(" ", 1)[0] + "…"
        lines.append(f"- [{title}]({url}) — {snippet}")
    lines.append("")
    lines.append(
        "If a topic is already covered above, write a short pointer paragraph "
        "linking to it instead of re-explaining."
    )
    return "\n".join(lines)

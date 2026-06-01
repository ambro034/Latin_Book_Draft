"""Integration tests for the style corpus against a real Postgres + pgvector.

Requires `BEOPS_TEST_DATABASE_URL` (CI) or `NEON_API_KEY` + `NEON_PROJECT_ID`
(ephemeral local branch). See conftest.py. Skipped otherwise.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

pytest.importorskip("sentence_transformers")
pytest.importorskip("psycopg")

from rag import style


def _write_corpus(d: Path, rows: list[dict]) -> Path:
    p = d / "telegram_posts.jsonl"
    p.write_text(
        "\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n",
        encoding="utf-8",
    )
    return p


def test_index_and_retrieve_voice_examples(conn, tmp_path):
    style.reset(conn)
    corpus = _write_corpus(
        tmp_path,
        [
            {"id": 1, "channel": "beops_it", "date": "2025-01-01T00:00:00+00:00",
             "text": "kubernetes readiness probes saved my sleep again, here is how I tune them in prod"},
            {"id": 2, "channel": "beops_it", "date": "2025-02-01T00:00:00+00:00",
             "text": "neon postgres scale-to-zero is great for cheap side projects and vector search"},
            {"id": 3, "channel": "beops_it", "date": "2025-03-01T00:00:00+00:00",
             "text": "short note about coffee and rubber ducks, nothing technical here at all"},
        ],
    )

    stats = style.index(conn, corpus)
    assert stats.scanned == 3
    assert stats.inserted == 3
    assert stats.chunks_written >= 3

    # idempotent: second run changes nothing
    stats2 = style.index(conn, corpus)
    assert stats2.inserted == 0
    assert stats2.unchanged == 3

    hits = style.style_examples(conn, "tuning kubernetes probes in production", k=2)
    assert hits, "expected at least one style example"
    assert hits[0].tg_id == 1

    block = style.examples_block(conn, "postgres vector database", k=2)
    assert "REAL EXAMPLES" in block
    assert "neon postgres" in block.lower()


def test_orphan_removal(conn, tmp_path):
    style.reset(conn)
    corpus = _write_corpus(
        tmp_path,
        [
            {"id": 10, "channel": "beops_it", "date": None, "text": "first post about devops and ci pipelines"},
            {"id": 11, "channel": "beops_it", "date": None, "text": "second post about terraform and cloud infra"},
        ],
    )
    style.index(conn, corpus)

    smaller = _write_corpus(
        tmp_path,
        [{"id": 10, "channel": "beops_it", "date": None, "text": "first post about devops and ci pipelines"}],
    )
    stats = style.index(conn, smaller)
    assert stats.deleted == 1

    with conn.cursor() as cur:
        cur.execute("select count(*) from style_posts")
        (n,) = cur.fetchone()
    assert n == 1

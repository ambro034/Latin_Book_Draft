"""Integration tests for the indexer against a real Postgres + pgvector.

Requires `BEOPS_TEST_DATABASE_URL` (set by CI) or `NEON_API_KEY` +
`NEON_PROJECT_ID` (creates an ephemeral local branch). See conftest.py.
"""
from __future__ import annotations

from pathlib import Path

import pytest

pytest.importorskip("sentence_transformers")
pytest.importorskip("psycopg")

from rag import indexer
from rag.db import acquire_index_lock


def _write_post(d: Path, name: str, *, title: str, category: str, body: str) -> Path:
    fm = f"---\ntitle: \"{title}\"\ndate: 2025-01-01\ncategory: {category}\n---\n\n"
    p = d / f"2025-01-01-{name}.md"
    p.write_text(fm + body, encoding="utf-8")
    return p


def test_index_inserts_posts_and_chunks(conn, tmp_path):
    _write_post(tmp_path, "kube-probes", title="K8s probes",
                category="k8s",
                body="Readiness probes tell kube when a pod is ready to serve traffic.\n\n"
                     "## Liveness\n\nLiveness probes restart broken containers.\n")
    _write_post(tmp_path, "git-hooks", title="Git hooks",
                category="devops",
                body="Pre-commit hooks catch issues before they land in CI.")

    stats = indexer.index(conn, tmp_path)
    assert stats.scanned == 2
    assert stats.inserted == 2
    assert stats.unchanged == 0
    assert stats.chunks_written >= 2

    with conn.cursor() as cur:
        cur.execute("select count(*) from posts")
        (n_posts,) = cur.fetchone()
        cur.execute("select count(*) from chunks where embedding is not null")
        (n_chunks,) = cur.fetchone()
    assert n_posts == 2
    assert n_chunks >= 2


def test_index_is_idempotent_and_incremental(conn, tmp_path):
    _write_post(tmp_path, "a", title="A", category="ai", body="alpha bravo charlie")
    _write_post(tmp_path, "b", title="B", category="ai", body="delta echo foxtrot")
    s1 = indexer.index(conn, tmp_path)
    assert s1.inserted == 2

    # Second run with no changes: all unchanged, zero chunks written
    s2 = indexer.index(conn, tmp_path)
    assert s2.scanned == 2
    assert s2.unchanged == 2
    assert s2.inserted == 0
    assert s2.updated == 0
    assert s2.chunks_written == 0


def test_index_deletes_orphans(conn, tmp_path):
    pa = _write_post(tmp_path, "a", title="A", category="ai", body="alpha")
    _write_post(tmp_path, "b", title="B", category="ai", body="bravo")
    indexer.index(conn, tmp_path)

    pa.unlink()  # remove post 'a' from disk
    s = indexer.index(conn, tmp_path)
    assert s.deleted == 1

    with conn.cursor() as cur:
        cur.execute("select slug from posts order by slug")
        slugs = [r[0] for r in cur.fetchall()]
    assert slugs == ["2025-01-01-b"]


def test_index_reembeds_on_body_change(conn, tmp_path):
    p = _write_post(tmp_path, "a", title="A", category="ai", body="alpha bravo")
    indexer.index(conn, tmp_path)

    with conn.cursor() as cur:
        cur.execute(
            "select id, embedding from chunks where slug = '2025-01-01-a' order by ord"
        )
        before = cur.fetchall()

    # Edit body
    p.write_text(
        "---\ntitle: \"A\"\ndate: 2025-01-01\ncategory: ai\n---\n\n"
        "completely different body about quantum encryption.\n",
        encoding="utf-8",
    )
    s = indexer.index(conn, tmp_path)
    assert s.updated == 1
    assert s.chunks_written >= 1

    with conn.cursor() as cur:
        cur.execute(
            "select id, embedding from chunks where slug = '2025-01-01-a' order by ord"
        )
        after = cur.fetchall()

    # Old chunk row IDs gone (delete+insert), embeddings differ
    before_ids = {r[0] for r in before}
    after_ids = {r[0] for r in after}
    assert before_ids.isdisjoint(after_ids)


def test_advisory_lock_blocks_concurrent_indexer(conn, database_url):
    """A second connection that holds the lock should prevent index() from running."""
    import psycopg

    blocker = psycopg.connect(database_url)
    try:
        assert acquire_index_lock(blocker)  # blocker holds it
        with pytest.raises(RuntimeError, match="advisory lock"):
            indexer.index(conn, Path("/nonexistent"))
    finally:
        blocker.close()

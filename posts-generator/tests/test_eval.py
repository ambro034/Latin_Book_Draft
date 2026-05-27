"""Retrieval-quality regression gate.

Indexes the *real* `_posts/` directory and asserts that each query in
`fixtures/eval_queries.yaml` retrieves its expected slug(s) in the top-K.

Failing this test means a change to the chunker / embedder / RRF / SQL
just regressed retrieval quality. Either revert, or update the fixture
with intent.
"""
from __future__ import annotations

from pathlib import Path

import pytest
import yaml

pytest.importorskip("sentence_transformers")
pytest.importorskip("psycopg")

from rag import indexer, retriever


REPO_ROOT = Path(__file__).resolve().parents[2]
POSTS_DIR = REPO_ROOT / "_posts"
FIXTURE = Path(__file__).with_name("fixtures") / "eval_queries.yaml"


@pytest.fixture(scope="module")
def real_corpus_db(database_url):
    """Index the real `_posts/` corpus once for all eval queries."""
    import psycopg

    if not POSTS_DIR.exists():
        pytest.skip(f"no posts at {POSTS_DIR}")

    c = psycopg.connect(database_url)
    try:
        with c.cursor() as cur:
            cur.execute("create extension if not exists vector")
        c.commit()
        indexer.reset(c)
        indexer.index(c, POSTS_DIR)
        yield c
    finally:
        c.close()


def _load_queries():
    data = yaml.safe_load(FIXTURE.read_text(encoding="utf-8"))
    return data["queries"]


@pytest.mark.parametrize("case", _load_queries(), ids=lambda c: c["query"][:40])
def test_eval_query_finds_expected_slug(real_corpus_db, case):
    k = case.get("top_k", 5)
    hits = retriever.search(real_corpus_db, case["query"], k=k)
    got_slugs = [h.slug for h in hits]
    for expected in case["expect_in_top"]:
        assert expected in got_slugs, (
            f"\nquery: {case['query']!r}\n"
            f"expected slug {expected!r} in top-{k}, got: {got_slugs}"
        )

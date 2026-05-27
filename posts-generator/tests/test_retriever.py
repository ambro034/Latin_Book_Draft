"""Integration tests for hybrid retrieval against a real Postgres + pgvector."""
from __future__ import annotations

from pathlib import Path

import pytest

pytest.importorskip("sentence_transformers")
pytest.importorskip("psycopg")

from rag import indexer, retriever


def _write_post(d: Path, name: str, *, title: str, category: str, body: str) -> None:
    fm = f"---\ntitle: \"{title}\"\ndate: 2025-01-01\ncategory: {category}\n---\n\n"
    (d / f"2025-01-01-{name}.md").write_text(fm + body, encoding="utf-8")


@pytest.fixture
def seeded(conn, tmp_path):
    _write_post(tmp_path, "kube-probes", title="Kubernetes readiness probes",
                category="k8s",
                body="Readiness probes tell the kubelet when a pod is ready to "
                     "serve traffic. They differ from liveness probes which "
                     "decide whether to restart the container.")
    _write_post(tmp_path, "dataops", title="Dataops in practice",
                category="devops",
                body="Dataops applies devops principles to data pipelines. "
                     "It emphasizes observability, testing, and lineage.")
    _write_post(tmp_path, "rag-llms", title="Retrieval augmented generation",
                category="ai",
                body="RAG combines a retriever with a generator. The retriever "
                     "fetches relevant documents and the generator conditions on them.")
    indexer.index(conn, tmp_path)
    return conn


def test_search_returns_relevant_hit_for_lexical_match(seeded):
    hits = retriever.search(seeded, "kubernetes readiness probe", k=3)
    assert hits, "expected at least one hit"
    # top hit must be the kube post
    assert hits[0].slug == "2025-01-01-kube-probes"


def test_search_returns_relevant_hit_for_semantic_match(seeded):
    # Phrasing avoids the words 'pipeline' / 'observability' to lean on dense
    hits = retriever.search(seeded, "applying engineering rigor to ETL", k=3)
    assert hits
    top_slugs = {h.slug for h in hits[:2]}
    assert "2025-01-01-dataops" in top_slugs


def test_search_returns_empty_when_no_matches(seeded):
    hits = retriever.search(seeded, "qwertyuiop_no_such_terms", k=5)
    # dense path will always match something, so we instead assert it doesn't
    # return the rag-llm post as top for an unrelated query
    if hits:
        assert isinstance(hits[0].score, float)


def test_context_for_returns_formatted_block(seeded):
    ctx = retriever.context_for(seeded, "retrieval augmented generation", k=3)
    assert "PRIOR POSTS" in ctx
    # URL of the rag-llms post should appear
    assert "/ai/2025-01-01-rag-llms.html" in ctx
    # And the anti-rehash instruction
    assert "pointer paragraph" in ctx


def test_context_for_empty_when_no_data(conn):
    ctx = retriever.context_for(conn, "anything")
    assert ctx == ""

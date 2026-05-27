"""Unit tests for the embedder.

Requires sentence-transformers; skipped if not installed (e.g. when running
the smoke test that asserts the generator can run without the RAG deps).
"""
from __future__ import annotations

import math

import pytest

st = pytest.importorskip("sentence_transformers")  # noqa: F841

from rag import EMBEDDING_DIM
from rag.embedder import embed, embed_one


def test_embed_returns_correct_shape_and_dtype():
    vecs = embed(["hello world", "kubernetes ingress controllers"])
    assert vecs.shape == (2, EMBEDDING_DIM)
    assert vecs.dtype.name == "float32"


def test_embed_is_l2_normalized():
    vecs = embed(["sample text for normalization check"])
    norm = float((vecs[0] ** 2).sum() ** 0.5)
    assert math.isclose(norm, 1.0, abs_tol=1e-3)


def test_embed_is_deterministic():
    a = embed_one("the quick brown fox")
    b = embed_one("the quick brown fox")
    assert (a == b).all()


def test_embed_empty_input():
    vecs = embed([])
    assert vecs.shape == (0, EMBEDDING_DIM)


def test_semantically_similar_inputs_have_higher_cosine():
    a = embed_one("kubernetes pod readiness probe")
    b = embed_one("k8s readiness check on pods")
    c = embed_one("how to bake sourdough bread")
    # cosine == dot since vectors are L2-normalized
    sim_ab = float((a * b).sum())
    sim_ac = float((a * c).sum())
    assert sim_ab > sim_ac, f"expected similar > unrelated, got {sim_ab} vs {sim_ac}"

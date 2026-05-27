"""Unit tests for Reciprocal Rank Fusion math."""
from __future__ import annotations

import math

from rag.retriever import RRF_K, rrf_fuse


def _score(rank: int, k: int = RRF_K) -> float:
    return 1.0 / (k + rank)


def test_single_ranking_preserves_order():
    out = rrf_fuse([["a", "b", "c"]])
    ids = [item for item, _ in out]
    assert ids == ["a", "b", "c"]


def test_item_in_both_rankings_beats_singleton_top():
    # 'x' is rank-1 in one list only;
    # 'y' is rank-2 in both lists → should outscore 'x' (2/(K+2) > 1/(K+1))
    out = dict(rrf_fuse([["x", "y"], ["z", "y"]]))
    assert out["y"] > out["x"]
    assert out["y"] > out["z"]


def test_score_matches_textbook_formula():
    out = dict(rrf_fuse([["a", "b"], ["b", "a"]]))
    assert math.isclose(out["a"], _score(1) + _score(2))
    assert math.isclose(out["b"], _score(2) + _score(1))
    # symmetric → equal
    assert math.isclose(out["a"], out["b"])


def test_empty_rankings_returns_empty():
    assert rrf_fuse([]) == []
    assert rrf_fuse([[], []]) == []


def test_missing_from_one_ranking_contributes_zero():
    # 'a' only in ranking 1 (rank 1); 'b' in both (ranks 2 and 1)
    out = dict(rrf_fuse([["a", "b"], ["b"]]))
    assert math.isclose(out["a"], _score(1))
    assert math.isclose(out["b"], _score(2) + _score(1))
    assert out["b"] > out["a"]


def test_custom_k_changes_smoothing():
    high_k = dict(rrf_fuse([["a", "b"]], k=1000))
    low_k = dict(rrf_fuse([["a", "b"]], k=1))
    # ratio a/b is closer to 1 with high k (more smoothing)
    high_ratio = high_k["a"] / high_k["b"]
    low_ratio = low_k["a"] / low_k["b"]
    assert high_ratio < low_ratio

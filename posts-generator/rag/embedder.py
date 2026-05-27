"""Sentence-transformers wrapper.

Lazy-imports the heavy `sentence_transformers` package so that downstream
code (e.g. the generator with BEOPS_RAG_ENABLED unset) doesn't pay the
~1s torch import on every invocation.
"""
from __future__ import annotations

from functools import lru_cache
from typing import Iterable

import numpy as np

from . import EMBEDDING_DIM, EMBEDDING_MODEL


@lru_cache(maxsize=1)
def _model():
    # imported lazily so unit tests / generator can avoid torch unless needed
    from sentence_transformers import SentenceTransformer

    return SentenceTransformer(EMBEDDING_MODEL)


def embed(texts: Iterable[str]) -> np.ndarray:
    """Return (n, EMBEDDING_DIM) float32, L2-normalized.

    L2-normalization makes cosine == dot product, which matches pgvector's
    `<=>` cosine operator behavior we use downstream.
    """
    texts = list(texts)
    if not texts:
        return np.zeros((0, EMBEDDING_DIM), dtype=np.float32)
    vecs = _model().encode(
        texts,
        normalize_embeddings=True,
        convert_to_numpy=True,
        show_progress_bar=False,
    ).astype(np.float32)
    assert vecs.shape[1] == EMBEDDING_DIM, (
        f"embedder dim drift: got {vecs.shape[1]}, want {EMBEDDING_DIM}"
    )
    return vecs


def embed_one(text: str) -> np.ndarray:
    return embed([text])[0]

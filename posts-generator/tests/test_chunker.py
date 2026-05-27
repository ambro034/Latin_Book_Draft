"""Unit tests for the chunker."""
from __future__ import annotations

from rag.chunker import (
    Chunk,
    approx_tokens,
    body_hash,
    chunk_markdown,
    parse_front_matter,
    strip_front_matter,
)


SAMPLE = """---
title: "Hello World"
date: 2025-01-01
category: devops
excerpt: >
  A test post about
  many things.
---

This is the lead paragraph. It introduces the topic in plain language.

This is the second paragraph. It elaborates further.

## First Section

Content of first section, paragraph one.

Content of first section, paragraph two.

## Second Section

Content of second section.
"""


def test_strip_front_matter_removes_block():
    body = strip_front_matter(SAMPLE)
    assert body.startswith("This is the lead paragraph.")
    assert "title:" not in body.splitlines()[0]


def test_strip_front_matter_noop_when_absent():
    assert strip_front_matter("no frontmatter here").startswith("no frontmatter")


def test_parse_front_matter_basics():
    fm, body = parse_front_matter(SAMPLE)
    assert fm["title"] == "Hello World"
    assert fm["date"] == "2025-01-01"
    assert fm["category"] == "devops"
    assert "many things" in fm["excerpt"]
    assert body.lstrip().startswith("This is the lead paragraph.")


def test_chunk_markdown_returns_ordered_chunks():
    chunks = chunk_markdown(SAMPLE, target_tokens=50, overlap_tokens=10)
    assert len(chunks) >= 2
    assert [c.ord for c in chunks] == list(range(len(chunks)))
    assert all(isinstance(c, Chunk) for c in chunks)
    # H2 headings preserved
    joined = "\n".join(c.text for c in chunks)
    assert "## First Section" in joined
    assert "## Second Section" in joined


def test_chunker_is_deterministic():
    a = chunk_markdown(SAMPLE)
    b = chunk_markdown(SAMPLE)
    assert [(c.ord, c.text) for c in a] == [(c.ord, c.text) for c in b]


def test_chunker_respects_target_size():
    # large doc with many small paragraphs
    body = "\n\n".join(f"Paragraph number {i} with some words." for i in range(60))
    md = "---\ntitle: x\n---\n\n" + body
    chunks = chunk_markdown(md, target_tokens=80, overlap_tokens=15)
    assert len(chunks) >= 3
    for c in chunks:
        # allow modest overshoot since we pack on paragraph boundaries
        assert approx_tokens(c.text) <= 200


def test_chunker_handles_no_h2():
    md = "---\ntitle: x\n---\n\nJust one paragraph here.\n\nAnd another."
    chunks = chunk_markdown(md, target_tokens=200, overlap_tokens=20)
    assert len(chunks) == 1
    assert "Just one paragraph" in chunks[0].text


def test_chunker_handles_empty_body():
    md = "---\ntitle: x\n---\n"
    assert chunk_markdown(md) == []


def test_body_hash_is_stable_and_frontmatter_invariant():
    other = SAMPLE.replace('title: "Hello World"', 'title: "Different Title"')
    assert body_hash(SAMPLE) == body_hash(other), (
        "body_hash must ignore front matter so metadata-only edits don't reindex"
    )
    edited = SAMPLE + "\n\nNew paragraph!"
    assert body_hash(SAMPLE) != body_hash(edited)

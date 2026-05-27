"""Markdown → chunks.

Strategy:
  1. Strip YAML front matter.
  2. Split on H2 (`## `) boundaries to keep semantic units intact.
  3. Within each section, pack paragraphs into windows of ~target_tokens
     tokens, with ~overlap_tokens of overlap between adjacent windows.

Token counting uses a tiny whitespace-based heuristic that is *good enough*
for fixed-budget chunking — no tokenizer dependency.
"""
from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from typing import Iterator

_FRONT_MATTER_RE = re.compile(r"^---\s*\n.*?\n---\s*\n?", re.DOTALL)
_H2_RE = re.compile(r"^##\s+", re.MULTILINE)


@dataclass(frozen=True)
class Chunk:
    ord: int
    text: str


def strip_front_matter(text: str) -> str:
    return _FRONT_MATTER_RE.sub("", text, count=1).lstrip()


def approx_tokens(text: str) -> int:
    """Rough token count: ~1 token per 0.75 words. Whitespace-split is fine
    here because we only need a *budget* signal, not exact tokenization."""
    return max(1, int(len(text.split()) / 0.75))


def _split_h2(body: str) -> list[str]:
    """Split markdown into H2-bounded sections, preserving the heading."""
    parts: list[str] = []
    last = 0
    matches = list(_H2_RE.finditer(body))
    if not matches:
        return [body] if body.strip() else []
    if matches[0].start() > 0:
        head = body[: matches[0].start()].strip()
        if head:
            parts.append(head)
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(body)
        section = body[m.start() : end].strip()
        if section:
            parts.append(section)
    return parts


def _pack_paragraphs(
    text: str, target_tokens: int, overlap_tokens: int
) -> list[str]:
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    if not paragraphs:
        return []

    windows: list[str] = []
    buf: list[str] = []
    buf_tokens = 0

    for p in paragraphs:
        pt = approx_tokens(p)
        if buf and buf_tokens + pt > target_tokens:
            windows.append("\n\n".join(buf))
            # build overlap from tail of previous buffer
            overlap_buf: list[str] = []
            o_tokens = 0
            for prev in reversed(buf):
                prev_t = approx_tokens(prev)
                if o_tokens + prev_t > overlap_tokens:
                    break
                overlap_buf.insert(0, prev)
                o_tokens += prev_t
            buf = list(overlap_buf)
            buf_tokens = o_tokens
        buf.append(p)
        buf_tokens += pt

    if buf:
        windows.append("\n\n".join(buf))
    return windows


def chunk_markdown(
    markdown: str,
    target_tokens: int = 500,
    overlap_tokens: int = 80,
) -> list[Chunk]:
    """Yield deterministically ordered Chunks for one post body."""
    body = strip_front_matter(markdown)
    sections = _split_h2(body)
    out: list[str] = []
    for sec in sections:
        out.extend(_pack_paragraphs(sec, target_tokens, overlap_tokens))
    return [Chunk(ord=i, text=t) for i, t in enumerate(out)]


def body_hash(markdown: str) -> str:
    """Stable hash of the post body (post-frontmatter). Used by indexer
    to skip unchanged posts."""
    body = strip_front_matter(markdown).encode("utf-8")
    return hashlib.sha256(body).hexdigest()


# ----------------- Markdown front-matter parser (shared with indexer) -----

_FM_FULL_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", re.DOTALL)


def parse_front_matter(text: str) -> tuple[dict[str, str], str]:
    """Minimal Jekyll-front-matter parser. Supports scalar values and
    `>`/`|` folded blocks. Lists/nested maps are returned as raw strings."""
    m = _FM_FULL_RE.match(text)
    if not m:
        return {}, text
    raw_fm, body = m.group(1), m.group(2)

    data: dict[str, str] = {}
    current_key: str | None = None
    block: list[str] = []
    block_indent: int | None = None

    def flush() -> None:
        nonlocal current_key, block, block_indent
        if current_key is not None:
            data[current_key] = " ".join(
                ln.strip() for ln in block if ln.strip()
            )
        current_key, block, block_indent = None, [], None

    for line in raw_fm.splitlines():
        if not line.strip():
            continue
        if current_key is not None and (line.startswith(" ") or line.startswith("\t")):
            indent = len(line) - len(line.lstrip())
            if block_indent is None or indent >= block_indent:
                if block_indent is None:
                    block_indent = indent
                block.append(line)
                continue
        flush()
        kv = re.match(r"^([A-Za-z0-9_\-]+)\s*:\s*(.*)$", line)
        if not kv:
            continue
        key, value = kv.group(1), kv.group(2).strip()
        if value in (">", "|", ">-", "|-"):
            current_key = key
        else:
            if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
                value = value[1:-1]
            data[key] = value
    flush()
    return data, body

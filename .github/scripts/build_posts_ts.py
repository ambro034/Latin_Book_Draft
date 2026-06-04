#!/usr/bin/env python3
"""
Build src/data/posts.ts for beops-main-site from BeOps _posts/*.md.

Reads every Markdown post under _posts/, extracts the YAML front matter
(title, date, category) and the body, computes a reading time from the
body word count (~200 wpm), maps Jekyll categories to the writing-page
filter categories, and emits a TypeScript module identical in shape to
the hand-maintained one.

Usage:
    python build_posts_ts.py <posts_dir> <output_ts_path>
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

JEKYLL_URL_BASE = "https://neverthesame.github.io/BeOps"

# Jekyll category -> /writing filter category
CATEGORY_MAP = {
    "devops": "devops",
    "k8s": "kubernetes",
    "ai": "ai",
    "job-interviews": "interviews",
    "sre": "devops",
    "data": "data",
}

FRONT_MATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", re.DOTALL)


def parse_front_matter(text: str) -> tuple[dict, str]:
    m = FRONT_MATTER_RE.match(text)
    if not m:
        return {}, text
    raw_fm, body = m.group(1), m.group(2)

    data: dict[str, str] = {}
    current_key: str | None = None
    block_lines: list[str] = []
    block_indent: int | None = None

    def flush_block() -> None:
        nonlocal current_key, block_lines, block_indent
        if current_key is not None:
            data[current_key] = " ".join(
                ln.strip() for ln in block_lines if ln.strip()
            )
        current_key = None
        block_lines = []
        block_indent = None

    for line in raw_fm.splitlines():
        if not line.strip():
            continue
        # continuation of a folded/literal block
        if current_key is not None and (line.startswith(" ") or line.startswith("\t")):
            indent = len(line) - len(line.lstrip())
            if block_indent is None or indent >= block_indent:
                if block_indent is None:
                    block_indent = indent
                block_lines.append(line)
                continue

        flush_block()

        m2 = re.match(r"^([A-Za-z0-9_\-]+)\s*:\s*(.*)$", line)
        if not m2:
            continue
        key, value = m2.group(1), m2.group(2).strip()
        if value in (">", "|", ">-", "|-"):
            current_key = key
            block_lines = []
            block_indent = None
        else:
            # strip optional surrounding quotes
            if len(value) >= 2 and value[0] == value[-1] and value[0] in ('"', "'"):
                value = value[1:-1]
            data[key] = value

    flush_block()
    return data, body


def word_count(body: str) -> int:
    # strip code fences and inline code to avoid skewing
    body = re.sub(r"```.*?```", " ", body, flags=re.DOTALL)
    body = re.sub(r"`[^`]*`", " ", body)
    # strip markdown link/image syntax, keep visible text
    body = re.sub(r"!?\[([^\]]*)\]\([^)]*\)", r"\1", body)
    # drop html tags
    body = re.sub(r"<[^>]+>", " ", body)
    words = re.findall(r"\b[\w'’-]+\b", body)
    return len(words)


def reading_time(body: str) -> str:
    wpm = 200
    minutes = max(1, round(word_count(body) / wpm))
    return f"{minutes} min"


def ts_string(s: str) -> str:
    return "'" + s.replace("\\", "\\\\").replace("'", "\\'") + "'"


def build(posts_dir: Path) -> str:
    entries: list[dict] = []
    for md in sorted(posts_dir.glob("*.md")):
        text = md.read_text(encoding="utf-8")
        fm, body = parse_front_matter(text)
        title = fm.get("title", "").strip()
        date = fm.get("date", "").strip()
        category = fm.get("category", "").strip()
        if not (title and date and category):
            print(f"skip (missing fm): {md.name}", file=sys.stderr)
            continue

        mapped = CATEGORY_MAP.get(category)
        if mapped is None:
            print(f"skip (unmapped category {category!r}): {md.name}", file=sys.stderr)
            continue

        # filename without .md is the Jekyll slug-with-date
        slug = md.stem
        url = f"{JEKYLL_URL_BASE}/{category}/{slug}.html"

        entries.append(
            {
                "title": title.lower(),
                "date": date,
                "category": mapped,
                "url": url,
                "read": reading_time(body),
            }
        )

    # newest first
    entries.sort(key=lambda e: e["date"], reverse=True)

    lines = [
        "export interface Post {",
        "  title: string;",
        "  date: string;",
        "  category: 'devops' | 'kubernetes' | 'ai' | 'interviews' | 'data';",
        "  url: string;",
        "  read?: string;",
        "}",
        "",
        "export const POSTS: Post[] = [",
    ]
    for i, e in enumerate(entries):
        lines.append("  {")
        lines.append(f"    title: {ts_string(e['title'])},")
        lines.append(f"    date: {ts_string(e['date'])},")
        lines.append(f"    category: {ts_string(e['category'])},")
        lines.append(f"    url: {ts_string(e['url'])},")
        lines.append(f"    read: {ts_string(e['read'])}")
        lines.append("  }" + ("," if i < len(entries) - 1 else ""))
    lines.append("];")
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: build_posts_ts.py <posts_dir> <output_ts>", file=sys.stderr)
        return 2
    posts_dir = Path(sys.argv[1])
    out_path = Path(sys.argv[2])
    ts = build(posts_dir)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(ts, encoding="utf-8")
    print(f"wrote {out_path} ({ts.count(chr(10))} lines)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Unit tests for the Substack drafter (no DB, no network, no python-substack)."""
from __future__ import annotations

from pathlib import Path

import substack_drafter
import llm_openrouter


def test_split_subtitle_extracts_first_line():
    sub, body = substack_drafter._split_subtitle(
        "SUBTITLE: a short hook\n\n## Heading\n\nbody text"
    )
    assert sub == "a short hook"
    assert body.startswith("## Heading")
    assert "SUBTITLE" not in body


def test_split_subtitle_missing_is_graceful():
    sub, body = substack_drafter._split_subtitle("## Heading\n\nbody")
    assert sub == ""
    assert body == "## Heading\n\nbody"


def test_related_context_no_db_is_empty(monkeypatch):
    for var in ("NEON_DATABASE_URL", "DATABASE_URL", "BEOPS_TEST_DATABASE_URL"):
        monkeypatch.delenv(var, raising=False)
    assert substack_drafter._related_context("seed", "slug") == ""


def test_shorten_post_parses_and_guarantees_backlink(monkeypatch):
    captured = {}

    def fake_chat(messages, **kwargs):
        captured["messages"] = messages
        # Model output WITHOUT the canonical link, to exercise the fallback.
        return "SUBTITLE: hooky line\n\n## Why\n\nShort but technical body."

    monkeypatch.setattr(llm_openrouter, "chat", fake_chat)
    for var in ("NEON_DATABASE_URL", "DATABASE_URL", "BEOPS_TEST_DATABASE_URL"):
        monkeypatch.delenv(var, raising=False)

    post = {
        "slug": "2026-06-03-foo",
        "title": "My Post",
        "category": "ai",
        "url": "https://neverthesame.github.io/BeOps/ai/2026-06-03-foo.html",
        "body": "A long technical article body.",
    }
    subtitle, body = substack_drafter.shorten_post(post)
    assert subtitle == "hooky line"
    assert "Short but technical body." in body
    # Backlink was missing from the model output, so it must be appended.
    assert post["url"] in body
    # The system prompt must forbid em-dashes and tables.
    system = captured["messages"][0]["content"]
    assert "em-dash" in system.lower()
    assert "table" in system.lower()


def test_normalize_pub_url():
    assert substack_drafter._normalize_pub_url("") == "https://beops.substack.com"
    assert substack_drafter._normalize_pub_url(None) == "https://beops.substack.com"
    assert substack_drafter._normalize_pub_url("beops.substack.com") == "https://beops.substack.com"
    assert substack_drafter._normalize_pub_url("https://x.substack.com/") == "https://x.substack.com"


def test_warn_unsupported_markdown_flags_table(capsys):
    substack_drafter._warn_unsupported_markdown("| a | b |\n| - | - |\n| 1 | 2 |")
    err = capsys.readouterr().err
    assert "table" in err.lower()


def test_load_post_reused(tmp_path: Path):
    md = tmp_path / "2026-06-03-foo.md"
    md.write_text(
        '---\ntitle: "My Post"\ncategory: ai\ndate: 2026-06-03\n---\n\nbody here\n',
        encoding="utf-8",
    )
    post = substack_drafter.load_post(md)
    assert post["title"] == "My Post"
    assert post["url"] == "https://neverthesame.github.io/BeOps/ai/2026-06-03-foo.html"

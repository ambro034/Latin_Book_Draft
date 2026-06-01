"""Unit tests for the Telegram style pipeline (no DB, no network)."""
from __future__ import annotations

import io
import json
from pathlib import Path

import scrape_telegram
import telegram_drafter
import llm_openrouter
from rag import style


SAMPLE_PAGE = """
<div class="tgme_widget_message_wrap">
  <div class="tgme_widget_message" data-post="beops_it/42">
    <div class="tgme_widget_message_text">hello <b>world</b><br/>second line</div>
    <div class="tgme_widget_message_footer">
      <time datetime="2025-08-21T22:59:20+00:00"></time>
    </div>
  </div>
</div>
<div class="tgme_widget_message_wrap">
  <div class="tgme_widget_message" data-post="beops_it/43">
    <div class="tgme_widget_message_text">just text</div>
    <div class="tgme_widget_message_footer">
      <time datetime="2025-08-22T00:00:00+00:00"></time>
    </div>
  </div>
</div>
"""


def test_parse_page_extracts_id_text_date():
    msgs = scrape_telegram._parse_page(SAMPLE_PAGE, "beops_it")
    assert set(msgs) == {42, 43}
    assert msgs[42]["text"] == "hello world\nsecond line"
    assert msgs[42]["date"] == "2025-08-21T22:59:20+00:00"


def test_load_corpus_drops_short_and_empty(tmp_path: Path):
    p = tmp_path / "c.jsonl"
    p.write_text(
        "\n".join(
            [
                json.dumps({"id": 1, "text": "Channel created"}),  # < 20 chars
                json.dumps({"id": 2, "text": ""}),  # empty
                json.dumps({"id": 3, "text": "x" * 50, "date": "2025-01-01T00:00:00+00:00"}),
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    rows = style.load_corpus(p)
    assert [r["id"] for r in rows] == [3]
    assert rows[0]["date"] == "2025-01-01T00:00:00+00:00"


def test_detect_language():
    assert telegram_drafter.detect_language("привет это русский текст") == "russian"
    assert telegram_drafter.detect_language("this is english text") == "english"


def test_blog_url_and_load_post(tmp_path: Path):
    md = tmp_path / "2026-05-28-foo.md"
    md.write_text(
        '---\ntitle: "My Post"\ncategory: ai\ndate: 2026-05-28\n---\n\nbody text here\n',
        encoding="utf-8",
    )
    post = telegram_drafter.load_post(md)
    assert post["title"] == "My Post"
    assert post["category"] == "ai"
    assert post["slug"] == "2026-05-28-foo"
    assert post["url"] == "https://neverthesame.github.io/BeOps/ai/2026-05-28-foo.html"
    assert "body text here" in post["body"]


def test_compose_message_has_header_and_draft():
    post = {"title": "My Post"}
    msg = telegram_drafter.compose_message(post, "draft body")
    assert "DRAFT for @beops_it" in msg
    assert "My Post" in msg
    assert "draft body" in msg


def test_openrouter_chat_parses_and_sends(monkeypatch):
    captured = {}

    class _Resp:
        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

        def read(self):
            return json.dumps(
                {"choices": [{"message": {"content": "  drafted post  "}}]}
            ).encode("utf-8")

    def fake_urlopen(req, timeout=0):
        captured["url"] = req.full_url
        captured["body"] = json.loads(req.data.decode("utf-8"))
        captured["auth"] = req.headers.get("Authorization")
        return _Resp()

    monkeypatch.setattr(llm_openrouter.urllib.request, "urlopen", fake_urlopen)
    out = llm_openrouter.chat(
        [{"role": "user", "content": "hi"}],
        model="test/model",
        api_key="sk-test",
    )
    assert out == "drafted post"
    assert captured["url"] == "https://openrouter.ai/api/v1/chat/completions"
    assert captured["body"]["model"] == "test/model"
    assert captured["auth"] == "Bearer sk-test"


def test_openrouter_empty_content_raises(monkeypatch):
    class _Resp:
        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

        def read(self):
            return json.dumps({"choices": [{"message": {"content": "   "}}]}).encode("utf-8")

    monkeypatch.setattr(
        llm_openrouter.urllib.request, "urlopen", lambda req, timeout=0: _Resp()
    )
    import pytest

    with pytest.raises(RuntimeError):
        llm_openrouter.chat(
            [{"role": "user", "content": "hi"}], api_key="sk-test", retries=1
        )


def test_send_telegram_posts_to_bot_api(monkeypatch):
    captured = {}

    class _Resp:
        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

        def read(self):
            return json.dumps({"ok": True, "result": {"message_id": 1}}).encode("utf-8")

    def fake_urlopen(req, timeout=0):
        captured["url"] = req.full_url
        captured["data"] = req.data.decode("utf-8")
        return _Resp()

    monkeypatch.setattr(telegram_drafter.urllib.request, "urlopen", fake_urlopen)
    resp = telegram_drafter.send_telegram("draft text", token="T", chat_id="123")
    assert resp["ok"] is True
    assert "/botT/sendMessage" in captured["url"]
    assert "chat_id=123" in captured["data"]

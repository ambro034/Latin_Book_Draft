"""Draft a Telegram channel post in the author's voice from a new blog post,
and DM it to the author for manual review/posting.

Pipeline:
  1. parse a Jekyll `_posts/*.md` (front matter + body)
  2. retrieve the author's own most-similar Telegram posts as voice exemplars
     (rag.style — a SEPARATE corpus from the blog RAG)
  3. retrieve related prior BLOG posts (the blog RAG corpus) so the draft can
     chain to earlier writing by linking one relevant earlier post
  4. ask an OpenRouter model to write a short Telegram post in that voice,
     ALWAYS in Russian (@beops_it is a Russian-language channel)
  5. send the draft to the author via the Telegram bot (sendMessage)

LLM: OpenRouter (OPENROUTER_API_KEY). Delivery: TELEGRAM_BOT_TOKEN +
TELEGRAM_CHAT_ID. Style retrieval needs NEON_DATABASE_URL.

CLI:
    python telegram_drafter.py path/to/_posts/2026-05-28-foo.md [--dry-run] [--no-send]
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

import llm_openrouter
from rag.chunker import parse_front_matter, strip_front_matter

JEKYLL_URL_BASE = "https://neverthesame.github.io/BeOps"

# Self-contained defaults so the CI workflow works without the (gitignored)
# prompts.json. If prompts.json is present locally, its values override these.
_DEFAULT_TELEGRAM_PROMPT_RU = (
    "Ты ведёшь авторский Telegram-канал @beops_it про IT, DevOps, SRE и AI. "
    "Тебе дают новый пост из блога. Напиши КОРОТКИЙ пост для Telegram-канала, который:\n"
    "1. Написан строго в стиле автора - изучи приложенные примеры его постов и "
    "имитируй тон, лексику, длину предложений, использование эмодзи и строчных букв.\n"
    "2. Цепляет с первой строки, передаёт суть статьи без пересказа целиком, "
    "вызывает желание перейти и прочитать.\n"
    "3. Длина - примерно 400-900 символов. Не используй заголовки в стиле markdown.\n"
    "4. В конце добавь ссылку на статью отдельной строкой.\n"
    "5. Пиши на русском языке.\n"
    "Важно: имитируй СТИЛЬ автора, а не копируй содержание примеров. "
    "Верни только текст поста, без пояснений."
)
_DEFAULT_TELEGRAM_PROMPT_EN = (
    "You run the author's Telegram channel @beops_it about IT, DevOps, SRE and AI. "
    "You are given a new blog post. Write a SHORT Telegram channel post that:\n"
    "1. Is strictly in the author's voice - study the provided examples of their "
    "posts and imitate the tone, vocabulary, sentence length, emoji use and "
    "lowercase habits.\n"
    "2. Hooks from the first line, conveys the gist without retelling the whole "
    "article, and makes the reader want to click through.\n"
    "3. Is roughly 400-900 characters. Do not use markdown headings.\n"
    "4. Ends with the article link on its own line.\n"
    "5. Is written in English.\n"
    "Important: imitate the author's STYLE, do not copy the content of the "
    "examples. Return only the post text, no explanations."
)


def detect_language(text: str) -> str:
    cyr = len(re.findall(r"[а-яё]", text.lower()))
    lat = len(re.findall(r"[a-z]", text.lower()))
    return "russian" if cyr > lat else "english"


def blog_url(category: str, slug: str) -> str:
    return f"{JEKYLL_URL_BASE}/{category}/{slug}.html"


def load_post(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    fm, _ = parse_front_matter(text)
    title = (fm.get("title") or "").strip()
    category = (fm.get("category") or "").strip()
    slug = path.stem
    body = strip_front_matter(text)
    return {
        "slug": slug,
        "title": title,
        "category": category,
        "url": blog_url(category, slug) if category else "",
        "body": body,
    }


def _load_prompts() -> dict:
    """Optional local prompt overrides. prompts.json is gitignored, so this
    returns {} in CI — the built-in defaults are used instead."""
    here = Path(__file__).resolve().parent
    f = here / "prompts.json"
    if not f.exists():
        return {}
    try:
        return json.loads(f.read_text(encoding="utf-8"))
    except Exception:  # pragma: no cover
        return {}


def _style_block(seed: str, k: int = 6) -> str:
    """Best-effort voice exemplars. Empty string if no DB / no hits."""
    if not (
        os.getenv("NEON_DATABASE_URL")
        or os.getenv("DATABASE_URL")
        or os.getenv("BEOPS_TEST_DATABASE_URL")
    ):
        return ""
    try:
        from rag.db import connect
        from rag.style import examples_block
    except Exception as e:  # pragma: no cover
        print(f"⚠️ style RAG not importable: {e}", file=sys.stderr)
        return ""
    try:
        with connect() as conn:
            return examples_block(conn, seed, k=k)
    except Exception as e:  # pragma: no cover
        print(f"⚠️ style retrieval failed (continuing without it): {e}", file=sys.stderr)
        return ""


def _related_block(seed: str, exclude_slug: str, k: int = 6) -> str:
    """Related prior BLOG posts (the blog RAG corpus, SEPARATE from the Telegram
    style corpus) so the draft can chain to the author's earlier writing.
    Returns a Russian, prompt-ready block, or empty string if no DB / no hits."""
    if not (
        os.getenv("NEON_DATABASE_URL")
        or os.getenv("DATABASE_URL")
        or os.getenv("BEOPS_TEST_DATABASE_URL")
    ):
        return ""
    try:
        from rag.db import connect
        from rag.retriever import search
    except Exception as e:  # pragma: no cover
        print(f"⚠️ blog RAG not importable: {e}", file=sys.stderr)
        return ""
    try:
        with connect() as conn:
            hits = search(conn, seed, k=k + 3)
            slugs: list[str] = []
            for h in hits:
                if h.slug == exclude_slug or h.slug in slugs:
                    continue
                slugs.append(h.slug)
            slugs = slugs[:k]
            if not slugs:
                return ""
            with conn.cursor() as cur:
                cur.execute(
                    "select slug, url, title from posts where slug = any(%s)", (slugs,)
                )
                meta = {s: (u, t) for s, u, t in cur.fetchall()}
    except Exception as e:  # pragma: no cover
        print(f"⚠️ related-posts retrieval failed (continuing without it): {e}", file=sys.stderr)
        return ""

    lines = [f"- {meta[s][1]}: {meta[s][0]}" for s in slugs if s in meta]
    if not lines:
        return ""
    header = (
        "РОДСТВЕННЫЕ ПРОШЛЫЕ ПОСТЫ автора (для связки с прошлыми материалами). "
        "Если один из них действительно близок по теме, добавь в конце поста "
        "отдельной строкой короткую отсылку со ссылкой на него "
        "(например: «Ранее писал об этом: <ссылка>»). Максимум одна такая отсылка, "
        "и только если она по делу. Не пересказывай их содержание."
    )
    return header + "\n" + "\n".join(lines)


def draft_post(post: dict, *, k: int = 6, model: str | None = None) -> str:
    """Generate the Telegram post text in the author's voice."""
    prompts = _load_prompts()
    seed = f"{post['title']}\n\n{post['body'][:1500]}"
    # @beops_it is a Russian-language channel: always draft in Russian,
    # regardless of the (usually English) blog post language.
    language = "russian"

    key = "telegram_style_prompt"
    default = _DEFAULT_TELEGRAM_PROMPT_RU
    system_message = prompts.get("additional_guidelines", "") + prompts.get(key, default)

    style_block = _style_block(seed, k=k)
    if style_block:
        system_message = system_message + "\n\n" + style_block

    related_block = _related_block(seed, exclude_slug=post["slug"], k=k)
    if related_block:
        system_message = system_message + "\n\n" + related_block

    if language == "russian":
        user_message = (
            "Вот мой новый пост в блоге. Напиши короткий пост для моего "
            "Telegram-канала в моём стиле, который заинтересует подписчиков и "
            "ведёт на статью. В конце добавь ссылку.\n\n"
            f"ЗАГОЛОВОК: {post['title']}\nССЫЛКА: {post['url']}\n\n"
            f"ТЕКСТ СТАТЬИ:\n{post['body'][:6000]}"
        )
    else:
        user_message = (
            "Here is my new blog post. Write a short Telegram channel post in "
            "my voice that hooks subscribers and links to the article. End with "
            "the link.\n\n"
            f"TITLE: {post['title']}\nURL: {post['url']}\n\n"
            f"ARTICLE:\n{post['body'][:6000]}"
        )

    return llm_openrouter.chat(
        [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message},
        ],
        model=model,
        max_tokens=900,
        temperature=0.85,
    )


def send_telegram(text: str, *, token: str | None = None, chat_id: str | None = None) -> dict:
    token = token or os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = chat_id or os.getenv("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        raise RuntimeError("TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID not set")
    data = urllib.parse.urlencode(
        {"chat_id": chat_id, "text": text, "disable_web_page_preview": "false"}
    ).encode("utf-8")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    req = urllib.request.Request(url, data=data)
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def compose_message(post: dict, draft: str) -> str:
    return (
        "📝 DRAFT for @beops_it — review & post manually\n"
        f"(from blog post: {post['title']})\n"
        "────────────────────\n"
        f"{draft}"
    )


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Draft a Telegram post from a blog post")
    p.add_argument("post", help="path to a _posts/*.md file")
    p.add_argument("-k", type=int, default=6, help="number of voice exemplars")
    p.add_argument("--model", default=None, help="OpenRouter model override")
    p.add_argument("--no-send", action="store_true", help="print only, do not DM")
    p.add_argument("--dry-run", action="store_true", help="skip LLM + Telegram (CI smoke)")
    args = p.parse_args(argv)

    post = load_post(Path(args.post))
    if not post["title"]:
        print(f"⚠️ {args.post}: no title in front matter; skipping", file=sys.stderr)
        return 0

    if args.dry_run:
        print(f"[dry-run] would draft Telegram post for: {post['title']} -> {post['url']}")
        return 0

    draft = draft_post(post, k=args.k, model=args.model)
    message = compose_message(post, draft)

    if args.no_send:
        print(message)
        return 0

    resp = send_telegram(message)
    if not resp.get("ok"):
        print(f"❌ Telegram send failed: {resp}", file=sys.stderr)
        return 1
    print(f"✅ DM sent for: {post['title']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

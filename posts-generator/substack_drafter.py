"""Draft a SHORTER Substack post from a new blog post and create it as a DRAFT
(never auto-published) on the author's Substack for manual review.

Pipeline:
  1. parse a Jekyll `_posts/*.md` (front matter + body)
  2. (best-effort) pull related prior BeOps posts from the blog RAG for coherence
  3. ask an OpenRouter model to rewrite it SHORTER in English, keeping ALL the
     technical detail, and ending with a link back to the canonical BeOps post
  4. create a Substack DRAFT via the unofficial python-substack API

Substack has no official API, so this uses the reverse-engineered client and
authenticates as the author. Auth (pick one):
  * SUBSTACK_COOKIES_STRING  (preferred; copy the cookie header from a logged-in
    browser session, e.g. "substack.sid=...; ...")
  * SUBSTACK_EMAIL + SUBSTACK_PASSWORD
plus SUBSTACK_PUBLICATION_URL (default https://beops.substack.com).
LLM: OPENROUTER_API_KEY (+ OPENROUTER_MODEL). RAG grounding: NEON_DATABASE_URL.

House style: never use em-dashes; the prompt enforces this.

CLI:
    python substack_drafter.py path/to/_posts/2026-06-03-foo.md \
        [--dry-run] [--no-send] [--force] [-k 6] [--model MODEL]
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

import llm_openrouter
from telegram_drafter import load_post  # reuse the same front-matter parser

# Convenience for LOCAL runs: auto-load a gitignored posts-generator/.env so the
# operator pastes NEON_DATABASE_URL / OPENROUTER_API_KEY / SUBSTACK_* only once.
# Real env vars (e.g. in CI) always win. No-op if python-dotenv isn't installed.
try:
    from dotenv import load_dotenv

    load_dotenv(Path(__file__).resolve().parent / ".env", override=False)
except Exception:
    pass

DEFAULT_PUBLICATION_URL = "https://beops.substack.com"

# Source body is sent to the model whole so no technical detail is lost. This
# cap is a safety bound only; we WARN loudly (never silently truncate) if a post
# is ever larger, so the operator knows to switch to a chunked rewrite.
MAX_BODY_CHARS = 40000

_SYSTEM_PROMPT = (
    "You are the author of the BeOps engineering blog. Rewrite the given blog "
    "post as a SHORTER post for the author's Substack newsletter.\n"
    "Hard rules:\n"
    "1. Keep ALL the technical substance: code blocks, shell commands, config, "
    "numbers, API names, and any before/after comparisons. Do NOT drop technical "
    "detail. This is the whole point.\n"
    "2. Cut only fluff: long intros, throat-clearing, and repetition. Aim for "
    "roughly half the original length.\n"
    "3. Keep the author's voice: practical, direct, engineering tone.\n"
    "4. Output clean Markdown that Substack understands: '##' headings, "
    "paragraphs, **bold**, *italic*, `inline code`, fenced ``` code blocks, "
    "bullet and numbered lists, blockquotes, and [text](url) links.\n"
    "5. DO NOT use Markdown tables. Substack ignores them. Convert any table or "
    "before/after comparison into labeled bullet lists or a fenced code block.\n"
    "6. DO NOT repeat the post title as a heading. Substack stores the title "
    "separately.\n"
    "7. NEVER use em-dashes or en-dashes. Use commas, periods, colons, or "
    "parentheses instead.\n"
    "8. End with a short final paragraph linking back to the canonical version, "
    "exactly in the form: Originally published on BeOps: [canonical version](<URL>)\n"
    "Output format: the FIRST line must be 'SUBTITLE: <one short subtitle line>'. "
    "Then a blank line. Then the Markdown body. Return nothing else."
)


def _related_context(seed: str, exclude_slug: str, k: int = 6) -> str:
    """Best-effort 'related prior BeOps posts' block from the blog RAG, for
    terminology coherence and optional cross-linking. '' if no DB / no hits."""
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
        print(f"⚠️ related-context retrieval failed (continuing without it): {e}", file=sys.stderr)
        return ""

    lines = [f"- [{meta[s][1]}]({meta[s][0]})" for s in slugs if s in meta]
    if not lines:
        return ""
    header = (
        "RELATED PRIOR BeOps POSTS (for coherence). The ONLY required link is the "
        "canonical backlink. You MAY link at most one of these if it is genuinely "
        "relevant, but do not force it and do not rehash them:"
    )
    return header + "\n" + "\n".join(lines)


def _clip_body(body: str) -> str:
    """Pass the full post to the model. WARN (do not silently drop) if a post is
    ever bigger than the safety cap, so technical detail loss is never silent."""
    if len(body) > MAX_BODY_CHARS:
        print(
            f"⚠️ post body is {len(body)} chars (> {MAX_BODY_CHARS}); the tail will "
            "be clipped for the LLM. Switch to a chunked rewrite to keep all detail.",
            file=sys.stderr,
        )
        return body[:MAX_BODY_CHARS]
    return body


def _warn_unsupported_markdown(body: str) -> None:
    """Substack's from_markdown drops Markdown tables and ignores raw HTML / Liquid.
    The prompt forbids these, but warn if the model emitted them anyway so the
    operator can spot dropped technical content during review."""
    import re

    if re.search(r"^\s*\|.*\|\s*$", body, flags=re.MULTILINE):
        print("⚠️ draft contains a Markdown table; Substack will drop it. Review the draft.", file=sys.stderr)
    if re.search(r"\{%.*?%\}|\{\{.*?\}\}", body):
        print("⚠️ draft contains Liquid tags; these will not render on Substack.", file=sys.stderr)


def _split_subtitle(text: str) -> tuple[str, str]:
    """Pull the leading 'SUBTITLE: ...' line out of the model output."""
    stripped = text.lstrip()
    if stripped.upper().startswith("SUBTITLE:"):
        first, _, rest = stripped.partition("\n")
        subtitle = first.split(":", 1)[1].strip()
        return subtitle, rest.lstrip("\n")
    return "", text


def shorten_post(post: dict, *, k: int = 6, model: str | None = None) -> tuple[str, str]:
    """Return (subtitle, markdown_body) for the Substack draft."""
    seed = f"{post['title']}\n\n{post['body'][:1500]}"
    system_message = _SYSTEM_PROMPT

    related = _related_context(seed, exclude_slug=post["slug"], k=k)
    if related:
        system_message = system_message + "\n\n" + related

    user_message = (
        "Here is my blog post. Rewrite it shorter for Substack, keeping every "
        "technical detail, and end with the canonical backlink.\n\n"
        f"TITLE: {post['title']}\n"
        f"CANONICAL URL: {post['url']}\n\n"
        f"ARTICLE:\n{_clip_body(post['body'])}"
    )

    out = llm_openrouter.chat(
        [
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message},
        ],
        model=model,
        max_tokens=2400,
        temperature=0.6,
    )
    subtitle, body = _split_subtitle(out)
    _warn_unsupported_markdown(body)
    # Belt and braces: guarantee the canonical backlink is present as a link.
    if post["url"] and post["url"] not in body:
        body = body.rstrip() + (
            f"\n\nOriginally published on BeOps: [canonical version]({post['url']})\n"
        )
    return subtitle, body


def _normalize_pub_url(raw: str | None) -> str:
    """Normalize the publication URL: fall back to default on empty, add the
    https scheme if missing, and strip a trailing slash."""
    url = (raw or "").strip() or DEFAULT_PUBLICATION_URL
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    return url.rstrip("/")


def _normalize_cookies_string(raw: str) -> str:
    """Accept either a full cookie header (``substack.sid=s%3A...; other=...``)
    or a bare ``substack.sid`` value pasted without its name. The substack
    client splits each pair on ``=`` and silently drops pairs that have no
    name, so a bare value would send zero cookies and yield a 401. If no
    ``name=value`` pair is present, assume the whole string is the sid value
    and prefix it with ``substack.sid=``."""
    s = raw.strip()
    has_named_pair = any(
        "=" in part.strip() for part in s.split(";") if part.strip()
    )
    if not has_named_pair:
        return "substack.sid=" + s
    return s


def _make_api():
    """Build an authenticated Substack Api from env. Imported lazily so dry-run
    and unit tests never need the package installed."""
    from substack import Api

    pub = _normalize_pub_url(os.getenv("SUBSTACK_PUBLICATION_URL"))
    cookies = os.getenv("SUBSTACK_COOKIES_STRING")
    if cookies and cookies.strip():
        cookies = _normalize_cookies_string(cookies)
        return Api(cookies_string=cookies, publication_url=pub), pub
    email = os.getenv("SUBSTACK_EMAIL")
    password = os.getenv("SUBSTACK_PASSWORD")
    if email and password:
        return Api(email=email, password=password, publication_url=pub), pub
    raise RuntimeError(
        "Substack auth not set: provide SUBSTACK_COOKIES_STRING or "
        "SUBSTACK_EMAIL + SUBSTACK_PASSWORD"
    )


def _existing_draft_id(api, title: str) -> str | None:
    """Best-effort idempotency: find a recent draft with the same title so
    re-runs do not spam duplicate drafts."""
    try:
        drafts = api.get_drafts(limit=50) or []
    except Exception as e:  # pragma: no cover
        print(f"⚠️ could not list drafts (continuing): {e}", file=sys.stderr)
        return None
    for d in drafts:
        if (d.get("draft_title") or d.get("title")) == title:
            return str(d.get("id"))
    return None


def create_substack_draft(
    post: dict, subtitle: str, body: str, *, force: bool = False
) -> dict:
    """Create (or skip if it already exists) a Substack DRAFT. Never publishes."""
    from substack.post import Post

    api, pub = _make_api()
    title = post["title"]

    if not force:
        existing = _existing_draft_id(api, title)
        if existing:
            url = f"{pub}/publish/post/{existing}"
            print(f"↩️ draft already exists for {title!r}: {url} (use --force to add another)")
            return {"id": existing, "url": url, "skipped": True}

    user_id = api.get_user_id()
    sub_post = Post(title=title, subtitle=subtitle, user_id=user_id, audience="everyone")
    sub_post.from_markdown(body, api=api)
    draft = api.post_draft(sub_post.get_draft())

    draft_id = draft.get("id")
    url = f"{pub}/publish/post/{draft_id}" if draft_id else pub
    print(f"✅ Substack draft created for {title!r}: {url}")
    return {"id": draft_id, "url": url, "skipped": False}


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Draft a Substack post from a blog post")
    p.add_argument("post", help="path to a _posts/*.md file")
    p.add_argument("-k", type=int, default=6, help="number of related posts for grounding")
    p.add_argument("--model", default=None, help="OpenRouter model override")
    p.add_argument("--no-send", action="store_true", help="print the draft, do not touch Substack")
    p.add_argument("--dry-run", action="store_true", help="skip LLM + Substack (CI smoke)")
    p.add_argument("--force", action="store_true", help="create a draft even if one with the same title exists")
    args = p.parse_args(argv)

    post = load_post(Path(args.post))
    if not post["title"]:
        print(f"⚠️ {args.post}: no title in front matter; skipping", file=sys.stderr)
        return 0

    if args.dry_run:
        print(f"[dry-run] would draft Substack post for: {post['title']} -> {post['url']}")
        return 0

    subtitle, body = shorten_post(post, k=args.k, model=args.model)

    if args.no_send:
        print(f"SUBTITLE: {subtitle}\n\n{body}")
        return 0

    create_substack_draft(post, subtitle, body, force=args.force)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

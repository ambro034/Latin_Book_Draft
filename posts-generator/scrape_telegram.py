"""Scrape the public web preview of a Telegram channel into JSONL.

The public preview at https://t.me/s/<channel> renders the latest page of
posts as HTML. We paginate backwards with `?before=<message_id>` until no
new posts appear, then write one JSON object per post to stdout / a file.

No credentials required — only works for public channels.

Usage:
    python scrape_telegram.py [--channel beops_it] [--out style_corpus/telegram_posts.jsonl]
"""
from __future__ import annotations

import argparse
import html
import json
import re
import sys
import time
import urllib.request
from pathlib import Path

_UA = {"User-Agent": "Mozilla/5.0"}


def _fetch(url: str) -> str:
    req = urllib.request.Request(url, headers=_UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")


def _parse_page(doc: str, channel: str) -> dict[int, dict]:
    """Return {message_id: {date, text}} for one preview page."""
    out: dict[int, dict] = {}
    id_re = re.compile(rf'data-post="{re.escape(channel)}/(\d+)"')
    blocks = doc.split("tgme_widget_message_wrap")
    for b in blocks:
        idm = id_re.search(b)
        if not idm:
            continue
        mid = int(idm.group(1))
        t = re.search(
            r'tgme_widget_message_text[^>]*>(.*?)</div>\s*'
            r'<div class="tgme_widget_message_footer',
            b,
            re.S,
        )
        if not t:
            t = re.search(r'tgme_widget_message_text[^>]*>(.*?)</div>', b, re.S)
        text = ""
        if t:
            raw = t.group(1).replace("<br/>", "\n").replace("<br>", "\n")
            text = html.unescape(re.sub(r"<[^>]+>", "", raw)).strip()
        d = re.search(r'datetime="([^"]+)"', b)
        when = d.group(1) if d else ""
        out[mid] = {"date": when, "text": text}
    return out


def scrape(channel: str, sleep: float = 0.5, max_rounds: int = 80) -> dict[int, dict]:
    """Paginate the whole public preview. Returns {message_id: {date, text}}."""
    all_msgs: dict[int, dict] = {}
    before: int | None = None
    rounds = 0
    while True:
        rounds += 1
        url = f"https://t.me/s/{channel}"
        if before is not None:
            url += f"?before={before}"
        page = _parse_page(_fetch(url), channel)
        if not page:
            break
        new = set(page) - set(all_msgs)
        all_msgs.update(page)
        min_id = min(page)
        print(
            f"round {rounds}: before={before} got {len(page)} "
            f"[{min(page)}..{max(page)}] new={len(new)} total={len(all_msgs)}",
            file=sys.stderr,
        )
        if not new:
            break
        if before is not None and min_id >= before:
            break
        before = min_id
        if rounds >= max_rounds:
            print("safety stop", file=sys.stderr)
            break
        time.sleep(sleep)
    return all_msgs


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Scrape public Telegram channel preview to JSONL")
    p.add_argument("--channel", default="beops_it")
    p.add_argument(
        "--out",
        default=str(Path(__file__).with_name("style_corpus") / "telegram_posts.jsonl"),
        help="output JSONL path (use '-' for stdout)",
    )
    p.add_argument("--keep-empty", action="store_true", help="keep media-only posts with no text")
    args = p.parse_args(argv)

    msgs = scrape(args.channel)
    rows = []
    for mid in sorted(msgs):
        rec = msgs[mid]
        if not rec["text"] and not args.keep_empty:
            continue
        rows.append({"id": mid, "channel": args.channel, **rec})

    body = "\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n"
    if args.out == "-":
        sys.stdout.write(body)
    else:
        out = Path(args.out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(body, encoding="utf-8")
        print(f"wrote {len(rows)} posts -> {out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

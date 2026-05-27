"""CLI: `python -m rag.cli <command>`.

Commands:
  init            create schema (idempotent)
  index [PATH]    index posts (default: ../_posts relative to this file)
  reset           drop + recreate schema (use when model/chunker version bumps)
  search "QUERY"  hybrid search smoke test, prints top-K hits
"""
from __future__ import annotations

import argparse
import logging
from pathlib import Path

from . import indexer, retriever
from .db import connect, init_schema


def _default_posts_dir() -> Path:
    # posts-generator/rag/cli.py → ../../_posts
    return Path(__file__).resolve().parents[2] / "_posts"


def main(argv: list[str] | None = None) -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s %(message)s")

    p = argparse.ArgumentParser(prog="rag")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("init", help="create schema (idempotent)")

    pi = sub.add_parser("index", help="index posts")
    pi.add_argument("path", nargs="?", default=None, help="posts dir (default: ../_posts)")
    pi.add_argument("--force", action="store_true", help="reindex even if body_hash unchanged")

    sub.add_parser("reset", help="drop + recreate schema (destructive)")

    ps = sub.add_parser("search", help="hybrid search smoke test")
    ps.add_argument("query")
    ps.add_argument("-k", type=int, default=8)

    args = p.parse_args(argv)

    if args.cmd == "init":
        with connect() as conn:
            init_schema(conn)
            conn.commit()
        print("schema ready")
        return 0

    if args.cmd == "reset":
        with connect() as conn:
            indexer.reset(conn)
        print("schema reset")
        return 0

    if args.cmd == "index":
        posts_dir = Path(args.path) if args.path else _default_posts_dir()
        with connect() as conn:
            stats = indexer.index(conn, posts_dir, force=args.force)
        print(stats)
        return 0

    if args.cmd == "search":
        with connect() as conn:
            hits = retriever.search(conn, args.query, k=args.k)
        for h in hits:
            print(f"  {h.score:.4f}  {h.slug}#{h.ord}")
            preview = h.text.replace("\n", " ")[:200]
            print(f"           {preview}…")
        return 0

    return 2


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())

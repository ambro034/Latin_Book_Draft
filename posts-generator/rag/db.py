"""Postgres connection helpers.

Connection string sources, in order:
  1. explicit `dsn` arg
  2. $BEOPS_TEST_DATABASE_URL  (CI: ephemeral Neon branch)
  3. $NEON_DATABASE_URL        (production)
  4. $DATABASE_URL             (generic fallback)
"""
from __future__ import annotations

import contextlib
import os
from pathlib import Path
from typing import Iterator

import psycopg

from . import (
    CHUNKER_VERSION,
    EMBEDDING_DIM,
    EMBEDDING_MODEL,
    SCHEMA_VERSION,
)


def get_dsn(dsn: str | None = None) -> str:
    if dsn:
        return dsn
    for env in ("BEOPS_TEST_DATABASE_URL", "NEON_DATABASE_URL", "DATABASE_URL"):
        v = os.getenv(env)
        if v:
            return v
    raise RuntimeError(
        "no database connection string set "
        "(BEOPS_TEST_DATABASE_URL / NEON_DATABASE_URL / DATABASE_URL)"
    )


@contextlib.contextmanager
def connect(dsn: str | None = None) -> Iterator[psycopg.Connection]:
    conn = psycopg.connect(get_dsn(dsn), autocommit=False)
    try:
        yield conn
    finally:
        conn.close()


def schema_path() -> Path:
    return Path(__file__).with_name("schema.sql")


def init_schema(conn: psycopg.Connection) -> None:
    """Create tables + functions. Idempotent."""
    sql = schema_path().read_text(encoding="utf-8")
    with conn.cursor() as cur:
        cur.execute(sql)
    _write_meta(
        conn,
        schema_version=SCHEMA_VERSION,
        embedding_model=EMBEDDING_MODEL,
        embedding_dim=str(EMBEDDING_DIM),
        chunker_version=CHUNKER_VERSION,
    )
    conn.commit()


def _write_meta(conn: psycopg.Connection, **kv: str) -> None:
    with conn.cursor() as cur:
        for k, v in kv.items():
            cur.execute(
                """
                insert into rag_meta(key, value) values (%s, %s)
                on conflict (key) do update
                  set value = excluded.value, updated_at = now()
                """,
                (k, v),
            )


def read_meta(conn: psycopg.Connection) -> dict[str, str]:
    with conn.cursor() as cur:
        cur.execute("select key, value from rag_meta")
        return {k: v for k, v in cur.fetchall()}


def assert_meta_matches(conn: psycopg.Connection) -> None:
    """Abort if the DB was indexed with a different model/chunker/schema.

    Prevents silent retrieval drift when we change embedding model, chunker
    semantics, or schema. Operator must run `python -m rag.cli reset` then
    `index` to recover.
    """
    meta = read_meta(conn)
    if not meta:
        return  # fresh DB
    expected = {
        "schema_version": SCHEMA_VERSION,
        "embedding_model": EMBEDDING_MODEL,
        "embedding_dim": str(EMBEDDING_DIM),
        "chunker_version": CHUNKER_VERSION,
    }
    mismatches = {k: (meta.get(k), v) for k, v in expected.items() if meta.get(k) != v}
    if mismatches:
        raise RuntimeError(
            "rag_meta mismatch — DB was indexed with different params. "
            f"got/want: {mismatches}. Run `python -m rag.cli reset` then `index`."
        )


def acquire_index_lock(conn: psycopg.Connection) -> bool:
    """Postgres advisory lock so concurrent indexer runs serialize.

    Returns True if lock acquired, False if another indexer is running.
    Lock is automatically released on connection close.
    """
    with conn.cursor() as cur:
        # arbitrary stable key for the "indexer" critical section
        cur.execute("select pg_try_advisory_lock(7142001)")
        (got,) = cur.fetchone()
        return bool(got)

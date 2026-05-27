"""Pytest fixtures.

Integration tests need a real Postgres with pgvector. Two modes:

1. **CI**: env var `BEOPS_TEST_DATABASE_URL` is set to an ephemeral Neon
   branch created by the workflow. We use it directly and *do not* clean up
   (the workflow deletes the branch after).

2. **Local**: if `NEON_API_KEY` + `NEON_PROJECT_ID` are set, this conftest
   creates a per-session branch (with 1h TTL so leaks expire) and tears it
   down at end-of-session. Otherwise, integration tests are skipped.
"""
from __future__ import annotations

import datetime as _dt
import os
import time
import uuid

import pytest
import requests

NEON_API = "https://console.neon.tech/api/v2"


def _create_branch(
    api_key: str, project_id: str, name: str, ttl_hours: int = 1
) -> tuple[str, str]:
    """Create a Neon branch with a compute endpoint; return (branch_id, dsn)."""
    expires = (
        _dt.datetime.now(_dt.timezone.utc) + _dt.timedelta(hours=ttl_hours)
    ).strftime("%Y-%m-%dT%H:%M:%SZ")
    r = requests.post(
        f"{NEON_API}/projects/{project_id}/branches",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "branch": {"name": name, "expires_at": expires},
            "endpoints": [{"type": "read_write"}],
        },
        timeout=60,
    )
    r.raise_for_status()
    payload = r.json()
    branch_id = payload["branch"]["id"]
    endpoint_host = payload["endpoints"][0]["host"]

    # Get the connection_uri for the default role/database on this branch
    role = payload.get("branch", {}).get("name", "neondb_owner")
    # Use the project-level connection_uri endpoint (more reliable than role lookup)
    r2 = requests.get(
        f"{NEON_API}/projects/{project_id}/connection_uri",
        headers={"Authorization": f"Bearer {api_key}"},
        params={
            "branch_id": branch_id,
            "database_name": "neondb",
            "role_name": "neondb_owner",
        },
        timeout=30,
    )
    r2.raise_for_status()
    dsn = r2.json()["uri"]
    # Wait briefly for compute to wake
    _wait_until_reachable(dsn)
    return branch_id, dsn


def _delete_branch(api_key: str, project_id: str, branch_id: str) -> None:
    try:
        requests.delete(
            f"{NEON_API}/projects/{project_id}/branches/{branch_id}",
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=30,
        )
    except Exception:  # pragma: no cover - best-effort cleanup
        pass


def _wait_until_reachable(dsn: str, deadline: float = 60.0) -> None:
    import psycopg

    start = time.monotonic()
    last_err: Exception | None = None
    while time.monotonic() - start < deadline:
        try:
            with psycopg.connect(dsn, connect_timeout=5) as c:
                with c.cursor() as cur:
                    cur.execute("select 1")
                    cur.fetchone()
            return
        except Exception as e:
            last_err = e
            time.sleep(1.5)
    raise RuntimeError(f"branch never became reachable: {last_err}")


@pytest.fixture(scope="session")
def database_url() -> str:
    """Return a DSN to a real Postgres+pgvector instance, or skip."""
    if dsn := os.getenv("BEOPS_TEST_DATABASE_URL"):
        return dsn

    api_key = os.getenv("NEON_API_KEY")
    project_id = os.getenv("NEON_PROJECT_ID")
    if not (api_key and project_id):
        pytest.skip(
            "integration tests skipped: set BEOPS_TEST_DATABASE_URL, "
            "or NEON_API_KEY + NEON_PROJECT_ID for local branch creation"
        )

    name = f"ci-pytest-{uuid.uuid4().hex[:8]}"
    branch_id, dsn = _create_branch(api_key, project_id, name)
    yield dsn
    _delete_branch(api_key, project_id, branch_id)


@pytest.fixture
def conn(database_url):
    """Per-test connection on a freshly-reset schema."""
    import psycopg

    from rag import indexer
    from rag.db import init_schema

    c = psycopg.connect(database_url)
    try:
        # ensure pgvector exists; reset schema for hermetic tests
        with c.cursor() as cur:
            cur.execute("create extension if not exists vector")
        c.commit()
        indexer.reset(c)
        yield c
    finally:
        c.close()

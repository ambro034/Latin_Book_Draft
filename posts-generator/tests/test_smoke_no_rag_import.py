"""Smoke test: importing the generator's hot path must NOT pull in
sentence_transformers, psycopg, or any RAG runtime.

This is the safety rail the rubber-duck pass called out: if the generator
silently imports torch on every invocation, we regress startup time and
break environments that don't have it installed.

The contract is now stronger: regardless of env vars, *importing*
openai_worker_4o never touches RAG modules. The heavy imports are gated
inside the _rag_context_block() call site.
"""
from __future__ import annotations

import os
import subprocess
import sys
import textwrap


SCRIPT = textwrap.dedent(
    """
    import os, sys
    # Force a clean import: no DB url, no flags.
    for k in ("BEOPS_RAG_DISABLED", "NEON_DATABASE_URL",
              "DATABASE_URL", "BEOPS_TEST_DATABASE_URL"):
        os.environ.pop(k, None)

    for mod in ("openai_worker_4o",):
        try:
            __import__(mod)
        except Exception:
            pass

    forbidden = {
        "sentence_transformers",
        "torch",
        "psycopg",
        "rag.embedder",
        "rag.retriever",
        "rag.db",
        "rag.indexer",
    }
    leaked = forbidden & set(sys.modules)
    if leaked:
        print("LEAKED:", sorted(leaked))
        sys.exit(1)
    print("OK")
    """
)


def test_generator_does_not_import_rag_on_module_import(tmp_path):
    env = os.environ.copy()
    for k in ("BEOPS_RAG_DISABLED", "NEON_DATABASE_URL",
              "DATABASE_URL", "BEOPS_TEST_DATABASE_URL"):
        env.pop(k, None)
    cwd = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out = subprocess.run(
        [sys.executable, "-c", SCRIPT],
        cwd=cwd,
        env=env,
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert out.returncode == 0, f"stdout={out.stdout!r} stderr={out.stderr!r}"
    assert out.stdout.strip().endswith("OK")

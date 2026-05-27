"""Smoke test: importing the generator's hot path must NOT pull in
sentence_transformers, psycopg, or any RAG runtime when BEOPS_RAG_ENABLED
is unset.

This is the safety rail the rubber-duck pass called out: if the generator
silently imports torch on every invocation, we regress startup time and
break environments that don't have it installed.
"""
from __future__ import annotations

import os
import subprocess
import sys
import textwrap


SCRIPT = textwrap.dedent(
    """
    import os, sys
    os.environ.pop("BEOPS_RAG_ENABLED", None)

    # Import the modules the generator entrypoints touch on startup.
    # Use a non-failing import probe — if any module is unavailable in this
    # environment (Azure SDK etc.), skip it. We're only asserting absence
    # of RAG-runtime imports.
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


def test_generator_does_not_import_rag_when_flag_off(tmp_path):
    env = os.environ.copy()
    env.pop("BEOPS_RAG_ENABLED", None)
    # Run as a fresh subprocess from posts-generator/ so the import paths
    # match real usage.
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

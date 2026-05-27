# BeOps RAG Architecture

How the **RAG-over-own-posts** pipeline is built and how it plugs into the
existing AI content generator.

The goal: when the generator drafts a new post, it first asks Postgres
*"what have I already written that touches this topic?"*, then receives a
short block of citations + an anti-rehash instruction inside its system
prompt. Cost target: **$0/month**.

---

## 1. System overview

```mermaid
flowchart LR
  subgraph Author["👤 Author / CI"]
    NEW[New Markdown post in _posts/]
  end

  subgraph GH["GitHub (gh-pages branch)"]
    REPO[(BeOps repo)]
    WF_IDX[["rag-index.yml<br/>workflow"]]
    WF_TST[["rag-tests.yml<br/>workflow"]]
  end

  subgraph PG["☁️ Neon Postgres (free tier)"]
    direction TB
    EXT([pgvector + tsvector])
    T_POSTS[("posts<br/>slug · title · url · body_hash")]
    T_CHUNKS[("chunks<br/>text · embedding(384) · tsv")]
    T_META[("rag_meta<br/>schema/model/chunker version")]
    FN[["search_chunks(q, q_emb)<br/>dense + FTS + RRF"]]
  end

  subgraph Gen["🤖 posts-generator (Python)"]
    direction TB
    HOOK{{"BEOPS_RAG_ENABLED=1?"}}
    RET[rag.retriever.context_for]
    EMB[sentence-transformers<br/>MiniLM-L6-v2  · 384-dim]
    WORKER[openai_worker_4o.py<br/>creates draft]
    OAI[(Azure OpenAI<br/>GPT-4o)]
  end

  NEW -->|git push| REPO
  REPO --> WF_IDX
  REPO --> WF_TST
  WF_IDX -->|"python -m rag.cli index"| PG
  WF_TST -->|ephemeral Neon branch<br/>4h TTL| PG

  WORKER --> HOOK
  HOOK -- yes --> RET
  RET -->|"embed(query)"| EMB
  EMB -->|"q_emb"| FN
  RET -->|"SELECT search_chunks(...)"| FN
  FN --> T_CHUNKS
  FN --> T_POSTS
  RET -->|"PRIOR POSTS YOU HAVE<br/>ALREADY WRITTEN\n+ citations"| WORKER
  HOOK -- no --> WORKER
  WORKER --> OAI
  OAI -->|"grounded draft"| WORKER

  classDef store fill:#1f2d3a,stroke:#5b9bd5,color:#e6edf3;
  classDef wf fill:#26312d,stroke:#7ec699,color:#e6edf3;
  class T_POSTS,T_CHUNKS,T_META,EXT store
  class WF_IDX,WF_TST wf
```

**Key properties**

| Concern | Choice | Why |
|---|---|---|
| Vector store | Neon pgvector (free, scale-to-zero) | $0 idle, no infra to babysit |
| Embeddings | `sentence-transformers/all-MiniLM-L6-v2` (384-dim, MIT, CPU) | runs in GH Actions, no API key, no quota |
| Lexical | Postgres `tsvector` + `ts_rank_cd` | comes with the database |
| Fusion | Reciprocal Rank Fusion (k=60) **in SQL** | dense + lexical hits combined inside one CTE — Python just calls one function |
| ANN index | **none at v1** (exact cosine scan) | tiny corpus (~65 chunks); IVFFlat hurts recall here |
| Drift guard | `rag_meta` table pins `(schema_version, embedding_model, chunker_version)` | indexer aborts with a clear error if any of these change |
| Concurrency | Postgres advisory lock `7142001` + GH Actions concurrency groups | safe under parallel pushes |
| Feature flag | `BEOPS_RAG_ENABLED` (default OFF) | smoke test asserts `torch`/`psycopg` are **not** imported when off |

---

## 2. Indexing flow

What happens on every push to `gh-pages` that touches `_posts/**`:

```mermaid
sequenceDiagram
    autonumber
    participant Dev as Author / git push
    participant GH as GitHub Actions<br/>(rag-index.yml)
    participant IDX as rag.indexer
    participant EMB as MiniLM-L6-v2
    participant PG as Neon Postgres

    Dev->>GH: push to gh-pages touching _posts/**
    GH->>IDX: python -m rag.cli index
    IDX->>PG: init_schema() (idempotent)
    IDX->>PG: assert_meta_matches()
    IDX->>PG: pg_try_advisory_lock(7142001)
    PG-->>IDX: lock acquired
    loop for each *.md in _posts/
        IDX->>IDX: parse front-matter + body_hash
        alt body_hash unchanged
            IDX->>PG: UPDATE posts (title/category only)
        else new or changed
            IDX->>IDX: chunk_markdown(target=500, overlap=80)
            IDX->>EMB: embed(chunks)  — batched
            EMB-->>IDX: 384-dim L2-normalized vectors
            IDX->>PG: DELETE old chunks, INSERT post + chunks
        end
    end
    IDX->>PG: DELETE posts no longer on disk (orphans)
    IDX->>PG: pg_advisory_unlock(7142001)
    IDX-->>GH: IndexStats(scanned, inserted, updated, deleted)
```

Idempotency comes from `body_hash` (sha256 of post-frontmatter body) —
metadata-only edits update title/url cheaply; identical content is a no-op.

---

## 3. Retrieval flow (generation time)

What happens when `posts-generator` drafts a new post with the flag on:

```mermaid
sequenceDiagram
    autonumber
    participant Worker as openai_worker_4o.py
    participant Hook as _rag_context_block()
    participant Ret as rag.retriever
    participant Emb as MiniLM-L6-v2
    participant PG as Neon Postgres
    participant Fn as search_chunks() (SQL)
    participant OAI as Azure OpenAI (GPT-4o)

    Worker->>Hook: seed_text[:2000]
    Note over Hook: BEOPS_RAG_ENABLED=1 ?
    Hook->>Ret: context_for(conn, seed, k=8)
    Ret->>Emb: embed(seed)
    Emb-->>Ret: q_emb (384-d)
    Ret->>PG: SELECT * FROM search_chunks(q, q_emb, 8, 50)
    PG->>Fn: dense (<=>) ⨯ FTS (ts_rank_cd)
    Fn->>Fn: RRF fuse (k=60)
    Fn-->>PG: top-K rows
    PG-->>Ret: hits[]
    Ret-->>Hook: "PRIOR POSTS YOU HAVE ALREADY WRITTEN:\n- [title](url)\n…\nDo NOT rehash. Cite by URL."
    Hook-->>Worker: appended to system_message
    Worker->>OAI: chat.completions.create(messages)
    OAI-->>Worker: grounded draft (cites prior URLs)
```

All ranking — dense cosine, BM25-style FTS, and RRF — happens inside one
SQL CTE in `search_chunks()`. Python is a thin client; if you change the
fusion strategy, you change one SQL function.

---

## 4. Quality gate

`rag-tests.yml` runs on every push and spins up a real Neon branch with
a 4-hour TTL so cancelled jobs can't leak past the 10-branch cap:

```mermaid
flowchart LR
  PUSH[push to gh-pages] --> WF[rag-tests.yml]
  WF -->|create branch<br/>expires_at = now + 4h| NEON[(Neon branch)]
  WF --> UNIT[Unit tests<br/>chunker · embedder · RRF]
  WF --> SMOKE[Smoke test<br/>no RAG imports when flag off]
  WF --> INT[Integration tests<br/>indexer · retriever]
  WF --> EVAL[Eval fixture<br/>5 queries → expected slugs]
  UNIT --> PASS
  SMOKE --> PASS
  INT --> NEON
  EVAL --> NEON
  INT --> PASS{All green?}
  EVAL --> PASS
  PASS -- yes --> MERGE[merge / index runs]
  PASS -- no --> BLOCK[CI red]
  WF -.->|always: delete branch| NEON
```

The eval fixture (`posts-generator/tests/fixtures/eval_queries.yaml`) is
the regression gate: hand-picked queries each declare the expected slug
in the top-K. If a future change breaks retrieval for "kubernetes
readiness probe configuration" → `2024-12-15-kubernetes`, CI goes red.

---

## 5. File map

```
posts-generator/
├── rag/
│   ├── __init__.py        # pins schema/chunker/model versions + EMBEDDING_DIM=384
│   ├── schema.sql         # posts, chunks, rag_meta + search_chunks() SQL fn
│   ├── db.py              # connect, init_schema, meta-check, advisory lock
│   ├── chunker.py         # front-matter strip, H2-bounded chunks w/ overlap
│   ├── embedder.py        # sentence-transformers wrapper (L2-normalized)
│   ├── indexer.py         # idempotent + incremental + orphan reconciliation
│   ├── retriever.py       # search() and context_for() (prompt block builder)
│   └── cli.py             # python -m rag.cli {init,index,reset,search}
├── tests/
│   ├── conftest.py        # Neon ephemeral branch fixture (4h TTL)
│   ├── fixtures/eval_queries.yaml
│   └── test_*.py          # unit · smoke · integration · eval
├── requirements-rag.txt
├── pytest.ini
└── openai_worker_4o.py    # _rag_context_block() — opt-in via BEOPS_RAG_ENABLED

.github/workflows/
├── rag-index.yml          # incremental indexer on _posts/** pushes
└── rag-tests.yml          # full pytest on ephemeral Neon branch
```

---

## 6. Operate it

```bash
# turn it on locally
export BEOPS_RAG_ENABLED=1
export NEON_DATABASE_URL='postgres://…'   # same as the GH secret

cd posts-generator

# see what's indexed
python -m rag.cli search "kubernetes probes"

# force a full reindex (e.g. after bumping CHUNKER_VERSION)
python -m rag.cli reset
python -m rag.cli index

# run the tests against your own ephemeral Neon branch
export NEON_API_KEY='napi_…' NEON_PROJECT_ID='…'
pytest -v
```

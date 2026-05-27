"""RAG package: index BeOps posts into pgvector and retrieve hybrid context."""

__version__ = "0.1.0"

# Schema/chunker/embedder versions are pinned in the DB's rag_meta table.
# Bump these when changing semantics; indexer aborts on mismatch.
SCHEMA_VERSION = "1"
CHUNKER_VERSION = "1"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
EMBEDDING_DIM = 384

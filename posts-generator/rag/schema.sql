-- BeOps RAG schema (v1)
-- pgvector + Postgres FTS. No ANN index at v1 scale (~hundreds of chunks);
-- exact cosine scan is fast and accurate.

create extension if not exists vector;

create table if not exists rag_meta (
  key         text primary key,
  value       text not null,
  updated_at  timestamptz not null default now()
);

create table if not exists posts (
  slug        text primary key,
  title       text not null,
  category    text not null,
  url         text not null,
  body_hash   text not null,
  body        text not null,
  body_tsv    tsvector generated always as
                (to_tsvector('english', coalesce(title,'') || ' ' || body)) stored,
  updated_at  timestamptz not null default now()
);
create index if not exists posts_tsv_idx on posts using gin(body_tsv);

create table if not exists chunks (
  id          bigserial primary key,
  slug        text not null references posts(slug) on delete cascade,
  ord         int  not null,
  text        text not null,
  text_tsv    tsvector generated always as
                (to_tsvector('english', text)) stored,
  embedding   vector(384)
);
create index if not exists chunks_tsv_idx on chunks using gin(text_tsv);
create unique index if not exists chunks_slug_ord_uniq on chunks(slug, ord);

-- Hybrid search: dense cosine + FTS rank, fused with Reciprocal Rank Fusion.
-- RRF constant k = 60 (textbook default from the Cormack et al. 2009 paper).
create or replace function search_chunks(
  q       text,
  q_emb   vector(384),
  k       int default 8,
  pool    int default 50
)
returns table(
  slug      text,
  ord       int,
  text      text,
  rrf       double precision
)
language sql stable
as $$
  with
  dense as (
    select c.id, c.slug, c.ord, c.text,
           row_number() over (order by c.embedding <=> q_emb) as r
    from chunks c
    where c.embedding is not null
    order by c.embedding <=> q_emb
    limit pool
  ),
  sparse as (
    select c.id, c.slug, c.ord, c.text,
           row_number() over (
             order by ts_rank_cd(c.text_tsv, plainto_tsquery('english', q)) desc
           ) as r
    from chunks c
    where c.text_tsv @@ plainto_tsquery('english', q)
    limit pool
  ),
  fused as (
    select coalesce(d.id, s.id)     as id,
           coalesce(d.slug, s.slug) as slug,
           coalesce(d.ord, s.ord)   as ord,
           coalesce(d.text, s.text) as text,
           coalesce(1.0 / (60 + d.r), 0)
         + coalesce(1.0 / (60 + s.r), 0) as rrf
    from dense d full outer join sparse s using (id)
  )
  select slug, ord, text, rrf
  from fused
  order by rrf desc
  limit k;
$$;

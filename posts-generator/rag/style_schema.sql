-- BeOps STYLE corpus schema (v1)
-- Separate from the blog RAG (posts/chunks). This stores the author's own
-- Telegram channel posts and is used ONLY to retrieve voice/tone exemplars
-- when drafting a new Telegram post. It never participates in blog
-- anti-rehash retrieval.
--
-- pgvector + Postgres FTS, exact cosine scan (tiny corpus).

create extension if not exists vector;

create table if not exists style_meta (
  key         text primary key,
  value       text not null,
  updated_at  timestamptz not null default now()
);

create table if not exists style_posts (
  tg_id       bigint primary key,
  channel     text not null,
  posted_at   timestamptz,
  body_hash   text not null,
  body        text not null,
  updated_at  timestamptz not null default now()
);

create table if not exists style_chunks (
  id          bigserial primary key,
  tg_id       bigint not null references style_posts(tg_id) on delete cascade,
  ord         int  not null,
  text        text not null,
  text_tsv    tsvector generated always as
                (to_tsvector('simple', text)) stored,
  embedding   vector(384)
);
create index if not exists style_chunks_tsv_idx on style_chunks using gin(text_tsv);
create unique index if not exists style_chunks_tgid_ord_uniq on style_chunks(tg_id, ord);

-- Hybrid search: dense cosine + FTS, fused with Reciprocal Rank Fusion (k=60).
-- 'simple' FTS config (not 'english') because the corpus is mixed RU/EN.
create or replace function search_style_chunks(
  q       text,
  q_emb   vector(384),
  k       int default 6,
  pool    int default 40
)
returns table(
  tg_id   bigint,
  ord     int,
  text    text,
  rrf     double precision
)
language sql stable
as $$
  with
  dense as (
    select c.id, c.tg_id, c.ord, c.text,
           row_number() over (order by c.embedding <=> q_emb) as r
    from style_chunks c
    where c.embedding is not null
    order by c.embedding <=> q_emb
    limit pool
  ),
  sparse as (
    select c.id, c.tg_id, c.ord, c.text,
           row_number() over (
             order by ts_rank_cd(c.text_tsv, plainto_tsquery('simple', q)) desc
           ) as r
    from style_chunks c
    where c.text_tsv @@ plainto_tsquery('simple', q)
    order by ts_rank_cd(c.text_tsv, plainto_tsquery('simple', q)) desc
    limit pool
  ),
  fused as (
    select coalesce(d.id, s.id)       as id,
           coalesce(d.tg_id, s.tg_id) as tg_id,
           coalesce(d.ord, s.ord)     as ord,
           coalesce(d.text, s.text)   as text,
           coalesce(1.0 / (60 + d.r), 0)
         + coalesce(1.0 / (60 + s.r), 0) as rrf
    from dense d full outer join sparse s using (id)
  )
  select tg_id, ord, text, rrf
  from fused
  order by rrf desc
  limit k;
$$;

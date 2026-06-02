---
name: beops-publish-post
description: Publishes a new post to the BeOps Jekyll site (NeverTheSame/BeOps) from a source file or topic. Runs the RAG store over prior posts for coherence and anti-rehash, writes a correctly-front-mattered _posts/*.md, creates a new category/subcategory when asked (categories.yml + _pages page + site-audit env), runs the Playwright/lychee site audit, shows the draft for approval, then commits and pushes to gh-pages. Use when the user asks to "create/publish a BeOps post", "turn this file into a post", "post this to BeOps", "add a new category", or similar BeOps authoring tasks.
---

# beops-publish-post — Author & Publish a BeOps Post

End-to-end workflow for turning a source file or topic into a published BeOps
post, grounded in the repo's RAG store and validated by the site audit.

**Repo:** `NeverTheSame/BeOps` (GitHub Pages, baseurl `/BeOps`). All authoring
happens on the **`gh-pages`** branch.

## When to Invoke

- "Create a post from `<file>`" / "turn this into a BeOps post"
- "Post this to BeOps" / "publish a new article"
- "Add it under a new category/subcategory"
- Any request to write/edit content under `_posts/` or `_pages/`.

## Golden Rules (do not skip)

1. **Always work on `gh-pages`.** `git branch --show-current` must be `gh-pages`.
2. **Always run RAG first** (see Step 2). The whole point is to cite prior work
   and stop repeating ourselves. Skipping it is a regression.
3. **Always use `relative_url`** for internal links — hard-coded `/devops/`-style
   paths 404 on the live site (baseurl is `/BeOps`).
4. **Always show the full draft to the user and get approval before pushing.**
5. **Always run the site audit before pushing** and fix any issues.

## Step 1 — Read the source & gather context

- Read the source file/topic the user provided.
- If the user says "don't mention X" (e.g. "don't say Day 1"), honor it — strip
  series framing and make it a standalone post.
- Note any link the user wants included (e.g. a GitHub repo).

## Step 2 — RAG grounding over prior posts (REQUIRED)

The RAG store lives in Neon; the DSN is the `NEON_DATABASE_URL` **GitHub Actions
secret** and is normally NOT in the local environment. Two ways to query it:

### Preferred: run it locally if the DSN is available

```bash
cd posts-generator
export NEON_DATABASE_URL='postgres://…'   # only if the user provides it
python -m rag.cli context "<one-paragraph description of the post>"
```

### If `NEON_DATABASE_URL` is NOT set locally: dispatch the Actions workflow

There is a dedicated workflow `rag-query.yml` that runs the query inside Actions
(the secret never leaves CI) and returns the prompt block as an artifact.

```bash
# Note: the repo's default `gh` remote may resolve to the upstream fork, so
# always pass -R NeverTheSame/BeOps and --ref gh-pages.
gh workflow run rag-query.yml -R NeverTheSame/BeOps --ref gh-pages \
  -f seed="<one-paragraph description of the post>" -f k=8

# Wait for it, then download the prompt block:
RID=$(gh run list -R NeverTheSame/BeOps --workflow=rag-query.yml --limit 1 \
        --json databaseId -q '.[0].databaseId')
gh run watch -R NeverTheSame/BeOps "$RID" --exit-status
gh run download -R NeverTheSame/BeOps "$RID" -n rag-context -D /tmp/ragctx
cat /tmp/ragctx/rag-context.txt
```

The output is a "PRIOR POSTS YOU HAVE ALREADY WRITTEN" block with URLs. Use it to:

1. **Cite** every prior post the draft overlaps with (link to its URL).
2. **Avoid rehashing** angles already covered — pick a new angle or explicitly
   extend/contradict prior coverage.
3. If the block is empty, the topic is new — proceed.

Convert the absolute prior-post URLs to `relative_url` form when citing inline,
e.g. `https://neverthesame.github.io/BeOps/ai/2025-11-20-foo.html` →
`[Title]({{ '/ai/2025-11-20-foo.html' | relative_url }})`.

## Step 3 — (Only if a new category/subcategory is requested)

Categories are defined in **three** places that MUST stay in sync
(`_data/categories.yml` is the single source of truth):

1. Append to `_data/categories.yml`:
   ```yaml
   - slug: <slug>
     title: <Title>
     description: <one-line description>
   ```
2. Create `_pages/<slug>.md` (copy an existing one like `_pages/ai.md`):
   ```yaml
   ---
   title: <Title>
   layout: home
   permalink: /<slug>/
   is_category: true
   description: <one-line description>.
   ---
   ```
   Keep the Liquid block that lists `site.categories.<slug>` posts.
3. Add the slug to `BEOPS_CATEGORIES` in `.github/workflows/site-audit.yml`
   (comma-separated list — the audit fails if a category page can't be reached).

The homepage (`index.md`) and sidebar (`_includes/toc-date.html`) iterate
`site.data.categories`, so they pick up the new category automatically.

## Step 4 — Write the post

- File: `_posts/YYYY-MM-DD-slug.md` (date MUST match the `date` front matter).
- Front matter (see `tests/site-audit/POST_TEMPLATE.md`):
  ```yaml
  ---
  title: "…"
  author: Kirill Kuklin
  date: YYYY-MM-DD
  category: <one of the slugs in _data/categories.yml>
  layout: post
  tags:
    - tag-one
    - tag-two
  excerpt: >
    1-3 sentence scannable summary (becomes the homepage excerpt).
  ---
  ```
- Voice/house style: first person, SRE/operator perspective, concrete code
  blocks and tables, opinionated but grounded. Match existing posts in `_posts/`.
- The first paragraph is the excerpt shown on the homepage — make it land.
- Internal links: `[Text]({{ '/<cat>/<file>.html' | relative_url }})`.
  External links: plain markdown. Include any repo/link the user requested.

## Step 5 — Show the draft & get approval

Print the full post (or the rendered file) to the user and explicitly ask for
approval **before** committing/pushing. Honor edit requests, then re-show.

## Step 6 — Validate with the site audit

```bash
cd tests/site-audit
npm run audit          # Playwright + lychee; fails on broken/missing-baseurl
                       # links, orphan/unreachable posts, or category pages
                       # that don't list their posts.
```
If `node_modules` is missing, run `npm ci` (or `npm install`) first. Fix every
issue the audit reports before proceeding.

## Step 7 — Commit & push

```bash
git add _posts/<file>.md _pages/<slug>.md _data/categories.yml \
        .github/workflows/site-audit.yml
git commit -m "post: <short title>"   # include only files you actually changed
git push origin gh-pages
```

Include the standard co-author trailer in the commit message unless told not to:
```
Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>
```

After push, GitHub Pages rebuilds automatically; `rag-index.yml` re-indexes the
corpus so the new post is available to future RAG queries.

## Reporting Back

Summarize: the post path, its category (and whether a new category was created),
which prior posts you cited, and the audit result (0 issues). Give the user the
live URL: `https://neverthesame.github.io/BeOps/<category>/<file>.html`.

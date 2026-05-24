# Authoring guide — new posts

This is the safe-by-construction checklist for new BeOps posts. Following it keeps the live site free of the bugs the audit catches.

## 1. Create the post

Filename: `_posts/YYYY-MM-DD-slug.md`

Required front matter:

```yaml
---
title: Your Title Here
author: Kirill Kuklin
date: YYYY-MM-DD
category: devops       # one of: devops | k8s | sre | ai
layout: post
cover: ../assets/your-cover.gif   # optional
tags:                            # optional
  - tag-one
  - tag-two
---
```

**Rules**
- `category` must be **one of the four supported slugs** (`devops`, `k8s`, `sre`, `ai`). Using anything else means the post won't appear on its category index page and the URL won't match the site structure.
- Filename date must match `date:` in front matter.
- `layout: post` is required.

## 2. Linking — never hand-roll paths

The site is served under a baseurl (`/BeOps`). Hard-coded absolute paths like `/devops/foo.html` will 404. Always use Jekyll's `relative_url` filter.

| ❌ DON'T | ✅ DO |
|---|---|
| `[Post]({{ post.url }})` | `[Post]({{ post.url | relative_url }})` |
| `<a href="/devops/">DevOps</a>` | `<a href="{{ '/devops/' | relative_url }}">DevOps</a>` |
| `![img](/assets/x.png)` | `![img]({{ '/assets/x.png' | relative_url }})` |
| `<a href="/feed.xml">RSS</a>` | `<a href="{{ '/feed.xml' | relative_url }}">RSS</a>` |

In plain markdown content (no Liquid), use relative paths to the asset:
`![img](../assets/x.png)` works inside post bodies because Jekyll renders posts with category paths.

## 3. Run the audit before pushing

```bash
cd tests/site-audit
npm install                          # one-time
npx playwright install chromium      # one-time
npm run audit                        # checks live site
```

The audit exits non-zero if any of these regress:
- broken internal links
- links missing the `/BeOps` baseurl
- posts unreachable from the homepage in ≤2 clicks
- orphan posts
- category index pages that don't list their posts

It also runs automatically in GitHub Actions on every push to `gh-pages` and nightly. The workflow artifact `site-audit-report` contains the full report.

## 4. New category? Update three places

If you ever add a 5th category (say `platform`):

1. Create `_pages/platform.md` with `permalink: /platform/` (copy `_pages/ai.md`).
2. Add the link to `index.md` under "📚 Categories".
3. Add the slug to the audit: `BEOPS_CATEGORIES=devops,k8s,sre,ai,platform` in `.github/workflows/site-audit.yml`.

## 5. Don't change

- `_config.yml` `baseurl: /BeOps` — changing this breaks every internal link.
- `permalink: /:categories/:year-:month-:day-:title:output_ext` — the audit's post-URL regex depends on this format.

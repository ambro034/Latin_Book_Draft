---
title: TITLE_HERE
author: Kirill Kuklin
date: YYYY-MM-DD
category: devops         # one of: devops | k8s | sre | ai | job-interviews
layout: post
cover: ../assets/COVER.gif
tags:
  - tag-one
  - tag-two
---

# TITLE_HERE

Intro paragraph (1-3 sentences). The first paragraph becomes the post excerpt
shown on the homepage, so make it scannable.

## Section heading

Body content. When linking to other site pages in raw HTML/Liquid, use the
`relative_url` filter:

- Internal page link: `[About]({{ '/pages/about/' | relative_url }})`
- Another post: `[Post title]({{ '/devops/2025-08-21-dataops.html' | relative_url }})`
- Asset: `![diagram]({{ '/assets/my-diagram.png' | relative_url }})`

Plain in-body relative paths (`../assets/foo.png`) also work because Jekyll
renders posts under `/BeOps/<category>/...`.

## Checklist before pushing

- [ ] Filename: `_posts/YYYY-MM-DD-slug.md` (date matches front matter)
- [ ] `category` is one of `devops | k8s | sre | ai | job-interviews`
- [ ] All links use `relative_url` or are `../`-relative
- [ ] Ran `cd tests/site-audit && npm run audit` → 0 issues

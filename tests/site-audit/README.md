# BeOps site audit

Live-site audit for https://neverthesame.github.io/BeOps/

## What it checks
1. **Broken internal links** — every internal `<a href>` resolved, any 4xx/5xx flagged.
2. **Missing baseurl** — links pointing at `neverthesame.github.io/<not-BeOps>` (Jekyll baseurl bug).
3. **Reachability** — every post is reachable from `/` in ≤2 clicks.
4. **Orphan posts** — posts with no incoming internal links.
5. **Category integrity** — each `/BeOps/<cat>/` page lists at least one post from its own category.

## Run
```bash
cd tests/site-audit
npm install
npx playwright install chromium
npm run audit      # Playwright structural + link audit
npm run lychee     # (optional) extra link check via lychee
```

Output: `tests/site-audit/reports/structure-report.md` and `raw.json`.

The audit exits non-zero when issues are found, so it can be wired into CI.

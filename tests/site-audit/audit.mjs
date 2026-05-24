// BeOps live-site audit.
// Crawls https://neverthesame.github.io/BeOps/ with Playwright (BFS),
// then reports broken internal links, orphan pages, reachability depth,
// and category-page integrity. Designed to be re-runnable in CI.

import { chromium } from 'playwright';
import { writeFile, mkdir } from 'node:fs/promises';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const ORIGIN = process.env.BEOPS_ORIGIN || 'https://neverthesame.github.io';
const BASE = process.env.BEOPS_BASEURL ?? '/BeOps';
const ROOT = `${ORIGIN}${BASE}/`;
const MAX_DEPTH = Number(process.env.BEOPS_MAX_DEPTH || 6);
const REACHABILITY_MAX = Number(process.env.BEOPS_REACH_MAX || 2);
const CATEGORY_SLUGS = (process.env.BEOPS_CATEGORIES || 'devops,k8s,sre,ai').split(',').map(s => s.trim()).filter(Boolean);
const CATEGORY_PATH_RE = new RegExp(`^${BASE}/(${CATEGORY_SLUGS.join('|')})/?$`);
const POST_PATH_RE     = new RegExp(`^${BASE}/(${CATEGORY_SLUGS.join('|')})/\\d{4}-\\d{2}-\\d{2}-[^/]+\\.html$`);

const __dirname = dirname(fileURLToPath(import.meta.url));
const OUT_DIR = resolve(__dirname, 'reports');

function normalize(url) {
  try {
    const u = new URL(url, ROOT);
    u.hash = '';
    // collapse accidental double slashes in path
    u.pathname = u.pathname.replace(/\/{2,}/g, '/');
    // case-fix the host (Jekyll baseurl is configured as NeverTheSame)
    if (u.host.toLowerCase() === 'neverthesame.github.io') {
      u.host = 'neverthesame.github.io';
    }
    return u.toString();
  } catch {
    return null;
  }
}

function isInternal(url) {
  try {
    const u = new URL(url);
    return u.host.toLowerCase() === new URL(ORIGIN).host.toLowerCase();
  } catch { return false; }
}

function looksLikeMissingBaseurl(url) {
  // Link on the BeOps site that goes to <origin>/<something>
  // where <something> is not /<BASE>/... — almost certainly a missing baseurl bug.
  if (!BASE) return false;
  try {
    const u = new URL(url);
    if (u.host.toLowerCase() !== new URL(ORIGIN).host.toLowerCase()) return false;
    return !u.pathname.startsWith(`${BASE}/`) && u.pathname !== BASE;
  } catch { return false; }
}

async function checkStatus(context, url) {
  try {
    const res = await context.request.fetch(url, { maxRedirects: 5, timeout: 20000 });
    return res.status();
  } catch (e) {
    return 0;
  }
}

async function main() {
  await mkdir(OUT_DIR, { recursive: true });

  const browser = await chromium.launch();
  const context = await browser.newContext();
  const page = await context.newPage();

  // BFS
  const depth = new Map();         // url -> depth
  const linksOnPage = new Map();   // url -> Set(linked urls)
  const incoming = new Map();      // url -> Set(referrer urls)
  const visited = new Set();
  const queue = [{ url: ROOT, d: 0 }];
  depth.set(ROOT, 0);

  while (queue.length) {
    const { url, d } = queue.shift();
    if (visited.has(url)) continue;
    visited.add(url);
    if (d > MAX_DEPTH) continue;

    let status = 0;
    let hrefs = [];
    try {
      const resp = await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 25000 });
      status = resp ? resp.status() : 0;
      if (status >= 200 && status < 400) {
        hrefs = await page.$$eval('a[href]', as => as.map(a => a.getAttribute('href')));
      }
    } catch (e) {
      status = 0;
    }
    linksOnPage.set(url, new Set());

    for (const h of hrefs) {
      if (!h) continue;
    if (h.startsWith('mailto:') || h.startsWith('tel:') || h.startsWith('javascript:') || h.startsWith('#')) continue;
      const n = normalize(new URL(h, url).toString());
      if (!n) continue;
      linksOnPage.get(url).add(n);
      if (!incoming.has(n)) incoming.set(n, new Set());
      incoming.get(n).add(url);
      if (isInternal(n) && !visited.has(n) && !depth.has(n)) {
        depth.set(n, d + 1);
        queue.push({ url: n, d: d + 1 });
      }
    }
    process.stdout.write(`[d=${d}] ${status} ${url}\n`);
  }

  // Status check every discovered internal URL (HEAD/GET via request context)
  const allInternal = new Set();
  for (const u of visited) if (isInternal(u)) allInternal.add(u);
  for (const set of linksOnPage.values()) for (const u of set) if (isInternal(u)) allInternal.add(u);

  const statusByUrl = new Map();
  const urls = [...allInternal];
  const CONC = 8;
  let i = 0;
  await Promise.all(Array.from({ length: CONC }, async () => {
    while (i < urls.length) {
      const idx = i++;
      const u = urls[idx];
      statusByUrl.set(u, await checkStatus(context, u));
    }
  }));

  // Findings
  const brokenLinks = []; // {from, to, status}
  for (const [from, set] of linksOnPage) {
    for (const to of set) {
      if (!isInternal(to)) continue;
      const s = statusByUrl.get(to) ?? 0;
      if (s >= 400 || s === 0) brokenLinks.push({ from, to, status: s });
    }
  }

  const missingBaseurl = [];
  for (const [from, set] of linksOnPage) {
    for (const to of set) {
      if (looksLikeMissingBaseurl(to)) missingBaseurl.push({ from, to });
    }
  }

  // Posts discovered
  const posts = [...allInternal].filter(u => POST_PATH_RE.test(new URL(u).pathname));
  const categories = [...allInternal].filter(u => CATEGORY_PATH_RE.test(new URL(u).pathname));

  // Reachability (posts only)
  const unreachable = posts.filter(p => !depth.has(p));
  const tooDeep = posts.filter(p => depth.has(p) && depth.get(p) > REACHABILITY_MAX);

  // Category integrity: each /<BASE>/<cat>/ should link to ≥1 post in that category,
  // UNLESS there are no posts in that category anywhere on the site (genuinely empty).
  const categoryIssues = [];
  for (const cat of categories) {
    const catSlug = new URL(cat).pathname.split('/').filter(Boolean).pop();
    const links = linksOnPage.get(cat) || new Set();
    const postsInCat = [...links].filter(u => {
      const p = new URL(u).pathname;
      return POST_PATH_RE.test(p) && p.startsWith(`${BASE}/${catSlug}/`);
    });
    const anyPostsExistInCat = posts.some(p => new URL(p).pathname.startsWith(`${BASE}/${catSlug}/`));
    if (postsInCat.length === 0 && anyPostsExistInCat) {
      categoryIssues.push({ category: cat, problem: 'has posts in this category but lists none' });
    }
  }

  // Orphan posts: posts in the post-set but with no incoming internal links
  const orphans = posts.filter(p => {
    const inc = incoming.get(p);
    return !inc || inc.size === 0;
  });

  // Report
  const lines = [];
  const push = (s = '') => lines.push(s);
  push(`# BeOps Live-Site Audit`);
  push(`Generated: ${new Date().toISOString()}`);
  push(`Root: ${ROOT}`);
  push('');
  push(`## Summary`);
  push(`- Pages crawled: ${visited.size}`);
  push(`- Internal URLs discovered: ${allInternal.size}`);
  push(`- Posts discovered: ${posts.length}`);
  push(`- Category pages discovered: ${categories.length}`);
  push(`- **Broken internal links: ${brokenLinks.length}**`);
  push(`- **Links missing /BeOps baseurl: ${missingBaseurl.length}**`);
  push(`- Posts unreachable from home: ${unreachable.length}`);
  push(`- Posts reachable but deeper than ${REACHABILITY_MAX} clicks: ${tooDeep.length}`);
  push(`- Category pages with integrity issues: ${categoryIssues.length}`);
  push(`- Orphan posts (no incoming links): ${orphans.length}`);
  push('');

  push(`## Broken internal links`);
  if (brokenLinks.length === 0) push('_None._');
  for (const b of brokenLinks) push(`- [${b.status}] ${b.to}  ← linked from ${b.from}`);
  push('');

  push(`## Links missing /BeOps baseurl`);
  if (missingBaseurl.length === 0) push('_None._');
  for (const m of missingBaseurl) push(`- ${m.to}  ← from ${m.from}`);
  push('');

  push(`## Posts unreachable from homepage`);
  if (unreachable.length === 0) push('_None._');
  for (const u of unreachable) push(`- ${u}`);
  push('');

  push(`## Posts too deep (> ${REACHABILITY_MAX} clicks from home)`);
  if (tooDeep.length === 0) push('_None._');
  for (const u of tooDeep) push(`- depth=${depth.get(u)}  ${u}`);
  push('');

  push(`## Category pages without their own posts listed`);
  if (categoryIssues.length === 0) push('_None._');
  for (const c of categoryIssues) push(`- ${c.category} — ${c.problem}`);
  push('');

  push(`## Orphan posts (no incoming links)`);
  if (orphans.length === 0) push('_None._');
  for (const o of orphans) push(`- ${o}`);
  push('');

  push(`## All discovered posts (depth, status)`);
  for (const p of posts.sort()) {
    push(`- d=${depth.has(p) ? depth.get(p) : '∞'} status=${statusByUrl.get(p) ?? '?'}  ${p}`);
  }

  const report = lines.join('\n');
  await writeFile(resolve(OUT_DIR, 'structure-report.md'), report, 'utf8');
  await writeFile(resolve(OUT_DIR, 'raw.json'), JSON.stringify({
    visited: [...visited],
    depth: Object.fromEntries(depth),
    statusByUrl: Object.fromEntries(statusByUrl),
    brokenLinks, missingBaseurl, unreachable, tooDeep, categoryIssues, orphans,
    posts, categories,
  }, null, 2));

  console.log('\n--- SUMMARY ---');
  console.log(`Broken: ${brokenLinks.length}  MissingBaseurl: ${missingBaseurl.length}  Unreachable: ${unreachable.length}  TooDeep: ${tooDeep.length}  CategoryIssues: ${categoryIssues.length}  Orphans: ${orphans.length}`);
  console.log(`Report: ${resolve(OUT_DIR, 'structure-report.md')}`);

  await browser.close();
  // Non-zero exit when issues found, useful for CI
  const totalIssues = brokenLinks.length + missingBaseurl.length + unreachable.length + tooDeep.length + categoryIssues.length;
  process.exit(totalIssues > 0 ? 1 : 0);
}

main().catch(e => { console.error(e); process.exit(2); });

---
name: blog-post-counter
description: Counts and compares blog posts across a target and competitors, audits content freshness via sitemap lastmod dates, and maps competitor organic keywords (US, non-branded, informational) against the target to surface ranking gaps. Use when asked to compare blog counts, content volume, publishing cadence, content freshness, keyword mapping, keyword gap analysis, or competitor keyword reports — e.g. "how many blog posts does X have vs Y", "how fresh is content on X", "where does [target] rank for [competitor] keywords", "keyword gap between X and Y". Works from company names alone. Always use for blog comparison, freshness audits, and keyword mapping tasks.
---

# Blog Post Counter + Keyword Mapping Skill

Two workflows in one skill:

1. **Blog Post Counter** — counts and compares blog post output across a target and competitors, with optional content freshness audit
2. **Keyword Mapping** — pulls competitor's organic keywords (US, non-branded, informational) and cross-references against target's keyword footprint to surface gaps and opportunities

---

---

# WORKFLOW A — Blog Post Counter

---

## Step 1 — Resolve each company to a URL

For each company name provided:
1. If a URL was given directly, use it.
2. If only a name was given, run `curl -sL "https://<likely-domain>/robots.txt"` to confirm the site exists and find the sitemap. If that 404s, do a quick web search for `"<company name>" official website` to get the correct domain.

---

## Step 2 — Find the sitemap

From the robots.txt, extract the `Sitemap:` line(s). Common patterns:
- Single sitemap: `Sitemap: https://example.com/sitemap.xml`
- Sitemap index: multiple `Sitemap:` lines, or a sitemap-index.xml that references sub-sitemaps

If no sitemap is in robots.txt, try these fallbacks in order:
```
/sitemap.xml
/sitemap_index.xml
/sitemap-index.xml
/blog/sitemap.xml
```

---

## Step 3 — Count blog posts

Fetch the sitemap and count URLs that are blog posts. Use this bash pattern:

```bash
curl -sL -A "Mozilla/5.0" "https://example.com/sitemap.xml" \
  | grep -o '<loc>[^<]*</loc>' \
  | grep -iE '/blog/|/posts?/|/articles?/|/news/' \
  | grep -v -E '^<loc>https://[^/]+/blog/?</loc>$' \
  | wc -l
```

**Important:** Exclude the blog index page itself (e.g. `/blog` or `/blog/`) — count only individual post URLs.

**Sitemap index handling:** If the sitemap is an index (contains `<sitemap>` tags rather than `<url>` tags), extract the sub-sitemap URLs and fetch the blog-specific one:
```bash
curl -sL -A "Mozilla/5.0" "https://example.com/sitemap-index.xml" \
  | grep -o '<loc>[^<]*</loc>' \
  | grep -i 'blog'
# Then fetch that sub-sitemap and count
```

**JS-rendered sites:** Some blog pages render via JavaScript and may not expose counts through sitemaps. In that case, fall back to `site:example.com/blog` search operator to estimate.

**Edge cases:**
- Some sites use `/resources/`, `/insights/`, `/learn/`, or `/hub/` instead of `/blog/` — check the sitemap structure if a `/blog/` grep returns 0.
- If the sitemap is very large (>1MB), grep for multiple blog path patterns.

---

## Step 4 — Build the output

Once all counts are collected, produce a ranked table with the target company highlighted:

```
Blog Post Count — [Target] vs Competitors
==========================================

Rank  Company          Posts   URL
────  ───────────────  ──────  ──────────────────────
 1    Hackmamba        137     hackmamba.io           ← COMPETITOR
 2    Infrasity        137     infrasity.com          ← COMPETITOR  
 3  ▶ Kubiya           95      kubiya.ai              ← TARGET
 4    Orgn             7       orgn.com               ← COMPETITOR

▶ = your company   Total companies analysed: 4
```

Then add a brief summary:
- Where the target ranks (e.g. "3rd out of 4")
- Gap to the leader (e.g. "42 posts behind the top competitor")
- Gap to the one above (if not already #1)
- Any notable observations (e.g. very new site, or tied for first)

---

## Content Freshness Audit (blog posts only)

Run this audit whenever the user asks about content freshness, recency, publishing cadence, or when it adds useful context to the blog count comparison.

### Step 5 — Extract blog post lastmod dates

For each domain, extract only blog post URLs and their `lastmod` dates from the sitemap:

```bash
curl -sL "https://example.com/sitemap.xml" \
  | python3 -c "
import sys, re
content = sys.stdin.read()
urls = re.findall(r'<url>(.*?)</url>', content, re.DOTALL)
for u in urls:
    loc = re.search(r'<loc>(.*?)</loc>', u)
    lastmod = re.search(r'<lastmod>(.*?)</lastmod>', u)
    if loc and lastmod:
        l = loc.group(1)
        if re.search(r'/blog/|/posts?/|/articles?/|/news/', l) and not re.match(r'https?://[^/]+/(blog|posts?|articles?|news)/?$', l):
            print(lastmod.group(1), l)
"
```

### Step 6 — Detect build-time stamp inflation

Before treating lastmod dates as real signals, check whether they are genuine per-post edit dates or build-time bulk stamps:

```python
from datetime import datetime, timezone

dates = [...]  # all lastmod values for blog posts

unique_dates = set(d[:10] for d in dates)  # compare date part only
if not dates:
    stamp_type = "UNKNOWN"
elif len(unique_dates) <= 3:
    # Likely build-time stamps — flag as unreliable
    stamp_type = "BUILD-TIME"
else:
    stamp_type = "REAL"
```

**Build-time stamps** = all (or nearly all) blog posts share the same date, usually within a narrow time window (seconds to minutes). This is common with Next.js/Vercel and similar SSG frameworks that regenerate the sitemap on every deploy. These dates do NOT reflect when content was actually written or updated.

**Real dates** = each post has a distinct lastmod that varies across weeks or months. These are trustworthy freshness signals.

Always flag build-time stamps clearly in the output so the user understands the dates are not meaningful for SEO or content analysis.

### Step 7 — Compute freshness buckets

Using today's date, bucket each blog post's lastmod into:

| Bucket | Age |
|--------|-----|
| Last 30 days | < 30 days old |
| 30–90 days | 30–89 days old |
| 91–180 days | 90–179 days old |
| 181–365 days | 180–364 days old |
| Over 365 days | 365+ days old |

```python
from datetime import datetime, timezone

today = datetime.now(timezone.utc)
buckets = {"<30d": 0, "30-90d": 0, "91-180d": 0, "181-365d": 0, ">365d": 0}

for date_str in lastmod_dates:
    dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    days = (today - dt).days
    if days < 30: buckets["<30d"] += 1
    elif days < 90: buckets["30-90d"] += 1
    elif days < 180: buckets["91-180d"] += 1
    elif days < 365: buckets["181-365d"] += 1
    else: buckets[">365d"] += 1
```

Also compute:
- **Newest post date** and days since
- **Oldest post date**
- **Monthly publishing cadence** — group posts by `YYYY-MM` to show volume over time
- **Days since last publish** — the key staleness metric

### Step 8 — Freshness output

Produce a per-domain freshness summary alongside (or below) the blog count table. Use the visualiser to render a side-by-side comparison widget when comparing multiple domains. The widget must show:

1. **Stamp type badge** — "Build-time stamps ⚠️" or "Real dates ✓"
2. **Key stats** — total posts, newest post date, days since newest, unique date count
3. **Freshness bar chart** — one bar per bucket showing count and percentage
4. **Monthly publishing activity** — small bar chart by month (blog posts only, last 12 months)
5. **Alert banners**:
   - Build-time stamps → warning banner explaining the dates are not real edit dates
   - No posts in 90+ days → warning banner flagging the content gap
   - Real dates with recent posts → info banner confirming trustworthy signal

**SEO freshness interpretation to include in the summary:**
- Build-time stamps: note that Google ignores inflated lastmod dates and they provide no freshness signal
- Real dates, posts < 30 days: strong freshness signal, good for SEO
- Real dates, no posts 90+ days: content gap, likely losing freshness ranking signals to competitors who publish regularly
- Real dates, bulk publish spike followed by drop: flag the pattern (migration or sprint, not sustained cadence)

---

## Notes (Workflow A)

- Always count from the sitemap — it's the most accurate and complete source.
- Robots.txt is always the first place to look for the sitemap URL.
- The `/blog` index page should never be counted as a post.
- If a company has no blog section at all, report 0 and note it.
- Sitemap data can lag real-time by days; note this if relevant.
- Run all company lookups in sequence (one bash block per company) to avoid hitting rate limits.
- For freshness: always filter to blog post URLs only — exclude static pages, service pages, glossary, etc.
- Never treat build-time stamps as real freshness data. Always detect and flag them.

---

---

# WORKFLOW B — Keyword Mapping

Maps a competitor's organic keyword footprint against a target domain to surface content gaps and ranking opportunities.

---

## Step 1 — Pull domain metrics

Pull `org_keywords` and `org_traffic` for both competitor and target via Ahrefs `site-explorer-metrics`:

```
tool: site-explorer-metrics
params:
  target: <domain>
  mode: subdomains
  date: <latest>
  select: org_keywords, org_traffic
```

Do this for both domains. The `org_keywords` count tells you how many batches you'll need to capture the full keyword set.

---

## Step 2 — Pull competitor keywords

Pull the competitor's full keyword set using Ahrefs `site-explorer-organic-keywords` with these fixed filters:

```
tool: site-explorer-organic-keywords
params:
  target: <competitor domain>
  country: us
  mode: subdomains
  is_branded: false
  is_informational: true
  limit: 500
  select: keyword, volume, best_position, sum_traffic, best_position_url, is_branded
```

**Pull multiple batches** using different `order_by` values to maximize coverage:
- Batch 1: `order_by: sum_traffic:desc`
- Batch 2: `order_by: volume:desc`
- Batch 3: `order_by: best_position:asc`

After each batch, deduplicate by keyword across all batches collected so far. Keep the entry with the lowest (best) `best_position` per keyword.

Continue batching until no new keywords appear across two consecutive batches, or until batch count exceeds the expected keyword universe from Step 1.

---

## Step 3 — Pull target keywords

Exact same pull for the target domain — same filters, same multiple sort orderings, same deduplication logic.

```
tool: site-explorer-organic-keywords
params:
  target: <target domain>
  country: us
  mode: subdomains
  is_branded: false
  is_informational: true
  limit: 500
  select: keyword, volume, best_position, sum_traffic, best_position_url, is_branded
```

Store the result as a lookup map: `{ keyword → { best_position, sum_traffic, best_position_url } }`

---

## Step 4 — Cross-reference

For each competitor keyword from Step 2, look it up in the target map from Step 3. Assign a status:

**Both rank:**
- `WINNING` — target position < competitor position (target is ahead)
- `IMPROVE` — competitor position < target position (competitor is ahead)

**Target does not rank:**
- `CRITICAL` — volume ≥ 1,000
- `HIGH` — volume 500–999
- `MEDIUM` — volume 200–499
- `LOW` — volume 100–199
- `NEW` — volume < 100

Each row in the output represents one competitor keyword. Fields per row:
- `keyword`
- `volume`
- `competitor_rank` (best_position)
- `competitor_traffic` (sum_traffic)
- `target_rank` (best_position, or null)
- `target_traffic` (sum_traffic, or null)
- `target_url` (best_position_url, or null)
- `status`

---

## Notes (Workflow B)

- Rows = competitor keywords only. The report answers: *"where is the competitor getting organic traction that the target has no presence?"*
- The `is_branded=false` and `is_informational=true` filters are applied at pull time — not as post-processing. This keeps the dataset clean from the start.
- Both competitor and target keyword pulls use identical filter parameters so the comparison is symmetric.
- If a target keyword exists in the map but the competitor keyword lookup returns null, that competitor keyword was not captured — it may be outside the top 100 positions Ahrefs tracks.
- Stat card counts must reflect the filtered (non-branded, informational) dataset only.

---

---

# COMBINED HTML REPORT

Both workflows feed into a single HTML report file. Run Workflow A and Workflow B fully first, collect all data, then generate the report in one pass.

---

## Report structure (top to bottom)

### 1. Header
- Dark background (#0f1117)
- Report title: `[Target] vs [Competitor] — Content & Keyword Report`
- Subtitle: target domain · competitor domain · date · filters applied
- Two domain pills: target (green dot) and competitor (red dot) showing `org_keywords` and `org_traffic` for each

### 2. Blog Post Count Section
- Section heading: "Blog Post Volume"
- Ranked table: Rank · Company · Posts · URL · Target/Competitor label
- Target row highlighted
- Summary line: where target ranks, gap to leader, gap to one above

### 3. Content Freshness Section
- Section heading: "Content Freshness"
- One card per domain showing:
  - Stamp type badge (Build-time ⚠️ or Real dates ✓)
  - Total posts
  - Newest post date + days since
  - Freshness bucket breakdown (bar per bucket)
  - Monthly publishing activity (last 12 months, bar chart)
  - Alert banner if no posts in 90+ days or build-time stamps detected

### 4. Keyword Mapping Section
- Section heading: "Keyword Gap — [Competitor] vs [Target]"
- Stat cards: All · Winning · Improve · Critical · High · Medium · Low · New (counts, clickable filters)
- Single table, one row per competitor keyword:
  - Keyword · Volume bar · Competitor Rank · Competitor Traffic · Target Rank · Target Traffic · Target URL · Status badge
- Default sort: competitor traffic descending
- Sortable on all columns by clicking headers

### 5. Footer
- Data sources: Ahrefs API (keyword data) · Sitemap (blog counts)
- Date of data pull
- Filters: US · non-branded · informational intent

---

## Styling

- **Fonts:** DM Sans (body) + DM Mono (numbers, badges, monospace values)
- **Header:** #0f1117 background, #edeae3 text, #7a8190 subtitles
- **Body background:** #f7f6f2
- **Cards/tables:** #ffffff background, #e4e2db borders, #faf9f6 table header rows
- **Status badge colours:**
  - WINNING — green (#14724e bg: #e5f5ee)
  - IMPROVE — orange (#994d00 bg: #fff0e0)
  - CRITICAL — red (#c0392b bg: #fce8e6)
  - HIGH — amber (#b85c00 bg: #fdf0e0)
  - MEDIUM — yellow (#7c5c00 bg: #fdf7e0)
  - LOW — teal (#1a6e7a bg: #e0f4f7)
  - NEW — grey (#555 bg: #efefef)
- **Rank colours:** pos 1–3 green · pos 4–6 mid-green · pos 7–10 orange · pos 11+ red
- **Volume bar:** 3px height, scaled to max volume in dataset, muted fill (#ccc8be)
- All sections separated by visible dividers with section labels in DM Mono uppercase

---

## Generation rules

- Collect all data from Workflow A and Workflow B before writing any HTML
- Inject all data as inline JavaScript arrays — no external data fetches at render time
- Single self-contained `.html` file — no external dependencies except Google Fonts CDN
- Save to `/mnt/user-data/outputs/report-[target]-vs-[competitor].html`
- Present with `present_files` after saving
---
name: no-outlinks-audit
description: >
  Runs a full dead-end page audit for any website. Discovers all blog/content pages,
  detects which ones have zero outgoing links to any URL on the same domain, fetches
  keywords, clusters pages by topic, and generates 3 outgoing link suggestions per
  dead-end page with anchor text, placement guidance, and ready-to-paste context copy.
  Outputs a styled HTML report matching report-style-reference.html. Automatically
  detects site framework (Next.js, static, WordPress) and uses the correct detection
  method: RSC header for Next.js/Vercel sites, standard curl for static and traditional
  CMS sites. Trigger when a user provides a domain or URL and asks for a dead-end page
  audit, outgoing internal links audit, "which pages don't link out", "find pages with
  no internal links in the content", "pages that are link dead-ends", or any variation
  of finding pages that have zero outgoing links to the same domain. Always use this
  skill for dead-end page audits — never attempt the workflow without following every
  step here.
---

# SKILL: Dead-End Pages — No Outgoing Internal Links Audit

## DESCRIPTION

Finds every blog/content page on a site that has **zero outgoing links to any URL on
the same domain** in its body content. These pages absorb link equity but pass none
on — they are structural dead-ends that silently suppress topical authority and hurt
crawl efficiency across the site.

For each dead-end page the skill generates 3 suggestions: pages on the same site that
the dead-end page SHOULD link out to, including the exact anchor text (the target
page's top keyword), where in the dead-end page to place the link, and a ready-to-paste
context copy sentence with the link already embedded.

This skill is the structural inverse of the Orphan Pages skill:
- **Orphan Pages**:   pages with no *incoming* internal links (nobody links TO them)
- **Dead-End Pages**: pages with no *outgoing* internal links (they link out to nobody)

---

## TOOLS

- Step 1 uses **curl via bash_tool** for sitemap discovery
- Step 2 uses **curl via bash_tool** for framework detection
- Step 3 uses **curl via bash_tool** for outgoing link detection (method varies by framework)
- Step 5 uses **Ahrefs MCP** (`site-explorer-top-pages`) for keyword research

---

## WORKFLOW

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 1 — DISCOVER ALL PAGES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

WHY THIS STEP EXISTS
You need a complete list of all blog/content pages to check. Curl-based sitemap
discovery is fast, free, and reflects the live site — not a stale crawl cache.

SUBSTEP 1A — FIND THE SITEMAP

Run in order until one returns valid XML:

```bash
curl -sL --max-time 15 "https://www.DOMAIN.com/sitemap.xml" | head -50
curl -sL --max-time 15 "https://www.DOMAIN.com/sitemap_index.xml" | head -50
curl -sL --max-time 15 "https://www.DOMAIN.com/robots.txt" | grep -i sitemap
```

If none work, crawl the blog index directly:
```bash
curl -sL "https://www.DOMAIN.com/blog/" | grep -oP 'href="[^"]*"' | grep '/blog/'
```

SUBSTEP 1B — EXTRACT ALL CONTENT URLS

```bash
curl -sL "https://www.DOMAIN.com/sitemap.xml" \
  | grep -oP '(?<=<loc>)[^<]+' \
  | grep '/blog/' \
  | grep -v '/blog/$' \
  | grep -v '/page/' \
  | sort -u > /tmp/blog_urls.txt

wc -l /tmp/blog_urls.txt
```

Call this LIST_ALL. Record TOTAL_PAGES = length of LIST_ALL.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 2 — DETECT SITE FRAMEWORK
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

WHY THIS STEP EXISTS
The detection method for outgoing links depends entirely on how the site renders HTML.
Running the wrong method gives completely wrong results — this step prevents that.

Run both checks:

```bash
# Check response headers
curl -sI "https://www.DOMAIN.com" | grep -i "x-powered-by\|x-nextjs\|x-vercel\|server\|generator"

# Check HTML source for framework signals
curl -sL "https://www.DOMAIN.com" \
  | grep -o 'name="generator"[^>]*\|__NEXT_DATA__\|_next\|__nuxt\|ng-version\|gatsby'
```

DECISION TABLE:

| Signal found                          | Framework        | Method       |
|---------------------------------------|------------------|--------------|
| x-nextjs-prerender in headers         | Next.js          | Step 3A      |
| _next or __NEXT_DATA__ in HTML        | Next.js          | Step 3A      |
| x-vercel-cache in headers + _next     | Next.js/Vercel   | Step 3A      |
| gatsby in HTML source                 | Gatsby (SSG)     | Step 3B      |
| name="generator" content="WordPress"  | WordPress        | Step 3B      |
| x-powered-by: PHP                     | Traditional CMS  | Step 3B      |
| Static HTML (<a> tags present)        | Static/SSG       | Step 3B      |
| Zero <a> tags in curl response        | Unknown SPA      | Step 3C      |
| __nuxt in HTML                        | Nuxt.js          | Step 3C      |

IMPORTANT: Always test the detection method on 3 sample pages before running the
full list. Verify that a page you know has links returns links, and a page you
know is sparse returns few/none. If results look wrong, re-read this step.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 3 — DETECT OUTGOING INTERNAL LINKS PER PAGE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Run the method determined in Step 2.

────────────────────────────────────────
STEP 3A — NEXT.JS SITES (RSC HEADER METHOD)
────────────────────────────────────────

HOW IT WORKS
Next.js with React Server Components exposes a server-rendered payload endpoint.
By sending `RSC: 1` as a request header, the server returns the full rendered page
data as a serialised React component tree — including all links — without needing
a headless browser. This works on all Next.js sites using the App Router (Next.js 13+).

This is the correct method for any site running on Next.js / Vercel, regardless of
whether it uses ISR, SSG, or SSR. The RSC payload always contains the rendered
content with all internal links visible as plain text paths.

HOW TO VALIDATE THE FETCH WORKED
A valid RSC response:
- Is always larger than 10KB (most blog posts return 50KB–250KB)
- Starts with React markers like `$Sreact.fragment` or `J:` or `1:"$`
- If a page returns less than 10KB or has no `$` in the first 500 chars,
  the fetch failed — flag that page for manual review, do NOT mark it as a dead-end

```python
import subprocess, re, time

domain = "DOMAIN.com"        # without www, e.g. "infrasity.com"
blog_prefix = "/blog/"       # content prefix, e.g. "/blog/"

with open('/tmp/blog_urls.txt') as f:
    urls = [u.strip() for u in f if u.strip()]

# Asset extensions to exclude — these are not outgoing content links
SKIP_EXT = (
    '.png','.webp','.jpg','.jpeg','.gif','.svg','.ico',
    '.woff2','.woff','.ttf','.eot','.otf',
    '.css','.js','.jsx','.ts','.tsx',
    '.xml','.txt','.pdf','.zip','.mp4','.mp3','.webm'
)

# Path prefixes to exclude — assets, CDN, internal Next.js paths
SKIP_PREFIX = (
    '/PostImages/', '/images/', '/fonts/', '/favicon',
    '/_next/', '/_vercel/', '/static/',
    '/api/', '//cdn.', '//assets.'
)

def get_outgoing_links(url):
    result = subprocess.run([
        'curl', '-sL', '--max-time', '10',
        '-H', 'RSC: 1',
        '-H', 'Next-Router-State-Tree: %5B%22%22%2C%7B%22children%22%3A%5B%22__PAGE__%22%2C%7B%7D%5D%7D%2Cnull%2Cnull%2Ctrue%5D',
        url
    ], capture_output=True, text=True, timeout=15)

    data = result.stdout

    # Validate RSC fetch succeeded
    if len(data) < 10000 or not any(m in data[:500] for m in ['$S', 'J:', '1:"']):
        return None  # Fetch failed — flag for manual review

    # Extract all paths pointing to the same domain
    # Extract both absolute domain links and relative paths starting with /
    # (excluding protocol-relative links starting with //)
    raw = re.findall(
        rf'(?:(?:https?://)?(?:www\\.)?{re.escape(domain)}|(?<!/))/(?!/)([^\\s\"\\\'\\\\),\\]]+)',
        data
    )
    raw = ['/' + r for r in raw]

    clean = set()
    for l in raw:
        # Normalise: strip trailing junk
        l = l.split('\\')[0].split('"')[0].split("'")[0].rstrip('),.]\\/')
        if len(l) < 2:
            continue
        # Exclude assets
        if any(l.lower().endswith(e) for e in SKIP_EXT):
            continue
        if any(l.startswith(p) for p in SKIP_PREFIX):
            continue
        # Exclude self-link
        slug = url.rstrip('/').split('/')[-1]
        if l.rstrip('/') == blog_prefix.rstrip('/') + '/' + slug:
            continue
        clean.add(l)

    return clean

dead_ends = []
has_outlinks = []
failed = []

for i, url in enumerate(urls):
    slug = url.split('/')[-1]
    try:
        links = get_outgoing_links(url)
        if links is None:
            failed.append(url)
            print(f"[{i+1:3d}] FAILED   {slug}")
        elif len(links) == 0:
            dead_ends.append(url)
            print(f"[{i+1:3d}] DEAD-END {slug}")
        else:
            has_outlinks.append(url)
            print(f"[{i+1:3d}] LINKS({len(links):2d}) {slug}")
    except Exception as e:
        failed.append(url)
        print(f"[{i+1:3d}] ERROR    {slug}: {e}")
    time.sleep(0.15)

with open('/tmp/dead_end_urls.txt', 'w') as f:
    f.write('\n'.join(dead_ends))

print(f"\nTotal:         {len(urls)}")
print(f"Dead-ends:     {len(dead_ends)}")
print(f"Has outlinks:  {len(has_outlinks)}")
print(f"Failed:        {len(failed)} (verify manually)")
print(f"Dead-end rate: {round(len(dead_ends)/len(urls)*100)}%")
```

────────────────────────────────────────
STEP 3B — STATIC / WORDPRESS / TRADITIONAL CMS (STANDARD CURL)
────────────────────────────────────────

HOW IT WORKS
For sites that serve fully-rendered HTML directly (static files, WordPress, Gatsby,
traditional CMS), standard curl fetches the complete page including all links.
Parse only the main content area to exclude nav/footer/sidebar links.

```python
import subprocess, re, time
from urllib.parse import urljoin

domain = "DOMAIN.com"
base = "https://www." + domain

with open('/tmp/blog_urls.txt') as f:
    urls = [u.strip() for u in f if u.strip()]

SKIP_EXT = (
    '.png','.webp','.jpg','.jpeg','.gif','.svg','.ico',
    '.woff2','.css','.js','.xml','.pdf','.zip'
)

def get_outgoing_links(url):
    result = subprocess.run([
        'curl', '-sL', '--max-time', '10',
        '-A', 'Mozilla/5.0 (compatible; InternalLinkBot/1.0)',
        url
    ], capture_output=True, text=True, timeout=15)

    html = result.stdout

    # Extract main content area only
    content = ''
    for tag in ['article', 'main', 'body']:
        m = re.search(rf'<{tag}[^>]*>(.*?)</{tag}>', html, re.DOTALL | re.IGNORECASE)
        if m:
            content = m.group(1)
            break
    if not content:
        content = html

    hrefs = re.findall(r'<a\\s+[^>]*href\\s*=\\s*["\']([^"\'\\ ]+)["\']', content, re.IGNORECASE)

    clean = set()
    for href in hrefs:
        href = href.strip()
        if not href or href.startswith('#') or href.startswith('mailto:') or href.startswith('tel:'):
            continue
        abs_url = urljoin(base, href)
        if domain not in abs_url:
            continue
        path = '/' + abs_url.split(domain, 1)[-1].lstrip('/')
        if any(path.lower().endswith(e) for e in SKIP_EXT):
            continue
        if abs_url.rstrip('/') == url.rstrip('/'):
            continue
        clean.add(path)
    return clean

dead_ends = []
has_outlinks = []

for i, url in enumerate(urls):
    slug = url.split('/')[-1]
    links = get_outgoing_links(url)
    if links:
        has_outlinks.append(url)
        print(f"[{i+1:3d}] LINKS({len(links):2d}) {slug}")
    else:
        dead_ends.append(url)
        print(f"[{i+1:3d}] DEAD-END {slug}")
    time.sleep(0.2)

with open('/tmp/dead_end_urls.txt', 'w') as f:
    f.write('\n'.join(dead_ends))

print(f"\nTotal:         {len(urls)}")
print(f"Dead-ends:     {len(dead_ends)}")
print(f"Has outlinks:  {len(has_outlinks)}")
print(f"Dead-end rate: {round(len(dead_ends)/len(urls)*100)}%")
```

────────────────────────────────────────
STEP 3C — UNKNOWN / PURE SPA — FLAG TO USER
────────────────────────────────────────

If framework detection is inconclusive (e.g. Nuxt.js, Angular, Vue SPA) or if
curl returns fewer than 10 `<a>` tags across 3 sample pages, stop and tell the user:

"This site appears to use client-side rendering that cannot be detected through
standard curl requests. To run this audit accurately, one of the following is needed:

1. Set up an Ahrefs Site Audit project for this domain (uses a headless browser
   that renders JS). Share the project ID once the first crawl completes.
2. Export a crawl from Screaming Frog with JavaScript rendering enabled and
   provide the CSV of internal links.
3. Confirm the exact framework being used so the right detection header can be applied.

Do not proceed to generate a report until the detection method is confirmed working
on at least 5 sample pages."

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 4 — VALIDATE RESULTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

WHY THIS STEP EXISTS
Detection bugs are silent. A misconfigured asset filter or a failed fetch can
silently produce a wrong dead-end list. This step catches that before suggestions
are generated.

Do ALL of the following before proceeding:

1. Pick 3 random pages from LIST_DEAD_ENDS. Open each in a browser and manually
   confirm the page genuinely has no outgoing links to the domain. If any DO have
   links, re-check the detection script's asset filter and domain pattern.

2. Pick 3 pages from LIST_HAS_OUTLINKS. Verify they have visible links in the browser
   to other pages on the same domain.

3. If DEAD_END_RATE > 80%, something is likely wrong — the fetch may be returning
   only asset links or the domain pattern may not be matching. Debug before continuing.

4. If DEAD_END_RATE is 0%, the filter may be too loose (counting assets or self-links).
   Check what links are being detected on known-sparse pages.

5. For Step 3A (Next.js): if the failed list is non-empty, manually check those
   pages. Some may genuinely be dead-ends; others may have errored. Re-run failed
   pages individually before finalising the list.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 5 — KEYWORD RESEARCH
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

WHY THIS STEP EXISTS
To generate relevant outgoing link suggestions you need to know what each dead-end
page AND each potential target page is about. One Ahrefs call covers the full blog.

TOOL: `Ahrefs:site-explorer-top-pages`

PARAMETERS:
- `target`: blog prefix (e.g. `www.DOMAIN.com/blog/`)
- `mode`: `prefix`
- `date`: today's date YYYY-MM-DD
- `select`: `url,top_keyword,sum_traffic`
- `limit`: 500
- `order_by`: `sum_traffic:desc`

RESULT: MAP_KEYWORDS — a keyword and traffic map for all pages.

For any dead-end page not in MAP_KEYWORDS, derive keyword from URL slug:
replace hyphens with spaces. NEVER fabricate traffic numbers — use null.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 6 — CLUSTER AND GENERATE SUGGESTIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

WHY THIS STEP EXISTS
Outgoing link suggestions must be topically relevant to the dead-end page. Clustering
first, then matching within and across clusters, produces natural and useful suggestions.

HOW TO CLUSTER
Group all dead-end pages by primary topic using their keyword and title. Create 5–15
clusters depending on the site's content breadth. Adapt cluster names to the actual
content — do not use generic names like "Misc" or "Other" unless truly necessary.

HOW TO GENERATE SUGGESTIONS
For each dead-end page, identify 3 pages from LIST_ALL (any page on the site, not
only other dead-ends) that:

1. Are topically related — same or adjacent subject matter
2. Would be a natural next step for a reader of the dead-end page
3. Are ideally already well-linked pages — so the dead-end connects into the
   broader internal link graph

For each of the 3 suggestions, provide:

ANCHOR TEXT
The top keyword of the TARGET page (the page being linked TO). Rules:
- Use the `kw` field from MAP_KEYWORDS for the target page
- If target has no keyword data, derive from its URL slug
- Must read naturally as hyperlinked text in a sentence
- No em dashes (—) in or around the anchor text

WHERE TO PLACE
A specific section-level description of where in the DEAD-END page to insert
the outgoing link. Rules:
- Section-level specific, not just "somewhere in the article"
- Contextually logical — where a reader would naturally want to go deeper
- Examples:
  "In the intro when defining the core concept"
  "After the comparison table when suggesting next steps"
  "In the Tools and Resources section at the end"
  "When first mentioning [adjacent topic] mid-article"

SUGGESTED CONTEXT COPY
A ready-to-paste sentence (1–2 sentences max) to drop directly into the dead-end
page at the placement location. Rules:
- Must contain the anchor text as a real HTML hyperlink to the TARGET page URL:
  <a href="[target_url]">[target_kw]</a>
- Must read naturally in the context described in WHERE TO PLACE
- Must add genuine value — not just "click here to learn more"
- Should feel written for the dead-end page's specific voice and section
- 15–35 words total (excluding HTML tags)
- No em dashes (—) anywhere in the copy. Replace any em dash with a comma
  or restructure the sentence entirely
- Examples:
  "If you are just getting started, a clear overview of <a href="...">developer
   marketing strategy</a> will give you the framework to make these tactics work."
  "Teams that combine this with a solid <a href="...">b2b content marketing
   strategy</a> see compounding returns across both organic traffic and pipeline."

Store this as the `copy` field in each suggestion object in D[].

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STEP 7 — GENERATE HTML REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

BEFORE WRITING ANY CODE read:
  → references/report-style-reference.html

The reference file is the single source of truth for all CSS variables, typography,
component styles, spacing values, and JavaScript patterns. Do not invent new styles.
Do not substitute different values. Copy them exactly from the reference.

REPORT HEADER VALUES

```
Site URL:        https://www.DOMAIN.com/blog/
Total Blogs:     TOTAL_PAGES
No Outlinks:     DEAD_END_COUNT        ← red stat (fail)
Have Outlinks:   PAGES_WITH_OUTLINKS   ← green stat (pass)
Dead-End Rate:   DEAD_END_RATE%        ← amber stat (warn)
Suggestions:     DEAD_END_COUNT × 3   ← indigo stat (accent)
```

Fix-tag (choose based on method used):
- Next.js:     `⚑ RSC payload detection (Next.js) · YYYY-MM-DD`
- Static/WP:   `⚑ Curl HTML parse · YYYY-MM-DD`
- Site Audit:  `⚑ Ahrefs Site Audit (project ID: XXXX) · YYYY-MM-DD`

REPORT FOOTER:
`DOMAIN.com · Dead-End Pages Audit · YYYY-MM-DD / Source: [detection method]`

SUGGESTION CARD LABELS (different from orphan skill)
- "Link To"        — the target page (page to link out TO)
- "Anchor Text"    — the target page's top keyword
- "Where to Place" — section in the dead-end page
- "Context Copy"   — ready-to-paste sentence with link embedded

DATA STRUCTURE — D[] array

One object per dead-end page:

```javascript
{
  url:     "https://www.DOMAIN.com/blog/page-slug",  // dead-end page URL
  title:   "Page Title",                              // display title
  kw:      "top keyword",                             // dead-end page's own keyword
  tr:      123,                                       // monthly traffic or null
  cluster: "Cluster Name",                            // must match a key in CC{}
  s: [
    {
      from:    "Target Page Title",                   // page to link OUT TO
      fromUrl: "https://www.DOMAIN.com/blog/target",  // target URL
      anchor:  "target page keyword",                 // target's top keyword
      place:   "Where in the dead-end page to add the link",
      copy:    "Sentence with <a href=\"...\">target keyword</a> embedded."
    },
    // × 3 per dead-end page
  ]
}
```

NOTE ON FIELD SEMANTICS
`from` and `fromUrl` refer to the TARGET page (the page being linked TO), not the
source page. This is the opposite direction from the orphan skill. The JS card
builder must label these as "Link To" not "Source Page":

```javascript
// In the suggestion card builder:
`<div class="sug-from-label">Link To</div>
 <div class="sug-from-title">${s.from}</div>
 <a class="sug-from-url" href="${s.fromUrl}" target="_blank">...</a>`
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STRICT RULES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. READ references/report-style-reference.html BEFORE writing any HTML or CSS.
   Mandatory — no exceptions.

2. ALWAYS run Step 2 (framework detection) before any link detection. Never assume
   the framework based on the domain name or a visual inspection of the site.

3. For Next.js sites, ALWAYS use the RSC header method (Step 3A). Never use standard
   curl on a Next.js site — it returns an empty JS shell and produces wrong results.

4. ALWAYS validate RSC fetch success per page. A response under 10KB or missing
   React markers means the fetch failed. Flag those pages, never silently mark them
   as dead-ends.

5. NEVER count asset links (images, fonts, scripts, stylesheets) as qualifying
   outgoing links. A page that only links to /logo.png and /styles.css is a dead-end.

6. NEVER count self-links (the page linking to itself) as a qualifying outgoing link.

7. ALWAYS validate results on sample pages (Step 4) before generating suggestions.
   If the dead-end rate is above 80% or exactly 0%, something is wrong — debug first.

8. ANCHOR TEXT = top keyword of the TARGET page, not the dead-end page.

9. NEVER use em dashes (—) in SUGGESTED CONTEXT COPY. Replace with a comma or
   restructure the sentence.

10. ALWAYS produce exactly 3 suggestions per dead-end page. No more, no fewer.

11. ALWAYS make the dead-end page URL and all 3 target page URLs clickable
    `<a href>` links opening in `target="_blank"`.

12. NEVER deviate from the CSS values in report-style-reference.html.

13. ALWAYS build the report data-driven using D[] and CC[]. Never write static HTML
    for individual blog cards.

14. ALWAYS clean LIST_DEAD_ENDS before generating suggestions. Remove non-200 pages,
    pagination, tag/category pages, and any URL that is not a standalone post.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
EDGE CASES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

NEXT.JS APP ROUTER vs PAGES ROUTER
RSC header works on App Router (Next.js 13+). For older Pages Router sites, the
RSC payload may not be available. Test signal: if response is under 10KB consistently
across multiple pages, the site may be using Pages Router. Fall back to checking
for __NEXT_DATA__ in the standard HTML response — this contains the serialised
page props and may include link data.

SITE USES A CDN THAT STRIPS HEADERS
Some CDN configurations strip custom request headers before they reach the origin.
If RSC responses consistently return under 10KB, test by adding a cache-busting
query param: `?_rsc=1` appended to the URL. If that also fails, the CDN is likely
stripping the RSC header — fall back to the __NEXT_DATA__ approach.

LARGE SITES (200+ PAGES)
For sites with more than 200 blog pages, run the detection in batches of 50 with
a 0.3s delay between requests to avoid rate limiting. Prioritise the top-traffic
pages from MAP_KEYWORDS first. If time is a constraint, audit the top 100 pages
by traffic and note in the report that the audit covers the top 100.

ALL PAGES ARE DEAD-ENDS (RATE = 100%)
This means the detection failed entirely — either the domain pattern is wrong or
the asset filter is too aggressive. Run the debug check: print the raw links found
on 3 known-linked pages. If nothing appears, fix the regex. If only assets appear,
widen the SKIP_EXT/SKIP_PREFIX rules.

DEAD-END RATE IS 0%
Every page appears to have outgoing links. The filter may be too loose — possibly
counting nav or footer links. Add `is_content` filtering by restricting the link
search to only the `<article>` or `<main>` tag content area.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
COMPUTING FINAL METRICS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TOTAL_PAGES          = len(LIST_ALL)
DEAD_END_COUNT       = len(LIST_DEAD_ENDS)
PAGES_WITH_OUTLINKS  = TOTAL_PAGES - DEAD_END_COUNT
DEAD_END_RATE        = round(DEAD_END_COUNT / TOTAL_PAGES * 100)
TOTAL_SUGGESTIONS    = DEAD_END_COUNT × 3
---
name: landing-page-auditor
description: >
  Audits any landing or service page across 48 checks in 10 categories for LLM/AI discoverability,
  GEO readiness, content clarity, schema markup, internal linking, freshness signals, and technical
  crawlability. Produces an overall score out of 100, a per-category score out of 100, pass/warn/fail/
  manual counts, and a prioritised fix list — all rendered as a standalone HTML report saved to disk.
  Use when a user provides a URL and asks to audit it, score it, check its GEO readiness, test its
  AI discoverability, run a landing page audit, or evaluate it for LLM citation potential.
  Also trigger on phrases like "audit this page", "score this URL", "check GEO for", "is this page
  AI-ready", "run a GEO audit", "LLM page check", "how would AI read this page", or "landing page score".
user-invokable: true
argument-hint: "[url]"
license: MIT
metadata:
  author: Infrasity
  version: "1.0.0"
  category: web-design
---

# Landing Page GEO & LLM Auditor

Audits any landing or service page across 48 checks in 10 categories. Given a URL, fetch all required
data, grade every check, calculate scores per category and overall, then render a standalone HTML report.

---

## Step 0 — Parse and Confirm the URL

If the user provided a URL in the invocation arguments, use it directly. If not, ask:
> "Please provide the URL of the page you'd like to audit."

**Normalisation rules:**
- Ensure the URL starts with `https://`
- Strip trailing slashes
- Keep the full path (e.g. `https://infrasity.com/claude-skills`, not just `infrasity.com`)
- Extract the bare domain for file naming (e.g. `infrasity.com`)
- Extract the domain root for auxiliary files (strip subdomains only if they differ — check both)

Echo back the resolved URL before proceeding:
> "Auditing `{URL}` — fetching data now..."

---

## Step 1 — Fetch All Required Data in Parallel

Run ALL of the following fetches simultaneously. Do not wait for one to complete before starting the next.

### 1a — Page Content Overview (WebFetch pass 1)

Fetch `{URL}` with this prompt:
> "Return the complete text content of the page. Include: all headings (H1, H2, H3, H4) with their exact levels and text, all paragraph text, all list items, the opening sentence and first 150 words of body text (excluding nav), any FAQ section content, testimonial or social proof text, pricing info, stats and numbers, target audience language, comparison language like 'unlike X' or 'instead of', negative scoping like 'not for X', measurable outcome claims like 'reduced X by Y%', all internal links with href and anchor text, all external links with href and anchor text, any visible date or 'last updated' text, any breadcrumb navigation, and any comparison tables."

### 1b — Page Schema and Technical (WebFetch pass 2)

Fetch `{URL}` with this prompt:
> "Return: 1) All JSON-LD schema blocks verbatim including their @type values, 2) All image tags with exact src and alt attributes — list every image, 3) The meta title tag content, 4) The meta description content, 5) The canonical URL from the canonical link tag, 6) The robots meta tag content, 7) Any BreadcrumbList schema, 8) Any Service, ProfessionalService, SoftwareApplication or Product schema, 9) Any FAQPage schema, 10) Whether page content is visible in raw HTML without JavaScript execution."

### 1c — robots.txt (WebFetch)

Fetch `{ROOT_DOMAIN}/robots.txt` with this prompt:
> "Return the complete robots.txt content. List every User-agent entry and its Allow/Disallow rules. Specifically call out rules for: GPTBot, ClaudeBot, PerplexityBot, OAI-SearchBot, and any wildcard User-agent. Note the Sitemap directive URL if present."

### 1d — sitemap.xml (WebFetch)

Fetch `{ROOT_DOMAIN}/sitemap.xml` with this prompt:
> "Check if {FULL_URL} or any variant appears in this sitemap. Return the exact URL match, its lastmod date, changefreq, and priority. Also return the total number of URLs in the sitemap."

If the first sitemap is an index file referencing sub-sitemaps, fetch the most relevant sub-sitemap and repeat the check.

### 1e — llms.txt (WebFetch)

Fetch `{ROOT_DOMAIN}/llms.txt` with this prompt:
> "Return the full content of this llms.txt file. List every URL or path mentioned. Specifically check whether '{PAGE_PATH}' (the path portion of the target URL) or the full URL '{FULL_URL}' appears anywhere in the file."

### 1f — Server Response Time (Bash / curl)

```bash
RESPONSE_MS=$(curl -o /dev/null -s -w "%{time_starttransfer}" --max-time 15 "{URL}" | awk '{printf "%.0f", $1 * 1000}')
echo "TTFB: ${RESPONSE_MS}ms"
```

If curl is unavailable, mark check 10.3 as ⚠ Warning with note "Response time could not be measured."

---

## Step 2 — Grade All 48 Checks

Use the fetched data to evaluate every check below. Assign one of four verdicts:

| Verdict | Symbol | Score Weight | When to use |
|---|---|---|---|
| Pass | ✓ | 1.0 | Clearly present and meets the criteria |
| Warning | ⚠ | 0.5 | Partially present, improvable, or ambiguous |
| Fail | ✗ | 0.0 | Missing, broken, or clearly absent |
| Manual | ○ | Excluded | Requires human review to verify accurately |

Also write a short **evidence note** for each check (1 sentence max) — what you found or didn't find.

---

### Category 1 — Content Clarity & Directness (5 checks)

**1.1 — Clear opening sentence describing the service**

Look at the first sentence of body text (exclude navigation, hero buttons, GitHub badges).

- **Pass:** First sentence clearly states what the product/service is or does
- **Warn:** Opening exists but is preceded by several non-sentence elements (buttons, badges, CTAs) that push it past the visual fold
- **Fail:** No clear opening sentence; page leads with only a tagline, image, or marketing puff

**1.2 — Service definition in first 100 words ('X is a [type] that…')**

Count the first 100 words of actual body copy (strip nav links, CTA button text, icon labels).

- **Pass:** An explicit definitional sentence ("X is a [type] that..." or "X [verb]s [object] so that...") appears within the first 100 words
- **Warn:** Definition exists but appears after 100 words, or it's implied rather than stated
- **Fail:** No definitional sentence found in first 100 words

**1.3 — No unexplained jargon or acronyms**

Scan for acronyms (all-caps sequences 2-5 chars) and technical terms used without definition.

- **Pass:** All acronyms defined on first use (e.g. "GEO (Generative Engine Optimization)"), or no acronyms present
- **Warn:** 1–2 unexplained acronyms/terms but core product concepts are clear
- **Fail:** 3+ acronyms or key terms used without any explanation on first use

**1.4 — Use case statements present ('designed for X', 'ideal for Y teams')**

Look for explicit target audience language.

- **Pass:** "designed for", "built for", "ideal for", "best for", or a named target customer type (company, role, or industry) appears
- **Warn:** Audience implied by content context but never explicitly named
- **Fail:** No use case or target audience language found anywhere on the page

**1.5 — Negative scoping present ('not for X', 'we don't do Z')**

Look for explicit exclusions.

- **Pass:** "not for", "we don't", "not designed for", "excludes", or a clear "do not recommend for" list present
- **Warn:** Scope narrowed implicitly (e.g. only lists technical use cases) but never stated in negative form
- **Fail:** No negative scoping of any kind

---

### Category 2 — Structure & Scannability (5 checks)

**2.1 — Proper H1 → H2 → H3 heading hierarchy**

Check the heading order from the heading list returned in fetch 1a.

- **Pass:** Clean hierarchy — H1 appears once at top; H2s follow; H3s only appear under H2s; no levels skipped
- **Warn:** Minor violations — H4 used once or twice where H3 was expected, or H3 directly after H1 in one section
- **Fail:** Significant violations — H4s appear before H3s in multiple sections, or no clear hierarchy

**2.2 — At least one question-phrased heading**

Scan all headings for text ending with `?`.

- **Pass:** At least one H2 or H3 in the main body content is phrased as a question
- **Warn:** Question headings exist but only in the FAQ section, none in main body
- **Fail:** No question-phrased headings at all

**2.3 — Short paragraphs (avg ≤15 words, no walls of text)**

Estimate average paragraph length from the body text returned.

- **Pass:** Paragraphs appear short; no block of text looks like a wall (>150 words unbroken)
- **Warn:** 1 paragraph that appears to be a wall of text (>150 words), or paragraphs are clearly longer than average
- **Fail:** 2+ walls of text detected, or the majority of body content is in dense paragraph form

**2.4 — Bullet points used for features or benefits**

Count list items from fetch 1a.

- **Pass:** Lists/bullets used for features, benefits, steps, or service items (10+ list items across the page)
- **Warn:** Some lists present but main benefits/features are paragraph-only
- **Fail:** No list elements found on the page

**2.5 — No generic filler opening paragraph**

Check if the opening section is specific and value-dense.

- **Pass:** Opening paragraph is specific, informative, and immediately relevant to the product
- **Warn:** Opening is OK but one paragraph elsewhere on the page is clearly generic filler
- **Fail:** Opening paragraph is vague, generic ("Welcome to our website"), or filled with marketing clichés

---

### Category 3 — Entity & Fact Signal (5 checks)

**3.1 — Brand name mentioned 5 or more times**

Count brand name occurrences in body text.

- **Pass:** Brand name appears 5+ times in body content (not just nav/footer)
- **Warn:** 3–4 occurrences
- **Fail:** Fewer than 3 occurrences

**3.2 — 3+ specific numbers or stats (not just years)**

Look for concrete numbers — percentages, counts, dollar amounts, time estimates (not "2026" or "v3").

- **Pass:** 3+ specific numbers or data points present in body content
- **Warn:** 1–2 specific numbers
- **Fail:** No specific numbers or stats found

**3.3 — Comparison language present ('unlike X', 'instead of', 'alternative to')**

- **Pass:** Explicit comparison language found: "unlike X", "instead of", "alternative to", "compared to", "vs", "rather than"
- **Warn:** Comparative positioning implied by listing differentiators but no explicit comparison language
- **Fail:** No comparison language of any kind

**3.4 — Named service offerings consistently styled (bold or capitalised)**

Check if product/service names are formatted consistently.

- **Pass:** Service names are bold, capitalised, or consistently styled throughout the page
- **Warn:** Service names styled inconsistently (sometimes bold, sometimes plain text)
- **Fail:** No consistent styling applied to named offerings

**3.5 — Pricing shown on page or link to /pricing page**

- **Pass:** Pricing, price range, or starting price visible on page OR a clear link to /pricing page present
- **Warn:** "Contact for pricing", "custom quote", or "book a call" with no numbers or pricing page link
- **Fail:** No pricing information and no pricing page link anywhere on the page

---

### Category 4 — Trust & Authority Signals (4 checks)

**4.1 — Client testimonials or customer quotes**

- **Pass:** Named customer quotes, testimonials with company affiliation, or attributed case study snippets
- **Warn:** Generic social proof language ("trusted by 500+ teams") but no direct quotes
- **Fail:** No testimonials, quotes, or social proof of any kind

**4.2 — Client logos or partner badges**

- **Pass:** Company logos, "as seen in" badges, partner logos, or award badges visually present
- **Warn:** Client company names mentioned in text but no logos
- **Fail:** No visual trust signals (logos, badges, certifications)

**4.3 — Specific measurable outcomes ('reduced X by Y% in N weeks')**

These must be outcomes your service delivered for clients — not stats about your clients' industry.

- **Pass:** At least one quantified client result: "reduced X by Y%", "grew X from A to B", "achieved X in N weeks"
- **Warn:** Qualitative outcomes described ("improved performance", "faster go-to-market") without numbers
- **Fail:** No outcome claims — only feature descriptions

**4.4 — 3+ external links to credible sources**

Count outbound links to authoritative domains (GitHub, research papers, government sites, established industry publications, Wikipedia).

- **Pass:** 3+ credible external links in body content
- **Warn:** 1–2 credible external links
- **Fail:** No credible external links (only social profiles or link farm sites)

---

### Category 5 — FAQ & Schema Signals (5 checks)

**5.1 — FAQ section with question-phrased H2/H3 headings**

- **Pass:** A dedicated FAQ section exists with H2 or H3 headings phrased as actual questions
- **Warn:** FAQ content exists but headings are not phrased as questions ("FAQ", "Common Questions" not qualifying)
- **Fail:** No FAQ section found

**5.2 — JSON-LD Service or ProfessionalService schema**

Check schema from fetch 1b.

- **Pass:** `Service`, `ProfessionalService`, `SoftwareApplication`, or `Product` @type found in JSON-LD
- **Warn:** `Organization` or `WebPage` schema present but no Service-type entity
- **Fail:** No JSON-LD schema at all, or no Service/Product-type schema

**5.3 — JSON-LD FAQPage schema**

- **Pass:** `FAQPage` @type with `Question` and `acceptedAnswer` pairs in JSON-LD
- **Warn:** FAQ content visible on page but no FAQPage schema markup
- **Fail:** No FAQ schema and no FAQ content

**5.4 — Meta title accurately describes the service**

From fetch 1b, check the `<title>` tag.

- **Pass:** Title is 30–60 characters, clearly states the product/service name and primary value prop
- **Warn:** Title present but generic, truncated (>70 chars), or matches only the domain name
- **Fail:** No meta title, or title is blank/placeholder

**5.5 — Canonical URL correctly set**

From fetch 1b, check the `<link rel="canonical">` tag.

- **Pass:** Canonical tag present and points to this exact page URL (or correct www/non-www variant)
- **Warn:** Canonical present but on wrong domain variant (e.g. points to www when page is non-www)
- **Fail:** No canonical tag, or canonical points to the homepage or a different page entirely

---

### Category 6 — Semantic Answer Coverage (5 checks)

**6.1 — What — service clearly explained**

- **Pass:** "X is...", "X allows...", "X [verb]s..." definitional statement present
- **Warn:** Service implied by feature list but never directly defined
- **Fail:** No explanation of what the service is

**6.2 — Who — ideal customer identified**

- **Pass:** Target company type, role, team, or industry explicitly stated (not just "businesses" or "teams")
- **Warn:** General audience implied ("for developers", "for marketers") without specifics
- **Fail:** No target customer identified

**6.3 — How — delivery process or workflow described**

- **Pass:** Step-by-step process, numbered workflow, or clear methodology for how the service works
- **Warn:** Process mentioned at a high level but not detailed
- **Fail:** No how-it-works or process content

**6.4 — Why — differentiation vs. alternatives stated**

- **Pass:** Explicit differentiation — "why choose us", "unlike X", unique mechanism, or distinctive advantage named
- **Warn:** Benefits listed but no comparison to alternatives or why this approach is better
- **Fail:** No differentiation or why-choose-us content

**6.5 — How much — pricing or budget range mentioned**

- **Pass:** A price, price range, tier name with cost, or clear "see pricing" CTA with /pricing link visible
- **Warn:** "Contact for pricing" or "custom pricing" with no ranges or starting points
- **Fail:** Cost not mentioned anywhere and no path to pricing information

---

### Category 7 — Internal Linking & Context Graph (5 checks)

**7.1 — 10+ contextual internal links**

Count internal links in body content from fetch 1a (exclude nav menu and footer).

- **Pass:** 10+ internal links found in body content
- **Warn:** 5–9 internal links in body
- **Fail:** Fewer than 5 internal links in body

**7.2 — Related services or blog/resource content linked**

- **Pass:** Links to related blog posts, guides, resources, or other service pages appear in body content
- **Warn:** Related content linked only in sidebar or footer, not in body
- **Fail:** No related content links found anywhere

**7.3 — Breadcrumb navigation (with BreadcrumbList schema)**

- **Pass:** Visible breadcrumb navigation AND `BreadcrumbList` JSON-LD schema both present
- **Warn:** Breadcrumb nav visible but no schema, OR BreadcrumbList schema present but no visible nav
- **Fail:** No breadcrumb navigation and no BreadcrumbList schema

**7.4 — Key service terms link to their own dedicated pages**

Check if the main services/features mentioned in body text are hyperlinked.

- **Pass:** Main service/feature names in body text link to their dedicated pages
- **Warn:** Some service terms linked, others mentioned as plain text
- **Fail:** No contextual linking of service terms in body copy

**7.5 — Comparison table present (tiers, packages, or vs. alternatives)**

- **Pass:** A pricing tier table, feature comparison table, or vs. alternatives table is present on the page
- **Warn:** Comparison information presented as text/bullets rather than a table
- **Fail:** No comparison tables of any kind

---

### Category 8 — Content Richness & Multimodal (3 checks)

**8.1 — Process or workflow steps defined (numbered or phased)**

- **Pass:** Numbered steps (1, 2, 3) or named phases (Phase 1, Step 1) define how the process works
- **Warn:** Process described in paragraph prose but not structured as numbered steps
- **Fail:** No process steps or workflow definition

**8.2 — Images with descriptive alt text**

From fetch 1b, check every image's alt attribute.

- **Pass:** 90%+ of images have meaningful alt text (not blank, not "image.png", not generic)
- **Warn:** 50–89% have descriptive alt text, or key images are missing alt text
- **Fail:** Fewer than 50% have alt text, or all product/feature images lack alt text

**8.3 — Page listed in llms.txt**

From fetch 1e, check llms.txt content.

- **Pass:** Exact page path (e.g. `/claude-skills`) or full URL appears in llms.txt
- **Warn:** Root domain appears in llms.txt but this specific page path is not listed
- **Fail:** llms.txt does not exist (404), or this page URL/path is absent from it

---

### Category 9 — Freshness & Maintenance Signals (4 checks)

**9.1 — Content reviewed/updated within last 6 months**

Check for any date signal: visible on-page date, sitemap lastmod, or content timestamps.

- **Pass:** Any date signal (visible date, sitemap lastmod, published/updated field) is within the last 6 months of today's date
- **Warn:** A date exists but is older than 6 months
- **Fail:** No date found anywhere — no visible date, no sitemap lastmod, no timestamp

**9.2 — 'Last updated' date visible on page**

From fetch 1a, look for explicit "Last updated", "Updated:", "Published:", or a date string visible in the page content.

- **Pass:** A visible "Last updated" or publication date is present in the page body
- **Warn:** Date exists in metadata (sitemap, meta tags) but is not visible to a human reader on the page
- **Fail:** No date indicator visible on the page at all

**9.3 — Outdated stats, prices, or claims removed**

- **Manual:** Requires human review. Check whether statistics, pricing, and named examples reference current dates and remain accurate. Cannot be verified programmatically.

**9.4 — Changelog or version history present**

- **Pass:** A changelog section, release notes link, or version history is visible on the page
- **Warn:** Versioning mentioned in text but no dedicated changelog or history
- **Fail:** No changelog, release notes, or version history of any kind

---

### Category 10 — Crawlability & Technical (7 checks)

**10.1 — Page found in XML sitemap**

From fetch 1d.

- **Pass:** Exact page URL (or www/non-www variant) found in sitemap.xml
- **Warn:** Sitemap exists and has URLs but this specific page is not found
- **Fail:** sitemap.xml returns 404 or does not exist

**10.2 — Sitemap lastmod within last 6 months**

From fetch 1d, check the `<lastmod>` value for this page's entry.

- **Pass:** lastmod date is within the last 6 months of today
- **Warn:** lastmod present but older than 6 months
- **Fail:** No lastmod date found for this page in the sitemap

**10.3 — Server response under 500ms**

From Step 1f curl result.

- **Pass:** TTFB under 500ms
- **Warn:** TTFB 500ms–1000ms
- **Fail:** TTFB over 1000ms, or measurement failed

**10.4 — AI crawlers allowed in robots.txt**

From fetch 1c.

- **Pass:** GPTBot, ClaudeBot, AND PerplexityBot are all either explicitly allowed (`Allow: /`) or not mentioned in any Disallow rule (permissive by default)
- **Warn:** Some AI bots allowed, others not mentioned or status ambiguous
- **Fail:** Any of GPTBot, ClaudeBot, or PerplexityBot is explicitly `Disallow`ed

**10.5 — Page is indexable (no noindex)**

From fetch 1b, check the `robots` meta tag.

- **Pass:** `<meta name="robots" content="index, follow">` or no restricting robots meta tag
- **Warn:** Robots meta tag missing (ambiguous — could default to index or noindex depending on server)
- **Fail:** `noindex` directive found in meta robots tag or X-Robots-Tag header

**10.6 — AI crawler path not restricted for this URL**

From fetch 1c, check whether the page's specific path is blocked for AI crawlers.

- **Pass:** No `Disallow` rule covers the page path for any AI crawler user-agent
- **Warn:** Wildcard Disallow rule exists that could affect this path but AI bots aren't named
- **Fail:** Specific `Disallow` rule on the page path applies to GPTBot, ClaudeBot, or PerplexityBot

**10.7 — Page content readable without JavaScript**

From fetch 1b, check whether substantive content is present in raw server-rendered HTML.

- **Pass:** 500+ meaningful words of content visible in raw HTML without JS execution
- **Warn:** 100–499 words in raw HTML (partial SSR — some content may be JS-only)
- **Fail:** Fewer than 100 words in raw HTML; page is client-side rendered and largely invisible to AI crawlers

---

## Step 3 — Calculate Scores

### Per-category score (out of 100)

```
Category Score = (Σ check_scores) / (total_scoreable_checks_in_category) × 100

Where:
  check_score = 1.0 for Pass
  check_score = 0.5 for Warning
  check_score = 0.0 for Fail
  Manual checks are excluded from both numerator and denominator
```

Round to the nearest integer.

### Overall score (out of 100)

```
Overall Score = (Σ all_check_scores across all categories) / (total_scoreable_checks) × 100
```

Total checks: 48. Manual checks excluded from denominator.

### Score colour thresholds

| Score | Colour label | Hex |
|---|---|---|
| 80–100 | Green | #22C55E |
| 60–79 | Amber | #F59E0B |
| 0–59 | Red | #EF4444 |

---

## Step 4 — Determine Top Fixes

After grading, compile a ranked list of all Fail and Warning checks sorted by impact. Use this priority framework:

**Impact tier assignment:**

| Impact | Criteria |
|---|---|
| High | Check is a known LLM citation lever (llms.txt listing, Service schema, FAQPage schema, heading hierarchy, paragraph length, canonical URL, AI crawler access, JS readability) |
| Medium | Check affects content quality or trust signals visible to both humans and LLMs (measurable outcomes, comparison table, use case language, breadcrumbs, alt text) |
| Low | Check affects polish or freshness signals (changelog, last updated date, server speed, negative scoping) |

List the top 10 fixes in priority order. For each fix, include:
- Priority number (P1–P10)
- Impact tier (High / Medium / Low)
- Category name
- Fix title (what to add or change)
- Detail note (one sentence explaining why it matters or what to do)

---

## Step 5 — Generate the HTML Report

Read `references/html-template.md` for the complete HTML structure.

Populate the `AUDIT_DATA` JavaScript object in the template with all real data from this audit:

```javascript
const AUDIT_DATA = {
  url: "{FULL_URL}",
  domain: "{BARE_DOMAIN}",
  date: "{AUDIT_DATE}",          // e.g. "June 16, 2026"
  overallScore: {OVERALL_SCORE},
  totalChecks: 48,
  scoreable: {SCOREABLE_COUNT},  // 48 minus manual count
  pass: {PASS_COUNT},
  warn: {WARN_COUNT},
  fail: {FAIL_COUNT},
  manual: {MANUAL_COUNT},
  categories: [
    {
      name: "Content Clarity & Directness",
      score: {CAT1_SCORE},
      pass: {CAT1_PASS},
      warn: {CAT1_WARN},
      fail: {CAT1_FAIL},
      manual: 0,
      checks: [
        { status: "pass|warn|fail|manual", label: "Clear opening sentence", note: "Evidence note — one sentence" },
        // ... all 5 checks
      ]
    },
    // ... all 10 categories in order
  ],
  topFixes: [
    { priority: 1, impact: "High", category: "Category Name", fix: "Fix title", detail: "One sentence detail" },
    // ... up to 10 fixes
  ]
};
```

**Do not leave any placeholder values unfilled.** Every number must be a real value from this audit.

---

## Step 6 — Write and Present

Write the completed HTML report to a file in the current working directory:

```
{domain}-landing-page-audit.html
```

For example: `infrasity-com-landing-page-audit.html`

After writing, tell the user:
> "Audit complete. Report saved to `{filename}.html` — open it in any browser.
> **Overall score: {SCORE}/100** ({PASS} pass · {WARN} warn · {FAIL} fail · {MANUAL} manual)
> Top fix: {P1_FIX}"

Then offer to explain any category in detail or generate a prioritised action plan.

---

## Error Handling

| Situation | Action |
|---|---|
| URL returns 404 or connection refused | Report the error clearly. Suggest the user verify the URL and try again. Do not proceed. |
| Page is entirely JS-rendered (raw HTML < 100 words) | Note that the page may be invisible to AI crawlers. Mark check 10.7 as Fail. Audit what can be assessed from the metadata and note limited coverage. |
| robots.txt returns 404 | Mark checks 10.4 and 10.6 as Warn with note "robots.txt not found — AI crawler access status unknown." |
| sitemap.xml returns 404 | Mark checks 10.1 and 10.2 as Fail with note "sitemap.xml not found." |
| llms.txt returns 404 | Mark check 8.3 as Fail with note "llms.txt not found at root domain." |
| JSON-LD not extractable via WebFetch | Note this limitation and mark schema checks as Warn rather than Fail unless confident the schema is absent. |
| curl unavailable for timing | Mark check 10.3 as Warning with note "Server response time could not be measured — curl unavailable." |

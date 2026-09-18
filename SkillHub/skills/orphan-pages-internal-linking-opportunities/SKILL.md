---
name: orphan-pages-internal-linking-opportunities
description: Audit any domain for orphan blog pages, map internal links across all blog posts, generate keyword-backed interlinking briefs via DataForSEO, and produce a self-contained downloadable HTML report. Invoke with the target domain as the argument.
arguments:
  - name: domain
    description: The domain to audit (e.g. example.com or https://www.example.com)
    required: true
example_invocation: /orphan-pages-internal-linking-opportunities infrasity.com
---

# Orphan Page Audit & Interlinking Brief Generator

You are running a complete SEO orphan page audit. The user has provided a domain as input via `args`. Your job is to execute every phase below in order, using the tools available, and produce a single downloadable HTML report file saved to the current working directory.

**Input domain:** `{args}`

---

## PHASE 1 — Domain Normalization & Sitemap Discovery

1. Normalize the input domain:
   - Strip leading/trailing whitespace
   - If it doesn't start with `http`, prepend `https://`
   - If it doesn't have `www.` and the base domain resolves with it, use `www.`
   - Remove any trailing slash
   - Store as `BASE_URL` (e.g., `https://www.example.com`)

2. Fetch `BASE_URL/robots.txt` using WebFetch. Look for any `Sitemap:` directive — if found, use that URL as the sitemap location. If not found, default to `BASE_URL/sitemap.xml`.

3. Fetch the sitemap URL. Determine its type:
   - **Sitemap index** (`<sitemapindex>` tag present): extract all `<loc>` child sitemap URLs, fetch each one, and merge all `<loc>` URLs from every child sitemap into a single master URL list
   - **Regular sitemap** (`<urlset>` tag): extract all `<loc>` URLs directly

4. Store the full master URL list.

---

## PHASE 2 — Blog URL Identification

From the master URL list:

1. Analyze all URL patterns to identify the blog/content section. Look for the URL prefix that appears most frequently in a uniform pattern. Common prefixes to check: `/blog/`, `/articles/`, `/posts/`, `/insights/`, `/resources/`, `/learn/`, `/news/`, `/guides/`

2. Select the prefix that best represents the blog content (most URLs, most uniform structure). If multiple prefixes qualify, include all of them.

3. Filter the master URL list to only include URLs matching the identified blog prefix(es). Exclude index/listing pages (e.g., `BASE_URL/blog` with no further slug). Store as `BLOG_URLS`.

4. If no blog prefix is identifiable from the sitemap, fetch `BASE_URL` homepage and look for a blog/articles navigation link, then fetch that page and extract all post URLs from it.

5. Log the total count: "Found {N} blog posts at {BASE_URL}"

---

## PHASE 3 — Crawl & Build Inbound Link Map

Run a **Workflow** to crawl all blog posts in parallel. The workflow should:

**Script logic:**
- Take `BLOG_URLS` as the items list
- For each URL, spawn an agent that:
  - Fetches the page using WebFetch
  - Extracts ALL href links in the body/article content (not nav, header, footer) that point to other pages on the same domain matching the blog URL pattern
  - Normalizes all found links to absolute URLs (no trailing slash, no query params, no hash)
  - Returns `{ source_url, outbound_blog_links: [...] }`
- Use schema: `{ type: 'object', properties: { source_url: { type: 'string' }, outbound_blog_links: { type: 'array', items: { type: 'string' } } }, required: ['source_url', 'outbound_blog_links'] }`

After the workflow completes, aggregate results:
- Build `inbound_count` map: `{ url -> number }` initialized to 0 for all `BLOG_URLS`
- Build `inbound_sources` map: `{ url -> [source_url, ...] }` initialized to `[]` for all `BLOG_URLS`
- For each crawl result, iterate `outbound_blog_links` and increment the inbound count + push the source URL for each valid link

Classify every page:
- **Orphan** = 0 inbound links → store as `ORPHAN_URLS`
- **Low-linked** = 1–2 inbound links → store as `LOW_LINKED_URLS`
- **Healthy** = 3+ inbound links → store as `HEALTHY_URLS`

Build `FULL_INBOUND_MAP`: array of `{ url, inbound, linked_from }` sorted descending by inbound count.

---

## PHASE 4 — Keyword Research for Orphan Pages

Run a **Workflow** to get the top US search volume keyword for each orphan page. The workflow should:

**Script logic:**
- Take `ORPHAN_URLS` as the items list
- For each orphan URL, spawn an agent that:
  1. Extracts the slug from the URL (last path segment)
  2. Generates 6–8 keyword variants from the slug (convert hyphens to spaces, try variations with different word orders, add/remove qualifiers)
  3. Uses ToolSearch to load `mcp__claude_ai_DataForSEO__kw_data_google_ads_search_volume`, then calls it with the keyword variants, `location_code: 2840` (United States), `language_code: "en"`
  4. Picks the keyword with the highest US monthly search volume as `anchor_text`
  5. Fallback: if DataForSEO returns no data or errors, convert the slug to a phrase (hyphens → spaces) as the `anchor_text`
  6. Fetches the page and writes a 2–3 sentence `page_summary` of what the page covers
  7. Returns `{ orphan_url, anchor_text, us_monthly_volume, page_summary }`
- Use schema: `{ type: 'object', properties: { orphan_url: { type: 'string' }, anchor_text: { type: 'string' }, us_monthly_volume: { type: 'number' }, page_summary: { type: 'string' } }, required: ['orphan_url', 'anchor_text', 'us_monthly_volume', 'page_summary'] }`

Store results as `KEYWORD_DATA`: map of `{ orphan_url -> { anchor_text, us_monthly_volume, page_summary } }`

---

## PHASE 5 — Generate Interlinking Briefs for Orphan Pages

Run a **Workflow** using a 2-stage pipeline over `ORPHAN_URLS`:

**Stage 1** — Pass through keyword data (already computed, no agent needed — use the `KEYWORD_DATA` directly)

**Stage 2** — For each orphan, spawn an agent that:
1. Receives `orphan_url`, `anchor_text`, `page_summary`, and the full `BLOG_URLS` list
2. Selects exactly **3 topically relevant source pages** from `BLOG_URLS` (exclude the orphan itself; prefer well-linked, non-orphan pages)
3. Fetches each of the 3 source pages using WebFetch
4. For each source page produces:
   - `source_url`: the full URL of the source page
   - `where_to_place`: specific, precise description of the location within that page — naming the H2/H3 section, which paragraph, what content surrounds it. Must be specific enough that a content editor can navigate there without guessing
   - `context_copy`: minimum 300 characters of naturally flowing copy to be inserted at that location. The `anchor_text` MUST appear exactly once within it as `<a href="ORPHAN_URL">ANCHOR_TEXT</a>`. Copy must read as if it was always part of the article — not promotional, not forced. Same anchor text across all 3 placements.
5. Returns `{ orphan_url, anchor_text, placements: [{ source_url, where_to_place, context_copy }, ...] }`
- Use schema with `placements` as array of 3 objects each requiring `source_url`, `where_to_place`, `context_copy`

After the workflow completes, post-process every `context_copy`:
- Check if `anchor_text` appears as a hyperlink (`href="orphan_url"` present)
- If not, find the first occurrence of `anchor_text` (case-insensitive) and replace with `<a href="orphan_url">anchor_text</a>`

Store as `BRIEFS`.

---

## PHASE 6 — Generate HTML Report

Using the Write tool, save a single self-contained HTML file to the current working directory named `orphan-audit-{domain}-{YYYYMMDD}.html` where `{domain}` is the base domain (no protocol, no www, dots replaced with hyphens) and `{YYYYMMDD}` is today's date.

The HTML file must be completely self-contained — all CSS inline in a `<style>` tag, no external CDN or font imports, works offline. Use clean, professional design with the following structure:

### HTML Report Structure

```
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>Orphan Page Audit — {domain}</title>
  <style>
    /* Full inline CSS — professional design, light background, clean typography */
    /* Use system fonts: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif */
    /* Color palette: #0f172a (headings), #334155 (body), #3b82f6 (accent/links), #f1f5f9 (backgrounds), #e2e8f0 (borders) */
    /* Stat cards, tables, collapsible sections, copy buttons */
  </style>
</head>
<body>
```

**Section 1 — Header**
- Site logo area with domain name (large)
- Audit date
- "Download Report" button (triggers `window.print()` or direct file save)

**Section 2 — Executive Summary**
Four stat cards in a row:
- Total Blog Posts Found: `{BLOG_URLS.length}`
- Orphan Pages: `{ORPHAN_URLS.length}` + percentage of total
- Low-Linked Pages: `{LOW_LINKED_URLS.length}` (1–2 inbound links)
- Healthy Pages: `{HEALTHY_URLS.length}` (3+ inbound links)

A horizontal bar showing the proportion of orphan / low-linked / healthy visually.

**Section 3 — Orphan Pages List**
Table with columns: `#` | `Page URL` (clickable link) | `Anchor Text` | `US Monthly Volume`
One row per orphan page.

**Section 4 — Inbound Link Map (Non-Orphan Pages)**
Table sorted descending by inbound count: `Page URL` | `Inbound Links` | `Linked From`
For the "Linked From" column, list each source URL on a new line or as a comma-separated list.

**Section 5 — Interlinking Briefs**
For each orphan page, a card containing:
- Orphan URL (h3, clickable)
- Anchor Text (badge/pill)
- US Monthly Search Volume
- Three placement blocks, each showing:
  - Source page URL (bold, clickable)
  - "Where to Place" — displayed as a styled blockquote or info box
  - "Context Copy" — displayed in a styled `<pre>` or `<div>` with a "Copy" button that uses `navigator.clipboard.writeText()` to copy the HTML

**Section 6 — Footer**
- "Generated by Infrasity Orphan Page Audit Skill"
- Audit date and domain

### JavaScript (inline `<script>` tag)
- Copy button functionality: `navigator.clipboard.writeText(element.innerText)`
- Smooth scroll for any nav links
- Optional: collapse/expand for brief cards

---

## PHASE 7 — Confirm & Report to User

After saving the HTML file:
1. Report the file path to the user
2. Give a brief summary:
   - Total blog posts found
   - Number of orphan pages
   - Number of interlinking briefs generated
   - File name and location
3. Note any pages where keyword data could not be fetched from DataForSEO (fell back to slug)

---

## Important Rules

- **Never hardcode `/blog/`** — always detect the URL pattern from the actual sitemap
- **Anchor text is fixed per orphan** — the same `anchor_text` string appears in all 3 `context_copy` blocks for that orphan, always as a hyperlink
- **Context copy minimum 300 characters** — enforce strictly; if an agent returns shorter copy, flag it
- **Where to place must be specific** — section heading + paragraph position + surrounding content context
- **HTML report is self-contained** — no external requests, no CDN, works offline
- **DataForSEO fallback** — if API returns no data, use the slug converted to a readable phrase
- **Post-process hyperlinks** — after all briefs are generated, always verify and fix anchor text hyperlinks before writing the HTML
- **File naming** — `orphan-audit-{domain}-{YYYYMMDD}.html` saved in the user's current working directory

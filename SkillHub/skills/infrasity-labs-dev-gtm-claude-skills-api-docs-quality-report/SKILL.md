---
name: api-docs-quality-report
description: >
  Audits any API documentation site by crawling every endpoint page and scoring each one
  across 5 checks: description quality, OpenAPI spec presence, body param descriptions,
  response codes, and response schema completeness. Produces a polished interactive HTML
  report with a summary scorecard, site-wide pattern analysis, ranked top issues, and
  per-endpoint findings with specific fix guidance.

  Trigger this skill whenever a user provides a documentation URL and asks to audit, review,
  analyse, or check their API docs. Also trigger for: "do the same audit for X", "audit
  docs.company.com", "check the API docs at X", "run the API docs audit on X", "review the
  docs for Y API", or pastes a URL alongside words like audit, review, crawl, check, analyse,
  quality, completeness, or gaps. Always use this skill — do not attempt the audit
  without following this structured crawl-score-report workflow.
user-invokable: true
argument-hint: "<docs_url>"
license: MIT
metadata:
  version: "1.0.0"
  category: api-docs
---

# API Docs Audit Skill

Crawls every API reference endpoint page on a documentation site, scores each against
5 quality checks, detects site-wide patterns, and outputs an interactive HTML report
matching the style of previously-generated audits in this session.

---

## STEP 0 — COLLECT INPUT

You need exactly one input: the docs URL.

If the user hasn't provided it, ask:
> Which API docs URL should I audit?

If the URL is provided, strip trailing slashes and confirm it before proceeding.

**Special case — "do the same for X":**
If the user says "do the same" or "same audit for X", they want the identical workflow
and HTML report format applied to the new URL. Proceed directly to Step 1.

---

## STEP 1 — DISCOVER ALL ENDPOINT PAGES

### 1a. Try llms.txt first

Fetch `<docs_url>/llms.txt`.

If found:
- Extract every line matching the pattern `- [Page Title](URL): description`
- Filter to API reference pages only — look for paths containing any of:
  `api-reference`, `api-reference/`, `/api/`, `/endpoints/`, `/rest/`, `/docs/`, `/reference/` or versioned paths (e.g., `/v1/`)
- Exclude: overview/index pages (no HTTP method implied), SDK docs, CLI docs,
  Terraform docs, guides, quickstart pages
- Store as `ENDPOINT_PAGES[]` — list of `{title, url, description}`

If not found or returns 404:
- Fetch the docs homepage
- Look for a nav sidebar or sitemap link referencing API/endpoints
- Extract all API reference page URLs from the nav structure
- Note in the report that llms.txt was unavailable

### 1b. Identify categories

Group discovered pages by their URL path prefix or nav section:
- e.g. `/api-reference/agents/` → Agents category
- e.g. `/api-reference/executions/` → Executions category
- Pages at the root level of api-reference → Uncategorized or infer from title

Store `CATEGORIES[]` — list of `{name, page_count, pages[]}`.

Report discovery summary:
> Found N endpoint pages across K categories. Fetching now...

---

## STEP 2 — CHECK OPENAPI SPEC AVAILABILITY

Before fetching individual pages, check if a standalone OpenAPI spec exists.

Try these discovery methods in order (stop at first success):
1. Inspect the `Link` HTTP header (RFC 8288) on the homepage or docs root for `rel="openapi"` or `rel="describedby"` — this is the standard discovery mechanism for API specifications
2. `<docs_url>/openapi.json`
3. `<docs_url>/openapi.yaml`
4. `<docs_url>/api/openapi.json`
5. Any URL referenced in llms.txt under "## OpenAPI Specs"

**Result:**
- If accessible: `SPEC_AVAILABLE = true`, store the URL
- If 404 on all attempts and no Link header found: `SPEC_AVAILABLE = false`

A missing spec is itself a **top-priority finding** — record it as Issue #1.

---

## STEP 3 — FETCH AND PARSE ALL ENDPOINT PAGES

Fetch each URL in `ENDPOINT_PAGES[]`. For each page, extract:

### 3a. Page-level prose description
The text that appears **above** the OpenAPI block (or between the `#` title and the
first `## OpenAPI` heading). This is the human-written description.

### 3b. OpenAPI block
Look for a fenced code block with language hint `yaml` or `json` that contains
an OpenAPI spec. Extract:
- `HTTP_METHOD` — e.g. `GET`, `POST`, `PUT`, `DELETE`, `PATCH`
- `HTTP_PATH` — e.g. `/api/v1/agents/{agent_id}/execute`
- `REQUEST_BODY_SCHEMA` — the requestBody schema section (if any)
- `PARAMETERS` — path + query params (if any)
- `RESPONSES` — the full responses object
- `RESPONSE_200_SCHEMA` — the schema under responses.200 or 201

If no OpenAPI block found, mark `SPEC_INLINE = false`.

---

## STEP 4 — SCORE EACH ENDPOINT (5 CHECKS)

For every endpoint, evaluate all 5 checks. Store results as
`{check_name: "pass"|"warn"|"fail", current_state: string, fix_guidance: string}`.

Read `references/scoring-rules.md` for the exact scoring criteria per check.

**Check 1 — Endpoint Description**
**Check 2 — OpenAPI Spec**
**Check 3 — Body Param Descriptions**
**Check 4 — Response Codes**
**Check 5 — Response Schema**

---

## STEP 5 — DETECT SITE-WIDE PATTERNS

After scoring all endpoints, look for patterns that repeat across many pages.

A pattern qualifies if it affects **≥ 60% of endpoints**:

| Pattern to detect | How to identify |
|---|---|
| Universal missing error codes | All endpoints missing 401, 429, 500 etc. |
| Universal empty response schemas | `schema: {}` on most endpoints |
| Free-form body schemas | `additionalProperties: true` on most request bodies |
| Inline spec only / broken canonical spec | All pages embed spec inline but canonical 404s |
| One-liner descriptions everywhere | Descriptions under 10 words on most pages |
| 422-only validation errors | Only FastAPI's 422 documented, not business errors |

For each detected pattern, write a **single paragraph** summarising:
- What the pattern is
- How many endpoints it affects
- Root cause (e.g. FastAPI auto-generation, missing middleware docs)
- Impact on developer experience

Store as `SITE_WIDE_PATTERNS[]`.

---

## STEP 6 — COMPILE TOP ISSUES

Rank the **10 most impactful issues** across all findings. Prioritise by:

1. Issues affecting the most endpoints
2. Issues on the highest-traffic / most important endpoints
3. Security-sensitive gaps (auth endpoints, credential endpoints with empty schemas)
4. Deprecated endpoints with no migration path
5. Spec availability (404 canonical spec blocks all SDK tooling)

For each issue, write:
- A concise `<strong>title</strong>`
- 1-2 sentence description with specific endpoint names or counts
- Badge: FAIL or WARN

Store as `TOP_ISSUES[]` (max 10).

---

## STEP 7 — BUILD SCORECARD

For each category, calculate:
- `total` — endpoint count
- `pass_count` — endpoints with all 5 checks passing
- `warn_count` — endpoints with at least one WARN and no FAIL
- `fail_count` — endpoints with at least one FAIL

Calculate overall totals.

Store as `SCORECARD[]`.

---

## STEP 8 — GENERATE HTML REPORT

Read `references/html-template.md` for the complete HTML structure, CSS variables,
JavaScript, and all section markup.

Substitute all `{{VARIABLE}}` placeholders with real audit data, ensuring all values are HTML-escaped to prevent XSS.

**Key variable map:**

| Variable | Source |
|---|---|
| `{{DOCS_URL}}` | Input URL |
| `{{AUDIT_DATE}}` | Today's date |
| `{{TOTAL_ENDPOINTS}}` | Count of ENDPOINT_PAGES |
| `{{TOTAL_PASS}}` | Sum of all pass_count across categories |
| `{{TOTAL_WARN}}` | Sum of all warn_count |
| `{{TOTAL_FAIL}}` | Sum of all fail_count |
| `{{SPEC_COUNT}}` | 1 if SPEC_AVAILABLE, else 0 |
| `{{SCORECARD_ROWS}}` | Generated `<tr>` rows from SCORECARD |
| `{{PATTERN_BOX}}` | Pattern box HTML (if SITE_WIDE_PATTERNS found) |
| `{{TOP_ISSUES_HTML}}` | Generated issue row HTML from TOP_ISSUES |
| `{{SIDEBAR_LINKS}}` | Generated sidebar `<div class="sbl">` links |
| `{{SECTIONS_HTML}}` | All section HTML for each category |

For section HTML generation rules, see `references/html-template.md` → Section: SECTIONS_HTML.

**Output the file to:**
```
/mnt/user-data/outputs/<slug>-api-audit-report.html
```
Where `<slug>` is the domain name with dots replaced by hyphens
(e.g. `docs.kubiya.ai` → `kubiya-ai`).

Then call `present_files` to deliver it.

---

## ERROR HANDLING

| Situation | Action |
|---|---|
| `llms.txt` returns 404 | Crawl nav links from homepage; note in report |
| Individual endpoint page returns 404 | Skip it; add to "inaccessible pages" count in footer |
| Page has no OpenAPI block | Score Spec check as FAIL; still score other checks from prose |
| Page has no prose description | Score Description as FAIL with note "No prose description" |
| Endpoint page is robots.txt blocked | Note in report; do not fetch |
| More than 200 endpoints found | Batch fetching — process in groups of 20, progress-report to user |
| Canonical spec accessible | Note as positive finding; do not flag as issue |

---

## WHAT NOT TO DO

- ❌ Never start generating HTML before all pages are fetched and scored
- ❌ Never skip an endpoint page — fetch every one listed in llms.txt
- ❌ Never infer scores from page titles alone — fetch the actual page content
- ❌ Never mark Response Codes as PASS just because 200 is documented
- ❌ Never mark Response Schema as PASS for `schema: {}` — that is FAIL
- ❌ Never mark Body Params as PASS for `additionalProperties: true` — that is WARN at minimum
- ❌ Never report a pattern as site-wide unless it affects ≥ 60% of endpoints
- ❌ Never put generic fix text — every fix_guidance must reference the specific endpoint

---

## REFERENCE FILES

- `references/scoring-rules.md` — Exact PASS/WARN/FAIL criteria for all 5 checks,
  with worked examples. **Read before scoring any endpoint.**

- `references/html-template.md` — Complete HTML/CSS/JS template with all section
  markup, variable map, and rendering instructions.
  **Read before writing any HTML.**
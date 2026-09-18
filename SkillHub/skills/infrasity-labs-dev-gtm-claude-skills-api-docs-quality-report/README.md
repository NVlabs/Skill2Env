# API Docs Audit

Crawls every endpoint page on an API documentation site, scores each one across 5 quality checks, detects site-wide patterns, and produces an interactive HTML report with a summary scorecard, ranked issues, and per-endpoint fix guidance.

---

## What this skill does

Most API docs have the same problems at scale: missing response schemas, one-liner endpoint descriptions, no error codes beyond 200. This skill finds all of them automatically.

It crawls every endpoint page on your API reference, scores each against 5 checks, and produces a dark-theme HTML report you can share with your team or embed in a doc review. The report includes a summary scorecard, site-wide pattern analysis (problems affecting 60%+ of endpoints), a ranked top-issues list, and per-endpoint findings with specific fix text.

Built for:
- **Developer experience and DevRel teams** auditing their API docs before a launch
- **Technical writers** running a structured gap analysis across all endpoints
- **Engineering teams** checking whether auto-generated docs are complete enough for external developers

---

## Installation

### Claude Code (Recommended)

Clone the repo — the skill activates automatically when you open it in Claude Code:

```bash
git clone https://github.com/Infrasity-Labs/dev-gtm-claude-skills.git
cd dev-gtm-claude-skills
claude
```

Then trigger it with:

```
/dev-gtm api-audit https://docs.example.com/api-reference
```

Or just describe what you want in natural language — Claude will activate the skill automatically.

### Claude Web (Free / Pro)

1. Go to **[Settings → Capabilities](https://claude.ai/settings/capabilities)** and enable **Code execution and file creation**
2. Go to **[Customize → Skills](https://claude.ai/customize/skills)**
3. Click **+** → **Create skill** → **Upload a skill**
4. Zip this skill folder and upload it:

```bash
cd dev-gtm-claude-skills/skills
zip -r api-docs-quality-report.zip api-docs-quality-report/
```

Upload `api-docs-quality-report.zip` and toggle it on.

---

## How to use

Drop an API docs URL in any message:

```
Audit the API docs at https://docs.kubiya.ai/api-reference
```

```
Check the API docs for https://api.example.com/docs
```

```
/dev-gtm api-audit https://docs.example.com/api-reference
```

Claude discovers all endpoint pages automatically — you only need to provide the root docs URL.

---

## The 5 checks

Every endpoint is scored against these 5 checks. Each returns **pass**, **warn**, or **fail** with a specific evidence note.

| # | Check | What it evaluates |
|---|-------|-------------------|
| 1 | **Endpoint Description** | Is there a human-written prose description above the OpenAPI block? Is it more than a one-liner? |
| 2 | **OpenAPI Spec** | Is there an inline OpenAPI block? Is there a canonical spec file accessible at a standard path? |
| 3 | **Body Param Descriptions** | Do all request body parameters have descriptions? Are schemas using `additionalProperties: true` (too loose)? |
| 4 | **Response Codes** | Are error codes documented beyond just 200? Are 401, 429, and 500 covered? |
| 5 | **Response Schema** | Is the 200/201 response schema fully defined? Is `schema: {}` used (empty schema = fail)? |

---

## What the report includes

**Summary scorecard** — a table showing pass/warn/fail counts per endpoint category (e.g. Agents, Executions, Webhooks).

**Site-wide patterns** — problems affecting 60%+ of endpoints are called out as patterns with a root cause analysis and DX impact note. Common patterns detected: universal missing error codes, empty response schemas, free-form body schemas, one-liner descriptions everywhere.

**Top 10 issues** — ranked by impact (endpoints affected, security sensitivity, spec availability). Each issue has a concise title, a description with specific endpoint names, and a FAIL or WARN badge.

**Per-endpoint findings** — every endpoint gets its own section with all 5 check results, the current state, and specific fix guidance referencing that endpoint's actual content.

---

## How endpoint discovery works

The skill uses a layered discovery approach:

1. Fetches `<docs_url>/llms.txt` — if found, extracts all API reference page links from it
2. If `llms.txt` is unavailable, falls back to crawling the homepage nav sidebar for API reference links
3. Checks for a canonical OpenAPI spec at standard paths (`/openapi.json`, `/openapi.yaml`, etc.) and via the `Link` HTTP header
4. Fetches every discovered endpoint page

Pages behind authentication are skipped and noted. If more than 200 endpoints are found, they are processed in batches of 20 with progress updates.

---

## Output

An HTML file saved to `/mnt/user-data/outputs/<slug>-api-audit-report.html`, delivered via `present_files`.

The report is self-contained — no external dependencies, no CDN. Share it as a file or open it directly in a browser.

---

## File structure

```
api-docs-quality-report/
├── SKILL.md               # Skill instructions Claude follows
├── README.md              # This file
└── references/
    ├── scoring-rules.md   # Exact pass/warn/fail criteria for all 5 checks
    └── html-template.md   # Full HTML/CSS/JS report template
```

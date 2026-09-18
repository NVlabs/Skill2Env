# Docs Auditor

Audits any developer documentation site across **33 checks** in **7 categories** and produces an interactive scored report out of 100, rendered inline in Claude.

<p align="center">
  <a href="../../assets/docs-auditor-gif.gif">
    <img
      src="../../assets/docs-auditor-gif.gif"
      width="100%"
      alt="Docs Auditor in action"
    />
  </a>
</p>

---

## What this skill does

Most documentation quality checks are manual and inconsistent. This skill automates a full audit by fetching the live site, sampling key pages, and evaluating 33 specific signals across structure, content, SEO, AI discoverability, and maintenance hygiene.

The output is a visual widget rendered directly in Claude: a color-coded score circle, per-category breakdowns, and a pass/warn/fail badge on every individual check with a short evidence note explaining the finding. No spreadsheets, no copy-pasting URLs, no manual checklist.

Built for:
- **Developer marketing and DevRel teams** evaluating their own docs before a launch or redesign
- **GEO practitioners** checking whether docs are structured for AI discoverability (`llms.txt`, sitemap, bot access)
- **Technical writers** running a structured gap analysis before a content audit
- **Agencies and consultants** producing a scored deliverable for a client docs review

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
/dev-gtm docs-audit https://docs.stripe.com
```

Or just describe what you want — Claude activates the skill automatically when you provide a docs URL with audit intent.

### Claude Web (Free / Pro)

1. Go to **[Settings → Capabilities](https://claude.ai/settings/capabilities)** and enable **Code execution and file creation**
2. Go to **[Customize → Skills](https://claude.ai/customize/skills)**
3. Click **+** → **Create skill** → **Upload a skill**
4. Zip this skill folder and upload it:

```bash
cd dev-gtm-claude-skills/skills
zip -r docs-auditor.zip docs-auditor/
```

Upload `docs-auditor.zip` and toggle it on.

---

## How to use

Drop a docs URL in any message:

```
Audit the docs at https://docs.stripe.com
```

```
How good are the docs for https://docs.example.com?
```

```
/dev-gtm docs-audit https://docs.example.com
```

<p align="center">
  <img
    src="../../assets/docs-auditor-trigger.gif"
    width="100%"
    alt="Triggering the audit with a URL"
  />
</p>

The skill picks up any phrasing that includes a docs URL and an audit intent. All required files (`robots.txt`, `sitemap.xml`, `llms.txt`, etc.) and page samples are fetched automatically.

---

## What gets checked

The audit runs 33 checks grouped into 7 categories. Each check is evaluated against the live site and marked **pass**, **warn**, or **fail**.

| # | Category | Checks |
|---|----------|--------|
| 1 | **AI & LLM Discoverability** | `llms.txt` present, `llms-full.txt` present, docs pages listed in llms.txt, AI bots allowed in robots.txt, docs pages in sitemap.xml |
| 2 | **Structure & Navigation** | Intro/overview page with real content, quickstart with actionable steps, API reference section, sidebar nav, breadcrumb nav, search functionality |
| 3 | **Content Completeness** | Tutorials or examples section, code examples present, multi-language examples (Python, JS, cURL), changelog or release notes, FAQ or troubleshooting page, error codes documented |
| 4 | **Content Quality** | Intro explains product and audience, quickstart reaches a working state, sampled pages have sufficient depth (no stubs) |
| 5 | **Technical SEO & Crawlability** | HTTPS enforced, meta titles on all pages, meta descriptions on all pages, canonical URLs correct, no noindex on docs pages |
| 6 | **Internal Linking & Flow** | Pages cross-link to each other, prev/next page navigation, links to GitHub or source, community or support links |
| 7 | **Versioning & Maintenance** | Version badge or indicator visible, last-updated freshness signal, install commands with version pinning, deprecation notices where applicable |

---

<p align="center">
  <a href="../../assets/docs-auditor-gif.gif">
    <img
      src="../../assets/docs-auditor-gif.gif"
      width="100%"
      alt="Example audit report widget"
    />
  </a>
</p>

---

## How the fetch works

The skill performs a structured multi-step fetch before evaluating any checks:

1. Runs a targeted web search to surface `robots.txt`, `sitemap.xml`, `llms.txt`, and `llms-full.txt` for both the docs subdomain and root domain
2. Fetches each of those files directly
3. Fetches the docs homepage plus 6–8 sampled pages: quickstart, changelog, API reference, an error codes or FAQ page, and one or two deeper guide pages
4. Evaluates all 33 checks against the fetched content

The skill handles common edge cases: JS-rendered pages (flagged as inconclusive rather than failed), subdomain vs root domain file hosting, auth-gated pages (marked warn with a note), and single-version products (check 7.4 deprecation notices marked N/A rather than fail).

---

## Limitations

- Pages behind authentication cannot be fetched. Affected checks are marked warn with a note.
- Heavily JS-rendered docs may return sparse HTML. The skill flags this and marks affected checks as inconclusive rather than failed.
- The audit samples 6–8 pages. It is not a full crawl — checks reflect the sampled content, not every page on the site.
- `robots.txt` AI bot policy is evaluated based on what can be fetched. If the file is not surfaced in search results, the check is marked warn rather than assumed pass or fail.

---

## File structure

```
docs-auditor/
├── SKILL.md                        # Skill instructions Claude follows
├── README.md                       # This file
├── references/
│   ├── widget-template.md          # HTML/CSS template for the report widget
│   ├── fetch-strategy.md           # Which URLs to fetch and what to extract
│   └── scoring.md                  # Point values per check and grade bands
└── tests/
    └── test-cases.json             # 5 test cases for validation
```

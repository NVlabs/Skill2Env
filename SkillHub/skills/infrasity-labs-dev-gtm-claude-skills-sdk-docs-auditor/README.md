# SDK Docs Auditor

Crawls any SDK documentation site, audits six core sections against a structured checklist, cross-references every gap across the full page corpus, and produces a scored downloadable HTML report.

---

## What this skill does

Most SDK doc quality checks are manual and inconsistent. This skill automates a full audit by discovering every relevant SDK page via `llms.txt` or `sitemap.xml`, fetching each one, and evaluating six sections (Installation, Quick Start, Error Handling, Troubleshooting, Examples, and Best Practices) against detailed must-have and should-have criteria.

The key differentiator: every gap is cross-referenced across the entire page corpus before being flagged. If the content exists elsewhere in the docs but is not linked, the audit says so, distinguishing "missing content" from "content that exists but isn't where it should be."

Built for:
- **Developer marketing and DevRel teams** doing a structured quality review of their own SDK docs before a launch or release
- **Technical writers** running a gap analysis to prioritise what to write next
- **Agencies and consultants** producing a scored deliverable for a client SDK review

---

## Installation

### Claude Code (Recommended)

Clone the repo. The skill activates automatically when you open it in Claude Code:

```bash
git clone https://github.com/Infrasity-Labs/dev-gtm-claude-skills.git
cd dev-gtm-claude-skills
claude
```

Then trigger it with:

```
/dev-gtm sdk-audit https://docs.example.com/sdk
```

Or just describe what you want. Claude activates the skill when you provide a docs URL and ask for an audit, review, or quality check.

### Claude Web (Free / Pro)

1. Go to **[Settings → Capabilities](https://claude.ai/settings/capabilities)** and enable **Code execution and file creation**
2. Go to **[Customize → Skills](https://claude.ai/customize/skills)**
3. Click **+** → **Create skill** → **Upload a skill**
4. Zip this skill folder and upload it:

```bash
cd dev-gtm-claude-skills/skills/sdk-docs-auditor
zip -r ../sdk-docs-auditor.zip .
```

Upload `sdk-docs-auditor.zip` and toggle it on.

> **Egress network required.** This skill uses curl to fetch pages from the target docs site. In Claude Code, you will be prompted to allow network access when the skill runs. In Claude Web, code execution (enabled above) covers this automatically.

---

## How to use

```
Audit the SDK docs at https://docs.example.com/sdk
```

```
How good are the docs at https://docs.example.com?
```

```
Review the SDK documentation at docs.example.com
```

```
/dev-gtm sdk-audit https://docs.example.com
```

Claude picks up any message that includes a docs URL alongside words like: audit, review, check, analyse, quality, completeness, or gaps.

---

## Inputs

| Field | Required | Notes |
|-------|----------|-------|
| Documentation URL | ✅ | The root URL of the SDK docs site to audit |

No other inputs are required. Page discovery, fetching, and section mapping all happen automatically.

---

## Output

A self-contained HTML report file saved to `/mnt/user-data/outputs/sdk-audit-report.html` and presented with a download link.

The report contains:
- **Overall score** (0–100): weighted average of the six section scores
- **Per-section scores and rating tiers**: Strong / Good / Adequate / Weak / Poor
- **Strengths**: what is done well in each section
- **Gap list**: every gap tagged as either `[covered in: page-name]` or `[not covered anywhere in corpus]`
- **Top priority recommendations**: 6–8 ranked actions by impact, distinguishing factual errors, missing content, and cross-referencing opportunities

After presenting the file, Claude gives a one-line summary: pages fetched, overall score, and the single most critical finding.

---

## Things to know

**Cross-referencing is the core value.** The audit never flags a gap without first checking whether the content exists somewhere else in the docs. "Gap covered elsewhere but not linked" is treated differently from "gap that does not exist anywhere."

**Discovery falls back gracefully.** The skill tries `llms.txt` first, then `sitemap.xml`, then the homepage nav. It always reports which method was used.

**Large sites are prioritised intelligently.** For sites with more than 30 pages, the six target section pages are fetched first, followed by overview and API reference pages, then service-specific pages.

**The report file does not appear in chat.** The full report HTML is presented as a download, not reproduced as chat text. Claude gives a brief summary inline.

---

## How it works

1. **Discover all SDK pages**: tries `llms.txt` first (extracts URLs from link lines), falls back to `sitemap.xml` (parses `<loc>` entries), then the homepage nav; filters to SDK-relevant paths only
2. **Map sections**: identifies which discovered pages correspond to the six audit targets (Installation, Quick Start, Error Handling, Troubleshooting, Examples, Best Practices)
3. **Fetch every page**: runs `curl` on each URL, strips HTML with Python to extract plain text; batches multiple pages in one bash call to minimise round-trips
4. **Audit each section**: evaluates must-haves (scored heavily) and should-haves (scored moderately) against the fetched content
5. **Cross-reference gaps**: for every gap identified, searches all other fetched pages to determine whether the content exists elsewhere in the corpus
6. **Score sections**: assigns 0–100 per section and a rating tier based on how many must-haves and should-haves are met
7. **Rank recommendations**: orders the top 6–8 actions by impact × effort: factual errors first, then unmet must-haves, then cross-referencing gaps, then should-haves
8. **Generate the HTML report**: injects all audit data into `assets/report-template.html` and saves the file

---

## Config schema reference

The JSON Claude assembles and injects into the report template:

```json
{
  "audit_url": "https://docs.example.com/sdk",
  "pages_fetched": 24,
  "audit_date": "2026-05-29",
  "overall_score": 71,
  "sections": [
    {
      "num": "01",
      "name": "Installation Guide",
      "rating": "Good",
      "score": 74,
      "strengths": [
        "Prerequisites with exact Python version listed",
        "pip install command present with package name"
      ],
      "gaps": [
        {
          "text": "No verification snippet to confirm the install succeeded",
          "covered_in": [],
          "nowhere": true
        },
        {
          "text": "Constructor parameter reference (timeout, retries) missing from this page",
          "covered_in": ["api-reference"],
          "nowhere": false
        }
      ]
    }
  ],
  "priorities": [
    {
      "rank": 1,
      "text": "Fix execute() call signature on quick-start page: api-reference shows it takes a session_id parameter that is absent from the quick-start example",
      "type": "error"
    },
    {
      "rank": 2,
      "text": "Add a verification snippet to the Installation page, not covered anywhere in the corpus",
      "type": "missing"
    }
  ]
}
```

Priority types: `"error"` (factual mistake), `"missing"` (not covered anywhere), `"xref"` (covered elsewhere, needs linking), `"improvement"` (should-have gap).

---

## File structure

```
sdk-docs-auditor/
├── SKILL.md                          # Skill instructions Claude follows
├── README.md                         # This file
├── assets/
│   └── report-template.html          # HTML report shell with injected placeholders
└── references/
    └── cross-reference-guide.md      # Rules for cross-referencing gaps across the corpus
```

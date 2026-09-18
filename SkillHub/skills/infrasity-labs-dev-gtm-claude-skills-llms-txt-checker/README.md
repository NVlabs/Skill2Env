# LLMs.txt Checker

Audits any domain's AI-readiness by probing `robots.txt`, `llms.txt`, and `llms-full.txt` directly, then scores each file against a structured checklist and delivers a formatted report with pass/warn/fail findings and actionable fixes.

---

## What this skill does

You give it a domain or URL. The skill normalises the input, fetches all three AI-readiness files via `curl`, and audits each one against a structured checklist covering structure, content completeness, and AI-readiness signals. It then reports what was found, what was missing, and exactly what to fix.

Built for:
- **Developer marketing and DevRel teams** checking whether their docs are discoverable by AI tools like Claude Code, Cursor, and GitHub Copilot
- **GEO / AEO practitioners** validating that `llms.txt` and `llms-full.txt` are correctly structured and referenced
- **Technical writers** doing a pre-launch AI-readiness check before a docs redesign

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
/dev-gtm llms-txt-check docs.example.com
```

Or just describe what you want. Claude activates the skill when you provide a domain and ask about `llms.txt` or AI-readiness.

### Claude Web (Free / Pro)

1. Go to **[Settings → Capabilities](https://claude.ai/settings/capabilities)** and enable **Code execution and file creation**
2. Go to **[Customize → Skills](https://claude.ai/customize/skills)**
3. Click **+** → **Create skill** → **Upload a skill**
4. Zip this skill folder and upload it:

cd dev-gtm-claude-skills/skills/llms-txt-checker
zip -r ../llms-txt-checker.zip .
zip -r llms-txt-checker.zip llms-txt-checker/
```

Upload `llms-txt-checker.zip` and toggle it on.

> **Egress network required.** This skill uses curl to make outbound HTTP requests. In Claude Code, you will be prompted to allow network access when the skill runs. In Claude Web, code execution (enabled above) covers this automatically.

---

## How to use

```
Check llms.txt for docs.anthropic.com
```

```
Does stripe.com have llms.txt?
```

```
Audit the AI-readiness of docs.example.com
```

```
/dev-gtm llms-txt-check linear.app
```

Claude accepts any phrasing that includes a domain and mentions `llms.txt`, AI-readiness, GEO, or AEO.

---

## Inputs

| Field | Required | Notes |
|-------|----------|-------|
| Domain or URL | ✅ | Any format: `example.com`, `https://docs.example.com/en/home`, etc. Claude normalises it |

---

## Output

A structured audit report rendered directly in chat:

```
## LLMs.txt Audit: docs.example.com

### Discovery
llms.txt: ✅ 200 (4.2 KB)   llms-full.txt: ❌ 404   robots.txt: ✅ 200

### llms.txt: ✅ Found
✅ H1 title present
✅ Blockquote summary below H1
✅ H2 sections grouping links
❌ Links use relative URLs (must be absolute)
❌ No reference to llms-full.txt

### llms-full.txt: ❌ Not Found

### robots.txt Signal
✅ User-agent: * with Allow: /
✅ ai-train=no (acceptable)

### Summary & Recommendations
1. Switch all link URLs to absolute paths
2. Create llms-full.txt and reference it from llms.txt
3. ...
```

---

## Things to know

**Redirects are followed automatically.** The skill uses `curl -L`, so 301/302 redirects are transparent; the final destination URL is what gets audited.

**404 ≠ broken site.** A 404 on `llms.txt` simply means the file is not published at the standard path. The skill always checks whether the file is referenced from a non-standard location before marking it absent.

**Mintlify and Fern auto-generate both files.** If the site is on Mintlify or Fern, both `llms.txt` and `llms-full.txt` are auto-generated. The skill notes this in the discovery section.

**No API keys needed.** This skill runs entirely on `curl`: no Ahrefs, no DataForSEO, no third-party services.

---

## How it works

1. **Normalise the domain**: strips `https://`, path segments, and trailing slashes from any input format
2. **Fetch all three files**: runs `curl` with redirect following and a 10-second timeout on `/robots.txt`, `/llms.txt`, and `/llms-full.txt`; captures HTTP status codes and file sizes
3. **Classify the result**: determines which case applies: both files found, only `llms.txt` found, or neither found
4. **Audit `llms.txt`**: checks structure (H1, blockquote, H2 sections, absolute URLs), content completeness (API reference, quickstart, SDK guides), and AI-readiness signals (reference to `llms-full.txt`)
5. **Audit `llms-full.txt`**: checks file size, document boundary markers, `Source:` URL references, and absence of raw HTML or JS artifacts
6. **Read `robots.txt` signals**: checks for AI-access directives (`ai-input`, `ai-train`, `Disallow` rules affecting known AI crawlers)
7. **Deliver the report**: structured pass/warn/fail output with 3–5 prioritised fixes

---

## File structure

```
llms-txt-checker/
├── SKILL.md                              # Skill instructions Claude follows
├── README.md                             # This file
└── references/
    └── llms-txt-report-reference.html    # Report format reference
```

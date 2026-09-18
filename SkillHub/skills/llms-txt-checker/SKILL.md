---
name: llms-txt-checker
description: >
  Audits any domain's AI-readiness by using curl to directly probe robots.txt, llms.txt, and
  llms-full.txt, then scores each file against a structured checklist and delivers a formatted
  report with pass/warn/fail findings and actionable fixes.
  Use this skill whenever a user provides a domain or URL and wants to know if llms.txt or llms-full.txt is
  available, discoverable, or properly structured. Trigger on phrases like "check llms.txt for",
  "does this site have llms.txt", "find llms.txt", "check llms for this url", "audit llms.txt",
  "is llms-full.txt available", or any time a user shares a domain/docs URL and wants AI-readiness checked.
  Also trigger when the user wants to verify GEO/AEO readiness of a documentation site.
---

# LLMs.txt Checker Skill

Audits any domain's AI-readiness by using `curl` to directly probe `robots.txt`, `llms.txt`, and `llms-full.txt`, then scores each file against a structured checklist and delivers a formatted report with pass/warn/fail findings and actionable fixes.

The user provides **only a domain** (e.g. `anthropic.com` or `docs.example.com`). Claude uses `bash_tool` with `curl` commands to directly probe the domain — no guessing, no page-scraping required.

---

## How it works

Instead of relying on web_fetch and hoping links surface organically, this skill uses **curl via bash_tool** to directly request the well-known paths for `robots.txt`, `llms.txt`, and `llms-full.txt`. This is reliable, fast, and works regardless of how the site is built.

The curl commands follow HTTP redirects, capture response codes, and save content to temp files for auditing.

---

## Step-by-Step Workflow

### Step 1: Normalise the domain

Take the user-provided input and strip any trailing slashes, `http://`, `https://`, or path segments to get a clean base domain (e.g. `docs.anthropic.com`). If the user provides a full URL like `https://docs.anthropic.com/en/home`, extract just `docs.anthropic.com`.

---

### Step 2: Fetch all three files via curl

Run the following curl commands using `bash_tool`. Use `-L` to follow redirects, `-s` for silent mode, `-o` to save content, `-w` to capture HTTP status codes, and a reasonable timeout (`--max-time 10`).

```bash
DOMAIN="<normalised-domain>"

# Fetch robots.txt
curl -L -s -o /tmp/robots.txt -w "%{http_code}" --max-time 10 "https://$DOMAIN/robots.txt" > /tmp/robots_status.txt

# Fetch llms.txt
curl -L -s -o /tmp/llms.txt -w "%{http_code}" --max-time 10 "https://$DOMAIN/llms.txt" > /tmp/llms_status.txt

# Fetch llms-full.txt
curl -L -s -o /tmp/llms-full.txt -w "%{http_code}" --max-time 10 "https://$DOMAIN/llms-full.txt" > /tmp/llms_full_status.txt

# Print status codes and file sizes for inspection
echo "robots.txt: $(cat /tmp/robots_status.txt) | $(wc -c < /tmp/robots.txt) bytes"
echo "llms.txt:   $(cat /tmp/llms_status.txt) | $(wc -c < /tmp/llms.txt) bytes"
echo "llms-full.txt: $(cat /tmp/llms_full_status.txt) | $(wc -c < /tmp/llms-full.txt) bytes"
```

Interpret the HTTP status codes:
- **200** → file exists, read and audit the content
- **301/302** → followed automatically by `-L`; final destination counts
- **404** → file does not exist at this path
- **403/429/5xx** → server-side block or error; note it explicitly
- **000** → connection failed (domain unreachable or timeout)

---

### Step 3: Read and classify results

After the curl commands complete, read the saved files:

```bash
cat /tmp/robots.txt
cat /tmp/llms.txt
# For llms-full.txt, show first 200 lines only to avoid flooding context:
head -200 /tmp/llms-full.txt
wc -l /tmp/llms-full.txt   # get total line count
wc -c /tmp/llms-full.txt   # get total byte size
```

**Case A — Both `llms.txt` (200) AND `llms-full.txt` (200)**
- Both files fetched successfully; proceed to the Audit Checklist (Step 4)

**Case B — Only `llms.txt` (200), `llms-full.txt` returned 404**
- Audit `llms.txt`
- Scan its content for any internal reference to `llms-full.txt` (it may be hosted at a non-standard path)
- If a custom path is found → curl that path and audit it
- If not found → report `llms-full.txt` as absent and not referenced

**Case C — `llms.txt` returned 404**
- Report that neither file is present at the standard paths
- Note whether `robots.txt` gave any hints (some sites reference llms.txt inside robots.txt)
- Report clearly to the user (see Response Templates section below)

**robots.txt (always check regardless of Case)**
- Even if `llms.txt` is missing, always read and audit `robots.txt` for AI-access signals

---

### Step 4: Audit the files

#### `llms.txt` Audit

Check for the following. Mark each ✅ or ❌:

**Structure**
- [ ] Starts with a single `# H1` title (site/product name)
- [ ] Has a `> blockquote` summary immediately below H1 (1–2 sentence description)
- [ ] Uses `## H2` sections to group links (e.g. Docs, API Reference, Guides, OpenAPI Specs)
- [ ] Each link follows format: `- [Page Title](https://absolute-url): brief description`
- [ ] Has an `## Optional` section for secondary/non-essential content (not required but best practice)
- [ ] No nested headings inside H2 link sections
- [ ] No images, HTML, or tables (plain markdown only)

**Content completeness**
- [ ] Core product/feature pages are listed
- [ ] API reference pages are included (if applicable)
- [ ] Getting started / quickstart pages included
- [ ] SDK/integration guides included (if applicable)
- [ ] Link descriptions are meaningful (not just page titles repeated)
- [ ] All links use absolute URLs (not relative paths)
- [ ] No broken or 404 links visible

**AI-readiness signals**
- [ ] References `llms-full.txt` (either directly or in a Documentation Sets section)
- [ ] Segmented sets for different use cases (advanced but excellent — e.g. Scalekit's topic-specific .txt files)

#### `llms-full.txt` Audit (if available)

- [ ] File exists and is non-empty
- [ ] Contains full page content (not just links)
- [ ] Has clear document boundary markers between pages (e.g. `---` or `# DOCUMENT BOUNDARY`)
- [ ] Each section has a `Source:` URL reference
- [ ] Content is clean markdown (no raw HTML, no JS artifacts)
- [ ] Reasonably sized (warn if extremely large — may exceed LLM context windows)

#### `robots.txt` Signal (check opportunistically)

If robots.txt was surfaced during the process:
- [ ] `User-agent: *` with `Allow: /` — all bots permitted
- [ ] `ai-input=yes` — explicitly permits AI agents to use content
- [ ] `ai-train=no` — training blocked (common and acceptable)
- [ ] Any `Disallow` rules that would block AI crawlers

---

### Step 5: Deliver the report

Structure the output as:

```
## LLMs.txt Audit: [domain]

### Discovery
[What was found and how it was surfaced]

### llms.txt — ✅ Found / ❌ Not Found
[Audit results with ✅/❌ per checklist item]
[Notable strengths]
[Issues found]

### llms-full.txt — ✅ Found / ❌ Not Found / ⚠️ Not Referenced
[Audit results or explanation]

### robots.txt Signal
[If available — what it says about AI access]

### Summary & Recommendations
[3–5 actionable bullets]
```

---

## Response Templates

### Neither llms.txt nor llms-full.txt surfaced

> Neither `llms.txt` nor `llms-full.txt` was discoverable from the provided URL.
>
> This means AI agents and LLMs browsing your docs will have no structured index to work from — they'll need to crawl individual pages or guess at your content structure.
>
> **To fix this**, surface the `llms.txt` URL somewhere Claude (and other AI tools) can see it when fetching your page. Good options:
> - Add it to your page footer (e.g. `LLM usage: /llms.txt`)
> - Include it in a blockquote at the top of your docs homepage or `.md` page version (e.g. `> Documentation index available at: https://yourdomain.com/llms.txt`)
> - Reference it in your `robots.txt` or a `<meta>` tag
>
> Once it's linked from a page that AI agents naturally land on, it becomes discoverable automatically.

### llms.txt found but llms-full.txt not referenced

> `llms.txt` was found and audited. However, `llms-full.txt` was not referenced anywhere in the file.
>
> `llms-full.txt` is the companion file containing the **full content** of all documentation pages in a single file — useful for AI coding assistants (Cursor, Claude Code, Copilot) that need deep context without fetching dozens of individual pages.
>
> **To add it**: Reference it in your `llms.txt` under a `## Documentation Sets` section or similar, like:
> ```
> - [Complete documentation](https://yourdomain.com/llms-full.txt): full content of all pages
> ```
> If you're on Mintlify, it's auto-generated — just make sure it's linked.

---

## Key facts to keep in mind

- **Mintlify** auto-generates both `llms.txt` and `llms-full.txt` for all projects, and adds HTTP headers (`Link: </llms.txt>; rel="llms-txt"`) for discovery
- **Fern** also auto-generates both files
- **Starlight** (Astro) does not auto-generate — must be added manually
- **GitBook** auto-generates `llms.txt`
- The `llms.txt` standard was proposed by Jeremy Howard (fast.ai) in September 2024
- `llms-full.txt` is not part of the original spec but has become widely adopted as the companion file
- No major AI crawler has *officially* committed to following these files, but Cursor, Claude Code, and similar tools actively use them
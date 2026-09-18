# No Outlinks Audit: Dead-End Pages

Finds every blog or content page that has zero outgoing links to any other page on the same domain, then generates 3 targeted outgoing link suggestions per dead-end, with anchor text, placement guidance, and ready-to-paste context copy. Outputs a styled, filterable HTML report.

---

## What this skill does

A **dead-end page** is a page that links out to no other page on the same domain. It absorbs link equity but passes none on, a structural gap that suppresses topical authority and hurts crawl efficiency across the site.

This skill detects dead-end pages by fetching each content page using the correct method for the site's framework (RSC payload for Next.js, standard curl for static and WordPress sites), identifies which have zero qualifying outgoing internal links, clusters them by topic, and generates 3 specific suggestions per page, with the exact anchor text to use, where in the dead-end page to place it, and a sentence ready to drop in.

This is the structural inverse of the Orphan Pages skill:
- **Orphan Pages**: pages with no *incoming* internal links (nobody links TO them)
- **No Outlinks (this skill)**: pages with no *outgoing* internal links (they link out to nobody)

Built for:
- **SEO and content teams** finding content that is silently breaking the internal link graph
- **Developer marketing** auditing a growing blog for structural link gaps
- **Agencies** delivering a dead-end page audit as part of a technical SEO engagement

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
/dev-gtm no-outlinks example.com/blog/
```

Or describe what you want. Claude activates the skill when you provide a domain and ask for a dead-end page audit or outgoing internal links report.

### Claude Web (Free / Pro)

1. Go to **[Settings → Capabilities](https://claude.ai/settings/capabilities)** and enable **Code execution and file creation**
2. Go to **[Customize → Skills](https://claude.ai/customize/skills)**
3. Click **+** → **Create skill** → **Upload a skill**
4. Zip this skill folder and upload it:

cd dev-gtm-claude-skills/skills/no-outlinks-audit
zip -r ../no-outlinks-audit.zip .
zip -r no-outlinks-audit.zip no-outlinks-audit/
```

Upload `no-outlinks-audit.zip` and toggle it on.

---

## Ahrefs Setup (Required)

This skill uses Ahrefs to fetch keyword and traffic data for every page, which powers topically accurate linking suggestions. An active Ahrefs account with API access is required.

### Claude Code

Open `.claude/settings.json` in the cloned repo and add your Ahrefs MCP credentials:

```json
{
  "mcpServers": {
    "Ahrefs": {
      "command": "npx",
      "args": ["-y", "@ahrefs/mcp-server"],
      "env": {
        "AHREFS_API_KEY": "your-ahrefs-api-key"
      }
    }
  }
}
```

### Claude Web (Free / Pro)

Go to **[Settings → Integrations](https://claude.ai/settings/integrations)**, find **Ahrefs**, and connect your account.

---

## How to use

```
Find pages with no outgoing internal links on example.com
```

```
Which blogs on example.com don't link out to anything?
```

```
Run a dead-end page audit for example.com/blog/
```

```
/dev-gtm no-outlinks example.com/blog/
```

---

## Inputs

| Field | Required | Notes |
|-------|----------|-------|
| Domain or URL | ✅ | Domain (`example.com`), full URL, or blog prefix URL |

---

## Output

A self-contained filterable HTML report saved to `/mnt/user-data/outputs/[domain]-dead-end-pages-audit.html` and presented with a download link.

The report contains:
- **Header stats**: Total Blogs, No Outlinks count, Have Outlinks count, Dead-End Rate %, Total Suggestions
- **Detection method fix-tag**: records whether RSC payload, standard curl, or Ahrefs Site Audit was used
- **Cluster sidebar**: topic clusters built automatically from dead-end pages, clickable for filtering
- **Search and filter bar**: live search across all page titles and keywords
- **Per-page cards**: title, URL, top keyword, monthly traffic, cluster tag
- **3 suggestions per dead-end**: Target page to link out to, anchor text (the target page's top keyword), where in the dead-end page to place the link, and a ready-to-paste sentence with the link already embedded

---

## Things to know

**Framework detection runs before any link detection.** The skill checks response headers and HTML source signals to determine whether the site is Next.js, WordPress, Gatsby, or something else before fetching a single page. Running the wrong method on a Next.js site produces an empty shell, with no links found anywhere, even on pages that have many.

**Asset links do not count.** A page that only links to `/logo.png`, `/styles.css`, or `/_next/static/` is still classified as a dead-end. Only links to other content pages on the same domain qualify.

**Self-links do not count.** A page linking to itself is not an outgoing link.

**Dead-end rate above 80% means something is wrong.** If more than 80% of pages are flagged as dead-ends, the detection is almost certainly misconfigured. The skill validates results on 3 sample pages before generating any suggestions and stops if the rate looks wrong.

**Pure SPAs (Nuxt, Angular, Vue) cannot be crawled by curl.** For JS-rendered sites that curl cannot read, the skill stops and explains the three options: Ahrefs Site Audit, Screaming Frog with JS rendering, or confirming the exact framework so the right detection header can be applied.

---

## How it works

1. **Discover content pages**: finds the sitemap via `curl` (tries `/sitemap.xml`, `/sitemap_index.xml`, `robots.txt` in order), extracts all URLs, filters to the content prefix, strips pagination and archive pages
2. **Detect the site framework**: checks response headers (`x-nextjs-prerender`, `x-vercel-cache`) and HTML source (`__NEXT_DATA__`, `_next`, `gatsby`, `generator` meta tag) to select the correct detection method
3. **Detect outgoing links per page**: for Next.js, sends `curl` with `RSC: 1` header to get the React Server Components payload, which contains all rendered links; for static/WordPress: fetches standard HTML and parses the `<article>` or `<main>` content area only
4. **Validate results**: manually confirms 3 sample dead-ends and 3 sample pages-with-links match reality before proceeding; flags and stops if dead-end rate is above 80% or exactly 0%
5. **Fetch keyword data**: calls `Ahrefs:site-explorer-top-pages` for the full content prefix to get the top keyword and traffic for every page in a single call
6. **Cluster by topic**: groups dead-end pages into 5–15 topic clusters adapted to the site's actual content
7. **Generate suggestions**: for each dead-end page, identifies 3 topically related target pages from the full URL list and writes anchor text (the target's top keyword), placement guidance, and a ready-to-paste context copy sentence per suggestion
8. **Generate the HTML report**: reads `references/report-style-reference.html` and builds a fully data-driven report by populating `CC{}` (cluster colour map) and `D[]` (dead-end data); the sidebar builder and `filterAll()` function render all cards from this data

---

## Config schema reference

The JavaScript data objects injected into the HTML report:

```javascript
// Cluster colour map
const CC = {
  "Developer Marketing": "c-devmkt",
  "SEO":                 "c-seo",
  "Content Marketing":   "c-content",
  "Documentation":       "c-docs",
  "GTM Strategy":        "c-gtm"
};

// Dead-end page data: one object per dead-end page
const D = [
  {
    url:     "https://www.example.com/blog/api-authentication",
    title:   "API Authentication Best Practices",
    kw:      "api authentication",
    tr:      340,
    cluster: "Documentation",
    s: [
      {
        to:      "OAuth 2.0 Implementation Guide",             // target page to link OUT TO
        toUrl:   "https://www.example.com/blog/oauth2-guide", // target page URL
        anchor:  "oauth 2.0 implementation",                  // target page's top keyword
        place:   "After the section on token storage, when recommending secure auth flows",
        copy:    "For teams implementing token-based auth, a detailed look at <a href=\"https://www.example.com/blog/oauth2-guide\">oauth 2.0 implementation</a> covers the handshake flow and scoping patterns that prevent over-permissioning."
      }
      // × 3 per dead-end page
    ]
  }
];
```

> **Note on field direction:** to and toUrl refer to the **target page** (the page being linked TO from the dead-end page), not the dead-end page itself. The suggestion card labels this "Link To", not "Source Page".

---

## File structure

```
no-outlinks-audit/
├── SKILL.md                          # Skill instructions Claude follows
├── README.md                         # This file
└── references/
    └── report-style-reference.html   # Canonical visual and code reference for the HTML report
```

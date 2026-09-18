# Orphan Pages: Internal Linking Opportunities

Discovers every blog or content page that receives zero incoming internal links, clusters them by topic, and generates 3 specific linking suggestions per orphan, with exact anchor text, placement guidance, and ready-to-paste context copy. Outputs a styled, filterable HTML report.

---

## What this skill does

An **orphan page** is a page that no other page on the site links to. It cannot be discovered through normal navigation and is invisible to crawlers following internal links. This audit finds every orphan in a content section and recommends exactly which existing pages should link to each one.

The skill discovers all content pages via sitemap, identifies which have incoming links using Ahrefs, derives keywords for each orphan, clusters pages by topic, and generates 3 fully formed linking suggestions per orphan, including the anchor text to use, where in the source page to place the link, and a sentence ready to copy and paste.

Built for:
- **SEO and content teams** finding pages that are being published but never surfaced through navigation
- **Developer marketing** fixing structural link gaps across a growing content library
- **Agencies** delivering an internal linking audit as a client deliverable

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
/dev-gtm orphan-pages example.com/blog/
```

Or describe what you want. Claude activates the skill when you provide a domain and ask for an orphan page audit or internal linking report.

### Claude Web (Free / Pro)

1. Go to **[Settings → Capabilities](https://claude.ai/settings/capabilities)** and enable **Code execution and file creation**
2. Go to **[Customize → Skills](https://claude.ai/customize/skills)**
3. Click **+** → **Create skill** → **Upload a skill**
4. Zip this skill folder and upload it:

```bash
cd dev-gtm-claude-skills/skills/orphan-pages-internal-linking-opportunities
zip -r ../orphan-pages-internal-linking-opportunities.zip .
```

Upload `orphan-pages-internal-linking-opportunities.zip` and toggle it on.

---

## Ahrefs Setup (Required)

This skill uses two Ahrefs tools to identify orphan pages and fetch keyword data. An active Ahrefs account with API access is required.

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
Run an orphan page audit for example.com
```

```
Which pages on example.com/blog/ have no internal links?
```

```
Find pages nobody links to on my site
```

```
/dev-gtm orphan-pages example.com/blog/
```

If the content section prefix (`/blog/`, `/articles/`, etc.) is not clear from the input, Claude asks before starting.

---

## Inputs

| Field | Required | Notes |
|-------|----------|-------|
| Domain or URL | ✅ | Domain (`example.com`), full URL, sitemap URL, or blog prefix URL |
| Content prefix | ⬜ | Optional. If not provided and not inferrable from the URL, Claude asks |

---

## Output

A self-contained filterable HTML report saved to `/mnt/user-data/outputs/[domain]-orphan-linking-audit.html` and presented with a download link.

The report contains:
- **Header stats**: Total Pages, Orphan Count, Pages With Links, Gap Rate %, Total Suggestions
- **Cluster sidebar**: topic clusters built automatically from the orphan set, clickable for filtering
- **Search and filter bar**: live search across all orphan titles and keywords
- **Per-orphan cards**: title, URL, top keyword, monthly traffic, cluster tag
- **3 suggestions per orphan**: Source page, anchor text, where to place it, and ready-to-paste context copy with the link already embedded as an HTML `<a>` tag

---

## Things to know

**Ahrefs is queried site-wide with no source URL filter.** The `site-explorer-pages-by-internal-links` call is intentionally run without a `url_from` filter. Filtering by source prefix misses links from the homepage, service pages, and navigation, producing false orphans. The fix-tag in the report footer records this.

**Keyword data may be absent for newer pages.** When a page has no Ahrefs ranking data, the skill derives its primary keyword from the URL slug (`/blog/developer-marketing-strategy` → "developer marketing strategy"). This is noted in the report.

**Suggestions are topically justified, not generic.** Every suggestion is chosen because the source page covers the same or adjacent subject matter. "Link from your homepage" is never suggested unless the homepage genuinely relates to the orphan's topic.

**JS-rendered sites cannot be crawled by curl.** If the sitemap is empty or the blog index returns no URLs from curl, the skill will ask for a static sitemap export or a manual URL list.

---

## How it works

1. **Discover content pages**: finds the sitemap via `curl` (tries `/sitemap.xml`, `/sitemap_index.xml`, `robots.txt`), extracts all `<loc>` URLs, filters to the content prefix, and strips pagination, category, and tag pages
2. **Identify orphans**: calls `Ahrefs:site-explorer-pages-by-internal-links` site-wide (no `url_from` filter) to get all pages with at least one incoming link; anything in the full URL list but not in this result is an orphan
3. **Fetch keyword data**: calls `Ahrefs:site-explorer-top-pages` for the full content prefix to get the top keyword and monthly traffic for every page in one call
4. **Derive missing keywords**: for any orphan not in the Ahrefs response, derives the primary keyword from the URL slug
5. **Cluster by topic**: groups orphans into 5–15 topic clusters adapted to the site's actual content
6. **Generate suggestions**: for each orphan, identifies 3 topically related pages from the full URL list and writes anchor text, placement guidance, and a ready-to-paste context copy sentence for each
7. **Generate the HTML report**: reads `references/report-style-reference.html` and builds a fully data-driven report by populating the `CC{}` (cluster colour map) and `D[]` (orphan data) JavaScript objects; the sidebar builder and `filterAll()` function render all cards from this data

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

// Orphan page data: one object per orphan
const D = [
  {
    url:     "https://www.example.com/blog/developer-marketing-strategy",
    title:   "Developer Marketing Strategy: A Complete Guide",
    kw:      "developer marketing strategy",
    tr:      null,
    cluster: "Developer Marketing",
    s: [
      {
        from:    "How to Build a Developer Community",
        fromUrl: "https://www.example.com/blog/build-developer-community",
        anchor:  "developer marketing strategy",
        place:   "In the intro when explaining why community building is part of a broader go-to-market plan",
        copy:    "Before diving into community tactics, it helps to understand how they fit into a wider <a href=\"https://www.example.com/blog/developer-marketing-strategy\">developer marketing strategy</a>, especially if you are building from scratch."
      }
      // × 3 per orphan
    ]
  }
];
```

---

## File structure

```
orphan-pages-internal-linking-opportunities/
├── SKILL.md                          # Skill instructions Claude follows
├── README.md                         # This file
└── references/
    └── report-style-reference.html   # Canonical visual and code reference for the HTML report
```

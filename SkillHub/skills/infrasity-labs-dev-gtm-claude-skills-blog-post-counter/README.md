# Blog Post Counter

Finds the blog URL for any company and counts the total number of unique blog posts published. Works from a company name alone — no URL required.

---

## What this skill does

Given a company name, domain, or sitemap URL, this skill finds the blog, crawls the sitemap, filters out pagination, category pages, and duplicate URLs, and returns an exact count of unique blog posts.

It handles multi-section blogs (e.g. `/blog/` and `/insights/` on the same domain), sitemap indexes with multiple child sitemaps, subdomain blogs (`blog.company.com`), and falls back to DataForSEO indexed URL data when a sitemap is missing or unreadable.

Built for:
- **Content and SEO teams** benchmarking competitors' publishing volume
- **Developer marketing** tracking content output across a list of companies
- **Agencies** running content audits for clients

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
/dev-gtm blog-count stripe.com
```

Or just ask naturally — Claude will activate the skill automatically.

### Claude Web (Free / Pro)

1. Go to **[Settings → Capabilities](https://claude.ai/settings/capabilities)** and enable **Code execution and file creation**
2. Go to **[Customize → Skills](https://claude.ai/customize/skills)**
3. Click **+** → **Create skill** → **Upload a skill**
4. Zip this skill folder and upload it:

```bash
cd dev-gtm-claude-skills/skills
zip -r blog-post-counter.zip blog-post-counter/
```

Upload `blog-post-counter.zip` and toggle it on.

---

## DataForSEO Setup (Optional)

This skill uses DataForSEO as a **fallback only** — when a sitemap cannot be found or is unreadable. Most domains have a readable sitemap, so this is not needed for most runs.

If you want full fallback coverage:

### Claude Code

Open `.claude/settings.json` in the cloned repo and replace the placeholder credentials:

```json
{
  "mcpServers": {
    "dataforseo": {
      "command": "npx",
      "args": ["-y", "@dataforseo/mcp-server"],
      "env": {
        "DATAFORSEO_USERNAME": "your-dataforseo-username",
        "DATAFORSEO_PASSWORD": "your-dataforseo-password"
      }
    }
  }
}
```

### Claude Web (Free / Pro)

Go to **[Settings → Integrations](https://claude.ai/settings/integrations)**, find **DataForSEO**, and connect your account.

---

## How to use

```
How many blog posts does stripe.com have?
```

```
Count the blog posts for these companies: vercel.com, netlify.com, railway.app
```

```
/dev-gtm blog-count linear.app
```

For batch runs, provide a list of company names or domains and the skill returns a table.

---

## Output

**Single company:**

```
Company:       Stripe
Blog URL:      https://stripe.com/blog/
Unique posts:  312
```

**Batch run:**

| Company | Blog URL | Unique Posts |
|---------|----------|-------------|
| Stripe | https://stripe.com/blog/ | 312 |
| Vercel | https://vercel.com/blog | 187 |
| Railway | https://railway.app/blog | 94 |

---

## How it works

1. **Resolve the sitemap** — tries `/sitemap.xml`, `/sitemap_index.xml`, and `www.` variants in order. Falls back to a web search if none work.
2. **Fetch all URLs** — if the sitemap is an index, fetches every child sitemap. Blog-specific child sitemaps (`post-sitemap.xml`, `blog-sitemap.xml`) are fetched first.
3. **Filter to blog posts** — keeps only URLs matching blog path patterns (`/blog/`, `/insights/`, `/articles/`, etc.) or blog subdomains (`blog.domain.com`), with at least one path segment after the pattern.
4. **Deduplicate** — removes listing pages, pagination, category/tag/author archives, RSS feeds, and query-param duplicates.
5. **Return the count** — reports each blog section separately if the domain has more than one, then sums to a total.

---

## Notes

- Sitemap data reflects what the site explicitly publishes. If a sitemap is capped or incomplete, the count will be lower than reality.
- Domains with multiple blog sections (e.g. both `/blog/` and `/resources/`) are reported per section with a combined total.
- The skill never mentions internal tool names in its output.

---

## File structure

```
blog-post-counter/
├── SKILL.md    # Skill instructions Claude follows
└── README.md   # This file
```

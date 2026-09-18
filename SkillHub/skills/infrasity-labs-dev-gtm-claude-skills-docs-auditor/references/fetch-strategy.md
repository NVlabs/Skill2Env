# Fetch Strategy

## URL derivation rules

When the user gives `https://docs.example.com/`, derive and fetch ALL of these:

### Round 1 — Infrastructure files (fetch first, in parallel)
```
https://docs.example.com/robots.txt
https://docs.example.com/sitemap.xml
https://docs.example.com/llms.txt
https://docs.example.com/llms-full.txt
https://example.com/robots.txt          ← root domain fallback
https://example.com/llms.txt            ← root domain fallback
https://example.com/sitemap.xml         ← root domain fallback
```

### Round 2 — Core pages (fetch these regardless)
```
https://docs.example.com/               ← homepage / intro
https://docs.example.com/quickstart     ← try: /quickstart, /getting-started, /get-started, /start
https://docs.example.com/changelog      ← try: /changelog, /releases, /release-notes, /whats-new
```

### Round 3 — Probe pages (try common slugs, use what works)
```
API Reference:    /api, /api-reference, /reference, /api-docs
FAQ/Support:      /faq, /troubleshooting, /help, /support
Tutorials:        /tutorials, /guides, /examples, /use-cases
Install/Setup:    /installation, /setup, /configuration, /config
```

### Round 4 — Sidebar links (pick 2–3 from the nav you found in Round 2)
Pick one deep settings page and one use-case/tutorial page from the sidebar links
you discovered. These are for depth-checking (check 4.3).

---

## What to extract from each file type

### robots.txt
- Is `Disallow: /` present? → everything blocked
- Are AI bots mentioned? Look for: `GPTBot`, `ClaudeBot`, `anthropic-ai`, `PerplexityBot`, `Googlebot-Extended`, `ChatGPT-User`, `cohere-ai`, `CCBot`
- Is there a `Sitemap:` directive?

### sitemap.xml
- Does it exist?
- Does it list doc page URLs?
- How many URLs? (rough count is fine)

### llms.txt
- Does it exist and have content?
- Does it link to doc pages?
- Does it reference `llms-full.txt`?

### llms-full.txt
- Does it exist?
- Is it non-empty?

### HTML pages
- `<title>` tag
- `meta name="description"` content
- `link rel="canonical"` href — check if it matches the actual domain
- `meta name="robots"` — check for noindex
- Sidebar HTML — look for `<nav>`, `<aside>`, or elements with class names like `sidebar`, `nav-menu`
- Breadcrumbs — look for `<nav aria-label="breadcrumb">` or class `breadcrumb`
- Search — look for `<input type="search">` or `role="search"` or class `search`
- Prev/next links — look for `rel="prev"` / `rel="next"` or text "Previous" / "Next" near bottom
- Code blocks — `<code>`, `<pre>`, language labels like `python`, `javascript`, `curl`
- Cross-links — `<a href="...">` pointing to other pages within the same domain
- GitHub links — links containing `github.com`
- Community links — links containing `discord`, `slack`, `forum`, `community`, `reddit`
- Version signals — text matching patterns like `v\d+\.\d+`, `"latest"`, version badge elements
- Last updated — text matching `"last updated"`, `"updated on"`, date stamps near top/bottom of page
- Install commands — `pip install`, `npm install`, `yarn add`, `brew install`, `cargo add`

---

## Handling fetch failures

| Failure type | How to score |
|---|---|
| 404 / not found | Mark as **fail** for that check |
| Connection timeout | Mark as **warn** — note "Could not verify" |
| Auth required (401/403) | Mark as **warn** — note "Requires authentication" |
| JS-rendered (sparse HTML < 200 chars) | Mark as **warn** — note "May be JS-rendered; check inconclusive" |
| Redirect to different domain | Follow redirect; note the redirect in evidence |

---

## Minimum fetch requirement

You must fetch at least **6 pages** before generating the report.
If fewer than 6 pages are accessible, note it in the report summary.
Never generate the report after fetching only 1–2 pages.
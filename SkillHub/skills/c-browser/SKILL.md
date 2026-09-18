---
name: c-browser
description: Headless browser automation — navigate pages, click elements, fill forms, take screenshots, scrape content using agent-browser or playwright-cli.
tags: [browser, automation, scraping, web]
---

# Browser Automation

## agent-browser (Vercel)

Navigate and interact with web pages using structured snapshots:

```bash
# Open a URL
agent-browser open "https://example.com"

# Get interactive element snapshot (shows clickable refs)
agent-browser snapshot -i

# Click an element by ref
agent-browser click @e2

# Fill a form field
agent-browser fill @e5 "search query"

# Take annotated screenshot
agent-browser screenshot --annotate

# Type text
agent-browser type "hello world"

# Press keys
agent-browser press Enter
```

## playwright-cli (Microsoft)

Token-efficient browser automation designed for AI agents:

```bash
# Install browser (first time)
playwright-cli install-browser

# Navigate to URL
playwright-cli navigate "https://example.com"

# Get page snapshot
playwright-cli snapshot

# Click element
playwright-cli click "Submit button"

# Fill input
playwright-cli fill "Search" "query text"

# Screenshot
playwright-cli screenshot
```

## Guidelines

- Use agent-browser for AI-driven web interaction (snapshot-ref pattern)
- Use playwright-cli for structured automation and testing flows
- Always check snapshots before clicking — element refs change between pages
- For login flows, navigate step by step and verify each page loads
- Respect robots.txt and rate limits when scraping

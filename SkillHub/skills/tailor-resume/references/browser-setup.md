# Browser Automation Setup

Standard sequence for skills that use Claude in Chrome MCP tools to fetch web pages.

## Tab Setup

```
1. tabs_context_mcp → get browser state
2. tabs_create_mcp → create a new tab
3. navigate → target URL
4. get_page_text → extract page content
```

## Context Window Safety

**Avoid `get_page_text` on large or dynamic pages** (job boards, search results, listing pages, dashboards). It returns the entire page and can blow out the context window, making the conversation unrecoverable.

Instead, use targeted extraction:
- `javascript_tool` with a selector to extract only the content you need
- `read_page` to get structured element refs
- `get_page_text` is safe only for simple pages with a single article/posting

## Error Handling

- If `tabs_context_mcp` returns no tabs or an error, ask the user to confirm Chrome is open with the Claude in Chrome extension active.
- If `navigate` fails or the page doesn't load, ask the user to paste the content directly.
- If `get_page_text` returns empty or unusable content, try `read_page` as a fallback, then ask the user to paste if that also fails.
- Do not retry a failing page more than once. Move on and ask the user for the content.

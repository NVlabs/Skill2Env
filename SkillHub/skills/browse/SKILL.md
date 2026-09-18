---
name: browse
description: |
  Visual feedback browser automation with multi-session, multi-tab, iframe support,
  and enterprise primitives. Navigate sites, interact with elements, manage tabs/sessions,
  handle file uploads, dropdowns, iframes, and verify results using the
  screenshot-analyze-act-verify loop. Use when asked to "open a site", "test a page",
  "fill a form", "check a deployment", "browse to", "click on", "verify the UI", "compare
  pages side by side", or any task involving web interaction. Also use proactively when a task
  would benefit from checking a live URL.
allowed-tools: Browser,Read,Grep,Glob
---

# Browse — Visual Feedback Browser Automation

You have a `Browser` tool with an action-based interface. This skill teaches you how to use it
effectively with a **screenshot → analyze → act → verify** loop that prevents blind clicking.

## Core Principle

Never act without seeing. Never assume an action worked. Always verify.

```
OBSERVE  →  DECIDE  →  ACT  →  VERIFY
(get_state   (analyze    (click/    (get_state
+ screenshot  elements)   type)     + screenshot
                                    + compare)
```

## Starting a Session

Every browser session starts the same way:

1. **Navigate** to the target URL
2. **Observe** the page with `get_state` — this returns the DOM with indexed interactive elements AND the page text
3. **Screenshot** to see the visual layout

```
Browser { action: "navigate", url: "https://example.com" }
Browser { action: "get_state" }
Browser { action: "screenshot" }
```

Read the screenshot to understand the visual layout. The `get_state` output gives you:
- URL and title
- Scroll position (how far down the page you are)
- Interactive element count (links, inputs, buttons)
- Indexed elements: `[0] <button> "Submit"`, `[1] <input:text> name="email"`
- Page text (first 3000 chars)

### JSON Format

For structured processing, use `format: "json"`:
```
Browser { action: "get_state", format: "json" }
```
Returns: `{ url, title, scroll, stats, elements: [{index, tag, text, ...}], text, session_id, active_tab_id }`

## Interacting with Elements

**Always prefer element indices over CSS selectors.** The indices come from `get_state` and are
reliable. CSS selectors can break if the page structure changes.

```
Browser { action: "click_element", index: 5 }
Browser { action: "type_element", index: 3, value: "hello@example.com" }
```

Fall back to CSS selectors only when:
- The element doesn't appear in the indexed list
- You need to target something very specific (like `input[name="csrf_token"]`)

```
Browser { action: "click", selector: "#submit-btn" }
Browser { action: "fill", selector: "input[name='email']", value: "test@example.com" }
```

## Keyboard Input (send_keys)

For named keys and key combinations:

```
Browser { action: "send_keys", keys: "Enter" }
Browser { action: "send_keys", keys: "Tab Tab Enter" }
Browser { action: "send_keys", keys: "Ctrl+a" }
Browser { action: "send_keys", keys: "Shift+Tab" }
```

Supported named keys: Enter, Tab, Escape, Backspace, Delete, Space, ArrowUp/Down/Left/Right, Home, End, PageUp, PageDown, F1-F12.
Modifiers: Ctrl, Alt, Shift, Meta/Cmd. Sequences: space-separated.

## File Upload

```
Browser { action: "upload_file", selector: "input[type='file']", file_path: "/path/to/file.pdf" }
```

## Dropdowns

```
Browser { action: "dropdown_options", selector: "#my-select" }
Browser { action: "select_dropdown", selector: "#my-select", value: "option_value" }
```

## Structured Data Extraction

Extract structured data from the page using CSS selectors:

```
Browser { action: "extract", schema: {"title": "h1", "price": ".price", "description": ".desc"} }
```

Returns JSON: `{"title": "Product Name", "price": "$29.99", "description": "..."}`

## Multi-Tab Workflows

Open, switch between, and close tabs for side-by-side comparison:

```
Browser { action: "navigate", url: "https://site-a.com" }
Browser { action: "new_tab", url: "https://site-b.com" }
Browser { action: "list_tabs" }
Browser { action: "switch_tab", tab_id: "PREVIOUS_TAB_ID" }
Browser { action: "close_tab", tab_id: "TAB_TO_CLOSE" }
```

Tab IDs are strings (CDP target IDs). Get them from `list_tabs`.

## Multi-Session Workflows

Use separate sessions for isolated browser instances (different profiles, auth states):

```
Browser { action: "new_session", session_id: "admin", profile_name: "admin-profile" }
Browser { action: "navigate", url: "https://app.com/admin", session_id: "admin" }
Browser { action: "new_session", session_id: "user", profile_name: "user-profile" }
Browser { action: "navigate", url: "https://app.com/dashboard", session_id: "user" }
Browser { action: "list_sessions" }
Browser { action: "close_session", session_id: "admin" }
```

### Named Profiles

Profiles persist cookies and state across sessions:
- `profile_name: "my-profile"` → stored in `~/.claude/browser-profiles/my-profile/`
- `user_data_dir: "/custom/path"` → raw Chrome user data directory
- `profile_dir: "Profile 1"` → Chrome's `--profile-directory` flag

## Attach Mode (Remote Chrome)

Connect to an already-running Chrome instance:

```
Browser { action: "new_session", session_id: "remote", cdp_url: "http://localhost:9222" }
```

Or set `BROWSER_CDP_URL=http://localhost:9222` env var for the default session.

In attach mode, `close` disconnects without killing Chrome.

## Iframe Support

```
Browser { action: "list_frames" }
Browser { action: "click_element", index: 0, frame_id: "FRAME_ID" }
Browser { action: "fill", selector: "input", value: "text", frame_id: "FRAME_ID" }
```

Frame IDs come from `list_frames`. Use `frame_id` on any DOM action to target elements inside iframes.

## Events & Dialogs

The browser captures events (dialogs, navigations, crashes, downloads):

```
Browser { action: "get_events" }
Browser { action: "set_dialog_auto_dismiss", enabled: true }
```

Dialogs (alert/confirm/prompt) are auto-dismissed by default. Disable with `enabled: false` to handle manually.

## The Verify Loop

After **every** action that changes the page, you must verify:

```
1. Take action (click, type, navigate, submit)
2. Wait briefly if needed:  Browser { action: "wait_for", selector: ".result", timeout: 3000 }
3. Observe again:           Browser { action: "get_state" }
4. Screenshot again:        Browser { action: "screenshot" }
5. Compare: did the page change as expected?
   - YES → continue to next step
   - NO  → try a different approach (different element, different selector, scroll first)
```

## Iteration Budget

You have a maximum of **10 iterations** (observe-act-verify cycles) per task. This prevents
infinite loops. If you haven't achieved the goal in 10 iterations:

1. Stop
2. Report what you accomplished and what failed
3. Include the last screenshot as evidence

Count your iterations. Mention the count when reporting.

## Error Recovery

When something doesn't work:

1. **Element not found** — the page may have changed. Run `get_state` again to refresh the element indices.
2. **Click didn't work** — the element might be obscured. Try `scroll_to` first, then click again.
3. **Page didn't load** — try `wait_for` with a key selector, or `reload`.
4. **Form submission failed** — screenshot to see error messages, read them, adjust input.
5. **Same action 3 times** — the Browser tool has loop detection. If you get a loop warning, you MUST try a completely different approach.

Fallback chain for clicking:
```
click_element by index  →  click by CSS selector  →  evaluate with JS click  →  scroll + retry
```

## Scrolling

Pages are often longer than the viewport. The `get_state` output shows scroll position.
If you need elements below the fold:

```
Browser { action: "scroll_to", value: "500" }     // scroll down 500px
Browser { action: "scroll_to", selector: "#footer" }  // scroll to element
Browser { action: "get_state" }                     // refresh elements after scroll
```

Always `get_state` after scrolling — the element indices change.

## Evidence and Reporting

When completing a task, provide evidence:

1. **Before state** — screenshot of the page before your actions
2. **Actions taken** — list of what you did (clicked X, typed Y, navigated to Z)
3. **After state** — screenshot showing the result
4. **Verification** — what you checked to confirm the task is done

Format your report:
```
## Browser Task: [description]

**URL:** https://example.com/page
**Session:** default
**Iterations:** 4/10

### Actions
1. Navigated to https://example.com
2. Clicked [3] <button> "Login"
3. Typed email into [5] <input:email>
4. Typed password into [7] <input:password>
5. Sent keys: Enter

### Verification
- Page title changed to "Dashboard"
- User avatar visible in header
- No error messages present

### Screenshots
- Before: [screenshot 1]
- After: [screenshot 2]
```

## JavaScript Evaluation

For complex checks or actions not covered by built-in actions:

```
Browser { action: "evaluate", value: "document.querySelectorAll('.error').length" }
Browser { action: "evaluate", value: "window.localStorage.getItem('token')" }
```

This is powerful but use it sparingly — prefer the built-in actions.

## Cookies

For authenticated sessions:
```
Browser { action: "cookies_get" }
Browser { action: "cookies_set", cookie: { name: "session", value: "abc123", domain: ".example.com" } }
Browser { action: "cookies_clear" }
```

## Closing

Always close the browser when done:
```
Browser { action: "close" }
```

This frees system resources. The browser will auto-launch again if needed.

## Quick Reference

| Goal | Action | Notes |
|------|--------|-------|
| See the page | `get_state` + `screenshot` | Always first |
| See page (structured) | `get_state` with `format: "json"` | For parsing |
| Click a button | `click_element` with index | From get_state |
| Type text | `type_element` with index and value | |
| Press keys | `send_keys` with keys | "Enter", "Tab", "Ctrl+a" |
| Navigate | `navigate` with url | |
| Upload a file | `upload_file` with selector, file_path | |
| Read dropdown | `dropdown_options` with selector | Returns [{value,text,selected}] |
| Select dropdown | `select_dropdown` with selector, value | |
| Extract data | `extract` with schema | Returns structured JSON |
| Wait for content | `wait_for` with selector | |
| Scroll down | `scroll_to` with value or selector | |
| Open new tab | `new_tab` with optional url | |
| Switch tab | `switch_tab` with tab_id | |
| List tabs | `list_tabs` | |
| Close tab | `close_tab` with tab_id | |
| New session | `new_session` with session_id | Optional: profile_name, cdp_url |
| List sessions | `list_sessions` | |
| List frames | `list_frames` | For iframe inspection |
| Get events | `get_events` | Dialog, crash, download, navigation |
| Run JS | `evaluate` with value | |
| Go back | `back` | |
| Save page as PDF | `pdf` | |
| Check cookies | `cookies_get` | |
| Done | `close` | |

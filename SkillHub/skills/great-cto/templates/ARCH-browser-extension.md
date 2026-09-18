---
name: ARCH-browser-extension
description: Mandatory ARCH for browser extensions: Manifest version, Three-worlds split (SW/content/popup/offscreen), Storage decision, Permissions justification per URL pattern, Web Store pre-flight checklist, Cross-browser compat
when_to_use: Writing ARCH for browser-extension archetype. Required for Web Store submission
applies_to:
  - browser-extension
---

# ARCH-{slug}.md — Browser extension project template

> **Reader:** the engineer who will ship the next Web Store update without getting flagged by the reviewers.
> **Source:** `skills/great_cto/templates/ARCH-browser-extension.md`. Mandatory for `archetype: browser-extension`.
> Required by `architect.md` SECURITY_REQUIRED block. Cannot ship without `## Permissions Justification` + `## Web Store Pre-flight`.

## Decision (one sentence)
{What the extension does for the user — no internal implementation language, the same sentence Web Store reviewers will read.}

## Manifest version
- **MV3** required for Chrome / Edge (MV2 deprecated). Firefox accepts both but MV3 preferred. Safari uses Web Extensions native, MV3-compatible.
- Single-purpose policy: this extension does **one thing** (declared above). If you can't describe purpose in one sentence, scope is too broad → Web Store will reject.

## Three-worlds split
| World | Runs in | Purpose | Lifetime |
|---|---|---|---|
| **Service worker** (`background.js`) | Browser process, no DOM | Cross-tab state, message routing, scheduled tasks via `chrome.alarms`, network requests with sensitive headers | Ephemeral; restarts on event, terminates after 30 s idle |
| **Content script** (`content.js`) | Page's process, sandboxed DOM | DOM manipulation, page-content scraping, message-relay to SW | Lives with the page tab |
| **Popup / options / side-panel** | Extension's own iframe | User-facing UI | Opens on click, closes on blur (popup) or persistent (side-panel API) |
| **Offscreen document** (Chrome 109+) | Browser process, has DOM | Long-running work needing DOM/audio/iframe API (LLM inference, audio analysis) | Created on demand by SW |

For long-running work (>50 ms): SW handler returns ack → spawns offscreen doc → reports back via message. Never block the SW handler.

## Storage decision
| Purpose | API | Why |
|---|---|---|
| User preferences (small, sync across devices) | `chrome.storage.sync` | 100 KB total quota, automatic sync |
| Detection cache / large local data | `chrome.storage.local` | 10 MB quota, faster, no sync |
| Per-tab transient state | `chrome.storage.session` | clears on browser close, fast |
| Cookies (existing site auth) | `chrome.cookies` | requires `cookies` permission |

API keys / OAuth tokens **never in `chrome.storage`** (unencrypted, readable by other extensions with `storage` permission). Use `chrome.identity.launchWebAuthFlow` + server-side proxy.

## Permissions justification
| Permission | Why needed | What user sees | Web Store reviewer note |
|---|---|---|---|
| `storage` | persist user preferences | "store your settings" | low risk, common |
| `activeTab` | act on current tab when user invokes extension | "see this tab when you click the extension" | preferred over broad host_permissions |
| `scripting` | inject sidebar/UI on demand | "inject scripts you can interact with" | scoped via activeTab |
| `optional_host_permissions: <all_urls>` | scrape page text on user-enabled domains | "access your data on websites you allow at runtime" | RUNTIME prompt — not blanket; flagged by reviewers if blanket |

Forbidden by default (unless single-purpose justifies):
- `<all_urls>` host_permission upfront → review takes 7+ days, often rejected
- `tabs` (broad — see all tab URLs and titles)
- `cookies` unless syncing existing site auth
- `webRequest` blocking (deprecated in MV3 anyway, use `declarativeNetRequest`)
- `nativeMessaging` (auto-flag)

## Web Store pre-flight checklist (filled by web-store-reviewer subagent)
- [ ] Privacy practices form filled in developer dashboard
  - Data type collected: {user activity / website content / personally identifiable info / NONE}
  - Purpose: {core function / analytics / ads / NONE}
  - Sold to third parties: {no}
  - Used for ad targeting: {no}
- [ ] Single-purpose declaration clearly stated in store description
- [ ] Each permission has a 1-sentence justification visible to reviewers
- [ ] No `unsafe-eval` or `unsafe-inline` in CSP
- [ ] No source maps in production zip
- [ ] DOMPurify applied to any HTML rendered from external sources
- [ ] `host_permissions: <all_urls>` either absent OR moved to `optional_host_permissions` with runtime prompt
- [ ] Screenshots: 5 minimum, 1280×800, show actual extension UI
- [ ] Demo video: 30-60 s loop showing core flow
- [ ] Service worker terminates cleanly (no `setInterval` / `setTimeout` long-lived)
- [ ] Content scripts injected at `document_idle` (not `document_start` unless absolutely required)

## Cross-browser compatibility
| Browser | Manifest | API namespace | Caveats |
|---|---|---|---|
| Chrome / Edge | MV3 | `chrome.*` | Side Panel API since Chrome 114 |
| Firefox | MV3 (since 109) | `browser.*` (Promise-based) | Use `webextension-polyfill` for unified API surface |
| Safari | Web Extensions (Xcode wrapper) | `browser.*` | needs Xcode project; native iOS/macOS app wrapper |
| Opera | Chrome-compatible | `chrome.*` | distributed via Opera addons |

Polyfill: `import browser from 'webextension-polyfill';` then use `browser.*` everywhere — works on all 4.

## Performance budget
- Content script bundle: < 100 KB (gzipped)
- Service worker bundle: < 250 KB (gzipped)
- Service worker handler: returns within 50 ms
- Long-running work: offloaded to offscreen doc, not in SW handler
- No polling: `chrome.alarms` minimum interval = 30 s

## Out of scope (explicit)
- {e.g. native messaging — phase 2 if needed}
- {e.g. firefox-specific UI — phase 2}

## Security
- CSP enforced in manifest: `script-src 'self'; object-src 'self'`
- No remote code execution: all JS bundled at build time
- API keys server-side only (extension is thin client; backend holds the key)
- Prompt-injection-via-page-content (if extension wraps an LLM): treat scraped text as untrusted, sanitize before LLM context — see browser-extension-pack.md § Cross-pack stacking
- Iframe injection (sidebar / overlay): use `chrome-extension://<id>/sidebar.html` URL, not `data:`/inline; isolate via `iframe.style.all = 'initial'`; postMessage with origin check

## Open questions
- {Items to decide before next ARCH revision}

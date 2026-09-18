---
name: browser-extension-pack
description: MV3 service worker patterns, three-worlds architecture (SW/content/popup/offscreen), storage decision table, host_permissions audit, Web Store review preflight, cross-browser compat
when_to_use: Building Chrome/Firefox/Edge/Safari extensions. Read at architecture time + by web-store-reviewer subagent
applies_to:
  - browser-extension
---

# Browser Extension Pack

> Extends `browser-extension` archetype with MV3 service worker patterns, content script isolation, host_permissions audit, Web Store review pre-flight, and cross-browser compatibility for Chrome / Firefox / Safari / Edge extensions.
> Auto-loaded when `archetype: browser-extension` is detected in PROJECT.md.
> Also loaded explicitly via `packs: [browser-extension-pack]`.

## Why a separate archetype (not `mobile-app`)

A browser extension shares almost nothing with a mobile app:

- **Runtime model**: event-driven service worker (no persistent process), not a long-lived app process
- **Architecture**: 3 isolated worlds (extension code, page DOM, content script) that communicate via `chrome.runtime.sendMessage` — hard to model with mobile patterns
- **Distribution**: Web Store review (24h-7d depending on browser) — different from App Store / Play
- **Update mechanism**: silent auto-update on the Store's schedule (no user prompt, no version pinning) — opposite of mobile
- **Threat model**: extensions read user's web sessions; the security stakes are entirely different
- **Manifest version migration**: MV2 deprecation killed thousands of extensions in 2024-2025; MV3 forced a complete rewrite

Cross-browser concerns (Chrome / Firefox / Safari / Edge) deserve their own pack — none of which apply to mobile apps.

## MV3 mental model — what changed from MV2

Manifest V3 is mandatory in Chrome since June 2024. If your extension is still MV2, it's already removed from Chrome Web Store.

The four changes that matter most:

### 1. Service worker replaces background page

```js
// MV2 (deprecated, won't ship)
// background.js — runs forever
chrome.runtime.onInstalled.addListener(() => {
  state.foo = 'persists across events';  // ← lost in MV3
});
```

```js
// MV3 — service worker, can terminate any time
// service-worker.js
chrome.runtime.onInstalled.addListener(() => {
  // Immediate-only logic. State lives in storage, not memory.
  chrome.storage.local.set({ foo: 'persists' });
});

chrome.alarms.onAlarm.addListener(async () => {
  const { foo } = await chrome.storage.local.get('foo');
  // ...
});
```

**Rule**: never assume background state survives between events. Every handler reads from `chrome.storage` first.

### 2. `declarativeNetRequest` replaces `webRequest` blocking

For ad blockers, content blockers, modifying requests:

```json
// rules.json — declarative, evaluated by browser
{
  "id": 1,
  "priority": 1,
  "action": { "type": "block" },
  "condition": {
    "urlFilter": "||doubleclick.net^",
    "resourceTypes": ["script", "image"]
  }
}
```

DNR has rule-count limits (currently 30k static + 30k dynamic in Chrome). uBlock Origin Lite hit these limits — it lost some power vs full uBlock Origin. Plan around the limits or pick a different feature.

### 3. Remote code execution forbidden

You can't `eval`, can't load remote `<script>` tags into your own pages, can't dynamically import code from your server. Your extension must ship its full logic in the package submitted to the Store.

This kills entire categories of extensions: live A/B testing of code, server-pushed feature flags that change executable code, runtime-loaded plugin systems.

Workaround: ship multiple "modes" inside the bundle, switch between them by config, A/B test the **config**, not the code.

### 4. Host permissions are reviewed harder

`<all_urls>` will get extra Web Store scrutiny and slower review. Justify it concretely or scope down:

```json
// Bad — instant red flag
"host_permissions": ["<all_urls>"]

// Better — narrow to the use case
"host_permissions": [
  "https://*.github.com/*",
  "https://*.gitlab.com/*"
]

// Best — use optional_host_permissions, request at runtime
"optional_host_permissions": ["<all_urls>"]
```

## Architecture — the three worlds

```
┌─────────────────────┐  ┌─────────────────────┐  ┌─────────────────────┐
│  Extension page     │  │  Service worker     │  │  Content script     │
│  (popup, options,   │  │  (event handlers,   │  │  (runs in page,     │
│   newtab)           │  │   alarms, storage)  │  │   isolated world)   │
└──────────┬──────────┘  └──────────┬──────────┘  └──────────┬──────────┘
           │                        │                        │
           └────────────────────────┴────────────────────────┘
                  chrome.runtime.sendMessage / onMessage
                  chrome.storage (shared state)
                                    │
                          ┌─────────┴─────────┐
                          │   Page DOM        │
                          │   (postMessage    │
                          │    via window     │
                          │    if needed)     │
                          └───────────────────┘
```

**Rule**: content scripts CAN read/write the page DOM but CANNOT read the page's JS variables (isolated world). To talk to page JS, inject a `<script>` into the page and exchange via `window.postMessage`.

**Anti-pattern**: putting business logic in the content script. Content scripts should be thin — read DOM, send to service worker, receive response, update DOM. Service worker holds the logic.

## Storage — pick the right one

| Storage | Quota | Synced across devices | Use for |
|---------|-------|----------------------|---------|
| `chrome.storage.local` | 10 MB (or 100 MB unlimitedStorage perm) | No | App state, cache, large data |
| `chrome.storage.sync` | 100 KB total, 8 KB per item | Yes (across user's signed-in Chrome) | User preferences |
| `chrome.storage.session` | 10 MB | No, cleared on browser close | Tab-scoped temp data |
| IndexedDB (page context) | Browser quota | No | Big data structures, queries |
| `localStorage` (page context) | 5-10 MB | No | Avoid in extensions — race conditions |

**Don't use `localStorage`** in service workers — it doesn't exist. Use `chrome.storage` everywhere.

## Cross-browser compatibility

Targets in 2026:

| Browser | Manifest | Notes |
|---------|----------|-------|
| **Chrome / Edge / Opera / Brave** (Chromium) | MV3 only | Single codebase works. Edge has its own Add-ons store with own review. |
| **Firefox** | MV2 + MV3 (MV3 GA since Oct 2023) | Slight API differences (`browser.*` namespace, returns Promise natively). Use `webextension-polyfill`. |
| **Safari** | MV2 + MV3 | Apple's "Safari Web Extensions" — must be wrapped in a native macOS/iOS app via Xcode. App Store review (~7d). |

**Use `webextension-polyfill`** for portable code across Chromium + Firefox. Safari requires a native wrapper either way.

```js
// portable.js
import browser from 'webextension-polyfill';

browser.tabs.query({ active: true }).then(tabs => {
  // works in Chrome (callback API wrapped to Promise) AND Firefox (native Promise)
});
```

**Pick your battles**: most new extensions ship Chromium only, add Firefox at month 3-6, Safari only if iOS demand justifies the native wrapper effort. Edge gets Chromium build for free.

## Web Store review pre-flight

The Chrome Web Store rejects extensions for predictable reasons. Run this checklist before every submit:

### Single-purpose policy

Chrome Web Store policy: **one core function per extension**. Bundling unrelated features = rejection.

```
Bad:    "Productivity Suite" — todos, calendar, weather, tab manager, color picker
Good:   "Tab Manager" — only tab management, separate extension for color picker
```

If your extension does 5 things, split it into 5.

### Permissions justified

Every permission you request needs a clear "why" in the listing description AND in the in-store privacy disclosure. Reviewers will reject if:

- `<all_urls>` host permission without justification
- `tabs` permission for an extension that doesn't visibly need tab data
- `cookies` permission for non-cookie features
- `webRequest` (read-only in MV3) for "tracking" features

### Privacy practices form

Filed in Web Store dashboard. You declare:
- What user data you collect
- How you use it
- Whether you sell it (almost always: no)
- Whether you share with third parties
- Whether you use it for ads, analytics, or core function

**Lying = removal + ban**. Be honest.

### Promotional content

- Screenshots: 1280×800 PNG, 4-5 of them, no excessive marketing copy on the screenshot
- Promo image: 440×280 small tile + 920×680 large promo
- Description: 132 char short + long description with feature list; no "best ever", no calls to "rate 5 stars"

### Testing tip — review on a clean profile

Always test your final build in a fresh Chrome profile (or Chrome Beta) before submission. Many bugs only show up without an existing logged-in session.

```bash
# Run a clean Chrome profile for testing
google-chrome --user-data-dir=/tmp/clean-profile-$(date +%s) \
  --load-extension=/path/to/your/extension/dist
```

## Build pipeline

| Stack | Tools |
|-------|-------|
| Vanilla JS / TypeScript | esbuild + manual `manifest.json` |
| React / Vue / Svelte | **WXT** (recommended), Plasmo, vite-plugin-web-extension |
| Standard quality | eslint with `eslint-plugin-chrome-extension` rules |

**WXT** (https://wxt.dev) is the strongest choice for new projects in 2026. Auto-imports, file-based extension structure, cross-browser builds with one command, MV3 + MV2 support.

```bash
# package.json scripts with WXT
{
  "scripts": {
    "dev": "wxt",
    "dev:firefox": "wxt -b firefox",
    "build": "wxt build",
    "build:firefox": "wxt build -b firefox",
    "build:safari": "wxt build -b safari",
    "submit": "wxt submit --chrome-zip dist/chrome.zip --firefox-zip dist/firefox.zip"
  }
}
```

`wxt submit` uploads to all stores in parallel.

## OWASP MASVS — extension equivalent

The OWASP Top 10 Browser Extensions (2024) covers the threat model:

| ID | Risk | Check |
|----|------|-------|
| BE01 | Cross-site scripting via content script | Never insert untrusted strings into DOM with `innerHTML`; use `textContent` or DOMPurify |
| BE02 | Insecure messaging between worlds | Validate all messages have expected shape; never trust `sender` blindly |
| BE03 | Sensitive data in storage | Don't store API keys / tokens in `chrome.storage` unencrypted; offload to background OAuth flow |
| BE04 | Excessive permissions | Use `optional_permissions`, request at runtime; minimise `host_permissions` |
| BE05 | Phishing via popup or new tab | Don't open external auth in popup — use `chrome.identity.launchWebAuthFlow` |
| BE06 | Injected page content trust | Treat data from `window.postMessage` as untrusted; same-origin check |
| BE07 | Unmaintained dependencies | Audit `package.json` regularly; pin versions; remove unused deps |
| BE08 | Update mechanism trust | Web Store handles updates; never bypass with custom mechanism |
| BE09 | CSP bypass attempts | Never `'unsafe-eval'` in CSP; never `eval()` user input |
| BE10 | Telemetry without consent | Opt-in only; document data collected; comply with GDPR if applicable |

`security-officer` runs this checklist when `archetype: browser-extension`.

## Performance — the 50ms rule

Extensions that slow down the browser get bad reviews fast.

- **Service worker startup**: must complete handler in < 50ms. If you need 500ms of init, do it lazily.
- **Content script injection**: avoid `run_at: document_start` unless absolutely required (it blocks page render)
- **Bundle size**: aim for content script < 100 KB, service worker < 250 KB. Lazy-load everything else.
- **Memory**: service worker can be killed if memory pressure; design for restart.
- **CPU**: don't poll. Use `chrome.alarms` (minimum interval: 30s in MV3).

Profile with: `chrome://extensions` → click "service worker" → DevTools → Performance tab.

## Long-running work — `chrome.offscreen` and the 50ms ceiling

The 50ms rule is for the SW message handler — it tells you "return fast." It does **not** mean the actual work must finish in 50ms. For anything that takes longer (LLM inference, image processing, audio analysis, heavy DOM work), the SW must offload the work and respond asynchronously, otherwise the SW gets killed mid-operation.

**Decision table:**

| Work duration | Where it runs | Pattern |
|---------------|---------------|---------|
| < 50 ms | Service worker | inline `chrome.runtime.onMessage` handler |
| 50 ms – 5 s, no DOM | Service worker, async | start work, return ack immediately, post result via `chrome.runtime.sendMessage` to UI |
| 50 ms – 5 s, needs DOM/audio/canvas | **Offscreen document** | `chrome.offscreen.createDocument()` — DOM access without a visible page |
| > 5 s, network-bound | Backend (your server) | extension is thin client; no SW process holds the wait |
| > 5 s, on-device (e.g. WASM model) | Offscreen + chunked progress | break work into chunks, post progress, allow user to cancel |

**Offscreen document quickstart** (for DOM-required work in MV3):

```js
// service worker
async function ensureOffscreen() {
  const has = await chrome.offscreen.hasDocument();
  if (has) return;
  await chrome.offscreen.createDocument({
    url: 'offscreen.html',
    reasons: ['DOM_PARSER'],         // or AUDIO_PLAYBACK, BLOBS, USER_MEDIA, IFRAME_SCRIPTING
    justification: 'parse HTML for content extraction'
  });
}
```

**LLM inference / remote model calls** — the common case (extensions wrapping an AI API):
- SW handler: dedupe → cache lookup → if miss, kick off `fetch` to backend → return ack to content script
- Backend, **never the extension**, holds API keys (extension storage is unencrypted; pack BE03)
- Stream results back via `chrome.runtime.sendMessage` or `chrome.tabs.sendMessage`
- Show progressive UI in sidebar/popup; do **not** block on the full response

## Sidebar / iframe injection (Grammarly / Honey pattern)

Many extensions need a persistent overlay UI on top of arbitrary pages. Two options:

| Approach | When to use | Caveats |
|----------|-------------|---------|
| **Side Panel API** (`chrome.sidePanel`, MV3) | Browser-managed sidebar, opens on user gesture | Chrome 114+, no Firefox parity (use `browser.sidebarAction` there) |
| **Injected iframe** (content script appends `<iframe>`) | You need full overlay control or work pre-Chrome-114 | **Must isolate** — iframe `src` must be `chrome-extension://<id>/sidebar.html`, never `data:` or inline HTML |

**Iframe isolation rules:**
- Use `chrome-extension://` URL — gives you your own CSP, immune to host page styles/scripts
- Communicate with content script via `window.postMessage` with origin check, **not** via `chrome.runtime` from inside the iframe (it works, but origin checks are clearer)
- Set `iframe.style.all = 'initial'` to prevent host-page CSS bleed
- Z-index conflicts: pick something insane (`2147483647`) and document it

## Cross-pack stacking — when to load more than one pack

Browser extensions often stack on another archetype's concerns. Set `packs:` in PROJECT.md to load both:

| Extension does | Stack | Why |
|----------------|-------|-----|
| Wraps an LLM / runs ML inference | `[browser-extension-pack, ai-pack]` | hallucination, prompt-injection-via-page-content, cost cap, eval suite |
| Talks to your own SaaS backend | `[browser-extension-pack, web-pack]` | API contract, auth flow, idempotency |
| Crypto wallet / signs transactions | `[browser-extension-pack, web3-pack]` | key storage, signing UX, phishing resistance |
| Touches payment forms (price comparison, autofill) | `[browser-extension-pack, commerce-pack]` | PCI surface, never read full PAN |

**Prompt-injection-via-page-content** is the most-missed risk in AI extensions: a malicious page can embed instructions in DOM that the extension scrapes and feeds to the LLM. Always treat scraped page text as untrusted; sanitize and box it before model context.

## Compliance defaults for `browser-extension`

| Trigger | Add to compliance |
|---------|-------------------|
| Always | `web-store-policy`, `mv3-security`, `csp` |
| Reads user data | `gdpr` if EU users, `ccpa` if California |
| Stores credentials | `host-permissions-audit` (justify every URL pattern) |
| Cookie reading | `cookie-disclosure` (declare in privacy practices form) |
| Children-targeting | `coppa` (US, under 13) — extra Web Store review |
| Crypto / Web3 | additional vetting; some browsers ban or restrict |

## Anti-patterns specific to `browser-extension`

| Pattern | Why it fails | Fix |
|---------|-------------|-----|
| Hardcoded API keys in extension bundle | Trivially extracted by anyone | Server-side proxy, OAuth flow |
| `<all_urls>` "just in case" | Slow review, distrust | Scope to specific origins; use `optional_host_permissions` |
| Heavy logic in content script | Slows every page | Logic in service worker, content script is a thin DOM glue |
| `setTimeout` to "wake up" service worker | MV3 will terminate it anyway | Use `chrome.alarms` (min 30s) for periodic work |
| Persistent state in service worker memory | Lost on every restart | All state in `chrome.storage` |
| Custom auto-update mechanism | Banned + ejection | Trust the Web Store; pre-stage previous build for emergency rollback |
| Submitting bundle with source maps | Reveals internal structure to competitors / attackers | Strip source maps from production build |
| Skipping Firefox / Safari "to ship faster" | Lock in to Chromium = leverage to Google Web Store | Ship MV3 cross-browser from day 1 with WXT |
| Ignoring "Single-purpose" policy | Rejection at submit | One extension = one core feature |

## QA extras provided by this pack

When `archetype: browser-extension`, `qa-engineer` automatically runs:

- **MV3 service worker lifecycle test** — kill SW, verify recovery from `chrome.storage`
- **Content script isolation test** — confirm content script cannot leak into page JS
- **Cross-browser smoke test** — load extension in Chrome, Firefox, Safari (if Safari target), verify popup + main flow
- **Web Store policy pre-flight** — single-purpose check, permissions justified, privacy practices form filled
- **Bundle size diff** vs main branch (fail if > 10% increase or > 250 KB SW)
- **OWASP BE Top 10** checklist
- **`<all_urls>` red-flag scan** — fail if added without explicit justification comment

## Recommended `PROJECT.md` for new browser-extension project

```yaml
primary: chrome-extension-mv3
archetype: browser-extension
project_size: small
stack: [typescript, wxt, react]
team-size: 2
compliance: [web-store-policy, mv3-security, gdpr, csp]
qa-extras: [mv3-lifecycle, cross-browser-smoke, web-store-preflight, bundle-size]
performance-sla: service-worker-startup < 50ms, content-script-bundle < 100KB
packs: [browser-extension-pack]
```

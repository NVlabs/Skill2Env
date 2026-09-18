---
name: chatgpt-search
description: |
  Search ChatGPT and extract the full response + hydration JSON that powers the UI.
  Attaches to a running Chrome instance (port 9222 by default), opens ChatGPT,
  submits a query, waits for the streamed response, and returns structured data:
  messages, product cards, hydration JSON, and API calls.
  Use when asked to "search chatgpt", "ask chatgpt", "chatgpt search",
  "get chatgpt response", or "scrape chatgpt".
allowed-tools: Browser,Bash,Read,Write,Glob,Grep
---

# ChatGPT Search — Extract structured response + hydration JSON

## Prerequisites

A Chrome instance must be running with `--remote-debugging-port=9222`.
If not running, launch it:

```bash
# Kill existing Chrome first
pkill -9 -f "Google Chrome" 2>/dev/null; sleep 2

# Launch with debug port + user's real profile copy
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --remote-debugging-port=9222 \
  --user-data-dir="$HOME/.claude/browser-profiles/chrome-debug-full" \
  --no-first-run &>/dev/null &
```

If the profile doesn't exist yet, create it by copying the user's real Chrome profile:
```bash
REAL="$HOME/Library/Application Support/Google/Chrome"
COPY="$HOME/.claude/browser-profiles/chrome-debug-full"
mkdir -p "$COPY"
cp "$REAL/Local State" "$COPY/" 2>/dev/null
cp -R "$REAL/Default" "$COPY/Default" 2>/dev/null
rm -rf "$COPY/Default/Cache" "$COPY/Default/Code Cache" 2>/dev/null
```

## Workflow

The user provides a search query. Execute these steps:

### Step 1: Verify Chrome is running with debug port

```bash
curl -s http://127.0.0.1:9222/json/version | head -1
```

If it fails, launch Chrome as described in Prerequisites.

### Step 2: Attach + enable network log + open ChatGPT

```
Browser { action: "new_session", session_id: "chatgpt", cdp_url: "http://127.0.0.1:9222" }
Browser { action: "enable_network_log", session_id: "chatgpt" }
Browser { action: "new_tab", url: "https://chatgpt.com", session_id: "chatgpt" }
```

Wait 5 seconds for page load.

### Step 3: Inject fetch/SSE interceptor

```
Browser { action: "evaluate", session_id: "chatgpt", value: "window.__sse=[];window.__api=[];const _f=window.fetch;window.fetch=async function(...a){const url=typeof a[0]==='string'?a[0]:a[0]?.url||'?';const m=a[1]?.method||'GET';const rb=a[1]?.body;const resp=await _f.apply(this,a);const ct=resp.headers.get('content-type')||'';const cl=resp.clone();if(ct.includes('event-stream')){const rd=cl.body.getReader();const dc=new TextDecoder();let full='';(async()=>{try{while(true){const{done,value:v}=await rd.read();if(done)break;full+=dc.decode(v,{stream:true});}}catch{}window.__sse.push({url,m,s:resp.status,sz:full.length,body:full,ts:Date.now()});})();}else{cl.text().then(t=>{if(t.length>30)window.__api.push({url,m,s:resp.status,sz:t.length,body:t,ts:Date.now()});}).catch(()=>{});}return resp;};'ok'" }
```

### Step 4: Type query + submit

Use real CDP key events for React compatibility:

```
Browser { action: "click", selector: "#prompt-textarea, textarea", session_id: "chatgpt" }
```

Then type each character of the query using `send_keys` — but for long queries, use `evaluate` with the native setter:

```
Browser { action: "evaluate", session_id: "chatgpt", value: "Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype,'value').set.call(document.querySelector('#prompt-textarea,textarea'),'THE QUERY HERE');document.querySelector('#prompt-textarea,textarea').dispatchEvent(new Event('input',{bubbles:true}));'typed'" }
```

Wait 800ms, then submit:

```
Browser { action: "evaluate", session_id: "chatgpt", value: "(function(){var btn=document.querySelector('[data-testid=\"send-button\"],button[aria-label*=\"Envoyer\"],button[aria-label*=\"Send\"]');if(btn&&!btn.disabled){btn.click();return 'sent';}var btns=[...document.querySelectorAll('button')];var s=btns.find(function(b){return b.querySelector('svg')&&!b.disabled&&b.closest('[class*=\"composer\"]');});if(s){s.click();return 'sent-svg';}return 'no-btn';})()" }
```

### Step 5: Wait for response

Poll every 5 seconds for up to 60 seconds, checking message count:

```
Browser { action: "evaluate", session_id: "chatgpt", value: "document.querySelectorAll('[data-message-author-role]').length" }
```

Stop when message count >= 2 (user + assistant).

### Step 6: Extract results

**Messages (user + assistant full text):**
```
Browser { action: "evaluate", session_id: "chatgpt", value: "(function(){var msgs=document.querySelectorAll('[data-message-author-role]');var r=[];msgs.forEach(function(m){r.push({role:m.getAttribute('data-message-author-role'),text:m.textContent.trim()})});return JSON.stringify(r);})()" }
```

**Hydration JSON (session, config, feature flags):**
```
Browser { action: "evaluate", session_id: "chatgpt", value: "var e=document.querySelector('script[type=\"application/json\"]');e?e.textContent:''" }
```

**Intercepted SSE streams (conversation stream + search product updates):**
```
Browser { action: "evaluate", session_id: "chatgpt", value: "JSON.stringify((window.__sse||[]).map(function(s){return{url:s.url,method:s.m,status:s.s,size:s.sz}}))" }
```

To get a specific SSE body (e.g., index 0):
```
Browser { action: "evaluate", session_id: "chatgpt", value: "(window.__sse||[])[0]?.body||''" }
```

**Intercepted API calls:**
```
Browser { action: "evaluate", session_id: "chatgpt", value: "JSON.stringify((window.__api||[]).filter(function(a){return a.url.includes('backend')}).map(function(a){return{url:a.url,method:a.m,status:a.s,size:a.sz}}))" }
```

**CDP network log (all HTTP requests/responses):**
```
Browser { action: "get_network_log", session_id: "chatgpt", filter: "backend" }
```

### Step 7: Save to /tmp

Save all extracted data to `/tmp/chatgpt-search-*.json`:
- `/tmp/chatgpt-search-messages.json` — user + assistant messages
- `/tmp/chatgpt-search-hydration.json` — UI hydration JSON
- `/tmp/chatgpt-search-sse.json` — SSE stream data (if captured)
- `/tmp/chatgpt-search-api.json` — API call responses

### Step 8: Report

Present the assistant's response to the user, and list saved files with sizes.

## Output format

```
## ChatGPT Search: [query]

### Response
[Full assistant message text]

### Files saved
- /tmp/chatgpt-search-messages.json (X KB) — conversation messages
- /tmp/chatgpt-search-hydration.json (X KB) — UI hydration data
- /tmp/chatgpt-search-sse.json (X KB) — SSE streams
- /tmp/chatgpt-search-api.json (X KB) — API responses

### Metadata
- Model: [from hydration or conversation init]
- Session ID: [from hydration]
- Country: [from hydration]
```

## Important notes

- ChatGPT works without login for basic queries (anonymous mode)
- For authenticated queries, the user must log in manually in the debug Chrome
- The fetch interceptor captures SSE streams (conversation + search/product_update)
- CDP network log captures JSON API calls but NOT SSE stream bodies
- Always close the session when done: `Browser { action: "close_session", session_id: "chatgpt" }`

#!/usr/bin/env node
// chatgpt-search — Search ChatGPT and extract response + hydration JSON
//
// Usage:
//   node search.mjs "best crossbody fashion luxury bag"
//   node search.mjs --port 9333 "query here"
//   node search.mjs --launch "query here"       # auto-launch Chrome
//   node search.mjs --json "query here"          # output JSON only
//
// Requires Chrome running with --remote-debugging-port (default 9222)

import fs from "node:fs";
import path from "node:path";
import os from "node:os";
import http from "node:http";
import https from "node:https";
import { spawn } from "node:child_process";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// ── Args ────────────────────────────────────────────────────────

const args = process.argv.slice(2);
let port = 9222;
let query = "";
let autoLaunch = false;
let jsonOnly = false;
let timeout = 60000;

for (let i = 0; i < args.length; i++) {
  if (args[i] === "--port" && args[i + 1]) { port = parseInt(args[i + 1]); i++; }
  else if (args[i] === "--launch") autoLaunch = true;
  else if (args[i] === "--json") jsonOnly = true;
  else if (args[i] === "--timeout" && args[i + 1]) { timeout = parseInt(args[i + 1]); i++; }
  else if (!args[i].startsWith("--")) query = args[i];
}

if (!query) {
  console.error("Usage: node search.mjs [--port 9222] [--launch] [--json] [--timeout 60000] \"query\"");
  process.exit(2);
}

// ── HTTP helper ─────────────────────────────────────────────────

function httpGet(url) {
  return new Promise((resolve, reject) => {
    const mod = url.startsWith("https") ? https : http;
    mod.get(url, { headers: { "User-Agent": "cloclo/1.0" } }, (res) => {
      if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) return httpGet(res.headers.location).then(resolve, reject);
      if (res.statusCode >= 400) { res.resume(); return reject(new Error(`HTTP ${res.statusCode}`)); }
      let data = ""; res.on("data", (c) => data += c); res.on("end", () => resolve(data)); res.on("error", reject);
    }).on("error", reject);
  });
}

// ── Load BrowserSession from claude-native.mjs ──────────────────

function loadBrowserSession() {
  const candidates = [
    path.join(__dirname, "..", "..", "..", "claude-native.mjs"),
    path.join(__dirname, "..", "..", "claude-native.mjs"),
    path.join(process.cwd(), "claude-native.mjs"),
  ];
  let src = null;
  for (const p of candidates) {
    if (fs.existsSync(p)) { src = fs.readFileSync(p, "utf-8"); break; }
  }
  if (!src) throw new Error("claude-native.mjs not found. Run from the project directory.");

  const startIdx = src.indexOf("// ── Browser Tool Pack");
  const endIdx = src.indexOf("// ── SecurityClassifier");
  if (startIdx === -1 || endIdx === -1) throw new Error("Browser Tool Pack not found in claude-native.mjs");

  const fn = new Function("spawn", "fs", "path", "os", "_http", "_https", "_httpGet",
    src.slice(startIdx, endIdx) + ";return { BrowserSession };");
  return fn(spawn, fs, path, os, http, https, httpGet).BrowserSession;
}

// ── Chrome launcher ─────────────────────────────────────────────

async function ensureChrome(debugPort) {
  // Check if Chrome is already running with debug port
  try {
    const resp = await httpGet(`http://127.0.0.1:${debugPort}/json/version`);
    JSON.parse(resp);
    return; // already running
  } catch { /* not running */ }

  if (!autoLaunch) {
    console.error(`Chrome not running on port ${debugPort}. Use --launch to auto-start, or run:`);
    console.error(`  pkill -9 -f "Google Chrome"; sleep 2`);
    console.error(`  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --remote-debugging-port=${debugPort} --user-data-dir="$HOME/.claude/browser-profiles/chrome-debug-full" --no-first-run &`);
    process.exit(3);
  }

  // Launch Chrome
  const profileDir = path.join(os.homedir(), ".claude", "browser-profiles", "chrome-debug-full");

  // If profile doesn't exist, copy from real Chrome
  if (!fs.existsSync(path.join(profileDir, "Default"))) {
    const realProfile = path.join(os.homedir(), "Library", "Application Support", "Google", "Chrome");
    if (fs.existsSync(path.join(realProfile, "Default"))) {
      if (!jsonOnly) console.error("Copying Chrome profile (first time)...");
      fs.mkdirSync(profileDir, { recursive: true });
      fs.cpSync(path.join(realProfile, "Local State"), path.join(profileDir, "Local State"), { force: true });
      fs.cpSync(path.join(realProfile, "Default"), path.join(profileDir, "Default"), { recursive: true, force: true });
      // Remove caches
      for (const d of ["Cache", "Code Cache", "Service Worker/CacheStorage"]) {
        fs.rmSync(path.join(profileDir, "Default", d), { recursive: true, force: true });
      }
    } else {
      fs.mkdirSync(profileDir, { recursive: true });
    }
  }

  const chromePaths = [
    process.env.CHROME_PATH,
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/opt/homebrew/bin/chromium",
    "/usr/bin/google-chrome-stable",
    "/usr/bin/chromium",
  ].filter(Boolean);

  let chromeBin = null;
  for (const p of chromePaths) { if (fs.existsSync(p)) { chromeBin = p; break; } }
  if (!chromeBin) { console.error("Chrome/Chromium not found"); process.exit(3); }

  if (!jsonOnly) console.error("Launching Chrome...");
  const child = spawn(chromeBin, [
    `--remote-debugging-port=${debugPort}`,
    `--user-data-dir=${profileDir}`,
    "--no-first-run",
  ], { stdio: "ignore", detached: true });
  child.unref();

  // Wait for Chrome to be ready
  for (let i = 0; i < 30; i++) {
    await new Promise(r => setTimeout(r, 500));
    try { const resp = await httpGet(`http://127.0.0.1:${debugPort}/json/version`); JSON.parse(resp); return; } catch { /* not ready */ }
  }
  console.error("Chrome failed to start"); process.exit(3);
}

// ── Main ────────────────────────────────────────────────────────

async function main() {
  const BrowserSession = loadBrowserSession();
  await ensureChrome(port);

  const b = new BrowserSession("chatgpt-search", { cdpUrl: `http://127.0.0.1:${port}` });

  try {
    if (!jsonOnly) console.error("Attaching to Chrome...");
    await b.ensureBrowser();
    await b.enableNetworkLog();

    // Open ChatGPT
    if (!jsonOnly) console.error("Opening ChatGPT...");
    await b.newTab("https://chatgpt.com");
    await new Promise(r => setTimeout(r, 5000));

    // Inject fetch/SSE interceptor
    await b.evaluate(`
      window.__sse=[];window.__api=[];
      const _f=window.fetch;
      window.fetch=async function(...a){
        const url=typeof a[0]==='string'?a[0]:a[0]?.url||'?';
        const m=a[1]?.method||'GET';
        const rb=a[1]?.body;
        const resp=await _f.apply(this,a);
        const ct=resp.headers.get('content-type')||'';
        const cl=resp.clone();
        if(ct.includes('event-stream')){
          const rd=cl.body.getReader();const dc=new TextDecoder();let full='';
          (async()=>{try{while(true){const{done,value:v}=await rd.read();if(done)break;full+=dc.decode(v,{stream:true});}}catch{}
          window.__sse.push({url,m,s:resp.status,sz:full.length,body:full,ts:Date.now()});})();
        }else{
          cl.text().then(t=>{if(t.length>30)window.__api.push({url,m,s:resp.status,sz:t.length,body:t,ts:Date.now()});}).catch(()=>{});
        }
        return resp;
      };'ok'
    `);

    // Type query — ChatGPT uses ProseMirror contenteditable, not textarea
    // Must use real CDP key events for React/ProseMirror to register input
    if (!jsonOnly) console.error(`Searching: "${query}"`);

    // Focus the input (ProseMirror div or fallback textarea)
    await b.click("#prompt-textarea, [contenteditable='true'], textarea");
    await new Promise(r => setTimeout(r, 300));

    // Type each character via CDP Input.dispatchKeyEvent
    const sid = b._activeCdpSession();
    for (const c of query) {
      await b._send("Input.dispatchKeyEvent", { type: "keyDown", text: c, key: c }, sid);
      await b._send("Input.dispatchKeyEvent", { type: "keyUp", key: c }, sid);
    }
    await new Promise(r => setTimeout(r, 800));

    // Click the send button
    await b.evaluate(`
      (function(){
        var btn=document.querySelector('[data-testid="send-button"],button[aria-label*="Envoyer"],button[aria-label*="Send"]');
        if(btn&&!btn.disabled){btn.click();return 'sent';}
        var btns=[...document.querySelectorAll('button')];
        var s=btns.find(function(b){return b.querySelector('svg')&&!b.disabled&&b.closest('[class*="composer"]');});
        if(s){s.click();return 'sent-svg';}
        return 'no-btn';
      })()
    `);

    // Wait for response
    if (!jsonOnly) console.error("Waiting for response...");
    const startTime = Date.now();
    let msgCount = 0;
    while (Date.now() - startTime < timeout) {
      await new Promise(r => setTimeout(r, 3000));
      const count = await b.evaluate("document.querySelectorAll('[data-message-author-role]').length");
      msgCount = parseInt(count) || 0;
      if (!jsonOnly) process.stderr.write(`  ${Math.round((Date.now() - startTime) / 1000)}s msgs=${msgCount}\r`);
      if (msgCount >= 2) {
        // Wait a bit more for streaming to finish
        await new Promise(r => setTimeout(r, 3000));
        break;
      }
    }
    if (!jsonOnly) console.error("");

    if (msgCount < 2) {
      console.error("Timeout: ChatGPT did not respond within " + (timeout / 1000) + "s");
      await b.close();
      process.exit(5);
    }

    // ── Extract everything ──────────────────────────────────────

    // Messages
    const messagesRaw = await b.evaluate(`
      (function(){
        var msgs=document.querySelectorAll('[data-message-author-role]');
        var r=[];
        msgs.forEach(function(m){
          r.push({role:m.getAttribute('data-message-author-role'),text:m.textContent.trim()});
        });
        return JSON.stringify(r);
      })()
    `);
    const messages = JSON.parse(messagesRaw);

    // Hydration JSON
    const hydrationRaw = await b.evaluate(`
      var e=document.querySelector('script[type="application/json"]');e?e.textContent:'{}'
    `);
    let hydration = {};
    try { hydration = JSON.parse(hydrationRaw); } catch { hydration = { raw: hydrationRaw }; }

    // SSE captures
    const sseRaw = await b.evaluate("JSON.stringify(window.__sse||[])");
    const sseList = JSON.parse(sseRaw);

    // API captures
    const apiRaw = await b.evaluate("JSON.stringify((window.__api||[]).filter(function(a){return a.url.includes('backend')}))");
    const apiList = JSON.parse(apiRaw);

    // CDP network log (backend calls)
    const cdpLog = JSON.parse(b.getNetworkLog("backend"));

    // ── Build result ────────────────────────────────────────────

    const result = {
      query,
      messages,
      hydration: {
        sessionId: hydration.sessionId,
        locale: hydration.locale,
        userCountry: hydration.userCountry,
        userCity: hydration.cfIpCity,
        cluster: hydration.cluster,
        authStatus: hydration.authStatus,
        isNoAuthEnabled: hydration.isNoAuthEnabled,
      },
      sse: sseList.map(s => ({ url: s.url, method: s.m, status: s.s, size: s.sz })),
      api: apiList.map(a => ({ url: a.url, method: a.m, status: a.s, size: a.sz })),
      cdpNetworkLog: cdpLog,
      timestamp: new Date().toISOString(),
    };

    // ── Save files ──────────────────────────────────────────────

    const outDir = "/tmp";
    fs.writeFileSync(path.join(outDir, "chatgpt-search-messages.json"), JSON.stringify(messages, null, 2));
    fs.writeFileSync(path.join(outDir, "chatgpt-search-hydration.json"), hydrationRaw);
    fs.writeFileSync(path.join(outDir, "chatgpt-search-sse.json"), sseRaw);
    fs.writeFileSync(path.join(outDir, "chatgpt-search-api.json"), apiRaw);
    fs.writeFileSync(path.join(outDir, "chatgpt-search-result.json"), JSON.stringify(result, null, 2));

    // Save individual SSE bodies
    for (let i = 0; i < sseList.length; i++) {
      fs.writeFileSync(path.join(outDir, `chatgpt-search-sse-${i}.txt`), sseList[i].body || "");
    }

    // ── Output ──────────────────────────────────────────────────

    if (jsonOnly) {
      process.stdout.write(JSON.stringify(result, null, 2));
    } else {
      console.log("\n" + "=".repeat(60));
      console.log(`ChatGPT Search: "${query}"`);
      console.log("=".repeat(60));

      for (const m of messages) {
        console.log(`\n[${m.role}]`);
        console.log(m.text);
      }

      console.log("\n" + "-".repeat(60));
      console.log("Files saved:");
      for (const f of ["messages", "hydration", "sse", "api", "result"]) {
        const fp = path.join(outDir, `chatgpt-search-${f}.json`);
        if (fs.existsSync(fp)) {
          console.log(`  ${fp} (${(fs.statSync(fp).size / 1024).toFixed(1)} KB)`);
        }
      }
      for (let i = 0; i < sseList.length; i++) {
        const fp = path.join(outDir, `chatgpt-search-sse-${i}.txt`);
        console.log(`  ${fp} (${(fs.statSync(fp).size / 1024).toFixed(1)} KB)`);
      }

      console.log("\nMetadata:");
      console.log(`  Session: ${hydration.sessionId || "unknown"}`);
      console.log(`  Country: ${hydration.userCountry || "unknown"} (${hydration.cfIpCity || "unknown"})`);
      console.log(`  Auth: ${hydration.authStatus || "unknown"}`);
      console.log(`  SSE streams: ${sseList.length}`);
      console.log(`  API calls: ${apiList.length}`);
      console.log(`  CDP requests: ${cdpLog.length}`);
    }

    // Close tab but keep Chrome running
    await b.close();

  } catch (e) {
    console.error("Error:", e.message);
    try { await b.close(); } catch {}
    process.exit(1);
  }
}

main();

# HTML Report Template Reference

This file contains the complete structure, CSS, JavaScript, and variable substitution
rules for generating the audit report HTML.

**Read this file entirely before writing any HTML.**

---

## Table of Contents

1. [Design System & CSS Variables](#1-design-system--css-variables)
2. [Full HTML Shell](#2-full-html-shell)
3. [Header Section](#3-header-section)
4. [Legend Bar](#4-legend-bar)
5. [Sidebar](#5-sidebar)
6. [Scorecard Table](#6-scorecard-table)
7. [Site-Wide Pattern Box](#7-site-wide-pattern-box)
8. [Top Issues Section](#8-top-issues-section)
9. [Section Layout (per category)](#9-section-layout-per-category)
10. [Endpoint Card — Detailed](#10-endpoint-card--detailed)
11. [Compact Group Table](#11-compact-group-table)
12. [JavaScript](#12-javascript)
13. [Variable Substitution Map](#13-variable-substitution-map)
14. [Section Rendering Decision Rules](#14-section-rendering-decision-rules)

---

## 1. Design System & CSS Variables

```css
:root {
  --bg: #06060a;
  --surface: #0e0e16;
  --surface2: #14141f;
  --border: #232336;
  --border2: #2e2e4a;
  --text: #e2e2f0;
  --text2: #8888aa;
  --text3: #4a4a6a;
  --pass: #34d399;       --pass-bg: #052015;   --pass-border: #064824;
  --warn: #fbbf24;       --warn-bg: #201500;   --warn-border: #4a3300;
  --fail: #f87171;       --fail-bg: #200808;   --fail-border: #4a1212;
  --accent: #a78bfa;     --accent2: #c4b5fd;   --accent-bg: #12093a;
  --tag-bg: #141424;
}
```

**Typography:** `'Space Grotesk', sans-serif` for body, `'Space Mono', monospace` for
code, labels, and numbers. Load both from Google Fonts.

**Badge classes:**
```html
<span class="badge pass">✓ PASS</span>
<span class="badge warn">⚠ WARN</span>
<span class="badge fail">✕ FAIL</span>
```

**Status dots (5 dots per endpoint, one per check):**
```html
<span class="dot pass"></span>
<span class="dot warn"></span>
<span class="dot fail"></span>
```

---

## 2. Full HTML Shell

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{SITE_NAME}} API Docs Audit Report</title>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>
  /* PASTE FULL CSS HERE — see sections below */
</style>
</head>
<body>
  {{HEADER}}
  {{LEGEND_BAR}}
  <div class="main">
    {{SIDEBAR}}
    <div class="content">
      {{SCORECARD_SECTION}}
      {{PATTERN_BOX}}
      {{TOP_ISSUES_SECTION}}
      <hr class="divider">
      {{ALL_CATEGORY_SECTIONS}}
    </div>
  </div>
  <script>{{JAVASCRIPT}}</script>
</body>
</html>
```

---

## 3. Header Section

```html
<div class="header">
  <div class="eyebrow">API Documentation Audit</div>
  <h1>{{SITE_NAME}} API Docs</h1>
  <div class="header-url">{{DOCS_URL}}</div>
  <div class="stats-row">
    <div class="stat-cell">
      <span class="sv sv-total">{{TOTAL_ENDPOINTS}}</span>
      <span class="slabel">Endpoints</span>
    </div>
    <div class="stat-cell">
      <span class="sv sv-pass">{{TOTAL_PASS}}</span>
      <span class="slabel">Pass</span>
    </div>
    <div class="stat-cell">
      <span class="sv sv-warn">{{TOTAL_WARN}}</span>
      <span class="slabel">Warn</span>
    </div>
    <div class="stat-cell">
      <span class="sv sv-fail">{{TOTAL_FAIL}}</span>
      <span class="slabel">Fail</span>
    </div>
    <div class="stat-cell">
      <span class="sv sv-accent">{{SPEC_COUNT}}</span>
      <span class="slabel">OpenAPI Spec{{SPEC_SUFFIX}}</span>
    </div>
    <div class="stat-cell">
      <span class="sv" style="color:var(--text2);font-size:18px">{{AUDIT_DATE}}</span>
      <span class="slabel">Audit Date</span>
    </div>
  </div>
</div>
```

`{{SPEC_SUFFIX}}` = "" if spec accessible, " (404)" if canonical spec returns 404.

**CSS for header:**
```css
.header {
  border-bottom: 1px solid var(--border);
  padding: 48px 64px 40px;
  position: relative;
  overflow: hidden;
  background: linear-gradient(135deg, #0a061a 0%, var(--bg) 60%);
}
.header::after {
  content: '';
  position: absolute;
  top: -100px; right: -100px;
  width: 500px; height: 500px;
  background: radial-gradient(circle, rgba(167,139,250,0.08) 0%, transparent 60%);
  pointer-events: none;
}
.eyebrow {
  font-family: 'Space Mono', monospace;
  font-size: 10px; color: var(--accent);
  letter-spacing: 0.2em; text-transform: uppercase;
  margin-bottom: 10px; display: flex; align-items: center; gap: 8px;
}
.eyebrow::before { content: ''; display: block; width: 20px; height: 1px; background: var(--accent); }
h1 { font-size: 36px; font-weight: 700; letter-spacing: -0.03em; margin-bottom: 6px; }
.header-url {
  font-family: 'Space Mono', monospace; font-size: 12px; color: var(--text3);
  background: var(--surface2); border: 1px solid var(--border);
  display: inline-flex; align-items: center; gap: 6px;
  padding: 5px 12px; border-radius: 4px; margin-bottom: 36px;
}
.header-url::before { content: '→'; color: var(--accent); font-size: 10px; }
.stats-row { display: flex; border: 1px solid var(--border); border-radius: 8px; overflow: hidden; width: fit-content; }
.stat-cell { padding: 16px 28px; border-right: 1px solid var(--border); display: flex; flex-direction: column; gap: 4px; background: var(--surface); }
.stat-cell:last-child { border-right: none; }
.sv { font-family: 'Space Mono', monospace; font-size: 26px; font-weight: 700; line-height: 1; }
.sv-total{color:var(--text)} .sv-pass{color:var(--pass)} .sv-warn{color:var(--warn)} .sv-fail{color:var(--fail)} .sv-accent{color:var(--accent2)}
.slabel { font-size: 10px; color: var(--text3); text-transform: uppercase; letter-spacing: 0.1em; }
```

---

## 4. Legend Bar

```html
<div class="legend-bar">
  <span class="ll">Legend</span>
  <div class="li"><span class="badge pass">✓ PASS</span> Present and correct</div>
  <div class="li"><span class="badge warn">⚠ WARN</span> Present but incomplete</div>
  <div class="li"><span class="badge fail">✕ FAIL</span> Missing or wrong</div>
</div>
```

```css
.legend-bar { padding: 12px 64px; border-bottom: 1px solid var(--border); background: var(--surface); display: flex; align-items: center; gap: 24px; flex-wrap: wrap; }
.ll { font-family: 'Space Mono', monospace; font-size: 9px; color: var(--text3); text-transform: uppercase; letter-spacing: 0.18em; }
.badge { display: inline-flex; align-items: center; gap: 4px; padding: 2px 8px; border-radius: 3px; font-family: 'Space Mono', monospace; font-size: 10px; font-weight: 700; letter-spacing: 0.06em; }
.badge.pass { background: var(--pass-bg); color: var(--pass); border: 1px solid var(--pass-border); }
.badge.warn { background: var(--warn-bg); color: var(--warn); border: 1px solid var(--warn-border); }
.badge.fail { background: var(--fail-bg); color: var(--fail); border: 1px solid var(--fail-border); }
.li { display: flex; align-items: center; gap: 8px; font-size: 12px; color: var(--text2); }
```

---

## 5. Sidebar

```html
<nav class="sidebar">
  <div class="sbh">Overview</div>
  <div class="sbl" onclick="scrollTo('scorecard')">Summary Scorecard</div>
  <div class="sbl" onclick="scrollTo('pattern')">Site-Wide Pattern</div>
  <div class="sbl" onclick="scrollTo('top-issues')">Top Issues</div>
  <div class="sbh" style="margin-top:8px">Sections</div>
  <!-- For each category: -->
  <div class="sbl" onclick="scrollTo('{{CAT_ID}}')">
    {{CAT_NAME}}
    <span class="sbp">
      <span class="spp spp-p">{{CAT_PASS}}P</span>
      <span class="spp spp-w">{{CAT_WARN}}W</span>
      <span class="spp spp-f">{{CAT_FAIL}}F</span>
    </span>
  </div>
</nav>
```

`{{CAT_ID}}` = category name lowercased, spaces replaced with hyphens.
e.g. "Context Graph" → `context-graph`

```css
.main { display: grid; grid-template-columns: 256px 1fr; min-height: calc(100vh - 200px); }
.sidebar { border-right: 1px solid var(--border); padding: 20px 0; position: sticky; top: 0; height: 100vh; overflow-y: auto; background: var(--surface); }
.sidebar::-webkit-scrollbar { width: 3px; } .sidebar::-webkit-scrollbar-thumb { background: var(--border2); }
.sbh { font-family: 'Space Mono', monospace; font-size: 9px; color: var(--text3); text-transform: uppercase; letter-spacing: 0.18em; padding: 8px 20px 4px; }
.sbl { display: flex; align-items: center; justify-content: space-between; padding: 7px 20px; font-size: 12px; color: var(--text2); cursor: pointer; border-left: 2px solid transparent; transition: all 0.12s; }
.sbl:hover { background: var(--surface2); color: var(--text); border-left-color: var(--border2); }
.sbp { display: flex; gap: 3px; }
.spp { font-family: 'Space Mono', monospace; font-size: 9px; padding: 1px 5px; border-radius: 2px; }
.spp-p { background: var(--pass-bg); color: var(--pass); }
.spp-w { background: var(--warn-bg); color: var(--warn); }
.spp-f { background: var(--fail-bg); color: var(--fail); }
.content { padding: 40px 56px; max-width: 1080px; }
```

---

## 6. Scorecard Table

```html
<div id="scorecard" style="margin-bottom:48px">
  <div class="st">Summary Scorecard</div>
  <table class="sc-table">
    <thead>
      <tr><th>Category</th><th>Endpoints</th><th>✓ Pass</th><th>⚠ Warn</th><th>✕ Fail</th></tr>
    </thead>
    <tbody>
      <!-- For each category row: -->
      <tr>
        <td><a class="clink" onclick="scrollTo('{{CAT_ID}}')">{{CAT_NAME}}</a></td>
        <td class="nt">{{CAT_TOTAL}}</td>
        <td class="np">{{CAT_PASS}}</td>
        <td class="nw">{{CAT_WARN}}</td>
        <td class="nf">{{CAT_FAIL}}</td>
      </tr>
      <!-- Total row (last): -->
      <tr>
        <td><strong>Total</strong></td>
        <td class="nt">{{TOTAL_ENDPOINTS}}</td>
        <td class="np">{{TOTAL_PASS}}</td>
        <td class="nw">{{TOTAL_WARN}}</td>
        <td class="nf">{{TOTAL_FAIL}}</td>
      </tr>
    </tbody>
  </table>
</div>
```

```css
.st { font-family: 'Space Mono', monospace; font-size: 9px; color: var(--accent); text-transform: uppercase; letter-spacing: 0.2em; margin-bottom: 14px; }
.sc-table { width: 100%; border-collapse: collapse; border: 1px solid var(--border); border-radius: 6px; overflow: hidden; margin-bottom: 48px; }
.sc-table thead tr { background: var(--surface2); border-bottom: 1px solid var(--border2); }
.sc-table th { padding: 10px 14px; text-align: left; font-family: 'Space Mono', monospace; font-size: 9px; color: var(--text3); text-transform: uppercase; letter-spacing: 0.12em; font-weight: 400; }
.sc-table th:not(:first-child) { text-align: center; }
.sc-table td { padding: 11px 14px; border-bottom: 1px solid var(--border); font-size: 13px; }
.sc-table td:not(:first-child) { text-align: center; font-family: 'Space Mono', monospace; font-size: 12px; font-weight: 700; }
.sc-table tbody tr:last-child td { border-bottom: none; background: var(--surface2); font-weight: 600; }
.sc-table tbody tr:hover:not(:last-child) { background: rgba(255,255,255,0.015); }
.np{color:var(--pass)} .nw{color:var(--warn)} .nf{color:var(--fail)} .nt{color:var(--text)}
.clink { color: var(--text); cursor: pointer; } .clink:hover { color: var(--accent2); }
```

---

## 7. Site-Wide Pattern Box

Only render this section if `SITE_WIDE_PATTERNS` is non-empty.

```html
<div id="pattern" style="margin-bottom:48px">
  <div class="st">Site-Wide Pattern — Applies to All {{PATTERN_SCOPE}} Endpoints</div>
  <div class="pbox">
    {{PATTERN_PARAGRAPH_1}}
    <br><br>
    {{PATTERN_PARAGRAPH_2}}
    <!-- Add <br><br> between each pattern paragraph -->
  </div>
</div>
```

`{{PATTERN_SCOPE}}` = "~N" where N is the total endpoint count, or "most" if patterns
are partial. e.g. "~230" or "most"

```css
.pbox { background: var(--accent-bg); border: 1px solid #2e1f6e; border-radius: 6px; padding: 16px 20px; margin-bottom: 20px; font-size: 13px; color: var(--text2); line-height: 1.7; }
.pbox strong { color: var(--accent2); }
code { font-family: 'Space Mono', monospace; font-size: 10px; background: var(--tag-bg); padding: 1px 5px; border-radius: 3px; color: var(--accent2); }
hr.divider { border: none; border-top: 1px solid var(--border); margin: 40px 0; }
```

---

## 8. Top Issues Section

```html
<div id="top-issues" style="margin-bottom:48px">
  <div class="st">Top Priority Issues</div>
  <div class="ibox">
    <!-- For each issue (max 10): -->
    <div class="irow">
      <span class="in">{{ISSUE_NUM}}</span>
      <span style="flex-shrink:0;padding-top:2px"><span class="badge {{ISSUE_SEVERITY}}">{{ISSUE_ICON}}</span></span>
      <span class="it"><strong>{{ISSUE_TITLE}}:</strong> {{ISSUE_DESCRIPTION}}</span>
    </div>
  </div>
</div>
```

`{{ISSUE_NUM}}` = zero-padded 2-digit number: 01, 02, ... 10
`{{ISSUE_SEVERITY}}` = `fail` or `warn`
`{{ISSUE_ICON}}` = `✕ FAIL` or `⚠ WARN`

```css
.ibox { border: 1px solid var(--border); border-radius: 6px; overflow: hidden; margin-bottom: 48px; }
.irow { display: flex; gap: 16px; padding: 14px 18px; border-bottom: 1px solid var(--border); align-items: flex-start; }
.irow:last-child { border-bottom: none; }
.in { font-family: 'Space Mono', monospace; font-size: 10px; color: var(--text3); flex-shrink: 0; padding-top: 2px; width: 20px; }
.it { font-size: 13px; color: var(--text2); line-height: 1.6; }
.it strong { color: var(--text); }
```

---

## 9. Section Layout (per category)

Each category gets one `<div class="as" id="{{CAT_ID}}">`.

```html
<div class="as" id="{{CAT_ID}}">
  <div class="sh">
    <div class="sn">{{CAT_NAME}}</div>
    <span class="sc">{{CAT_TOTAL}} endpoints</span>
    <span class="badge pass">{{CAT_PASS}} pass</span>
    <span class="badge warn">{{CAT_WARN}} warn</span>
    <span class="badge fail">{{CAT_FAIL}} fail</span>
  </div>

  <!-- Optional: pattern box for this category if a sub-pattern exists -->
  <div class="pbox" style="margin-bottom:12px">
    <strong>Pattern:</strong> {{CATEGORY_PATTERN_TEXT}}
  </div>

  <!-- Endpoint cards and/or group tables go here -->
  {{ENDPOINTS_HTML}}

</div>
```

```css
.as { margin-bottom: 56px; scroll-margin-top: 20px; }
.sh { display: flex; align-items: center; gap: 10px; padding-bottom: 14px; border-bottom: 1px solid var(--border); margin-bottom: 16px; }
.sn { font-size: 20px; font-weight: 700; letter-spacing: -0.01em; }
.sc { font-size: 11px; color: var(--text3); background: var(--surface2); border: 1px solid var(--border); padding: 3px 10px; border-radius: 20px; }
```

---

## 10. Endpoint Card — Detailed

Use this for **notable endpoints** that have at least one FAIL or a complex story worth
showing in detail. Typically: the most important 1-3 endpoints per category, always including
any with FAIL status that have a useful fix. Collapse by default; open the most important one.

```html
<div class="ec {{CARD_CLASS}}" id="ep-{{EP_SLUG}}">
  <div class="eh" onclick="toggle(this)">
    <span class="mt {{METHOD_CLASS}}">{{METHOD}}</span>
    <span class="ep">{{EP_PATH}}</span>
    <span class="en">{{EP_NAME}}</span>
    <div class="eds">
      <!-- 5 dots, one per check, in order: desc, spec, params, codes, schema -->
      <span class="dot {{CHECK1_STATUS}}"></span>
      <span class="dot {{CHECK2_STATUS}}"></span>
      <span class="dot {{CHECK3_STATUS}}"></span>
      <span class="dot {{CHECK4_STATUS}}"></span>
      <span class="dot {{CHECK5_STATUS}}"></span>
    </div>
    <span class="chv">▼</span>
  </div>
  <div class="eb">
    <table class="ct">
      <!-- Check row template: -->
      <tr class="{{ROW_CLASS}}">
        <td class="cl">{{CHECK_LABEL}}</td>
        <td class="cs"><span class="badge {{CHECK_STATUS}}">{{CHECK_ICON}}</span></td>
        <td>
          <div class="cn">{{CURRENT_STATE}}</div>
          <div class="cx"><strong>Fix:</strong> {{FIX_GUIDANCE}}</div>
          <!-- Only show cx div if status is WARN or FAIL -->
        </td>
      </tr>
    </table>
  </div>
</div>
```

**`{{CARD_CLASS}}`** based on worst check status:
- Any FAIL → `ec cf`
- Only WARNs → `ec cw`
- All PASS → `ec cp`
- Add `open` to pre-expand: `ec cf open`

**`{{METHOD_CLASS}}`:**
- GET → `mt mg`
- POST → `mt mp`
- PUT → `mt mu` (use orange)
- DELETE → `mt md`
- PATCH → `mt mpatch`

**`{{ROW_CLASS}}`:** `rp` (pass), `rw` (warn), `rf` (fail)

**`{{CHECK_LABEL}}`:** Description | OpenAPI Spec | Body Params | Response Codes | Response Schema

**`{{CHECK_ICON}}`:** `✓ PASS` | `⚠ WARN` | `✕ FAIL`

**Only show the Fix guidance div** (`cx`) when status is WARN or FAIL.

```css
.ec { border: 1px solid var(--border); border-radius: 6px; margin-bottom: 10px; overflow: hidden; }
.ec.cf { border-left: 3px solid var(--fail); }
.ec.cw:not(.cf) { border-left: 3px solid var(--warn); }
.ec.cp { border-left: 3px solid var(--pass); }
.eh { display: flex; align-items: center; gap: 10px; padding: 12px 18px; background: var(--surface); cursor: pointer; user-select: none; transition: background 0.1s; }
.eh:hover { background: var(--surface2); }
.mt { font-family: 'Space Mono', monospace; font-size: 9px; font-weight: 700; padding: 2px 6px; border-radius: 3px; flex-shrink: 0; letter-spacing: 0.05em; }
.mg { background: #052015; color: #4ade80; border: 1px solid #064824; }
.mp { background: #12093a; color: #a78bfa; border: 1px solid #2e1f6e; }
.mu { background: #1a0e00; color: #fb923c; border: 1px solid #431c00; }
.md { background: #200808; color: #f87171; border: 1px solid #4a1212; }
.mpatch { background: #111400; color: #bef264; border: 1px solid #2a3100; }
.ep { font-family: 'Space Mono', monospace; font-size: 11px; color: var(--text3); flex: 1; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.en { font-size: 13px; font-weight: 500; flex-shrink: 0; color: var(--text); }
.eds { display: flex; gap: 3px; flex-shrink: 0; }
.dot { width: 7px; height: 7px; border-radius: 50%; }
.dot.pass { background: var(--pass); } .dot.warn { background: var(--warn); } .dot.fail { background: var(--fail); }
.chv { color: var(--text3); font-size: 9px; transition: transform 0.18s; flex-shrink: 0; }
.ec.open .chv { transform: rotate(180deg); }
.eb { display: none; border-top: 1px solid var(--border); }
.ec.open .eb { display: block; }
.ct { width: 100%; border-collapse: collapse; }
.ct tr { border-bottom: 1px solid var(--border); }
.ct tr:last-child { border-bottom: none; }
.ct td { padding: 11px 18px; vertical-align: top; }
.cl { width: 190px; font-family: 'Space Mono', monospace; font-size: 9px; color: var(--text3); text-transform: uppercase; letter-spacing: 0.1em; padding-top: 13px; white-space: nowrap; }
.cs { width: 72px; padding-top: 10px; }
.cn { color: var(--text2); font-size: 13px; line-height: 1.6; }
.cx { font-size: 11px; color: var(--text3); margin-top: 3px; font-style: italic; }
.cx strong { color: var(--warn); font-style: normal; }
.rp { background: rgba(52,211,153,0.02); }
.rw { background: rgba(251,191,36,0.02); }
.rf { background: rgba(248,113,113,0.03); }
```

---

## 11. Compact Group Table

Use this for the **remaining endpoints** in a category after showing the notable cards.
Also use this as the primary display for categories where the pattern is completely
uniform (e.g. all endpoints fail the same two checks — just show the table).

```html
<div style="margin-top:10px;border:1px solid var(--border);border-radius:6px;overflow:hidden;">
  <table style="width:100%;border-collapse:collapse;">
    <thead>
      <tr style="background:var(--surface2);border-bottom:1px solid var(--border2);">
        <th style="{{TH_STYLE}} text-align:left">Endpoint</th>
        <th style="{{TH_STYLE}} text-align:center">Desc</th>
        <th style="{{TH_STYLE}} text-align:center">Spec</th>
        <th style="{{TH_STYLE}} text-align:center">Params</th>
        <th style="{{TH_STYLE}} text-align:center">Codes</th>
        <th style="{{TH_STYLE}} text-align:center">Schema</th>
        <!-- Add Notes column only if any row has a note: -->
        <th style="{{TH_STYLE}} text-align:left">Notes</th>
      </tr>
    </thead>
    <tbody>
      <!-- For each endpoint: -->
      <tr style="border-bottom:{{BORDER}}">
        <td style="padding:9px 14px;font-family:'Space Mono',monospace;font-size:10px;color:var(--text2);">
          {{EP_PATH}}
        </td>
        <td style="padding:9px;text-align:center">{{BADGE_DESC}}</td>
        <td style="padding:9px;text-align:center">{{BADGE_SPEC}}</td>
        <td style="padding:9px;text-align:center">{{BADGE_PARAMS}}</td>
        <td style="padding:9px;text-align:center">{{BADGE_CODES}}</td>
        <td style="padding:9px;text-align:center">{{BADGE_SCHEMA}}</td>
        <td style="padding:9px 14px;font-size:11px;color:var(--text3);">{{ROW_NOTE}}</td>
      </tr>
    </tbody>
  </table>
  <div style="padding:9px 14px;font-size:11px;color:var(--text3);border-top:1px solid var(--border);background:var(--surface2);font-style:italic;">
    {{TABLE_FOOTER_NOTE}}
  </div>
</div>
```

`{{TH_STYLE}}` = `padding:9px 14px;font-family:'Space Mono',monospace;font-size:9px;color:var(--text3);text-transform:uppercase;letter-spacing:0.1em;background:var(--surface2);border-bottom:1px solid var(--border2);font-weight:400;`

`{{BORDER}}` = `1px solid var(--border)` for all rows except last, `none` for last row.

`{{BADGE_*}}` = mini badge HTML:
```html
<!-- pass --> <span class="badge pass" style="font-size:9px">✓</span>
<!-- warn --> <span class="badge warn" style="font-size:9px">⚠</span>
<!-- fail --> <span class="badge fail" style="font-size:9px">✕</span>
```

`{{TABLE_FOOTER_NOTE}}` = summary of common issues, e.g.:
"❌ All missing 400, 401, 403, 404, 500. Execute Team and Execute Team Stream have empty response schemas."

**When to use a footer note:** Always when the table has a pattern note. Make it specific —
list actual endpoint names and actual missing codes. Never write "see above".

---

## 12. JavaScript

Include this script block at the end of `<body>`:

```javascript
function toggle(h) { h.closest('.ec').classList.toggle('open'); }
function scrollTo(id) {
  document.getElementById(id)?.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// Dynamic table builder — used to inject group tables from JS arrays
// This is optional if tables are pre-rendered as HTML strings.
// Use this pattern if building tables programmatically:
const b = (s) => {
  if (s === 'pass') return '<span class="badge pass" style="font-size:9px">✓</span>';
  if (s === 'warn') return '<span class="badge warn" style="font-size:9px">⚠</span>';
  return '<span class="badge fail" style="font-size:9px">✕</span>';
};
```

---

## 13. Variable Substitution Map

| Variable | How to derive |
|---|---|
| `{{SITE_NAME}}` | Domain name with caps: "Kubiya", "AIsa", "Fount" etc. |
| `{{DOCS_URL}}` | Raw input URL |
| `{{AUDIT_DATE}}` | Today's date in "Month DD, YYYY" format |
| `{{TOTAL_ENDPOINTS}}` | Count of all endpoint pages fetched. Use "~N" if approximate. |
| `{{TOTAL_PASS}}` | Sum of pass_count across all categories |
| `{{TOTAL_WARN}}` | Sum of warn_count |
| `{{TOTAL_FAIL}}` | Sum of fail_count |
| `{{SPEC_COUNT}}` | `1` if canonical spec accessible, `0` if 404. Or count of spec files. |
| `{{SPEC_SUFFIX}}` | `" (404)"` if canonical spec 404, `""` otherwise |
| `{{CAT_ID}}` | Category name → lowercase → spaces to hyphens |
| `{{CAT_NAME}}` | Category display name (title case) |
| `{{CAT_TOTAL}}` | Endpoint count in category |
| `{{CAT_PASS/WARN/FAIL}}` | Count per status in category |
| `{{ISSUE_NUM}}` | 01, 02, ... 10 |
| `{{ISSUE_SEVERITY}}` | `fail` or `warn` |
| `{{EP_SLUG}}` | Endpoint path → lowercase → slashes to hyphens |
| `{{PATTERN_SCOPE}}` | "~N" total endpoints or "most" |

---

## 14. Section Rendering Decision Rules

For each category, decide which combination of cards and tables to use:

### Rule A — Small category (≤ 5 endpoints, varied results)
Render every endpoint as an individual collapsible card. Open the worst ones by default.

### Rule B — Medium category (6–15 endpoints, 1–3 notable endpoints)
Render the 1–3 most notable endpoints (highest severity or most complex findings) as
detailed cards. Render the remaining endpoints in a compact group table beneath.

### Rule C — Large category (> 15 endpoints, uniform pattern)
Render a `pbox` pattern summary at the top of the section. Render 1 representative
detailed card showing the pattern. Render all remaining endpoints in a compact group table.

### Rule D — All endpoints pass
No cards needed. Just render a green banner:
```html
<div style="background:var(--pass-bg);border:1px solid var(--pass-border);border-radius:6px;padding:14px 18px;font-size:13px;color:#86efac;">
  All {{CAT_TOTAL}} endpoints in this category are fully documented.
</div>
```

### Rule E — Black hole category (all endpoints have no meaningful docs)
Render a red banner summarising the problem, then a compact table.
```html
<div class="fail-banner">
  <strong style="color:var(--fail)">All {{CAT_TOTAL}} endpoints in this category are undocumented.</strong>
  {{EXPLANATION}}
</div>
```

```css
.fail-banner { background: var(--fail-bg); border: 1px solid var(--fail-border); border-radius: 6px; padding: 14px 18px; margin-bottom: 12px; font-size: 13px; color: #fca5a5; }
```

### Rule F — Deprecated endpoints
Always give deprecated endpoints their own category section at the bottom, after all
functional sections. Show each as a table row with the issue and the fix.

---

## Responsive / mobile CSS

```css
@media (max-width: 900px) {
  .main { grid-template-columns: 1fr; }
  .sidebar { display: none; }
  .header, .legend-bar, .content { padding-left: 20px; padding-right: 20px; }
}
```
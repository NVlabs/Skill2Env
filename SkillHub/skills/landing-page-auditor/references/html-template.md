# Landing Page GEO Audit — HTML Report Template

Use this template when generating the audit report. Copy the full HTML below, populate the
`AUDIT_DATA` JavaScript object with real audit values, and write the completed file to disk.

**Never leave placeholder text or `{{VARIABLE}}` strings in the output file.**
Every value in `AUDIT_DATA` must come from the actual audit results.

---

## Full HTML Template

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Landing Page Audit Report</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@400;500;600;700&family=DM+Sans:wght@400;500&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    :root {
      --bg:           #0D0A1A;
      --bg-card:      #161228;
      --bg-elevated:  #1E1838;
      --border:       #2A2347;
      --border-light: #342C5A;
      --accent:       #8157F2;
      --accent-dim:   rgba(129, 87, 242, 0.12);
      --accent-glow:  rgba(129, 87, 242, 0.25);
      --text-1:       #F0EDF9;
      --text-2:       #9B93BE;
      --text-3:       #5E577A;
      --pass:         #22C55E;
      --pass-bg:      rgba(34, 197, 94, 0.10);
      --pass-border:  rgba(34, 197, 94, 0.20);
      --warn:         #F59E0B;
      --warn-bg:      rgba(245, 158, 11, 0.10);
      --warn-border:  rgba(245, 158, 11, 0.20);
      --fail:         #EF4444;
      --fail-bg:      rgba(239, 68, 68, 0.10);
      --fail-border:  rgba(239, 68, 68, 0.20);
      --manual:       #64748B;
      --manual-bg:    rgba(100, 116, 139, 0.10);
      --manual-border:rgba(100, 116, 139, 0.20);
      --green-score:  #22C55E;
      --amber-score:  #F59E0B;
      --red-score:    #EF4444;
    }

    body {
      font-family: 'DM Sans', system-ui, sans-serif;
      background: var(--bg);
      color: var(--text-1);
      min-height: 100vh;
      line-height: 1.6;
    }

    /* ── Layout ── */
    .page { max-width: 1100px; margin: 0 auto; padding: 0 24px 80px; }

    /* ── Header ── */
    .header {
      display: flex; align-items: center; justify-content: space-between;
      padding: 20px 0; border-bottom: 1px solid var(--border); margin-bottom: 40px;
    }
    .header-brand {
      font-family: 'Instrument Sans', sans-serif;
      font-size: 18px; font-weight: 700; color: var(--text-1); letter-spacing: -0.3px;
    }
    .header-brand span { color: var(--accent); }
    .header-label {
      font-size: 12px; font-weight: 500; color: var(--text-3);
      text-transform: uppercase; letter-spacing: 1px;
    }

    /* ── Hero ── */
    .hero {
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 36px;
      display: grid;
      grid-template-columns: 1fr auto;
      gap: 40px;
      align-items: center;
      margin-bottom: 32px;
      position: relative;
      overflow: hidden;
    }
    .hero::before {
      content: '';
      position: absolute;
      top: -60px; right: -60px;
      width: 200px; height: 200px;
      background: radial-gradient(circle, var(--accent-glow) 0%, transparent 70%);
      pointer-events: none;
    }
    .hero-left { min-width: 0; }
    .hero-tag {
      display: inline-flex; align-items: center; gap: 6px;
      background: var(--accent-dim); border: 1px solid var(--accent-glow);
      border-radius: 99px; padding: 4px 12px;
      font-size: 11px; font-weight: 500; color: var(--accent);
      text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 16px;
    }
    .hero-url {
      font-family: 'DM Mono', monospace;
      font-size: 14px; color: var(--text-2);
      word-break: break-all; margin-bottom: 8px;
    }
    .hero-date { font-size: 13px; color: var(--text-3); margin-bottom: 24px; }
    .hero-counts { display: flex; gap: 12px; flex-wrap: wrap; }
    .count-pill {
      display: flex; align-items: center; gap: 6px;
      padding: 6px 14px; border-radius: 99px;
      font-size: 13px; font-weight: 500;
      border: 1px solid transparent;
    }
    .count-pill.pass { background: var(--pass-bg); border-color: var(--pass-border); color: var(--pass); }
    .count-pill.warn { background: var(--warn-bg); border-color: var(--warn-border); color: var(--warn); }
    .count-pill.fail { background: var(--fail-bg); border-color: var(--fail-border); color: var(--fail); }
    .count-pill.manual { background: var(--manual-bg); border-color: var(--manual-border); color: var(--manual); }
    .count-dot { width: 7px; height: 7px; border-radius: 50%; background: currentColor; }

    /* ── Score gauge ── */
    .score-gauge { position: relative; width: 140px; height: 140px; flex-shrink: 0; }
    .score-gauge svg { width: 140px; height: 140px; transform: rotate(-90deg); }
    .gauge-track { fill: none; stroke: var(--border); stroke-width: 10; }
    .gauge-fill  { fill: none; stroke-width: 10; stroke-linecap: round; transition: stroke-dasharray 1s ease; }
    .score-text {
      position: absolute; inset: 0;
      display: flex; flex-direction: column; align-items: center; justify-content: center;
    }
    .score-num {
      font-family: 'Instrument Sans', sans-serif;
      font-size: 40px; font-weight: 700; line-height: 1; letter-spacing: -2px;
    }
    .score-denom { font-size: 13px; color: var(--text-3); margin-top: 2px; }

    /* ── Category grid ── */
    .section-title {
      font-family: 'Instrument Sans', sans-serif;
      font-size: 14px; font-weight: 600; color: var(--text-3);
      text-transform: uppercase; letter-spacing: 1px;
      margin-bottom: 16px;
    }
    .cat-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
      gap: 12px;
      margin-bottom: 40px;
    }
    .cat-card {
      background: var(--bg-card); border: 1px solid var(--border);
      border-radius: 12px; padding: 18px 20px;
      cursor: pointer; transition: border-color 0.15s, background 0.15s;
    }
    .cat-card:hover { border-color: var(--border-light); background: var(--bg-elevated); }
    .cat-card.active { border-color: var(--accent); }
    .cat-card-top { display: flex; align-items: center; justify-content: space-between; margin-bottom: 10px; }
    .cat-name {
      font-family: 'Instrument Sans', sans-serif;
      font-size: 13px; font-weight: 600; color: var(--text-1);
    }
    .cat-score-badge {
      font-family: 'Instrument Sans', sans-serif;
      font-size: 16px; font-weight: 700;
    }
    .cat-bar-track {
      height: 6px; background: var(--border); border-radius: 99px; overflow: hidden; margin-bottom: 10px;
    }
    .cat-bar-fill { height: 100%; border-radius: 99px; transition: width 0.8s ease; }
    .cat-mini-counts { display: flex; gap: 10px; }
    .cat-mini { font-size: 11px; color: var(--text-3); }
    .cat-mini span { font-weight: 600; }
    .cat-mini.p span { color: var(--pass); }
    .cat-mini.w span { color: var(--warn); }
    .cat-mini.f span { color: var(--fail); }
    .cat-mini.m span { color: var(--manual); }

    /* ── Checks detail ── */
    .checks-wrapper { margin-bottom: 40px; }
    .checks-section {
      background: var(--bg-card); border: 1px solid var(--border);
      border-radius: 12px; overflow: hidden; margin-bottom: 10px;
    }
    .checks-section-header {
      display: flex; align-items: center; justify-content: space-between;
      padding: 14px 20px; cursor: pointer; user-select: none;
      transition: background 0.15s;
    }
    .checks-section-header:hover { background: var(--bg-elevated); }
    .checks-section-title {
      font-family: 'Instrument Sans', sans-serif;
      font-size: 14px; font-weight: 600; color: var(--text-1);
    }
    .checks-section-right { display: flex; align-items: center; gap: 12px; }
    .checks-section-score {
      font-family: 'Instrument Sans', sans-serif;
      font-size: 15px; font-weight: 700;
    }
    .chevron {
      width: 16px; height: 16px; color: var(--text-3);
      transition: transform 0.2s; flex-shrink: 0;
    }
    .checks-section.open .chevron { transform: rotate(180deg); }
    .checks-body { display: none; border-top: 1px solid var(--border); }
    .checks-section.open .checks-body { display: block; }
    .check-row {
      display: flex; align-items: flex-start; gap: 12px;
      padding: 12px 20px; border-bottom: 1px solid var(--border);
    }
    .check-row:last-child { border-bottom: none; }
    .check-icon {
      width: 20px; height: 20px; border-radius: 50%;
      display: flex; align-items: center; justify-content: center;
      font-size: 10px; font-weight: 700; flex-shrink: 0; margin-top: 1px;
    }
    .icon-pass { background: var(--pass-bg); color: var(--pass); }
    .icon-warn { background: var(--warn-bg); color: var(--warn); }
    .icon-fail { background: var(--fail-bg); color: var(--fail); }
    .icon-manual { background: var(--manual-bg); color: var(--manual); }
    .check-content { flex: 1; min-width: 0; }
    .check-label { font-size: 13px; font-weight: 500; color: var(--text-1); line-height: 1.4; }
    .check-note { font-size: 12px; color: var(--text-2); margin-top: 3px; line-height: 1.5; }

    /* ── Top Fixes ── */
    .fixes-list { display: flex; flex-direction: column; gap: 10px; margin-bottom: 40px; }
    .fix-card {
      background: var(--bg-card); border: 1px solid var(--border);
      border-radius: 12px; padding: 18px 20px;
      display: grid; grid-template-columns: auto 1fr; gap: 16px; align-items: start;
    }
    .fix-priority {
      font-family: 'Instrument Sans', sans-serif;
      font-size: 11px; font-weight: 700; color: var(--accent);
      background: var(--accent-dim); border: 1px solid var(--accent-glow);
      border-radius: 99px; padding: 2px 10px; white-space: nowrap; margin-top: 2px;
    }
    .fix-body { min-width: 0; }
    .fix-top { display: flex; align-items: center; gap: 8px; margin-bottom: 4px; flex-wrap: wrap; }
    .fix-title {
      font-family: 'Instrument Sans', sans-serif;
      font-size: 14px; font-weight: 600; color: var(--text-1);
    }
    .fix-tags { display: flex; gap: 6px; }
    .fix-tag {
      font-size: 11px; padding: 1px 8px; border-radius: 99px;
      border: 1px solid var(--border-light); color: var(--text-3);
    }
    .fix-tag.high { border-color: var(--fail-border); color: var(--fail); background: var(--fail-bg); }
    .fix-tag.medium { border-color: var(--warn-border); color: var(--warn); background: var(--warn-bg); }
    .fix-tag.low { border-color: var(--pass-border); color: var(--pass); background: var(--pass-bg); }
    .fix-detail { font-size: 13px; color: var(--text-2); line-height: 1.5; }

    /* ── Footer ── */
    .footer {
      border-top: 1px solid var(--border); padding-top: 24px;
      display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 12px;
    }
    .footer-brand {
      font-family: 'Instrument Sans', sans-serif;
      font-size: 13px; font-weight: 600; color: var(--text-3);
    }
    .footer-brand span { color: var(--accent); }
    .footer-note { font-size: 12px; color: var(--text-3); }

    /* ── Utilities ── */
    .color-green { color: var(--green-score); }
    .color-amber { color: var(--amber-score); }
    .color-red   { color: var(--red-score); }
    .bar-green   { background: var(--green-score); }
    .bar-amber   { background: var(--amber-score); }
    .bar-red     { background: var(--red-score); }

    @media (max-width: 640px) {
      .hero { grid-template-columns: 1fr; }
      .score-gauge { margin: 0 auto; }
      .hero-counts { gap: 8px; }
    }
  </style>
</head>
<body>
<div class="page">

  <!-- Header -->
  <header class="header">
    <div class="header-brand">infra<span>sity</span></div>
    <div class="header-label">Landing Page GEO Audit</div>
  </header>

  <!-- Hero -->
  <div class="hero">
    <div class="hero-left">
      <div class="hero-tag">
        <span>●</span> GEO &amp; LLM Readiness
      </div>
      <div class="hero-url" id="hero-url"></div>
      <div class="hero-date" id="hero-date"></div>
      <div class="hero-counts" id="hero-counts"></div>
    </div>
    <div class="score-gauge">
      <svg viewBox="0 0 120 120">
        <circle class="gauge-track" cx="60" cy="60" r="52"/>
        <circle class="gauge-fill" id="gauge-fill" cx="60" cy="60" r="52"
          stroke-dasharray="0 326.73" stroke-dashoffset="0"/>
      </svg>
      <div class="score-text">
        <div class="score-num" id="score-num"></div>
        <div class="score-denom">/100</div>
      </div>
    </div>
  </div>

  <!-- Category Grid -->
  <div class="section-title">Score by Category</div>
  <div class="cat-grid" id="cat-grid"></div>

  <!-- Detailed Checks -->
  <div class="section-title">Detailed Checks</div>
  <div class="checks-wrapper" id="checks-wrapper"></div>

  <!-- Top Fixes -->
  <div class="section-title">Top Fixes by Priority</div>
  <div class="fixes-list" id="fixes-list"></div>

  <!-- Footer -->
  <footer class="footer">
    <div class="footer-brand">infra<span>sity</span> Landing Page Auditor v1.0</div>
    <div class="footer-note" id="footer-note"></div>
  </footer>

</div>

<script>
// ─────────────────────────────────────────────────────────────
// POPULATE THIS OBJECT WITH REAL AUDIT DATA — NO PLACEHOLDERS
// ─────────────────────────────────────────────────────────────
const AUDIT_DATA = {
  url: "FILL_URL",
  domain: "FILL_DOMAIN",
  date: "FILL_DATE",
  overallScore: 0,
  totalChecks: 48,
  scoreable: 47,
  pass: 0,
  warn: 0,
  fail: 0,
  manual: 0,
  categories: [
    {
      name: "Content Clarity & Directness",
      score: 0,
      pass: 0, warn: 0, fail: 0, manual: 0,
      checks: [
        { status: "pass", label: "Clear opening sentence describing the service", note: "Evidence note here" },
        { status: "fail", label: "Service definition in first 100 words", note: "Evidence note here" },
        { status: "fail", label: "No unexplained jargon or acronyms", note: "Evidence note here" },
        { status: "pass", label: "Use case statements present", note: "Evidence note here" },
        { status: "pass", label: "Negative scoping present", note: "Evidence note here" }
      ]
    },
    {
      name: "Structure & Scannability",
      score: 0,
      pass: 0, warn: 0, fail: 0, manual: 0,
      checks: [
        { status: "fail", label: "Proper H1 → H2 → H3 heading hierarchy", note: "Evidence note here" },
        { status: "pass", label: "At least one question-phrased heading", note: "Evidence note here" },
        { status: "fail", label: "Short paragraphs (avg ≤15 words, no walls of text)", note: "Evidence note here" },
        { status: "pass", label: "Bullet points used for features or benefits", note: "Evidence note here" },
        { status: "warn", label: "No generic filler opening paragraph", note: "Evidence note here" }
      ]
    },
    {
      name: "Entity & Fact Signal",
      score: 0,
      pass: 0, warn: 0, fail: 0, manual: 0,
      checks: [
        { status: "pass", label: "Brand name mentioned 5 or more times", note: "Evidence note here" },
        { status: "pass", label: "3+ specific numbers or stats", note: "Evidence note here" },
        { status: "pass", label: "Comparison language present", note: "Evidence note here" },
        { status: "pass", label: "Named service offerings consistently styled", note: "Evidence note here" },
        { status: "pass", label: "Pricing shown on page or link to /pricing page", note: "Evidence note here" }
      ]
    },
    {
      name: "Trust & Authority Signals",
      score: 0,
      pass: 0, warn: 0, fail: 0, manual: 0,
      checks: [
        { status: "pass", label: "Client testimonials or customer quotes", note: "Evidence note here" },
        { status: "pass", label: "Client logos or partner badges", note: "Evidence note here" },
        { status: "fail", label: "Specific measurable outcomes ('reduced X by Y%')", note: "Evidence note here" },
        { status: "pass", label: "3+ external links to credible sources", note: "Evidence note here" }
      ]
    },
    {
      name: "FAQ & Schema Signals",
      score: 0,
      pass: 0, warn: 0, fail: 0, manual: 0,
      checks: [
        { status: "pass", label: "FAQ section with question-phrased H2/H3 headings", note: "Evidence note here" },
        { status: "fail", label: "JSON-LD Service or ProfessionalService schema", note: "Evidence note here" },
        { status: "pass", label: "JSON-LD FAQPage schema", note: "Evidence note here" },
        { status: "pass", label: "Meta title accurately describes the service", note: "Evidence note here" },
        { status: "pass", label: "Canonical URL correctly set", note: "Evidence note here" }
      ]
    },
    {
      name: "Semantic Answer Coverage",
      score: 0,
      pass: 0, warn: 0, fail: 0, manual: 0,
      checks: [
        { status: "pass", label: "What — service clearly explained", note: "Evidence note here" },
        { status: "pass", label: "Who — ideal customer identified", note: "Evidence note here" },
        { status: "pass", label: "How — delivery process or workflow described", note: "Evidence note here" },
        { status: "pass", label: "Why — differentiation vs. alternatives stated", note: "Evidence note here" },
        { status: "pass", label: "How much — pricing or budget range mentioned", note: "Evidence note here" }
      ]
    },
    {
      name: "Internal Linking & Context Graph",
      score: 0,
      pass: 0, warn: 0, fail: 0, manual: 0,
      checks: [
        { status: "pass", label: "10+ contextual internal links", note: "Evidence note here" },
        { status: "pass", label: "Related services or blog/resource content linked", note: "Evidence note here" },
        { status: "fail", label: "Breadcrumb navigation (with BreadcrumbList schema)", note: "Evidence note here" },
        { status: "pass", label: "Key service terms link to dedicated pages", note: "Evidence note here" },
        { status: "warn", label: "Comparison table present (tiers, packages, or vs. alternatives)", note: "Evidence note here" }
      ]
    },
    {
      name: "Content Richness & Multimodal",
      score: 0,
      pass: 0, warn: 0, fail: 0, manual: 0,
      checks: [
        { status: "pass", label: "Process or workflow steps defined", note: "Evidence note here" },
        { status: "warn", label: "Images with descriptive alt text", note: "Evidence note here" },
        { status: "fail", label: "Page listed in llms.txt", note: "Evidence note here" }
      ]
    },
    {
      name: "Freshness & Maintenance Signals",
      score: 0,
      pass: 0, warn: 0, fail: 0, manual: 0,
      checks: [
        { status: "warn", label: "Content reviewed/updated within last 6 months", note: "Evidence note here" },
        { status: "fail", label: "'Last updated' date visible on page", note: "Evidence note here" },
        { status: "manual", label: "Outdated stats, prices, or claims removed", note: "Requires manual review" },
        { status: "warn", label: "Changelog or version history present", note: "Evidence note here" }
      ]
    },
    {
      name: "Crawlability & Technical",
      score: 0,
      pass: 0, warn: 0, fail: 0, manual: 0,
      checks: [
        { status: "pass", label: "Page found in XML sitemap", note: "Evidence note here" },
        { status: "pass", label: "Sitemap lastmod within last 6 months", note: "Evidence note here" },
        { status: "warn", label: "Server response under 500ms", note: "Evidence note here" },
        { status: "pass", label: "AI crawlers allowed in robots.txt (GPTBot, ClaudeBot, PerplexityBot)", note: "Evidence note here" },
        { status: "pass", label: "Page is indexable (no noindex)", note: "Evidence note here" },
        { status: "pass", label: "AI crawler path not restricted for this URL", note: "Evidence note here" },
        { status: "pass", label: "Page content readable without JavaScript", note: "Evidence note here" }
      ]
    }
  ],
  topFixes: [
    { priority: 1, impact: "high",   category: "Category Name", fix: "Fix title here", detail: "One sentence explaining the fix and its impact." },
    { priority: 2, impact: "high",   category: "Category Name", fix: "Fix title here", detail: "One sentence explaining the fix and its impact." },
    { priority: 3, impact: "high",   category: "Category Name", fix: "Fix title here", detail: "One sentence explaining the fix and its impact." },
    { priority: 4, impact: "medium", category: "Category Name", fix: "Fix title here", detail: "One sentence explaining the fix and its impact." },
    { priority: 5, impact: "medium", category: "Category Name", fix: "Fix title here", detail: "One sentence explaining the fix and its impact." },
    { priority: 6, impact: "medium", category: "Category Name", fix: "Fix title here", detail: "One sentence explaining the fix and its impact." },
    { priority: 7, impact: "medium", category: "Category Name", fix: "Fix title here", detail: "One sentence explaining the fix and its impact." },
    { priority: 8, impact: "low",    category: "Category Name", fix: "Fix title here", detail: "One sentence explaining the fix and its impact." },
    { priority: 9, impact: "low",    category: "Category Name", fix: "Fix title here", detail: "One sentence explaining the fix and its impact." },
    { priority: 10, impact: "low",   category: "Category Name", fix: "Fix title here", detail: "One sentence explaining the fix and its impact." }
  ]
};
// ─────────────────────────────────────────────────────────────

// ── Score colour ──────────────────────────────────────────────
function scoreColor(s) {
  if (s >= 80) return { text: 'color-green', bar: 'bar-green', hex: '#22C55E' };
  if (s >= 60) return { text: 'color-amber', bar: 'bar-amber', hex: '#F59E0B' };
  return { text: 'color-red', bar: 'bar-red', hex: '#EF4444' };
}

// ── Gauge ─────────────────────────────────────────────────────
function renderGauge() {
  const r = 52, circ = 2 * Math.PI * r; // ≈ 326.73
  const fill = document.getElementById('gauge-fill');
  const { hex } = scoreColor(AUDIT_DATA.overallScore);
  const pct = AUDIT_DATA.overallScore / 100;
  fill.setAttribute('stroke', hex);
  fill.setAttribute('stroke-dasharray', `${pct * circ} ${circ}`);
  const num = document.getElementById('score-num');
  num.textContent = AUDIT_DATA.overallScore;
  num.className = 'score-num ' + scoreColor(AUDIT_DATA.overallScore).text;
}

// ── Hero ──────────────────────────────────────────────────────
function renderHero() {
  document.getElementById('hero-url').textContent = AUDIT_DATA.url;
  document.getElementById('hero-date').textContent = 'Audited ' + AUDIT_DATA.date;
  const counts = document.getElementById('hero-counts');
  counts.innerHTML = `
    <span class="count-pill pass"><span class="count-dot"></span>${AUDIT_DATA.pass} pass</span>
    <span class="count-pill warn"><span class="count-dot"></span>${AUDIT_DATA.warn} warn</span>
    <span class="count-pill fail"><span class="count-dot"></span>${AUDIT_DATA.fail} fail</span>
    <span class="count-pill manual"><span class="count-dot"></span>${AUDIT_DATA.manual} manual</span>
  `;
}

// ── Category grid ─────────────────────────────────────────────
function renderCatGrid() {
  const grid = document.getElementById('cat-grid');
  AUDIT_DATA.categories.forEach((cat, i) => {
    const { text, bar } = scoreColor(cat.score);
    const card = document.createElement('div');
    card.className = 'cat-card';
    card.dataset.idx = i;
    card.innerHTML = `
      <div class="cat-card-top">
        <div class="cat-name">${cat.name}</div>
        <div class="cat-score-badge ${text}">${cat.score}</div>
      </div>
      <div class="cat-bar-track">
        <div class="cat-bar-fill ${bar}" style="width:${cat.score}%"></div>
      </div>
      <div class="cat-mini-counts">
        ${cat.pass   ? `<span class="cat-mini p"><span>${cat.pass}</span> pass</span>` : ''}
        ${cat.warn   ? `<span class="cat-mini w"><span>${cat.warn}</span> warn</span>` : ''}
        ${cat.fail   ? `<span class="cat-mini f"><span>${cat.fail}</span> fail</span>` : ''}
        ${cat.manual ? `<span class="cat-mini m"><span>${cat.manual}</span> manual</span>` : ''}
      </div>
    `;
    card.addEventListener('click', () => scrollToSection(i));
    grid.appendChild(card);
  });
}

// ── Detailed checks ───────────────────────────────────────────
function iconFor(status) {
  if (status === 'pass')   return { cls: 'icon-pass',   sym: '✓' };
  if (status === 'warn')   return { cls: 'icon-warn',   sym: '!' };
  if (status === 'fail')   return { cls: 'icon-fail',   sym: '✗' };
  return { cls: 'icon-manual', sym: '○' };
}

function renderChecks() {
  const wrapper = document.getElementById('checks-wrapper');
  AUDIT_DATA.categories.forEach((cat, i) => {
    const { text } = scoreColor(cat.score);
    const section = document.createElement('div');
    section.className = 'checks-section';
    section.id = `section-${i}`;

    const checksHtml = cat.checks.map(c => {
      const { cls, sym } = iconFor(c.status);
      return `
        <div class="check-row">
          <div class="check-icon ${cls}">${sym}</div>
          <div class="check-content">
            <div class="check-label">${c.label}</div>
            <div class="check-note">${c.note}</div>
          </div>
        </div>`;
    }).join('');

    section.innerHTML = `
      <div class="checks-section-header">
        <div class="checks-section-title">${i + 1}. ${cat.name}</div>
        <div class="checks-section-right">
          <div class="checks-section-score ${text}">${cat.score}/100</div>
          <svg class="chevron" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="6 9 12 15 18 9"/>
          </svg>
        </div>
      </div>
      <div class="checks-body">${checksHtml}</div>
    `;

    section.querySelector('.checks-section-header').addEventListener('click', () => {
      section.classList.toggle('open');
    });
    wrapper.appendChild(section);
  });
}

// ── Top fixes ─────────────────────────────────────────────────
function renderFixes() {
  const list = document.getElementById('fixes-list');
  AUDIT_DATA.topFixes.forEach(f => {
    const card = document.createElement('div');
    card.className = 'fix-card';
    card.innerHTML = `
      <div class="fix-priority">P${f.priority}</div>
      <div class="fix-body">
        <div class="fix-top">
          <div class="fix-title">${f.fix}</div>
          <div class="fix-tags">
            <span class="fix-tag ${f.impact}">${f.impact.charAt(0).toUpperCase() + f.impact.slice(1)} impact</span>
            <span class="fix-tag">${f.category}</span>
          </div>
        </div>
        <div class="fix-detail">${f.detail}</div>
      </div>
    `;
    list.appendChild(card);
  });
}

// ── Footer ────────────────────────────────────────────────────
function renderFooter() {
  document.getElementById('footer-note').textContent =
    `${AUDIT_DATA.totalChecks} checks · ${AUDIT_DATA.scoreable} scored · ${AUDIT_DATA.date}`;
}

// ── Scroll helper ─────────────────────────────────────────────
function scrollToSection(i) {
  const el = document.getElementById(`section-${i}`);
  if (el) {
    el.classList.add('open');
    el.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
}

// ── Init ──────────────────────────────────────────────────────
document.title = `Landing Page Audit — ${AUDIT_DATA.domain}`;
renderHero();
renderGauge();
renderCatGrid();
renderChecks();
renderFixes();
renderFooter();
</script>
</body>
</html>
```

---

## Variable Reference

Every value that Claude must fill into `AUDIT_DATA`:

| Field | Type | Example |
|---|---|---|
| `url` | string | `"https://infrasity.com/claude-skills"` |
| `domain` | string | `"infrasity.com"` |
| `date` | string | `"June 16, 2026"` |
| `overallScore` | integer 0–100 | `75` |
| `scoreable` | integer | `47` (48 minus manual count) |
| `pass` | integer | `32` |
| `warn` | integer | `6` |
| `fail` | integer | `9` |
| `manual` | integer | `1` |
| `categories[n].score` | integer 0–100 | `60` |
| `categories[n].pass` | integer | `3` |
| `categories[n].warn` | integer | `0` |
| `categories[n].fail` | integer | `2` |
| `categories[n].manual` | integer | `0` |
| `categories[n].checks[m].status` | `"pass"`, `"warn"`, `"fail"`, or `"manual"` | `"fail"` |
| `categories[n].checks[m].note` | string, 1 sentence | `"Definition appears after CTA buttons, past 100-word mark"` |
| `topFixes[n].impact` | `"high"`, `"medium"`, or `"low"` | `"high"` |
| `topFixes[n].category` | string | `"Content Richness & Multimodal"` |
| `topFixes[n].fix` | string | `"Add /claude-skills to llms.txt"` |
| `topFixes[n].detail` | string, 1 sentence | `"Page URL missing from llms.txt — invisible to LLM crawlers that use it"` |

## Score Colour Rules

The `scoreColor()` function in the template handles colouring automatically:
- 80–100 → green (`#22C55E`)
- 60–79 → amber (`#F59E0B`)
- 0–59  → red (`#EF4444`)

This applies to: overall score gauge, category score badges, category score bars, and per-section scores.

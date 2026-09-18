# Docs Audit Report — Widget Template

Use this template when rendering the audit report via `show_widget`. Copy the structure
and substitute real audit data. Always call `read_me` with `["mockup", "data_viz"]` first.

---

## Score color rules

| Score | Circle border color |
|-------|-------------------|
| 80–100 | `#639922` (green) |
| 60–79 | `#BA7517` (amber) |
| 0–59 | `#E24B4A` (red) |

---

## Full HTML template

```html
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
.wrap { padding: 1.5rem 0; }
.score-hero { display: flex; align-items: center; gap: 24px; padding: 1.25rem 1.5rem; background: var(--color-background-secondary); border-radius: var(--border-radius-lg); margin-bottom: 1.5rem; }
.score-circle { width: 80px; height: 80px; border-radius: 50%; border: 3px solid {SCORE_COLOR}; display: flex; flex-direction: column; align-items: center; justify-content: center; flex-shrink: 0; }
.score-num { font-size: 26px; font-weight: 500; color: var(--color-text-primary); line-height: 1; }
.score-denom { font-size: 12px; color: var(--color-text-secondary); }
.score-meta { flex: 1; }
.score-title { font-size: 17px; font-weight: 500; color: var(--color-text-primary); margin-bottom: 4px; }
.score-sub { font-size: 13px; color: var(--color-text-secondary); line-height: 1.6; }
.legend { display: flex; gap: 16px; margin-bottom: 1.25rem; flex-wrap: wrap; }
.leg { display: flex; align-items: center; gap: 6px; font-size: 12px; color: var(--color-text-secondary); }
.dot { width: 10px; height: 10px; border-radius: 50%; }
.dot-pass { background: #639922; }
.dot-warn { background: #BA7517; }
.dot-fail { background: #E24B4A; }
.category { margin-bottom: 1.25rem; border: 0.5px solid var(--color-border-tertiary); border-radius: var(--border-radius-lg); overflow: hidden; }
.cat-header { display: flex; align-items: center; justify-content: space-between; padding: 0.75rem 1rem; background: var(--color-background-secondary); }
.cat-left { display: flex; align-items: center; gap: 10px; }
.cat-name { font-size: 14px; font-weight: 500; color: var(--color-text-primary); }
.cat-score { font-size: 12px; color: var(--color-text-secondary); }
.cat-pills { display: flex; gap: 6px; flex-wrap: wrap; }
.pill { font-size: 11px; padding: 2px 8px; border-radius: 99px; font-weight: 500; }
.pill-pass { background: #EAF3DE; color: #27500A; }
.pill-warn { background: #FAEEDA; color: #633806; }
.pill-fail { background: #FCEBEB; color: #791F1F; }
.checks { padding: 0; }
.check-row { display: flex; align-items: flex-start; gap: 10px; padding: 0.6rem 1rem; border-top: 0.5px solid var(--color-border-tertiary); }
.check-icon { flex-shrink: 0; width: 18px; height: 18px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-top: 1px; font-size: 10px; font-weight: 700; }
.icon-pass { background: #EAF3DE; color: #3B6D11; }
.icon-warn { background: #FAEEDA; color: #854F0B; }
.icon-fail { background: #FCEBEB; color: #A32D2D; }
.check-text { flex: 1; }
.check-label { font-size: 13px; color: var(--color-text-primary); line-height: 1.4; }
.check-note { font-size: 12px; color: var(--color-text-secondary); margin-top: 2px; line-height: 1.4; }
</style>

<div class="wrap">
  <h2 class="sr-only">Docs audit report for {DOMAIN}</h2>

  <div class="score-hero">
    <div class="score-circle">
      <span class="score-num">{SCORE}</span>
      <span class="score-denom">/100</span>
    </div>
    <div class="score-meta">
      <div class="score-title">{DOMAIN} — {SITE_TITLE}</div>
      <div class="score-sub">
        {PASS_COUNT} pass &nbsp;·&nbsp; {WARN_COUNT} warn &nbsp;·&nbsp; {FAIL_COUNT} fail &nbsp;·&nbsp; 33 total checks<br>
        Strongest: {STRONGEST_CATEGORY} &nbsp;·&nbsp; Weakest: {WEAKEST_CATEGORY}
      </div>
    </div>
  </div>

  <div class="legend">
    <span class="leg"><span class="dot dot-pass"></span>Pass</span>
    <span class="leg"><span class="dot dot-warn"></span>Warn</span>
    <span class="leg"><span class="dot dot-fail"></span>Fail</span>
  </div>

  <div id="cats"></div>
</div>

<script>
const categories = [
  {
    name: "1. AI & LLM Discoverability",
    score: "X/5",
    checks: [
      { status: "pass|warn|fail", label: "llms.txt present at root domain", note: "Evidence note here" },
      { status: "pass|warn|fail", label: "llms-full.txt present", note: "Evidence note here" },
      { status: "pass|warn|fail", label: "Docs pages listed in llms.txt", note: "Evidence note here" },
      { status: "pass|warn|fail", label: "AI bots allowed in robots.txt", note: "Evidence note here" },
      { status: "pass|warn|fail", label: "Docs pages in sitemap.xml", note: "Evidence note here" },
    ]
  },
  {
    name: "2. Structure & Navigation",
    score: "X/6",
    checks: [
      { status: "pass|warn|fail", label: "Introduction / overview page with real content", note: "" },
      { status: "pass|warn|fail", label: "Quickstart / Getting Started with actionable steps", note: "" },
      { status: "pass|warn|fail", label: "API Reference / Reference section present", note: "" },
      { status: "pass|warn|fail", label: "Sidebar / navigation menu present", note: "" },
      { status: "pass|warn|fail", label: "Breadcrumb navigation present", note: "" },
      { status: "pass|warn|fail", label: "Search functionality present", note: "" },
    ]
  },
  {
    name: "3. Content Completeness",
    score: "X/6",
    checks: [
      { status: "pass|warn|fail", label: "Use cases / tutorials / examples section present", note: "" },
      { status: "pass|warn|fail", label: "Code examples present", note: "" },
      { status: "pass|warn|fail", label: "Multiple language examples (Python, JS, cURL, etc.)", note: "" },
      { status: "pass|warn|fail", label: "Changelog / Release notes present", note: "" },
      { status: "pass|warn|fail", label: "FAQ / Troubleshooting section present", note: "" },
      { status: "pass|warn|fail", label: "Error messages / status codes documented", note: "" },
    ]
  },
  {
    name: "4. Content Quality",
    score: "X/3",
    checks: [
      { status: "pass|warn|fail", label: "Intro page explains what the product is and who it's for", note: "" },
      { status: "pass|warn|fail", label: "Quickstart gets user to a working state", note: "" },
      { status: "pass|warn|fail", label: "Sampled pages have sufficient depth (not stubs)", note: "" },
    ]
  },
  {
    name: "5. Technical SEO & Crawlability",
    score: "X/5",
    checks: [
      { status: "pass|warn|fail", label: "HTTPS enforced", note: "" },
      { status: "pass|warn|fail", label: "Meta titles present on docs pages", note: "" },
      { status: "pass|warn|fail", label: "Meta descriptions present on docs pages", note: "" },
      { status: "pass|warn|fail", label: "Canonical URLs present and correct", note: "" },
      { status: "pass|warn|fail", label: "No noindex directives on docs pages", note: "" },
    ]
  },
  {
    name: "6. Internal Linking & Flow",
    score: "X/4",
    checks: [
      { status: "pass|warn|fail", label: "Docs pages cross-link to each other", note: "" },
      { status: "pass|warn|fail", label: "Next / previous page navigation present", note: "" },
      { status: "pass|warn|fail", label: "Links to GitHub / source code", note: "" },
      { status: "pass|warn|fail", label: "Community / support links present", note: "" },
    ]
  },
  {
    name: "7. Versioning & Maintenance",
    score: "X/4",
    checks: [
      { status: "pass|warn|fail", label: "Version indicator visible", note: "" },
      { status: "pass|warn|fail", label: "Last updated / freshness signal on pages", note: "" },
      { status: "pass|warn|fail", label: "Install commands include version pinning", note: "" },
      { status: "pass|warn|fail", label: "Deprecation notices present (if multi-version)", note: "" },
    ]
  }
];

const iconMap = { pass: "✓", warn: "!", fail: "✗" };
const iconClass = { pass: "icon-pass", warn: "icon-warn", fail: "icon-fail" };
const pillClass = { pass: "pill-pass", warn: "pill-warn", fail: "pill-fail" };
const container = document.getElementById("cats");

categories.forEach(cat => {
  const passCount = cat.checks.filter(c => c.status === "pass").length;
  const warnCount = cat.checks.filter(c => c.status === "warn").length;
  const failCount = cat.checks.filter(c => c.status === "fail").length;
  const el = document.createElement("div");
  el.className = "category";
  const checksHTML = cat.checks.map(c => `
    <div class="check-row">
      <div class="check-icon ${iconClass[c.status]}">${iconMap[c.status]}</div>
      <div class="check-text">
        <div class="check-label">${c.label}</div>
        <div class="check-note">${c.note}</div>
      </div>
    </div>
  `).join("");
  const pillsHTML = [
    passCount ? `<span class="pill pill-pass">${passCount} pass</span>` : "",
    warnCount ? `<span class="pill pill-warn">${warnCount} warn</span>` : "",
    failCount ? `<span class="pill pill-fail">${failCount} fail</span>` : "",
  ].join("");
  el.innerHTML = `
    <div class="cat-header">
      <div class="cat-left">
        <span class="cat-name">${cat.name}</span>
        <span class="cat-score">${cat.score}</span>
      </div>
      <div class="cat-pills">${pillsHTML}</div>
    </div>
    <div class="checks">${checksHTML}</div>
  `;
  container.appendChild(el);
});
</script>
```

---

## Scoring helper

```
Category max points = 100 / 7 = 14.286

Points per check (within category):
  pass = (category_max / num_checks_in_category)
  warn = (category_max / num_checks_in_category) / 2
  fail = 0

Final score = round(sum of all category points)
```

Example: Category 1 has 5 checks → each check worth 14.286/5 = 2.857 pts.
3 pass + 1 warn + 1 fail = (3 × 2.857) + (1 × 1.429) + 0 = 9.999 ≈ 10 pts for that category.
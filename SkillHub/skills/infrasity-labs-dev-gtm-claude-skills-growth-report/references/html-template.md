# HTML Report Template Reference — Infrasity Brand Design

This file contains the complete Infrasity-branded HTML template for the SEO Performance Report.
Replace all `{{VARIABLE}}` placeholders with real data from the DataForSEO API calls.

**Design system:** Infrasity brand v1 — `#0D0A1A` background · `#8157F2` purple accent ·
Instrument Sans + DM Sans + DM Mono. No other colour palette or font stack is permitted.

---

## Variable Reference

| Variable | Source |
|---|---|
| `{{TARGET_DOMAIN}}` | User input |
| `{{START_DATE}}` | User input (e.g. Feb 20, 2026) |
| `{{END_DATE}}` | User input (e.g. May 20, 2026) |
| `{{BASELINE_TRAFFIC}}` | Step 1: historical etv, formatted with commas |
| `{{BASELINE_KEYWORDS}}` | Step 1: historical count, formatted with commas |
| `{{BASELINE_TOP3}}` | Step 1: pos_1 + pos_2_3, formatted with commas |
| `{{BASELINE_RANK}}` | Step 3: competitive rank at baseline period |
| `{{CURRENT_TRAFFIC}}` | Step 2: current etv, formatted with commas |
| `{{CURRENT_KEYWORDS}}` | Step 2: current count, formatted with commas |
| `{{CURRENT_TOP3}}` | Step 2: pos_1 + pos_2_3 |
| `{{CURRENT_COMP_RANK}}` | Step 3: rank in sorted competitive table |
| `{{TOTAL_COMPETITORS}}` | Count of all domains including target |
| `{{TRAFFIC_GROWTH_PCT}}` | Step 2 calc: formatted like "+36.2%" or "-31.4%" |
| `{{TRAFFIC_GROWTH_CLASS}}` | "pos" if positive, "neg" if negative |
| `{{KEYWORDS_CHANGE}}` | Step 2 calc: e.g. "-1,147" or "+523" |
| `{{KEYWORDS_CHANGE_PCT}}` | Step 2 calc: e.g. "-50.1%" |
| `{{KEYWORDS_CHANGE_CLASS}}` | "pos" or "neg" |
| `{{TOP3_GROWTH_PCT}}` | Step 2 calc: e.g. "+28.9%" |
| `{{TOP3_GROWTH_CLASS}}` | "pos" or "neg" |
| `{{TARGET_GOAL_TRAFFIC}}` | Step 5 derived target |
| `{{TARGET_GOAL_KEYWORDS}}` | Step 5 derived target |
| `{{TARGET_GOAL_TOP3}}` | Step 5 derived target |
| `{{TARGET_BADGE_TEXT}}` | e.g. "Challenge #2" or "Maintain #1" |
| `{{COMP_TABLE_ROWS}}` | Step 3: HTML `<tr>` rows for all domains |
| `{{MARKET_INSIGHT_TEXT}}` | Step 3: 2–3 sentence market insight paragraph |
| `{{BIG_STAT_VAL}}` | e.g. "+36.2%" — the hero traffic growth number |
| `{{BIG_STAT_CLASS}}` | "green" if positive, "red" if negative |
| `{{GAP_TO_NEXT}}` | Step 3: etv gap to competitor one rank above |
| `{{NEXT_ABOVE_DOMAIN}}` | Domain ranked one above target |
| `{{LEAD_BELOW_DOMAIN}}` | Domain ranked one below target |
| `{{LEAD_OVER_BELOW}}` | etv lead over competitor one rank below |
| `{{TREND_LABEL_1}}` | Month label for trend bar 1 (e.g. "Feb 2026") |
| `{{TREND_ETV_1}}` | ETV value for trend bar 1 |
| `{{TREND_BAR_WIDTH_1}}` | Width % for trend bar 1 (highest month = 100%) |
| `{{TREND_LABEL_2}}` | Month label for trend bar 2 |
| `{{TREND_ETV_2}}` | ETV value for trend bar 2 |
| `{{TREND_BAR_WIDTH_2}}` | Width % for trend bar 2 |
| `{{TREND_LABEL_3}}` | Month label for trend bar 3 |
| `{{TREND_ETV_3}}` | ETV value for trend bar 3 |
| `{{TREND_BAR_WIDTH_3}}` | Width % for trend bar 3 |
| `{{TREND_LABEL_4}}` | Month label for trend bar 4 |
| `{{TREND_ETV_4}}` | ETV value for trend bar 4 |
| `{{TREND_BAR_WIDTH_4}}` | Width % for trend bar 4 |
| `{{KW_POS_1}}` | Step 2: pos_1 count |
| `{{KW_POS_2_3}}` | Step 2: pos_2_3 count |
| `{{KW_POS_4_10}}` | Step 2: pos_4_10 count |
| `{{KW_POS_11_20}}` | Step 2: pos_11_20 count |
| `{{KW_POS_21_100}}` | Step 2: sum pos_21_30 through pos_91_100 |
| `{{PAGE1_URL}}` | Step 4: top page address (strip https://www.) |
| `{{PAGE1_ETV}}` | Step 4: top page etv |
| `{{PAGE1_KW}}` | Step 4: top page keyword count |
| `{{PAGE2_URL}}` | Step 4: second page address |
| `{{PAGE2_ETV}}` | Step 4: second page etv |
| `{{PAGE2_KW}}` | Step 4: second page keyword count |
| `{{PAGE3_URL}}` | Step 4: third page address |
| `{{PAGE3_ETV}}` | Step 4: third page etv |
| `{{PAGE3_KW}}` | Step 4: third page keyword count |
| `{{STRAT_1_NUM_LABEL}}` | Label for strategy card 1 (e.g. "Close Gap") |
| `{{STRAT_1_TITLE}}` | Strategic priority 1 title |
| `{{STRAT_1_DESC}}` | Strategic priority 1 description |
| `{{STRAT_2_NUM_LABEL}}` | Label for strategy card 2 |
| `{{STRAT_2_TITLE}}` | Strategic priority 2 title |
| `{{STRAT_2_DESC}}` | Strategic priority 2 description |
| `{{STRAT_3_NUM_LABEL}}` | Label for strategy card 3 |
| `{{STRAT_3_TITLE}}` | Strategic priority 3 title |
| `{{STRAT_3_DESC}}` | Strategic priority 3 description |
| `{{STRAT_4_NUM_LABEL}}` | Label for strategy card 4 |
| `{{STRAT_4_TITLE}}` | Strategic priority 4 title |
| `{{STRAT_4_DESC}}` | Strategic priority 4 description |
| `{{STRAT_5_NUM_LABEL}}` | Label for strategy card 5 |
| `{{STRAT_5_TITLE}}` | Strategic priority 5 title |
| `{{STRAT_5_DESC}}` | Strategic priority 5 description |
| `{{STRAT_6_NUM_LABEL}}` | Label for strategy card 6 |
| `{{STRAT_6_TITLE}}` | Strategic priority 6 title |
| `{{STRAT_6_DESC}}` | Strategic priority 6 description |
| `{{EXEC_PARA_1}}` | Executive summary paragraph 1 |
| `{{EXEC_PARA_2}}` | Executive summary paragraph 2 |
| `{{EXEC_PARA_3}}` | Executive summary paragraph 3 |
| `{{EXEC_PARA_4}}` | Executive summary paragraph 4 |
| `{{EXEC_BADGE_TEXT}}` | Summary badge text |
| `{{COMP_TABLE_LABEL}}` | "X of Y" competitive position label |
| `{{FASTEST_GROWING_COLOR}}` | CSS colour for fastest growing label (`var(--up)` or `var(--text-3)`) |
| `{{FASTEST_GROWING_LABEL}}` | Text label for the fastest growing domain |
| `{{RANK_ABOVE}}` | Rank number of the competitor immediately above |
| `{{COMP_DOMAIN_LIST}}` | Comma-separated list of all domains in the set |

---

## Trend Bar Width Calculation

```
max_etv       = highest ETV value across the 4 monthly data points
width_pct_N   = round((etv_N / max_etv) * 100)
```
Minimum width = 10% so labels are always visible.

---

## Competitive Table Row Template

CSS classes used in the table rows — match exactly:

```html
<!-- Target domain row (highlighted): -->
<tr class="hl">
  <td><span class="rank-badge rank-N">N</span></td>
  <td><span class="dname me">🔥 {{TARGET_DOMAIN}}</span></td>
  <td><span class="mono">{{ETV_FORMATTED}}</span></td>
  <td><span class="mono">{{KW_COUNT_FORMATTED}}</span></td>
  <td><span class="tbadge t-up">↑ +XX%</span></td>
</tr>

<!-- Competitor row: -->
<tr>
  <td><span class="rank-badge rank-N">N</span></td>
  <td><span class="dname">{{DOMAIN}}</span></td>
  <td><span class="mono">{{ETV_FORMATTED}}</span></td>
  <td><span class="mono">{{KW_COUNT_FORMATTED}}</span></td>
  <td><span class="tbadge t-stable">→ Stable</span></td>
</tr>
```

**Rank badge classes:** `rank-1` (red), `rank-2` (gold), `rank-3` (purple), `rank-other` (gray).
**Trend badge classes:** `t-up` (green `#5DCEA6`), `t-dn` (red `#F07070`), `t-stable` (muted gray).

---

## Infrasity Design Pre-fill Checklist

Before writing the HTML, confirm every item:

- [ ] Background is `#0D0A1A` — not black, not navy, not any other dark
- [ ] Primary accent is `#8157F2` only — never blue, teal, or any other colour
- [ ] `Instrument Sans` on all headings, KPI values, section numbers, badges
- [ ] `DM Sans` on all body copy, table cells, descriptions, labels
- [ ] `DM Mono` on all URL paths, ETV values in bars, footer data note
- [ ] All cards use `border-radius: 12px` and `var(--surface)` background
- [ ] Purple `rgba(129,87,242,0.35)` border appears on card hover
- [ ] Status chips: `#5DCEA6` (up/positive), `#F07070` (down/negative)
- [ ] Trend bars use `rgba(129,87,242,0.75)` fill; target domain bar uses `#8157F2`
- [ ] Table header: `rgba(129,87,242,0.06)` background · `rgba(129,87,242,0.80)` text
- [ ] No light-mode styles — this is a dark-only output
- [ ] Google Fonts loaded: Instrument Sans + DM Sans + DM Mono

---

## Full HTML Template

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{{TARGET_DOMAIN}} — SEO Performance Report</title>
<link href="https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@400;500;600;700&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;1,9..40,300&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
:root{
  --bg:#0D0A1A;
  --purple:#8157F2;
  --purple-deep:#6B3FD4;
  --purple-light:#EFE0FF;
  --surface:rgba(255,255,255,0.04);
  --surface-2:rgba(255,255,255,0.07);
  --surface-3:rgba(255,255,255,0.10);
  --border:rgba(255,255,255,0.08);
  --border-2:rgba(255,255,255,0.15);
  --border-purple:rgba(129,87,242,0.35);
  --text-1:#FFFFFF;
  --text-2:rgba(255,255,255,0.60);
  --text-3:rgba(255,255,255,0.30);
  --up:#5DCEA6;
  --up-bg:rgba(93,206,166,0.10);
  --dn:#F07070;
  --dn-bg:rgba(240,112,112,0.10);
  --head:'Instrument Sans',sans-serif;
  --body:'DM Sans',sans-serif;
  --mono:'DM Mono',monospace;
}
body{font-family:var(--body);background:var(--bg);color:var(--text-1);font-size:14px;line-height:1.5;-webkit-font-smoothing:antialiased}
.page{max-width:940px;margin:0 auto;padding:48px 28px 88px}

/* ── HEADER ─────────────────────────────────────── */
.hdr{text-align:center;padding:44px 0 40px}
.hdr-pill{display:inline-flex;align-items:center;gap:8px;background:rgba(129,87,242,0.08);border:1px solid rgba(129,87,242,0.22);border-radius:100px;padding:5px 16px;font-family:var(--head);font-size:10px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--purple-light);margin-bottom:22px}
.hdr-pill-dot{width:6px;height:6px;border-radius:50%;background:var(--purple);box-shadow:0 0 8px var(--purple);flex-shrink:0}
.hdr-title{font-family:var(--head);font-size:clamp(30px,4.5vw,46px);font-weight:700;line-height:1.12;margin-bottom:8px;letter-spacing:-.01em}
.hdr-title em{font-style:normal;color:var(--purple)}
.hdr-sub{color:var(--text-3);font-size:12px;font-family:var(--mono);letter-spacing:.02em}
.hdr-divider{width:64px;height:1px;background:rgba(129,87,242,0.30);margin:18px auto 0}

/* ── SECTION HEADER ─────────────────────────────── */
.sec-hdr{display:flex;align-items:center;gap:10px;margin:48px 0 18px}
.sec-dot{width:5px;height:5px;border-radius:50%;background:var(--purple);box-shadow:0 0 7px var(--purple);flex-shrink:0}
.sec-num{font-family:var(--head);font-size:10px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--purple)}
.sec-label{font-family:var(--head);font-size:19px;font-weight:600;color:var(--text-1)}

/* ── TIMELINE ───────────────────────────────────── */
.timeline{display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-bottom:48px;position:relative}
.timeline::before{content:'';position:absolute;top:44px;left:calc(33.33% - 4px);width:calc(33.33% + 8px);height:1px;background:rgba(129,87,242,0.25);z-index:0}
.tc{background:var(--surface);border:1px solid var(--border);border-radius:12px;padding:22px 20px;position:relative;z-index:1;transition:border-color .2s}
.tc:hover{border-color:var(--border-purple)}
.tc.live{background:rgba(129,87,242,0.07);border-color:var(--border-purple)}
.tc.live::after{content:'';position:absolute;inset:0;border-radius:12px;box-shadow:0 0 28px rgba(129,87,242,0.10);pointer-events:none}
.tc-top-bar{position:absolute;top:0;left:0;right:0;height:2px;border-radius:12px 12px 0 0;background:var(--purple);opacity:0}
.tc.live .tc-top-bar{opacity:1}
.tc-label{font-family:var(--head);font-size:9px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:var(--text-3);margin-bottom:4px}
.tc-period{font-family:var(--head);font-size:12px;font-weight:600;color:var(--text-2);margin-bottom:16px}
.tc-row{display:flex;justify-content:space-between;align-items:center;padding:7px 0;border-bottom:1px solid var(--border)}
.tc-row:last-of-type{border-bottom:none}
.tc-row-l{font-size:11px;color:var(--text-3);font-family:var(--body)}
.tc-row-v{font-family:var(--head);font-size:13px;font-weight:600;color:var(--text-1);display:flex;align-items:center;gap:5px}
.tc-badge{margin-top:14px;padding:5px 11px;border-radius:100px;font-size:10px;font-weight:700;font-family:var(--head);letter-spacing:.04em;text-align:center;border:1px solid rgba(129,87,242,0.22);background:rgba(129,87,242,0.08);color:var(--purple-light)}
.tc-badge.green{background:var(--up-bg);color:var(--up);border-color:rgba(93,206,166,0.22)}
.tc-badge.dim{background:rgba(255,255,255,0.03);color:var(--text-3);border-color:var(--border)}
/* delta chips inside tc-row-v */
.delta{font-size:10px;font-weight:600;padding:2px 7px;border-radius:100px;font-family:var(--head)}
.delta.pos{background:var(--up-bg);color:var(--up)}
.delta.neg{background:var(--dn-bg);color:var(--dn)}
.delta.na{background:rgba(255,255,255,0.04);color:var(--text-3);border:1px solid var(--border)}

/* ── COMPETITIVE TABLE ──────────────────────────── */
.comp-wrap{background:var(--surface);border:1px solid var(--border);border-radius:12px;overflow:hidden;margin-bottom:48px}
table{width:100%;border-collapse:collapse}
thead tr{background:rgba(129,87,242,0.06)}
th{padding:11px 18px;text-align:left;font-family:var(--head);font-size:10px;font-weight:700;letter-spacing:.09em;text-transform:uppercase;color:rgba(129,87,242,0.80);border-bottom:1px solid var(--border)}
td{padding:14px 18px;font-size:13px;border-bottom:1px solid var(--border);color:var(--text-2);font-family:var(--body)}
tbody tr:last-child td{border-bottom:none}
tbody tr:hover td{background:rgba(129,87,242,0.03)}
tr.hl td{background:rgba(129,87,242,0.05)}
/* rank badges */
.rank-badge{display:inline-flex;align-items:center;justify-content:center;width:24px;height:24px;border-radius:6px;font-family:var(--head);font-size:11px;font-weight:700}
.rank-1{background:rgba(240,112,112,0.12);color:var(--dn)}
.rank-2{background:rgba(255,185,50,0.10);color:#FFB932}
.rank-3{background:rgba(129,87,242,0.15);color:var(--purple-light)}
.rank-other{background:rgba(255,255,255,0.06);color:var(--text-3)}
/* domain names */
.dname{font-family:var(--head);font-size:13px;font-weight:600;color:var(--text-1)}
.dname.me{color:var(--purple)}
.mono{font-family:var(--mono);font-size:12px;color:var(--text-2)}
/* trend badges */
.tbadge{display:inline-flex;align-items:center;padding:3px 9px;border-radius:100px;font-size:10px;font-weight:700;font-family:var(--head);letter-spacing:.03em}
.t-up{background:var(--up-bg);color:var(--up)}
.t-dn{background:var(--dn-bg);color:var(--dn)}
.t-stable{background:rgba(255,255,255,0.05);color:var(--text-3);border:1px solid var(--border)}
.mkt-note{padding:16px 20px;border-top:1px solid var(--border);background:rgba(129,87,242,0.03)}
.mkt-note p{font-size:12px;color:var(--text-2);line-height:1.65}

/* ── TWO-COL ─────────────────────────────────────── */
.two-col{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-bottom:48px}
.card{background:var(--surface);border:1px solid var(--border);border-radius:12px;padding:22px 20px;transition:border-color .2s}
.card:hover{border-color:var(--border-purple)}
.card-ttl{font-family:var(--head);font-size:10px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--text-3);margin-bottom:14px}
/* hero stat */
.big-stat-val{font-family:var(--head);font-size:48px;font-weight:700;line-height:1;margin-bottom:4px}
.big-stat-val.green{color:var(--up)}
.big-stat-val.red{color:var(--dn)}
.big-stat-val.na{color:var(--text-3)}
.big-stat-label{font-size:11px;color:var(--text-3);font-family:var(--body);margin-bottom:18px;line-height:1.4}
/* stat rows */
.srow{display:flex;justify-content:space-between;align-items:center;padding:8px 0;border-bottom:1px solid var(--border)}
.srow:last-of-type{border-bottom:none}
.srow-l{font-size:12px;color:var(--text-3)}
.srow-v{font-family:var(--head);font-size:13px;font-weight:600;color:var(--text-1)}
/* content clusters */
.cluster{padding:10px 0;border-bottom:1px solid var(--border)}
.cluster:last-child{border-bottom:none}
.cluster-url{font-family:var(--mono);font-size:11px;color:var(--purple-light);margin-bottom:4px;word-break:break-all}
.cluster-meta{display:flex;gap:14px;font-size:11px;color:var(--text-3)}
.cluster-meta strong{color:var(--text-2);font-weight:500}
/* monthly trend bars */
.trend-row{margin-bottom:12px}
.trend-row:last-child{margin-bottom:0}
.trend-meta{display:flex;justify-content:space-between;align-items:center;margin-bottom:5px}
.trend-month{font-family:var(--head);font-size:11px;font-weight:600;color:var(--text-2)}
.trend-etv{font-family:var(--mono);font-size:11px;color:var(--text-3)}
.trend-track{height:10px;background:rgba(255,255,255,0.05);border-radius:100px;overflow:hidden}
.trend-bar{height:100%;border-radius:100px;background:rgba(129,87,242,0.55)}
/* keyword distribution */
.kw-dist{margin-top:2px}
.kw-row{display:flex;justify-content:space-between;align-items:center;padding:8px 0;border-bottom:1px solid var(--border)}
.kw-row:last-child{border-bottom:none}
.kw-label{font-size:12px;color:var(--text-3)}
.kw-val{font-family:var(--head);font-size:13px;font-weight:600;color:var(--text-1)}
.kw-val.hot{color:var(--up)}
.kw-val.warm{color:var(--purple-light)}

/* ── STRATEGIC PRIORITIES ───────────────────────── */
.strat-shell{background:var(--surface);border:1px solid var(--border);border-radius:12px;padding:26px 24px;margin-bottom:48px}
.strat-shell-hdr{display:flex;justify-content:space-between;align-items:center;margin-bottom:22px}
.strat-shell-ttl{font-family:var(--head);font-size:15px;font-weight:600;color:var(--text-1)}
.strat-period-chip{font-family:var(--head);font-size:10px;font-weight:700;padding:4px 12px;border-radius:100px;background:rgba(129,87,242,0.08);color:var(--purple-light);border:1px solid rgba(129,87,242,0.22);letter-spacing:.04em}
.strat-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}
.sc{background:rgba(255,255,255,0.03);border:1px solid var(--border);border-radius:10px;padding:18px 16px;transition:border-color .2s,background .2s}
.sc:hover{border-color:var(--border-purple);background:rgba(129,87,242,0.04)}
.sc-num{font-family:var(--head);font-size:9px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--purple);margin-bottom:7px}
.sc-title{font-family:var(--head);font-size:13px;font-weight:600;color:var(--text-1);margin-bottom:9px;line-height:1.3}
.sc-desc{font-size:12px;color:var(--text-2);line-height:1.6}

/* ── EXECUTIVE SUMMARY ──────────────────────────── */
.exec{background:rgba(129,87,242,0.05);border:1px solid rgba(129,87,242,0.18);border-radius:12px;padding:30px 28px;margin-bottom:48px}
.exec-title{display:flex;align-items:center;gap:9px;font-family:var(--head);font-size:15px;font-weight:600;color:var(--purple-light);margin-bottom:20px}
.exec-title::before{content:'';display:inline-block;width:5px;height:5px;border-radius:50%;background:var(--purple);box-shadow:0 0 7px var(--purple);flex-shrink:0}
.exec p{font-size:13px;color:var(--text-2);line-height:1.75;margin-bottom:14px}
.exec p:last-of-type{margin-bottom:22px}
.exec-badge{display:inline-block;background:rgba(129,87,242,0.10);border:1px solid rgba(129,87,242,0.28);border-radius:100px;padding:8px 20px;font-family:var(--head);font-size:11px;font-weight:700;color:var(--purple-light);letter-spacing:.04em}

/* ── FOOTER ─────────────────────────────────────── */
.footer{border-top:1px solid var(--border);padding:20px 0 0;text-align:center;font-family:var(--mono);font-size:11px;color:var(--text-3);line-height:1.7}

/* ── RESPONSIVE ─────────────────────────────────── */
@media(max-width:700px){
  .timeline{grid-template-columns:1fr}
  .timeline::before{display:none}
  .two-col{grid-template-columns:1fr}
  .strat-grid{grid-template-columns:1fr 1fr}
}
@media(max-width:460px){.strat-grid{grid-template-columns:1fr}}
</style>
</head>
<body>
<div class="page">

  <!-- ── HEADER ─────────────────────────────────── -->
  <div class="hdr">
    <div class="hdr-pill">
      <span class="hdr-pill-dot"></span>
      Infrasity &nbsp;·&nbsp; SEO Performance Report
    </div>
    <div class="hdr-title">Strategic Performance<br><em>{{TARGET_DOMAIN}}</em></div>
    <div class="hdr-sub">{{START_DATE}} → {{END_DATE}} &nbsp;·&nbsp; United States &nbsp;·&nbsp; Competitive Set: {{COMP_DOMAIN_LIST}}</div>
    <div class="hdr-divider"></div>
  </div>

  <!-- ── 01 PERFORMANCE TIMELINE ─────────────────── -->
  <div class="sec-hdr">
    <span class="sec-dot"></span>
    <span class="sec-num">01</span>
    <span class="sec-label">Performance Timeline</span>
  </div>
  <div class="timeline">

    <!-- Baseline card -->
    <div class="tc">
      <div class="tc-top-bar"></div>
      <div class="tc-label">Baseline</div>
      <div class="tc-period">{{START_DATE}}</div>
      <div class="tc-row">
        <span class="tc-row-l">Monthly Traffic</span>
        <span class="tc-row-v">{{BASELINE_TRAFFIC}}</span>
      </div>
      <div class="tc-row">
        <span class="tc-row-l">Organic Keywords</span>
        <span class="tc-row-v">{{BASELINE_KEYWORDS}}</span>
      </div>
      <div class="tc-row">
        <span class="tc-row-l">Top 3 Keywords</span>
        <span class="tc-row-v">{{BASELINE_TOP3}}</span>
      </div>
      <div class="tc-row">
        <span class="tc-row-l">Competitive Rank</span>
        <span class="tc-row-v">#{{BASELINE_RANK}}</span>
      </div>
      <div class="tc-badge dim">Baseline · {{START_DATE}}</div>
    </div>

    <!-- Current card (active / highlighted) -->
    <div class="tc live">
      <div class="tc-top-bar"></div>
      <div class="tc-label">Current State</div>
      <div class="tc-period">{{END_DATE}}</div>
      <div class="tc-row">
        <span class="tc-row-l">Monthly Traffic</span>
        <span class="tc-row-v">{{CURRENT_TRAFFIC}} <span class="delta {{TRAFFIC_GROWTH_CLASS}}">{{TRAFFIC_GROWTH_PCT}}</span></span>
      </div>
      <div class="tc-row">
        <span class="tc-row-l">Organic Keywords</span>
        <span class="tc-row-v">{{CURRENT_KEYWORDS}} <span class="delta {{KEYWORDS_CHANGE_CLASS}}">{{KEYWORDS_CHANGE_PCT}}</span></span>
      </div>
      <div class="tc-row">
        <span class="tc-row-l">Top 3 Keywords</span>
        <span class="tc-row-v">{{CURRENT_TOP3}} <span class="delta {{TOP3_GROWTH_CLASS}}">{{TOP3_GROWTH_PCT}}</span></span>
      </div>
      <div class="tc-row">
        <span class="tc-row-l">Competitive Rank</span>
        <span class="tc-row-v">#{{CURRENT_COMP_RANK}} of {{TOTAL_COMPETITORS}}</span>
      </div>
      <div class="tc-badge">Rank #{{CURRENT_COMP_RANK}} Overall</div>
    </div>

    <!-- Q2 target card -->
    <div class="tc">
      <div class="tc-top-bar"></div>
      <div class="tc-label">Q2 Target</div>
      <div class="tc-period">Where We're Going</div>
      <div class="tc-row">
        <span class="tc-row-l">Monthly Traffic</span>
        <span class="tc-row-v">{{TARGET_GOAL_TRAFFIC}}+</span>
      </div>
      <div class="tc-row">
        <span class="tc-row-l">Organic Keywords</span>
        <span class="tc-row-v">{{TARGET_GOAL_KEYWORDS}}+</span>
      </div>
      <div class="tc-row">
        <span class="tc-row-l">Top 3 Keywords</span>
        <span class="tc-row-v">{{TARGET_GOAL_TOP3}}+</span>
      </div>
      <div class="tc-row">
        <span class="tc-row-l">Target Position</span>
        <span class="tc-row-v">{{TARGET_BADGE_TEXT}}</span>
      </div>
      <div class="tc-badge green">Target: {{TARGET_BADGE_TEXT}}</div>
    </div>

  </div>

  <!-- ── 02 COMPETITIVE LANDSCAPE ─────────────────── -->
  <div class="sec-hdr">
    <span class="sec-dot"></span>
    <span class="sec-num">02</span>
    <span class="sec-label">Competitive Landscape</span>
  </div>
  <div class="comp-wrap">
    <table>
      <thead>
        <tr>
          <th>Rank</th>
          <th>Domain</th>
          <th>Monthly Traffic</th>
          <th>Keywords</th>
          <th>Q1 Trend</th>
        </tr>
      </thead>
      <tbody>
        {{COMP_TABLE_ROWS}}
      </tbody>
    </table>
    <div class="mkt-note">
      <p>{{MARKET_INSIGHT_TEXT}}</p>
    </div>
  </div>

  <!-- ── 03 TRAFFIC & CONTENT ──────────────────────── -->
  <div class="sec-hdr">
    <span class="sec-dot"></span>
    <span class="sec-num">03</span>
    <span class="sec-label">Traffic &amp; Content</span>
  </div>
  <div class="two-col">

    <!-- Left: Business Impact + Content Clusters -->
    <div class="card">
      <div class="card-ttl">Business Impact</div>
      <div class="big-stat-val {{BIG_STAT_CLASS}}">{{BIG_STAT_VAL}}</div>
      <div class="big-stat-label">Traffic change {{START_DATE}} → {{END_DATE}}</div>

      <div class="srow">
        <span class="srow-l">Competitive Position</span>
        <span class="srow-v">#{{CURRENT_COMP_RANK}} of {{TOTAL_COMPETITORS}}</span>
      </div>
      <div class="srow">
        <span class="srow-l">Fastest Growing in Set</span>
        <span class="srow-v" style="color:{{FASTEST_GROWING_COLOR}}">{{FASTEST_GROWING_LABEL}}</span>
      </div>
      <div class="srow" style="margin-bottom:20px">
        <span class="srow-l">Gap to Close (#{{RANK_ABOVE}})</span>
        <span class="srow-v" style="color:var(--dn)">{{GAP_TO_NEXT}} ETV</span>
      </div>

      <div class="card-ttl" style="margin-top:2px">Top Content Clusters</div>
      <div class="cluster">
        <div class="cluster-url">{{PAGE1_URL}}</div>
        <div class="cluster-meta"><span>ETV: <strong>{{PAGE1_ETV}}</strong></span><span>Keywords: <strong>{{PAGE1_KW}}</strong></span></div>
      </div>
      <div class="cluster">
        <div class="cluster-url">{{PAGE2_URL}}</div>
        <div class="cluster-meta"><span>ETV: <strong>{{PAGE2_ETV}}</strong></span><span>Keywords: <strong>{{PAGE2_KW}}</strong></span></div>
      </div>
      <div class="cluster">
        <div class="cluster-url">{{PAGE3_URL}}</div>
        <div class="cluster-meta"><span>ETV: <strong>{{PAGE3_ETV}}</strong></span><span>Keywords: <strong>{{PAGE3_KW}}</strong></span></div>
      </div>
    </div>

    <!-- Right: Monthly Trend Bars + Keyword Distribution -->
    <div class="card">
      <div class="card-ttl">Monthly Traffic Trend</div>
      <div class="trend-row">
        <div class="trend-meta">
          <span class="trend-month">{{TREND_LABEL_1}}</span>
          <span class="trend-etv">{{TREND_ETV_1}}</span>
        </div>
        <div class="trend-track"><div class="trend-bar" style="width:{{TREND_BAR_WIDTH_1}}%"></div></div>
      </div>
      <div class="trend-row">
        <div class="trend-meta">
          <span class="trend-month">{{TREND_LABEL_2}}</span>
          <span class="trend-etv">{{TREND_ETV_2}}</span>
        </div>
        <div class="trend-track"><div class="trend-bar" style="width:{{TREND_BAR_WIDTH_2}}%"></div></div>
      </div>
      <div class="trend-row">
        <div class="trend-meta">
          <span class="trend-month">{{TREND_LABEL_3}}</span>
          <span class="trend-etv">{{TREND_ETV_3}}</span>
        </div>
        <div class="trend-track"><div class="trend-bar" style="width:{{TREND_BAR_WIDTH_3}}%"></div></div>
      </div>
      <div class="trend-row" style="margin-bottom:22px">
        <div class="trend-meta">
          <span class="trend-month">{{TREND_LABEL_4}}</span>
          <span class="trend-etv">{{TREND_ETV_4}}</span>
        </div>
        <div class="trend-track"><div class="trend-bar" style="width:{{TREND_BAR_WIDTH_4}}%"></div></div>
      </div>

      <div class="card-ttl">Keyword Distribution (Current)</div>
      <div class="kw-dist">
        <div class="kw-row">
          <span class="kw-label">Position 1</span>
          <span class="kw-val">{{KW_POS_1}}</span>
        </div>
        <div class="kw-row">
          <span class="kw-label">Position 2–3</span>
          <span class="kw-val">{{KW_POS_2_3}}</span>
        </div>
        <div class="kw-row">
          <span class="kw-label">Position 4–10</span>
          <span class="kw-val hot">{{KW_POS_4_10}}</span>
        </div>
        <div class="kw-row">
          <span class="kw-label">Position 11–20</span>
          <span class="kw-val warm">{{KW_POS_11_20}}</span>
        </div>
        <div class="kw-row">
          <span class="kw-label">Position 21–100</span>
          <span class="kw-val">{{KW_POS_21_100}}</span>
        </div>
      </div>
    </div>

  </div>

  <!-- ── 04 STRATEGIC PRIORITIES ───────────────────── -->
  <div class="sec-hdr">
    <span class="sec-dot"></span>
    <span class="sec-num">04</span>
    <span class="sec-label">Q2 Strategic Priorities</span>
  </div>
  <div class="strat-shell">
    <div class="strat-shell-hdr">
      <div class="strat-shell-ttl">6 Data-Driven Actions</div>
      <div class="strat-period-chip">Q2 · {{END_DATE}}</div>
    </div>
    <div class="strat-grid">
      <div class="sc">
        <div class="sc-num">1. {{STRAT_1_NUM_LABEL}}</div>
        <div class="sc-title">{{STRAT_1_TITLE}}</div>
        <div class="sc-desc">{{STRAT_1_DESC}}</div>
      </div>
      <div class="sc">
        <div class="sc-num">2. {{STRAT_2_NUM_LABEL}}</div>
        <div class="sc-title">{{STRAT_2_TITLE}}</div>
        <div class="sc-desc">{{STRAT_2_DESC}}</div>
      </div>
      <div class="sc">
        <div class="sc-num">3. {{STRAT_3_NUM_LABEL}}</div>
        <div class="sc-title">{{STRAT_3_TITLE}}</div>
        <div class="sc-desc">{{STRAT_3_DESC}}</div>
      </div>
      <div class="sc">
        <div class="sc-num">4. {{STRAT_4_NUM_LABEL}}</div>
        <div class="sc-title">{{STRAT_4_TITLE}}</div>
        <div class="sc-desc">{{STRAT_4_DESC}}</div>
      </div>
      <div class="sc">
        <div class="sc-num">5. {{STRAT_5_NUM_LABEL}}</div>
        <div class="sc-title">{{STRAT_5_TITLE}}</div>
        <div class="sc-desc">{{STRAT_5_DESC}}</div>
      </div>
      <div class="sc">
        <div class="sc-num">6. {{STRAT_6_NUM_LABEL}}</div>
        <div class="sc-title">{{STRAT_6_TITLE}}</div>
        <div class="sc-desc">{{STRAT_6_DESC}}</div>
      </div>
    </div>
  </div>

  <!-- ── 05 INFRASITY'S NOTES ───────────────────────── -->
  <div class="sec-hdr">
    <span class="sec-dot"></span>
    <span class="sec-num">05</span>
    <span class="sec-label">Infrasity's Notes</span>
  </div>
  <div class="exec">
    <div class="exec-title">Strategic Overview</div>
    <p>{{EXEC_PARA_1}}</p>
    <p>{{EXEC_PARA_2}}</p>
    <p>{{EXEC_PARA_3}}</p>
    <p>{{EXEC_PARA_4}}</p>
    <div class="exec-badge">{{EXEC_BADGE_TEXT}}</div>
  </div>

  <!-- ── FOOTER ─────────────────────────────────────── -->
  <div class="footer">
    Data sourced from DataForSEO (ignore_synonyms: false) · Traffic figures represent estimated organic traffic value (ETV)<br>
    Competitive set: {{COMP_DOMAIN_LIST}} · Report period: {{START_DATE}} – {{END_DATE}} · Generated by Infrasity
  </div>

</div>
</body>
</html>
```
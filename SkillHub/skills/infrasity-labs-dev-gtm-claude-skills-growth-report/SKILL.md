---
name: growth-report
description: >
  Generates a 3-month SEO performance HTML report for any domain using DataForSEO data.
  Fetches baseline vs current traffic, keyword rankings, top content pages, and competitive
  landscape, then outputs a report styled with the Infrasity brand design system:
  #0D0A1A background, #8157F2 purple accent, Instrument Sans + DM Sans + DM Mono typography.
  Use this skill whenever a user provides a target domain and a list of competitor URLs and asks
  for an SEO report, performance report, SEO analysis, competitive SEO comparison, traffic report,
  ranking report, or 3-month SEO summary. Also trigger when the user says "generate SEO report for
  X vs Y and Z", "create a performance report", "compare my SEO against competitors", or pastes a
  domain and asks how it's performing versus the market. Always use this skill for SEO report
  generation — do not attempt to build the report without following this structured data-fetch and
  HTML generation workflow.
user-invokable: true
argument-hint: "[target_domain] [competitor1] [competitor2] ..."
license: MIT
metadata:
  author: Infrasity
  version: "1.3.0"
  category: seo
  design: infrasity-brand-v1
---

# SEO Performance Report Skill

Generates a comprehensive 3-month SEO performance HTML report using live DataForSEO data.
The report covers traffic trends, keyword rankings, top content clusters, competitive positioning,
strategic priorities, and an executive summary — all in the Infrasity brand design system.

---

## STEP 0 — COLLECT ALL INPUTS BEFORE DOING ANYTHING

**All four inputs are mandatory.** Do not make any API calls until all four are confirmed.

Collect them in a single message using this exact format — ask for everything at once, never
ask for inputs one at a time:

---

**If the user has NOT provided all four inputs**, ask:

> To generate the report I need 4 things:
>
> 1. **Target domain** — the site to report on, e.g. `firefly.ai`
> 2. **Competitor domains** — up to 5–6 competitors, e.g. `spacelift.io, env0.com, terraform.io`
> 3. **Date range** — start and end date for the 3-month window *(default: **Feb 20 → May 20, 2026**)*
> 4. **Location** — country for search data *(default: **United States**)*
>
> Which of these do you want to change from the defaults?

---

**If the user has already provided the target domain and competitors** (e.g. "generate SEO report
for firefly.ai vs spacelift.io, env0.com"), confirm the two optional inputs:

> Got it — I'll generate the report for **firefly.ai** vs spacelift.io, env0.com.
>
> Just confirming the defaults:
> - **Date range:** Feb 20 → May 20, 2026
> - **Location:** United States
>
> OK to proceed with these, or would you like to change either?

---

**Input parsing rules:**

| Input | Rules |
|---|---|
| `TARGET_DOMAIN` | Strip `https://`, `http://`, `www.`, and trailing slashes. Store bare domain only (e.g. `firefly.ai`) |
| `COMPETITORS` | Strip same prefixes from each. Accept comma-separated or space-separated list. Min 2, max 6 competitors. |
| `START_DATE` | Parse any human date format → `YYYY-MM-DD`. Default: `2026-02-20` |
| `END_DATE` | Parse any human date format → `YYYY-MM-DD`. Default: `2026-05-20` |
| `LOCATION` | Accept country name. Default: `United States`. Must be a valid DataForSEO `location_name` (full country name only, never city or region). |

**After confirmation, echo back the resolved inputs clearly before proceeding:**

> ✓ **Target:** firefly.ai
> ✓ **Competitors:** spacelift.io, env0.com, controlmonkey.io, scalr.com, terraform.io
> ✓ **Date range:** Feb 20, 2026 → May 20, 2026
> ✓ **Location:** United States
>
> Fetching data now...

---

## CRITICAL API SETTINGS

**Always use `ignore_synonyms: false` on every DataForSEO call.**
Using the default `ignore_synonyms: true` underreports traffic and keyword counts by 30–50%.
This is the single most important parameter to get right — never omit it.

---

## STEP 1 — Baseline Metrics

Call `dataforseo_labs_google_historical_rank_overview` with:
```
target:          TARGET_DOMAIN
location_name:   LOCATION
language_code:   en
ignore_synonyms: false
```

From the returned monthly array, find the snapshot **closest to START_DATE** (match by year+month).
Extract and store:
- `baseline_traffic`  = `metrics.organic.etv`
- `baseline_keywords` = `metrics.organic.count`
- `baseline_top3`     = `metrics.organic.pos_1` + `metrics.organic.pos_2_3`

> ⚠️ There is NO `pos_1_3` field in DataForSEO. Always compute Top 3 as `pos_1 + pos_2_3`.

Also extract **all monthly snapshots** between START_DATE and END_DATE for the traffic trend
bars in the report (typically 3–4 data points):
- For each snapshot store: `month_label` (e.g. "Feb 2026"), `etv`, `year`, `month`
- Sort ascending by date
- These become `TREND_LABEL_1..4`, `TREND_ETV_1..4` in the HTML template

---

## STEP 2 — Current Metrics

Call `dataforseo_labs_google_domain_rank_overview` with:
```
target:          TARGET_DOMAIN
location_name:   LOCATION
language_code:   en
ignore_synonyms: false
```

Extract from `metrics.organic`:
- `current_traffic`     = `etv`
- `current_keywords`    = `count`
- `current_top3`        = `pos_1` + `pos_2_3`
- `current_pos_1`       = `pos_1`
- `current_pos_2_3`     = `pos_2_3`
- `current_pos_4_10`    = `pos_4_10`
- `current_pos_11_20`   = `pos_11_20`
- `current_pos_21_100`  = sum of `pos_21_30` + `pos_31_40` + `pos_41_50` + `pos_51_60` + `pos_61_70` + `pos_71_80` + `pos_81_90` + `pos_91_100`

Calculate all deltas:
```
traffic_growth_pct  = ((current_traffic - baseline_traffic) / baseline_traffic) * 100
keywords_change     = current_keywords - baseline_keywords
keywords_change_pct = (keywords_change / baseline_keywords) * 100
top3_growth_pct     = ((current_top3 - baseline_top3) / baseline_top3) * 100
```

Format rules:
- Prefix `+` for positive values, `-` is automatic for negative
- Round all percentages to 1 decimal place
- Add `pos` CSS class for positive deltas, `neg` for negative

---

## STEP 3 — Competitive Landscape

### 3a — Current Traffic Snapshot

Call `dataforseo_labs_bulk_traffic_estimation` with:
```
targets:         [TARGET_DOMAIN, ...COMPETITORS]   ← all domains in a single API call
location_name:   LOCATION
language_code:   en
item_types:      ["organic"]
ignore_synonyms: false
```

For each domain returned, extract: `etv`, `count`.

Sort all domains **descending by etv**. Assign rank 1 = highest traffic.
Determine:
- `competitive_rank`     = rank position of TARGET_DOMAIN (1 = #1)
- `total_domains`        = total count of all domains in the table
- `domain_above`         = domain ranked one position above TARGET_DOMAIN (if any)
- `domain_below`         = domain ranked one position below TARGET_DOMAIN (if any)
- `gap_to_next_above`    = etv of domain_above − current_traffic (0 if TARGET_DOMAIN is #1)
- `lead_over_next_below` = current_traffic − etv of domain_below (0 if TARGET_DOMAIN is last)

### 3b — Competitor Trend Signals (Historical, Option 1)

For **each competitor** (not the target domain), call `dataforseo_labs_google_historical_rank_overview`:
```
target:          COMPETITOR_DOMAIN
location_name:   LOCATION
language_code:   en
ignore_synonyms: false
```

From the returned monthly array:
- Find the snapshot closest to **START_DATE** → extract `comp_baseline_etv`
- Find the snapshot closest to **END_DATE** → extract `comp_current_etv`
- Calculate: `comp_trend_pct = ((comp_current_etv - comp_baseline_etv) / comp_baseline_etv) * 100`

**Trend badge assignment rules (±5% stability threshold):**

| Condition | Badge | CSS class |
|---|---|---|
| `comp_trend_pct > +5%` | `↑ +X.X%` | `trend-up` (green) |
| `comp_trend_pct < -5%` | `↓ -X.X%` | `trend-down` (red) |
| `-5% ≤ comp_trend_pct ≤ +5%` | `→ Stable (X.X%)` | `trend-stable` (gray) |

**TARGET_DOMAIN trend for the competitive table** must also use the same START_DATE → END_DATE
window for consistency. The historical data fetched in Step 1 already contains this:
- `target_table_trend_pct = ((end_date_snapshot_etv - baseline_traffic) / baseline_traffic) * 100`

Where `end_date_snapshot_etv` is the ETV from the Step 1 historical array snapshot closest to
END_DATE (not `current_traffic` from Step 2, which is a live figure).

Apply the same ±5% threshold rules to derive the target's trend badge.

> ⚠️ `traffic_growth_pct` from Step 2 (baseline → live) is used for the timeline cards,
> delta badges, and executive summary — but **NOT** for the competitive table trend column.
> The competitive table trend column uses `target_table_trend_pct` (START_DATE → END_DATE)
> for all domains including the target, ensuring a consistent apples-to-apples comparison.

> ⚠️ Never default any competitor to "Stable" without running this calculation.
> Every trend badge in the competitive table must be derived from real historical ETV data.

---

## STEP 4 — Top Content Clusters

Call `dataforseo_labs_google_relevant_pages` with:
```
target:          TARGET_DOMAIN
location_name:   LOCATION
language_code:   en
order_by:        ["metrics.organic.etv,desc"]
limit:           3
ignore_synonyms: false
```

For each of the top 3 pages extract:
- `page_address` — shorten display URL: remove `https://www.` prefix, keep path
- `metrics.organic.etv`   → page_etv (format with commas, round to nearest integer)
- `metrics.organic.count` → page_keywords

**Homepage concentration check:**
If `page_1_etv / current_traffic > 0.80`, set `homepage_concentration = true`.
This triggers a specific paragraph in the executive summary.

---

## STEP 5 — Derive Report Targets (Q2 Card)

```
IF traffic_growth_pct >= 0:
  traffic_goal   = round(current_traffic * (1 + traffic_growth_pct/100))
ELSE:
  traffic_goal   = round(baseline_traffic * 0.9)   ← recovery target

keywords_goal    = max(round(current_keywords * 1.2), round(baseline_keywords * 0.95))
top3_goal        = round(current_top3 * 1.3)

IF competitive_rank == 1:
  target_badge = "Maintain #1"
ELSE:
  target_badge = "Challenge #" + str(competitive_rank - 1)
```

Format traffic_goal as e.g. `62,000+`. Round to nearest thousand for clean presentation.

---

## STEP 6 — Derive Strategic Priority Cards

Always generate exactly 6 cards. Use actual data values in every description — no generic text.
Reference competitor trend data from Step 3b to enrich card descriptions where relevant.

| # | Card title formula | Content rule |
|---|---|---|
| 1 | "Close Gap to #[rank_above]" | Name domain_above, state gap_to_next_above as ETV and its trend badge (growing/declining). If declining, frame as narrowing window opportunity. |
| 2 | "Defend vs. / Watch [domain_below or fastest_growing_competitor]" | If a lower-ranked competitor is growing fast (>+20%), flag it as a rising threat. Otherwise name domain_below, state lead_over_next_below. |
| 3 | Traffic recovery OR scale | If declined: "Reverse the [X]% Decline" with pos_4_10 count as pipeline. If grew: "Sustain [X]% Growth Trajectory" and note market context (e.g. if most competitors declined) |
| 4 | "Scale Top Content Clusters" | Reference page_1 URL and its ETV; flag homepage concentration if true |
| 5 | "Recover/Expand Keyword Coverage" | Use keywords_change as the specific number to recover or build on |
| 6 | "Convert Pos 4–10 to Top 3" | Use current_pos_4_10 count; state that converting 20% would add ~N new top-3 rankings |

---

## STEP 7 — Derive Executive Summary (4 paragraphs)

Write naturally — no bullet points inside the paragraphs. All numbers must be real API values.

- **Para 1:** Overall result. State traffic_growth_pct, competitive_rank of total_domains. State the trend distribution of competitors (how many are growing, stable, or declining derived from Step 3b) and whether the target is the fastest growing. Name the domains ranked immediately above and below with their ETVs and trend directions.

- **Para 2:** If `homepage_concentration = true`: flag that X% of traffic comes from one page,
  frame it as both a risk and an opportunity to diversify.
  Otherwise: describe content breadth advantage — keyword count vs competitors.

- **Para 3:** Top 3 keywords trend (top3_growth_pct). Flag keywords_change — if negative,
  state the specific number lost and the urgency to recapture. If positive, call it momentum.

- **Para 4:** Q2 strategy. Name the specific gap to close (gap_to_next_above), the competitor
  to chase (domain_above) and whether it is growing or declining. If domain_above is declining,
  frame the opportunity as a narrowing window. Name the recovery/scale action most impactful
  based on the data.

**Fastest growing determination** — compare `target_table_trend_pct` against all competitors'
`comp_trend_pct` values from Step 3b. If TARGET_DOMAIN has the highest trend percentage in the
set, set `is_fastest_growing = true`. Use this in Para 1 and the summary badge.

**Summary badge format:**
`Rank #[competitive_rank] | [current_traffic_K]K Traffic | [traffic_growth_pct]% Growth | [current_top3] Top-3 Keywords | [Fastest Growing / Declining / Stable]`

Where the last label is:
- Fastest Growing if is_fastest_growing = true
- Growing if traffic_growth_pct > 5% and not fastest growing
- Declining if traffic_growth_pct < -5% and not fastest growing
- Stable if -5% <= traffic_growth_pct <= +5% and not fastest growing

---

## STEP 8 — Generate the HTML Report

Read `references/html-template.md` for the complete HTML structure, CSS, and variable map.

The template uses the **Infrasity brand design system** exclusively:
- Background: `#0D0A1A` (Blackish-Violet) — never white, never any other dark
- Primary accent: `#8157F2` — the only accent colour; never substitute blue or green
- Fonts: `Instrument Sans` for all headings / KPI values / section numbers,
  `DM Sans` for all body / labels / UI text, `DM Mono` for paths / code / data values
- Status colours: `#5DCEA6` (positive delta), `#F07070` (negative delta)

Do **not** alter, override, or mix in any other colour palette or font stack.
Fill every `{{VARIABLE}}` with real data. Output the file to:
```
/mnt/user-data/outputs/{TARGET_DOMAIN}_seo_report.html
```

Then call `present_files` to deliver it to the user.

---

## ERROR HANDLING

| Situation | Action |
|---|---|
| Domain returns no data from bulk_traffic_estimation | Omit that domain from the competitive table; add a footnote |
| Historical snapshot missing for START_DATE or END_DATE month | Use nearest available month; note actual date used in report footer |
| `baseline_traffic` is 0 (division by zero) | Set `traffic_growth_pct` to "N/A", skip all delta badges that depend on it, and note in the report footer that baseline data was unavailable for START_DATE |
| `baseline_top3` is 0 (division by zero) | Set top3_growth_pct to "N/A" and skip the delta badge |
| `comp_baseline_etv` is 0 (division by zero for competitor trend) | Mark that competitor as "N/A" in the trend column |
| `backlinks_bulk_ranks` 40204 error | Do not call this endpoint — it requires a separate subscription. Skip entirely. |
| `ai_opt_llm_ment_agg_metrics` 40204 error | Do not include AI citations section. It is excluded from this skill. |

---

## WHAT NOT TO INCLUDE

- ❌ **No AI/LLM citation section** — excluded by design (requires paid DataForSEO add-on)
- ❌ **No DFS Rank (0–1000) column** — excluded by design (requires separate subscription)
- ❌ **No `ignore_synonyms: true`** — always `false`, no exceptions
- ❌ **No placeholder text** — every number in the HTML must come from a real API response
- ❌ **No asking for inputs one at a time** — always collect all missing inputs in a single message
- ❌ **No defaulting competitors to "Stable"** — always derive trend from historical ETV comparison

---

## REFERENCE FILES

- `references/html-template.md` — Full Infrasity-branded HTML template with CSS design system,
  all section markup, competitive table row patterns, and complete variable substitution map.
  **Always read this file before writing any HTML. The Infrasity design is the only permitted
  output design — do not use any other colour palette, font stack, or layout.**
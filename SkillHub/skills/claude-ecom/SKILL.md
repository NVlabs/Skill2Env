---
name: ecom
description: >
  Ecommerce business review for D2C stores from order transaction CSVs.
  Runs the bundled Python engine (KPI trees, ~30 pass/watch/fail health
  checks, 30d/90d/365d windows), then interprets the results: either a
  full narrative business review written to REVIEW.md, or an inline
  answer to a focused question.
when_to_use: >
  Use for "ecommerce review", "store review", "store health", "business
  review", revenue/customer/product analysis of an online store, or
  questions over order data like "how was last month", "how's retention",
  "why did revenue drop".
argument-hint: "review [30d|90d|365d] [question]"
allowed-tools:
  - Read
  - Grep
  - Glob
  - Write
  - Bash(ecom *)
---

# ecom — Ecommerce Business Review Toolkit

D2C ecommerce analytics. The bundled Python engine computes KPIs, runs
health checks, and scores performance from order transaction data;
**you** (Claude) interpret the numbers and write the human-readable report.

**Key principle:** Python computes the numbers. Claude interprets them.
Never present raw numbers without business context.

**Arguments:** `$ARGUMENTS` (if empty, infer intent from the conversation)

## Mode Selection

| Arguments / intent | Mode | Output |
|---|---|---|
| empty or `review` | Full Review (auto-selects periods from data) | `REVIEW.md` |
| `review 30d` / `90d` / `365d` | Full Review, single period | `REVIEW_{PERIOD}.md` |
| contains a natural-language question | Focused Query | Inline answer, no file |

## Input

Order transaction CSV. Each row = one order or line item.
Required columns: order ID, order date, customer ID (or email), revenue
(after discounts, before tax/shipping). Optional: quantity, SKU/product,
discount amount. Column names are fuzzy-matched by the loader.

If no CSV is specified, Glob for `*.csv` in the working directory and ask
the user if multiple plausible candidates exist.

## Running the Engine

The `ecom` CLI is on PATH while this plugin is enabled:

```bash
ecom review orders.csv --output <output-dir>
ecom review orders.csv --period 90d --output <output-dir>
```

If `ecom` is not on PATH, use the bundled launcher with the same
arguments: `"${CLAUDE_SKILL_DIR}/../../bin/ecom"`. The first run
bootstraps a private Python venv under `~/.local/share/claude-ecom/`
and may take a minute; later runs are instant.

Output: `review.json` (or `review_{period}.json` for `--period` runs)
in the output directory (defaults to current directory).

## Workflow

### Phase 1: Compute (Python)

Run the engine (add `--period` per Mode Selection). It computes, per
available period: summary KPIs with prior-period comparison, a
new-vs-returning KPI tree, revenue driver decomposition (AOV / volume /
mix), and — for 365d — repeat purchase rate and a 12-month
monthly_trend. It also evaluates ~30 health checks across Revenue,
Customer, and Product; each returns pass / watch / fail and powers the
🟢/🟡/🔴 markers.

### Phase 2: Interpret (you — Claude)

**Full Review:**

1. Read `review.json` (see Data Rules below; full schema in
   [review-schema.md](references/review-schema.md))
2. Read [report-format.md](references/report-format.md) — REQUIRED
   before writing; contains all section templates and Finding Quality
   Standards
3. Read [review-narratives.md](references/review-narratives.md) to pick
   the narrative arc
4. Load other references as needed (table below)
5. Write `REVIEW.md` (or `REVIEW_{PERIOD}.md`) satisfying the Report
   Contract below

**Focused Query:**

1. Read [focused-query.md](references/focused-query.md) — REQUIRED;
   contains the query-to-period mapping and answer format
2. Run the engine per that mapping, read the JSON, answer inline
   (10-30 lines). Do NOT write a file.

Your job is to weave trends and diagnostics into one coherent story.
Period analysis tells you *where things are heading*; health checks tell
you *what's broken right now*. The report combines both.

## Report Contract (Full Review)

Before writing, verify the report will contain ALL sections in this
exact order. Missing or reordered sections are a format violation.

1. [ ] Executive Summary — narrative blockquote (4-6 lines) + Scoreboard table
2. [ ] 30d Pulse section (if data available) — KPI tree + max 1 finding
3. [ ] 90d Momentum section (if data available) — KPI tree + drivers + max 2 findings
4. [ ] 365d Structure section (if data available) — KPI tree + drivers + max 3 findings
5. [ ] Action Plan — max 5 items grouped by time horizon + Guardrails (REQUIRED)
6. [ ] Data Notes — 2-4 lines

Hard rules:

- Target ~150 lines total; 5-7 findings max across all periods; never
  repeat a finding across periods
- Sections in this order; do NOT reorganize by theme; no standalone
  "What's Working Well" / "Issues to Address" sections — positive
  signals live in the Executive Summary and KPI tree markers
- Every period section uses the KPI tree format with 🟢/🟡/🔴 markers
- Every finding follows **What is → Why it matters → What to do**
  (quantitative fact → data-backed tension → direction; "consider",
  "improve", "optimize", "explore" are banned)
- Action Plan is the single source of truth for deadlines and success
  metrics, and ends with Guardrails (2-3 must-not-deteriorate metrics)

Templates, examples, and the full quality standards are in
[report-format.md](references/report-format.md).

## Reference Files

Load on-demand — do NOT load all at startup. Paths are relative to this
skill's directory.

| File | When to load |
|---|---|
| [report-format.md](references/report-format.md) | Every Full Review, before writing |
| [review-narratives.md](references/review-narratives.md) | Every Full Review — narrative arc by health level and trajectory |
| [focused-query.md](references/focused-query.md) | Every Focused Query |
| [review-schema.md](references/review-schema.md) | When review.json semantics are unclear |
| [finding-clusters.md](references/finding-clusters.md) | Full Review — to group related issues into themes |
| [recommended-actions.md](references/recommended-actions.md) | When turning watch/fail checks into actions |
| [impact-formulas.md](references/impact-formulas.md) | When estimating revenue impact |
| [health-checks.md](references/health-checks.md) | When a check's definition/threshold is unclear |
| [benchmarks.md](references/benchmarks.md) | When comparing KPIs to D2C benchmarks |

## Data Rules

- **review.json only.** All numbers MUST come from review.json or be
  derived from its values. Never reference external sources (Shopify
  Analytics, GA, ...). Recommending an external investigation as an
  action is allowed; quoting numbers from one is not.
- `periods` contains only the periods listed true in `data_coverage`;
  all `_change` fields are proportional vs the prior period (0.08 = +8%).
- `health.top_issues` is the pre-sorted subset of failing checks;
  `action_candidates` are Python's suggestions — refine and rewrite them
  in business language, never copy verbatim.
- Never expose internal check IDs or check counts in the report.
- When `data_quality` is non-empty, mention relevant warnings in Data
  Notes, and do not present partial-month MoM as real performance signals.

## Incomplete Data

- Omit what you can't measure. No N/A, no empty sections, no apologies.
- Shorter data = shorter report. Gaps are noted in Data Notes only.

## Language

Write the entire report (including Data Notes) in ONE language — match
the user's prompt/store language.

## Quality Gates

- Never present numbers without interpretation — always explain why
- Business language, not jargon; explain terms on first use
- Connect related findings into systemic patterns
- 80/20 rule: ~80% confirmation (builds trust), ~20% surprise (drives action)
- No numeric scores, letter grades, or percentage health ratings —
  pass/watch/fail signals only

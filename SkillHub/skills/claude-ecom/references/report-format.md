# Report Format: REVIEW.md / REVIEW_{PERIOD}.md

Full templates and quality standards for Full Review mode. The mandatory
section checklist and hard caps live in SKILL.md (Report Contract); this
file specifies how each part looks.

One report. Three parts. **Target: ~150 lines.** Tighter is better.

---

## Part 1: Executive Summary

### Narrative (4-6 lines, blockquote)

Synthesize across all available periods. Structure:

```
[North Star result + trend across periods]
[What's working: 1-2 strengths confirmed by data -- 80/20 rule]
[What needs attention: the key tension/risk, with data]
[Most important action, with timeline]
```

**Example:**
> Revenue reached $1.38M for the year (+25.7% YoY), but growth is decelerating --
> the last 90 days grew only 8% vs prior 90 days, and last month was flat (+0.3%).
> Growth depends on existing customer AOV increases (+14.8%), while new customer
> acquisition has stalled (share: 42.3%, unchanged). Reallocate 20% of retention
> budget to acquisition channels by end of this month, targeting CPA below $XX.

### Scoreboard

```
          30d Pulse     90d Momentum    365d Structure
Revenue   $98K (= flat) $340K (+ 8%)    $1.38M (+ 26%)
Orders    412 (- 3%)    1,280 (+ 5%)    5,784 (+ 10%)
AOV       $238 (= flat) $266 (+ 12%)    $239 (+ 15%)
Customers 287 (- 5%)    812 (+ 3%)      2,765 (+ 10%)
```

`+` improving, `-` deteriorating, `=` stable.
Only show periods that data supports.

---

## Part 2: Period Sections

**CRITICAL: Each period gets its own heading and its own KPI tree. Do NOT
merge periods into thematic sections.**

All periods use the same skeleton. **But they are not equal length:**

| Period | Depth | Findings cap | Role |
|--------|-------|-------------|------|
| 30d Pulse | Shallow -- KPI tree + 1-2 sentences + max 1 finding | 1 | Flag fires only |
| 90d Momentum | Medium -- KPI tree + drivers + max 2 findings | 2 | Main analytical body |
| 365d Structure | Deep -- KPI tree + drivers + max 3 findings | 3 | Strategic narrative |

If only one period is available, give it the full depth (3 findings).

**The total across all periods must not exceed 5-7 findings.** If a theme
appears in multiple periods, state it once at the most structural level and
reference supporting signals from shorter periods.

### Skeleton

#### [Period Name]: [One-line headline -- the "so what"]

**KPI Tree:**

```
Revenue $X (vs prior period: +X%)
|-- 🟢 New Customer Revenue $X (X% of total)
|   |-- New Customers: X (+X%)
|   |-- New Customer AOV: $X (+X%)
|-- 🟡 Existing Customer Revenue $X (X% of total)
    |-- Returning Customers: X (+X%)
    |-- Returning AOV: $X (+X%)
    |-- Repeat Purchase Rate: X% -- first-to-second purchase conversion (365d only)
```

🟢 healthy / 🟡 watch / 🔴 problem (driven by health check results).

**Growth Drivers** (1-2 sentences, 90d and 365d only):

Was the change volume-driven or price-driven? Connect to KPI tree nodes.

**Findings** (within period cap):

Each follows Finding Quality Standards (below). Findings should weave trend
data and health check diagnostics together, not present them separately.
Use this format:

```
### [Finding title]

**What is:** [1 sentence, quantitative fact]

**Why it matters:** [Data-backed tension with "however"/"despite"/"but"]

**What to do:** [Direction only — 1 sentence. Details go in Action Plan.]
```

---

## Part 3: Action Plan (unified, max 5 items)

**Hard cap: 5 action items. Exceeding 5 is a format violation.**

Action Plan is the single source of truth for deadlines and success metrics.
Findings point to the problem and direction; Action Plan specifies the execution.

One list synthesizing across all periods. Group by time horizon:

```
Immediate (from 30d signals)
1. ...

This Month (from 90d findings)
2. ...

This Quarter (from 365d insights)
3. ...
```

For each item:
- **What** (one concrete sentence)
- **Why** (reference specific data)
- **When** (specific deadline)
- **Success metric** (measurable)

End with (REQUIRED -- omitting Guardrails is a format violation):
> **Guardrails:** [2-3 metrics that must not deteriorate while executing above actions]
>
> Example: AOV must stay above $X | Repeat purchase rate must not drop below X% | Discount rate must stay under X%

---

## Data Notes (2-4 lines)

Always include:
- Revenue definition (from `metadata.revenue_definition`)
- Data period and order count
- Periods included/omitted

---

## Period Interaction Rules

- **Confirm or contradict across periods.** Don't let periods exist in isolation.
- **Zoom in:** If 90d shows a break, check 30d for continuation.
- **Never repeat a finding across periods.** State once at the structural level.
- **Executive Summary synthesizes**, does not summarize sequentially.

---

## Finding Quality Standards

**Every finding follows: What is → Why it matters → What to do**

- **What is:** 1 sentence. Quantitative fact. No interpretation.
- **Why it matters:** Data-backed tension. Must show contrast ("despite", "however").
  Abstract concerns like "growth must be validated" are PROHIBITED.
- **What to do:** Direction and rationale only — 1 sentence. Deadlines and
  success metrics belong in the Action Plan. "Consider", "improve", "optimize",
  "explore" are PROHIBITED.

**Good:**
```
What is:       Annual revenue grew 25.7% YoY.
Why it matters: However, despite a 25.4% reduction in discount rate, new customer
               revenue share remains at 42.3% -- growth depends entirely on
               existing customer AOV increases (+14.8%).
What to do:    Reallocate retention budget toward acquisition channels to diversify growth sources.
```

**Bad (PROHIBITED):**
```
What is:       Revenue grew 25.7%.
Why it matters: Rapid growth must be validated. <-- no data, no tension
What to do:    Consider improving acquisition. <-- banned verb, no deadline
```

# Focused Query Mode

How to answer a natural-language question from the data instead of writing
a full report. Output is an inline conversational response — do NOT create
a REVIEW.md file.

## Query-to-Period Mapping

| Query pattern | Data source |
|---|---|
| last 30 days | `--period 30d` |
| last 3 months / last 90 days | `--period 90d` |
| last year / this year | `--period 365d` |
| last month / specific month name | full run, extract from monthly_trend |
| Q1-Q4 / specific quarter | full run, extract from monthly_trend |

Calendar-month questions ("last month", "January") use the 365d
monthly_trend, NOT a 30d trailing window. Use `--period 30d` only when the
user explicitly asks for "last 30 days".

If the query doesn't map to a clear period, run full (no --period flag) and
answer from the most relevant data.

**Examples:**
- "how was last month?" → extract from monthly_trend
- "how was last year?" → 365d data
- "how was Q4 last year?" → extract from monthly_trend
- "how's retention looking?" → customer metrics focus

## Fallback when 365d coverage is unavailable

Calendar-month and quarter queries require 365d monthly_trend data. If 365d
coverage is missing (data < 400 days):

- Answer from the best available trailing window data
- State that exact calendar-month/quarter breakdown is not available
- Suggest running a full review for deeper analysis

## monthly_trend limitation: no year-over-year comparison by month/quarter

monthly_trend covers only the most recent 12 months. Comparing "Q4 this year
vs Q4 last year" is not possible. Instead:

- Present absolute values (revenue, orders) for the requested period
- Calculate its share of annual revenue (seasonality concentration)
- Compare against Q1-Q3 average for relative scale
- Add 365d overall YoY growth rate as context
- Do not mention the absence of YoY comparison (follow the incomplete-data
  rules in SKILL.md — omit what you can't measure)

## Response Format

1. **Direct answer** (2-3 sentences with key numbers from review.json)
2. **Supporting context** (1-2 observations that add nuance — tensions, comparisons)
3. **One actionable takeaway** (if warranted by the data)

Total: 10-30 lines. Headings, KPI tree, and Finding format are NOT required.
Use whatever structure best fits the answer. For example, "what's the new vs
returning split?" is clearest as a partial KPI tree.

Apply the same data rules as full reviews: all numbers from review.json
only, match the user's language.

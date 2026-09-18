# Review Narrative Templates

Reference file for interpreting business review reports (REVIEW.md).
Use these templates to write natural language interpretation.　Single unified review with multi-period architecture
(30d Pulse / 90d Momentum / 365d Structure).

---

## 1. Performance Narrative Templates

Select the template matching the growth trajectory. Used in the Executive
Summary narrative and as a starting point for period-level headlines.

### Strong Growth (revenue > +10% vs prior period)

> {Period} delivered strong revenue growth of {delta}%, driven primarily by
> {primary_driver: new customers / returning customers / AOV increase}.
> {secondary_observation}. The key question is whether this momentum is
> sustainable or driven by one-time factors.

### Stable Performance (-5% to +10% vs prior period)

> {Period} showed stable performance with revenue {direction} {delta}%,
> largely in line with expectations. {strength_callout}. The focus should
> shift to incremental optimization rather than diagnosing problems.

### Declining Performance (revenue < -5% vs prior period)

> {Period} saw a {delta}% revenue decline, primarily driven by
> {primary_driver: fewer orders / lower AOV / customer churn}.
> {urgency_statement}. Immediate investigation is needed to determine
> whether this is cyclical or structural.

### Mixed Signals

> {Period} presents a mixed picture: {positive_signal} but offset by
> {negative_signal}. The {metric} improvement of {value} is encouraging,
> but the {concerning_metric} decline of {value} warrants monitoring.

---

## 2. Executive Summary Template

The Executive Summary is a 4-6 line narrative that synthesizes across all
available periods. It is NOT a KPI list.

### Structure

```
[North Star + trend across periods]
[What's driving it -- connect 365d structure to 90d momentum to 30d signal]
[Most important action, with timeline]
```

### Worked Example

> Revenue reached $1.38M for the year (+25.7% YoY), but growth is decelerating --
> the last 90 days grew only 8% vs prior 90 days, and last month was flat (+0.3%).
> Growth depends on existing customer AOV increases (+14.8%), while new customer
> acquisition has stalled (share: 42.3%, unchanged). Reallocate 20% of retention
> budget to acquisition channels by end of this month, targeting CPA below $XX.

### Anti-patterns (PROHIBITED)

- "Revenue $1.38M, Orders 5,784, AOV $239, Customers 2,765..." -- number dump
- "The store performed well across most metrics" -- no specifics
- "Several areas show room for improvement" -- no direction
- "In the last 30 days X. In the last 90 days Y. In the last year Z." -- sequential summary instead of synthesis

---

## 3. KPI Tree Template

The KPI Tree replaces flat KPI tables. Revenue is the root, decomposed into
branches. Each node shows metric value + change vs prior period + health marker.

Markers are driven by internal health check results:
- 🟢 healthy (all associated checks pass)
- 🟡 watch (any associated check in warning)
- 🔴 problem (any associated check failing)

### Template

```
Revenue {value} (vs prior period: {change}%)
|-- {marker} New Customer Revenue {value} ({share}% of total)
|   |-- New Customers: {n} ({change}%)
|   |-- New Customer AOV: ${value} ({change}%)
|-- {marker} Existing Customer Revenue {value} ({share}% of total)
    |-- Returning Customers: {n} ({change}%)
    |-- Returning AOV: ${value} ({change}%)
    |-- Repeat Purchase Rate: {pct}% -- first-to-second purchase conversion (365d only)
```

### Worked Example (365d)

```
Revenue $1.38M (YoY +25.7%)
|-- 🟡 New Customer Revenue $584K (42.3% of total)
|   |-- New Customers: 1,812 (+10.3%)
|   |-- New Customer AOV: $323 (+4.1%)
|-- 🟢 Existing Customer Revenue $799K (57.7% of total)
    |-- Returning Customers: 953 (+10.3%)
    |-- Returning AOV: $838 (+18.2%)
    |-- Repeat Purchase Rate: 38%
```

### Worked Example (30d)

Keep 30d trees compact -- same structure, but no extra commentary:

```
Revenue $98K (MoM: = flat)
|-- 🟡 New Customer Revenue $38K (38.8%)
|   |-- New Customers: 95 (-8%)
|   |-- New Customer AOV: $400 (+3%)
|-- 🟢 Existing Customer Revenue $60K (61.2%)
    |-- Returning Customers: 192 (-3%)
    |-- Returning AOV: $312 (+1%)
    |-- Repeat Purchase Rate: 96%
```

### Marker Decision Rules

| Condition | Marker | When to use |
|-----------|--------|-------------|
| 🟢 | All checks pass | Metric is healthy, on track |
| 🟡 | Any check in warning | Emerging concern, worth noting |
| 🔴 | Any check failing | Active problem, must appear in findings |

---

## 4. Finding Templates

Every finding in the report follows: **What is → Why it matters → What to do**

See SKILL.md Finding Quality Standards for the rules. This section provides
worked examples for common D2C patterns.

### Growth Dependency

```
What is:       Annual revenue grew 25.7% YoY.
Why it matters: However, despite a 25.4% reduction in discount rate, new customer
               revenue share remains at 42.3% -- growth depends entirely on
               existing customer AOV increases (+14.8%). If existing customer
               purchase frequency slows, growth stops.
What to do:    Reallocate retention budget toward acquisition channels to diversify growth sources.
```

### Retention Cliff

```
What is:       Repeat purchase rate (first-to-second purchase conversion) is 38%, near top quartile.
Why it matters: However, F3 rate drops to 18% -- a 53% falloff between second and
               third purchase. More than half of second-time buyers never come back,
               creating a ceiling on customer lifetime value.
What to do:    Launch a post-second-purchase re-engagement sequence to close the F2-to-F3 gap.
```

### Seasonality Dependency

```
What is:       Q4 (Oct-Dec) accounts for 41% of annual revenue.
Why it matters: Q4 dependency rose 5 percentage points from prior year (was 36%).
               Q1-Q3 quarterly average is $197K and flat -- any Q4 shortfall now
               threatens the full-year target with no buffer.
What to do:    Build a non-Q4 revenue lever (e.g., summer campaign) to reduce seasonal dependency.
```

### Product Concentration

```
What is:       Top 5 SKUs account for 62% of total revenue.
Why it matters: Two of these SKUs are 18+ months old with YoY growth declining 8%.
               No replacement SKUs are in the pipeline. If these two slow further,
               total revenue declines directly.
What to do:    Accelerate new SKU pipeline to reduce top-5 revenue concentration.
```

### Revenue Volatility

```
What is:       Daily revenue coefficient of variation is 0.77 over the last 90 days.
Why it matters: D2C benchmark is below 0.5. High volatility means revenue depends on
               spike days (promotions, viral moments) rather than consistent demand.
               This makes forecasting unreliable and inventory planning difficult.
What to do:    Shift promotional budget from flash sales toward always-on acquisition to stabilize daily revenue.
```

### Discount Creep

```
What is:       Average discount rate is 6.6%, within healthy range.
Why it matters: However, 55% of orders include a discount -- up from 42% last quarter.
               The rate per order is low, but the breadth of discounting is expanding.
               If unchecked, customers begin to expect discounts on every purchase.
What to do:    Restrict promo code distribution to targeted segments to cap discounted order ratio.
```

### Customer Acquisition Stall

```
What is:       New customer count grew 10.3% YoY.
Why it matters: Despite this, new customer revenue share has not improved (42.3%,
               unchanged). New customer AOV is 2.6x lower than returning customer AOV,
               meaning acquisition growth isn't translating to revenue share gains.
What to do:    Test an upsell flow for first-time buyers to lift new customer AOV.
```

---

## 5. Period-Specific Guidance

Each period has a different role. The narrative tone and finding emphasis
should match.

### 30d Pulse

**Tone:** Direct, concise. Flag fires only.

**KPI Tree:** Show the full tree but keep it compact. No growth drivers section.

**Findings:** Max 1. Only surface findings if something anomalous happened --
a sudden drop, a spike, a metric crossing a threshold. If the month was
unremarkable, say so in one sentence and move on.

**Headline examples:**
- "30d Pulse: New customer acquisition dropped 15% -- investigate channel performance"
- "30d Pulse: Steady month, no anomalies detected"
- "30d Pulse: AOV spike of +12% driven by a single high-value cohort"

### 90d Momentum

**Tone:** Analytical. This is the main body of the review.

**KPI Tree:** Full tree with growth drivers (2-3 sentences on volume vs price).

**Findings:** Max 2. Focus on whether trends are improving or deteriorating,
and whether recent initiatives are working. Compare to prior 90 days.

**Headline examples:**
- "90d Momentum: Growth is decelerating -- AOV gains slowing while volume is flat"
- "90d Momentum: Retention improvements are paying off -- repeat purchase rate up 4pp"
- "90d Momentum: Mixed signals -- orders up but AOV declining, net revenue flat"

### 365d Structure

**Tone:** Strategic. This is the "big picture" section.

**KPI Tree:** Full tree with growth drivers (2-3 sentences on structural changes).

**Findings:** Max 3. Focus on structural issues: concentration risk, dependency
patterns, customer mix evolution, product lifecycle shifts. These findings
should drive the quarterly actions in the Action Plan.

**Headline examples:**
- "365d Structure: Revenue doubled, but growth is entirely AOV-driven -- volume engine needs building"
- "365d Structure: Healthy diversification -- no single product exceeds 15% share"
- "365d Structure: Customer base is aging -- 40% of revenue comes from cohorts acquired 18+ months ago"

---

## 6. Risk Assessment Rubric

Risks surface as findings (using the standard "What is / Why it matters / What to do"
format). Use this rubric to determine severity when a health check or trend
suggests structural risk.

### Severity Determination

| Risk Factor | High (must appear in findings) | Medium (mention if space) | Low (omit) |
|-------------|-------------------------------|--------------------------|------------|
| Revenue Concentration | Top product >50% share | Top product 30-50% | <30% |
| Acquisition Dependency | Returning share <30% | Returning share 30-40% | >40% |
| Discount Dependency | Avg discount >25% or rising trend | 15-25% | <15% stable |
| Product Lifecycle | Decline stage >50% of SKUs | 30-50% | <30% |
| Growth Sustainability | Revenue AND customers declining | One declining | Both growing |
| Revenue Volatility | Daily CV >0.8 | 0.5-0.8 | <0.5 |

High-severity risks MUST appear as findings. Medium risks appear only if the
finding cap for that period allows. Low risks are omitted from the report.

---

## 7. Action Plan Templates by Time Horizon

Actions in the unified Action Plan are grouped by time horizon. Each horizon
maps to the period that surfaced the finding.

### Immediate (from 30d Pulse signals)

Actions should be:
- Executable this week or next
- Measurable within 30 days
- Focused on stopping bleeding or capturing quick wins

Template:
```
1. {Specific action, one sentence}
   Why: {Data reference from 30d finding}
   When: {This week / Next week / By [date]}
   Success metric: {Measurable outcome}
```

### This Month (from 90d Momentum findings)

Actions should be:
- Executable within 30 days
- Connected to trend reversal or acceleration
- Include a clear test/learn component

Template:
```
2. {Specific action, one sentence}
   Why: {Data reference from 90d finding}
   When: By end of {month}
   Success metric: {Measurable outcome within 90 days}
```

### This Quarter (from 365d Structure insights)

Actions should be:
- Structural or foundational changes
- May require cross-team coordination
- Impact measured over 3-6 months

Template:
```
4. {Specific action, one sentence}
   Why: {Data reference from 365d finding}
   When: {Q2 / By end of June / etc.}
   Success metric: {Measurable outcome within 6 months}
```

### Guardrails

Every Action Plan ends with guardrails. These are metrics NOT being optimized
but that must be monitored for unintended side effects.

Template:
```
Guardrails:
- {Metric} must stay {above/below} {threshold} (currently {value})
- {Metric} must stay {above/below} {threshold} (currently {value})
```

Common guardrail pairs:
| If optimizing... | Monitor as guardrail |
|-----------------|---------------------|
| Revenue growth | Discount rate, gross margin |
| New customer acquisition | Customer acquisition cost |
| AOV increase | Conversion rate, order volume |
| Discount reduction | Revenue, order volume |
| Email open rate | Unsubscribe rate |

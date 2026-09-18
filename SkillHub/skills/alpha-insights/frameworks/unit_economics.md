# Unit Economics | Unit Economics Model

**Creator/Source**: Venture Capital / Internet industry standard framework
**Core Value**: Validate whether a business model's basic economic unit is healthy and determine if scaling is sustainable
**One-liner**: If you lose money on every transaction, scaling only makes you die faster

---

> **Case Boundary**: Company/industry cases in this file are illustrative examples for framework structure and reasoning, not current factual claims by Alpha Insights. Before reusing any numbers, shares, dates, or conclusions in a live study, re-check sources and record them in the Evidence Claim Ledger.

## Overview

Unit Economics is a framework for analyzing the profitability of individual economic units (users/orders/stores, etc.), and is the core tool for validating business model sustainability.

**Core Design Principles**:
- **Unit Thinking**: Simplify complex businesses into individual economic unit analysis
- **Sustainability Validation**: LTV > CAC is the fundamental condition for a viable business model
- **Scalability Assessment**: Healthy unit economics is the prerequisite for scaling

**Best Use Cases**:
- Business model sustainability validation
- User acquisition and retention strategy
- Pricing strategy optimization
- Fundraising feasibility assessment

**Output Value**:
- LTV/CAC ratio calculation
- Unit economics model decomposition
- Path to profitability map
- Key leverage point identification

---

## I. Framework Overview

### 1.1 Unit Economics Core Logic

```
┌─────────────────────────────────────────────────────────────┐
│                  Unit Economics Logic                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Healthy UE:                    Unhealthy UE:                │
│  ─────────                      ───────────                  │
│  LTV > CAC                      LTV < CAC                    │
│  (Profit per unit)               (Loss per unit)              │
│       ↓                              ↓                       │
│  Scaling = Profitable growth    Scaling = Accelerated death  │
│                                                             │
│  Key Questions:                                              │
│  • How much do you earn per customer? (LTV - CAC)            │
│  • How long to break even? (Payback Period)                  │
│  • How much return per ¥1 invested? (LTV/CAC)               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 Core Metric Definitions

| Metric | Full Name | Definition | Formula |
|--------|-----------|-----------|---------|
| **UE** | Unit Economics | Unit economics model | Revenue - Variable costs |
| **LTV** | Lifetime Value | Customer lifetime value | ARPU × Gross margin × Avg. lifetime |
| **CAC** | Customer Acquisition Cost | Cost to acquire a customer | Marketing spend / New customers |
| **ARPU** | Average Revenue Per User | Average revenue per user | Total revenue / User count |
| **CM** | Contribution Margin | Marginal contribution | Revenue - Variable costs |

### 1.3 Healthy UE Benchmarks

```
┌─────────────────────────────────────────────┐
│     Healthy UE Benchmarks (Internet)        │
├─────────────────────────────────────────────┤
│                                             │
│  LTV/CAC > 3     (¥1 invested earns ¥3)    │
│                                             │
│  CAC payback period < 12 months             │
│                                             │
│  Contribution margin > 30%                  │
│                                             │
│  12-month LTV / CAC > 3                     │
│                                             │
└─────────────────────────────────────────────┘
```

---

## II. UE Core Metrics Explained

### 2.1 LTV (Customer Lifetime Value)

**Definition**: The gross profit a customer contributes over their entire lifecycle.

**Calculation Formulas**:
```
Basic formula:
LTV = ARPU × Gross margin × Average lifetime

OR

LTV = Σ(Per-period revenue × Gross margin × Retention probability) / (1 + Discount rate)^period
```

**Key Parameters**:
| Parameter | Description | Estimation Method |
|-----------|-----------|------------------|
| ARPU | Average revenue per user | Historical data average |
| Gross margin | (Revenue - Variable costs) / Revenue | Financial data |
| Average lifetime | Duration of customer activity | 1 / Churn rate |
| Retention rate | Per-period retention proportion | Cohort analysis |
| Discount rate | Cost of capital | Typically 10% |

**Lifetime Estimation Methods**:
```
Method 1: Simple estimation
Average lifetime = 1 / Monthly churn rate

Example:
Monthly churn rate = 5%
Average lifetime = 1 / 0.05 = 20 months

Method 2: Cohort analysis
• Track same-cohort retention curves
• Calculate area under the curve
• More precise but requires more data
```

### 2.2 CAC (Customer Acquisition Cost)

**Definition**: Marketing cost required to acquire one paying customer.

**Calculation Formula**:
```
CAC = Marketing spend / New paying customers
```

**Marketing Cost Components**:
| Cost Type | Description | Example |
|----------|-----------|---------|
| Ad spend | Various advertising expenditures | Feed ads, search ads |
| Channel fees | Channel commissions | App store commissions |
| Marketing staff | Marketing team salaries | Optimization specialists, operations |
| Marketing tools | SaaS tool costs | Marketing automation |
| Brand marketing | Brand building costs | PR, events |

**Cautions**:
```
⚠️ Common CAC calculation errors:
1. Only counting ad spend, ignoring labor costs
2. Ignoring channel commissions
3. Ignoring brand marketing amortization
4. Calculating current month CAC from current month new users (lag effect)
```

### 2.3 LTV/CAC Ratio

**Definition**: Return on investment ratio, measuring customer acquisition efficiency.

**Benchmark Values**:
| Ratio | Meaning | Recommendation |
|-------|---------|---------------|
| >5 | Extremely high acquisition efficiency | Increase investment |
| 3-5 | Healthy | Maintain steady investment |
| 2-3 | Needs optimization | Improve LTV or reduce CAC |
| 1-2 | Dangerous | Re-examine the model |
| <1 | Unsustainable | Adjust immediately |

**Dynamic Perspective**:
```
LTV/CAC trend:

Early stage: May be low (high acquisition costs, LTV unvalidated)
Growth stage: Should improve (scale effects, retention improvements)
Mature stage: May decline (acquisition costs rising)

Key: Trend matters more than absolute value
```

### 2.4 CAC Payback Period

**Definition**: How long until customer acquisition cost is recouped.

**Calculation Formula**:
```
CAC Payback Period = CAC / (ARPU × Gross margin)

OR

CAC Payback Period = CAC / Monthly contribution margin
```

**Benchmark Values**:
| Period | Meaning | Cash Flow Impact |
|--------|---------|-----------------|
| <6 months | Excellent | Low cash flow pressure |
| 6-12 months | Healthy | Acceptable |
| 12-18 months | Needs attention | High cash flow pressure |
| >18 months | Dangerous | Requires funding support |

### 2.5 Contribution Margin

**Definition**: Revenue remaining after deducting variable costs.

**Calculation Formula**:
```
Contribution Margin = Revenue - Variable costs

Contribution Margin Rate = Contribution Margin / Revenue
```

**Variable Cost Components**:
| Cost Type | Description | Example |
|----------|-----------|---------|
| Fulfillment costs | Product/service delivery costs | Logistics, payment processing fees |
| Service costs | Customer service costs | Customer support staff |
| Content costs | Content acquisition costs | Licensing fees, revenue sharing |
| Refund losses | Costs from refunds | Refund amounts |

---

## III. UE Analysis Execution Steps

### Step 1: Define the "Unit"

**Goal**: Clarify the basic unit of analysis.

**Common Units**:
| Business Type | Unit Definition | Example |
|--------------|----------------|---------|
| E-commerce | Per order/per customer | Taobao order |
| SaaS | Per customer | Subscription user |
| Platform | Per user/per transaction | Didi order |
| Content | Per user | Member user |
| Finance | Per customer/per loan | Loan customer |

**Selection Principles**:
```
1. Revenue identifiable
   • Revenue contribution from the unit is trackable

2. Costs attributable
   • Variable costs can be attributed to the unit

3. Decision-relevant
   • The unit is the basic unit of business decisions
```

### Step 2: Identify Revenue and Costs

**Goal**: Attribute revenue and costs to the unit.

**Revenue Identification**:
```
Direct revenue:
• Product sales
• Service fees
• Subscription fees

Indirect revenue:
• Advertising revenue
• Commission revenue
• Data monetization
```

**Cost Attribution**:
```
Variable costs (included in UE):
• Fulfillment costs
• Payment processing fees
• Customer service costs
• Refund losses

Fixed costs (excluded from UE):
• R&D expenses
• Administrative expenses
• Office rent
```

### Step 3: Calculate UE Metrics

**Goal**: Calculate core UE metrics.

**Calculation Template**:
```
Unit UE Calculation:

Revenue:
├─ GMV/Order value: XXX
├─ Net revenue (after refunds): XXX
└─ Other revenue: XXX

Variable costs:
├─ Fulfillment costs: XXX
├─ Payment processing fees: XXX
├─ Customer service costs: XXX
└─ Other variable costs: XXX

Contribution Margin = Revenue - Variable costs
Contribution Margin Rate = Contribution Margin / Revenue
```

### Step 4: Calculate LTV and CAC

**Goal**: Calculate LTV and CAC.

**LTV Calculation**:
```
LTV Calculation Steps:

1. Calculate ARPU
   ARPU = Total revenue / User count

2. Calculate gross margin
   Gross margin = (Revenue - Variable costs) / Revenue

3. Estimate average lifetime
   Average lifetime = 1 / Churn rate

4. Calculate LTV
   LTV = ARPU × Gross margin × Average lifetime
```

**CAC Calculation**:
```
CAC Calculation Steps:

1. Aggregate marketing costs
   • Ad spend
   • Channel fees
   • Marketing staff
   • Marketing tools

2. Count new customers
   • New paying customers

3. Calculate CAC
   CAC = Marketing spend / New customer count
```

### Step 5: Analyze and Optimize

**Goal**: Identify optimization directions.

**Analysis Framework**:
```
UE Health Diagnostic:

1. LTV/CAC < 3
   → Improve LTV or reduce CAC

2. CAC payback period > 12 months
   → Increase ARPU or gross margin

3. Contribution margin rate < 30%
   → Raise prices or reduce variable costs

4. Churn rate too high
   → Improve retention
```

**Optimization Directions**:
| Metric | Optimization Direction | Specific Measures |
|--------|----------------------|-------------------|
| LTV ↑ | Increase ARPU | Price increases, cross-sell, upsell |
| LTV ↑ | Improve retention | Product improvement, increase stickiness |
| LTV ↑ | Improve gross margin | Cost reduction, structure optimization |
| CAC ↓ | Reduce acquisition cost | Optimize ad spend, improve conversion |
| CAC ↓ | Increase organic traffic | Brand, SEO, word-of-mouth |

---

## IV. Output Format

### 4.1 UE Analysis Report

```markdown
## Unit Economics - [Business Name]

### Unit Definition
- **Analysis unit**: [Per customer/per order/...]
- **Time period**: [Month/quarter/year]

### UE Calculation
| Item | Amount | Share |
|------|--------|-------|
| Revenue | XXX | 100% |
| Variable costs | XXX | XX% |
| Contribution margin | XXX | XX% |

### Core Metrics
| Metric | Value | Industry Benchmark | Health |
|--------|-------|--------------------|--------|
| LTV | XXX | - | - |
| CAC | XXX | - | - |
| LTV/CAC | X.X | >3 | Healthy/Warning/Danger |
| CAC payback period | X months | <12 months | Healthy/Warning/Danger |
| Contribution margin rate | XX% | >30% | Healthy/Warning/Danger |

### Trend Analysis
| Metric | This Month | Last Month | Change |
|--------|-----------|-----------|--------|
| LTV | ... | ... | ↑/↓ |
| CAC | ... | ... | ↑/↓ |
| LTV/CAC | ... | ... | ↑/↓ |

### Optimization Recommendations
| Priority | Optimization Direction | Specific Measures | Expected Impact |
|---------|----------------------|-------------------|----------------|
| P0 | ... | ... | ... |
| P1 | ... | ... | ... |
```

### 4.2 UE Sensitivity Analysis

```markdown
## UE Sensitivity Analysis

### Key Assumptions
| Assumption | Baseline | Optimistic | Pessimistic |
|-----------|----------|-----------|-------------|
| Acquisition cost | XXX | -10% | +20% |
| Retention rate | XX% | +5% | -5% |
| ARPU | XXX | +10% | -10% |

### Sensitivity Results
| Scenario | LTV | CAC | LTV/CAC | Payback Period |
|----------|-----|-----|---------|---------------|
| Baseline | ... | ... | ... | ... |
| Optimistic | ... | ... | ... | ... |
| Pessimistic | ... | ... | ... | ... |

### Break-even Analysis
- **Break-even CAC**: XXX
- **Break-even retention rate**: XX%
- **Break-even ARPU**: XXX
```

---

## External Research Supplement: Unit Economics Best Practices

Based on VC industry practice:

### 1. Core Formulas

```
LTV = ARPU × Gross margin × Average lifetime
CAC = Marketing spend / New users
LTV/CAC > 3 is healthy

Payback period = CAC / (ARPU × Gross margin)
<12 months is healthy
```

### 2. Unit Selection

| Business Type | Recommended Unit |
|--------------|-----------------|
| SaaS | Single customer |
| E-commerce | Single order |
| Platform | Single transaction |
| Retail | Single store/per sqm |
| Mobility | Single trip |

### 3. Common Errors

| Error | Manifestation | Correction |
|-------|--------------|-----------|
| Ignoring retention | Only calculating first-order LTV | Include retention curves in LTV calculation |
| Confusing gross profit | Using revenue instead of gross profit | Calculate LTV using gross profit |
| Averaging trap | Using overall averages that mask differences | Calculate by channel/user segment |

---

## V. Case Study

### Online Education vs SaaS Unit Economics Comparison (2024)

| Metric | Online Education (Vocational) | SaaS (Enterprise Collaboration) |
|--------|------------------------------|-------------------------------|
| **CAC** | ~¥3,000 | ~¥15,000 |
| **LTV** | ~¥8,000 | ~¥45,000 |
| **LTV/CAC** | 2.7 | 3.0 |
| **Payback period** | ~6 months | ~14 months |
| **Gross margin** | ~65% | ~75% |
| **NDR (Net Dollar Retention)** | ~85% (constrained by re-enrollment rates) | >110% (seat expansion) |
| **User lifetime** | ~18 months (churn upon course completion) | ~36 months (high switching costs) |

**Comparative Analysis**:
- **SaaS has higher CAC but NDR drives continuous growth**: NDR >100% means even without acquiring new customers, existing revenue is growing — this is the core advantage of the SaaS model
- **Education LTV constrained by course repurchase rates**: Users leave after completing courses, unless new courses or career growth paths are continuously developed
- **Payback period difference**: Education 6 months vs SaaS 14 months — SaaS faces greater cash flow pressure but offers higher long-term returns

**So What**: LTV/CAC >3 is the health standard, but **payback period is more critical** — it determines fundraising cadence and cash flow safety margin. Education companies recover costs quickly but have a low ceiling; SaaS recovers slowly but NDR-driven compounding makes long-term value higher. Investors should focus on the NDR and payback period combination rather than solely on the LTV/CAC ratio.

---

## VI. Data Source Recommendations

| Analysis Dimension | Recommended Data Sources |
|-------------------|------------------------|
| CAC data | Company filings (marketing spend/new users), prospectus CAC disclosures |
| LTV estimation | User retention curves (cohort analysis) + ARPU, customer churn rates from filings |
| Industry benchmarks | SaaS Capital annual reports, securities research industry benchmarks |
| Competitor comparison | Prospectuses (S-1/F-1 typically disclose key UE metrics) |
| Unit costs | Internal company data, expert interviews, earnings calls |
| NDR/Retention | SaaS company filings (Dollar-Based NDR), third-party SaaS benchmark databases |

---

## VII. Common Mistakes

| Mistake Type | Manifestation | Correction |
|-------------|--------------|-----------|
| Ignoring variable costs | Only counting marketing costs | Fully attribute all variable costs |
| LTV overestimation | Using theoretical lifetime | Use cohort analysis actual data |
| CAC underestimation | Only counting ad spend | Include staff, tools, etc. |
| Ignoring lag effects | Current month new users for current month CAC | Account for conversion cycle |
| Averaging trap | Using overall averages | Analyze by channel/user segment |
| Ignoring fixed costs | Healthy UE but overall losses | UE is only the first step |

---

## VIII. Integration with Other Frameworks

| Upstream Framework | Input Content | This Framework's Output | Downstream Framework |
|-------------------|--------------|------------------------|---------------------|
| Business model | Revenue model | UE validation | Flywheel |
| Three-Layer Analysis | Business data | Unit profitability | BCG Matrix |
| Competitive analysis | Competitor data | UE comparison | Value Chain |
| JTBD | Value proposition | LTV assumptions | TAM/SAM/SOM |

**Typical Combinations**:
- **Business model analysis**: BMC → Value Chain → Unit Economics
- **Business opportunity discovery**: JTBD → Unit Economics → Flywheel
- **Market entry**: TAM/SAM/SOM → Unit Economics → Three Horizons

---

## IX. China Market Specifics

| Dimension | China Characteristics | Case |
|-----------|----------------------|------|
| High acquisition costs | Fierce traffic competition; mainstream platform CAC continues rising | E-commerce CAC rose from ~¥100 in 2018 to ~¥300 in 2024 |
| Retention challenges | Low user loyalty; multi-app switching is the norm | Fresh grocery users simultaneously use 3-4 platforms to compare prices |
| Monetization pressure | Low C-end willingness to pay; freemium model predominates | iQiyi member ARPU far below Netflix |
| Subsidy dependency | Users educated by subsidies; churn when subsidies stop | Community group buying order volume typically halved after subsidy removal |
| Traffic cost divergence | Large price differences across platforms; precise channel selection needed | Douyin CPM ~¥50 vs WeChat private domain nearly free |
| Subsidy war dynamics | Competitor subsidies directly inflate industry CAC | Didi vs Kuaidi subsidy war, per-ride subsidy exceeded ¥20 |
| Ecosystem dependency | Customer acquisition highly dependent on Super App ecosystems | WeChat Mini Programs/Alipay Life accounts became standard for cold starts |

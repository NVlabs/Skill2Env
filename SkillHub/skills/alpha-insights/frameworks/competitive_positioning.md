# Competitive Positioning Map

> **Core Value**: Visualize competitor positions in a two-dimensional space, revealing positioning gaps and clusters at a glance
>
> **Source**: General strategic / marketing analysis tool, also known as Perceptual Map
>
> **One-liner**: One chart to see who competes with whom and where the white spaces are

---

> **Case Boundary**: Company/industry cases in this file are illustrative examples for framework structure and reasoning, not current factual claims by Alpha Insights. Before reusing any numbers, shares, dates, or conclusions in a live study, re-check sources and record them in the Evidence Claim Ledger.

## Overview

The Competitive Positioning Map is a two-dimensional matrix visualization tool for analyzing competitive landscapes, used to identify market gaps and differentiation opportunities.

**Core Design Principles**:
- **Two-Dimensional Space**: Build the competitive space using two key dimensions
- **Relative Positioning**: Visualize each competitor's relative position
- **White Space Identification**: Discover unoccupied positioning spaces

**Best Use Cases**:
- Competitive landscape visualization
- Differentiation opportunity identification
- New brand / new product positioning
- Competitive strategy design

**Output Value**:
- Two-dimensional competitive positioning map
- Competitor position annotations
- Market white space identification
- Recommended positioning strategies

---

## Framework Overview

```
Dimension Y (e.g., Price / Quality)
  High │
     │    ★ Competitor A      ★ Competitor B
     │
     │              ┌─────────┐
     │              │ White    │ ← Potential opportunity
     │              │ Space    │
     │              └─────────┘
     │
     │  ★ Competitor C
     │                    ★ Competitor D
  Low │
     └──────────────────────────────→ Dimension X (e.g., Feature Breadth / Specialization)
    Low                              High
```

---

## Why You Need Competitive Positioning Maps

| Other Competitive Tools | Limitation | What Positioning Maps Add |
|------------------------|-----------|--------------------------|
| Five Forces | Analyzes at the industry level, doesn't distinguish individual competitors | Pinpoints each competitor's exact position |
| SWOT | Text-based lists of strengths and weaknesses | Visual spatial relationships |
| SCP | Analyzes competitive behavior logic | Directly shows competitive outcomes |

**Core Value**:
1. Discover **competitive clusters** (red oceans)
2. Discover **white spaces** (potential blue oceans)
3. Identify **direct competitors** (same zone) vs. **indirect competitors** (different zones)
4. Assess the degree of **positioning differentiation**

---

## Execution Steps

### Step 1: Select Positioning Dimensions

**This is the most critical step**. Dimension selection determines the analytical power.

Selection criteria:
1. Dimensions must be things **customers care about** (not internal perspectives)
2. The two dimensions should be **relatively independent** (not highly correlated)
3. Competitors should have **clear differentiation** on these two dimensions

Common dimension combinations:

| Industry | Dimension X | Dimension Y |
|----------|------------|------------|
| General | Price | Quality / Service level |
| Internet products | Feature breadth | User experience / Ease of use |
| B2B services | Degree of customization | Price |
| Retail | Convenience | Product variety |
| Fintech | Service coverage range | Technology sophistication |
| Consumer goods | Price tier | Brand positioning (mass ↔ premium) |

**Advanced technique**: Create 2-3 different dimension combinations for positioning maps to observe the competitive landscape from multiple angles.

### Step 2: List Competitors

| Competitor | Dimension X Score (1-10) | Dimension Y Score (1-10) | Market Share |
|-----------|------------------------|------------------------|-------------|
| Our Company | | | |
| Competitor A | | | |
| Competitor B | | | |
| ... | | | |

Scoring methods (by priority):

| Priority | Method | Applicable Scenario | Specific Approach |
|----------|--------|--------------------|--------------------|
| **P0** | Direct conversion from objective data | Price, feature count, number of cities covered, and other quantifiable dimensions | Map industry max/min values to 1-10 linearly. E.g., for price: highest price=10, lowest=1, others proportionally |
| **P1** | User perception data | Experience, brand positioning, and other subjective dimensions | Use App Store ratings (1-5 → 2-10), review platform average ratings, NPS data |
| **P2** | Expert scoring | Dimensions with no public data | 3+ industry practitioners score independently, take median, label as "expert assessment" |

**Key Rules**:
- Scoring basis must cite sources; unsubstantiated scoring is not allowed
- All competitors on the same dimension must use the same scoring method
- Dimension scores require back-testing: If you swap two adjacent-scored competitors, does the conclusion still hold?

### Step 3: Draw the Positioning Map

Place competitors in the two-dimensional space. Circle size can represent market share or revenue scale.

### Step 4: Analyze the Positioning Map

Extract the following insights from the positioning map:

| Analysis Dimension | Focus |
|-------------------|-------|
| **Cluster zones** | Which competitors are crowded together? → Red ocean, most intense competition |
| **White space** | Where are no competitors? → May be an opportunity or a false demand |
| **Our position** | Is there differentiation? Who is the closest competitor? How far apart? |
| **Movement trends** | Which direction have competitors moved over the past 1-2 years? |
| **Scale distribution** | Where do large players concentrate? Small players? |

### Step 5: Derive Strategic Implications

Based on the positioning map, answer:
1. **Is the current positioning reasonable?** Is differentiation insufficient?
2. **Is the white space worth entering?** (Must combine with JTBD to verify demand authenticity)
3. **Which direction should we move toward?**
4. **Which competitors are the true direct threats?**

---

## Output Format

```markdown
## Competitive Positioning Analysis: [Industry/Market]

### Dimension Selection
- **X Axis**: [Dimension name] — [Selection rationale]
- **Y Axis**: [Dimension name] — [Selection rationale]

### Competitor Scoring
| Competitor | [Dimension X] (1-10) | [Dimension Y] (1-10) | Market Share | Scoring Basis |
|-----------|---------------------|---------------------|-------------|---------------|
| **Our Company** | X | X | XX% | [basis] |
| Competitor A | X | X | XX% | [basis] |
| Competitor B | X | X | XX% | [basis] |

### Positioning Map Insights
1. **Cluster zones**: [description] → [implications]
2. **White space**: [description] → [opportunity assessment]
3. **Our positioning**: [description] → [differentiation assessment]
4. **Movement trends**: [description] → [future competitive trajectory]

### Strategic Recommendations
- **Positioning adjustment direction**: [recommendation]
- **Core differentiation elements**: [recommendation]
- **Competitor movements to monitor**: [competitor + direction]
```

---

## Best Practices

### Data Source Recommendations

| Analysis Need | Recommended Data Sources |
|---------------|------------------------|
| Dimension scoring (objective) | Product specification comparisons (official websites/review sites), price data (e-commerce platform scraping), third-party reviews (Consumer Reports, DxOMark) |
| Dimension scoring (perception) | User survey questionnaires, App Store / review platform scores, social media sentiment analysis, NPS data |
| Market share | Brokerage research reports, QuestMobile (apps), Euromonitor/GfK (consumer goods), IDC/Canalys (tech) |
| Competitor movement trajectory | Product line evolution over years, pricing strategy adjustments, strategic direction stated in financial reports, executive public speeches |

### Industry Positioning Map Cases

| Industry | Recommended Dimension Combination | Typical Insights |
|----------|----------------------------------|-----------------|
| New tea drinks | Price tier × Product innovation frequency | Heytea/Nayuki cluster in high-price innovative zone, Mixue Bingcheng alone in low-price standardized zone, middle ground is white space |
| New energy vehicles | Price × Degree of intelligence | Tesla/NIO occupy high-price high-intelligence, BYD occupies mid-low price mid-intelligence, high-price low-intelligence zone (traditional luxury) is being eroded |
| SaaS tools | Feature depth × Ease of use | Enterprise products cluster in "high depth/low ease of use," emerging tools cluster in "low depth/high ease of use," their intersection is the competitive focal point |
| Cross-border e-commerce | Category breadth × Fulfillment speed | SHEIN occupies "narrow category + fast fulfillment," Temu occupies "broad category + slow fulfillment," Amazon occupies "full category + fast fulfillment" |

### Full Case Study: New Tea Drinks Industry Positioning Map

**Dimension Selection**: X = Average product price (RMB); Y = Product innovation frequency (monthly new SKU count)

| Brand | Avg. Price (RMB) | X Score | Monthly New Items | Y Score | Annual Revenue (B RMB) | Scoring Basis |
|-------|-------------------|---------|-------------------|---------|------------------------|---------------|
| Heytea | 25-35 | 8 | 6-8 items | 9 | ~6 | Meituan/Ele.me price data + official account new-item tracking |
| Nayuki | 22-32 | 7 | 4-5 items | 7 | 5.2 (2023 financials) | Public company financials + menu tracking |
| Chabaidao | 12-20 | 5 | 2-3 items | 4 | 5.7 (2023 prospectus) | Prospectus data |
| Guming | 10-18 | 4 | 2-3 items | 4 | 5.5+ (2023 prospectus) | Prospectus data |
| Mixue Bingcheng | 4-8 | 1 | 1-2 items | 2 | 20+ (2023 prospectus) | Prospectus data |
| Bawangchaji | 14-22 | 5 | 3-4 items | 5 | ~5 | Meituan data + industry estimates |
| Hushang Ayi | 10-16 | 3 | 2-3 items | 3 | ~4 | Industry research reports |

**Positioning Map Insights**:
1. **Cluster zone**: Mid-price (10-20 RMB) + low innovation (2-3 items/month) is highly crowded — Chabaidao, Guming, and Hushang Ayi in fierce competition
2. **White space**: High innovation + low price zone is unoccupied (innovation requires R&D investment, low-price models can't support it) → false demand
3. **Bawangchaji's differentiation**: Using the "Oriental Tea" concept to carve out differentiation in mid-price, avoiding head-on competition with Heytea
4. **Mixue Bingcheng's isolated advantage**: Only scaled player in the low-price zone, deep moat (supply chain + density)

**So What**: New entrants should avoid the mid-price red ocean. Either do extreme innovation at high price (benchmarking Heytea) or do "quality at accessible prices" that Mixue Bingcheng cannot reach (e.g., average 8-12 RMB + quality perception).

---

### China Market Specifics

| Dimension | China Characteristics | Case |
|-----------|----------------------|------|
| Dimension selection | Chinese consumers are extremely "value-for-money" sensitive — price is almost always a required dimension; social attributes are often a hidden but critical second dimension | New tea drinks positioning maps must include "price" dimension; Pop Mart's "social currency" dimension |
| High dynamism | Chinese market competitive landscapes change rapidly — recommend updating positioning maps every 6 months, tracking "competitor movement speed" | Luckin's price tier dropped from 15-25 RMB to 9.9 RMB in 2023, reshaping the coffee positioning map within 6 months |
| Ecosystem dimension | For platform-type companies, an "ecosystem completeness" dimension should be added | WeChat ecosystem vs. Alipay ecosystem vs. Douyin ecosystem competitive positioning comparison |

---

## Common Mistakes

| Mistake | Correct Approach |
|---------|-----------------|
| Arbitrary dimension selection | Must be dimensions customers care about and where competitors differ |
| Purely subjective scoring | Support scores with data/user feedback |
| Only drawing without analyzing | The chart is the means; insights (clusters, white space, trends) are the goal |
| White space = opportunity | White space may be false demand — needs JTBD verification |
| Only one set of dimensions | Create 2-3 sets for multi-angle observation |

---

## Integration with Other Frameworks

| Partner Framework | Relationship | Specific Synergy |
|-------------------|-------------|------------------|
| Blue Ocean Strategy | Strategy Canvas is multi-dimensional comparison; positioning map is 2D spatial comparison | Positioning map discovers white space → Blue Ocean's "Eliminate-Reduce-Raise-Create" validates white space value |
| JTBD | Demand verification for white spaces | Positioning map finds white space → JTBD verifies whether real unmet tasks exist in that zone |
| SWOT | Positioning analysis results feed into S and W | Positioning map differentiation advantages → S; positioning weaknesses → W; movement trends → O/T |
| SCP | Visual presentation of Conduct analysis | SCP's Conduct-layer behavior analysis → positioning map visually displays competitive behavior outcomes |
| Five Forces | Industry-level competitive intensity → firm-level competitive relationships | Five Forces judges industry attractiveness → positioning map pinpoints each competitor's position and differentiation |
| Playing to Win | Positioning map outputs support WTP/HTW choices | Cluster zones = red ocean (avoid); white space = WTP candidates; differentiation distance = HTW clues |

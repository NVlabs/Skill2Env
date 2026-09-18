# Industry Lifecycle

> **Core Value**: Determine which evolutionary stage an industry is in — different stages demand different strategic approaches
>
> **Source**: Raymond Vernon (Product Life Cycle) → extended to the industry level
>
> **One-liner**: Entering during the growth phase vs. entering during decline requires entirely different strategies — identify the stage first, then set the strategy

---

> **Case Boundary**: Company/industry cases in this file are illustrative examples for framework structure and reasoning, not current factual claims by Alpha Insights. Before reusing any numbers, shares, dates, or conclusions in a live study, re-check sources and record them in the Evidence Claim Ledger.

## Overview

The Industry Lifecycle framework describes how industries evolve from birth to decline, serving as a foundational tool for judging development stages and forecasting future trends.

**Core Design Principles**:
- **Phased Evolution**: Industries pass through Introduction → Growth → Maturity → Decline
- **Stage Characteristics**: Each stage has unique competitive dynamics, profit models, and key success factors
- **Strategy Fit**: Different stages require different competitive strategies

**Best Use Cases**:
- Industry development stage assessment
- Market entry timing evaluation
- Competitive strategy selection
- Investment timing decisions

**Output Value**:
- Lifecycle stage determination
- Stage-characteristic matching analysis
- Evolutionary trend forecasts
- Strategy-fit recommendations

---

## Framework Overview

```
Market Size / Growth Rate
    ↑
    │          ╱╲
    │        ╱    ╲
    │      ╱  Growth  ╲        Maturity
    │    ╱              ╲──────────────╲
    │  ╱                                ╲  Decline
    │╱  Introduction                      ╲────────
    └──────────────────────────────────────────→ Time
```

---

## Four-Stage Characteristics

| Dimension | Introduction | Growth | Maturity | Decline |
|-----------|-------------|--------|----------|---------|
| **Market Growth** | Low / uncertain | High (>20%) | Slowing (<10%) | Negative |
| **Market Size** | Very small | Rapidly expanding | Large and stable | Shrinking |
| **Number of Competitors** | Few (pioneers) | Rapidly increasing | Consolidating | Few (survivors) |
| **Profit Levels** | Mostly losses | High profits | Margin compression | Low profits |
| **Customer Type** | Innovators / early adopters | Early majority | Late majority | Laggards |
| **Competitive Focus** | Product viability | Feature differentiation | Cost efficiency | Cost / exit |
| **Entry Barriers** | High technology barriers | Medium | High scale barriers | Not worth investing |
| **Key Success Factors** | Technical innovation | Speed of market acquisition | Operational efficiency / scale | Cash flow management |

---

## Execution Steps

### Step 1: Collect Stage-Assessment Indicators

The following data is needed to determine the industry stage:

| Indicator | Data Source | Assessment Use |
|-----------|-----------|----------------|
| Market size (past 3-5 years) | Industry reports / TAM estimates | Scale magnitude |
| Market growth rate (YoY) | Industry reports / statistics | Growth trend |
| Industry concentration (CR5/HHI) | Competitor data | Degree of competitive consolidation |
| Number / frequency of new entrants | Business registration databases | Entry intensity |
| Profit margins of leading firms | Financial reports / research reports | Profit headroom |
| Technology iteration frequency | Patent data / tech coverage | Technology maturity |
| User penetration rate | User data | Market saturation |

### Step 2: Stage Determination

Use a decision tree for quick positioning:

```
Market growth > 20%?
├── Yes → Does the market have a proven business model?
│        ├── Yes → Growth stage
│        └── No → Late Introduction / Early Growth
│
└── No → Market growth > 0%?
         ├── Yes → Is industry concentration increasing?
         │        ├── Yes → Maturity (consolidation phase)
         │        └── No → Maturity (stable phase)
         └── No → Decline
```

**Important Note**: Many industries are not uniformly in one stage. Distinguish between:
- **Overall industry** vs. **sub-segments** (some segments may be at different stages)
- **Domestic market** vs. **global market** (one may lag or lead the other)

### Step 3: Derive Strategic Implications

| Stage | Core Strategic Logic | Typical Strategies |
|-------|---------------------|-------------------|
| **Introduction** | Validate demand, iterate rapidly | Focus on core use cases, MVP validation, market education |
| **Growth** | Capture share, build moats | Rapid expansion, scaled customer acquisition, fundraising, ecosystem building |
| **Maturity** | Improve efficiency, differentiate | Cost optimization, deep sub-segment focus, M&A consolidation |
| **Decline** | Harvest or pivot | Cash flow management, strategic pivots, divestiture |

### Step 4: Identify Stage-Transition Signals

Identify leading indicators (with quantitative thresholds) for an industry about to enter the next stage:

| Transition | Leading Signals | Quantitative Thresholds | Assessment Method |
|------------|----------------|------------------------|-------------------|
| **Introduction → Growth** | Killer app emerges, policy support, major players enter | Penetration rate breaks 5-10%; YoY >30% for 2 consecutive quarters; 3+ companies raise Series A or above | Meet 2 of 3 criteria to confirm transition |
| **Growth → Maturity** | Growth inflection point, price wars, M&A wave | YoY drops >5pct quarter-over-quarter for 2 consecutive quarters (e.g., 25%→20%→15%); CR5 exceeds 60%; >3 M&A deals per year | Growth inflection is the most reliable signal; others serve as validation |
| **Maturity → Decline** | Substitutes emerge, user attrition, leaders pivot | Core MAU declines >3% QoQ for 2 consecutive quarters; substitute penetration >15%; leaders' non-core revenue >30% | User attrition is the earliest signal, typically leading financial indicators by 2-3 quarters |

**Precise Growth Inflection Detection**:
```
Focus on the rate of change of growth (acceleration), not the absolute rate:
- Accelerating growth (e.g., 20%→25%→30%) = Still in upper growth phase
- Flat growth (e.g., 25%→24%→25%) = Peak of growth stage, watch for transition
- Decelerating growth (e.g., 30%→22%→15%) = Transition has begun
- YoY drops >5pct QoQ for 2 consecutive quarters = Confirmed entry into maturity
```

---

## Output Format

```markdown
## Industry Lifecycle Analysis: [Industry Name]

### Stage Determination
**Current Stage**: [Growth / Maturity / ...]
**Supporting Evidence**:
- Market growth rate: [XX%] → [explanation]
- Industry concentration: CR5 = [XX%] → [explanation]
- User penetration rate: [XX%] → [explanation]
- New entrant trends: [description]

### Sub-Segment Differences (if applicable)
| Sub-Segment | Stage | Growth Rate | Notes |
|-------------|-------|-------------|-------|
| [Segment 1] | Growth | XX% | [notes] |
| [Segment 2] | Maturity | XX% | [notes] |

### Strategic Implications
The core strategic logic for this stage is: [...]
This specifically means:
1. [Implication 1]
2. [Implication 2]

### Stage Transition Signal Monitoring
| Signal | Current Status | Trigger Condition |
|--------|---------------|-------------------|
| [Signal 1] | [status] | [condition] |
| [Signal 2] | [status] | [condition] |
```

---

## Best Practices

### Data Source Recommendations

| Analysis Need | Recommended Data Sources |
|---------------|------------------------|
| Market size / growth | Brokerage industry research reports (iResearch, IDC, Frost & Sullivan), national statistics bureau industry data, industry association annual reports |
| Industry concentration | Public company financials (revenue comparisons), business registration data (registrations/cancellations), bidding data |
| User penetration | QuestMobile (internet industries), CNNIC reports, industry white papers |
| Technology maturity | Gartner Hype Cycle, patent searches (CNKI/Google Patents), academic publication trends |
| Investment activity | IT Juzi, PitchBook, 36Kr, Crunchbase |

### Industry Stage Assessment Cases

| Industry | Stage Assessment | Key Evidence | So What |
|----------|-----------------|-------------|---------|
| **New Energy Vehicles** | Growth → Maturity transition (2024) | YoY dropped from 96% in 2022 to ~25% in 2024; penetration exceeded 40%; intense price wars (BYD leading price cuts); CR5 >65% | Window has closed. New entrants should focus on niches (e.g., pickups, MPVs) rather than competing head-on in sedan/SUV main battlegrounds |
| **Online Education (K12)** | Policy-driven jump directly to Decline (2021) | "Double Reduction" policy changed industry structure overnight; leading companies (TAL/New Oriental) K12 revenue went to zero; massive workforce exodus | China-specific: Policy can skip natural lifecycle stages. Industry analysis must treat policy risk as the primary variable |
| **Live Commerce** | Late Growth stage (2024) | YoY still ~30% but decelerating (2022: 48%→2023: 35%→2024: ~28%); top streamer share dispersing; platform commission rates increasing | Deceleration signals evident. Expect maturity by 2025-2026. Entering now requires differentiated positioning (e.g., vertical-specific live streaming) |
| **Medical Aesthetics** | Stage stratification (2024) | Tier 1 cities: Maturity (penetration >20%, growth <10%, fierce price wars); Lower-tier markets: Growth (penetration <5%, growth >25%) | Classic "one industry, two stages." Strategy should be tailored by market tier |
| **AI Large Model Applications** | Late Introduction (2024) | Rapid tech iteration but unproven business models; heavy funding but very few profitable players; user penetration <10% (DAU/MAU basis) | Focus on scenario validation over scaling. Wait for "killer app" emergence signals |

---

### Deep Case: China Bike-Sharing Full Lifecycle Review (2015–2025)

> **Why This Case**: Bike-sharing is the most complete "textbook example" of industry lifecycle in China's consumer internet — having gone through Introduction → Growth → Maturity → Restart in just 5 years. Every stage has clear quantitative signals, and the transition from Growth to Maturity is particularly dramatic, offering high reference value for stage-transition signal detection.

#### Stage 1: Introduction (2015–2016H1)

| Dimension | Manifestation | Data |
|-----------|--------------|------|
| Market size | Very small | Total bikes <500k nationwide; daily orders <100k |
| Growth rate | High but low base | YoY >200%, but from near-zero base |
| Number of firms | Very few | Only Mobike, ofo, and 1-2 local players |
| Profit | All losing money | Single-ride revenue <RMB 0.5, single-ride cost >RMB 2, unit economics not closed |
| Customer type | Innovators / early adopters | University students, young white-collar workers in Tier 1 cities |
| Competitive focus | Product viability | "Can the bike be found?" "Can it be unlocked?" "Does it ride well?" |
| Key success factor | Product + capital | Mobike's GPS + smart lock tech lead; ofo's low-cost mechanical lock scaling |

**Introduction stage characteristic**: Product form still being validated (dockless vs. docked, smart lock vs. mechanical lock), capital moving cautiously (<RMB 500M total).

---

#### Stage 2: Growth (2016H2–2017)

| Dimension | Manifestation | Data |
|-----------|--------------|------|
| Market size | Explosive scaling | Total bikes from <500k → 23M (46x in 1 year); daily orders from <100k → 70M (700x) |
| Growth rate | Super-high speed | 2017 YoY >300%; market size exceeded RMB 10B |
| Number of firms | Rapid increase | From 3 → 60+ (Bluegogo, Coolqi, Xiaoming, etc.), VC capital flooding in |
| Profit | All losing money, but capital doesn't care | Total industry financing RMB 25.8B in 2017; ofo alone raised >RMB 10B |
| Customer type | Early majority | Spreading from students/white-collar to all urban residents; user base >200M |
| Competitive focus | Market acquisition speed | "Hundred-city battle" — whoever covers most cities wins first; daily deployment in ten-thousands |
| Key success factor | Financing capability + operational speed | Monthly burn rate of hundreds of millions; "free riding" subsidy wars |

**Typical growth-stage characteristics**:
- **Capital catalysis effect**: Chinese VCs poured >RMB 30B into bike-sharing within 18 months, compressing what should be 5-8 years of growth into 1.5 years
- **Excessive competition**: 60+ firms = severe oversupply, but growth-stage momentum masked the bubble
- **"Scale first, profit later" logic**: All firms were loss-making expansions, betting on winner-take-all

---

#### Stage 3: Maturity / Shakeout (2018–2019)

| Dimension | Manifestation | Data |
|-----------|--------------|------|
| Growth rate | Sharp slowdown | 2018 YoY plummeted from >300% to <10% |
| Competitor consolidation | Mass exits | 60+ → 3 survivors. Bluegogo/Xiaoming/Coolqi and 20+ others bankrupt, ofo collapsed (16M users queued for deposit refunds) |
| Industry concentration | Rapid consolidation | CR3 from ~40% → >90%: Meituan acquired Mobike (USD 2.7B), Hellobike got Alibaba investment, Didi took over Bluegogo |
| Profit | Industry-wide losses | Mobike wrote down RMB 4.55B impairment after Meituan acquisition; ofo liabilities exceeded RMB 6.5B |
| Competitive focus | Cost efficiency + fine operations | Shifted from "who deploys more" to "who loses less" |
| Policy | Regulatory intervention | 2018 multiple cities issued "ban on new deployments," total volume control (Beijing/Shanghai/Guangzhou/Shenzhen) |

**Transition signal review** (Growth → Maturity):
1. ✅ Growth inflection: 2017 Q4 QoQ growth first decline (from >50% QoQ to <15%)
2. ✅ CR5 exceeds 60%: ofo+Mobike combined >80% share
3. ✅ >3 annual M&A: 2018 saw 5+ M&A/exit events
4. ✅ Policy restrictions: Government total volume control = growth ceiling confirmed

**Key lesson**: Growth → Maturity transitions are often faster and steeper than expected — ofo went from USD 3B valuation to insolvency in just 1 year.

---

#### Stage 4: Restart / Steady State (2020–2025)

| Dimension | Manifestation | Data |
|-----------|--------------|------|
| Market structure | Tri-oligopoly steady state | Meituan Bike, Hellobike, Didi Qingju, CR3 ≈95% |
| Growth rate | Low single digits | YoY ~5-8%, following urban population and commuting demand natural growth |
| Business model | From deposit to deposit-free/monthly pass | Monthly pass RMB 15-25, per-ride price RMB 1.5-2.5, average 2-3 rides/bike/day |
| Competitive focus | Fine operations + government relations | Dispatch efficiency (AI predicting tidal flows), vehicle turnover rate, compliance rate |
| Profit | Approaching break-even | Hellobike overall profitable in 2023; Meituan Bike still a traffic acquisition tool (no standalone P&L) |
| Industry positioning | From "hot trend" to "infrastructure" | Bike-sharing became part of urban public transportation, no longer a startup glamour |

**Restart characteristic**: Bike-sharing did not truly "decline" — it experienced a return to rationality after a bubble burst. This is common in China: capital catalysis causes lifecycle "premature overdraft," and after shakeout, the industry restarts with a healthier business model.

---

#### Lifecycle Panorama (Data Version)

```
Indicator     2015   2016   2017   2018   2019   2020   2025
─────────────────────────────────────────────────────────────
Firms          3      15     60+    30     5      3      3
Deployment(10k bikes) <50    200    2300   2500   1800   1500   ~2000
Financing(RMB B)<0.5 3      25.8   <2     <0.5   —      —
Daily orders(M) <0.1   5      70     50     40     45     ~60
Users(100M)   <0.1   0.5    2+     2.5    2.5    2.8    ~3.5
Stage         Intro  Intro→Growth Growth Explosion Maturity Shakeout Steady Steady
```

---

#### Case Methodology Takeaways

1. **China market lifecycle compression effect**: Bike-sharing went from Introduction to Maturity in just 3 years (global norm: 10-15 years). Capital catalysis is the main compression driver — RMB 25.8B financing flooded in within 1 year, artificially accelerating the growth phase
2. **Practical value of transition signals**: Growth inflection (2017 Q4) appeared 2 quarters before firm bankruptcies (2018 Q2) — if investors had exited at the growth inflection, they could have avoided >80% of losses
3. **Policy is China's "super variable"**: The ban on new deployments directly drew a full stop on the growth phase, which would not happen in purely market-driven economies. China industry analysis must treat policy as the primary dimension of stage judgment
4. **"Death ≠ Decline"**: The bike-sharing industry itself did not decline; what declined was the bubble-inflated business model. The tri-oligopoly operates healthily to this day after shakeout — distinguishing "industry decline" from "bubble burst" is a key cognitive insight

---

### Cross-Industry Lifecycle Speed Comparison

| Industry | Introduction | Growth | Maturity | Total Cycle | Compression Factor |
|----------|-------------|--------|----------|------------|-------------------|
| **Bike-sharing (China)** | 1.5 years | 1.5 years | 2 years | **5 years** | Capital + mobile payment |
| **Community group buying (China)** | 1 year | 1 year | 1 year | **3 years** | Capital + giant ecosystem entry |
| **NEV (China)** | 5 years (2010–2015) | 8 years (2015–2023) | Ongoing | **13+ years** | Policy + tech cycle |
| **E-commerce (US)** | 7 years (1995–2002) | 10 years (2002–2012) | Ongoing | **20+ years** | Natural evolution |
| **Smartphones (Global)** | 3 years (2007–2010) | 7 years (2010–2017) | Ongoing | **15+ years** | Hardware iteration cycle |

**Pattern**: Chinese consumer internet industry lifecycles are typically **1/3 to 1/2** of global markets. Main compression factors: (1) Highest VC capital density globally (2) Mature mobile payment infrastructure (3) Super-large population network effects (4) Policy can accelerate or terminate any stage.

---

### China Market Specifics

| Dimension | China Characteristics | Case |
|-----------|----------------------|------|
| Stage compression | Chinese market lifecycles are typically 30-50% shorter than Western markets (capital + population dividend acceleration); growth phase may last only 2-3 years | Community group buying went from boom to shakeout in just 2 years (2020-2022) |
| Policy-driven transitions | Policy can change industry stages in a short time, directly skipping or compressing certain phases | "Double Reduction" jumped education into decline; carbon neutrality accelerated NEV into growth |
| Lower-tier market extension | When Tier 1 markets enter maturity, lower-tier markets may still be in growth, creating "stage stratification" across the industry | Food delivery is saturated in Tier 1 but still penetrating in county-level cities; live commerce follows the same pattern |
| Frequent second curves | Chinese companies are more adept at restarting the lifecycle through "cross-industry expansion" | Meituan: group buying → delivery → in-store → travel; ByteDance: news → short video → e-commerce |

---
## Common Mistakes

| Mistake | Correct Approach |
|---------|-----------------|
| Equating industry growth rate with stage | Use multiple indicators comprehensively; growth rate is just one of them |
| Ignoring sub-segment stage differences | Assess each sub-segment separately |
| Assuming lifecycle is linear and irreversible | Technology breakthroughs can restart the lifecycle (e.g., AI restarting fintech) |
| Only determining stage without deriving implications | Must output "so what should be done" |

---

## Integration with Other Frameworks

| Partner Framework | Relationship |
|-------------------|-------------|
| PESTEL | T (Technology) and L (Legal) factors often drive stage transitions |
| TAM/SAM/SOM | Industry stage affects SAM/SOM growth assumptions |
| Five Forces | Competitive force intensities differ across stages |
| Three Horizons | H1/H2/H3 allocation depends on the industry's current stage |
| Disruption Theory | Industries in decline are more vulnerable to disruption |

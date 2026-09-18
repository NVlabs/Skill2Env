# TAM/SAM/SOM | Market Sizing

**Creator/Source**: Venture Capital industry standard framework
**Core Value**: Layered estimation of market space to assess business growth ceilings and fundraising potential
**One-liner**: Not all markets are yours — TAM/SAM/SOM helps you calculate "how much you can capture"

---

> **Case Boundary**: Company/industry cases in this file are illustrative examples for framework structure and reasoning, not current factual claims by Alpha Insights. Before reusing any numbers, shares, dates, or conclusions in a live study, re-check sources and record them in the Evidence Claim Ledger.

## Overview

TAM/SAM/SOM is a classic layered market sizing framework used in venture capital and corporate strategy, originating from Silicon Valley's VC ecosystem and now a standard component of business plans and strategic planning.

**Core Design Principles**:
- **Layered Thinking**: Not all markets are yours — estimation must be layered
- **Real-World Constraints**: Progressively add constraint conditions from the theoretical maximum
- **Stage Matching**: Different development stages focus on different market layers

**Best Use Cases**:
- Market space estimation in business plans
- Market feasibility assessment for new businesses/products
- Market attractiveness presentation in fundraising pitches
- Growth ceiling assessment in corporate strategic planning

**Output Value**:
- Quantitative estimates for three market layers (TAM/SAM/SOM)
- Market penetration roadmap
- Growth headroom and ceiling assessment

**Key Insight**: TAM/SAM/SOM quality depends on data sources and assumption reasonableness. Avoid inflating TAM — clear calculation logic is essential.

---

## I. Framework Overview

### 1.1 TAM/SAM/SOM Structure

```
┌─────────────────────────────────────────────┐
│           Market Size Layers                │
├─────────────────────────────────────────────┤
│                                             │
│        ┌─────────────────────┐              │
│        │       TAM           │              │
│        │  Total Addressable  │              │
│        │    Market           │              │
│        │                     │              │
│        │  ┌───────────────┐  │              │
│        │  │     SAM       │  │              │
│        │  │ Serviceable   │  │              │
│        │  │ Addressable   │  │              │
│        │  │   Market      │  │              │
│        │  │  ┌─────────┐  │  │              │
│        │  │  │   SOM   │  │  │              │
│        │  │  │ Service- │  │  │              │
│        │  │  │ able     │  │  │              │
│        │  │  │ Obtain-  │  │  │              │
│        │  │  │ able Mkt │  │  │              │
│        │  │  └─────────┘  │  │              │
│        │  └───────────────┘  │              │
│        └─────────────────────┘              │
│                                             │
└─────────────────────────────────────────────┘
```

### 1.2 Three-Layer Market Definitions

| Layer | Definition | Core Question | Purpose |
|-------|-----------|---------------|---------|
| **TAM** | Theoretically maximum possible market | How high is the ceiling? | Assess track attractiveness |
| **SAM** | Market serviceable after capability/resource constraints | How much can you actually serve? | Set medium-term targets |
| **SOM** | Market actually obtainable after considering competition | How much can you capture short-term? | Set short-term targets |

### 1.3 Typical Ratios Across Three Layers

```
Typical Ratios (by stage):

Early-stage startup:
TAM : SAM : SOM = 100 : 10 : 1

Growth stage:
TAM : SAM : SOM = 100 : 30 : 10

Mature stage:
TAM : SAM : SOM = 100 : 50 : 30
```

---

## II. Three-Layer Market Detailed Analysis

### 2.1 TAM (Total Addressable Market)

**Definition**: The maximum market space a product or service could potentially reach under ideal conditions.

**Calculation Logic**:
```
TAM = Total potential customers × Average spend per customer

OR

TAM = Total industry size (if authoritative data exists)
```

**Estimation Methods**:
| Method | Description | Applicable Scenarios | Accuracy |
|--------|-----------|---------------------|----------|
| Top-down | Use industry report data | Mature industries | Medium |
| Bottom-up | Customer count × unit price | Emerging markets | High |
| Comparable | Benchmark against mature markets | New markets | Medium |

**Data Sources**:
| Source | Applicable Scenarios | Reliability |
|--------|---------------------|-------------|
| Government statistics | Macro data | High |
| Industry reports | Industry segments | Medium-High |
| Public company filings | Public markets | High |
| Third-party data | Internet industries | Medium |
| Expert interviews | Emerging markets | Medium |

**Cautions**:
```
⚠️ Common TAM estimation errors:
1. Market definition too broad → Inflated TAM
2. Ignoring willingness to pay → Demand without a market
3. Confusing users with customers → Decision-makers vs. end users
4. Ignoring geographic boundaries → National/global confusion
```

### 2.2 SAM (Serviceable Addressable Market)

**Definition**: The market actually serviceable after considering company capabilities, resources, and geographic constraints.

**Constraint Factors**:
```
┌─────────────────────────────────────────────┐
│          SAM Constraint Factors              │
├─────────────────────────────────────────────┤
│                                             │
│  1. Geographic constraints                  │
│     • Cities/regions covered                │
│     • Logistics reach                       │
│                                             │
│  2. Product constraints                     │
│     • Product line category coverage        │
│     • Technology capability boundaries      │
│                                             │
│  3. Channel constraints                     │
│     • Sales channel coverage capacity       │
│     • Online/offline channel footprint      │
│                                             │
│  4. Resource constraints                    │
│     • Team size                             │
│     • Capital limitations                   │
│                                             │
│  5. Regulatory constraints                  │
│     • Licenses and qualifications           │
│     • Industry access requirements          │
│                                             │
└─────────────────────────────────────────────┘
```

**Calculation Logic**:
```
SAM = TAM × Serviceable ratio

Serviceable ratio = f(geographic coverage, product fit, channel capability, resource constraints)
```

### 2.3 SOM (Serviceable Obtainable Market)

**Definition**: The market share actually obtainable in the short term after considering the competitive landscape.

**Determining Factors**:
```
┌─────────────────────────────────────────────┐
│          SOM Determining Factors             │
├─────────────────────────────────────────────┤
│                                             │
│  1. Competitive intensity                   │
│     • Number of competitors                 │
│     • Competitor strength                   │
│     • Market concentration                  │
│                                             │
│  2. Own competitiveness                     │
│     • Differentiation advantages            │
│     • Brand influence                       │
│     • Resource investment                   │
│                                             │
│  3. Market stage                            │
│     • Early market → High education costs   │
│     • Growth market → Fast but competitive  │
│     • Mature market → Stable structure      │
│                                             │
│  4. Time window                             │
│     • Entry timing                          │
│     • Competitive response speed            │
│                                             │
└─────────────────────────────────────────────┘
```

**Calculation Logic**:
```
SOM = SAM × Obtainable share

Obtainable share = f(competitiveness, competitive intensity, time window)
```

---

## III. TAM/SAM/SOM Execution Steps

### Step 1: Define Market Boundaries

**Goal**: Clarify market boundaries and scope.

**Definition Framework**:
```
Market Boundary 6 Dimensions:

1. Product boundary
   • Core products/services
   • Related categories

2. Geographic boundary
   • City/province/national/global
   • Tier-1/lower-tier markets

3. Customer boundary
   • B2B/B2C
   • Industry/demographic

4. Price boundary
   • Premium/mid-range/budget

5. Channel boundary
   • Online/offline

6. Time boundary
   • Current/next 3 years/next 5 years
```

### Step 2: Collect Data

**Goal**: Gather data needed for estimation.

**Data Source Priority**:
```
Data reliability ranking:

1. Official statistics (most reliable)
   • National Bureau of Statistics
   • Industry associations

2. Public company data
   • Annual reports, prospectuses
   • Securities research reports

3. Third-party data
   • iResearch, Analysys, QuestMobile
   • Consulting firm reports

4. Expert interviews
   • Industry experts
   • Practitioners

5. Primary research
   • User surveys
   • Competitive analysis
```

### Step 3: Select Estimation Method

**Goal**: Choose the appropriate method based on market characteristics.

**Method Selection Framework**:
```
Market type → Estimation method

Mature market:
├─ Authoritative data available → Top-down
└─ No authoritative data → Bottom-up

Emerging market:
├─ Comparable market exists → Comparable method
└─ No comparable market → Bottom-up + Expert interviews

Platform market:
└─ Two-sided market → Estimate both sides separately
```

### Step 4: Calculate TAM

**Goal**: Estimate the Total Addressable Market.

**Calculation Methods**:

#### Method 1: Top-Down
```
Formula: TAM = Total industry size

Example:
• China e-commerce market size: ¥13 trillion (2022)
• China cloud services market size: ¥300 billion (2022)

Pros: Fast, backed by authority
Cons: May be too broad, imprecise
```

#### Method 2: Bottom-Up
```
Formula: TAM = Total potential customers × Average spend per customer

Example:
• China middle-class households: 200 million
• Average annual education spending: ¥50,000
• TAM = 200M × ¥50,000 = ¥10 trillion

Pros: Precise, verifiable
Cons: High data acquisition cost
```

#### Method 3: Comparable
```
Formula: TAM = Comparable market size × Adjustment coefficient

Example:
• US SaaS market: $200 billion
• China GDP / US GDP ≈ 0.7
• China SaaS TAM ≈ $140 billion

Pros: Quick estimation for new markets
Cons: Adjustment coefficient hard to determine
```

### Step 5: Calculate SAM

**Goal**: Estimate the Serviceable Addressable Market.

**Calculation Framework**:
```
SAM = TAM × Serviceable ratio

Serviceable ratio = Geographic coverage × Product fit × Channel capability

Example:
• TAM: ¥100 billion
• Geographic coverage: 50% (tier-1 and tier-2 only)
• Product fit: 80% (products cover 80% of demand)
• Channel capability: 60% (channels reach 60% of customers)
• SAM = 100B × 50% × 80% × 60% = ¥24 billion
```

### Step 6: Calculate SOM

**Goal**: Estimate the Serviceable Obtainable Market.

**Calculation Framework**:
```
SOM = SAM × Obtainable share

Obtainable share = f(competitiveness, competitive intensity)

Competitiveness assessment:
┌────────────────────────────────┐
│ Factor          │ Weight │ Score│
├────────────────────────────────┤
│ Product strength│ 30%    │ /10  │
│ Brand strength  │ 20%    │ /10  │
│ Channel strength│ 20%    │ /10  │
│ Capital strength│ 15%    │ /10  │
│ Team strength   │ 15%    │ /10  │
└────────────────────────────────┘
Composite score = Σ(weight × score)

Obtainable share = Composite score / 10 × Competition adjustment coefficient
```

---

## IV. Output Format

### 4.1 Market Sizing Report

```markdown
## TAM/SAM/SOM Analysis - [Market/Business Name]

### Market Definition
- **Product boundary**: [...]
- **Geographic boundary**: [...]
- **Customer boundary**: [...]
- **Time boundary**: [...]

### TAM Estimation
- **Estimation method**: [Top-down/Bottom-up/Comparable]
- **Data sources**: [...]
- **Calculation process**: [...]
- **TAM size**: ¥XXX billion

### SAM Estimation
- **Constraint factors**:
  • Geographic constraints: [...]
  • Product constraints: [...]
  • Channel constraints: [...]
- **Serviceable ratio**: X%
- **SAM size**: ¥XXX billion

### SOM Estimation
- **Competitive landscape**: [...]
- **Competitiveness assessment**: [...]
- **Obtainable share**: X%
- **SOM size**: ¥XXX billion

### Market Attractiveness
- **TAM attractiveness**: [High/Medium/Low]
- **SAM achievability**: [High/Medium/Low]
- **SOM attainability**: [High/Medium/Low]
```

### 4.2 Market Penetration Roadmap

```markdown
## Market Penetration Roadmap

### Short-term Target (1 year)
- **SOM target**: ¥XXX billion
- **Market share**: X%
- **Key actions**: [...]

### Medium-term Target (3 years)
- **SAM penetration**: ¥XXX billion
- **Market share**: X%
- **Key actions**: [...]

### Long-term Vision (5 years)
- **TAM penetration**: ¥XXX billion
- **Market share**: X%
- **Key actions**: [...]
```

---

## Case Study: China Pet Food Market TAM/SAM/SOM Estimation (2024)

**Scenario**: A new brand plans to enter the domestic freeze-dried pet food segment and needs to estimate market space and validate commercial viability.

### TAM — Total Addressable Market

| Estimation Method | Calculation | Result |
|-------------------|-----------|--------|
| **Top-down** | China pet economy total market ~¥300B (2024, iResearch), pet food accounts for ~40% | **~¥120B** |
| **Bottom-up validation** | China urban pet cats and dogs ~120M × annual food spending ~¥1,000/pet | **~¥120B** ✅ Cross-validation passed |

**TAM Structure Breakdown**:

| Sub-category | Market Size | Share | YoY Growth |
|-------------|------------|-------|-----------|
| Staple food (dry + wet + freeze-dried) | ~¥60B | 50% | ~15% |
| Treats | ~¥30B | 25% | ~20% |
| Supplements/nutrition | ~¥10B | 8% | ~30% |
| Other (prescription food, etc.) | ~¥20B | 17% | ~10% |

### SAM — Serviceable Addressable Market

**Focus Track**: Freeze-dried staple pet food (carved from ¥60B staple food)

| Constraint Factor | Constraint Condition | SAM Calculation |
|-------------------|---------------------|----------------|
| Category constraint | Freeze-dried ~13% of staple food (growing rapidly) | ¥60B × 13% = **~¥8B** |
| Price band constraint | Positioned mid-to-premium (¥50-120/bag), covers ~70% of freeze-dried users | ¥8B × 70% = ~¥5.6B |
| Channel constraint | Online-only initially (Tmall/JD.com/Douyin), online = ~80% of freeze-dried sales | ¥5.6B × 80% = **~¥4.5B** |
| Geographic constraint | Tier-1 and tier-2 cities primarily (~75% of freeze-dried consumption) | Already included in channel constraint |

**SAM ≈ ¥4.5 billion**

### SOM — Serviceable Obtainable Market

| Competitive Landscape | Status |
|----------------------|--------|
| Leading brands | K9 Natural, Ziwi Peak (imported), Xiaoxiandun Pet, Maodali (domestic) |
| Market concentration | CR5 ~35%, market still fragmented |
| Competitive dynamics | Domestic substitution trend evident, but brand trust is the core barrier |

| Competitiveness Factor | Weight | Score (/10) | Weighted |
|-----------------------|--------|-------------|----------|
| Product strength (formula/ingredients) | 30% | 7 | 2.1 |
| Brand strength (new brand) | 20% | 3 | 0.6 |
| Channel strength (online operations) | 20% | 6 | 1.2 |
| Capital strength | 15% | 5 | 0.75 |
| Team strength | 15% | 6 | 0.9 |
| **Composite score** | | | **5.55/10** |

```
SOM = SAM × Obtainable share
    = ¥4.5B × (5.55/10 × Competition adjustment coefficient 0.15)
    ≈ ¥4.5B × 8.3%
    ≈ ¥370M (3-year target)
```

### Method Comparison

| Dimension | Top-down | Bottom-up |
|-----------|---------|-----------|
| TAM | Industry report ¥300B × 40% = ¥120B | 120M pets × ¥1,000 = ¥120B ✅ |
| SAM | Freeze-dried staple market ¥8B → constrained to ¥4.5B | Target users 3M × annual spend ¥1,500 = ¥4.5B ✅ |
| SOM | Share method: ¥4.5B × 8% ≈ ¥370M | Sales target: ¥30M/month × 12 = ¥360M ✅ |

### So What

1. **High track attractiveness**: Freeze-dried food YoY >30%, the fastest-growing pet food sub-category. TAM ceiling will continue expanding as staple food category penetration increases
2. **SOM achievable but conditional**: The ¥370M 3-year target requires validating two key assumptions —
   - **Customer acquisition cost**: Douyin/Tmall pet food CAC has risen to ¥80-120. Can ROI turn positive?
   - **Repurchase rate**: Freeze-dried food repurchase cycle ~45 days. Can brand loyalty sustain 40%+ annual repurchase?
3. **Risk point**: If leading general pet food brands (Royal Canin, Orijen) launch freeze-dried product lines, their brand trust advantage could rapidly squeeze new brand space — this is the biggest uncertainty in SOM estimation

---

## V. Common Mistakes

| Mistake Type | Manifestation | Correction |
|-------------|--------------|-----------|
| Market defined too broadly | "Trillion-dollar market" | Clarify boundaries, focus on segments |
| Confusing the three layers | TAM/SAM/SOM conflated | Clearly define each layer |
| Single data source | Only one source used | Multi-source cross-validation |
| Ignoring competition | SOM estimated too high | Factor in competitive intensity |
| Static estimation | Not considering growth | Estimate dynamic changes |
| Lacking basis | Arbitrary numbers | Provide calculation process |

---

## VI. Integration with Other Frameworks

| Upstream Framework | Input Content | This Framework's Output | Downstream Framework |
|-------------------|--------------|------------------------|---------------------|
| PESTEL | Macro trends | Market growth assumptions | Three Horizons |
| Industry research | Industry size | TAM estimation | Playing to Win |
| JTBD | Demand definition | Customer boundary | BMC |
| Competitive analysis | Competitive landscape | SOM share | SCP |

**Typical Combinations**:
- **Industry research**: PESTEL → TAM/SAM/SOM → SCP
- **Business opportunity discovery**: JTBD → TAM/SAM/SOM → BMC
- **Market entry**: TAM/SAM/SOM → Playing to Win → Three Horizons

---

## VII. China Market Specifics

| Dimension | China Characteristics | Case |
|-----------|----------------------|------|
| Large regional disparities | Significant spending power gap between tier-1 and lower-tier markets; TAM needs layered estimation | Luckin tier-1 city AOV ¥20 vs lower-tier ¥12 |
| Rapid change | Market growth generally faster than mature markets; estimates need dynamic adjustment | NEV penetration jumped from 15% to 40% within 3 years |
| Fragmented data | Limited authoritative public data; multi-source cross-validation needed | Industry data often requires combining statistics bureau, securities research, QuestMobile |
| Policy impact | Rapid policy changes can reshape entire TAM | "Double Reduction" policy directly eliminated a trillion-yuan education market |
| Lower-tier market upside | 600 million lower-income population represents massive incremental space | Pinduoduo proved lower-tier TAM was severely underestimated |
| Leading online penetration | China's online penetration leads globally; online SAM proportion is higher | Physical e-commerce penetration exceeds 30%, far above Western markets |
| Capital acceleration | VC/PE accelerates market education, shortening SOM ramp-up period | Community group buying achieved market education in 1 year through capital |

## External Research Supplement: TAM/SAM/SOM Best Practices

Based on mainstream VC and consulting firm research:

### 1. Three Calculation Methods

| Method | Description | Applicable Scenarios | Credibility |
|--------|-----------|---------------------|-------------|
| Top-down | Top-down derivation from macro data | Early-stage projects | Lower |
| Bottom-up | Bottom-up accumulation from unit economics | With operational data | High |
| Value theory | Based on value created for users | Disruptive innovation | Medium |

### 2. Bottom-up Calculation Template

TAM = Total target users × Average spend per customer; SAM = Reachable users × Unit price; SOM = SAM × Expected penetration rate

### 3. Common Errors

| Error | Manifestation | Correction |
|-------|--------------|-----------|
| TAM too large | "Trillion-dollar market" without logic | Use bottom-up to show calculations |
| Confusing TAM/SAM | Treating SAM as TAM | Clearly define constraint conditions |
| Static view | Only calculating current size | Add CAGR projections |

---

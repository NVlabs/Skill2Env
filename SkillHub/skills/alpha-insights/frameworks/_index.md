# Framework Index & Matching Rules (Framework Index)

> **Purpose**: Loaded during Stage 2 problem definition to match the most suitable analytical framework combination for research topics
>
> **Core Mechanism**: Primary Framework (analysis backbone) + Enhancement Framework (supplementary depth) + Optional Framework (add-on as needed)
>
> **Usage**: AI selects and loads framework combinations from this index based on research type and topic characteristics

---

> **Case Boundary**: Company/industry cases in this file are illustrative examples for framework structure and reasoning, not current factual claims by Alpha Insights. Before reusing any numbers, shares, dates, or conclusions in a live study, re-check sources and record them in the Evidence Claim Ledger.

## Framework Tier Definitions

| Tier | Symbol | Definition | Quantity Limit |
|------|--------|-----------|---------------|
| 🏗️ **Primary Framework** | Primary | Analysis backbone, provides complete structure; all analysis revolves around it | 1 |
| 🔧 **Enhancement Framework** | Enhancement | Supplements specific dimensions of the Primary Framework with depth; has explicit insertion points | 2-4 |
| 📎 **Optional Framework** | Optional | Added on-demand based on topic characteristics; not mandatory | 0-2 |

### Usage Principles

1. **Primary Framework is the backbone**: All analysis follows the Primary Framework's steps/dimensions; Enhancement Frameworks embed within it
2. **Enhancement Frameworks have insertion points**: Each Enhancement Framework clearly indicates which step/dimension of the Primary Framework it plugs into
3. **Not a parallel relationship**: Enhancement Frameworks serve the Primary Framework — they don't form standalone chapters but deepen analysis at specific steps
4. **Integrated synthesis**: Frameworks don't contradict each other; analysis comprehensively integrates and applies all selected frameworks
5. **User can override**: Stage 2 checkpoint presents the recommended combination to the user, who can add or remove frameworks

---

## Matching Process

```
User topic → Identify research scenario (can match 1-2 scenarios)
           → Load this file (Stage 2 Step 1)
           → Match Primary + Enhancement Frameworks by scenario
           → Present framework combination to user
           → User confirms (Stage 2 Step 2)
           → Deep-load selected framework files (obtain dimension structures)
           → Reference framework dimensions during MECE decomposition (Stage 2 Step 3)
              Ensure critical dimensions are not missed; N/A dimensions explicitly marked
           → Assign analytical lenses to each sub-question (Q→Framework dimension)
```

### N/A Dimension Judgment Criteria

Marking ➖ N/A requires BOTH conditions to be met:
1. **Weak relevance**: The dimension has no direct causal or constraining relationship with the core research question
2. **Low impact**: Even if that dimension changes significantly, it would not alter the core conclusions

> If either condition is not met, keep ⏳ and conduct targeted supplementary research in Layer 3. Better to over-search than to miss-mark.

### Multi-Scenario Matching Rules (Important)

A topic may simultaneously match 2 scenarios — **one is the purpose, the other is the method**. In this case:

**Priority**: Purpose scenario (5-9) > Method scenario (1-4)

| Scenario Type | Scenario Numbers | Meaning |
|--------------|-----------------|---------|
| **Method scenarios** | 1-4 (Industry Research, Competitive Analysis, Product Analysis, Business Model Analysis) | "What analytical approach to use" |
| **Purpose scenarios** | 5-9 (Opportunity Discovery, Market Entry, Investment Decision, Strategic Planning, Due Diligence) | "What decision the analysis serves" |

**Matching Rules**:
1. **Single scenario match** (common): Topic involves only one scenario → Use that scenario's framework combination directly
2. **Dual scenario match** (purpose ≠ method): Primary Framework comes from the **purpose scenario**; the method scenario's Primary Framework is demoted to Enhancement Framework
3. Scenario 10 (Special Topics) is a catch-all scenario and does not participate in dual-scenario matching

**Examples**:

| User Topic | Method Scenario | Purpose Scenario | Primary Framework | Enhancement Frameworks |
|-----------|----------------|-----------------|-------------------|----------------------|
| "Analyze competitive landscape of the second-hand recycling industry" | Competitive Analysis (2) | — | Five Forces | Competitive Positioning Map, SWOT |
| "Develop competitive strategy for Zhima Credit" | Competitive Analysis (2) | Strategic Planning (8) | **3A 8-Steps** (from Scenario 8) | Five Forces (demoted from Scenario 2), SWOT, Playing to Win |
| "Evaluate whether to invest in a SaaS company" | Business Model Analysis (4) | Investment Decision (7) | **3A 8-Steps** (from Scenario 7) | BMC (demoted from Scenario 4), Unit Economics, Five Forces |

---

## Ten Research Scenarios — Framework Combinations

---

### [Cognitive Foundation] — Understanding Industry, Competition, Product, Model

#### Scenario 1: Industry Research

> Keywords: industry panorama, market size, growth drivers, industry chain, key players

| Tier | Framework | Insertion Point | Purpose |
|------|-----------|----------------|---------|
| 🏗️ Primary | [3A 8-Steps Strategy](3a_8steps_strategy.md) | — | Eight-step panoramic analysis + 3A Strategic Synthesis, providing complete industry research backbone |
| 🔧 Enhancement | [PESTEL](pestel.md) | → Steps 1-2 (Industry Definition + Development Stage) | Supplement macro-environment six-dimension scan, deepen external factor analysis |
| 🔧 Enhancement | [Five Forces](porters_five_forces.md) | → Step 3 (Competitive Landscape) | Supplement competitive structure deep analysis, quantify five forces intensity |
| 🔧 Enhancement | [Industry Lifecycle](industry_lifecycle.md) | → Step 2 (Development Stage) | Supplement lifecycle stage determination with quantitative criteria and evolution curves |
| 🔧 Enhancement | [TAM/SAM/SOM](tam_sam_som.md) | → Step 1 (Industry Definition) | Supplement three-layer market size quantification |

📎 Optional add-ons:
- [SCP](scp.md) — For heavily regulated industries, supplement Step 3 with structure→conduct→performance causal chain
- [Value Chain](value_chain.md) — When deep-diving into value distribution across industry chain segments, supplement Step 4

---

#### Scenario 2: Competitive Analysis

> Keywords: competitive landscape, competitor strategies, differentiated positioning, competitive response

| Tier | Framework | Insertion Point | Purpose |
|------|-----------|----------------|---------|
| 🏗️ Primary | [Five Forces](porters_five_forces.md) | — | Five Forces model as backbone, systematically analyzing competitive structure and intensity |
| 🔧 Enhancement | [Competitive Positioning Map](competitive_positioning.md) | → Existing competition analysis | Visualize each player's relative position on key dimensions |
| 🔧 Enhancement | [SWOT](swot.md) | → Strategic Synthesis | Integrate internal and external factors to form competitive response strategy |

📎 Optional add-ons:
- [BCG Matrix](bcg_matrix.md) — Analyze competitors' business portfolios and investment priorities
- [Disruption Theory](disruption_theory.md) — Assess new entrants' disruption potential
- [SCP](scp.md) — Analyze structural causes behind competitive behavior

---

#### Scenario 3: Product Analysis

> Keywords: product features, user experience, product comparison, product iteration, product positioning

| Tier | Framework | Insertion Point | Purpose |
|------|-----------|----------------|---------|
| 🏗️ Primary | [JTBD](jtbd.md) | — | Build analysis backbone from user task perspective, understanding what jobs the product solves for users |
| 🔧 Enhancement | [Competitive Positioning Map](competitive_positioning.md) | → Competitive solution analysis | Visualize product's market position and differentiation space |
| 🔧 Enhancement | [Blue Ocean Strategy](blue_ocean_strategy.md) | → Value innovation opportunities | Use strategy canvas to discover differentiated value innovation space |

📎 Optional add-ons:
- [BMC](business_model_canvas.md) — Analyze the business model behind the product
- [Flywheel](flywheel.md) — Analyze the product's growth mechanism
- [Disruption Theory](disruption_theory.md) — Assess the product's disruption potential

---

#### Scenario 4: Business Model Analysis

> Keywords: business model decomposition, profitability logic, unit economics model

| Tier | Framework | Insertion Point | Purpose |
|------|-----------|----------------|---------|
| 🏗️ Primary | [BMC](business_model_canvas.md) | — | Nine-element panoramic decomposition of business model, providing analysis backbone |
| 🔧 Enhancement | [Unit Economics](unit_economics.md) | → Revenue Streams + Cost Structure | Quantify unit economics model, validate profitability sustainability |
| 🔧 Enhancement | [Flywheel](flywheel.md) | → Key Activities + Customer Relationships | Identify self-reinforcing growth loops |

📎 Optional add-ons:
- [Platform Canvas](platform_canvas.md) — For two-sided/multi-sided platform models, replaces BMC as Primary Framework
- [BCG Matrix](bcg_matrix.md) — Multi-product-line investment portfolio analysis
- [Value Chain](value_chain.md) — Analyze profit distribution across value chain segments

---

### [Opportunity Discovery] — Finding Value Gaps

#### Scenario 5: Business Opportunity Discovery

> Keywords: value gaps, unmet needs, emerging trends, entry points

| Tier | Framework | Insertion Point | Purpose |
|------|-----------|----------------|---------|
| 🏗️ Primary | [3A 8-Steps Strategy](3a_8steps_strategy.md) | — | Eight-step industry panorama scan + 3A convergence for opportunity assessment |
| 🔧 Enhancement | [JTBD](jtbd.md) | → Step 8 (User Research) | Deep-dive into unmet needs from user task perspective |
| 🔧 Enhancement | [Blue Ocean Strategy](blue_ocean_strategy.md) | → Step 3 (Competitive Landscape) | Use strategy canvas to discover competitive whitespace and value innovation opportunities |
| 🔧 Enhancement | [Three Horizons](three_horizons.md) | → 3A Strategic Synthesis | Categorize opportunities into near/mid/long-term horizons, forming an investment portfolio |

📎 Optional add-ons:
- [Disruption Theory](disruption_theory.md) — Assess low-end/new-market disruption opportunities
- [Competitive Positioning Map](competitive_positioning.md) — Visualize competitive whitespace
- [Industry Lifecycle](industry_lifecycle.md) — Determine entry timing

---

### [Strategic Decisions] — Making Critical Choices

#### Scenario 6: Market Entry Strategy

> Keywords: new market, new business, feasibility assessment, entry path

| Tier | Framework | Insertion Point | Purpose |
|------|-----------|----------------|---------|
| 🏗️ Primary | [3A 8-Steps Strategy](3a_8steps_strategy.md) | — | Systematically understand the industry + form "enter/don't enter" 3A strategic judgment |
| 🔧 Enhancement | [PESTEL](pestel.md) | → Steps 1-2 (Industry Definition + Development Stage) | Assess target market's macro-environment risks and opportunities |
| 🔧 Enhancement | [Playing to Win](playing_to_win.md) | → 3A Strategic Synthesis | Clarify Where to Play / How to Win strategic choices |
| 🔧 Enhancement | [SWOT](swot.md) | → 3A Strategic Synthesis | Comprehensively assess entry feasibility, form strategic judgment |

📎 Optional add-ons:
- [TAM/SAM/SOM](tam_sam_som.md) — Quantify target market size
- [Three Horizons](three_horizons.md) — Determine entry timing and investment pacing
- [Industry Lifecycle](industry_lifecycle.md) — Target market maturity assessment

---

#### Scenario 7: Investment Decision Support

> Keywords: investment due diligence, investment value assessment, valuation analysis, investment recommendations

| Tier | Framework | Insertion Point | Purpose |
|------|-----------|----------------|---------|
| 🏗️ Primary | [3A 8-Steps Strategy](3a_8steps_strategy.md) | — | Systematically analyze target company's industry + 3A assessment of investment attractiveness |
| 🔧 Enhancement | [Five Forces](porters_five_forces.md) | → Step 3 (Competitive Landscape) | Assess competitive intensity and profit pool of target company's industry |
| 🔧 Enhancement | [BMC](business_model_canvas.md) | → Steps 5-6 (Profitability Model + Channels) | Decompose target company's business model |
| 🔧 Enhancement | [Unit Economics](unit_economics.md) | → Step 5 (Profitability Model) | Validate business model's unit economics sustainability |
| 🔧 Enhancement | [SWOT](swot.md) | → 3A Strategic Synthesis | Comprehensively assess investment risks and opportunities |

📎 Optional add-ons:
- [TAM/SAM/SOM](tam_sam_som.md) — Quantify market opportunity
- [BCG Matrix](bcg_matrix.md) — Multi-business-line company portfolio analysis
- [Industry Lifecycle](industry_lifecycle.md) — Determine industry stage and growth potential

---

### [Planning & Execution] — Implementation

#### Scenario 8: Strategic Planning

> Keywords: annual plan, three-year plan, strategic goals, strategic roadmap

| Tier | Framework | Insertion Point | Purpose |
|------|-----------|----------------|---------|
| 🏗️ Primary | [3A 8-Steps Strategy](3a_8steps_strategy.md) | — | Eight-step analysis provides factual foundation for strategy + 3A forms strategic judgment |
| 🔧 Enhancement | [Playing to Win](playing_to_win.md) | → 3A Strategic Synthesis | Five-layer cascade clarifying strategic choices: Where to Play + How to Win |
| 🔧 Enhancement | [Three Horizons](three_horizons.md) | → 3A Strategic Synthesis | Plan near/mid/long-term growth portfolio and investment pacing |
| 🔧 Enhancement | [SWOT](swot.md) | → 3A Strategic Synthesis | Integrate internal and external factors, validate strategic feasibility |

📎 Optional add-ons:
- [Flywheel](flywheel.md) — Design strategic growth flywheel
- [Blue Ocean Strategy](blue_ocean_strategy.md) — Discover differentiated strategic direction
- [BCG Matrix](bcg_matrix.md) — Multi-business-line investment portfolio optimization

---

#### Scenario 9: Due Diligence

> Keywords: DD, risk audit, compliance review, background investigation

| Tier | Framework | Insertion Point | Purpose |
|------|-----------|----------------|---------|
| 🏗️ Primary | [3A 8-Steps Strategy](3a_8steps_strategy.md) | — | Eight-step panoramic audit + 3A assessment of target's overall feasibility |
| 🔧 Enhancement | [PESTEL](pestel.md) | → Steps 1-2 (Industry Definition + Development Stage) | Scan macro-environment risks (policy, regulation, compliance) |
| 🔧 Enhancement | [Five Forces](porters_five_forces.md) | → Step 3 (Competitive Landscape) | Assess industry competitive risk and profit pool stability |
| 🔧 Enhancement | [BMC](business_model_canvas.md) | → Steps 5-6 (Profitability Model + Channels) | Identify business model vulnerabilities and dependency risks |
| 🔧 Enhancement | [SWOT](swot.md) | → 3A Strategic Synthesis | Consolidate all risks and opportunities, form DD conclusion |

📎 Optional add-ons:
- [Unit Economics](unit_economics.md) — Validate financial sustainability
- [Value Chain](value_chain.md) — Analyze supply chain risks
- [SCP](scp.md) — Analyze regulatory risks

---

### [Specialized Advisory] — Issue Resolution

#### Scenario 10: Special Topics

> **Sub-types and Keywords** (auto-match framework after keyword recognition):
>
> | Sub-type | Keyword Examples | Primary Framework | Rationale |
> |----------|-----------------|-------------------|----------|
> | **Concept clarification** | "What exactly is XX", "What's the difference between XX and YY" | [Issue Tree](../methodology/issue_tree.md) (specialized as "Define → Compare → Judge" three-step) | The task is cognitive decomposition, not strategic decision-making; heavy frameworks create empty spins |
> | **Policy interpretation** | "What's the current status of XX policy", "How does XX policy affect us" | [Playing to Win](playing_to_win.md) | Need to analyze policy constraints on strategic choices |
> | **Trend assessment** | "Will XX disrupt the industry", "How will XX trend develop" | [Playing to Win](playing_to_win.md) | Need to infer changes in WTP/HTW direction |
> | **Event impact** | "What impact does XX event have on the industry" | [Playing to Win](playing_to_win.md) | Need structured assessment of event impact on strategic space |
> | **Decision advisory** (no clear action intent) | "Is XX direction worth watching" | [Playing to Win](playing_to_win.md) | Need to first clarify whether it's worth playing |

> **Lightweight process for concept-clarification questions (replaces PTW cascade)**:
> ```
> Step 1: Definition decomposition (What) — Use Issue Tree to break the core concept into 2-4 dimensions
> Step 2: Comparative judgment (So What) — For comparison questions, establish criteria (1-3 core differentiating dimensions) and compare each
> Step 3: Deliver conclusion (conclusion-first) — One-sentence core judgment + applicability boundaries/exception notes
> ⚠️ Do NOT cascade into five-layer "Winning Aspiration → WTP → HTW → Capabilities → Management Systems"
> ```

> **Boundary exclusions**:
> - ❌ Clear "entry" intent → Scenario 6 (Market Entry Strategy)
> - ❌ Clear "investment" intent → Scenario 7 (Investment Decision Support)
> - ❌ Targeting competitors → Scenario 2 (Competitive Analysis)
> - ❌ Targeting specific products → Scenario 3 (Product Analysis)
> - ❌ Internal strategy formulation → Scenario 8 (Strategic Planning)

| Tier | Framework | Insertion Point | Purpose |
|------|-----------|----------------|---------|
| 🏗️ Primary | [Playing to Win](playing_to_win.md) / [Issue Tree](../methodology/issue_tree.md) (concept clarification) | — | Structured analysis (see sub-type table above) |
| 🔧 Enhancement | [SWOT](swot.md) | → Strategic Synthesis | Integrated analysis to form judgment |

📎 Dynamic enhancement: Select from other scenarios' frameworks based on topic nature
- Policy interpretation → Layer on [PESTEL](pestel.md)
- Trend assessment → Layer on [Industry Lifecycle](industry_lifecycle.md)
- Event impact → Layer on [Five Forces](porters_five_forces.md)
- Needs industry panorama → Upgrade to 3A 8-Steps Strategy as Primary Framework

---

## Growth Direction Quick Classifier (Ansoff Matrix)

During Stage 2 problem definition, quickly classify growth direction type to assist framework selection:

```
                   Existing Products    New Products
              ┌──────────────┬──────────────┐
 Existing     │  Market        │  Product       │
 Markets      │  Penetration   │  Development   │
              │  → Scenario 2/4│  → Scenario 3/4│
              ├──────────────┼──────────────┤
 New          │  Market        │  Diversi-      │
 Markets      │  Development   │  fication      │
              │  → Scenario 6  │  → Scenario 1+6│
              └──────────────┴──────────────┘
```

| Growth Type | Recommended Add-on Frameworks |
|-------------|------------------------------|
| Market Penetration | Competitive Positioning Map + Flywheel |
| Product Development | JTBD + BMC |
| Market Development | PESTEL + TAM/SAM/SOM + Playing to Win |
| Diversification | Full Industry Research + Playing to Win + Three Horizons |

> **Scenario number reference**: 1 Industry Research, 2 Competitive Analysis, 3 Product Analysis, 4 Business Model Analysis, 5 Business Opportunity Discovery, 6 Market Entry Strategy, 7 Investment Decision Support, 8 Strategic Planning, 9 Due Diligence, 10 Special Topics

---

## 3A 8-Steps Strategy — Enhancement Framework Insertion Point Quick Reference

> When 3A 8-Steps Strategy is the Primary Framework (Scenarios 1, 5, 6, 7, 8, 9), Enhancement Framework embedding positions:

| Eight Steps | Analysis Content | Embeddable Enhancement Frameworks |
|-------------|-----------------|----------------------------------|
| Step 1: Industry Definition & Classification | Define boundaries, segment tracks | TAM/SAM/SOM (market size quantification), PESTEL (macro environment) |
| Step 2: Development Stage & Trends | Lifecycle stage determination | Industry Lifecycle (stage quantification), PESTEL (trend drivers) |
| Step 3: Competitive Landscape | Concentration, five forces | Five Forces (competitive depth), Blue Ocean Strategy (competitive whitespace), Competitive Positioning Map (visualization) |
| Step 4: Value Chain | Industry chain, value distribution | Value Chain (segment deep-dive) |
| Step 5: Profitability Model | Gross margin, cost structure | BMC (model decomposition), Unit Economics (unit economics quantification) |
| Step 6: Channels | Online/offline, direct/distribution | BMC (channel element) |
| Step 7: Merchant Profile | B-side customer profiles | — (covered by Primary Framework itself) |
| Step 8: User Research | User profiles, pain points | JTBD (user task deep-dive) |
| 3A Strategic Synthesis | Aspiration/Ability/Accessibility | Playing to Win (strategic choices), SWOT (comprehensive assessment), Three Horizons (time-horizon planning) |

**Usage Instructions**:
- When analysis reaches a specific step of the Primary Framework, automatically embed the corresponding Enhancement Framework's analytical dimensions
- Enhancement Frameworks don't form standalone chapters but deepen the Primary Framework's output at that step
- Example: When analyzing Step 3 (Competitive Landscape), embed Five Forces' five-force quantitative assessment within the 3A 8-Steps' competitive landscape analysis

---

## Framework Quick Reference Table

### Original Framework

| Framework | File | Core Value | Scenarios as Primary Framework |
|-----------|------|-----------|-------------------------------|
| **3A 8-Steps Strategy** | [3a_8steps_strategy.md](3a_8steps_strategy.md) | Complete methodology integrating 3A strategic perspective with eight-step analysis process | Scenarios 1, 5, 6, 7, 8, 9 |

> **Note**: The former `3a_strategy.md` (3A Strategic Matching Framework) and `industry_8steps.md` (Industry Research Eight Steps) have been consolidated into this framework and are no longer used separately.

### Classic Frameworks

| Framework | File | Core Value | Typical Role |
|-----------|------|-----------|-------------|
| Porter's Five Forces | [porters_five_forces.md](porters_five_forces.md) | Industry competitive intensity and profit pool analysis | Scenario 2 Primary / Multi-scenario Enhancement |
| Value Chain | [value_chain.md](value_chain.md) | Industry chain value distribution and strategic control points | Optional Enhancement |
| BMC | [business_model_canvas.md](business_model_canvas.md) | Nine-element business model panoramic decomposition | Scenario 4 Primary / Multi-scenario Enhancement |
| TAM/SAM/SOM | [tam_sam_som.md](tam_sam_som.md) | Three-layer market size quantification | Enhancement (Step 1) |
| Blue Ocean Strategy | [blue_ocean_strategy.md](blue_ocean_strategy.md) | Value innovation and differentiated competition space | Enhancement |
| Unit Economics | [unit_economics.md](unit_economics.md) | Unit economics model and profitability sustainability | Enhancement (Step 5) |
| PESTEL | [pestel.md](pestel.md) | Macro-environment six-dimension scan | Enhancement (Steps 1-2) |
| SWOT | [swot.md](swot.md) | Internal/external factor strategic synthesis | Enhancement (Strategic Synthesis) |
| SCP | [scp.md](scp.md) | Industry structure→conduct→performance causal chain | Optional Enhancement |
| Industry Lifecycle | [industry_lifecycle.md](industry_lifecycle.md) | Industry evolution stage determination | Enhancement (Step 2) |
| Competitive Positioning Map | [competitive_positioning.md](competitive_positioning.md) | Two-dimensional competitive position visualization | Enhancement |
| BCG Matrix | [bcg_matrix.md](bcg_matrix.md) | Business portfolio investment prioritization | Optional Enhancement |

### Modern Frameworks

| Framework | File | Core Value | Typical Role |
|-----------|------|-----------|-------------|
| JTBD | [jtbd.md](jtbd.md) | Demand-side "user task" insight | Scenario 3 Primary / Enhancement (Step 8) |
| Flywheel | [flywheel.md](flywheel.md) | Self-reinforcing growth loop design | Enhancement |
| Platform Canvas | [platform_canvas.md](platform_canvas.md) | Platform/ecosystem business model analysis | Scenario 4 Optional Primary (replaces BMC) |
| Disruption Theory | [disruption_theory.md](disruption_theory.md) | Disruptive innovation threat and opportunity assessment | Optional Enhancement |
| Three Horizons | [three_horizons.md](three_horizons.md) | Multi-time-horizon growth investment portfolio | Enhancement (Strategic Synthesis) |
| Playing to Win | [playing_to_win.md](playing_to_win.md) | Five-layer strategic choice cascade | Scenario 10 (policy/trend/event/advisory) Primary / Enhancement (Strategic Synthesis) |
| Issue Tree | [methodology/issue_tree.md](../methodology/issue_tree.md) | Structured problem decomposition | Scenario 10 (concept-clarification) Lightweight Primary |

---

## Interfaces with Other Modules

### Input
| Upstream | Input Content | Usage |
|----------|--------------|-------|
| Stage 1 user_brief | Research type, topic keywords | Match research scenario |
| User preferences | Frameworks user specifies or excludes | Override default selection |

### Output
| Downstream | Output Content | Usage |
|------------|---------------|-------|
| Stage 2 research_definition | Selected frameworks + dimension coverage check + sub-question lens assignments + N/A dimension annotations | Written to research definition document |
| Stage 3 research_plan | Hypothesis analytical lens annotations (Q→H→Lens mapping) | Written to research plan |
| Stage 4 evidence_base | Framework evidence map initialization (auto-generated from H→Lens mapping) | Layer 1 Step 1.0 |
| Stage 5 insights | Framework analysis conclusions + cross-framework discoveries | Structured input for insight generation |
| `methodology/_index.md` | After framework combination is determined | Auto-match Tier 1/Tier 2 methodology |

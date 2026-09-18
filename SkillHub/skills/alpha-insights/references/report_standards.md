# Report Standards

> **Purpose**: Quality standards for Stage 6 report generation
>
> **Usage**: Ensure reports are professional, clear, insightful, and actionable

---

## Report Structure Standards

### Standard Structure (Seven-Section Format)

```
1. Executive Summary (1 page, no more than 1 page)
2. Research Background & Methodology (1 page)
3. Core Analysis Chapters (4-5 chapters, 3-5 pages each)
4. Key Insights & Recommendations (2-3 pages)
5. Risks & Mitigation (1 page)
6. Blind Spot Review (1 page)
7. Evidence Appendix
```

### Chapter Standards

#### 1. Executive Summary

**Must include**:
- Core conclusion (1 sentence, with a clear viewpoint)
- 3-5 key insights (each ≤2 lines)
- Action recommendations (prioritized)
- Key data support (2-3 core figures)

**Writing standards**:
- Standalone readable: core conclusions understandable without reading the full report
- Conclusion-first: first sentence is the core judgment
- Data-backed: every insight has specific data

**❌ Bad example**:
> This report analyzes the XX industry, finding that the market is growing, competition is intensifying, and the company should strengthen its competitiveness...

**✅ Good example**:
> **Core Conclusion**: Recommend entering the pet insurance market within 12 months — the window is closing.
> - Insight 1: Market CAGR 35%, but CR5 already at 60%, window period ~18 months
> - Insight 2: Existing players have clear gaps in product innovation and service experience
> - Insight 3: 40% of our existing customers express demand for pet insurance
> - Recommendation: Launch product design in Q2, pilot in Q4, budget XXX million

---

#### 2. Research Background & Methodology

**Must include**:
- Research question (from Stage 2)
- Analytical frameworks (list frameworks used + N/A dimension explanations)
- Data sources (count of P0/P1/P2 level sources)
- Verification level (proportion of A/B grade data)

---

#### 3. Core Analysis Chapters

**Structure standard**:
```
Chapter X: [Chapter Title]

X.1 Core Findings (1 paragraph, conclusion-first)
X.2 Data Evidence (charts + key metrics, Tier 3 ≥1 ECharts per chapter)
X.3 Dimension Breakdown (expand ≥1 level of sub-dimensions, Tier 3 ≥2 paragraphs per dimension)
X.4 Comparative Anchoring (≥1 set of reference points, Tier 3 each comparison includes data table or chart)
X.5 So What Analysis (implication interpretation, ≥2 layers of reasoning; core insight chapters ≥3 layers. Tier 3 each layer as separate paragraph, no merging)
X.6 Relevance to Us (context anchoring, Tier 3 ≥2 paragraphs: impact assessment + action implications)
```

**X.3 Dimension Breakdown (prevent "giving only totals without expansion")**:
- Market size → Break down by segment/region/customer group
- Competitive landscape → Break down by player/market tier/business model
- User behavior → Break down by scenario/frequency/willingness to pay
- **Tier requirements**: Tier 1 may omit | Tier 2 ≥1 dimension | Tier 3 ≥2 dimensions (target 3+, each dimension expanded in its own paragraph)

**X.4 Comparative Anchoring (prevent "absolute numbers without context")**:
- Temporal comparison: YoY/QoQ/CAGR
- Competitor comparison: metric comparison with key competitors
- Industry comparison: vs. industry average/benchmark companies
- Cross-market comparison: mature vs. emerging markets, international vs. domestic
- **Tier requirements**: Tier 1 may omit | Tier 2 ≥1 comparison set | Tier 3 ≥2 comparison sets (target 3+, each with quantitative data)

**Writing standards**:
- Each chapter focuses on one insight theme (most insight themes correspond to a single sub-question; rare cross-question insights may form independent chapters)
- Chapter titles are judgments or findings (e.g., "Market Consolidation Creates a Three-Year Window"), not sub-questions or framework names
- Every chapter has dimension breakdown (not just one aggregate number)
- Every chapter has comparative anchoring (not just absolute values)
- Every chapter has a clear So What
- Every chapter answers "Relevance to Us"

**Framework presentation in reports**:
- "Research Background & Methodology" chapter: explicitly list framework combinations used + N/A dimension explanations (demonstrating methodological rigor)
- Core analysis chapters: frameworks used as analytical tools within chapters, not as chapter titles
- N/A dimension handling: one sentence in parentheses (e.g., "Environmental dimension has no direct relevance to this analysis and was excluded"), demonstrating completeness and intellectual honesty

---

#### 4. Key Insights & Recommendations

**Insight standards** (from judgment_rules.md):
- Specificity: supported by data/cases
- Uniqueness: non-obvious findings
- Actionability: translatable into specific actions
- Impact: influences key decisions

**Insight tiers** (aligned with Stage 5 `insights.md`):
- **A-class core insights** (18-20 points): expanded in depth across main report chapters
- **B-class core insights** (16-17 points): presented concisely, grouped by theme

**Recommendation standards**:
- Complete 5W1H: What/Why/Who/When/Where/How
- Clear prioritization: P0/P1/P2 ranking
- ROI estimates: quantified input-output estimates
- Risk flagging: key risks and mitigation strategies

---

#### 5. Risks & Mitigation

**Must include**:
- Major risks (3-5 items)
- Probability (High/Medium/Low)
- Impact level (High/Medium/Low)
- Mitigation strategies (specific actions)

---

#### 6. Evidence Appendix

**Must include**:
- Data source list (labeled by priority level)
- Verification level labels (A/B/C/D)
- Supplementary analysis (supporting but non-core content)

---

## Chart Standards

### Chart Selection Principles

| Purpose | Recommended Chart |
|---------|------------------|
| Show trends | Line chart, area chart |
| Compare data | Bar chart, horizontal bar chart |
| Show proportions | Pie chart, donut chart |
| Relationship analysis | Scatter plot, bubble chart |
| Process display | Flowchart |
| Structure breakdown | Tree diagram, pyramid chart |
| Competitive positioning | 2D matrix chart |
| Market sizing | Funnel chart |

### Chart Quality Standards

- **Clear titles**: Chart titles state the core finding, not "XX Market Size" but "Market Size 5-Year CAGR 25%"
- **Data labels**: All data points cite their sources
- **Consistent colors**: Same meaning uses same color throughout the report
- **Simplicity first**: Avoid excessive decoration, highlight the data itself

---

## Language Standards

### Writing Principles

1. **Conclusion-first**: First sentence of each paragraph is the conclusion
2. **Data-backed**: Every judgment has data/evidence
3. **Avoid vagueness**: Don't use "maybe", "roughly", "approximately"
4. **Active voice**: Use active sentences, not passive
5. **Concise expression**: Each sentence ≤30 words

### Prohibited Expressions

| Vague Expression | Replacement |
|-----------------|-------------|
| "maybe", "roughly" | Provide probability: "approximately 70% likelihood" |
| "rapid growth" | "CAGR 25%" |
| "market leader" | "No.1 market share at 35%" |
| "strengthen competitiveness" | "Specific action: invest XXX million to build XX capability" |
| "seize opportunities" | "Specific action: enter market in Q2, target X% market share" |

---

## Chapter Material Type Reference Menu

> **Purpose**: Reference for writing chapter blueprints in Stage 3 (not a constraint). AI selects applicable types from the menu and may also add custom items not listed here.

| Material Type | Description | Common Use Cases |
|--------------|-------------|-----------------|
| Market Size Breakdown | TAM/SAM/SOM + segments + drivers + growth rate | Market overview, opportunity assessment |
| Player Landscape | List major entities by category (≥10), with brief positioning | Competitive landscape, supply side |
| Entity Deep Profiles | Top N entities × multi-dimension detailed descriptions (product/pricing/customers/differentiation/weaknesses) | Competition, benchmarking |
| Quantitative Comparison Table | ≥3 entities × ≥4 metrics in structured comparison | Competition, benchmarking, selection |
| Positioning Matrix | 2-axis scatter/quadrant chart data (axis definitions + entity coordinate rationale) | Competitive positioning, market segmentation |
| Time Trends | ≥3 years of data + inflection points/driver annotations | Market trends, technology evolution |
| User/Demand Profiles | Layered description by scenario/segment/frequency/willingness to pay | Demand analysis, user research |
| Cases/Stories | ≥2 specific cases with background, approach, and outcomes | Strategy validation, pattern recognition |
| Value Chain/Process Map | Stage breakdown + player distribution/value capture per stage | Industry analysis, business models |
| Policy/Regulatory Environment | Regulations, compliance requirements, policy trends and impact | Macro analysis, market entry assessment |
| Technology Approach Comparison | Technology roadmap/architecture/capability matrix comparison | Technology selection, trend assessment |
| Financial/Unit Economics | Cost structure, revenue model, margins, break-even | Business model, investment decisions |
| Scenario Analysis | Optimistic/base/pessimistic scenarios + key assumptions + projections | Forecasting, risk assessment |

---

## Chapter Self-Check (7 Items)

After generating each chapter, mandatory self-check:

- [ ] **Relevance**: Does it directly support the core research question?
- [ ] **Evidence**: Is it backed by data/evidence?
- [ ] **Dimension breakdown**: Has it expanded at least 1 level of sub-dimensions? (Can't just give a total and stop)
- [ ] **Comparative anchoring**: Does it have at least 1 set of reference points? (YoY/competitor/industry average/cross-market)
- [ ] **So What**: Is there a clear implication interpretation? (Standard chapters ≥2 layers; core insight chapters ≥3 layers, aligned with Stage 5)
- [ ] **Anti-pattern scan**: Check each paragraph against the 10 anti-patterns from `anti_patterns.md` — if any hit, immediately rewrite that paragraph
- [ ] **Context anchoring**: Does it answer "Relevance to Us"?

---

## Output Tier Standards

> Tiers are confirmed by the user in Stage 1, written to `user_brief.md`, and control depth and length throughout the entire workflow.

### Three-Tier Definitions

| Tier | Name | Length | Structure Requirements | Stage 4 Depth | Stage 5 Rules | Chart Count |
|------|------|--------|----------------------|---------------|---------------|-------------|
| **Tier 1** | Quick Scan | 1-2 pages | Executive Summary only | Layer 1 | All 8 rules | 0-2 |
| **Tier 2** | Topic Brief | 5-8 pages | Condensed seven-section (1 page/chapter) | Layer 1-2 | All 8 rules | 3-5 |
| **Tier 3** | Deep Report | 20-35 pages | Full seven-section (3-5 pages/chapter) | Layer 1-2-3 | All 8 rules | 6-12 |

### Tier 3 Page Budget Reference

| Section | Pages | Notes |
|---------|-------|-------|
| Executive Summary | 1 | Standalone readable, max 1 page. Core figures + insights + recommendations |
| Research Background & Methodology | 1 | Framework combinations + N/A explanations + data source overview |
| Core Analysis Chapters | 12-25 | 4-5 chapters × 3-5 pages, report body |
| Key Insights & Recommendations | 2-3 | A-class expanded individually, B-class grouped by theme |
| Risks & Mitigation | 1 | 3-5 risks + mitigation strategies |
| Blind Spot Review | 1 | Framework dimension coverage gaps + data blind spots |
| Evidence Appendix | 2-3 | Data sources + verification levels + supplementary analysis |
| **Total** | **20-35** | |

> Core analysis chapters should account for 60-70% of total length. If core chapters are under 12 pages, dimension breakdowns or comparative anchoring need more expansion.

### Chapter Selection by Tier

| Section | Tier 1 | Tier 2 | Tier 3 |
|---------|--------|--------|--------|
| Executive Summary | ✅ Full | ✅ Full | ✅ Full (≤1 page) |
| Research Background & Methodology | ❌ | ✅ Condensed (half page) | ✅ Full (1 page) |
| Core Analysis Chapters | ❌ | ✅ 2-3 chapters (1 page each) | ✅ 4-5 chapters (3-5 pages each) |
| Key Insights & Recommendations | ✅ Merged into Summary | ✅ Standalone chapter | ✅ Standalone chapter + detailed 5W1H |
| Risks & Mitigation | ❌ | ✅ Condensed (half page) | ✅ Full (1 page) |
| Evidence Appendix | ❌ | ❌ | ✅ Full |
| Blind Spot Review | ❌ | ✅ Brief notes | ✅ Standalone chapter |

### Quality Standards Do Not Decrease with Tier

Regardless of tier, these standards remain constant:
- Conclusion-first (first sentence is a judgment)
- Data-backed (every judgment has a source)
- Core data ≥ B-grade verification
- No "correct platitudes"

---

## HTML Format Standards

### Style Requirements

- **Page-based layout**: Cover page → Table of contents → Chapter pages → Footer page, read page by page
- **Responsive**: Supports desktop and mobile reading
- **Visualization**: All charts use ECharts (line, bar, pie, radar, etc.); layout components use CSS (data cards, highlight boxes, etc.)
- **Exportable**: Supports printing to PDF (automatic pagination)

### Structure Requirements

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <title>Report Title</title>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <!-- Styles (inline, see report_template.html) -->
</head>
<body>
  <div class="page cover-page"><!-- Cover --></div>
  <div class="page toc-page"><!-- Table of Contents --></div>
  <div class="page chapter-section"><!-- Chapters (multiple) --></div>
  <div class="page footer-page"><!-- Footer --></div>
</body>
</html>
```

### Available CSS Layout Components

| Component | CSS Class | Purpose |
|-----------|----------|---------|
| Highlight box | `.highlight-box` / `.yellow` / `.red` / `.green` | Core findings, risk alerts |
| Data cards | `.stats-grid` + `.stat-card` | Key data display |
| Chart container | `.chart-container` | ECharts chart wrapper |
| Strategy cards | `.strategy-card.blue/green/yellow/red` | Action recommendations |
| Insight cards | `.insight-card` | Finding → Implication → Recommendation |
| Data tables | `.data-table` | Structured data |
| Tags | `.tag-p0` / `.tag-p1` / `.badge-high/medium/low` | Priority, risk level |

> ⚠️ All data visualization charts (bar, pie, line, radar, etc.) use ECharts exclusively. CSS charts are not used.

### ECharts Charts

> **Purpose**: All data visualizations use ECharts exclusively. Tier 2 ≥3, Tier 3 ≥6.
> `report_template.html` includes a built-in ECharts CDN. Generate reports using `report_template.html` + `scripts/report_helper.py`; `report_demo.html` is a legacy layout reference only, not the ECharts standard example.

**Recommended chart types**:

| Analysis Scenario | Recommended Chart | ECharts type |
|-------------------|------------------|-------------|
| Market size trends | Line/area chart | `line` |
| Competitor comparison | Bar chart (grouped) | `bar` |
| Market share distribution | Pie/donut chart | `pie` |
| Competitive positioning | Scatter plot | `scatter` |
| Multi-dimensional comparison | Radar chart | `radar` |
| Industry chain/flow | Sankey diagram | `sankey` |
| Trend + comparison | Dual-axis (bar+line) | `bar` + `line` |

**⚠️ Generation method (mandatory: Python + step-by-step generation)**:

Report HTML must be written to file via **Python scripts**. **Recommended: `ReportBuilder` step-by-step generation**:

```python
# ━━━ Recommended: ReportBuilder step-by-step ━━━
# Each step is one Bash call, adding only 1-2 chapters per step
import sys, os; sys.path.insert(0, 'scripts')
from report_helper import ReportBuilder

# Step 1: Initialize (determine workspace absolute path)
ws = os.path.join(os.getcwd(), 'workspace', '{project}')
os.makedirs(ws, exist_ok=True)
b = ReportBuilder("Report Title", "Subtitle")
b.set_toc_conclusion("Core conclusion")
b.save_state("/tmp/rpt.json")

# Step 2-N: Add chapters step by step (one Bash call per step)
b = ReportBuilder.load_state("/tmp/rpt.json")
b.add_chapter(1, "Executive Summary", "<h2>Core Conclusion</h2><p>...</p>")
b.add_chart("chart1", {
    "xAxis": {"type": "category", "values": ["2023", "2024", "2025E"]},
    "series": [{"type": "bar", "values": [100, 200, 300]}]
}, claim_ids=["E-001"])
b.save_state("/tmp/rpt.json")

# Final step: Assemble (use absolute paths)
ws = os.path.join(os.getcwd(), 'workspace', '{project}')
b = ReportBuilder.load_state("/tmp/rpt.json")
b.build(os.path.join(ws, 'report.html'))
```

> **Key**: All ECharts `data` keys should be written as `"values"` in Python dicts. The script's `_to_js()` automatically maps `"values"` → `"data"` during JS serialization, eliminating filtering issues at the code level. Each chart must link back to the `Evidence Claim Ledger` through `claim_ids` or `source_ids`.
> **ReportBuilder auto-generates**: cover page, table of contents, chapter headers, footer page, ECharts JS initialization. The model only needs to output chapter content HTML + chart option dicts.

**Fallback method** (when ReportBuilder is unavailable, fall back to raw `build_report()`):

```python
import sys, os; sys.path.insert(0, 'scripts')
from report_helper import build_report
ws = os.path.join(os.getcwd(), 'workspace', '{project}')
body = '<div class="page cover-page">...</div>'
build_report(body=body, charts=[...], title="Title", output=os.path.join(ws, 'report.html'))
```

> **Why not use the Write tool?** (1) Large HTML files lose content parameters under context pressure; (2) The model output layer filters `data` + array patterns (misidentified as data URIs), causing blank ECharts; (3) Generating a Tier 3 report in one pass requires 15-25K tokens, easily timing out.

**Design specifications**:
- Unified color scheme: Primary `#1A365D` (deep blue, consistent with report_template.html), accent `#667EEA`, secondary `#f59e0b` `#10b981` `#ef4444`
- Chart titles must express findings (e.g., "B2B Market Growth Far Exceeds B2C"), not simple descriptions (e.g., "Market Size")
- All charts must have data source annotations
- Print compatible: ECharts charts auto-render as static images when printing

**Division of labor with CSS layout components**:
- **ECharts**: All data visualizations (trends, comparisons, distributions, positioning, radar, etc.)
- **CSS Components**: Layout elements (data card grids, highlight boxes, strategy cards, insight cards, tables)

### 🚨 Post-Generation Chart Self-Check (executed within the Python script)

After writing the report HTML to file, the following self-check **must be executed in the same Python script**:

```python
import re

with open('report.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Check 1: Number of ECharts initializations
init_count = len(re.findall(r'echarts\.init', html))

# Check 2: Number of data keys (each echarts.init should have at least 1 data)
data_count = len(re.findall(r'\bdata\s*:', html))

# Check 3: Empty array detection (data: [] means data wasn't filled in)
empty_data = len(re.findall(r'\bdata\s*:\s*\[\s*\]', html))

print(f"[Chart Self-Check] ECharts instances: {init_count}, data keys: {data_count}, empty arrays: {empty_data}")

if data_count < init_count:
    print(f"⚠️ Warning: data key count({data_count}) < ECharts instance count({init_count}), chart data may have been filtered!")
if empty_data > 0:
    print(f"⚠️ Warning: Found {empty_data} empty arrays, charts will render without data!")
if data_count >= init_count and empty_data == 0:
    print("✅ Chart data integrity check passed")
```

> If self-check reports ⚠️, **you must stop and fix before delivery**. Do not ignore warnings and proceed.

---

## Quality Checklist

### Stage 5 Post-Insight Self-Check

- [ ] Every insight scored ≥16? (Specificity + Uniqueness + Actionability + Impact)
- [ ] Every recommendation has complete 5W1H?
- [ ] Core conclusions have counter-arguments?
- [ ] All 7 positive behaviors met? (see anti_patterns.md)
- [ ] All 10 anti-patterns avoided? (see anti_patterns.md)

### Stage 6 Post-Chapter Self-Check

- [ ] Conclusion-first? (First sentence is a judgment, not a description)
- [ ] Data-backed? (Every judgment has a source)
- [ ] So What? (Every data point has an implication interpretation)
- [ ] Context anchoring? (Answers "Relevance to Us")
- [ ] Anti-pattern scan? (No platitudes/data dumping/vagueness/context disconnect)

### Stage 6 Post-Report Final Check

**Content quality**:
- [ ] Executive Summary is standalone readable
- [ ] Core conclusion has a viewpoint, not a neutral description
- [ ] Every insight has data support
- [ ] Every recommendation is specific and actionable
- [ ] All data cites sources
- [ ] Core data achieves B-grade verification
- [ ] Every chapter has So What analysis
- [ ] Every chapter has context anchoring
- [ ] Chart titles state findings, not simple descriptions
- [ ] Language is concise, no vague expressions

**Format consistency** (scan each item; if any fails, fix before delivery):
- [ ] **Unit consistency**: Same metric uses same unit throughout (no mixing "billion yuan" and "millions", "%" and "percentage points")
- [ ] **Terminology consistency**: Same concept uses same name throughout (no mixing "market size" and "market volume", "users" and "customers")
- [ ] **Time base consistency**: Data year is explicit, no year-less "market size of 50 billion"; comparative data for the same dimension uses the same time base
- [ ] **Data consistency**: Same data point at different locations (Executive Summary, body text, charts, appendix) has exactly the same value
- [ ] **Confidence level consistency**: All data points labeled A/B/C/D, none omitted
- [ ] **Chart-text alignment**: Chart data matches body text references exactly; chart titles don't contradict body descriptions
- [ ] **Priority label consistency**: P0/P1/P2 labels use the same standard across insights and recommendations, no confusion
- [ ] **Citation format consistency**: Entire report uses uniform source citation format ("Source Name, Year")

# Alpha Insights-BizAdvisor

> **Elite analyst methodology and frameworks, coded into a SKILL**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blue)](https://claude.ai/code)
[![Codex Desktop](https://img.shields.io/badge/Codex%20Desktop-Skill-111111)](https://github.com/openai/codex)

![Alpha Insights](assets/poster_en.png)

---

## What is Alpha Insights?

Alpha Insights is a professional business analysis AI assistant for Claude Code compatible runtimes and Codex Desktop. It produces in-depth, decision-ready research reports — the kind a senior analyst would deliver.

### Why this is not just prompts

Alpha Insights enforces the research workflow with runtime checks, not only instructions:

- `html_write_guard` prevents premature report writing before required artifacts are ready.
- Stage gates validate each research stage, including the Stage 3.5 interview gate.
- `resume_check` catches broken or inconsistent run state before continuing.
- Progress logging and persisted artifacts make long research runs auditable instead of ephemeral.

**Why Alpha Insights?**

| Typical AI Analysis | Alpha Insights |
|---------------------|----------------|
| Generic, surface-level | **Framework-driven** — 19 professional analysis frameworks |
| No source tracing | **Evidence chain** — every conclusion tagged with source & confidence |
| Single data source | **Multi-track parallel** search with triangulation |
| One-shot output | **Interactive iteration** — progressively deeper insights |
| Skips steps silently | **Harness-enforced** — script-based gates, not just prompt instructions |

### See It in Action

> **[View Demo Report (HTML)](https://ericyoung-183.github.io/alpha-insights/assets/demo-report.html)** — A competitive analysis of China's EV charging industry.
> Compact public demo with executive summary, Porter's Five Forces, competitive positioning charts, evidence-graded findings, and strategic recommendations — generated in one session. It is a Tier 2 topic-brief sample, not a full Tier 3 deep report.

> **[Read the V4.1 launch note](https://ericyoung-183.github.io/alpha-insights/launch.html)** — Why Alpha Insights treats serious AI research as a harness-enforced workflow, not another prompt pack.

**Core Value**:
- **L1 Efficiency Replacement**: Save 60%+ desk research time
- **L2 Capability Surpass**: Methodology-driven output on par with senior analysts
- **L3 Experience Compound**: Every research compounds into knowledge assets

### V4: Harness Engineering

Prompt instructions are probabilistic — AI tends to skip steps as context fills up. V4 invests in the **execution environment** instead of just prompts:

- **State machine** — tracks research stage, tier, loaded frameworks, interview status
- **7-stage + Stage 3.5 gate validators** — auto-check deliverables before advancing (PASS/FAIL/WARN)
- **Evidence & Numeric Integrity Gate** — blocks stale entity claims, weak-source strong recommendations, and unlinked headline/chart numbers
- **Hook automation** — HTML write guard, auto gate checks, incremental file persistence
- **Dual-platform adapters** — native frontmatter hooks for Claude Code compatible runtimes, Codex wrappers for Codex Desktop
- **Quality dashboard** — one-screen overview of all quality metrics before report generation

---

## Features

### Thinking OS — 9 Methodologies

MECE | Issue Tree | Hypothesis-Driven | Pyramid Principle | Triangulation | Pre-Mortem | First Principles | ACH (Analysis of Competing Hypotheses) | Expert Interview

### Research Frameworks — 19

**Original**:
- ★ 3A-8 Steps Strategy — End-to-end methodology from industry landscape to strategic convergence

**Classic**:
- Strategy: Porter's Five Forces, Value Chain, SWOT, PESTEL, BCG Matrix
- Business Model: Business Model Canvas, Platform Canvas, Unit Economics
- Market: TAM/SAM/SOM, Competitive Positioning, Industry Lifecycle
- Innovation: Disruption Theory, Blue Ocean Strategy, Jobs-to-be-Done
- Planning: Playing to Win, Three Horizons, Flywheel, SCP

### 10 Research Scenarios

| Scenario | Coverage |
|----------|----------|
| 🎯 Industry Research | Market size, growth drivers, value chain, key players |
| ⚔️ Competitive Analysis | Landscape, rival strategies, differentiation, response |
| 📱 Product Analysis | Features, UX, comparison, positioning, iteration |
| 💼 Business Model | Model teardown, revenue logic, unit economics |
| 🔍 Opportunity Discovery | Value gaps, unmet needs, emerging trends |
| 🌍 Market Entry | New market feasibility, entry path, go-to-market |
| 💰 Investment Decision | Due diligence, valuation, investment thesis |
| 📈 Strategic Planning | Annual/3-year plan, goals, roadmap |
| 🔒 Due Diligence | Risk review, compliance, background check |
| ❓ Ad-hoc Advisory | Policy impact, trend analysis, event assessment |

---

## Quick Start

### Install

**Recommended — ask your AI coding agent**:

```text
Install Alpha Insights from this repository. Follow INSTALL_FOR_AGENTS.md exactly.
```

**Codex Desktop direct install**:

```bash
git clone https://github.com/Ericyoung-183/alpha-insights.git
cd alpha-insights
python3 scripts/install_codex.py --verify
```

**Claude Code compatible install**:

Install this repository as the `alpha-insights` skill package. For the standard
Claude Code skill directory:

```bash
git clone https://github.com/Ericyoung-183/alpha-insights.git
mkdir -p ~/.claude/skills
rm -rf ~/.claude/skills/alpha-insights
cp -R alpha-insights ~/.claude/skills/alpha-insights
python3 ~/.claude/skills/alpha-insights/scripts/verify_cloudcode.py --skill-root ~/.claude/skills/alpha-insights
```

Keep the root `SKILL.md` frontmatter hooks intact. If your runtime uses a
different skill root, copy the same package directory there and run the verifier
with that path.

### Usage

After installation, ask a business analysis question:

```
User: Analyze the competitive landscape of the EV charging industry in China
```

Alpha Insights will automatically:
1. Identify the research scenario (Competitive Analysis)
2. Select matching frameworks (Porter's Five Forces + Competitive Positioning)
3. Run multi-track parallel data search
4. Generate a structured HTML research report

---

## Data Source Configuration

### 🟢 Works Out of the Box

| Source | Description | How |
|--------|------------|-----|
| **Public channels** | Industry reports, analyst research, filings, news, policy docs | Search engine + web scraping |
| **Expert interviews** | Custom interview guides, recording templates, analysis guidance | Built-in methodology |

### 🟡 Optional Extensions

| Source | Description | Required Setup |
|--------|------------|----------------|
| **Xiaohongshu (RedNote)** | Consumer sentiment, product feedback, trend signals | Public web search or a separately installed private adapter; the GitHub package does not bundle provider-specific collection scripts |
| **Knowledge base** | Historical reports, industry notes | Knowledge-base CLI, Notion connector, or another available knowledge-base tool |
| **Internal data** | Business metrics, user behavior | Available database or data warehouse tool |

> Unconfigured data sources are automatically skipped — core functionality is not affected.

#### Internal Data Setup

SQL examples in SKILL files use `{project}.{table_name}` placeholders. Once you configure a database or data-processing tool, the AI will discover available tables through the current environment's table search/query capability — no manual replacement needed.

---

## Directory Structure

```
alpha-insights/
├── SKILL.md              # Main file (workflow orchestration, V4.1.4)
├── INSTALL_FOR_AGENTS.md # Agent-first installation contract
├── CHANGELOG.md          # Version history
├── README.md             # This file
├── frameworks/           # 19 analysis frameworks
│   ├── _index.md         # Framework routing table
│   ├── 3a_8steps_strategy.md
│   ├── porters_five_forces.md
│   └── ...
├── methodology/          # 9 methodologies
│   ├── mece.md
│   ├── hypothesis_driven.md
│   └── ...
├── resources/            # Execution resources (Stage 3-5 input)
│   ├── data_sources.md
│   ├── research_engine.md
│   ├── judgment_rules.md
│   ├── quality_review.md # Independent Quality Review (IQR)
│   └── anti_patterns.md
├── references/           # Report standards (Stage 6-7 output)
│   ├── report_standards.md
│   └── report_template.html
└── scripts/
    ├── install_codex.py  # Codex Desktop installer
    ├── verify_codex.py   # Codex Desktop verifier
    ├── verify_cloudcode.py # Claude Code compatible verifier
    ├── report_helper.py  # ReportBuilder for HTML generation
    ├── codex_hooks/      # Codex hook wrappers
    ├── harness/          # V4 Harness Engineering
    │   ├── state_manager.py
    │   ├── stage_gate.py
    │   ├── dashboard.py
    │   ├── resume_check.py
    │   ├── validators/   # 7-stage + Stage 3.5 gate validators
    │   └── hooks/        # automation hooks
```

---

## Sample Output

Reports generated by Alpha Insights follow this structure:

```
📊 Research Report
├── Executive Summary (1 page)
├── Key Findings (3-5)
├── Detailed Analysis
│   ├── Industry Overview
│   ├── Competitive Landscape
│   ├── Key Player Profiles
│   └── Opportunities & Risks
├── Strategic Recommendations
└── Appendix
    ├── Source List (A/B/C/D graded)
    └── Evidence Base
```

**Data Quality Grading**:

| Grade | Standard | Confidence |
|-------|----------|------------|
| A | 3+ independent sources cross-validated | ✅ High |
| B | 2 sources cross-validated | ⚠️ Moderate |
| C | Single authoritative source | ⚠️ Suggest further validation |
| D | Single source, questionable reliability | ❌ Reference only |

---

## Contributing

Contributions welcome!

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

**Areas to contribute**:
- New analysis frameworks
- Methodology improvements
- Additional data source adapters
- Test cases

---

## License

MIT License

---

## Acknowledgments

**Classic frameworks by**:
- Michael Porter (Five Forces, Value Chain)
- Boston Consulting Group (BCG Matrix)
- McKinsey & Company (Three Horizons, Hypothesis-Driven)
- Clayton Christensen (Disruption Theory, JTBD)
- Jim Collins (Flywheel)
- Alexander Osterwalder (Business Model Canvas)

---

**Author**: Eric Young
**Original framework**: ★ 3A-8 Steps Strategy
**Core philosophy**: Encode methodology into code

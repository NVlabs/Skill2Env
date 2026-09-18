# Software Tools, Methods-Section Templates, and Research-Question Structures

Catalog of software for mixed methods integration, a full methods-section template, and the common structures for mixed methods research questions. Referenced from the "Software Tools", "Writing a Mixed Methods Methods Section", and "Common Mixed Methods Research Questions" capabilities in SKILL.md.

## Software Tools for Mixed Methods Integration

```
Dedicated mixed methods software:
  - NVivo: Mixed methods project support with quantitative import
    and matrix coding queries; can import SPSS data
  - MAXQDA: "Mixed Methods" workspace, joint displays built in,
    statistical integration, imports survey data
  - Dedoose: Cloud-based, designed specifically for mixed methods,
    real-time collaboration, code co-occurrence with demographics

Quantitative analysis:
  - R/RStudio: Comprehensive statistical analysis, integrates with
    qualitative exports via packages (RQDA, qualitativeR)
  - SPSS: Standard statistical package, exports to NVivo
  - Stata: Strong for survey and panel data
  - Python (pandas, scipy, statsmodels): Flexible, scriptable

Qualitative analysis:
  - NVivo, MAXQDA, ATLAS.ti, Dedoose (see above)
  - Python (qualitative coding with custom scripts, NLP)

Integration and visualization:
  - R (ggplot2, ComplexHeatmap): Joint displays and integrated visualizations
  - Python (matplotlib, seaborn, plotly): Custom joint displays
  - Tableau: Interactive dashboards combining qual and quan
  - Excel/Google Sheets: Simple joint display tables

Data management:
  - OSF (Open Science Framework): Manage both strands in one project
  - REDCap: Collect structured and free-text data
  - Qualtrics: Surveys with open-ended questions

Diagramming tools for mixed methods designs:
  - Lucidchart, draw.io, Miro: Visual design diagrams
  - LaTeX (TikZ): Publication-quality design diagrams
```

## Writing a Mixed Methods Methods Section

```markdown
## Template: Methods Section Structure

### Research Design
- Name the specific mixed methods design (e.g., explanatory sequential)
- Provide the notation (e.g., QUAN → qual)
- Include a visual diagram of the design
- Justify why mixed methods is needed (not just convenient)
- State the philosophical worldview (typically pragmatism)
- Cite methodological literature (Creswell & Plano Clark, Teddlie & Tashakkori)

### Participants and Sampling
- Describe sampling for each strand separately
- Explain the relationship between samples
- For sequential designs, explain how Phase 1 informed Phase 2 sampling
- Report sample sizes with justification for each strand

### Data Collection
- Describe quantitative instruments (with psychometric properties)
- Describe qualitative protocols (with sample questions)
- Explain timing and sequencing of data collection
- Address IRB considerations for each phase

### Data Analysis
- Describe quantitative analysis procedures
- Describe qualitative analysis procedures
- **Critically: Describe integration procedures explicitly**
  - When does integration occur?
  - What integration strategy is used (merging, connecting, embedding)?
  - What specific techniques are employed (joint displays, data transformation)?

### Quality and Rigor
- Report validity/reliability for quantitative strand
- Report trustworthiness criteria for qualitative strand
- Report mixed methods legitimation criteria
- Describe researcher positionality and reflexivity
```

## Common Mixed Methods Research Questions

```
Structure of mixed methods research questions:

Type 1: Hybrid question (single integrated question)
  "How and why do faculty members' quantitative research productivity
   metrics relate to their qualitative experiences of academic identity?"

Type 2: Separate strand questions + integration question
  Quantitative: "What is the relationship between X and Y?"
  Qualitative: "How do participants experience Z?"
  Mixed: "In what ways do the quantitative relationships between X and Y
          converge with or diverge from participants' experiences of Z?"

Type 3: Phased questions (for sequential designs)
  Phase 1: "What themes characterize participants' experiences?"
  Phase 2: "To what extent do the themes from Phase 1 predict outcomes
            when tested with a larger sample?"
  Integration: "How do the qualitative themes and quantitative predictive
                model together explain the phenomenon?"
```

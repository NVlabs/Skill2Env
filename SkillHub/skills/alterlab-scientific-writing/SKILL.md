---
name: alterlab-scientific-writing
description: Writes scientific manuscripts in full flowing paragraphs (never bullet points) via a two-stage process — section outlines with key points using research-lookup, then conversion to prose — applying IMRAD structure, citations (APA/AMA/Vancouver), figures/tables, and reporting guidelines (CONSORT/STROBE/PRISMA). Use when drafting or revising research papers, journal submissions, or any manuscript section (abstract, introduction, methods, results, discussion), or professional/technical reports. For a specific venue's LaTeX template and house style use alterlab-venue-templates; to build a BibTeX bibliography or verify reference metadata use alterlab-citation-mgmt. Part of the AlterLab Academic Skills suite.
allowed-tools: Read Write Edit Bash
license: MIT
compatibility: No API key or external service required for drafting; optional professional-report formatting with scientific_report.sty needs a LaTeX distribution (XeLaTeX/LuaLaTeX)
metadata:
    skill-author: AlterLab
    version: "1.0.0"
---

# Scientific Writing

## Overview

Scientific writing communicates research with precision and clarity. Write manuscripts using IMRAD structure, citations (APA/AMA/Vancouver), figures/tables, and reporting guidelines (CONSORT/STROBE/PRISMA). Apply this skill for research papers and journal submissions. Ground claims in literature gathered via the **alterlab-research-lookup** skill, and verify every citation against its source.

**Critical Principle: Always write in full paragraphs with flowing prose. Never submit bullet points in the final manuscript.** Use a two-stage process: first create section outlines with key points using research-lookup, then convert those outlines into complete paragraphs.

## When to Use This Skill

This skill should be used when:
- Writing or revising any section of a scientific manuscript (abstract, introduction, methods, results, discussion)
- Structuring a research paper using IMRAD or other standard formats
- Formatting citations and references in specific styles (APA, AMA, Vancouver, Chicago, IEEE)
- Creating, formatting, or improving figures, tables, and data visualizations
- Applying study-specific reporting guidelines (CONSORT for trials, STROBE for observational studies, PRISMA for reviews)
- Drafting abstracts that meet journal requirements (structured or unstructured)
- Preparing manuscripts for submission to specific journals
- Improving writing clarity, conciseness, and precision
- Ensuring proper use of field-specific terminology and nomenclature
- Addressing reviewer comments and revising manuscripts

## Figures and Visual Elements (Optional)

Well-chosen figures—such as a graphical abstract, methods flowchart, or conceptual diagram—can strengthen a manuscript, but they are optional and should be added only where they genuinely improve clarity. If a diagram or figure would aid comprehension, invoke the **alterlab-scientific-schematics** skill (diagrams/schematics) or the **alterlab-generate-image** skill (images).

---

## Core Capabilities

### 1. Manuscript Structure and Organization

**IMRAD Format**: Guide papers through the standard Introduction, Methods, Results, And Discussion structure used across most scientific disciplines. This includes:
- **Introduction**: Establish research context, identify gaps, state objectives
- **Methods**: Detail study design, populations, procedures, and analysis approaches
- **Results**: Present findings objectively without interpretation
- **Discussion**: Interpret results, acknowledge limitations, propose future directions

For detailed guidance on IMRAD structure, refer to `references/imrad_structure.md`.

**Alternative Structures**: Support discipline-specific formats including:
- Review articles (narrative, systematic, scoping)
- Case reports and case series
- Meta-analyses and pooled analyses
- Theoretical/modeling papers
- Methods papers and protocols

### 2. Section-Specific Writing Guidance

**Abstract Composition**: Craft concise, standalone summaries (100-250 words) that capture the paper's purpose, methods, results, and conclusions. Support both structured abstracts (with labeled sections) and unstructured single-paragraph formats.

**Introduction Development**: Build compelling introductions that:
- Establish the research problem's importance
- Review relevant literature systematically
- Identify knowledge gaps or controversies
- State clear research questions or hypotheses
- Explain the study's novelty and significance

**Methods Documentation**: Ensure reproducibility through:
- Detailed participant/sample descriptions
- Clear procedural documentation
- Statistical methods with justification
- Equipment and materials specifications
- Ethical approval and consent statements

**Results Presentation**: Present findings with:
- Logical flow from primary to secondary outcomes
- Integration with figures and tables
- Statistical significance with effect sizes
- Objective reporting without interpretation

**Discussion Construction**: Synthesize findings by:
- Relating results to research questions
- Comparing with existing literature
- Acknowledging limitations honestly
- Proposing mechanistic explanations
- Suggesting practical implications and future research

### 3. Citation and Reference Management

Apply citation styles correctly across disciplines. For comprehensive style guides, refer to `references/citation_styles.md`.

**Major Citation Styles:**
- **AMA (American Medical Association)**: Numbered superscript citations, common in medicine
- **Vancouver**: Numbered citations in square brackets, biomedical standard
- **APA (American Psychological Association)**: Author-date in-text citations, common in social sciences
- **Chicago**: Notes-bibliography or author-date, humanities and sciences
- **IEEE**: Numbered square brackets, engineering and computer science

**Best Practices:**
- Cite primary sources when possible
- Include recent literature (last 5-10 years for active fields)
- Balance citation distribution across introduction and discussion
- Verify all citations against original sources
- Use reference management software (Zotero, Mendeley, EndNote)

### 4. Figures and Tables

Create effective data visualizations that enhance comprehension. For detailed best practices, refer to `references/figures_tables.md`.

**When to Use Tables vs. Figures:**
- **Tables**: Precise numerical data, complex datasets, multiple variables requiring exact values
- **Figures**: Trends, patterns, relationships, comparisons best understood visually

**Design Principles:**
- Make each table/figure self-explanatory with complete captions
- Use consistent formatting and terminology across all display items
- Label all axes, columns, and rows with units
- Include sample sizes (n) and statistical annotations
- Follow the "one table/figure per 1000 words" guideline
- Avoid duplicating information between text, tables, and figures

**Common Figure Types:**
- Bar graphs: Comparing discrete categories
- Line graphs: Showing trends over time
- Scatterplots: Displaying correlations
- Box plots: Showing distributions and outliers
- Heatmaps: Visualizing matrices and patterns

### 5. Reporting Guidelines by Study Type

Ensure completeness and transparency by following established reporting standards. For comprehensive guideline details, refer to `references/reporting_guidelines.md`.

**Key Guidelines:**
- **CONSORT**: Randomized controlled trials
- **STROBE**: Observational studies (cohort, case-control, cross-sectional)
- **PRISMA**: Systematic reviews and meta-analyses
- **STARD**: Diagnostic accuracy studies
- **TRIPOD**: Prediction model studies
- **ARRIVE**: Animal research
- **CARE**: Case reports
- **SQUIRE**: Quality improvement studies
- **SPIRIT**: Study protocols for clinical trials
- **CHEERS**: Economic evaluations

Each guideline provides checklists ensuring all critical methodological elements are reported.

### 6. Writing Principles and Style

Apply fundamental scientific writing principles. For detailed guidance, refer to `references/writing_principles.md`.

**Clarity**:
- Use precise, unambiguous language
- Define technical terms and abbreviations at first use
- Maintain logical flow within and between paragraphs
- Use active voice when appropriate for clarity

**Conciseness**:
- Eliminate redundant words and phrases
- Favor shorter sentences (15-20 words average)
- Remove unnecessary qualifiers
- Respect word limits strictly

**Accuracy**:
- Report exact values with appropriate precision
- Use consistent terminology throughout
- Distinguish between observations and interpretations
- Acknowledge uncertainty appropriately

**Objectivity**:
- Present results without bias
- Avoid overstating findings or implications
- Acknowledge conflicting evidence
- Maintain professional, neutral tone

### 7. Writing Process: From Outline to Full Paragraphs

**CRITICAL: Always write in full paragraphs, never submit bullet points in scientific papers.** Use a two-stage process for every section:

1. **Outline (planning only)** — use research-lookup to gather literature, then jot bullet points marking the main arguments, key studies to cite, and data to include. These are scaffolding, not the manuscript.
2. **Convert to prose** — expand each bullet into complete sentences with natural transitions and citations integrated into the text, varying sentence structure and ensuring logical flow.

Lists are acceptable only in Methods (inclusion/exclusion criteria, materials) and supplementary materials — never in the Abstract, Introduction, Results, Discussion, or Conclusions. Abstracts are flowing paragraphs, not labeled sections, unless the journal explicitly requires structured format.

For the full worked example (outline → prose), the outline-vs-final comparison table, the complete mistakes-to-avoid list, and research-lookup integration, see `references/outline_to_prose.md`.

### 8. Professional Report Formatting (Non-Journal Documents)

For research reports, technical reports, white papers, grant/progress reports, and other professional documents that are NOT journal manuscripts, use the `scientific_report.sty` LaTeX style package (Helvetica typography, colored box environments, professional tables, and scientific-notation commands for p-values/effect sizes/CIs). Journal manuscripts and conference papers should instead use the **venue-templates** skill; theses use institutional templates.

Box environments, table formatting, notation commands, the getting-started preamble, and XeLaTeX/LuaLaTeX compilation are documented in `references/professional_report_quickref.md`, with the full guide in `references/professional_report_formatting.md` and the package itself plus template in `assets/`.

### 9. Journal-Specific Formatting

Adapt manuscripts to journal requirements:
- Follow author guidelines for structure, length, and format
- Apply journal-specific citation styles
- Meet figure/table specifications (resolution, file formats, dimensions)
- Include required statements (funding, conflicts of interest, data availability, ethical approval)
- Adhere to word limits for each section
- Format according to template requirements when provided

### 10. Field-Specific Language and Terminology

Adapt language, terminology, and conventions to match the specific scientific discipline. Each field has established vocabulary, preferred phrasings, and domain-specific conventions that signal expertise and ensure clarity for the target audience. Identify conventions by reviewing recent high-impact papers in the target journal, noting field-specific abbreviations, units, notation, and preferred terms (e.g., "participants" vs. "subjects").

General principles apply across fields: match terminology to audience expertise (define more for broad-impact journals like *Nature*/*Science*); define abbreviations at first use; maintain consistent terms and nomenclature throughout; avoid field-mixing errors (don't call mice "patients"); and verify usage against field style guides, ontologies (Gene Ontology, MeSH), and recent papers.

For per-discipline conventions (biomedical/clinical, molecular biology and genetics, chemistry, ecology, physics/engineering, neuroscience, social and behavioral sciences) and the full set of general principles, see `references/field_terminology.md`.

### 11. Common Pitfalls to Avoid

**Top Rejection Reasons:**
1. Inappropriate, incomplete, or insufficiently described statistics
2. Over-interpretation of results or unsupported conclusions
3. Poorly described methods affecting reproducibility
4. Small, biased, or inappropriate samples
5. Poor writing quality or difficult-to-follow text
6. Inadequate literature review or context
7. Figures and tables that are unclear or poorly designed
8. Failure to follow reporting guidelines

**Writing Quality Issues:**
- Mixing tenses inappropriately (use past tense for methods/results, present for established facts)
- Excessive jargon or undefined acronyms
- Paragraph breaks that disrupt logical flow
- Missing transitions between sections
- Inconsistent notation or terminology

## Workflow for Manuscript Development

**Stage 1: Planning**
1. Identify target journal and review author guidelines
2. Determine applicable reporting guideline (CONSORT, STROBE, etc.)
3. Outline manuscript structure (usually IMRAD)
4. Plan figures and tables as the backbone of the paper

**Stage 2: Drafting** (Use two-stage writing process for each section)
1. Start with figures and tables (the core data story)
2. For each section below, follow the two-stage process:
   - **First**: Create outline with bullet points using research-lookup
   - **Second**: Convert bullet points to full paragraphs with flowing prose
3. Write Methods (often easiest to draft first)
4. Draft Results (describing figures/tables objectively)
5. Compose Discussion (interpreting findings)
6. Write Introduction (setting up the research question)
7. Craft Abstract (synthesizing the complete story)
8. Create Title (concise and descriptive)

**Remember**: Bullet points are for planning only—the final manuscript must be in complete paragraphs.

**Stage 3: Revision**
1. Check logical flow and "red thread" throughout
2. Verify consistency in terminology and notation
3. Ensure figures/tables are self-explanatory
4. Confirm adherence to reporting guidelines
5. Verify all citations are accurate and properly formatted
6. Check word counts for each section
7. Proofread for grammar, spelling, and clarity

**Stage 4: Final Preparation**
1. Format according to journal requirements
2. Prepare supplementary materials
3. Write cover letter highlighting significance
4. Complete submission checklists
5. Gather all required statements and forms

## Integration with Other Scientific Skills

Use this skill for the general scientific-writing craft (IMRAD, clarity, prose, citation styles in text). Hand off to a sibling skill when the task is theirs:

- **alterlab-research-lookup** — literature search to populate Stage-1 outlines and ground claims.
- **alterlab-venue-templates** — a specific venue's LaTeX template, page-limit/formatting rules, and house writing style (Nature/Science, Cell Press, medical journals, ML/CS conferences). Apply this skill's principles first, then adapt to the venue there.
- **alterlab-citation-mgmt** — building/validating a BibTeX bibliography and pulling reference metadata (this skill applies citation *styles* in text but does not build the reference library).
- **alterlab-scientific-schematics** / **alterlab-generate-image** — diagrams/schematics and images when a figure would aid clarity.

**Formatting routing**: Journal manuscripts and conference papers use the `venue-templates` skill. Research reports, white papers, technical reports, and grant/progress reports use `scientific_report.sty` (this skill, §8). Theses use institutional templates.

## References

This skill includes comprehensive reference files covering specific aspects of scientific writing:

- `references/imrad_structure.md`: Detailed guide to IMRAD format and section-specific content
- `references/citation_styles.md`: Complete citation style guides (APA, AMA, Vancouver, Chicago, IEEE)
- `references/figures_tables.md`: Best practices for creating effective data visualizations
- `references/reporting_guidelines.md`: Study-specific reporting standards and checklists
- `references/writing_principles.md`: Core principles of effective scientific communication
- `references/outline_to_prose.md`: Two-stage outline-to-paragraph process with full worked example and mistakes to avoid
- `references/field_terminology.md`: Per-discipline language conventions and general terminology principles
- `references/professional_report_quickref.md`: `scientific_report.sty` box environments, table formatting, notation commands, and getting-started preamble
- `references/professional_report_formatting.md`: Comprehensive guide to professional report styling with `scientific_report.sty`

## Assets

This skill includes LaTeX style packages and templates for professional report formatting:

- `assets/scientific_report.sty`: Professional LaTeX style package with Helvetica fonts, colored boxes, and attractive tables
- `assets/scientific_report_template.tex`: Complete report template demonstrating all style features
- `assets/REPORT_FORMATTING_GUIDE.md`: Quick reference guide for the style package

**Key Features of `scientific_report.sty`:**
- Helvetica font family for modern, professional appearance
- Professional color scheme (blues, greens, oranges, purples)
- Box environments: `keyfindings`, `methodology`, `resultsbox`, `recommendations`, `limitations`, `criticalnotice`, `definition`, `executivesummary`, `hypothesis`
- Tables with alternating row colors and professional headers
- Scientific notation commands for p-values, effect sizes, confidence intervals
- Professional headers and footers

Load these references as needed when working on specific aspects of scientific writing.


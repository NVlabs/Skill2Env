---
name: alterlab-qualitative-methods
description: "Comprehensive qualitative research methods assistant supporting thematic analysis (Braun & Clarke), grounded theory (Strauss & Corbin; Charmaz), interpretative phenomenological analysis (IPA), content analysis, narrative inquiry, ethnography, case study methodology (Yin), coding techniques (open/axial/selective), NVivo-style workflows with Python alternatives, trustworthiness criteria (Lincoln & Guba), reflexivity, and member checking. Use when designing or analyzing qualitative research — thematic analysis, grounded theory, coding data, phenomenology, IPA, ethnography, case study, narrative inquiry, content analysis, qualitative coding, NVivo, trustworthiness, member checking, reflexivity, interview analysis, or focus group analysis. Part of the AlterLab Academic Skills suite."
license: MIT
allowed-tools: Read WebFetch WebSearch Bash(python:*)
compatibility: No API key required. Guidance-focused skill; uses WebFetch/WebSearch and optional Python helpers via `uv run python`.
metadata:
  skill-author: AlterLab
  version: "1.0.0"
  last_updated: "2026-03-18"
---

# Qualitative Methods — Qualitative Research Design & Analysis Agent

A comprehensive qualitative research methods tool for faculty and researchers conducting, supervising, or teaching qualitative inquiry. Covers methodology selection, data collection design, systematic coding, analysis techniques, and quality assurance across all major qualitative traditions.

## Overview

Qualitative research seeks to understand phenomena through the meanings people assign to them. This skill guides researchers through the full qualitative research process: choosing an appropriate methodology, designing data collection instruments, conducting systematic analysis, ensuring trustworthiness, and reporting findings in ways that meet disciplinary standards.

Unlike quantitative research, which tests hypotheses through numerical data, qualitative research generates rich, contextualized understanding through words, images, and observations. This skill treats methodological rigor as non-negotiable while acknowledging the interpretive nature of qualitative work.

## When to Use This Skill

This skill should be used when:
- Selecting a qualitative methodology for a research project
- Designing interview protocols, observation guides, or document analysis frameworks
- Coding qualitative data (transcripts, field notes, documents)
- Conducting thematic analysis, grounded theory, IPA, or other analytic approaches
- Establishing trustworthiness and quality criteria for qualitative findings
- Writing the methodology section of a qualitative paper or thesis
- Reviewing qualitative research for methodological rigor
- Teaching qualitative methods courses
- Transitioning from quantitative to qualitative or mixed-methods research
- Working with CAQDAS (Computer-Assisted Qualitative Data Analysis Software)

### Does NOT Trigger

| Scenario | Use Instead |
|----------|-------------|
| Statistical analysis | Data science skills |
| Survey design and validation | `alterlab-survey-design` |
| Writing the full paper | `alterlab-paper-writer` |
| Systematic review / meta-analysis | `alterlab-deep-research` |

---

## Core Capabilities

### 1. Methodology Selection Guide

Choosing the right qualitative methodology depends on your research question, philosophical stance, and the kind of knowledge you seek.

**Methodology Decision Framework:**

```
What is your primary research interest?
│
├── LIVED EXPERIENCE of individuals
│   ├── Focus on meaning-making and interpretation
│   │   └── Interpretative Phenomenological Analysis (IPA)
│   ├── Focus on the essence/structure of experience
│   │   └── Descriptive/Transcendental Phenomenology (Husserl/Moustakas)
│   └── Focus on life stories and identity construction
│       └── Narrative Inquiry
│
├── SOCIAL PROCESSES and how they unfold
│   ├── Want to generate theory from data
│   │   └── Grounded Theory (Strauss & Corbin or Charmaz)
│   └── Want to describe a process in context
│       └── Case Study (Yin) or Ethnography
│
├── CULTURAL PATTERNS in a group or setting
│   ├── Immersive fieldwork possible (months/years)
│   │   └── Ethnography
│   └── Bounded, focused investigation
│       └── Case Study (Yin)
│
├── CONTENT/MEANING in texts or media
│   ├── Seeking patterns and themes across a dataset
│   │   └── Thematic Analysis (Braun & Clarke)
│   └── Systematic categorization of content
│       └── Content Analysis (qualitative or directed)
│
└── A BOUNDED SYSTEM (program, event, organization)
    ├── Single case with depth
    │   └── Single Case Study
    ├── Multiple cases for comparison
    │   └── Multiple Case Study
    └── Evaluating a program or intervention
        └── Case Study with evaluation framework
```

**Methodology Comparison Table:**

| Feature | Thematic Analysis | Grounded Theory | IPA | Ethnography | Case Study | Narrative Inquiry |
|---------|------------------|-----------------|-----|-------------|------------|-------------------|
| Primary aim | Identify patterns/themes | Generate theory | Understand lived experience | Describe cultural patterns | In-depth bounded system analysis | Understand experience through stories |
| Philosophical roots | Flexible (realist to constructionist) | Pragmatism / symbolic interactionism | Phenomenology, hermeneutics, idiography | Cultural anthropology | Pragmatism | Dewey's experiential philosophy |
| Sample size | Flexible (6-30+) | 20-60 (theoretical saturation) | 3-10 (homogeneous) | 1 setting (extended) | 1-10 cases | 1-5 participants |
| Data types | Interviews, focus groups, documents, any text | Interviews, observations, documents | In-depth interviews (2-3 per participant) | Fieldwork, observations, interviews, artifacts | Multiple sources (triangulation required) | Interviews, journals, life documents |
| Analysis | 6-phase coding | Open → axial → selective coding | Line-by-line → emergent themes → superordinate themes | Thick description, cultural themes | Within-case and cross-case analysis | Restorying, narrative structure |
| Output | Theme map with evidence | Substantive or formal theory | Rich account of lived experience | Cultural portrait / ethnographic account | Case description and themes | Narrative retelling and interpretation |
| Time investment | Moderate | High | High per participant | Very high | Moderate to high | Moderate |
| Key reference | Braun & Clarke (2006, 2019) | Strauss & Corbin (1998); Charmaz (2014) | Smith, Flowers & Larkin (2009) | Hammersley & Atkinson (2019) | Yin (2018); Stake (1995) | Clandinin & Connelly (2000) |

### 2. Thematic Analysis (Braun & Clarke)

The most widely used qualitative analysis method. Braun & Clarke (2006, updated 2019) provide a reflexive approach.

**Six Phases of Reflexive Thematic Analysis:**

```
Phase 1: Familiarization with the Data
│   Read and re-read transcripts
│   Note initial observations (not codes yet)
│   Immerse yourself in the data
│   Record preliminary thoughts in a research journal
│
Phase 2: Systematic Coding
│   Generate initial codes across the entire dataset
│   Code inclusively (code everything potentially relevant)
│   Codes are semantic (surface meaning) or latent (underlying assumptions)
│   One extract can have multiple codes
│   Use line-by-line or segment-by-segment approach
│
Phase 3: Generating Initial Themes
│   Collate codes into potential themes
│   Use visual methods: mind maps, affinity diagrams, tables
│   Themes are patterns of shared meaning organized around a central concept
│   Not every code becomes a theme — some are subthemes, some are discarded
│
Phase 4: Reviewing Themes
│   Check themes against coded extracts (Level 1)
│   Check themes against entire dataset (Level 2)
│   Do themes tell a coherent story?
│   Are themes distinct or overlapping?
│   Refine: split, merge, or discard themes as needed
│
Phase 5: Defining and Naming Themes
│   Write a detailed analysis of each theme
│   Identify the "essence" of each theme
│   Create concise, vivid theme names
│   Determine how themes relate to each other
│
Phase 6: Writing Up
    Weave together analytic narrative and data extracts
    Go beyond description — interpret and contextualize
    Embed extracts as evidence, not illustration only
    Relate findings to literature and research question
```

Worked coding example and theme-development example: see `references/worked_examples.md`.

### 3. Grounded Theory

Grounded theory generates theory that is "grounded" in systematically collected and analyzed data.

**Strauss & Corbin (1998) — Systematic Approach:**

```
OPEN CODING
│   Break data into discrete parts
│   Label phenomena (concepts)
│   Group concepts into categories
│   Identify properties and dimensions of categories
│
│   Example:
│   Concept: "Time pressure"
│   Properties: Source (institutional, self-imposed), Intensity, Duration
│   Dimensions: Mild ←──────→ Severe
│
AXIAL CODING
│   Reassemble data around categories
│   Use the paradigm model:
│
│   Causal Conditions → Phenomenon → Context
│                                    → Intervening Conditions
│                                    → Action/Interaction Strategies
│                                    → Consequences
│
│   Example:
│   Causal conditions: Publish-or-perish culture
│   Phenomenon: Research anxiety
│   Context: Early-career faculty, research university
│   Intervening conditions: Mentorship availability, institutional support
│   Strategies: Strategic collaboration, prioritization, avoidance
│   Consequences: Productivity variation, burnout, career trajectory
│
SELECTIVE CODING
    Identify the core category
    Systematically relate all categories to the core
    Fill in categories that need further development
    Validate the emerging theory against data
    Write the storyline

    Example core category: "Surviving the Tenure Track"
    All other categories (research anxiety, teaching load, institutional
    politics, mentorship) relate to this central phenomenon
```

**Charmaz (2014) — Constructivist Grounded Theory:**

Key differences from Strauss & Corbin:
- Emphasizes researcher's role in constructing (not discovering) theory
- Uses initial coding and focused coding (not open/axial/selective)
- Prioritizes gerunds (action words) in coding: "struggling with," "negotiating," "adapting to"
- Memo writing is central from the very beginning
- Theoretical sampling continues until categories are saturated

**Theoretical Sampling:**

```
Initial data collection (purposive sampling)
│
├── Analyze → Emerging categories
│
├── Identify gaps in categories
│
├── Sample specifically to develop/test categories
│   (Who to interview? What to observe? What documents to examine?)
│
├── Analyze new data → Refine categories
│
├── Repeat until THEORETICAL SATURATION
│   (No new properties, dimensions, or relationships emerge)
│
└── Articulate substantive theory
```

### 4. Interpretative Phenomenological Analysis (IPA)

IPA explores how individuals make sense of significant life experiences. It is idiographic, phenomenological, and hermeneutic.

**IPA Analysis Steps (Smith, Flowers & Larkin, 2009):**

```
Step 1: Reading and Re-reading
│   Read the transcript multiple times
│   Listen to the audio recording alongside
│   Note initial observations in the margin
│
Step 2: Initial Noting
│   Three types of comments:
│   - Descriptive (content, what is said)
│   - Linguistic (language use, metaphors, pauses, laughter)
│   - Conceptual (interpretive, interrogative)
│
│   Example:
│   Transcript: "It was like hitting a brick wall"
│   Descriptive: Encountered a major obstacle
│   Linguistic: Metaphor of physical barrier — sudden, painful, solid
│   Conceptual: Sense of helplessness? Unexpected nature of the barrier?
│
Step 3: Developing Emergent Themes
│   Transform notes into concise themes
│   Themes capture psychological essence, not just content
│   Balance participant's words with analyst's interpretation
│   (The hermeneutic circle: part ↔ whole)
│
Step 4: Searching for Connections Across Themes
│   Organize emergent themes:
│   - Abstraction: Group similar themes under superordinate theme
│   - Subsumption: One theme becomes superordinate, absorbs others
│   - Polarization: Identify oppositional relationships
│   - Contextualization: Identify temporal or narrative connections
│   - Numeration: Note frequency (but do not reduce to counting)
│   - Function: Examine what themes do for the participant
│
Step 5: Moving to the Next Case
│   Bracket (as much as possible) findings from previous cases
│   Repeat Steps 1-4 for each participant individually
│
Step 6: Looking for Patterns Across Cases
    Identify recurrent themes across participants
    Note convergence and divergence
    Create a master table of themes
    Retain idiographic detail — do not flatten into generic themes
```

IPA master table-of-themes example (superordinate themes, subthemes, per-participant page references): see `references/worked_examples.md`.

### 5. Case Study Methodology (Yin, 2018)

**Types of Case Study Designs:**

```
                    Single-Case              Multiple-Case
                    ┌──────────────────┐     ┌──────────────────┐
Holistic            │ Type 1           │     │ Type 3           │
(single unit        │ Critical, unique,│     │ Replication      │
of analysis)        │ revelatory, or   │     │ logic across     │
                    │ longitudinal case│     │ cases            │
                    └──────────────────┘     └──────────────────┘
                    ┌──────────────────┐     ┌──────────────────┐
Embedded            │ Type 2           │     │ Type 4           │
(multiple units     │ Single case with │     │ Multiple cases   │
of analysis)        │ embedded sub-    │     │ each with        │
                    │ units            │     │ embedded units   │
                    └──────────────────┘     └──────────────────┘
```

**Five Components of Case Study Design:**

1. **Research questions** — "How" and "why" questions are best suited
2. **Propositions** (if any) — Direct attention to what should be examined
3. **Unit of analysis** — Define the "case" (individual, organization, program, event)
4. **Logic linking data to propositions** — Pattern matching, explanation building, time-series
5. **Criteria for interpreting findings** — Rival explanations, sufficient evidence

**Data Collection — Six Sources of Evidence:**

| Source | Strengths | Weaknesses |
|--------|-----------|------------|
| Documents | Stable, unobtrusive, broad coverage | Retrievability, biased selectivity, reporting bias |
| Archival records | Precise, quantitative | Privacy restrictions, accessibility |
| Interviews | Targeted, insightful, explanatory | Bias from poor questions, response bias, inaccuracies from recall |
| Direct observations | Real-time, contextual | Time-consuming, selectivity, reflexivity effects |
| Participant observation | Insightful about interpersonal behavior | Bias from researcher participation |
| Physical artifacts | Insightful about cultural features | Selectivity, availability |

**Chain of Evidence:**

```
Research questions
    ↓
Case study protocol
    ↓
Citations to specific evidence in case study database
    ↓
Case study database (organized notes, documents, tabular materials)
    ↓
Case study report
```

### 6. Coding Techniques

**Coding Hierarchy:**

```
Level 1: OPEN/INITIAL CODES
│   Line-by-line or segment-by-segment labels
│   Stay close to the data
│   Example: "feeling unprepared," "seeking guidance," "peer support"
│
Level 2: FOCUSED/AXIAL CODES (Categories)
│   Group open codes into higher-level categories
│   Identify relationships between categories
│   Example: "Navigation strategies" (contains: seeking guidance, peer
│   support, trial and error, online resources)
│
Level 3: THEMES / THEORETICAL CODES
    Abstract, interpretive-level patterns
    Capture the meaning across categories
    Example: "The invisible apprenticeship" (captures how new academics
    learn the unwritten rules of their profession)
```

Full codebook template (definition, inclusion/exclusion criteria, worked example): see `references/worked_examples.md`.

### 7. Python-Based Qualitative Analysis Workflows

For researchers who prefer open-source tools over NVivo/Atlas.ti, ready-to-run Python recipes cover keyword-based initial coding, bigram/trigram frequency and collocation analysis, and thematic-network visualization.

Full code recipes: see `references/python_workflows.md`.

### 8. Trustworthiness Criteria (Lincoln & Guba, 1985)

Trustworthiness in qualitative research parallels validity and reliability in quantitative research.

| Quantitative Criterion | Qualitative Parallel | Strategies |
|----------------------|---------------------|------------|
| Internal validity | **Credibility** | Prolonged engagement, persistent observation, triangulation, peer debriefing, negative case analysis, member checking |
| External validity | **Transferability** | Thick description of context, purposive sampling, detailed methodology |
| Reliability | **Dependability** | Audit trail, inquiry audit, reflexive journal, code-recode stability |
| Objectivity | **Confirmability** | Audit trail, triangulation, reflexivity |

**Additional Quality Criterion — Authenticity (Guba & Lincoln, 1989):**
- Fairness: Multiple viewpoints represented equitably
- Ontological authenticity: Participants' understanding is enhanced
- Educative authenticity: Participants understand others' perspectives better
- Catalytic authenticity: Research stimulates action
- Tactical authenticity: Participants are empowered to act

**Triangulation Types:**

```
1. Data triangulation      — Multiple data sources (interviews + documents + observations)
2. Investigator triangulation — Multiple researchers coding/analyzing
3. Theory triangulation    — Multiple theoretical lenses applied to the same data
4. Methodological triangulation — Multiple methods (interviews + surveys + observations)
```

Full member-checking procedure and reporting template: see `references/worked_examples.md`.

### 9. Reflexivity

Reflexivity is the researcher's ongoing critical self-examination of their role, assumptions, and influence on the research process.

Reflexive journal prompts spanning before, during, and after data collection and analysis: see `references/worked_examples.md`.

---

## Best Practices

1. **Choose methodology before collecting data.** Your methodology shapes your research question, sampling, data collection, and analysis. Do not collect data and then decide how to analyze it.

2. **Maintain an audit trail.** Document every decision: why you chose a methodology, how you recruited participants, how codes evolved, why you merged or split themes. This is your evidence of rigor.

3. **Code systematically.** Whether using software or paper, code the entire dataset consistently. Do not cherry-pick excerpts that confirm your expectations.

4. **Write memos throughout.** Memos are where analytical thinking happens. Write early, write often, write about codes, categories, themes, puzzles, and surprises.

5. **Achieve saturation thoughtfully.** Saturation is not a number (e.g., "12 interviews"). It is a judgment that new data are no longer generating new insights relevant to your research question.

6. **Use participants' words.** Direct quotes are the evidence of qualitative research. Weave them into your analysis, not as decoration, but as the foundation of your argument.

7. **Distinguish description from interpretation.** Description says what the data contain. Interpretation says what the data mean. Both are needed; do not confuse them.

8. **Triangulate.** Use multiple data sources, methods, or analysts to strengthen credibility. No single source is sufficient.

9. **Practice reflexivity.** Your positionality shapes what you see and how you interpret it. Make this explicit, not as a confession, but as a methodological practice.

10. **Report transparently.** Include your codebook, describe your analysis process in detail, justify your sample, and acknowledge limitations. Readers should be able to evaluate your rigor.

---

## Common Pitfalls

| Pitfall | Why It Happens | How to Avoid |
|---------|---------------|--------------|
| Methodology-method confusion | Conflating a method (interviews) with a methodology (grounded theory) | Study the philosophical foundations of your chosen methodology |
| Anecdotalism | Selecting quotes that support a preconceived narrative | Code the entire dataset; report disconfirming evidence |
| Premature closure | Stopping data collection too early | Use theoretical sampling; document saturation decisions |
| Superficial coding | Staying at descriptive level without interpretive depth | Use latent as well as semantic codes; write analytical memos |
| Theme = topic | Calling a topic a theme (e.g., "communication" is a topic, not a theme) | Themes are patterns of shared meaning — they make a claim |
| Ignoring context | Treating excerpts as decontextualized data points | Preserve context in your codebook; use thick description |
| No reflexivity | Assuming the researcher is a neutral instrument | Maintain a reflexive journal from day one |
| Over-reliance on frequency | Treating qualitative analysis as counting code occurrences | A theme's importance is about meaning, not frequency |
| Mixed methodology without justification | Combining elements of grounded theory and thematic analysis without explanation | Be clear about your methodological commitments and why |
| Poor data management | Transcripts scattered, no version control, no backup | Use a systematic folder structure; back up regularly; use CAQDAS |

---

## References

- Braun, V., & Clarke, V. (2006). Using thematic analysis in psychology. *Qualitative Research in Psychology*, 3(2), 77-101.
- Braun, V., & Clarke, V. (2019). Reflecting on reflexive thematic analysis. *Qualitative Research in Sport, Exercise and Health*, 11(4), 589-597.
- Charmaz, K. (2014). *Constructing grounded theory* (2nd ed.). Sage.
- Clandinin, D. J., & Connelly, F. M. (2000). *Narrative inquiry: Experience and story in qualitative research*. Jossey-Bass.
- Creswell, J. W., & Poth, C. N. (2018). *Qualitative inquiry and research design: Choosing among five approaches* (4th ed.). Sage.
- Lincoln, Y. S., & Guba, E. G. (1985). *Naturalistic inquiry*. Sage.
- Smith, J. A., Flowers, P., & Larkin, M. (2009). *Interpretative phenomenological analysis: Theory, method, and research*. Sage.
- Strauss, A., & Corbin, J. (1998). *Basics of qualitative research: Techniques and procedures for developing grounded theory* (2nd ed.). Sage.
- Yin, R. K. (2018). *Case study research and applications: Design and methods* (6th ed.). Sage.

See also: `references/qualitative-frameworks.md` for expanded methodology details.

Part of the AlterLab Academic Skills suite.
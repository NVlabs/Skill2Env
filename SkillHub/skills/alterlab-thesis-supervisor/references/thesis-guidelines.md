# Thesis & Dissertation Guidelines Reference

## 1. Dissertation Proposal — Detailed Expectations

### What Committees Look For in a Proposal

| Criterion | Excellent | Acceptable | Needs Work |
|-----------|-----------|-----------|------------|
| Problem statement | Clear, evidence-based gap; significant to field | Identifiable gap but weak evidence | Vague, no clear gap, or trivial problem |
| Research questions | Specific, answerable, aligned to methods | Clear but could be sharper | Vague, yes/no, or too many |
| Literature review | Comprehensive, synthesized, identifies specific gap | Adequate coverage but more summary than synthesis | Laundry list of studies; no synthesis |
| Theoretical framework | Well-articulated, appropriate, visually mapped | Present but not deeply integrated | Missing or superficially applied |
| Methodology | Detailed, justified, replicable | Adequate but missing some details | Vague, inappropriate, or unjustified |
| Feasibility | Realistic timeline, accessible population, obtainable data | Feasible with some concerns | Unrealistic scope, timeline, or access |
| Writing quality | Clear, concise, professional academic prose | Generally clear with some rough areas | Unclear, verbose, or unprofessional |

### Proposal Defense Outcomes

| Outcome | Meaning | Next Steps |
|---------|---------|------------|
| Pass without revisions | Rare. Proposal is ready as-is. | Proceed to IRB and data collection |
| Pass with minor revisions | Most common. Small changes needed. | Make revisions; advisor approves; no re-defense |
| Pass with major revisions | Significant changes required. | Make revisions; committee reviews; may or may not re-defend |
| Revise and resubmit | Proposal is not ready. | Major rewriting required; must re-defend |
| Fail | Very rare. Fundamental problems. | May need to change topic, advisor, or reconsider program |

---

## 2. Literature Review Strategies

### Search Strategy Documentation

```markdown
## Systematic Literature Search Strategy

### Databases Searched
1. [Database name] — Date searched: [Date]
2. [Database name] — Date searched: [Date]
3. [Database name] — Date searched: [Date]

### Search Terms

| Concept | Search Terms | Boolean |
|---------|-------------|---------|
| Concept 1 | "term A" OR "term B" OR "synonym C" | OR within concept |
| Concept 2 | "term D" OR "term E" OR "synonym F" | OR within concept |
| Concept 3 | "term G" OR "term H" | OR within concept |
| Combined | Concept 1 AND Concept 2 AND Concept 3 | AND across concepts |

### Inclusion Criteria
- Published between [Year] and [Year]
- Peer-reviewed journals
- English language (or specify others)
- [Other criteria relevant to your review]

### Exclusion Criteria
- Conference abstracts only (no full text)
- [Other criteria]

### Search Results

| Database | Initial Hits | After Dedup | After Title/Abstract Screen | After Full-Text Screen | Included |
|----------|-------------|-------------|---------------------------|----------------------|----------|
| PubMed | 342 | 298 | 87 | 42 | 38 |
| PsycINFO | 215 | 156 | 45 | 28 | 25 |
| ERIC | 178 | 134 | 38 | 18 | 15 |
| **Total** | **735** | **588** | **170** | **88** | **78** |

### Additional Sources
- Backward citation searching (reference lists of included studies): [N] additional
- Forward citation searching (Google Scholar "cited by"): [N] additional
- Expert recommendations: [N] additional
```

### Synthesis Matrix

```markdown
## Synthesis Matrix

| Source | Year | Method | Sample | Key Findings | Theme 1 | Theme 2 | Theme 3 | Quality |
|--------|------|--------|--------|-------------|---------|---------|---------|---------|
| Smith | 2022 | Quantitative (survey) | 450 faculty | Positive correlation between X and Y | X | | X | High |
| Jones | 2021 | Qualitative (interviews) | 15 faculty | Three themes emerged: A, B, C | X | X | | Medium |
| Lee | 2023 | Mixed methods | 200 + 20 | Quantitative confirmed; qualitative nuanced | X | X | X | High |
| Brown | 2020 | Meta-analysis | 35 studies | Overall effect size d = 0.45 | | X | | High |
```

### Writing the Literature Review — Paragraph Structure

Each paragraph in a literature review should follow this structure:

```
Topic sentence:     State the point this paragraph will make
Evidence:           Cite 2-4 studies that support, challenge, or nuance the point
Synthesis:          Compare/contrast findings across studies
Connection:         Link to your study's research questions or framework
Transition:         Bridge to the next paragraph
```

Example:

```
Several studies have examined the relationship between mentoring quality
and doctoral completion rates (Topic). Smith (2022) found that students
who met weekly with their advisor were 2.3 times more likely to complete
within six years, while Jones (2021) reported that meeting frequency
mattered less than the perceived quality of feedback (Evidence). Together,
these findings suggest that it is not merely access to a supervisor but
the nature of the interaction that predicts success (Synthesis). This
aligns with the present study's focus on supervisory practices rather
than structural factors (Connection). However, the role of peer support
networks, which may moderate the advisor-student relationship, has
received less attention (Transition to next paragraph).
```

---

## 3. Data Analysis Decision Trees

### Quantitative Analysis Selection

```
What is your research question type?
│
├── DIFFERENCE between groups
│   ├── How many groups?
│   │   ├── 2 groups
│   │   │   ├── Independent? → Independent samples t-test
│   │   │   └── Related/paired? → Paired samples t-test
│   │   └── 3+ groups
│   │       ├── Independent? → One-way ANOVA
│   │       │   └── Significant? → Post-hoc tests (Tukey, Bonferroni)
│   │       └── Related? → Repeated measures ANOVA
│   ├── Need to control covariates? → ANCOVA
│   └── Multiple DVs? → MANOVA
│
├── RELATIONSHIP between variables
│   ├── Two continuous variables → Pearson or Spearman correlation
│   ├── Predicting a continuous DV
│   │   ├── One predictor → Simple linear regression
│   │   └── Multiple predictors → Multiple regression
│   │       ├── All entered together → Simultaneous
│   │       ├── Theory-driven order → Hierarchical
│   │       └── Data-driven → Stepwise (use cautiously)
│   └── Predicting a categorical DV → Logistic regression
│
├── STRUCTURE in data
│   ├── Reduce variables → Factor analysis (EFA/CFA)
│   ├── Group cases → Cluster analysis
│   └── Nested data (students in classrooms) → Multilevel modeling (HLM)
│
└── Non-parametric alternatives (when assumptions violated)
    ├── t-test → Mann-Whitney U (independent) / Wilcoxon (paired)
    ├── ANOVA → Kruskal-Wallis
    ├── Correlation → Spearman's rho
    └── Chi-square → Fisher's exact test (small samples)
```

### Qualitative Analysis Selection

```
What is your analytical goal?
│
├── Identify patterns/themes across dataset
│   └── Thematic Analysis (Braun & Clarke)
│
├── Generate theory from data
│   └── Grounded Theory (Strauss & Corbin; Charmaz)
│
├── Understand lived experience in depth
│   └── IPA (Smith et al.) or Phenomenology (Moustakas)
│
├── Describe cultural patterns
│   └── Ethnographic analysis
│
├── Understand experience through stories
│   └── Narrative analysis
│
├── Categorize manifest content systematically
│   └── Content analysis
│
└── Analyze in-depth bounded system
    └── Case study analysis (Yin)
```

---

## 4. Committee Management

### Selecting Committee Members

| Consideration | Questions to Ask |
|--------------|-----------------|
| Expertise | Does this person have knowledge relevant to my topic, theory, or methods? |
| Availability | Will they be available for the duration of my study? (Sabbatical? Retirement?) |
| Compatibility | Do their supervision style and expectations align with mine and my advisor's? |
| Track record | Do their students finish? On time? Do they attend meetings and provide timely feedback? |
| Strategic value | Can they open doors to networks, publications, or positions? |
| Balance | Does the committee as a whole cover all my needs (content, methods, theory)? |

### Committee Communication Protocol

```markdown
## Committee Communication Guide

### Regular Updates (quarterly or per milestone)
- Brief email to full committee
- 1-2 paragraphs: progress, next steps, timeline status
- Attach any relevant documents

### Before Committee Meetings
- Send agenda + documents 2 weeks in advance
- Confirm date/time 1 month in advance
- Book room/set up video link

### After Committee Meetings
- Send summary of decisions and action items within 1 week
- Note any disagreements among committee members and how they were resolved
- Update timeline based on committee input

### Managing Conflicting Feedback
1. Identify the specific disagreement
2. Discuss with your advisor first
3. If unresolved, request a committee meeting to discuss
4. Document the resolution and the rationale
5. In the dissertation, acknowledge the tension if it represents
   a genuine debate in the field
```

---

## 5. Formatting Quick Reference

### Front Matter Order (typical)

```
1. Title page
2. Copyright page (optional)
3. Approval/signature page
4. Abstract
5. Dedication (optional)
6. Acknowledgments
7. Table of contents
8. List of tables
9. List of figures
10. List of abbreviations (if needed)
```

### Back Matter Order (typical)

```
1. References / Bibliography
2. Appendices
   A. IRB approval letter
   B. Informed consent form
   C. Survey instrument / interview protocol
   D. Codebook (qualitative)
   E. Additional tables or figures
   F. Permission letters (for copyrighted materials)
```

### Common Formatting Errors to Check

```markdown
## Pre-Submission Formatting Checklist

### Document-Level
- [ ] Margins consistent throughout (check after inserting tables/figures)
- [ ] Font consistent throughout (including headers, footers, table text)
- [ ] Page numbers correct and continuous
- [ ] Running head correct (if required)
- [ ] All chapters start on new page

### Headings
- [ ] Heading levels consistent with style guide
- [ ] Table of contents matches actual headings and page numbers
- [ ] No orphan headings (heading at bottom of page with text on next page)

### Tables and Figures
- [ ] All tables/figures referenced in text before they appear
- [ ] Numbering is sequential and correct
- [ ] Titles follow style guide format
- [ ] Notes present when needed
- [ ] Tables do not break awkwardly across pages

### Citations and References
- [ ] Every in-text citation has a reference list entry
- [ ] Every reference list entry has at least one in-text citation
- [ ] Citation format is consistent (no mixing styles)
- [ ] DOIs included where available
- [ ] Hanging indent in reference list

### Appendices
- [ ] Each appendix has a title
- [ ] Appendices referenced in text
- [ ] Page numbers continue from body text
- [ ] IRB approval letter included

### Final Steps
- [ ] Run spell-check one final time
- [ ] Convert to PDF and check formatting is preserved
- [ ] Check that all hyperlinks work (if electronic submission)
- [ ] Verify file size meets submission requirements
```

---

## 6. Post-Defense: Publishing from Your Dissertation

### Strategies for Converting Chapters to Journal Articles

| Approach | Description | Effort | Timeline |
|----------|-------------|--------|----------|
| Single comprehensive article | Condense entire dissertation into one article | High (must cut 80%+ of content) | 3-6 months |
| Results-focused article | Chapter 4 + key elements of 1, 3, 5 | Medium | 2-4 months |
| Methodology article | If your methods are novel, publish the methodology separately | Medium | 2-3 months |
| Literature review article | Chapter 2 as a standalone review (if systematic or comprehensive) | Medium | 2-4 months |
| Multiple articles | Different RQs or themes as separate publications | Varies | 6-12 months |

### Key Differences: Dissertation vs. Journal Article

| Feature | Dissertation | Journal Article |
|---------|-------------|-----------------|
| Length | 150-300+ pages | 5,000-10,000 words |
| Audience | Committee (experts who want detail) | Journal readers (experts who want efficiency) |
| Literature review | Comprehensive (prove you know the field) | Focused (set up the specific gap) |
| Methodology | Exhaustive detail | Sufficient for replication |
| Results | Complete (every analysis) | Selective (most important findings) |
| Discussion | Thorough implications and future research | Concise; focused on contribution |
| Tone | Sometimes instructional | Peer-to-peer scholarly discourse |

---

## Key References

- APA. (2020). *Publication manual of the American Psychological Association* (7th ed.). American Psychological Association.
- Bolker, J. (1998). *Writing your dissertation in fifteen minutes a day*. Holt.
- Dunleavy, P. (2003). *Authoring a PhD*. Palgrave Macmillan.
- Murray, R. (2011). *How to write a thesis* (3rd ed.). Open University Press.
- Paltridge, B., & Starfield, S. (2020). *Thesis and dissertation writing in a second language* (2nd ed.). Routledge.
- Roberts, C. M. (2010). *The dissertation journey* (2nd ed.). Corwin.
- Turabian, K. L. (2018). *A manual for writers* (9th ed.). University of Chicago Press.
- University of Chicago Press. (2017). *The Chicago manual of style* (17th ed.). University of Chicago Press.
- Wisker, G. (2012). *The good supervisor* (2nd ed.). Palgrave Macmillan.

---
name: alterlab-social-science-methods
description: "Guides advanced social science research methods — discourse analysis (Fairclough CDA, Gee), conversation analysis, quantitative content analysis, Qualitative Comparative Analysis (QCA), process tracing, archival research, participatory/community-based research (PAR, CBPR), Delphi and Q methodology, social network analysis (SNA), bibliometrics and scientometrics, systematic mapping reviews, and program/policy evaluation. Use when designing or conducting any of these studies — choosing a specialized method, building a coding scheme, establishing causal mechanisms in case studies, mapping relational or subjective data, or applying an evaluation framework. For interpretive/qualitative coding (thematic analysis, grounded theory, IPA, ethnography, qualitative content analysis) use alterlab-qualitative-methods; for combining qual+quant strands use alterlab-mixed-methods. Part of the AlterLab Academic Skills suite."
license: MIT
allowed-tools: Read Write Edit Bash(python:*)
compatibility: No API key required. Guidance-focused skill; optional Python helpers run via `uv run python`.
metadata:
  skill-author: AlterLab
  version: "1.0.0"
  last_updated: "2026-03-18"
---

# Social Science Research Methods

## Overview

Social science research encompasses a remarkably diverse methodological landscape. Beyond the familiar quantitative-qualitative divide lie specialized methods refined over decades within particular disciplinary traditions -- each carrying specific epistemological commitments, analytical procedures, and quality criteria. This skill covers advanced and specialized methods that go beyond introductory courses: discourse analysis in its multiple traditions, conversation analysis, quantitative content analysis, comparative methods including Qualitative Comparative Analysis (QCA), process tracing, archival research, participatory and community-based research, the Delphi method and Q methodology, social network analysis, bibliometrics and scientometrics, systematic mapping reviews, and program evaluation and policy analysis.

It is designed for faculty and researchers across the social sciences -- sociology, political science, education, public health, communication, public policy, social work, and interdisciplinary fields. Many of these methods are also used in the humanities and applied fields such as management, urban planning, and international development.

The skill body below is a router: it states what each method is, when to reach for it, and where the full procedures, worked examples, and reference tables live. Detailed content has been split into the `references/` files indexed at the end.

## When to Use This Skill

Use this skill when you need to:

- Conduct or design a discourse analysis study using Fairclough's CDA or Gee's framework
- Analyze naturally occurring talk-in-interaction using conversation analysis (CA)
- Design a quantitative content analysis with reliable coding schemes
- Apply Qualitative Comparative Analysis (QCA) or Mill's methods for cross-case comparison
- Use process tracing to establish causal mechanisms in case study research
- Plan and conduct archival research with primary historical sources
- Design a participatory action research (PAR) or community-based participatory research (CBPR) project
- Implement a Delphi study to build expert consensus
- Conduct a Q methodology study to map subjective viewpoints
- Perform social network analysis (SNA) on relational data
- Conduct bibliometric or scientometric analysis of scholarly literatures
- Design a systematic mapping review (as distinct from a systematic review)
- Plan a program evaluation using established frameworks
- Conduct policy analysis using structured analytical approaches

## Method Families at a Glance

### Language-focused interpretive methods

- **Discourse analysis** examines how language constructs social reality. Two dominant traditions: **Fairclough's Critical Discourse Analysis (CDA)**, a three-dimensional framework linking text, discursive practice, and social practice; and **Gee's discourse analysis**, organized around seven building tasks of language. Both assume a constructionist epistemology.
- **Conversation analysis (CA)** studies the sequential organization of naturally occurring talk-in-interaction (turn-taking, preference organization, repair). It is empirical and data-driven, using fine-grained Jefferson-system transcription.
- **Quantitative content analysis** systematically codes textual/visual/audio content into categories and analyzes them statistically, prioritizing reliability (intercoder agreement) and generalizability over interpretive depth.

Full procedures, the CDA and CA worked examples, Gee's seven tasks, the Jefferson transcription table, and the intercoder-reliability metrics table are in `references/discourse-and-conversation-analysis.md`. The CDA analytical checklist and a discourse-framework selection guide are in `references/social-science-frameworks.md`.

### Comparative and case-based methods

- **QCA** (Ragin) uses Boolean algebra and set theory to analyze causal complexity across medium-N cases (10-50). Variants: csQCA, fsQCA, mvQCA.
- **Mill's methods** (agreement, difference, concomitant variation, joint) guide comparative case selection.
- **Process tracing** is a within-case method for identifying causal mechanisms, using hoop / smoking-gun / doubly-decisive / straw-in-the-wind evidence tests.
- **Archival research** systematically analyzes primary source documents, evaluated for authenticity, reliability, representativeness, and meaning.

Variant tables, fsQCA steps, the QCA truth-table example, the four process-tracing test types, and the archival workflow are in `references/comparative-and-case-methods.md`. QCA calibration methods, truth-table analysis steps, QCA reporting standards, and process-tracing causal-mechanism and evidence-evaluation templates are in `references/social-science-frameworks.md`.

### Participatory and consensus methods

- **PAR / CBPR** position community members as co-researchers (research *with*, not *on*, communities), guided by the nine Israel et al. (2005) principles and a five-phase partnership process.
- **Delphi method** builds expert consensus through structured, anonymized, iterative rating rounds against pre-defined consensus thresholds.
- **Q methodology** maps subjective viewpoints by having participants rank-order statements into a forced distribution, then factor-analyzing the sorts.

CBPR principles and phases, the Delphi process and consensus thresholds, and Q methodology steps are in `references/participatory-and-consensus-methods.md`. A Delphi reporting checklist is in `references/social-science-frameworks.md`.

### Relational, bibliometric, review, and evaluation methods

- **Social network analysis (SNA)** examines the structure of relationships between actors via centrality, density, clustering, homophily, and structural-hole measures; software ranges from Gephi to statnet/ERGM.
- **Bibliometrics / scientometrics** map research fields through citation, co-citation, bibliographic-coupling, co-authorship, and keyword co-occurrence analysis.
- **Systematic mapping (scoping) reviews** broadly chart the volume and nature of evidence without synthesizing effect sizes; report against PRISMA-ScR.
- **Program evaluation** uses frameworks (Logic Model, Theory of Change, RE-AIM, CIPP, Utilization-Focused, Developmental, Empowerment); **policy analysis** uses Bardach's Eightfold Path and CBA/CEA.

The SNA concept and software tables, the research-question-to-measure mapping example, bibliometric techniques and tools, the mapping-vs-systematic-review comparison, PRISMA-ScR items, the evaluation-framework table, the logic-model template, and policy-analysis methods are in `references/network-bibliometric-evaluation.md`. The SNA measures quick reference, the ERGM guide, the full bibliometric study protocol, and Theory of Change / RE-AIM templates are in `references/social-science-frameworks.md`.

## Best Practices

### Method Selection

1. **Start with the question, not the method** -- The research question should drive method selection. Ask: what kind of evidence would answer my question?
2. **Consider mixed methods** -- Many questions benefit from combining approaches (e.g., QCA for cross-case patterns + process tracing for within-case mechanisms).
3. **Match epistemology to method** -- Discourse analysis assumes constructionist epistemology; QCA assumes configurational causation. Ensure your assumptions align with your method.
4. **Be realistic about resources** -- Archival research requires travel and time; CBPR requires long-term community relationships; SNA requires relational data that may be hard to collect.
5. **Study exemplars** -- Read 5-10 published studies that use your chosen method well before designing your own.

### Rigor and Quality

1. **Transparent reporting** -- Document every analytical decision, not just the results.
2. **Reliability** -- In content analysis, report intercoder reliability; in qualitative methods, keep audit trails.
3. **Validity** -- Use member checking, triangulation, and negative case analysis.
4. **Reflexivity** -- In interpretive methods, acknowledge how your positionality shapes the analysis.
5. **Replicability** -- Share data and materials to the extent ethically possible.

### Ethics

1. **Informed consent** -- Ensure participants understand what they are agreeing to, especially in participatory and archival research.
2. **Community benefit** -- In CBPR, ensure the research benefits the community, not just the researcher.
3. **Power dynamics** -- Be attentive to power differentials between researchers and participants, institutions and communities.
4. **Data sensitivity** -- Social science data often involves personal information; follow institutional and legal requirements for data protection.
5. **Representation** -- Report findings in ways that do not stigmatize or misrepresent communities.

## Common Pitfalls

- **Discourse analysis** -- Cherry-picking supportive extracts; over-interpreting mundane language; ignoring conditions of production/reception; conflating description with analysis.
- **Comparative methods** -- Too many conditions for the number of cases (aim for >=3 cases per condition); atheoretical / data-mined conditions; dismissing rather than explaining contradictory cases; treating Boolean minimization as a substitute for case knowledge.
- **Process tracing** -- Confirmation bias; relying on a single "decisive" piece of evidence; conflating within-case co-occurrence with mechanism; failing to test competing explanations.
- **CBPR** -- Tokenistic participation; extractive research; unresolved power dynamics dressed as "equal partnership"; conflicting academic vs. community timelines.
- **SNA** -- Incorrect network boundary specification; missing/non-response data (more damaging than in attribute surveys); reading structural position as causal; ignoring tie strength and direction.

## References

Detailed procedures, worked examples, reference tables, and code blocks live in `references/`:

- **`references/discourse-and-conversation-analysis.md`** -- Fairclough CDA framework + policy-document worked example; Gee's seven building tasks and analytical tools; CA principles, the Jefferson transcription table, and the doctor-patient worked example; quantitative content analysis steps and the intercoder-reliability metrics table.
- **`references/comparative-and-case-methods.md`** -- QCA variants and fsQCA steps, the truth-table worked example; Mill's methods; process tracing variants and the four evidence-test types; archival source types, the four evaluation questions, and the archival workflow.
- **`references/participatory-and-consensus-methods.md`** -- CBPR principles and five-phase process; the Delphi process and consensus-threshold table; Q methodology steps.
- **`references/network-bibliometric-evaluation.md`** -- SNA concept and software tables and the question-to-measure mapping; bibliometric techniques and tools; mapping-vs-systematic-review comparison and PRISMA-ScR items; the evaluation-framework table and logic-model template; policy analysis (Bardach's Eightfold Path, CBA/CEA).
- **`references/social-science-frameworks.md`** -- Deep-dive supplement: discourse-framework selection guide, CDA analytical checklist, QCA calibration and reporting standards, process-tracing templates, SNA measures quick reference and ERGM guide, the full bibliometric study protocol, Theory of Change and RE-AIM templates, the Delphi reporting checklist, and an essential reading list by method.

### Key foundational texts

- Fairclough, N. (2003). *Analysing Discourse: Textual Analysis for Social Research*. Routledge.
- Gee, J. P. (2014). *An Introduction to Discourse Analysis: Theory and Method* (4th ed.). Routledge.
- Sacks, H., Schegloff, E. A., & Jefferson, G. (1974). A simplest systematics for the organization of turn-taking for conversation. *Language*, 50(4), 696-735.
- Ragin, C. C. (2008). *Redesigning Social Inquiry: Fuzzy Sets and Beyond*. University of Chicago Press.
- Beach, D., & Pedersen, R. B. (2019). *Process-Tracing Methods: Foundations and Guidelines* (2nd ed.). University of Michigan Press.
- Israel, B. A., Eng, E., Schulz, A. J., & Parker, E. A. (Eds.). (2005). *Methods in Community-Based Participatory Research for Health*. Jossey-Bass.
- Wasserman, S., & Faust, K. (1994). *Social Network Analysis: Methods and Applications*. Cambridge University Press.
- Aria, M., & Cuccurullo, C. (2017). bibliometrix: An R-tool for comprehensive science mapping analysis. *Journal of Informetrics*, 11(4), 959-975.
- Patton, M. Q. (2010). *Developmental Evaluation: Applying Complexity Concepts to Enhance Innovation and Use*. Guilford Press.
- Bardach, E., & Patashnik, E. M. (2019). *A Practical Guide for Policy Analysis* (6th ed.). CQ Press.

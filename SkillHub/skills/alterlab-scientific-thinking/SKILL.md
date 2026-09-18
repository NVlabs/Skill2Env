---
name: alterlab-scientific-thinking
description: Evaluate scientific claims and evidence quality using evidence grading frameworks (GRADE, Cochrane Risk of Bias), assessing experimental design validity and identifying biases, confounders, statistical pitfalls, and logical fallacies. Use when judging evidence quality, grading certainty of evidence, spotting design or causal-inference flaws, identifying biases or confounders, naming statistical fallacies, or teaching critical analysis. For writing a formal submittable peer review use alterlab-peer-review; for a multi-reviewer mock panel verdict use alterlab-paper-reviewer; for IRB/consent/conflict-of-interest ethics use alterlab-research-ethics. Part of the AlterLab Academic Skills suite.
allowed-tools: Read Write Edit Bash
license: MIT
compatibility: No API key required. Guidance-focused skill; optional Python helpers run via `uv run python`.
metadata:
    skill-author: AlterLab
    version: "1.0.0"
---

# Scientific Critical Thinking

## Overview

Critical thinking is a systematic process for evaluating scientific rigor. Assess methodology, experimental design, statistical validity, biases, confounding, and evidence quality using GRADE and Cochrane ROB frameworks. Apply this skill for critical analysis of scientific claims.

## When to Use This Skill

This skill should be used when:
- Evaluating research methodology and experimental design
- Assessing statistical validity and evidence quality
- Identifying biases and confounding in studies
- Reviewing scientific claims and conclusions
- Conducting systematic reviews or meta-analyses
- Applying GRADE or Cochrane risk of bias assessments
- Providing critical analysis of research papers

## Core Capabilities

### 1. Methodology Critique

Evaluate research methodology for rigor, validity, and potential flaws.

**Apply when:**
- Reviewing research papers
- Assessing experimental designs
- Evaluating study protocols
- Planning new research

**Evaluation framework:**

1. **Study Design Assessment**
   - Is the design appropriate for the research question?
   - Can the design support causal claims being made?
   - Are comparison groups appropriate and adequate?
   - Consider whether experimental, quasi-experimental, or observational design is justified

2. **Validity Analysis**
   - **Internal validity:** Can we trust the causal inference?
     - Check randomization quality
     - Evaluate confounding control
     - Assess selection bias
     - Review attrition/dropout patterns
   - **External validity:** Do results generalize?
     - Evaluate sample representativeness
     - Consider ecological validity of setting
     - Assess whether conditions match target application
   - **Construct validity:** Do measures capture intended constructs?
     - Review measurement validation
     - Check operational definitions
     - Assess whether measures are direct or proxy
   - **Statistical conclusion validity:** Are statistical inferences sound?
     - Verify adequate power/sample size
     - Check assumption compliance
     - Evaluate test appropriateness

3. **Control and Blinding**
   - Was randomization properly implemented (sequence generation, allocation concealment)?
   - Was blinding feasible and implemented (participants, providers, assessors)?
   - Are control conditions appropriate (placebo, active control, no treatment)?
   - Could performance or detection bias affect results?

4. **Measurement Quality**
   - Are instruments validated and reliable?
   - Are measures objective when possible, or subjective with acknowledged limitations?
   - Is outcome assessment standardized?
   - Are multiple measures used to triangulate findings?

**Reference:** See `references/scientific_method.md` for detailed principles and `references/experimental_design.md` for comprehensive design checklist.

### 2. Bias Detection

Identify and evaluate potential sources of bias that could distort findings.

**Apply when:**
- Reviewing published research
- Designing new studies
- Interpreting conflicting evidence
- Assessing research quality

**Systematic bias review** spans five families: cognitive biases (confirmation, HARKing, publication bias, cherry-picking), selection biases (sampling, volunteer, attrition, survivorship), measurement biases (observer, recall, social desirability, instrument), analysis biases (p-hacking, outcome switching, selective reporting, subgroup fishing), and confounding (measured, unmeasured, and alternative explanations).

**Reference:** Full detection-question checklist for every bias in each family moved to `references/evaluation_checklists.md` (Bias Detection section). See `references/common_biases.md` for the comprehensive bias taxonomy with mitigation strategies.

### 3. Statistical Analysis Evaluation

Critically assess statistical methods, interpretation, and reporting.

**Apply when:**
- Reviewing quantitative research
- Evaluating data-driven claims
- Assessing clinical trial results
- Reviewing meta-analyses

**Statistical review checklist** covers eight areas: sample size and power, statistical test appropriateness, multiple-comparison correction, p-value interpretation, effect sizes and confidence intervals, missing-data handling, regression/modeling assumptions, and common pitfalls (correlation-as-causation, regression to the mean, base-rate neglect, Texas sharpshooter, Simpson's paradox).

**Reference:** Full question-by-question checklist for all eight areas moved to `references/evaluation_checklists.md` (Statistical Analysis Evaluation section). See `references/statistical_pitfalls.md` for detailed pitfalls and correct practices.

### 4. Evidence Quality Assessment

Evaluate the strength and quality of evidence systematically.

**Apply when:**
- Weighing evidence for decisions
- Conducting literature reviews
- Comparing conflicting findings
- Determining confidence in conclusions

**Evidence evaluation framework** works through five components: the study-design hierarchy (meta-analysis down to expert opinion, with the caveat that level does not guarantee quality), quality within a design type (risk-of-bias tools, rigor, transparency, conflicts of interest), GRADE considerations (start from design type, then downgrade/upgrade), convergence of evidence (what makes it stronger vs. weaker), and contextual factors (plausibility, consistency, temporality, specificity, strength).

**Reference:** Full framework with the complete GRADE downgrade/upgrade criteria and convergence signals moved to `references/evaluation_checklists.md` (Evidence Quality Assessment section). See `references/evidence_hierarchy.md` for the detailed hierarchy, GRADE system, and quality assessment tools.

### 5. Logical Fallacy Identification

Detect and name logical errors in scientific arguments and claims.

**Apply when:**
- Evaluating scientific claims
- Reviewing discussion/conclusion sections
- Assessing popular science communication
- Identifying flawed reasoning

**Common fallacies in science** fall into six categories: causation fallacies (post hoc, correlation = causation, reverse causation, single cause), generalization fallacies (hasty generalization, anecdotal, cherry-picking, ecological), authority/source fallacies (appeal to authority, ad hominem, genetic, appeal to nature), statistical fallacies (base-rate neglect, Texas sharpshooter, multiple comparisons, prosecutor's fallacy), structural fallacies (false dichotomy, moving goalposts, begging the question, straw man), and science-specific fallacies (Galileo gambit, argument from ignorance, nirvana fallacy, unfalsifiability).

**Reference:** Full fallacy catalog with the plain-language definition of each named fallacy moved to `references/evaluation_checklists.md` (Logical Fallacy Identification section). See `references/logical_fallacies.md` for examples and detection strategies.

**When identifying fallacies:**
- Name the specific fallacy
- Explain why the reasoning is flawed
- Identify what evidence would be needed for valid inference
- Note that fallacious reasoning doesn't prove the conclusion false—just that this argument doesn't support it

**Reference:** See `references/logical_fallacies.md` for comprehensive fallacy catalog with examples and detection strategies.

### 6. Research Design Guidance

Provide constructive guidance for planning rigorous studies.

**Apply when:**
- Helping design new experiments
- Planning research projects
- Reviewing research proposals
- Improving study protocols

**Design process:**

1. **Research Question Refinement**
   - Ensure question is specific, answerable, and falsifiable
   - Verify it addresses a gap or contradiction in literature
   - Confirm feasibility (resources, ethics, time)
   - Define variables operationally

2. **Design Selection**
   - Match design to question (causal → experimental; associational → observational)
   - Consider feasibility and ethical constraints
   - Choose between-subjects, within-subjects, or mixed designs
   - Plan factorial designs if testing multiple factors

3. **Bias Minimization Strategy**
   - Implement randomization when possible
   - Plan blinding at all feasible levels (participants, providers, assessors)
   - Identify and plan to control confounds (randomization, matching, stratification, statistical adjustment)
   - Standardize all procedures
   - Plan to minimize attrition

4. **Sample Planning**
   - Conduct a priori power analysis (specify expected effect, desired power, alpha)
   - Account for attrition in sample size
   - Define clear inclusion/exclusion criteria
   - Consider recruitment strategy and feasibility
   - Plan for sample representativeness

5. **Measurement Strategy**
   - Select validated, reliable instruments
   - Use objective measures when possible
   - Plan multiple measures of key constructs (triangulation)
   - Ensure measures are sensitive to expected changes
   - Establish inter-rater reliability procedures

6. **Analysis Planning**
   - Prespecify all hypotheses and analyses
   - Designate primary outcome clearly
   - Plan statistical tests with assumption checks
   - Specify how missing data will be handled
   - Plan to report effect sizes and confidence intervals
   - Consider multiple comparison corrections

7. **Transparency and Rigor**
   - Preregister study and analysis plan
   - Use reporting guidelines (CONSORT, STROBE, PRISMA)
   - Plan to report all outcomes, not just significant ones
   - Distinguish confirmatory from exploratory analyses
   - Commit to data/code sharing

**Reference:** See `references/experimental_design.md` for comprehensive design checklist covering all stages from question to dissemination.

### 7. Claim Evaluation

Systematically evaluate scientific claims for validity and support.

**Apply when:**
- Assessing conclusions in papers
- Evaluating media reports of research
- Reviewing abstract or introduction claims
- Checking if data support conclusions

**Claim evaluation process:**

1. **Identify the Claim**
   - What exactly is being claimed?
   - Is it a causal claim, associational claim, or descriptive claim?
   - How strong is the claim (proven, likely, suggested, possible)?

2. **Assess the Evidence**
   - What evidence is provided?
   - Is evidence direct or indirect?
   - Is evidence sufficient for the strength of claim?
   - Are alternative explanations ruled out?

3. **Check Logical Connection**
   - Do conclusions follow from the data?
   - Are there logical leaps?
   - Is correlational data used to support causal claims?
   - Are limitations acknowledged?

4. **Evaluate Proportionality**
   - Is confidence proportional to evidence strength?
   - Are hedging words used appropriately?
   - Are limitations downplayed?
   - Is speculation clearly labeled?

5. **Check for Overgeneralization**
   - Do claims extend beyond the sample studied?
   - Are population restrictions acknowledged?
   - Is context-dependence recognized?
   - Are caveats about generalization included?

6. **Red Flags**
   - Causal language from correlational studies
   - "Proves" or absolute certainty
   - Cherry-picked citations
   - Ignoring contradictory evidence
   - Dismissing limitations
   - Extrapolation beyond data

**Provide specific feedback:**
- Quote the problematic claim
- Explain what evidence would be needed to support it
- Suggest appropriate hedging language if warranted
- Distinguish between data (what was found) and interpretation (what it means)

## Application Guidelines

### General Approach

1. **Be Constructive**
   - Identify strengths as well as weaknesses
   - Suggest improvements rather than just criticizing
   - Distinguish between fatal flaws and minor limitations
   - Recognize that all research has limitations

2. **Be Specific**
   - Point to specific instances (e.g., "Table 2 shows..." or "In the Methods section...")
   - Quote problematic statements
   - Provide concrete examples of issues
   - Reference specific principles or standards violated

3. **Be Proportionate**
   - Match criticism severity to issue importance
   - Distinguish between major threats to validity and minor concerns
   - Consider whether issues affect primary conclusions
   - Acknowledge uncertainty in your own assessments

4. **Apply Consistent Standards**
   - Use same criteria across all studies
   - Don't apply stricter standards to findings you dislike
   - Acknowledge your own potential biases
   - Base judgments on methodology, not results

5. **Consider Context**
   - Acknowledge practical and ethical constraints
   - Consider field-specific norms for effect sizes and methods
   - Recognize exploratory vs. confirmatory contexts
   - Account for resource limitations in evaluating studies

### When Providing Critique

**Structure feedback as:**

1. **Summary:** Brief overview of what was evaluated
2. **Strengths:** What was done well (important for credibility and learning)
3. **Concerns:** Issues organized by severity
   - Critical issues (threaten validity of main conclusions)
   - Important issues (affect interpretation but not fatally)
   - Minor issues (worth noting but don't change conclusions)
4. **Specific Recommendations:** Actionable suggestions for improvement
5. **Overall Assessment:** Balanced conclusion about evidence quality and what can be concluded

**Use precise terminology:**
- Name specific biases, fallacies, and methodological issues
- Reference established standards and guidelines
- Cite principles from scientific methodology
- Use technical terms accurately

### When Uncertain

- **Acknowledge uncertainty:** "This could be X or Y; additional information needed is Z"
- **Ask clarifying questions:** "Was [methodological detail] done? This affects interpretation."
- **Provide conditional assessments:** "If X was done, then Y follows; if not, then Z is concern"
- **Note what additional information would resolve uncertainty**

## Reference Materials

This skill includes comprehensive reference materials that provide detailed frameworks for critical evaluation:

- **`references/scientific_method.md`** - Core principles of scientific methodology, the scientific process, critical evaluation criteria, red flags in scientific claims, causal inference standards, peer review, and open science principles

- **`references/common_biases.md`** - Comprehensive taxonomy of cognitive, experimental, methodological, statistical, and analysis biases with detection and mitigation strategies

- **`references/statistical_pitfalls.md`** - Common statistical errors and misinterpretations including p-value misunderstandings, multiple comparisons problems, sample size issues, effect size mistakes, correlation/causation confusion, regression pitfalls, and meta-analysis issues

- **`references/evidence_hierarchy.md`** - Traditional evidence hierarchy, GRADE system, study quality assessment criteria, domain-specific considerations, evidence synthesis principles, and practical decision frameworks

- **`references/logical_fallacies.md`** - Logical fallacies common in scientific discourse organized by type (causation, generalization, authority, relevance, structure, statistical) with examples and detection strategies

- **`references/experimental_design.md`** - Comprehensive experimental design checklist covering research questions, hypotheses, study design selection, variables, sampling, blinding, randomization, control groups, procedures, measurement, bias minimization, data management, statistical planning, ethical considerations, validity threats, and reporting standards

- **`references/evaluation_checklists.md`** - Operational, question-form review checklists for the Bias Detection, Statistical Analysis Evaluation, Evidence Quality Assessment, and Logical Fallacy Identification capabilities (the full item-by-item detail relocated from the Core Capabilities section)

**When to consult references:**
- Load references into context when detailed frameworks are needed
- Use grep to search references for specific topics: `grep -r "pattern" references/`
- References provide depth; SKILL.md provides procedural guidance
- Consult references for comprehensive lists, detailed criteria, and specific examples

## Remember

**Scientific critical thinking is about:**
- Systematic evaluation using established principles
- Constructive critique that improves science
- Proportional confidence to evidence strength
- Transparency about uncertainty and limitations
- Consistent application of standards
- Recognition that all research has limitations
- Balance between skepticism and openness to evidence

**Always distinguish between:**
- Data (what was observed) and interpretation (what it means)
- Correlation and causation
- Statistical significance and practical importance
- Exploratory and confirmatory findings
- What is known and what is uncertain
- Evidence against a claim and evidence for the null

**Goals of critical thinking:**
1. Identify strengths and weaknesses accurately
2. Determine what conclusions are supported
3. Recognize limitations and uncertainties
4. Suggest improvements for future work
5. Advance scientific understanding


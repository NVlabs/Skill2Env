# Research Methods and Approach: Writing the Methodology

## Overview

The methods (or "Approach") section is where reviewers decide whether the proposed work is **feasible** and **rigorous**. A brilliant idea with a vague or flawed approach will not be funded. This guide covers how to write methodology that demonstrates competence, anticipates problems, and satisfies agency expectations for rigor and reproducibility.

**Core Principle**: Provide enough detail for an expert reviewer to judge feasibility, while keeping the narrative readable. Push exhaustive protocol detail to supplementary materials where the agency allows it.

## General Structure of a Methods Section

A well-organized approach typically moves through these elements for each aim or objective:

1. **Rationale and design overview** — Why this approach? What is the overall experimental or analytical design?
2. **Detailed procedures** — Materials, instruments, datasets, protocols, and sequence of steps.
3. **Analysis plan** — How data will be analyzed, including statistics or computational methods.
4. **Expected outcomes and interpretation** — What results would support or refute the hypothesis?
5. **Potential problems and alternatives** — What could go wrong, and what is the contingency?

Use subheadings tied to each specific aim so reviewers can map methods to goals.

## Rigor and Reproducibility

Most federal agencies now require explicit attention to rigor and reproducibility. NIH formalized this through its "Rigor and Reproducibility" policy; NSF and DOE expect comparable scientific soundness.

**Address these dimensions explicitly:**
- **Scientific premise**: The rigor of the prior research that justifies the proposal.
- **Experimental design**: Controls, randomization, blinding, and replication where applicable.
- **Biological variables**: For relevant research, consideration of sex as a biological variable and other relevant variables.
- **Authentication**: For key resources (cell lines, antibodies, reagents, datasets, software versions).
- **Statistical robustness**: Pre-specified analysis plans, power/sample-size justification, and correction for multiple comparisons.

Reviewers penalize proposals that treat reproducibility as an afterthought. Weave it into the design, not a closing paragraph.

## Methods by Research Type

### Experimental / Wet-Lab Research

- Describe the experimental design: independent and dependent variables, controls (positive, negative, vehicle), and replication (biological vs. technical replicates).
- Specify materials, reagents, model systems, and equipment; note sources and authentication.
- Detail data-collection protocols and the order of operations.
- State the statistical analysis plan and the sample size with a power calculation.
- Identify rigor measures: blinding, randomization, pre-registration where appropriate.

### Computational / Data-Intensive Research

- Describe algorithms, models, and software, including versions and dependencies.
- Specify datasets: provenance, size, splits (train/validation/test), and any preprocessing.
- State validation strategy: cross-validation, held-out test sets, baselines, and ablations.
- Report the computational resources required (compute, storage, runtime) to demonstrate feasibility.
- Address code and data availability, documentation, and reproducible environments (e.g., pinned dependencies, containers).
- Define benchmarking and performance metrics, and how results will be compared to prior work.

### Clinical / Translational Research

- Describe the study population, inclusion/exclusion criteria, and recruitment plan.
- Detail the intervention or treatment protocol and comparator/control.
- Define primary and secondary outcome measures and how they are assessed.
- Address regulatory approvals and timelines (IRB, and where relevant IND/IDE).
- Describe the clinical trial design (e.g., randomized controlled, crossover), monitoring, and stopping rules.
- Include a data and safety monitoring plan proportional to risk.

### Qualitative / Mixed-Methods Research

- Justify the qualitative approach (e.g., grounded theory, case study, ethnography) and its fit to the questions.
- Describe sampling strategy, data sources, and saturation criteria.
- Explain coding, analysis, and steps taken for trustworthiness (triangulation, member checking, inter-coder reliability).
- For mixed methods, specify how qualitative and quantitative strands integrate (sequential, concurrent, embedded).

## Statistical Analysis and Power

- State the hypotheses in testable form before describing tests.
- Justify the sample size with a power analysis grounded in expected effect sizes (cite preliminary data or literature; do not invent effect sizes).
- Pre-specify the primary analysis to avoid the appearance of fishing.
- Address missing data, multiple comparisons, and assumptions of the chosen tests.
- Where effect sizes are uncertain, say so and describe a sensitivity analysis rather than overclaiming precision.

## Anticipating Problems and Alternatives

Reviewers trust investigators who see around corners. For each aim:
- Identify the most likely failure mode.
- State an early indicator that would reveal the problem.
- Provide a concrete alternative approach that keeps the project on track.

This is not a confession of weakness — it demonstrates command of the science and de-risks the proposal.

## Common Methodological Mistakes

1. **Insufficient detail** to judge feasibility (reviewers assume the worst).
2. **No controls or inadequate controls** for the experimental design.
3. **Unjustified sample sizes** or absent power analysis.
4. **No analysis plan**, leaving statistical approach implied rather than stated.
5. **Ignoring reproducibility** (no authentication, no versioning, no pre-specification).
6. **No contingencies**, so any setback appears fatal to the project.
7. **Method-question mismatch**, where the chosen approach cannot actually answer the stated question.

## Checklist Before Finalizing

- [ ] Each aim maps to clearly described methods.
- [ ] Controls, replication, and randomization/blinding are specified where relevant.
- [ ] Sample size is justified with a power analysis or principled rationale.
- [ ] A pre-specified statistical or computational analysis plan is stated.
- [ ] Rigor and reproducibility are addressed within the design.
- [ ] Key resources are authenticated and versioned.
- [ ] Potential problems each have an alternative approach.
- [ ] Regulatory approvals (IRB/IACUC/IND/IDE) are addressed where applicable.

For agency-specific expectations on the approach section, see `nsf_guidelines.md`, `nih_guidelines.md`, `doe_guidelines.md`, `darpa_guidelines.md`, and `nstc_guidelines.md`.

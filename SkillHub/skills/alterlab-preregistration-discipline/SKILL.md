---
name: alterlab-preregistration-discipline
description: "Enforces pre-registration discipline with the Iron Law NO DATA ANALYSIS WITHOUT A PRE-REGISTERED ANALYSIS PLAN FIRST, a spirit-vs-letter line, an Excuse-vs-Reality rationalization table, and a Red-Flags-STOP list (HARKing, optional stopping, post-hoc covariates, outlier-dropping, test-shopping). Runs a PLAN/COLLECT/CONFIRM/EXPLORE workflow that freezes hypotheses, tests, exclusions, and stopping rules before data, then forces unplanned findings to be labeled exploratory (their p-values lose confirmatory status, per COS confirmatory/exploratory model). Orchestrates, not replaces, alterlab-open-science (OSF/AsPredicted registration), alterlab-statistical-analysis (test selection, assumptions), and alterlab-scientific-thinking (bias grading). Use when analyzing data without a frozen plan, switching the primary outcome or adding covariates after seeing results, weighing early stopping, dropping outliers post-hoc, pre-registering a study, or rationalizing deviation. Part of the AlterLab Academic Skills suite."
license: MIT
allowed-tools: Read Write Edit Bash(python:*)
compatibility: No API key required. Judgment/discipline skill; the optional helper runs locally via `uv run python` (stdlib only). Defers all registration mechanics and statistics to the sibling skills it orchestrates.
metadata:
  skill-author: AlterLab
  version: "1.0.0"
  last_updated: "2026-06-06"
  depends_on: "alterlab-open-science, alterlab-statistical-analysis, alterlab-scientific-thinking"
---

# Pre-registration Discipline (Iron Law)

**Skill type: DISCIPLINE-ENFORCING.** This is not a how-to and not a reference. It
exists to stop one specific failure mode — exploiting researcher degrees of freedom
after seeing the data, then reporting the result as if it were planned. It governs
*when you are allowed to claim a confirmatory result*; it does not teach you how to
pick a test or fill an OSF form. Those are sibling skills (see the routing table).

```
THE IRON LAW

    NO DATA ANALYSIS WITHOUT A PRE-REGISTERED ANALYSIS PLAN FIRST.
```

The frozen hypothesis + analysis plan is the research analog of a failing test
written before the implementation: you commit to what would count as a result
*before* you can see whether you got one. Run an unplanned analysis and the rule is
absolute — **it is exploratory. Label it, timestamp it, and you cannot report its
p-value as confirmatory.** (Per the Center for Open Science confirmatory/exploratory
model: in exploratory work, p-values lose their diagnostic value and findings require
independent replication. Verified at https://www.cos.io/initiatives/prereg.)

> **Violating the letter of the pre-registration is violating the spirit of the science.**

That line pre-empts the predictable defense — *"pre-registration is bureaucratic, I'm
following the scientific spirit."* There is no spirit-following exception. Iterate
freely in the EXPLORE phase; the confirmatory claim needs the frozen plan.

## When to Use This Skill

Use it the moment a confirmatory claim is on the table without a frozen plan behind
it, or the moment the plan is being bent after data are visible:

- About to analyze a dataset and there is no written, pre-data analysis plan.
- Switching the primary outcome, adding/removing a covariate, or changing the test
  *after* seeing results or p-values.
- Peeking at accruing data and weighing whether to stop now ("it's already significant").
- Dropping outliers, transforming variables, or changing exclusions that were not
  pre-specified.
- Drafting an OSF / AsPredicted / PROSPERO pre-registration (route the *mechanics* to
  `alterlab-open-science`; this skill enforces that the plan is actually *frozen* and
  honored).
- Rationalizing a deviation from an existing registration.
- A deadline-pressure ask like *"just p-hack this borderline result into something
  publishable."* — refuse the framing; offer the PLAN/CONFIRM/EXPLORE path instead.

### Does NOT Trigger

This skill is the *gatekeeper*, not the *toolbox*. It orchestrates siblings and routes
everything mechanical away. Route adjacent requests as follows:

| The request is really about… | Route to | Not this skill because… |
|---|---|---|
| Registration mechanics: OSF Registries / AsPredicted templates / PROSPERO, DMPs, FAIR data, repository choice, registered reports | `alterlab-open-science` | That skill owns the *how to register*; this one only enforces *freeze and honor it*. |
| Which test to run, assumption checks (Shapiro/Levene), power/sample-size, APA results | `alterlab-statistical-analysis` | Test *selection and execution* is statistics, not pre-registration discipline. |
| Grading evidence quality (GRADE, RoB), spotting biases/confounders, design validity | `alterlab-scientific-thinking` | Judging an *existing* body of evidence ≠ committing to a plan before data. |
| Whether a citation exists / supports a claim | `alterlab-citation-verifier` | Citation integrity, not analysis-plan integrity. |
| Reporting completeness of an analysis already run (effect sizes, CIs, every test disclosed) | `alterlab-results-transparency` | That is the *reporting* gate downstream of CONFIRM/EXPLORE. |
| Choosing among candidate tests for a borderline distribution before any peeking | `alterlab-test-selection-guard` | Locking the test choice is its own guard; this skill assumes the test is already in the frozen plan. |
| Writing a TÜBİTAK / grant proposal's methods section | `alterlab-tubitak-proposal` / `alterlab-grant-reporting` | Proposal authoring, not pre-registration enforcement. |
| Research ethics approval / KVKK / data-management compliance | `alterlab-tr-research-ethics` / `alterlab-kvkk-dmp` | Ethics & data governance, distinct from analysis-plan freezing. |

**REQUIRED BACKGROUND** (this skill orchestrates, it does not reimplement):
`alterlab-open-science` for the registration artifact, `alterlab-statistical-analysis`
for test choice + assumptions, `alterlab-scientific-thinking` for bias framing. When a
step needs any of those, hand off — do not restate their content here.

## The Workflow: PLAN → COLLECT → CONFIRM → EXPLORE

This is the research analog of red → green → refactor. Each phase has an exit gate; you
may not enter the next phase until the current gate passes.

### 1. PLAN — freeze it before any data are visible

Write down, and lock, **all** of:

1. The hypotheses (directional where applicable).
2. The primary outcome and any secondary outcomes — ranked.
3. The exact test(s) for each hypothesis (defer the *choice* to
   `alterlab-statistical-analysis`; record the decision here).
4. Inclusion/exclusion rules and the **outlier rule**, pre-specified.
5. The stopping rule / planned sample size (so optional stopping is off the table).
6. Covariates, transformations, and how missing data are handled.

Register the artifact via `alterlab-open-science` (OSF Registries / AsPredicted /
PROSPERO). **Gate:** the plan exists, is timestamped, and nothing in it depends on
having seen the outcome data. If you cannot answer "what result would falsify this?"
you are not done planning.

### 2. COLLECT — data, untouched

Collect according to the stopping rule. **Do not peek at the outcome to decide whether
to keep going.** If an interim look is genuinely needed, it had to be a pre-specified
sequential design (record that in PLAN). **Gate:** data collection matched the frozen
rule; no outcome-dependent stopping occurred.

### 3. CONFIRM — run exactly the planned tests

Run the pre-specified tests, in the pre-specified order, on the pre-specified sample.
Assumption checks (via `alterlab-statistical-analysis`) run and are reported **before**
interpreting the result — you do not get to swap the test because an assumption failed
unless the swap was pre-specified; an unplanned swap demotes the result to EXPLORE.
**Gate:** every confirmatory number traces to a line in the frozen plan.

### 4. EXPLORE — everything else, explicitly flagged

Anything not in the frozen plan lives here: new subgroups, post-hoc covariates,
alternative tests, interesting patterns. This work is valuable — it generates the
*next* study's hypotheses — but it is reported under an **Exploratory** heading, its
p-values are descriptive not confirmatory, and it carries a "requires replication"
caveat. **Gate:** every exploratory finding is labeled as such; none is laundered into
the confirmatory narrative.

A decision flowchart and the full phase gates live in
[references/workflow_gates.md](references/workflow_gates.md).

## Excuse vs. Reality

The predictable rationalizations, and what is actually happening. (Seeded from the
documented researcher-degrees-of-freedom literature — see
[references/researcher_degrees_of_freedom.md](references/researcher_degrees_of_freedom.md).)

| Excuse | Reality |
|---|---|
| "The data suggested a better test/model." | You are fitting noise. That is HARKing — hypothesizing after results are known. Report it as exploratory. |
| "We only peeked once." | Optional stopping inflates the Type I error rate. Report the (pre-specified) sequential design, or stop peeking. |
| "Pre-registration is rigid; science is iterative." | Iterate in the EXPLORE section. The confirmatory claim still needs the frozen plan. |
| "We dropped 3 outliers to meet normality." | Outlier rules must be pre-specified, or reported as a sensitivity analysis — not a silent edit. |
| "This covariate obviously belongs in the model." | "Obvious" post-hoc = a researcher degree of freedom. Pre-specify it, or flag it as exploratory. |
| "We switched to Mann–Whitney because the t-test wasn't significant." | Choosing a test by its p-value is test-shopping. Pre-register the decision rule or label the result exploratory. |
| "The deviation follows the spirit of the registration." | Violating the letter is violating the spirit. There is no spirit exception. |
| "It's only exploratory, so registration is overkill." | Then label every finding exploratory and claim no confirmatory p-values. You don't get confirmatory credit without the plan. |

## Red Flags — STOP

If you catch yourself (or the user) thinking any of these, **STOP**:

- "Let me just try a different test and see."
- "I'll drop these outliers and rerun."
- "The effect is there if I add this one covariate."
- "We can stop collecting now — it's already significant."
- "I'll just report the analyses that worked."
- "This subgroup is fascinating (we didn't predict it, but…)."
- "Let me change the primary outcome to the one that came out."
- "Pre-registration is overkill for a study like this."

All of these mean the same thing: **you are exploiting researcher degrees of freedom.**
Either return to the frozen plan, or label the work exploratory and forfeit the
confirmatory claim. There is no third option.

## The Multiple-Comparisons Escalation Gate

A hard, countable rule (the analog of "3 failed fixes = wrong architecture"):

> Ran **3+ tests on the same hypothesis** searching for significance? STOP. This is
> multiple comparisons / test-shopping. Either correct for **all** of them (Bonferroni /
> Benjamini–Hochberg FDR — via `alterlab-statistical-analysis`) or declare the whole
> analysis exploratory. Do **not** run test #4 to find p < .05.

## Deviation Disclosure Gate

If a deviation from the frozen plan is unavoidable (a genuine error in the plan, an
impossible assumption), it is not silently absorbed. Run, in order:

1. **STATE** the original frozen specification (quote the plan).
2. **STATE** the deviation and the concrete reason it was forced.
3. **CLASSIFY** the affected result as exploratory unless the deviation provably
   cannot have been outcome-driven.
4. **DISCLOSE** the deviation in the manuscript's transparency/deviations section
   (route reporting completeness to `alterlab-results-transparency`).

You can run a quick structured self-audit of a plan-vs-actual story with the optional
helper:

```bash
uv run python skills/methodology/alterlab-preregistration-discipline/scripts/prereg_check.py \
    --plan plan.json --actual actual.json
```

It is a stdlib-only checklist scorer (no network, no third-party APIs) — it does **not**
run statistics. See its `--help`.

## Self-Check Before Claiming a Confirmatory Result

- Does a frozen, timestamped plan exist, written before the outcome data were visible?
- Does every confirmatory number trace to a line in that plan?
- Were assumption checks run and reported before interpretation?
- Is every unplanned analysis under an **Exploratory** heading with a replication caveat?
- Are all deviations disclosed, not absorbed?

Any "no" → the result is exploratory, not confirmatory. Say so plainly.

## References

- [references/workflow_gates.md](references/workflow_gates.md) — the PLAN/COLLECT/CONFIRM/EXPLORE
  phase gates and decision flowchart in full.
- [references/researcher_degrees_of_freedom.md](references/researcher_degrees_of_freedom.md) —
  the documented failure modes (HARKing, optional stopping, p-hacking, the garden of
  forking paths) this skill is built to catch, with sources.
- Center for Open Science — Preregistration. https://www.cos.io/initiatives/prereg
  (confirmatory vs. exploratory model; verified during authoring).
- Orchestrated siblings: `alterlab-open-science`, `alterlab-statistical-analysis`,
  `alterlab-scientific-thinking`.

Part of the AlterLab Academic Skills suite.

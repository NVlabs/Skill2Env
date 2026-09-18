---
name: alterlab-results-transparency
description: Enforces results-reporting transparency as a discipline gate built on the Iron Law "NO RESULTS CLAIM WITHOUT REPORTING EVERY ANALYSIS RUN" — a numbered Gate Function (IDENTIFY the claim, LIST every test actually run including the ones that did not "work", CHECK assumptions were reported, CHECK effect size with 95% CI is present, CHECK pre-registration deviations are disclosed, ONLY THEN write the sentence), plus an Excuse-vs-Reality table and Red-Flags-STOP list for selective reporting, cherry-picking, and bare p-values. Use when writing up Results, claiming a finding from a subset of analyses, reporting a p-value without an effect size or confidence interval, dropping outliers post hoc, or omitting analyses that did not pan out. Orchestrates alterlab-statistical-analysis (tests, effect sizes), alterlab-preregistration-discipline (the frozen plan), and alterlab-open-science (TOP, disclosure); it does not run the tests itself. Part of the AlterLab Academic Skills suite.
license: MIT
allowed-tools: Read Bash(python:*)
compatibility: No API key required. Judgment/discipline skill; the optional reporting-gate helper runs locally via `uv run python` (stdlib only).
metadata:
  skill-author: AlterLab
  version: "1.0.0"
---

# Results Transparency — The Reporting Discipline Gate

**Skill type: DISCIPLINE-ENFORCING.** This skill is not a how-to for running
statistics. It is a gate that stands between *analyses you ran* and the
*sentence you are about to write* in the Results section. It exists to stop the
single most common integrity failure in quantitative write-ups: reporting the
analyses that "worked" and quietly dropping the rest.

It **orchestrates**, it does not reimplement:

- **REQUIRED BACKGROUND — `alterlab-statistical-analysis`** runs the tests,
  checks assumptions (its `alterlab-statistical-analysis/scripts/assumption_checks.py`),
  computes effect sizes and CIs, and produces the APA-formatted numbers. This
  skill checks that those outputs are all *present and disclosed* before a claim
  is written.
- **REQUIRED BACKGROUND — `alterlab-preregistration-discipline`** owns the
  frozen plan. This skill checks that confirmatory claims match it and that
  deviations are labelled.
- **`alterlab-open-science`** owns the disclosure mechanics (TOP Guidelines,
  registration links, data/code availability).
- **`alterlab-scientific-thinking`** owns judging evidence *quality*; this skill
  only enforces reporting *completeness*.

---

## The Iron Law

```
NO RESULTS CLAIM WITHOUT REPORTING EVERY ANALYSIS RUN
```

Violating the letter of full reporting is violating the spirit of the science.
"Reporting every analysis" means every test you actually executed against the
data for this hypothesis — including the ones that returned p > .05, the
specification you abandoned, and the outlier rule you tried first. A Results
section is a census of what you did, not a highlight reel of what confirmed you.

---

## When to Use This Skill

Invoke it the moment a results *claim* is being written or defended:

- About to write a sentence in the Results / Findings section.
- Stating "we found that…", "X significantly predicted Y", "there was no effect".
- Reporting a p-value, a coefficient, a group difference, or a correlation.
- Defending a finding drawn from a subset of the analyses that were run.
- Tempted to drop outliers, switch a test, or add a covariate *after* seeing the result.
- Writing the abstract's results sentence or a figure caption that asserts a finding.

If you are *choosing* which test to run, *checking assumptions*, or *computing*
an effect size, that is `alterlab-statistical-analysis` — come back here when you
move from computing numbers to claiming findings.

### Does NOT Trigger — route these elsewhere

| The request is really about… | Route to |
|------------------------------|----------|
| Choosing/running a test, assumption checks, computing effect size or CI | `alterlab-statistical-analysis` |
| Whether the analysis plan was frozen before data; HARKing / optional stopping | `alterlab-preregistration-discipline` |
| Picking the right test *before* seeing the p-value (test-shopping guard) | `alterlab-test-selection-guard` |
| Where/how to disclose: TOP Guidelines, registration link, data/code availability | `alterlab-open-science` |
| Judging evidence *quality* (GRADE, risk of bias, confounding, design validity) | `alterlab-scientific-thinking` |
| Verifying cited references exist / are not fabricated | `alterlab-citation-verifier` |
| Section-by-section peer review and an accept/revise/reject verdict | `alterlab-paper-reviewer` |
| Drafting the full IMRaD manuscript from a finished synthesis | `alterlab-paper-writer` |
| Writing the grant's final/technical report narrative | `alterlab-grant-reporting` |

---

## The Gate Function

Before any results claim is written, run these steps in order. This mirrors the
`verification-before-completion` gate (obra/superpowers): evidence before
assertions, always.

1. **IDENTIFY** — State the exact claim sentence you intend to write.
2. **LIST** — Enumerate *every* test actually run against this hypothesis,
   including the ones that did not "work" (p > .05, abandoned specs, alternative
   exclusion rules). If the list has more entries than the write-up mentions,
   STOP — the gap is selective reporting.
3. **CHECK assumptions reported** — For each reported test, the assumption
   results from `alterlab-statistical-analysis/scripts/assumption_checks.py`
   (normality, homogeneity, linearity, outliers) must appear in the write-up, with
   the remediation taken if any were violated.
4. **CHECK effect size + CI present** — The claim carries an effect size *with a
   95% confidence interval*, not a bare p-value. A p-value alone never clears the
   gate (see the sufficiency table).
5. **CHECK pre-registration deviations disclosed** — Every difference from the
   frozen plan (`alterlab-preregistration-discipline`) is named and labelled
   confirmatory vs. exploratory.
6. **ONLY THEN** — Write the sentence, with the test name, statistic, df, *exact*
   p, effect size + CI, and the confirmatory/exploratory label.

A self-contained checker that enforces steps 2–5 over a small JSON manifest of
the claim is `scripts/reporting_gate.py` (stdlib only; see Quick Start).

### What is sufficient vs. not sufficient

Analogous to the verification-gap table: the left column does **not** clear the
gate; the right column is the actual requirement.

| Looks done (NOT sufficient) | Actual requirement to clear the gate |
|-----------------------------|--------------------------------------|
| "p < .05" | Test name, statistic, **df**, **exact p**, effect size **+ 95% CI** |
| "the effect was significant" | The direction, magnitude (effect size + CI), and the n it rests on |
| Only the significant tests shown | Every test run on this hypothesis, significant or not |
| "assumptions were fine" | The reported normality / homogeneity / linearity / outlier results |
| Results match the paper's story | Results match the **frozen plan**, with deviations labelled exploratory |
| "we removed outliers" | The pre-specified rule, or a sensitivity analysis with and without them |

---

## Excuse vs. Reality

Seeded from the rationalizations that precede selective reporting. When you hear
yourself think the left column, the right column is the truth.

| Excuse | Reality |
|--------|---------|
| "I'll just report the analyses that worked." | The ones that did not work are data. Omitting them is selective reporting — report all planned analyses, significant or not. |
| "It's only a p-value, the effect size is obvious." | A bare p-value is not interpretable. Effect size + 95% CI is mandatory; existence is not magnitude. |
| "We dropped 3 outliers so the test would pass." | Outlier rules must be pre-specified or reported as a sensitivity analysis — not chosen because they flip significance. |
| "The covariate obviously belongs in the model." | A covariate added after seeing the result is a researcher degree of freedom. Pre-specify it or label the model exploratory. |
| "We switched to a non-parametric test, it's more appropriate." | If you switched *after* the parametric test was non-significant, that is test-shopping. Decide before, via `alterlab-test-selection-guard`. |
| "This subgroup is interesting (we didn't predict it)." | Unplanned subgroups are exploratory. Report them as hypothesis-generating, never as confirmatory. |
| "Reporting the failed analyses will confuse readers." | A supplementary table of all analyses run is standard transparency (TOP). Clarity is not a license to hide. |
| "The pre-registration was too rigid; I'm following the scientific spirit." | Iterate in the exploratory section. The confirmatory claim needs the frozen plan. |

---

## Red Flags — STOP

If you catch yourself thinking any of these, STOP. You are about to exploit a
researcher degree of freedom. Either report it in full or label it exploratory.

- "Let me just report the analyses that worked."
- "I'll drop these outliers and rerun before writing it up."
- "The effect is there if I add this one covariate."
- "Let me try a different test — this one isn't quite significant."
- "We can leave the non-significant models out of the Results."
- "This subgroup is interesting, I'll write it as a finding."
- "Close enough to p < .05 — I'll call it a trend and move on."
- "No need to mention we changed the primary outcome."
- "I'll round the p-value down and skip the effect size for now."

**All of these mean: STOP. Run the Gate Function. Report everything, or label it
exploratory.**

---

## Escalation Gate (multiple comparisons / test-shopping)

Mirrors the systematic-debugging "3 failures = wrong approach" rule:

> Ran **3+ tests on the same hypothesis** searching for significance? STOP. This
> is multiple comparisons / test-shopping. Either correct for *all* of them
> (Bonferroni / FDR — via `alterlab-statistical-analysis`) or declare the
> analysis exploratory. Do **not** run test #4 to find p < .05.

---

## Quick Start

```bash
# 1. Build a tiny manifest of the claim and what was actually run (see references).
# 2. Run the gate; non-zero exit = claim is not clear to write.
uv run python skills/methodology/alterlab-results-transparency/scripts/reporting_gate.py claim.json
```

The script is a deterministic transparency linter, not a statistics engine: it
checks that the manifest lists all runs, that an effect size + CI accompany every
reported claim, that assumption results are present, and that deviations are
labelled. It never computes a p-value or an effect size — that is
`alterlab-statistical-analysis`'s job.

---

## Deeper Detail

- `references/gate_function.md` — the full gate walkthrough, the claim-manifest
  schema, and a worked pass/fail example.
- `references/transparency_standards.md` — what a complete Results report
  contains (CONSORT/STROBE results items, TOP Guidelines reporting standards,
  APA results requirements) and how this skill maps onto sibling skills.

## Self-Check Before Reporting

- Did you LIST every test run, or only the ones in the draft?
- Does every claim carry an effect size **+ 95% CI**, not a bare p-value?
- Are the assumption-check results from `alterlab-statistical-analysis` reported?
- Is every deviation from the frozen plan labelled confirmatory vs. exploratory?
- Ran 3+ tests on one hypothesis? Corrected, or declared exploratory?

Part of the AlterLab Academic Skills suite.

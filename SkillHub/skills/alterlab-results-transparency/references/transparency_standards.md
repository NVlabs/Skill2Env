# Transparency Standards & Skill Boundaries

What a *complete* Results report contains, which established reporting standard
each requirement comes from, and exactly where this discipline skill stops and a
sibling skill takes over.

---

## A complete results report (the checklist this gate enforces)

For every reported quantitative claim:

1. **Descriptive statistics** — M, SD, and n for each group/condition.
2. **The test** — its name, the statistic, the **degrees of freedom**, and the
   **exact p-value** (not "p < .05").
3. **Effect size + 95% confidence interval** — magnitude, not just existence.
4. **Assumption results** — the normality / homogeneity / linearity / outlier
   checks that were run, and any remediation taken when violated.
5. **All analyses run** — every test executed on the hypothesis, significant or
   not, including abandoned specifications and alternative exclusion rules.
6. **Confirmatory vs. exploratory label** — claims tied to the frozen plan are
   confirmatory; anything else is exploratory and labelled as such.
7. **Deviations disclosed** — every difference from the pre-registered plan named.

Items 1–4 are the substance produced by `alterlab-statistical-analysis`
(it lists exactly these reporting elements: descriptives, test statistic + df +
exact p, effect sizes with CIs, assumption checks, and all planned analyses).
Items 5–7 are the transparency discipline this skill adds on top.

## Where the requirements come from

These are recognised reporting standards, named here as the relevant standard —
the disclosure *mechanics* (links, statements, where to file) are owned by
`alterlab-open-science`, not by this skill:

- **TOP Guidelines** (Transparency and Openness Promotion) — journal-level
  standards for reporting standards, analytic transparency, and disclosure of all
  analyses. `alterlab-open-science` covers TOP adoption and disclosure routes.
- **CONSORT** — the reporting standard for randomized controlled trials; its
  Results items require reporting outcomes and estimation (effect size + precision)
  for *each* primary and secondary outcome, and all harms/unintended effects.
- **STROBE** — the reporting standard for observational studies; its Results items
  require reporting numbers analysed, unadjusted and adjusted estimates with their
  precision, and the analyses actually performed.
- **APA results reporting** — exact statistics, effect sizes with CIs, and full
  reporting of analyses; the APA mechanics are owned by
  `alterlab-statistical-analysis` (`references/reporting_standards.md`).

This skill does not re-teach any of these standards in depth — it enforces the
one cross-cutting rule they all share: **report everything you ran, with magnitude
and uncertainty, and disclose deviations.**

---

## Skill boundary map

| Concern | Owner skill | This skill's role |
|---------|-------------|-------------------|
| Choosing a test, checking assumptions, computing effect size + CI, APA numbers | `alterlab-statistical-analysis` | Requires the outputs are present and disclosed |
| The frozen hypothesis + analysis plan; HARKing, optional stopping | `alterlab-preregistration-discipline` | Requires confirmatory claims match it; deviations labelled |
| Choosing the test *before* seeing the p-value (anti test-shopping) | `alterlab-test-selection-guard` | Flags post-hoc test switches in the LIST step |
| Disclosure mechanics: TOP, registration links, data/code availability | `alterlab-open-science` | Points to it; does not implement disclosure |
| Judging evidence quality (GRADE, risk of bias, confounding) | `alterlab-scientific-thinking` | Out of scope — completeness ≠ quality |
| Verifying references exist / are not fabricated | `alterlab-citation-verifier` | Out of scope |
| Manuscript drafting / peer review | `alterlab-paper-writer` / `alterlab-paper-reviewer` | Out of scope |

## Why this is a discipline skill, not a technique

Per the superpowers skill taxonomy, only rules that are *judgment calls under
pressure* warrant an Iron Law, an Excuse-vs-Reality table, and a Red-Flags list.
Selective reporting is exactly that: every step is individually defensible
("this test is more appropriate", "these outliers are unusual"), and the failure
only appears in aggregate. The mechanical parts — computing the statistics,
checking assumptions — are *techniques* and live in
`alterlab-statistical-analysis`. Bolting Iron Laws onto mechanical content would
dilute the force of the real law, so this skill deliberately delegates them.

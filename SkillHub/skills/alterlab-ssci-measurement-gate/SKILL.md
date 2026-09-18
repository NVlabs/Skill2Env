---
name: alterlab-ssci-measurement-gate
description: "Gates measurement quality before a scale or instrument is trusted — checks that each construct is defined and operationalized, that reliability is evidenced with McDonald omega (not Cronbach alpha alone, which assumes tau-equivalence and is only a lower bound), that reliability is not confused with validity (content, criterion, convergent/discriminant construct validity), and that measurement invariance is tested before comparing groups. Use when asking whether a scale or survey instrument is valid, reporting a Cronbach alpha, building or adopting a multi-item measure, or comparing a latent construct across groups. For designing the questionnaire items prefer alterlab-survey-design; for running the confirmatory factor analysis prefer alterlab-sem-psychometrics; to execute basic statistics prefer alterlab-statistical-analysis. Part of the AlterLab Academic Skills suite."
license: MIT
allowed-tools: Read Bash(python:*)
compatibility: No API key required. A discipline-enforcing measurement-quality skill; reliability/CFA execution is handed to sibling skills that run locally via `uv run python`.
metadata:
    skill-author: AlterLab
    version: "1.0.0"
    depends_on: "alterlab-survey-design (item design), alterlab-sem-psychometrics (CFA/invariance), alterlab-statistical-analysis"
---

# Measurement Gate — Reliability Is Not Validity

**Skill type: DISCIPLINE-ENFORCING.** Before any hypothesis test consumes a scale, this gate
checks that the scale measures what it claims, reliably, and comparably across groups. It does
not fit factor models itself — it *requires* the right evidence and routes execution to the
psychometrics skill.

## The Core Rule

```
A RELIABLE MEASURE OF THE WRONG CONSTRUCT IS STILL WRONG. RELIABILITY ≠ VALIDITY.
```

High internal consistency only means the items move together; it says nothing about whether
they capture the intended construct. Evidence for *validity* (content, criterion, construct) is
separate and mandatory. And the usual reliability number — Cronbach alpha — rests on an
assumption (tau-equivalence: equal item loadings) that real scales rarely meet, so alpha is a
**lower bound** that can under- or (with correlated errors) over-state reliability.

## When to Use This Skill

- "Is my scale / survey instrument valid?"
- "My Cronbach alpha is 0.78 — is the scale good to use?" (← alpha alone is not enough)
- "I built a new 6-item measure of burnout; how do I show it works?"
- "I want to compare a latent trait (e.g. trust) across countries/groups."

### Does NOT Trigger

| The request is really about… | Route to | Why not this skill |
|---|---|---|
| Writing / wording the questionnaire items, response scales | `alterlab-survey-design` | Instrument construction, upstream of validation. |
| Running the CFA / SEM / IRT / invariance model | `alterlab-sem-psychometrics` | This gate requires CFA; that skill fits it. |
| Basic descriptive/inferential stats execution | `alterlab-statistical-analysis` | Computation, not measurement discipline. |
| Which statistical test to run on a measured outcome | `alterlab-test-selection-guard` | Test choice, not measurement quality. |
| Sampling frame / how many respondents | `alterlab-ssci-sampling-gate` | Sampling, not measurement. |

## Reliability: report alpha AND omega

Cronbach's alpha assumes **tau-equivalence** (all items load equally on one factor) and is a
**lower bound** on reliability under that model. **McDonald's omega** relaxes tau-equivalence by
weighting items by their factor loadings and should be reported alongside alpha (McNeish, 2018,
*Psychological Methods*, "Thanks coefficient alpha, we'll take it from here"). In practice the
alpha-vs-omega gap for well-constructed unidimensional scales is often small (Warne, 2025 —
around 4.5% underestimate), so the discipline is: **report both**, plus item-total correlations
and a dimensionality check — not to fetishize a single number, but to show the estimate is not
resting on an unexamined assumption.

Rules this gate enforces:

1. **Alpha alone is insufficient.** Ask for omega; if only alpha is available, state the
   tau-equivalence caveat explicitly.
2. **Reliability presupposes dimensionality.** A high alpha on a multidimensional set is
   meaningless — check the factor structure (CFA, `alterlab-sem-psychometrics`) first.
3. **Item diagnostics.** Item-total correlations and (for two halves) Spearman-Brown; drop or
   revise items that do not cohere — but pre-specify such decisions, do not fish.

## Validity: four kinds, none optional

| Validity | Question | Evidence |
|----------|----------|----------|
| **Content** | Do items cover the construct's domain? | expert review, blueprint against the definition |
| **Criterion** | Does it predict/correlate with a gold standard? | concurrent & predictive correlations |
| **Convergent** | Does it correlate with related measures? | AVE, correlations with kindred scales |
| **Discriminant** | Is it distinct from other constructs? | heterotrait-monotrait ratio, cross-loadings |

Construct validity is established with a **confirmatory factor analysis** — route the fit to
`alterlab-sem-psychometrics` (CFI/TLI, RMSEA, SRMR against Hu & Bentler cutoffs).

## Measurement invariance before group comparison

Comparing a latent construct across groups (countries, waves, conditions) is only valid if the
measure means the same thing in each group. Require a **multi-group CFA invariance** sequence —
configural → metric → scalar — before interpreting group differences in means. Without at least
metric/scalar invariance, a "difference" may be a measurement artifact, not a real effect.
Route the test to `alterlab-sem-psychometrics`.

## The Design Passport (hand-off)

Append to each construct in the Passport: `reliability` (alpha + omega + caveat),
`validity_evidence` (which of the four kinds are shown), `dimensionality` (CFA fit), and
`invariance` (level established) before any group comparison downstream.

## Self-Check Before Advancing

- Is each construct explicitly defined and operationalized to its items?
- Is reliability shown with omega (or alpha with the tau-equivalence caveat stated)?
- Is at least one form of validity evidence present — not just reliability?
- Was dimensionality confirmed (CFA) before trusting a single reliability coefficient?
- Is measurement invariance established before comparing the construct across groups?

## References

- `references/reliability_and_validity.md` — alpha vs omega math, the four validities, the
  invariance sequence, and reporting templates. Loaded on demand.

Part of the AlterLab Academic Skills suite.

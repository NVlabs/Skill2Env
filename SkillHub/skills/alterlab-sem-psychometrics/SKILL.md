---
name: alterlab-sem-psychometrics
description: "Fits and evaluates measurement models — confirmatory factor analysis, full structural equation models, exploratory factor analysis, item response theory, and multi-group measurement invariance — using the verified Python stack: semopy (model syntax =~ / ~ / ~~, Model.fit, inspect(std_est=True), calc_stats for CFI/TLI/RMSEA), factor_analyzer (EFA, KMO, Bartlett, ConfirmatoryFactorAnalyzer), and pingouin/girth, computing McDonald's omega from standardized loadings and judging fit against Hu & Bentler cutoffs. Use when the request mentions confirmatory factor analysis, structural equation modeling, a latent variable or construct model, factor loadings, IRT, or measurement invariance across groups. For deciding whether a scale is trustworthy at all prefer alterlab-ssci-measurement-gate; for plain regression prefer alterlab-statistical-analysis. Part of the AlterLab Academic Skills suite."
license: MIT
allowed-tools: Read Bash(python:*)
compatibility: "Requires (declare in-session, no runtime install on Anthropic API): semopy>=2.3, factor_analyzer>=0.5, pingouin>=0.5, optionally girth (IRT) (pip). SRMR and omega are not returned by semopy — compute omega with the bundled script; IRT beyond 2PL is often better in R mirt. Runs locally via `uv run python`; no API key."
metadata:
    skill-author: AlterLab
    version: "1.0.0"
    depends_on: "alterlab-ssci-measurement-gate (gates whether to trust the scale), alterlab-statistical-analysis; audited by alterlab-ssci-inference-gate"
---

# SEM & Psychometrics — Fit the Measurement Model, Judge It Honestly

**Skill type: ANALYSIS MODULE.** Fits CFA / SEM / EFA / IRT and tests measurement invariance.
The discipline: report fit against real cutoffs, report reliability with **omega** (not alpha
alone), and establish invariance before comparing groups. Whether the scale should be trusted at
all is the upstream call of `alterlab-ssci-measurement-gate`.

## Core Mission

```
A MEASUREMENT MODEL IS ONLY DONE WHEN FIT, RELIABILITY (OMEGA), AND INVARIANCE ARE ALL REPORTED.
```

## When to Use This Skill

- "Run a confirmatory factor analysis on my scale."
- "Fit a structural equation model / a latent-variable path model."
- "Do an exploratory factor analysis — how many factors?"
- "Fit an IRT model / get item difficulty and discrimination."
- "Test measurement invariance across countries before I compare latent means."

### Does NOT Trigger

| The request is really about… | Route to | Why not this skill |
|---|---|---|
| Whether the scale is valid/trustworthy at all (reliability≠validity discipline) | `alterlab-ssci-measurement-gate` | Gate decision, upstream of fitting. |
| Writing / wording the questionnaire items | `alterlab-survey-design` | Instrument construction. |
| Plain regression / descriptive stats | `alterlab-statistical-analysis` | No latent structure. |
| A causal treatment-effect estimate | `alterlab-causal-inference` | Different problem. |

## Verified calls (pinned)

**CFA / SEM — semopy (v2.3):**

```python
from semopy import Model, calc_stats
desc = """
# measurement model
Trust =~ q1 + q2 + q3
Efficacy =~ q4 + q5 + q6
# structural path
Trust ~ Efficacy
"""
m = Model(desc); m.fit(data)          # obj='MLW' default; 'FIML' for missing
est = m.inspect(std_est=True)          # standardized loadings for omega
stats = calc_stats(m)                  # DataFrame: chi2, CFI, TLI, RMSEA, AIC, BIC ...
```

Note: `calc_stats` returns CFI/TLI/RMSEA but **not SRMR** — report the indices it gives and
compute SRMR separately if required.

**EFA — factor_analyzer (v0.5):**

```python
from factor_analyzer import FactorAnalyzer, calculate_kmo, calculate_bartlett_sphericity
kmo_all, kmo_model = calculate_kmo(X)          # sampling adequacy > .60
chi2, p = calculate_bartlett_sphericity(X)      # sphericity
fa = FactorAnalyzer(n_factors=3, rotation="promax"); fa.fit(X)
fa.loadings_; fa.get_factor_variance()          # (variance, proportional, cumulative)
```

`ConfirmatoryFactorAnalyzer` + `ModelSpecificationParser.parse_model_specification_from_dict`
give a CFA alternative when semopy is unavailable.

**Reliability — omega (not alpha alone):** pingouin gives `cronbach_alpha` but **no omega**, and
semopy does not return omega. Compute McDonald's omega from the standardized loadings with
`scripts/omega.py` (ω = (Σλ)² / [(Σλ)² + Σ(1−λ²)]). Report alpha + omega together.

**IRT:** `girth` (`twopl_mml`, `rasch_mml`) for dichotomous 2PL/Rasch; `py-irt` for Bayesian/
scalable. For polytomous/multidimensional IRT with full fit statistics, R `mirt` is the practical
standard — say so rather than forcing a thin Python path.

## Fit cutoffs (Hu & Bentler 1999, as guidelines not gates)

CFI/TLI ≥ .95 · RMSEA ≤ .06 · SRMR ≤ .08. Use a two-index combination; do not chase a single
number. Report the χ² and df alongside (χ² is sample-size sensitive, so not decisive).

## Measurement invariance (before any group comparison)

Multi-group CFA sequence — **configural → metric → scalar → strict** — judged by ΔCFI ≤ .01 /
ΔRMSEA ≤ .015, not only Δχ². Scalar invariance is the prerequisite for comparing **latent means**;
without it a group "difference" may be a measurement artifact. Fit each nested model and compare.

## Output Template

```
MODEL:        <CFA/SEM/EFA/IRT + the semopy/factor_analyzer spec>
FIT:          CFI= TLI= RMSEA= (chi2/df=)   vs Hu & Bentler cutoffs
RELIABILITY:  omega= (alpha= )              per factor, from standardized loadings
VALIDITY:     <AVE, HTMT if convergent/discriminant claimed>
INVARIANCE:   <configural|metric|scalar|strict established; ΔCFI reported>
```

## References

- `references/fit_and_invariance.md` — omega math, fit-index nuance, the invariance sequence, IRT notes.
- `scripts/omega.py` — stdlib McDonald's omega from standardized loadings.

Part of the AlterLab Academic Skills suite.

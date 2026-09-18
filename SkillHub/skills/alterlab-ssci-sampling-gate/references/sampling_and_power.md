# Sampling and Power — Full Reference

Loaded on demand from the sampling-gate SKILL.md. Covers the three sizing logics, probability
vs non-probability methods, design effects, finite-population correction, and reporting templates.

## Three sizing logics in detail

### 1. A-priori power analysis (for hypothesis tests)

Power is the probability of detecting an effect of a given size if it is real:
`power = 1 − β`. Fix three of {effect size, α, power, N} and solve for the fourth. For planning,
fix α (usually .05), power (usually .80 or .90) and the **smallest effect size of interest**
(SESOI), then solve for N.

Two-group mean comparison (Cohen's *d*, equal groups), normal approximation:

```
n_per_group ≈ 2 · (z_{1−α/2} + z_{1−β})² / d²
```

Two-proportion comparison:

```
n_per_group ≈ (z_{1−α/2} + z_{1−β})² · [p1(1−p1) + p2(1−p2)] / (p1 − p2)²
```

The critical discipline is the **effect size you power on**. Powering on the effect observed in
a small pilot systematically underpowers the confirmatory study, because small pilots
over-estimate effects (winner's curse). Use the smallest effect that would be *theoretically or
practically meaningful*, or a conservative literature meta-estimate — not the pilot point
estimate.

**Post-hoc / "observed" power is not evidence.** Once you have the p-value, observed power is a
one-to-one transform of it and adds nothing; a non-significant result does not become
interpretable by reporting that its observed power was low. Report a confidence interval instead.

### 2. Precision / margin of error (for estimation)

When the goal is to *estimate* a quantity (a mean, a proportion) rather than test a hypothesis,
size for a target **half-width** (margin of error) `E` at confidence `1−α`.

Proportion:

```
n ≈ z_{1−α/2}² · p(1−p) / E²        (use p = 0.5 for the conservative maximum)
```

Mean:

```
n ≈ z_{1−α/2}² · σ² / E²
```

Report the margin of error you designed for, not just N.

### 3. Saturation / information power (for qualitative studies)

Sample size is argued, not calculated. **Information power** (Malterud et al., 2016) rises — so
the needed N falls — when the study aim is narrow, the sample is highly specific to the topic,
established theory supports the analysis, the dialogue is strong, and the analysis is a
case-focused in-depth strategy rather than cross-case. **Saturation** is the point at which new
data stop yielding new codes/themes/theoretical properties. Neither is a fixed number; a study
that reports "N=12 because that is standard" has substituted a citation for an argument. Route the
depth mechanics (coding, constant comparison, theoretical sampling) to
`alterlab-qualitative-methods`.

## Probability vs non-probability methods

| Method | Type | Selection mechanism | Generalization |
|--------|------|---------------------|----------------|
| Simple random (SRS) | probability | every unit equal known probability | statistical |
| Stratified | probability | random within strata; can improve precision | statistical |
| Systematic | probability | every k-th unit from a random start (beware periodicity) | statistical |
| Cluster / multistage | probability | sample clusters, then units within | statistical (with design effect) |
| Quota | non-probability | fill demographic quotas by availability | analytical only |
| Convenience | non-probability | whoever is reachable | analytical only |
| Snowball | non-probability | referrals from participants (hidden populations) | analytical only |
| Purposive / theoretical | non-probability | chosen to inform theory (qual) | analytical/theoretical |

Only probability methods license a sampling-error statement (standard errors, CIs, margins of
error) about the population. Attaching a "±3% margin of error" to a convenience or opt-in sample
is a category error.

## Design effect and effective sample size

Cluster and stratified samples do not behave like an SRS of the same size. The **design effect**
`DEFF = 1 + (m̄ − 1)·ICC` (for clusters of average size `m̄` and intraclass correlation `ICC`)
inflates the variance; the **effective sample size** is `n_eff = n / DEFF`. Power and precision
formulas above assume SRS — divide by DEFF (or multiply N by DEFF) for clustered designs.

## Finite-population correction

When the sample is a large fraction of a finite population `N_pop`, multiply the required n by the
FPC: `n_adj = n / (1 + (n − 1)/N_pop)`. Negligible when the population is large relative to n.

## Non-response and attrition

A frame that perfectly covers the population still yields a biased sample if non-response is
selective. Report the response rate; compare respondents vs non-respondents on known frame
variables; consider non-response weighting or inverse-probability weighting. In longitudinal
designs, model attrition and test whether it is related to the outcome (informative dropout).

## Reporting template (paste into the Design Passport)

```yaml
sampling:
  target_population: <who the claim is about>
  sampling_frame: <the list actually drawn from>
  coverage_gap: <who the frame omits or over-represents>
  method: <SRS | stratified | cluster | systematic | quota | convenience | snowball | purposive>
  type: <probability | non-probability>
  size_logic: <power | precision | saturation>
  size_inputs: <effect size, alpha, power  |  margin, confidence, variance  |  saturation argument>
  n_planned: <number, or "governed by saturation">
  design_effect: <DEFF if clustered/stratified, else 1>
  expected_nonresponse: <rate + mitigation>
  generalization: <statistical | analytical>
```

## References

- Malterud, K., Siersma, V. D., & Guassora, A. D. (2016). Sample size in qualitative interview
  studies: guided by information power. *Qualitative Health Research*.
- Cohen, J. (1988). *Statistical Power Analysis for the Behavioral Sciences.*
- Lohr, S. L. (2019). *Sampling: Design and Analysis.*
- Hoenig, J. M., & Heisey, D. M. (2001). The abuse of power: the pervasive fallacy of power
  calculations for data analysis. *The American Statistician.*

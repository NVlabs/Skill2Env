# When a Reliability Coefficient Applies — and When It Does Not

Loaded on demand from the qualitative-analysis SKILL.md. The single most important judgment in
qualitative reliability is *whether a coefficient is even the right tool*. It depends on the
analytic tradition.

## Two traditions, two criteria

### Codebook / content-analytic coding → coefficient
The design treats coding as (approximately) replicable classification into a fixed scheme. Multiple
coders should converge; disagreement signals an ambiguous codebook or under-trained coders. Here a
chance-corrected agreement coefficient (Krippendorff's α) is meaningful and expected. This includes
**quantitative content analysis**, **framework analysis** with a set matrix, and **codebook thematic
analysis** where reliability is claimed.

Report: α + CI + threshold, coders, % double-coded, resolution process.

### Reflexive thematic analysis (Braun & Clarke) → consensus + reflexivity
The design treats the researcher as the analytic instrument; themes are *generated*, not *found*,
and coder subjectivity is a resource, not error to be averaged out. In this tradition an ICR
coefficient is epistemologically mismatched: the goal is not that two coders independently produce
the same codes, but that the analysis is a rich, reflexively-examined interpretation. Braun & Clarke
explicitly caution against ICR statistics for reflexive TA.

Here the "reliability" work is: **collaborative discussion** among analysts to understand and use
differences, an audit trail, and reflexivity (see `alterlab-ssci-reflexivity-gate`). Reporting a
kappa here would misrepresent the method.

## The decision

```
Is coding a replicable classification into a fixed codebook, with agreement a quality signal?
  ├─ YES → compute Krippendorff's alpha (+ CI, threshold); report the ICR checklist.
  └─ NO (reflexive/interpretive TA) → consensus + reflexivity + audit trail; NO coefficient required.
        route trustworthiness to alterlab-ssci-reflexivity-gate.
Mixed / framework analysis → a coefficient on the structured-coding portion is defensible; say so.
```

## Why this matters

Overselling a coefficient on reflexive work invites a reviewer to reject the epistemology; omitting
one on content-analytic work invites a reviewer to reject the rigor. Matching the criterion to the
tradition is the methodologically correct — and defensible — behavior. State the branch explicitly
in the methods section so readers know which standard you are being held to.

## References

- Braun, V., & Clarke, V. (2021). *Thematic Analysis: A Practical Guide.*
- O'Connor, C., & Joffe, H. (2020). Intercoder reliability in qualitative research: debates and practical guidelines.
- Guest, MacQueen & Namey (2012). *Applied Thematic Analysis* (codebook tradition).

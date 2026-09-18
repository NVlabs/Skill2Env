---
name: alterlab-qca
description: "Runs Qualitative Comparative Analysis — crisp-set (csQCA), multi-value (mvQCA), and fuzzy-set (fsQCA) — for small-to-medium-N configurational research: calibrating raw data into set membership, building and refining a truth table, and Boolean minimization into conservative / parsimonious / intermediate solutions with consistency and coverage. Because there is no maintained Python QCA library, it shells out to R's QCA package (calibrate, truthTable, minimize) via Rscript and documents that dependency honestly rather than faking a Python API. Use when the request mentions QCA, fsQCA, csQCA, configurational or set-theoretic analysis, necessary/sufficient conditions, truth tables, or calibration of conditions. For net-effect estimation of a single treatment prefer alterlab-causal-inference; for interpretive analysis prefer alterlab-qualitative-methods. Part of the AlterLab Academic Skills suite."
license: MIT
allowed-tools: Read Bash(Rscript:*)
compatibility: "Requires R with the QCA package (install.packages('QCA'); optionally SetMethods). NO maintained Python QCA library exists, so this skill shells to R via Rscript — declare R as a dependency. No API key. On the Anthropic API (no runtime install) document the R requirement and degrade gracefully."
metadata:
    skill-author: AlterLab
    version: "1.0.0"
    depends_on: "alterlab-ssci-design-gate (configurational vs net-effects), alterlab-qualitative-methods; audited by alterlab-ssci-inference-gate"
---

# QCA — Set-Theoretic, Configurational, Equifinal

**Skill type: ANALYSIS MODULE.** Qualitative Comparative Analysis (Ragin) treats cases as
**configurations** of conditions and asks which combinations are consistently sufficient (or
necessary) for an outcome. It is not net-effects regression: it assumes **equifinality** (several
paths to the same outcome), **conjunctural** causation (conditions work in combination), and
**asymmetry** (the path to Y is not the mirror of the path to not-Y).

## Core Mission

```
QCA IS ABOUT COMBINATIONS AND SET RELATIONS, NOT AVERAGE MARGINAL EFFECTS. CALIBRATE, THEN MINIMIZE.
```

## When to Use This Skill

- "Run a fuzzy-set QCA / fsQCA on my configurational data."
- "Which combinations of conditions are sufficient for the outcome?"
- "Calibrate these variables into set membership and build a truth table."
- "Test necessary and sufficient conditions across my ~20 cases."

### Does NOT Trigger

| The request is really about… | Route to | Why not this skill |
|---|---|---|
| The net effect of one treatment (DiD/IV/RDD/regression) | `alterlab-causal-inference` | Correlational/marginal effects, not set relations. |
| Whether a configurational design is even appropriate | `alterlab-ssci-design-gate` | Design routing, upstream. |
| Interpretive/thematic analysis of qualitative data | `alterlab-qualitative-methods` | Not set-theoretic. |
| Plain descriptive statistics | `alterlab-statistical-analysis` | No calibration/minimization. |

## The R path (verified — QCA package, no Python equivalent)

There is **no maintained Python QCA library** (the only PyPI option, `scpQCA`, is stale and
non-standard). The field standard is Adrian Dușa's R **`QCA`** package. Shell to it via `Rscript`.
The three verified calls:

```r
library(QCA)

# 1. Calibrate raw columns into fuzzy (or crisp) set membership.
#    thresholds for the direct method = c(exclusion, crossover, inclusion), ascending.
df$A <- calibrate(raw$A, type = "fuzzy", thresholds = c(4, 6, 8))

# 2. Build the truth table.
#    incl.cut = consistency cutoff; n.cut = min frequency for an observed row.
tt <- truthTable(df, outcome = "OUT", conditions = c("A","B","C"),
                 incl.cut = 0.80, n.cut = 1, show.cases = TRUE, sort.by = "incl")

# 3. Boolean minimization.
#    conservative = no remainders; parsimonious = include "?"; intermediate = supply dir.exp.
sol_c <- minimize(tt, details = TRUE)                       # conservative
sol_p <- minimize(tt, include = "?", details = TRUE)        # parsimonious
sol_i <- minimize(tt, include = "?", dir.exp = c(A=1,B=1,C=1), details = TRUE)  # intermediate
```

Fit parameters printed: **inclS** (sufficiency consistency), **PRI**, **covS** (raw coverage),
**covU** (unique coverage); necessity uses **inclN**, **RoN**. `pof()` tests parameters of fit for
a specific expression; `SetMethods` adds necessity/sufficiency XY plots, robustness, and
clustered-data diagnostics. Full runnable template and the calibration guidance:
`references/qca_in_r.md`.

## The discipline QCA demands

1. **Calibration is a theoretical act, not a mechanical one.** Anchor the three thresholds
   (full-out, crossover, full-in) on substantive knowledge; **avoid membership exactly 0.5** (it is
   undefined for logical operations). Justify each anchor.
2. **Report both the parsimonious and intermediate solutions**, and be explicit about which logical
   remainders (counterfactuals) the intermediate solution used — that is where analytic choices hide.
3. **Consistency before coverage.** A solution term needs high sufficiency consistency (inclS,
   commonly ≥ .80) before its coverage is worth interpreting; report PRI to catch simultaneous
   subset relations in Y and not-Y.
4. **Necessity and sufficiency are separate analyses** — test necessary conditions before minimizing
   for sufficiency; do not read a sufficiency solution as a necessity claim.

## Output Template

```
CALIBRATION:  <per condition: anchors (excl, crossover, incl) + justification>
TRUTH TABLE:  <rows, incl.cut, n.cut, contradictions handled>
SOLUTIONS:    conservative / parsimonious / intermediate (state remainders used)
FIT:          per term inclS, PRI, covS, covU; overall solution consistency + coverage
CLAIM:        configurational (combinations X are sufficient for Y); NOT "X raises Y on average"
```

## References

- `references/qca_in_r.md` — full runnable Rscript template, calibration guidance, fit-parameter glossary, and the graceful-degradation note when R is unavailable.

Part of the AlterLab Academic Skills suite.

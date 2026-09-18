# QCA in R — Runnable Template and Guidance

Loaded on demand from the qca SKILL.md. Verified against the CRAN `QCA` package (v3.25, Adrian
Dușa) and the QCA book (bookdown.org/dusadrian/QCAbook). There is no maintained Python equivalent,
so this is the real path — shell to R via `Rscript`.

## Full runnable Rscript template

Save as `qca_run.R` and run `Rscript qca_run.R data.csv`:

```r
#!/usr/bin/env Rscript
args <- commandArgs(trailingOnly = TRUE)
suppressMessages(library(QCA))
raw <- read.csv(args[1])

# --- 1. Calibration -------------------------------------------------------
# type = "fuzzy" | "crisp"; direct-method thresholds = c(exclusion, crossover, inclusion).
# Ascending anchors => increasing set membership; descending => decreasing.
data <- data.frame(
  A   = calibrate(raw$income,    type = "fuzzy", thresholds = c(20000, 40000, 80000)),
  B   = calibrate(raw$education, type = "fuzzy", thresholds = c(9, 12, 16)),
  C   = calibrate(raw$urban,     type = "crisp", thresholds = 0.5),
  OUT = calibrate(raw$success,   type = "fuzzy", thresholds = c(3, 5, 7))
)

# --- 2. Necessity (test BEFORE sufficiency) ------------------------------
# superSubset finds necessary (super)sets above consistency/coverage cutoffs.
nec <- superSubset(data, outcome = "OUT", incl.cut = 0.90, cov.cut = 0.60)
print(nec)

# --- 3. Truth table -------------------------------------------------------
tt <- truthTable(data, outcome = "OUT", conditions = c("A", "B", "C"),
                 incl.cut = 0.80, n.cut = 1, show.cases = TRUE, sort.by = "incl")
print(tt)

# --- 4. Minimization: conservative, parsimonious, intermediate -----------
sol_c <- minimize(tt, details = TRUE)
sol_p <- minimize(tt, include = "?", details = TRUE)
sol_i <- minimize(tt, include = "?", dir.exp = c(A = 1, B = 1, C = 1), details = TRUE)
cat("\n--- CONSERVATIVE ---\n"); print(sol_c)
cat("\n--- PARSIMONIOUS ---\n"); print(sol_p)
cat("\n--- INTERMEDIATE ---\n"); print(sol_i)
```

## Verified argument reference

- **`calibrate(x, type=, method="direct", thresholds=, logistic=TRUE, ...)`** — `type="fuzzy"`/
  `"crisp"`; `thresholds=c(excl, crossover, incl)` for s-shaped direct calibration; `logistic=TRUE`
  (default) vs linear (`logistic=FALSE`); `method` = "direct"/"indirect"/"TFR".
- **`truthTable(data, outcome=, conditions=, incl.cut=, n.cut=, pri.cut=, sort.by=, show.cases=, ...)`**
  — `incl.cut` consistency cutoff (length-2 allowed for absence); `n.cut` frequency cutoff (rows
  below become remainders); `sort.by="incl"` (add `-`/`+` for direction).
- **`minimize(input, include="", dir.exp=NULL, details=FALSE, all.sol=FALSE, row.dom=FALSE,
  method="CCubes", ...)`** — `input` a truthTable (preferred); `include="?"` adds logical
  remainders (parsimonious); `dir.exp` directional expectations produce the intermediate solution.
- **Fit parameters**: sufficiency → `inclS` (consistency), `PRI`, `covS` (raw coverage), `covU`
  (unique coverage); necessity → `inclN`, `RoN`. `pof(expression, outcome, data, relation=)` tests
  fit for a specific term.
- **Companion**: `SetMethods` (XY plots, robustness, Enhanced Standard Analysis, clustered QCA);
  `QCAGUI` (Shiny GUI).

## Calibration guidance

- The three anchors encode theory: full non-membership (0), the point of maximum ambiguity
  (crossover, 0.5), and full membership (1). Choose them from substantive/theoretical knowledge,
  not sample quantiles by default.
- **Avoid exactly 0.5** membership — it is logically undefined; nudge crossover so no case lands on
  it.
- Report the calibration for every condition; it is the most consequential and most contestable
  step.

## Solution-reporting discipline

- Present **parsimonious and intermediate** solutions side by side; state which logical remainders
  (easy counterfactuals) the intermediate solution incorporated.
- Interpret a term only if its sufficiency consistency (`inclS`) clears the cutoff (commonly ≥ .80);
  use `PRI` to guard against a term being a subset of both Y and not-Y.
- Coverage tells you empirical importance (raw `covS`) and distinctiveness (`covU`), not truth —
  a low-coverage but high-consistency path is still a valid sufficient configuration.

## Graceful degradation when R is unavailable

If `Rscript` or the `QCA` package is not installed, do NOT fabricate a Python fsQCA run. State the
dependency, give the exact `install.packages("QCA")` step and the template above, and offer to (a)
hand-compute a small crisp-set truth table, or (b) outline the calibration so the user can run it in
R or the QCAGUI. Never emit numbers from a non-existent Python QCA API.

## References

- Ragin (2008), *Redesigning Social Inquiry: Fuzzy Sets and Beyond.*
- Dușa (2019), *QCA with R: A Comprehensive Resource* (bookdown.org/dusadrian/QCAbook).
- Schneider & Wagemann (2012), *Set-Theoretic Methods for the Social Sciences.*

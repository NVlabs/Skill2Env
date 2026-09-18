# Changelog

All notable changes to this skill will be documented in this file.

## [1.2.2] - 2026-06-24

### Added
- **SKILL.md:** `Verification checklist` section (6 evidence-based checkbox items)
  tying trust in a convergence result to concrete script outputs — `mean_order`,
  per-triplet `observed_orders`, `convergence_assessment` PASS, `in_asymptotic_range`,
  refinement ratios >= 1.3, safety-factor choice, `gci_fine`, and `extrapolated_value`.
- **SKILL.md:** `Common pitfalls & rationalizations` section (6-row table) covering
  the 2-grid "converged" fallacy, the constant-ratio `AR = f1/f2` trap,
  tiny-GCI grid-independence claims, superconvergence misread as extra accuracy,
  quoting an extrapolated value when the order is non-positive, and conflating
  temporal stability with temporal accuracy.

## [1.2.0] - 2026-06-23

### Fixed
- **gci_calculator.py (wrong science):** for non-uniform refinement ratios
  (`r21 != r32`) the observed order is now solved with the iterative ASME V&V 20 /
  Celik et al. (2008) fixed-point procedure (damped for robust convergence) instead
  of the simple equal-ratio formula. Example `--spacings 0.08,0.02,0.01 --values
  1.05,1.0032,1.0008` now reports observed_order ~1.98 (was ~4.29).
- **gci_calculator.py:** safety factor is now validated as a finite number `>= 1.0`
  (NaN/inf and values like 0.5 are rejected with exit code 2); previously only
  `<= 0` was rejected.
- **gci_calculator.py:** guarded the `r^p == 1` / non-finite path when computing the
  asymptotic ratio.
- **h_refinement.py / dt_refinement.py:** a non-positive (diverging) observed order
  now forces `in_asymptotic_range = false` and suppresses Richardson extrapolation
  (`richardson_extrapolated_value = null`) with an explicit diverging note, instead
  of reporting `in_asymptotic_range: true` with a meaningless extrapolated value.
- **references/gci_guidelines.md:** corrected the worked-example `GCI_fine` from the
  wrong `0.027%` to `0.10%` (precise 0.0999%) and added `GCI_coarse = 0.40%`.
- **SKILL.md:** removed the self-contradictory "NumPy (not required)" requirement.

### Added
- Entry-count cap (max 10000 levels, exit code 2) in all four scripts, matching the
  documented Security safeguards.
- `results.notes` field in `gci_calculator.py` JSON output, flagging non-uniform
  iterative solves and the constant-ratio `AR = f1/f2` caveat.
- Interpretation-guidance caveat in SKILL.md explaining that for constant refinement
  ratios the asymptotic ratio degenerates to `f1/f2` and that order-vs-expected
  comparison (and 4+ grid consistency) is the meaningful asymptotic-range check.
- Regression unit tests for each of the above fixes.

### Changed
- Reworked eval case 4 so the assertions match the data (observed order is exactly
  2.0; the prompt's superconvergence suspicion is debunked rather than presupposed).

## [1.1.0] - 2026-03-26

### Added
- Optimized description for agent discovery (agentskills.io compliant)
- Evaluation suite with test cases and assertions
- Security review documentation with risk tier classification
- Standardized metadata block (author, version, security_tier, tested_with)
- This CHANGELOG file

### Changed
- Updated SKILL.md frontmatter with metadata block

## [1.0.0] - 2026-02-25

### Added
- Initial release
- h-refinement, dt-refinement, Richardson extrapolation, GCI calculation per ASME V&V 20 standards
- CLI scripts with --json output and argparse interface
- Reference documentation

# Changelog

All notable changes to this skill will be documented in this file.

## [1.2.2] - 2026-06-24

### Added
- **Verification checklist** section (6 evidence-based checkbox items) tying trust
  in results to concrete script outputs: `doe_generator.py` `coverage.count`/factorial
  `note`, `optimizer_selector.py` `recommended`/`expected_evals` (`<= budget`),
  `sensitivity_summary.py` `ranking` low-sensitivity flag, and surrogate
  `cv_error` vs `output_variance` (with the RBF in-sample `mse` caveat) plus a
  finite-`cv_error` (sample-count) check.
- **Common pitfalls & rationalizations** table (6 rows) covering RBF in-sample
  `mse`, factorial budget-vs-`levels` sizing, the deprecated `sobol` alias,
  budget-gated optimizer selection, the script ranking pre-supplied scores it does
  not compute, and "ran without error != valid".

## [1.2.0] - 2026-06-23

### Fixed
- **Surrogate science (F1/F7):** `surrogate_builder.py` no longer reports the data
  variance mislabeled as `mse`. It now performs a real fit — least-squares
  polynomial (degree up to 2) for `model=poly` and Gaussian RBF interpolation for
  `model=rbf` — and reports an honest residual `mse`, a leave-one-out `cv_error`,
  and the data `output_variance` as a clearly separate baseline. The metric now
  responds to model choice and to the x layout.
- **Optimizer dimension cutoff (F4):** harmonized the Bayesian Optimization
  applicability bound to `dim <= 10` across `optimizer_selector.py` and the
  SKILL.md decision tree, matching `references/optimizer_selection.md`. A 7D /
  budget-50 problem now correctly routes to Bayesian Optimization.
- **Factorial silent wrong-design (F6):** added an explicit `--levels` flag
  (`samples = levels**params`). When `--budget` is used and the realized factorial
  sample count differs from the request, the script now emits a warning and a
  `note`/`requested_budget` field instead of silently rounding. `--budget` is now
  optional when `--levels` is supplied for factorial.
- **Documentation drift (F2/F3/F5):** corrected the Security section surrogate
  allowlist to `(rbf, poly)`, the DOE method allowlist to include
  `quasi-random`/`sobol`, and the Error Handling table to quote the messages the
  scripts actually emit. Updated the output-field and DOE-method tables.

### Added
- `--levels` argument and `coverage.levels` / `requested_budget` / `note` output
  fields for factorial designs.
- `metrics.cv_error` and `metrics.output_variance` to surrogate output.
- Regression unit tests for each fix (surrogate residual semantics, BO cutoff,
  factorial levels/budget warnings).

### Changed
- `evals.json` eval 4 assertions strengthened to verify `mse` responds to fit
  quality (catching the former Var(y) mislabel); eval 3 updated to the dim>10 BO
  cutoff; eval 5 updated to set 4 levels via `--levels 4` or `--budget 16`.

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
- DOE sample plan generation (LHS, quasi-random, factorial), sensitivity ranking, optimizer selection, surrogate model fitting
- CLI scripts with --json output and argparse interface
- Reference documentation

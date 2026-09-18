# Changelog

All notable changes to this skill will be documented in this file.

## [1.2.2] - 2026-06-24

### Added
- `SKILL.md`: "Verification checklist" section (4-7 evidence-based items) requiring concrete artifacts from this skill's scripts — recorded `convergence_type`/`estimated_rate` and `converged` vs the real tolerance from `convergence_analyzer.py`, `patterns_detected` from `residual_monitor.py`, `condition_number`/`jacobian_quality`/`finite_diff_error`/`rank_deficient` from `jacobian_diagnostics.py`, trust-region reduction `ratio`/`trust_radius_action` from `step_quality.py`, and agreement with `solver_selector.py`/`globalization_advisor.py` recommendations
- `SKILL.md`: "Common pitfalls & rationalizations" table (7 rows) covering constant-ratio-misread-as-superlinear, run-completion-vs-convergence, insufficient-iterations order estimation, unverified analytic Jacobians, loosening tolerance to mask divergence, trust-region step acceptance/expansion by ρ, and large/expensive-Jacobian Newton-Krylov routing

## [1.2.0] - 2026-06-23

### Added
- `solver_selector.py`: `--problem-type {root-finding,optimization,least-squares}` with a dedicated nonlinear least-squares path that recommends Levenberg-Marquardt (primary) and Gauss-Newton (alternative)
- `globalization_advisor.py`: `--far-from-solution` flag so a distant initial guess can drive a trust-region recommendation (the decisive factor was previously inexpressible)
- Input-validation hardening to match the SKILL.md Security section: size cap (10 billion) on `--size`, 100,000-entry caps on residual / step-size lists, finite checks on all numeric CLI inputs, matrix file-size limit and `.npy` loading with `allow_pickle=False` in `jacobian_diagnostics.py`
- Regression unit tests for the least-squares path, size-vs-high-accuracy ordering, large+expensive-Jacobian routing, `--far-from-solution`, the `-Infinity` JSON fix, and constant-ratio linear classification

### Changed
- `solver_selector.py`: problem size is now resolved before high-accuracy, so large/very-large problems are routed to Newton-Krylov (GMRES) instead of full Newton; large + expensive-Jacobian problems now recommend matrix-free Newton-Krylov (JFNK). The large-problem threshold is aligned to the documented n ≥ 1000
- `globalization_advisor.py`: Levenberg-Marquardt is now surfaced as `trust_region_type` for least-squares problems (previously only mentioned in a note)
- `convergence_analyzer.py`: convergence classification uses an order estimate (p ≈ log(r_{k+1}/r_k)/log(r_k/r_{k-1})); a constant contraction ratio is now correctly classified as linear (annotated "fast linear" for small ratios) rather than superlinear

### Fixed
- `step_quality.py`: `--json` output no longer emits the non-RFC-8259 token `-Infinity` for the `ratio` field; all non-finite ratios are serialized as `null`
- All scripts emit JSON with `allow_nan=False` so any future non-finite leak fails loudly instead of producing invalid JSON
- `SKILL.md`: Version History, convergence interpretation table, error table, and CLI examples updated to match actual script behavior

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
- Newton/quasi-Newton solver selection, line search and trust-region globalization, convergence rate analysis, Jacobian diagnostics
- CLI scripts with --json output and argparse interface
- Reference documentation

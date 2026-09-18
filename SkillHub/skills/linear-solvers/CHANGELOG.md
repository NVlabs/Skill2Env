# Changelog

All notable changes to this skill will be documented in this file.

## [1.2.2] - 2026-06-24

### Added
- **SKILL.md**: Added a "Verification checklist" section (6 evidence-based items
  tied to `convergence_diagnostics.py`, `residual_norms.py`, `solver_selector.py`,
  `sparsity_stats.py`, `scaling_equilibration.py`, and `preconditioner_advisor.py`
  outputs) and a "Common pitfalls & rationalizations" table (6 rows) covering
  mean-vs-asymptotic rate, absolute-vs-relative residual, CG misuse on indefinite
  systems, dense-direct memory gating, one-sided scaling, and GMRES stagnation.

## [1.2.0] - 2026-06-23

### Fixed
- **convergence_diagnostics.py**: Stagnation is now detected from the asymptotic
  (trailing-window) residual ratio instead of the whole-history mean, so a fast
  early drop followed by a flat tail is correctly flagged. Added an
  `asymptotic_rate` field to the JSON/text output alongside the existing `rate`.
- **solver_selector.py**: Replaced the magic `size >= 200000` cutoff with a
  dense-memory feasibility gate (dense float64 storage n²·8 bytes < ~2 GB). Large
  dense SPD systems now route to CG with a storage-estimate note instead of
  recommending an infeasible dense Cholesky.
- **solver_selector.py**: Small dense nonsymmetric and symmetric-indefinite
  systems now correctly recommend direct LU / LDLᵀ (Bunch-Kaufman), matching the
  documented decision tree. Added a `--saddle-point` flag that routes to a
  Schur-complement/Uzawa block approach.
- **scaling_equilibration.py**: For nonsymmetric matrices, `col_scale` is now
  derived from the row-scaled matrix (the documented Safe Default Strategy), so
  applying both reported scales actually equilibrates the system.
- **residual_norms.py**: Reject non-finite (inf/nan) absolute and relative
  tolerances (exit code 2), matching the Security section's finite-input claim.
- **preconditioner_advisor.py**: Symmetric-indefinite advice now notes that a
  MINRES preconditioner must be SPD (an indefinite incomplete LDLᵀ is invalid).
- **SKILL.md**: Corrected the conversational-workflow command (`--ill-conditioned`
  instead of the non-existent `--stagnation`), the Security flag/allowlist list,
  the symmetric-indefinite preconditioner entry, the direct-vs-iterative threshold,
  and added `asymptotic_rate` to the output-field table.
- **references/solver_decision_tree.md**: Corrected the CG worst-case iteration
  table to follow the quoted convergence bound and aligned the dense-direct
  threshold with the script's memory gate.
- **evals/evals.json**: Updated eval-4 assertions to reference the new
  `--saddle-point` flag; eval-2 stagnation assertion is now satisfiable.

### Added
- Regression unit tests for asymptotic stagnation, dense-feasibility routing,
  small-dense direct solvers, saddle-point routing, two-sided equilibration,
  the MINRES SPD-preconditioner note, and non-finite tolerance rejection.

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
- Solver selection (CG, GMRES, BiCGSTAB, direct), preconditioner recommendation (AMG, ILU, IC), convergence diagnostics
- CLI scripts with --json output and argparse interface
- Reference documentation

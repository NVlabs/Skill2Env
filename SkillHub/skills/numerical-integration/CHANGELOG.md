# Changelog

All notable changes to this skill will be documented in this file.

## [1.2.2] - 2026-06-24

### Added
- **Verification checklist** (6 evidence-based items): recording scaled
  `error_norm`/`scale_min` from `error_norm.py`, confirming per-step
  `error_norm <= accept_threshold` and logging rejected steps from
  `adaptive_step_controller.py`, verifying `controller_used: pi` when using the
  PI controller, recording integrator `recommended`/`notes` from
  `integrator_selector.py`, checking `error_estimate <= target-error` after
  substepping from `splitting_error_estimator.py`, and running the
  tighter-tolerance convergence validation.
- **Common pitfalls & rationalizations** table (6 rows) covering
  stability-vs-accuracy for implicit methods, single-tolerance over-trust, the
  silent PI->P fallback when `--prev-error` is omitted, lie-vs-strang splitting
  order, misuse of the stiff-without-Jacobian selector branch, and
  "ran without crashing != correct".

### Changed
- Bumped SKILL.md `version` to 1.2.2 (patch).

## [1.2.0] - 2026-06-23

### Fixed
- **PI step-size controller (science fix)**: corrected the PI factor to the
  standard `err^(-alpha) * err_prev^(beta)` form with `alpha=0.7/(p+1)`,
  `beta=0.4/(p+1)` (Hairer & Wanner / `error_control.md`). The previous code
  applied `(threshold/prev_error)^0.3*exp`, which used the wrong sign on the
  previous-error exponent and a non-standard `beta=0.3`. (F4)
- **error_norm.py crash**: solution-based scaling with `rtol=0`, `atol=0` and
  default `min_scale=0` no longer raises an uncaught `ZeroDivisionError`
  (exit 1); it now raises a clean validation error and exits 2, consistent with
  the `--scale` path. (F1)

### Changed
- SKILL.md Error Handling table now quotes the exact strings the scripts emit
  (`rtol/atol must be a non-negative finite number`,
  `error_norm must be finite and non-negative`, the scale-positivity message,
  the argparse `--controller` invalid-choice message, and
  `Provide at least one stiff or non-stiff term`). (F3)
- SKILL.md controller documentation, frontmatter description, and Security
  allowlist corrected to the implemented controllers `{p, pi}` (removed the
  non-existent `i`/`pid` CLI controllers; PID retained in `error_control.md` as
  reference-only theory). (F2)
- evals.json eval #2 expected_output updated to reference the implemented
  `P`/`PI` controllers.

### Added
- Regression tests: PI-controller formula lock-in, error_norm scale-collapse
  validation, and CLI message/allowlist anti-drift checks.

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
- Integrator selection (RK, BDF, Rosenbrock, Adams), adaptive step-size control (I/PI/PID), IMEX operator splitting
- CLI scripts with --json output and argparse interface
- Reference documentation

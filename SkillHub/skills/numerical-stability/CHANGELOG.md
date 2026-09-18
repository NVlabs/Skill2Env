# Changelog

All notable changes to this skill will be documented in this file.

## [1.2.2] - 2026-06-24

### Added
- **Verification checklist** section in SKILL.md: 7 evidence-based checkbox items, each requiring a concrete recorded value from the scripts (`cfl_checker.py` `metrics.cfl`/`metrics.fourier`/`metrics.reaction` vs `limits.*` and `criteria_applied`/`recommended_dt`; `von_neumann_analyzer.py` `max_amplification`; `stiffness_detector.py` `real_part_stiffness_ratio`/`imag_dominated`/`stiff`; `matrix_condition.py` `condition_number`/`status`) before a "stable" verdict.
- **Common pitfalls & rationalizations** table in SKILL.md: 6 domain-specific rows (implicit-stability-vs-accuracy, run-completion-vs-correctness, the `Fo ≤ 1/(2d)` dimension trap, magnitude vs real-part stiffness for imaginary-dominated spectra, recomputing `dt` after mesh refinement, and conditioning after a "successful" solve).

## [1.2.0] - 2026-06-23

### Fixed
- **Critical (wrong-science):** Corrected the phase-field "Conversational Workflow Example" in SKILL.md. The previous inputs (D=1e-3) computed Fo=0.001 (stable) yet the narrative declared the run unstable. Changed the example to D=1.0 so Fo=1.0 > 0.25 is genuinely unstable, matching the "blowing up after 100 steps" story; recommended_dt=2.5e-5 now reproduces the tool output.
- **Eval defect:** evals.json case 1 asserted Fo=0.1 for inputs (alpha=1e-5, dt=0.001, dx=0.01) that actually give Fo=1e-4. Corrected the expected_output and assertion to Fo=1e-4 (still stable, << 0.5).
- **Doc drift:** Interpretation Guidance now lists conditioning thresholds (>1e8 poorly-conditioned, >1e10 ill-conditioned) that match `matrix_condition.py` `status`, plus an IEEE-double-precision caveat. Replaces the previous single ">1e6 -> ill-conditioned" row that contradicted the tool by 2-4 orders of magnitude.
- **Doc drift:** Error Handling table now documents the actual message `Matrix not found: <path>`.

### Changed
- **Stiffness detection (wrong-science nuance):** `stiffness_detector.py` now bases the `stiff` verdict on scale separation among genuinely decaying modes (Re(λ)<0) via a new `real_part_stiffness_ratio`, and flags imaginary-axis-dominated spectra (oscillatory/wave/Hamiltonian) with `imag_dominated` and a `warning` instead of recommending BDF/Radau on magnitude alone. The classical magnitude `stiffness_ratio` is still reported. New output keys: `real_part_stiffness_ratio`, `imag_dominated`, `warning`.

### Security
- Enforced the safeguards previously only documented: `--dimensions` restricted to {1,2,3} (cfl_checker.py); finite-value validation of dx/dt/safety and physics params; `--eigs` and `--coeffs` capped at 10,000 entries; 500 MB file-size guard and explicit `allow_pickle=False` in `matrix_condition.py` and `stiffness_detector.py`; 100,000-per-side matrix dimension limit in `matrix_condition.py`. All raise and exit 2 on bad input.

### Tests
- Added regression tests for the phase-field example, eval-case-1 Fourier value, dimensions whitelist, non-finite inputs, conditioning status thresholds, imaginary-dominated stiffness, and the new input/size caps.

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
- CFL/Fourier analysis, von Neumann stability checks, stiffness detection, matrix conditioning
- CLI scripts with --json output and argparse interface
- Reference documentation

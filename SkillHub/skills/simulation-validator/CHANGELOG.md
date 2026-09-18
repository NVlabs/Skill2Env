# Changelog

All notable changes to this skill will be documented in this file.

## [1.2.2] - 2026-06-24

### Added
- **SKILL.md:** "Verification checklist" section (7 checkbox items) requiring concrete artifacts from the four validation scripts — `result_validator` `status`/`confidence_score`/`checks`/`failed_checks`, the recorded `--mass-tol`, `runtime_monitor` `residual_stats`/`dt_stats`/`alerts`, separate CFL/Fourier gating via `cfl_checker.py`, and `failure_diagnoser` output on failure.
- **SKILL.md:** "Common pitfalls & rationalizations" table (7 rows) covering preflight-vs-stability confusion, `INSUFFICIENT_DATA`/`null` confidence, weak vs strict (`--variational`) energy checks, `bounds_unverifiable` vs vacuous pass, run-completion-is-not-correctness, direction-aware dt collapse, and default-threshold misuse.

### Changed
- Bumped SKILL.md version to 1.2.2 (patch) and added a Version History entry.

## [1.2.0] - 2026-06-23

### Fixed
- **failure_diagnoser.py (F2):** removed the bare `residual` token from the convergence-failure regex (now `diverg|explo|did not converge|failed to converge|max.?iter|stagnat`), so healthy, fully-converged logs are no longer mis-diagnosed as "Convergence failure".
- **failure_diagnoser.py + runtime_monitor.py + log_patterns.md (F3):** anchored the numerical blow-up regex (`(?<![A-Za-z])(?:nan(?:s)?|inf(?:inity)?|overflow)(?![A-Za-z])`) so domain words like "nanometer", "infrastructure", "information", and "financial" no longer trigger false "Numerical blow-up", while "NaN", "NaNs", "infinity", and "overflow" still match.
- **runtime_monitor.py + log_patterns.md (F4):** replaced the default dt regex with `\bdt\b\D*?([0-9][0-9eE+.\-]*)` plus a dedicated adaptive-reduction rule capturing the post-reduction "to" value; "dt reduced from 1e-3 to 5e-4" now parses and "width 0.5 mm" no longer false-matches as dt.
- **runtime_monitor.py (F5):** dt-collapse detection is now direction-aware (running-max vs current); a healthy dt ramp-up no longer raises a false "Time step reduced" alert.
- **runtime_monitor.py (F1):** added a NaN/Inf/overflow log scan that emits an alert, matching the SKILL description and eval-2.
- **result_validator.py (F8):** added an opt-in strict variational energy check (`--variational` flag or `"energy_variational": true`) enforcing monotone non-increasing energy with a relative tolerance; the default weaker check is renamed `energy_net_decrease` and documented as not detecting mid-run spikes.
- **result_validator.py (F9):** eliminated vacuous passes — a requested bound with no matching field value is reported as `bounds_unverifiable` (failed), and an empty/unrecognized metrics file returns `confidence_score: null` with status `INSUFFICIENT_DATA` instead of a false 1.0.
- **preflight_checker.py (F10):** output-dir from the config is now resolved relative to the config file's directory, and the disk-space check probes the volume hosting the resolved output directory (nearest existing ancestor), naming the probed path in the message.

### Security
- Implemented the controls the Security section documents: a finite-positive validator for `--min-free-gb`, `--residual-growth`, `--dt-drop`, `--mass-tol`; a finite validator for `--bound-min`/`--bound-max` with `--bound-max > --bound-min` enforced; a `^[A-Za-z0-9_.-]+$` allowlist for `--required` names; `max > min` and finiteness enforced on `--ranges`; and a 500 MB file-size cap before reading logs in `runtime_monitor.py` and `failure_diagnoser.py`. Invalid input exits with code 2.

### Changed
- Updated SKILL.md output-field/error tables, confidence interpretation, and Security section to match actual script behavior; bumped version to 1.2.0; added advisory notes to validation_protocol.md clarifying that stability (CFL/Fourier) checks are not performed by preflight (use `cfl_checker.py`).
- Re-scoped evals.json eval 5 assertions to verifiable tool outputs and tightened eval 2 assertion wording.

### Tests
- Added regression tests for every fix above across test_failure_diagnoser.py, test_runtime_monitor.py, test_result_validator.py, and test_preflight_checker.py.

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
- Pre-flight config validation, runtime log monitoring (NaN/Inf, residual growth, dt collapse), post-flight result checks, failure diagnosis
- CLI scripts with --json output and argparse interface
- Reference documentation

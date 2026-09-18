# Changelog

All notable changes to this skill will be documented in this file.

## [1.1.3] - 2026-06-24

### Added
- `SKILL.md`: new **Verification checklist** section (7 evidence-based items) requiring the agent to reconcile `summary.total_jobs`/`completed`/`failed`, confirm the swept key path actually altered the solver-read value, record `summary.minimize` direction, independently verify real exit status (since `job_tracker.py` flags "completed" from result-file existence alone), apply an outlier sanity check, and record the LHS `--seed`/`manifest.json` for reproducibility.
- `SKILL.md`: new **Common pitfalls & rationalizations** table (7 rows) covering the result-file-only completion heuristic, silently-skipped runs, minimize-by-default direction, bare-vs-dotted key-path merge, metric-name typos returning `None`, grid `n^d` explosion, and unrecorded LHS seeds.

## [1.1.1] - 2026-06-23

### Fixed
- `sweep_generator.py`: `merge_config` now supports dot-notation override keys (e.g. `parameters.kappa`) so swept parameters can target nested config locations. Previously a shallow top-level `dict.update()` would write a new top-level key while leaving a nested base value (e.g. `parameters.kappa`) untouched, making nested sweeps scientifically meaningless.
- Corrected the `sweep_generator.py` module-docstring linspace example (`dt:1e-4:1e-2:5` -> `[0.0001, 0.002575, 0.00505, 0.007525, 0.01]`).
- `SKILL.md`: corrected the Script Outputs table to be action-specific for `campaign_manager.py` (init vs status vs list), documented `--maximize` (aggregator minimizes by default) and the read-only `list` action / `--status-filter`, and fixed the Version History dates to match this CHANGELOG.
- `evals/evals.json`: bound eval 3 assertion to the status invocation's output fields.

### Added (security hardening)
- `sweep_generator.py`: validate swept parameter names against `[a-zA-Z_][a-zA-Z0-9_]*(.[...])*`, reject non-finite (`NaN`/`Inf`) bounds, require positive integer counts capped at 100,000, cap parameters per sweep at 32, and validate `--samples` as a positive integer capped at 1,000,000. All bad input exits with code 2.

### Changed
- `result_aggregator.py`: docstring example metric renamed from the direction-ambiguous `objective_value` to direction-explicit `final_energy` (minimize) / `yield` (`--maximize`).
- Flattened the bundled fixture `tests/fixtures/simulation-orchestrator/base_config.json` so `dt`/`kappa` are top-level keys, matching the top-level reads in the documented sweep examples.

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
- Parameter sweep generation (grid, linspace, LHS), campaign initialization and tracking, job status monitoring, result aggregation
- CLI scripts with --json output and argparse interface
- Reference documentation

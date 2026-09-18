# Changelog

All notable changes to this skill will be documented in this file.

## [1.1.3] - 2026-06-24

### Added
- **"Verification checklist" section** in SKILL.md (7 evidence-based items) tying
  trust in a result to concrete artifacts the scripts actually emit: listing real
  field names/shape via `field_extractor.py --list`, choosing the right
  convergence test (`--absolute-threshold`/`convergence_threshold` for residuals
  vs `--detect-steady-state`/`steady_state` for physical quantities), reconciling
  `convergence.type`/`rate` with `steady_state.reached`, conservation drift via
  `derived_quantities.py --quantity mass`/`integral`, the echoed `spacing` block
  and absence of the inconsistent-`dx` warning, non-finite (NaN/Inf) guards, and
  mapping `comparison_tool.py` error to the documented agreement bands.
- **"Common pitfalls & rationalizations" table** (7 rows) covering domain-specific
  rationalizations: misreading `steady_state.reached`, mistaking a stalled
  plateau for convergence, assuming field names/grid size, treating two-grid
  agreement as mesh independence, conflating volume fraction with conserved mass,
  the `dx=1.0` grid-unit fallback, and "it ran so it's valid".

### Changed
- Bumped SKILL.md `version` to 1.1.3 and added the matching Version History entry.
  Documentation only; no script behavior change.

## [1.1.1] - 2026-06-23

### Fixed
- **`statistical_analyzer.py` `--region` now actually filters** (was a stub that
  silently returned whole-field statistics under a region label). Coordinates
  are derived from the field shape and grid spacing (explicit `dx`/`dy` or
  `Lx`/`Ly` via `dx = Lx/(nx-1)`); the parsed condition is applied as a real
  per-cell coordinate mask. SKILL.md and the Security section were corrected to
  match (only `x`/`y`/`z` vs numbers, joined by `and`/`or`; invalid input exits 2).
- **`report_generator.py` reads the nested `fields.*.values` layout.** The
  statistics section previously found only top-level flat fields and reported an
  empty final-state for the skill's own nested fixture format; it now discovers
  fields from both the top level and `fields`, skipping scalar metadata
  (`timestep`, `time`, `dx`, ...).
- **`derived_quantities.py` grid spacing gives explicit `dx`/`dy`/`dz`
  precedence.** Explicit spacing was being unconditionally overwritten by the
  node-based `Lx/(nx-1)` formula whenever a domain size was present (≈11% error
  on a cell-centered 10-cell field). A warning is emitted on genuinely
  inconsistent input.

### Added
- `time_series_analyzer.py --absolute-threshold` convergence mode: the
  physically correct `|x_final| <= tol` test for residual/error quantities,
  alongside the relative steady-state test for physical quantities.
- Residual-vs-physical interpretation guidance in SKILL.md and
  `statistical_methods.md`, reconciling the steady-state and convergence signals.
- `--bins` (statistical_analyzer) and `--window` (time_series_analyzer) bounds
  validation (positive, with an upper cap; exit 2 on bad input).
- Regression unit tests for each of the above fixes.

### Changed
- Corrected the SKILL.md Output Format example, `data_formats.md` output-schema
  section, and Version History to reflect what scripts actually emit (no
  fabricated `script`/`version`/`input_file` keys; documented the
  `derived_quantities.py` `{inputs, results}` envelope).
- Fixed eval case 2 assertions to interpret residual convergence correctly.

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
- Field extraction, time-series analysis, line profiles, statistical summaries, derived quantities, comparison tools, report generation
- CLI scripts with --json output and argparse interface
- Reference documentation

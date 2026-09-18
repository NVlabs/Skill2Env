# Changelog

All notable changes to this skill will be documented in this file.

## [1.2.2] - 2026-06-24

### Added
- SKILL.md: "Verification checklist" section (7 evidence-based checkbox items)
  tying trust in a result to concrete script outputs — non-empty
  `timing_analyzer.py` `results.phases`, phase percentages summing to ~100%,
  recorded `average_efficiency`/`efficiency_threshold_processors` from
  `scaling_analyzer.py`, the four-term memory breakdown and correct `solver.type`
  from `memory_profiler.py`, `per_process_gb` vs `--available-gb`, and a
  before/after re-profile after each optimization.
- SKILL.md: "Common pitfalls & rationalizations" section (6-row table) covering
  empty-pattern "balanced run" false negatives, two-point scaling claims,
  iterative-vs-direct/matrix-free memory under-estimation, total-vs-per-process
  RAM, the 30% I/O threshold, and recommendations being limited to the JSON
  inputs actually supplied.

## [1.2.0] - 2026-06-23

### Fixed
- **bottleneck_detector.py**: Read the actual analyzer output schema. The
  detector previously looked for non-existent top-level keys (`timing_data`,
  `scaling_analysis`, `memory_profile`) and silently returned zero bottlenecks
  when fed real `timing_analyzer.py` / `scaling_analyzer.py` / `memory_profiler.py`
  output (which nests its payload under `results`). It now resolves the `results`
  envelope with a backward-compatible bare-payload fallback, so a solver-dominated
  run correctly produces a high-severity solver bottleneck.
- **bottleneck_detector.py**: Per-type dominance thresholds matching the docs —
  I/O phases are flagged above 30% (was 50%), solver/assembly/general above 50%,
  high severity above 70%. Phases between 30-50% are no longer silently ignored.
- **bottleneck_detector.py**: Canonical phase name `I/O` (lowercases to `i/o`)
  is now classified as I/O instead of falling through to the generic category;
  classification normalizes non-alphanumerics before keyword matching.
- **memory_profiler.py**: Added the matrix-storage term and made solver-memory
  depend on `solver.type`, implementing the three-term formula
  `Total = Field + Solver Workspace + Matrix Storage` from `profiling_guide.md`.
  `direct` solvers now estimate substantially more memory than `iterative`
  (conservative fill-in factor), and `matrix-free` stores no matrix — fixing the
  previously identical, unsafe estimates. New `results.matrix_storage_gb` field.
- **timing_analyzer.py**: When a user `--pattern` matches zero entries, emit a
  hint (stderr and `results.message` / `results.suggested_patterns`) listing the
  built-in formats, so users can recover from a non-matching custom pattern.

### Changed
- Output of `bottleneck_detector.py` timing bottlenecks now includes a `category`
  field (`solver`/`assembly`/`io`/`general`).
- SKILL.md: corrected the Script Outputs table to the real `inputs`/`results`
  envelope, reconciled timing-threshold guidance, documented the memory model,
  and pointed Version History to the CHANGELOG.
- evals.json: assertions reference `results.*` fields and require non-empty,
  correctly-categorized bottlenecks for the comprehensive analysis case.

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
- Timing log analysis, strong/weak scaling efficiency evaluation, memory estimation, bottleneck detection with optimization recommendations
- CLI scripts with --json output and argparse interface
- Reference documentation

# Changelog

All notable changes to this skill will be documented in this file.

## [1.2.2] - 2026-06-24

### Added
- "Verification checklist" section in SKILL.md: 6 evidence-based checkbox items tied to `timestep_planner.py`, `output_schedule.py`, and `checkpoint_planner.py` outputs (dt vs limit, safety margin, endpoint-inclusive count, checkpoint overhead band, clean exit codes).
- "Common pitfalls & rationalizations" section in SKILL.md: 6-row table of domain-specific shortcuts (implicit-so-any-dt, safety > 1.0, ran-so-valid, off-by-one frame count, checkpoint-every-step, stale-plan reuse) and their corrections.

## [1.2.0] - 2026-06-23

### Fixed
- Corrected the checkpoint-overhead numbers in the worked example and eval id=1: the documented command yields ~6.7% overhead (Acceptable band), not ~0.7% (F1).
- Fixed the output-schedule frame count in eval id=3: t=0..5 at 0.05 s spacing produces 101 endpoint-inclusive frames (100 intervals), not 100 (F5).
- Removed accumulated floating-point drift in `output_schedule.py` by generating times by index and snapping the final point exactly to `t_end` (F6).

### Added
- `checkpoint_planner.py`: rejects `checkpoint-cost >= run-time` (exit 2) and emits a `warnings` field when overhead exceeds 10% (F3).
- `timestep_planner.py`: rejects `safety > 1.0` (would otherwise return a dt above the stability limit) and adds a "Recommended dt exceeds stability limit" note (F2); rejects negative `ramp-steps`/`preview-steps` and enforces a 1,000,000 upper bound, materializing only the previewed slice to bound memory (F4).
- Finite (`inf`/`nan`) input validation across all three scripts to match the Security section.
- Regression unit tests for every critical/high fix.

### Changed
- SKILL.md Security section, Script Outputs table, and worked example updated to match actual script behavior.

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
- Time-step planning with CFL-coupled stability limits, adaptive ramping, output scheduling, and checkpoint cadence
- CLI scripts with --json output and argparse interface
- Reference documentation

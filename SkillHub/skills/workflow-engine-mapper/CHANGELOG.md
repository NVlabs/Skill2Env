# Changelog

## 1.2.2 - 2026-06-24

- Added a `Verification checklist` section (7 checkbox items) requiring concrete artifacts: the full `--json` payload with echoed inputs, the documented engine precedence, branch+sweep DAG composition and restart-checkpoint suffix, the `provenance_requirements`/`restart_strategy` flags, the one-off `migration_triggers` entry, the `storage_layout` scaffold, and a `0` exit code.
- Added a `Common pitfalls & rationalizations` table (6 rows) covering one-off-as-permanent, AiiDA over-selection vs. lighter stores, trusting a run without re-reading echoed input flags, collapsing a screening DAG that should compose a property branch, skipping checkpointing despite the `runs>=20` rule, and masking input mismatches with `--preferred`.
- Bumped SKILL.md frontmatter version 1.2.1 -> 1.2.2 (docs only; no script behavior change).

## 1.1.0 - 2026-06-23

- Fixed `dag_pattern` to compose branch (relax/static/property) and sweep (screen/campaign) structures instead of overwriting one with the other; a high-throughput relax-static-DOS screening now reports `map over structures -> (relax -> static -> property branches) -> collect -> rank` (F4).
- One-off recommendations now emit a concrete forward-looking entry in `migration_triggers` (when to move to a workflow engine) instead of an empty list (F2).
- Documented the AiiDA gating and the fixed recommendation precedence in SKILL.md Decision Guidance so the prose matches the implemented thresholds (F3).
- Hardened input validation to match the Security section: `runs` capped at 1,000,000 and rejected for non-positive/boolean values; `task` length-capped at 2000 chars, `code`/`preferred` at 100 chars; invalid input exits with code 2.
- Repaired the `atomate2_vasp_dos` and `one_off_exploration` eval cases so expected_outputs/assertions test derived behavior rather than echoed inputs (F1, F2).
- Added regression unit tests for the DAG composition, one-off migration trigger, and input-validation bounds.

## 1.0.0 - 2026-05-18

- Initial workflow engine mapping skill.

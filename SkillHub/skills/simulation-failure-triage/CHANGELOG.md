# Changelog

## 1.1.3 - 2026-06-24

- Docs: added a `Verification checklist` (7 items) requiring concrete artifacts
  tied to `failure_triage.py` outputs — preserved-evidence set before rerun,
  the FIRST warning/error captured in `evidence.log_excerpt`, every
  `likely_causes` entry logged with `category`/`first_action`, correct
  `crash` vs `corrupted-output` and `out-of-memory` vs `incomplete-run`
  classification, strict one-change-per-rung retry ladder, observed
  `stop_conditions`, and handoff to `simulation-validator` for validity.
- Docs: added a `Common pitfalls & rationalizations` table (6 rows) covering
  last-line-only triage, treating a segfault as an I/O/disk issue, bumping
  walltime for an OOM, stacking multiple stabilizing changes at once,
  assuming a clean run after a missing-potential fix means valid physics, and
  equating "it runs" with "results are trustworthy".

## 1.1.0 - 2026-06-23

- Fix (F1): segmentation faults / SIGSEGV / signal 11 / core dumped now map to a
  dedicated `crash` ("process crash / memory fault") symptom instead of being
  mislabeled `corrupted-output` (I/O failure). First action now points to
  memory/ABI/debugger investigation rather than checking disk/scratch.
- Fix (F2): "out of memory" / `bad_alloc` / `oom-kill` / "allocation failed" now
  map to a dedicated `out-of-memory` ("memory exhaustion") symptom with
  resource-reduction guidance, instead of the generic `incomplete-run`. A bare
  "killed" remains `incomplete-run` (genuinely ambiguous). Added a
  resource-reduction rung to the retry ladder and memory/crash lines to
  references/failure_patterns.md.
- Fix (F5): `evidence.log_excerpt` now preserves original casing of the log
  (matching is still case-insensitive), consistent with the "preserve evidence"
  guidance.
- Fix (F3): corrected `missing_potential` eval `expected_outputs` token from
  "missing potential" (space) to "missing-potential" (the string the script
  actually emits).
- Fix (F4): sharpened the skill description to claim its first-response triage /
  retry-ladder / stop-conditions niche and explicitly defer deep validation to
  simulation-validator.
- Security: added input-validation caps (max 50 symptoms, 100 chars per symptom,
  100-char code) exiting with code 2, matching the SKILL.md Security section.

## 1.0.0 - 2026-05-18

- Initial cross-code simulation failure triage skill.

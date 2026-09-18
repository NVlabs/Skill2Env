# Changelog

## 1.1.3 - 2026-06-24

### Added
- "Verification checklist" section with 6 evidence-based checkbox items tied to
  the script's actual outputs (`resource_layout`, `tasks_per_node`/`total_cpus`,
  resolved total `gpus` and ranks/GPU vs the 16 threshold, the full `warnings`
  list, `environment_checks` artifacts, `diagnoses`/`custom` handling, and the
  `retry_plan`).
- "Common pitfalls & rationalizations" table with 6 domain-specific
  rationalizations (run completion != correctness, per-node vs total ranks/GPU,
  `--gpus` vs `--gpus-per-node`, scheduler-kill vs physics, unknown/`custom`
  symptoms, and one-variable-at-a-time retries).

## 1.1.0 - 2026-06-23

### Fixed
- Ranks-per-GPU warning now uses a unit-consistent metric (total ranks / total
  GPUs) instead of comparing per-node tasks against the whole-job GPU count. The
  old rule missed genuine oversubscription on multi-node jobs (e.g. 512 tasks /
  4 GPUs = 128 ranks/GPU previously produced no warning). The warning now reports
  the computed ranks/GPU value and fires above 16 ranks/GPU. (F1)
- `tasks_per_node` is now reported as an integer when tasks divide evenly across
  nodes; a non-divisible layout keeps the float value and emits a new warning
  about uneven rank placement and load imbalance instead of silently leaking a
  fractional value into the JSON. (F3)
- Default (non-JSON) output now prints a resource-layout summary, all warnings,
  environment checks, and the retry plan, and is never silent when no symptoms
  are supplied. Previously only per-symptom diagnoses were printed, hiding the
  most actionable warnings. (F4)

### Added
- `--gpus-per-node` argument (SLURM `--gres=gpu:N` semantics). When set, total
  GPUs are computed as `gpus_per_node * nodes` and it overrides `--gpus`.
  Documented that `--gpus` is the total (whole-job) GPU count.
- Input caps for security: resource counts capped at 1,000,000, symptoms limited
  to 64 entries of <= 64 characters each, and `--walltime` limited to 32
  characters. Out-of-range or non-integer input exits with code 2.

### Tests
- Added `tests/unit/test_hpc_runtime_doctor.py` with regression coverage for the
  ranks-per-GPU fix, uneven task placement, human-readable output, and the input
  caps; extended `tests/unit/test_new_skill_planners.py` accordingly.

## 1.0.0 - 2026-05-18

- Initial HPC runtime diagnosis skill.

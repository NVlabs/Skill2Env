# Changelog

## 1.2.2 - 2026-06-24

- Docs: added a "Verification checklist" section (7 evidence-based items tied to
  `fair_checks.has_hashes_for_existing_files`, `missing_files`, per-file `sha256`,
  `engine_version`, `units`, `structure_id`, and `--out` output) and a
  "Common pitfalls & rationalizations" table (6 rows) so agents validate the
  manifest's real output instead of trusting a clean exit code.

## 1.2.0 - 2026-06-23

- Evals: made all three eval cases discriminating by adding `script_checks` that pin
  `fair_packager.py --json` output to verified values — per-file `sha256` and
  `size_bytes`, the parsed `units`, `structure_id`, `engine_version`, `missing_files`
  ordering, the `manifest_schema`, and the tri-state `has_hashes_for_existing_files`
  (`true` with files, `null` with none). A from-memory agent cannot reproduce these
  exact hashes, so the cases now measure the skill's real output rather than generic
  domain knowledge.
- Fixtures: added committed `evals/files/` inputs (`in.lammps`, `data.lmp`,
  `log.lammps`, `POSCAR`, `OUTCAR`) so the hash checks are reproducible.

## 1.1.0 - 2026-06-23

- Docs: rewrote the "Script Outputs" section to show the real `--json` envelope
  (`inputs` + `results.manifest.<field>`) instead of a misleading flat list, and noted
  that `--out` writes only the bare manifest object (F3).
- Script: `fair_checks.has_hashes_for_existing_files` is now tri-state — it emits `null`
  when there are no existing files (check not applicable) instead of a vacuously `true`
  value (F4).
- Security/hardening: added an entry-count cap (max 1000 input/output/unit entries) and a
  per-field length cap (max 4096 characters); both raise exit code 2. Documented these
  alongside the existing control-character and 500 MB file-size limits.
- Docs: corrected the "Error Handling" and "Security" wording to describe the tool's
  actual path handling — arbitrary and absolute paths are inventoried by design, and
  `--out` is not sandboxed to the working directory (F1, F2).
- Tests: added `tests/unit/test_fair_packager.py` with regression coverage for the
  tri-state FAIR check and the new input caps.

## 1.0.0 - 2026-05-18

- Initial FAIR simulation packaging skill.

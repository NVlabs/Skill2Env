---
name: workflow-engine-mapper
description: >
  Map computational materials tasks onto workflow engines such as atomate2,
  jobflow, AiiDA, pyiron, or a simple one-off script. Use when deciding how to
  structure a reproducible campaign, DAG, restart strategy, provenance record,
  storage layout, or migration path from ad hoc scripts to managed workflows.
allowed-tools: Read, Bash, Write, Grep, Glob
metadata:
  author: HeshamFS
  version: "1.2.2"
  security_tier: high
  security_reviewed: true
  tested_with:
    - claude-code
  last_evaluated: "2026-06-23"
  eval_cases: 3
  last_reviewed: "2026-06-24"
  standards:
    - "Ganose et al. (2025), atomate2: high-throughput workflows"
    - "Rosen et al. (2024), jobflow workflow library"
    - "Huber et al. (2020), AiiDA 1.0 provenance/workflow framework"
    - "Janssen et al. (2019), pyiron integrated development environment"
    - "Jain et al. (2013), The Materials Project / input sets"
---

# Workflow Engine Mapper

## Goal

Choose the smallest workflow structure that preserves reproducibility, restartability, and provenance for a materials simulation task.

## Requirements

- Python 3.10+
- No external dependencies
- Works on Linux, macOS, and Windows

## Inputs to Gather

| Input | Description | Example |
|-------|-------------|---------|
| Task | Workflow purpose | `VASP relax-static-DOS for 200 structures` |
| Code | Main simulation engine | `vasp`, `qe`, `lammps`, `ase` |
| Runs | Approximate number of calculations | `200` |
| Provenance | Whether audit trail matters | `true` |
| Restart | Whether jobs may resume after failure | `true` |
| HPC | Whether remote scheduler is required | `true` |

## Decision Guidance

- Use **one-off scripts** for fewer than 5 local exploratory runs (no provenance, no HPC).
- Use **jobflow/atomate2** when the workflow is Python-native and Materials Project style input sets are useful.
- Use **AiiDA** when provenance-critical work is also remote (HPC) or large (>= 50 runs) — i.e. long-lived, database-backed campaigns. For smaller local provenance needs, atomate2 (Materials Project codes, >= 10 runs) or jobflow stores already capture inputs, outputs, code version, and environment, so the mapper recommends those instead of the heavier AiiDA stack.
- Use **pyiron** when interactive atomistic workflows, notebooks, and job management are the primary user surface (ASE/LAMMPS without strict provenance).

The recommendations are emitted in a fixed precedence so the prose and the implemented thresholds agree: an explicit `--preferred` engine overrides everything; otherwise one-off (small local, no provenance/HPC) -> AiiDA (provenance AND remote/large) -> atomate2 (VASP/QE/CP2K/force-field, >= 10 runs) -> pyiron (ASE/LAMMPS, no provenance) -> jobflow (fallback).

## Script Outputs

`scripts/workflow_engine_mapper.py` emits:

- `recommended_engine`
- `dag_pattern`
- `provenance_requirements`
- `restart_strategy`
- `storage_layout`
- `migration_triggers`
- `notes`

## Workflow

```bash
python3 skills/simulation-workflow/workflow-engine-mapper/scripts/workflow_engine_mapper.py \
  --task "relax static dos for 200 oxides" \
  --code vasp \
  --runs 200 \
  --needs-provenance \
  --needs-restart \
  --hpc \
  --json
```

Use the output to scaffold the workflow before writing engine-specific code.

## Error Handling

If the task has too few details, choose the conservative pattern and ask for engine, run count, and restart needs before implementation.

## Limitations

The skill does not replace the official APIs of atomate2, jobflow, AiiDA, or pyiron; it selects and explains the workflow shape.

## Verification checklist

- [ ] Recorded the full `--json` payload from `workflow_engine_mapper.py` (including `inputs`) and confirmed the echoed `runs`, `code`, `needs_provenance`, `needs_restart`, and `hpc` match the task you actually intend, not a guessed default.
- [ ] Confirmed `recommended_engine` follows the documented precedence for these inputs: `--preferred` override -> one-off (`runs<5`, no provenance, no HPC) -> aiida (provenance AND (`hpc` or `runs>=50`)) -> atomate2 (`code` in vasp/qe/cp2k/forcefield AND `runs>=10`) -> pyiron (ase/lammps, no provenance) -> jobflow fallback; if the result surprises you, re-check which branch the inputs hit rather than overriding blindly.
- [ ] Verified `dag_pattern` reflects the task keywords: branch terms (`dos`/`band`/`phonon`/`static`) and sweep terms (`screen`/`sweep`/`campaign`/`many`/`batch`) compose into the map+branch pattern, and `with restart checkpoints` is appended only when `--needs-restart` was passed.
- [ ] Checked `provenance_requirements` and `restart_strategy` against intent: `store_code_version`/`store_environment`, `checkpoint_jobs` (also auto-true at `runs>=20`), and `resume_by_job_id_or_name` (false for one-off) are consistent with how the campaign will actually be audited and resumed.
- [ ] Read `migration_triggers`; for a one-off recommendation, confirmed the forward-looking "migrate once results are compared/published/screened/resumed or runs reach ~5+" entry is present and planned for, rather than treating one-off as permanent.
- [ ] Used `storage_layout` (`inputs/`, `runs/<job-id>/`, `outputs/`, `metadata/workflow.json`, `reports/`) as the on-disk scaffold and confirmed it maps onto the chosen engine's native store before writing engine-specific code.
- [ ] Confirmed the mapper exit code was `0` (a `2` means input validation rejected the args and no recommendation was produced) before trusting any output.

## Common pitfalls & rationalizations

| Tempting shortcut | Why it's wrong / what to do |
|-------------------|-----------------------------|
| "It's only a few runs now, so a one-off script is fine forever." | The mapper emits a `migration_triggers` entry precisely because one-off is exploratory-only; once results are compared, published, screened, or resumed (or runs reach ~5+), promote to an engine. Treat one-off as a starting point, not a destination. |
| "I need provenance, so the answer must be AiiDA." | AiiDA is gated on provenance AND (HPC or `runs>=50`). For smaller/local provenance needs the mapper deliberately picks atomate2 or jobflow, whose stores already capture inputs, outputs, code version, and environment. Do not reach for the heavier stack when the lighter store suffices. |
| "The engine ran and printed a recommendation, so the inputs were right." | The script validates bounds, not intent. A forgotten `--needs-provenance` or `--hpc` flag, or a defaulted `--code general`, silently changes the branch taken. Re-read the echoed `inputs` block in the JSON and confirm each flag matches the real task. |
| "It's a screening campaign, so the DAG is just a map over structures." | If the task also names a property (dos/band/phonon/static), the correct pattern composes both: `map over structures -> (relax -> static -> property branches) -> collect -> rank`. Check that branch and sweep keywords both surfaced in `dag_pattern`. |
| "Restart isn't critical, so I can skip checkpointing." | `checkpoint_jobs` is also forced true at `runs>=20` independent of `--needs-restart`, because large sweeps fail partway. Honor the emitted `restart_strategy` rather than your gut feel about restart importance. |
| "The recommended engine doesn't match what I'd have picked, so I'll just use `--preferred`." | `--preferred` overrides everything before any heuristic runs, so it can mask a genuine mismatch in your inputs. First confirm `runs`/`code`/provenance/HPC are stated correctly; only override when you have a specific reason, and record it. |

## Security

### Input Validation

- The script accepts only scalar CLI inputs and boolean flags (`--needs-provenance`, `--needs-restart`, `--hpc`, `--json` via `store_true`).
- `runs` must be a positive integer (rejects booleans, non-integers, and values `<= 0`) and is capped at `MAX_RUNS = 1,000,000`; `main()` also rejects non-finite values via `math.isfinite`.
- Free-text fields are length-bounded: `task` <= 2000 characters (`MAX_TASK_LEN`) and must be non-empty after stripping; `code` and `preferred` <= 100 characters each (`MAX_FIELD_LEN`).
- `preferred` must be one of the allowed engine names: `auto`, `one-off`, `jobflow`, `atomate2`, `aiida`, `pyiron`.
- The `task` and `code` strings are not otherwise restricted by an allowlist; only their length and (for `task`) emptiness are validated.
- All invalid input raises `ValueError`, which is printed to stderr and exits with code 2 before any recommendation is computed.

### File Access

- The script reads and writes no files; all I/O is CLI args in -> stdout (JSON or two summary lines) out.
- It accepts no path arguments, so there is no path-sandboxing concern; there are no on-disk size limits because nothing is read from disk.

### Tool Restrictions

- The frontmatter declares `allowed-tools: Read, Bash, Write, Grep, Glob`.
- `Bash` is used only to run the bundled `scripts/workflow_engine_mapper.py`.
- `Read`/`Grep`/`Glob` are used to inspect the skill's own files and references (e.g. `references/workflow_engines.md`) and the user's task context; `Write` is available to scaffold workflow files from the recommended structure.

### Safety Measures

- No `eval`/`exec`, no `subprocess`, and no shell invocation inside the script.
- No network access: it does not connect to remote services, submit jobs, or deserialize untrusted data.
- Output is emitted as structured JSON via `json.dumps` (with `--json`) or plain text summary lines.
- DoS caps bound resource use: the `runs` ceiling (1,000,000) and the `task`/`code`/`preferred` length caps prevent unbounded input.

## References

- See `references/workflow_engines.md` for engine selection heuristics.

## Version History

- 1.2.2: Add a Verification checklist (evidence tied to the mapper's JSON outputs, precedence, DAG composition, and exit code) and a Common pitfalls & rationalizations table covering one-off permanence, AiiDA over-selection, unread input flags, and forced checkpointing.
- 1.2.0: Strengthen evals with deterministic `script_checks` that pin the mapper's exact output (recommended_engine, dag_pattern, provenance_requirements, restart_strategy, migration_triggers) so each case discriminates the skill from a from-memory baseline.
- 1.1.0: Compose branch+sweep DAG patterns instead of overwriting; emit a forward-looking migration trigger for one-off runs; document AiiDA gating/precedence; add input-validation safeguards (bounds, length caps) matching the Security section.
- 1.0.0: Initial workflow engine mapping skill.

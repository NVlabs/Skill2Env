---
name: simulation-failure-triage
description: >
  First-response triage for cross-code (LAMMPS/VASP/QE/MOOSE) simulation
  failures: classifies the failure signature (nonconvergence, NaN/Inf,
  exploding energy, unstable timestep, pressure blow-up, missing
  potentials/pseudopotentials, memory exhaustion, process crash/segfault,
  corrupted output, incomplete runs) and proposes a SAFE one-change-at-a-time
  RETRY LADDER with explicit STOP CONDITIONS, prioritizing evidence
  preservation. Use as the immediate first response to a failed or suspicious
  run. For deep per-stage validation, conservation/physical-bounds checks, and
  "can I trust these results" analysis, defer to the simulation-validator skill.
allowed-tools: Read, Bash, Write, Grep, Glob
metadata:
  author: HeshamFS
  standards:
    - "SchedMD Slurm sbatch specification (--mem / --mem-per-cpu memory request flags)"
    - "POSIX signal semantics (SIGSEGV / signal 11, core dump) for crash classification"
    - "GNU GDB, Valgrind, and AddressSanitizer (ASan) memory-fault debugging tools"
    - "LAMMPS / VASP / Quantum ESPRESSO / MOOSE solver error diagnostics (e.g. 'Lost atoms', ZBRENT nonconvergence)"
    - "Zeller (2009), Why Programs Fail: delta debugging / one-change-at-a-time minimal reproducing case"
  version: "1.1.3"
  security_tier: high
  security_reviewed: true
  tested_with:
    - claude-code
  last_evaluated: "2026-06-23"
  eval_cases: 3
  last_reviewed: "2026-06-24"
---

# Simulation Failure Triage

## Goal

Classify common simulation failure signatures and return immediate actions, retry ladders, and stop conditions.

## Requirements

- Python 3.10+
- No external dependencies
- Works on Linux, macOS, and Windows

## Inputs to Gather

| Input | Description | Example |
|-------|-------------|---------|
| Code | Simulation code | `LAMMPS`, `VASP`, `MOOSE`, `QE` |
| Stage | Setup, runtime, postprocess | `runtime` |
| Symptoms | Failure signs | `nan,pressure-blowup` |
| Log text or file | Error evidence | `Lost atoms`, `ZBRENT` |
| Recent change | Last modified setting | `larger timestep` |

## Decision Guidance

- First preserve evidence: logs, inputs, executable version, and scheduler output.
- Separate setup errors from numerical instability and physical model issues.
- Retry with a single controlled change.
- Stop retrying when the result becomes scientifically meaningless or a required model input is missing.

## Script Outputs

`scripts/failure_triage.py` emits:

- `likely_causes`
- `immediate_actions`
- `retry_ladder`
- `stop_conditions`
- `evidence`

## Workflow

```bash
python3 skills/robustness/simulation-failure-triage/scripts/failure_triage.py \
  --code LAMMPS \
  --stage runtime \
  --symptoms nan,pressure-blowup \
  --recent-change "increased timestep" \
  --json
```

## Error Handling

Invalid stages or oversized log files stop with exit code 2. Unknown symptoms are retained as custom evidence.

## Limitations

This skill gives first-response triage. It does not guarantee that a failed simulation can be repaired.

## Verification checklist

- [ ] Recorded the preserved-evidence set BEFORE any rerun: copied logs, input decks, scheduler output, and the executable/version string (per the first `immediate_actions` item) so the original failure is reproducible.
- [ ] Quoted the FIRST warning/error from the run, not just the final crash line, and confirmed `evidence.log_excerpt` (first 500 chars, original casing) captures it; re-run with `--log-file`/`--log-text` if the excerpt misses the root signature.
- [ ] Logged every `likely_causes` entry with its `symptom`, `category`, and `first_action`, and verified no real signature landed in the `category: custom` bucket because its keyword was absent from `LOG_HINTS`/`PATTERNS`.
- [ ] Confirmed the failure category is correct rather than mislabeled: a segfault/SIGSEGV/signal 11/core-dumped maps to `crash` (not `corrupted-output`), and an OOM/`bad_alloc`/`oom-kill` maps to `out-of-memory` (not `incomplete-run`).
- [ ] Applied the `retry_ladder` strictly one change at a time, recording the single parameter changed and its effect at each rung (including the memory rung when memory-bound).
- [ ] Checked every `stop_conditions` entry and halted the retry loop instead of stacking arbitrary stabilizing tweaks when any condition is met (e.g. unverifiable potential/pseudopotential, results dependent on arbitrary stabilizers).
- [ ] After any numerical recovery, handed off to the `simulation-validator` skill for conservation / physical-bounds / "can I trust these results" checks rather than declaring success here.

## Common pitfalls & rationalizations

| Tempting shortcut | Why it's wrong / what to do |
|-------------------|-----------------------------|
| "The last line of the log is the error, so I'll fix that." | The final crash line is often a downstream symptom; the script's second `immediate_actions` item exists because the FIRST warning/error is the real cause. Capture it in `evidence.log_excerpt` and triage from there. |
| "It segfaulted, so it's a corrupted-output / disk issue." | A `crash` (SIGSEGV/signal 11/core dumped) is a memory-fault category pointing at out-of-bounds/null-pointer/ABI bugs and a gdb/valgrind/ASan repro — not I/O. Do not treat it as `corrupted-output`. |
| "The job got killed, so I'll just bump the walltime." | `killed` alone is genuinely ambiguous and stays `incomplete-run`; an OOM signature (`bad_alloc`, `oom-kill`, "out of memory") is a distinct `out-of-memory` cause needing memory reduction / `--mem` increase, not more walltime. |
| "I'll lower dt AND change the preconditioner AND adjust the barostat to get it running." | The retry ladder is one controlled change per rung; stacking fixes makes results "depend on arbitrary stabilizing changes" — an explicit `stop_conditions` trigger. Change one parameter, record its effect, then proceed. |
| "I added the missing PAIR coeff path and it ran, so the physics is fine." | A clean run after fixing `missing-potential`/`bad-pseudopotential` resolves setup, not validity; species mapping, valence, or functional may still be wrong. Run completion is not correctness. |
| "It runs now, triage is done." | Triage only restores execution. Conservation, physical bounds, and convergence are out of scope here — defer to `simulation-validator` before trusting any number. |

## Security

### Input Validation

- `--stage` is checked against a fixed allowlist (`setup`, `runtime`, `postprocess`, `unknown`); any other value exits with code 2.
- `--code` must be non-empty and at most 100 characters; an empty or oversized value exits with code 2.
- `--symptoms` are split on commas and capped at 50 entries, each at most 100 characters; exceeding either limit exits with code 2.
- Unknown symptoms are not rejected; they are retained as `custom` evidence rather than silently dropped.
- There are no numeric arguments, so no finite/positive checks apply.
- All input-validation failures (and log read errors) are caught and exit with code 2 and a stderr message.

### File Access

- The only file read is the optional `--log-file` path; when omitted, the script reads no files.
- Before reading, the log file's size is checked via `stat`; if it exceeds the 10 MB cap (`MAX_LOG_SIZE`) the script raises and exits with code 2. Both file content and `--log-text` are then truncated to 10 MB.
- The script writes no files; all results go to stdout (JSON with `--json`, otherwise plain text).
- Path-sandboxing caveat: the log path is not restricted to a working directory, so the script can read any file the invoking process has permission to read; only pass trusted paths.

### Tool Restrictions

- `allowed-tools` is `Read, Bash, Write, Grep, Glob`.
- `Bash` runs only the bundled `scripts/failure_triage.py`.
- `Read` opens the skill's own files and a user-provided log to inspect failure evidence; `Grep`/`Glob` locate log files, inputs, and prior output; `Write` records triage notes or preserved evidence at the user's direction. The bundled script itself does not write files.

### Safety Measures

- No `eval`/`exec` and no dynamic code execution; log text is treated as data and never run.
- The script spawns no subprocesses and runs no external solvers.
- Output is structured JSON (`--json`), making results machine-checkable.
- DoS caps bound resource use: 10 MB log size/text limit, 50 symptoms, and 100-character limits on `code` and each symptom.

## References

- See `references/failure_patterns.md` for common failure signatures and retry ladders.

## Version History

- 1.1.3: Add `Verification checklist` (evidence-based checks tied to `failure_triage.py` outputs — preserved-evidence set, first-error excerpt, category-mislabel guards, one-change retry ladder, stop conditions, simulation-validator handoff) and `Common pitfalls & rationalizations` table covering last-line-only triage, segfault-as-I/O, OOM-vs-walltime, stacked stabilizing changes, and "it ran so it's valid".
- 1.1.1: Strengthen evals to be discriminating — each case now pins the exact `failure_triage.py` JSON output via `script_checks` (specific `category`/`first_action` strings, log-hint symptom inference, fixed retry-ladder/stop-condition text, recent-change immediate action), so the suite measures the skill's actual output rather than generic triage knowledge.
- 1.1.0: Add dedicated `out-of-memory` and `crash` (segfault) classifications; segfaults and OOM are no longer mislabeled as I/O or interrupted-execution. Preserve original-case log excerpt. Add input-validation caps (symptoms, code length). Sharpen description to defer deep validation to simulation-validator. Fix `missing-potential` eval token.
- 1.0.0: Initial cross-code simulation failure triage skill.

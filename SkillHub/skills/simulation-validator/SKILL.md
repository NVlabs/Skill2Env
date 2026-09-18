---
name: simulation-validator
description: >
  Validate simulations across three stages — run pre-flight checks on
  configuration files (parameter ranges, required fields, disk space),
  monitor runtime logs for residual growth, NaN/Inf, and adaptive dt
  collapse, and perform post-flight validation of results (physical bounds,
  mass/energy conservation, convergence). Diagnose failed simulations with
  probable-cause analysis and recommended fixes. Use when preparing to
  launch a simulation, checking whether a running job is healthy, verifying
  that finished results are trustworthy, or debugging a crash or blow-up,
  even if the user only says "my simulation crashed" or "can I trust
  these results."
allowed-tools: Read, Bash, Write, Grep, Glob
metadata:
  author: HeshamFS
  version: "1.2.2"
  security_tier: high
  security_reviewed: true
  tested_with:
    - claude-code
  last_evaluated: "2026-06-24"
  eval_cases: 5
  last_reviewed: "2026-06-23"
  standards:
    - "Courant-Friedrichs-Lewy (CFL) stability condition (Courant, Friedrichs & Lewy, 1928)"
    - "von Neumann stability analysis (diffusion-Fourier number limit dt <= dx^2/(2*D*dim))"
    - "IEEE 754 floating-point arithmetic (NaN / Inf / overflow detection)"
    - "Variational / gradient-flow energy dissipation for Allen-Cahn and Cahn-Hilliard phase-field models"
    - "Conservation laws (mass / energy / momentum drift checks)"
---

# Simulation Validator

## Goal

Provide a three-stage validation protocol: pre-flight checks, runtime monitoring, and post-flight validation for materials simulations.

## Requirements

- Python 3.10+
- No external dependencies (uses Python standard library only)
- Works on Linux, macOS, and Windows

## Inputs to Gather

Before running validation scripts, collect from the user:

| Input | Description | Example |
|-------|-------------|---------|
| Config file | Simulation configuration (JSON/YAML) | `simulation.json` |
| Log file | Runtime output log | `simulation.log` |
| Metrics file | Post-run metrics (JSON) | `results.json` |
| Required params | Parameters that must exist | `dt,dx,kappa` |
| Valid ranges | Parameter bounds | `dt:1e-6:1e-2` |

## Decision Guidance

### When to Run Each Stage

```
Is simulation about to start?
├── YES → Run Stage 1: preflight_checker.py
│         └── BLOCK status? → Fix issues, do NOT run simulation
│         └── WARN status? → Review warnings, document if accepted
│         └── PASS status? → Proceed to run simulation
│
Is simulation running?
├── YES → Run Stage 2: runtime_monitor.py (periodically)
│         └── Alerts? → Consider stopping, check parameters
│
Has simulation finished?
├── YES → Run Stage 3: result_validator.py
│         └── Failed checks? → Do NOT use results
│                            → Run failure_diagnoser.py
│         └── All passed? → Results are valid
```

### Choosing Validation Thresholds

| Metric | Conservative | Standard | Relaxed |
|--------|--------------|----------|---------|
| Mass tolerance | 1e-6 | 1e-3 | 1e-2 |
| Residual growth | 2x | 10x | 100x |
| dt reduction | 10x | 100x | 1000x |

## Script Outputs (JSON Fields)

| Script | Output Fields |
|--------|---------------|
| `scripts/preflight_checker.py` | `report.status`, `report.blockers`, `report.warnings` |
| `scripts/runtime_monitor.py` | `alerts`, `residual_stats`, `dt_stats` (alerts include NaN/Inf/overflow detection, residual growth, and dt collapse) |
| `scripts/result_validator.py` | `checks`, `confidence_score`, `failed_checks`, `status` (`PASS` / `FAIL` / `INSUFFICIENT_DATA`); `confidence_score` is `null` when no check ran |
| `scripts/failure_diagnoser.py` | `probable_causes`, `recommended_fixes` |

## Three-Stage Validation Protocol

### Stage 1: Pre-flight (Before Simulation)

1. Run `scripts/preflight_checker.py --config simulation.json`
2. **BLOCK status**: Stop immediately, fix all blocker issues
3. **WARN status**: Review warnings, document accepted risks
4. **PASS status**: Proceed to simulation

> Note: `preflight_checker.py` validates required keys, numeric ranges,
> output-directory access, and disk space. It does **not** evaluate numerical
> stability (CFL / diffusion-Fourier). For explicit stability gating use
> `skills/core-numerical/numerical-stability/scripts/cfl_checker.py`.

```bash
python3 scripts/preflight_checker.py \
    --config simulation.json \
    --required dt,dx,kappa \
    --ranges "dt:1e-6:1e-2,dx:1e-4:1e-1" \
    --min-free-gb 1.0 \
    --json
```

### Stage 2: Runtime (During Simulation)

1. Run `scripts/runtime_monitor.py --log simulation.log` periodically
2. Configure alert thresholds based on problem type
3. Stop simulation if critical alerts appear

```bash
python3 scripts/runtime_monitor.py \
    --log simulation.log \
    --residual-growth 10.0 \
    --dt-drop 100.0 \
    --json
```

### Stage 3: Post-flight (After Simulation)

1. Run `scripts/result_validator.py --metrics results.json`
2. **All checks PASS**: Results are valid for analysis
3. **Any check FAIL**: Do NOT use results, diagnose failure

```bash
python3 scripts/result_validator.py \
    --metrics results.json \
    --bound-min 0.0 \
    --bound-max 1.0 \
    --mass-tol 1e-3 \
    --json
```

For variational / gradient-flow models (Allen-Cahn, Cahn-Hilliard), add
`--variational` to enforce a strict monotone non-increasing energy check.

### Failure Diagnosis

When validation fails:

```bash
python3 scripts/failure_diagnoser.py --log simulation.log --json
```

## Conversational Workflow Example

**User**: My phase field simulation crashed after 1000 steps. Can you help me figure out why?

**Agent workflow**:
1. First, check the log for obvious errors:
   ```bash
   python3 scripts/failure_diagnoser.py --log simulation.log --json
   ```
2. If diagnosis suggests numerical blow-up, check runtime stats:
   ```bash
   python3 scripts/runtime_monitor.py --log simulation.log --json
   ```
3. Recommend fixes based on findings:
   - If residual grew rapidly → reduce time step
   - If dt collapsed → check stability conditions
   - If NaN detected → check initial conditions

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| `Config not found` | File path invalid | Verify config path exists |
| `Non-numeric value` | Parameter is not a number | Fix config file format |
| `out of range` | Parameter outside bounds | Adjust parameter or bounds |
| `Output directory not writable` | Permission issue | Check directory permissions |
| `Insufficient disk space at <path>` | Disk nearly full on the output volume | Free up space or reduce output |
| `Invalid parameter name` | `--required` name has disallowed characters | Use only letters, digits, `_`, `.`, `-` |
| `range max ... must be greater than min` | Inverted/degenerate `--ranges` or bounds | Ensure max > min |
| `must be a finite positive number` | `nan`/`inf`/negative threshold supplied | Pass a finite positive value |
| `Log file too large` | Log exceeds the 500 MB parse cap | Truncate or pre-filter the log |

## Interpretation Guidance

### Status Meanings

| Status | Meaning | Action |
|--------|---------|--------|
| PASS | All checks passed | Proceed with confidence |
| WARN | Non-critical issues found | Review and document |
| BLOCK | Critical issues found | Must fix before proceeding |

### Confidence Score Interpretation

| Score | Meaning |
|-------|---------|
| 1.0 | All validation checks passed → proceed with confidence |
| 0.75+ | Most checks passed, minor issues |
| 0.5-0.75 | Significant issues, review carefully |
| < 0.5 | Major problems, do not trust results |
| `null` (status `INSUFFICIENT_DATA`) | No recognized metrics fields; **no check ran** — NOT a pass. Inspect the metrics file. |

A requested bound (`--bound-min`/`--bound-max`) with no matching `field_min`/`field_max`
in the metrics is reported as a failed `bounds_unverifiable` check, never a vacuous pass.
For variational/gradient-flow runs, pass `--variational` (or set `"energy_variational": true`
in the metrics) to enforce a strict monotone non-increasing energy check (`energy_monotone`);
otherwise a weaker `energy_net_decrease` check is used, which does not detect mid-run spikes.

### Common Failure Patterns

| Pattern in Log | Likely Cause | Recommended Fix |
|----------------|--------------|-----------------|
| NaN, Inf, overflow | Numerical instability | Reduce dt, increase damping |
| max iterations, did not converge | Solver failure | Tune preconditioner, tolerances |
| out of memory | Memory exhaustion | Reduce mesh, enable out-of-core |
| dt reduced | Adaptive stepping triggered | May be okay if controlled |

## Verification checklist

Do not trust a validation verdict until each applicable item below is satisfied
with the concrete artifact named. Record these in your summary to the user.

- [ ] Ran `result_validator.py --json` and confirmed `results.status` is `PASS` (not `INSUFFICIENT_DATA`) AND `results.confidence_score == 1.0`; a `null` score or `INSUFFICIENT_DATA` means no check ran — treat as unverified, not as a pass.
- [ ] Listed `results.checks` and confirmed every requested check actually appears (e.g. `mass_conserved`, `bounds_satisfied`, `no_nan`, and `energy_monotone`/`energy_net_decrease`); confirmed `results.failed_checks` is empty and contains no `bounds_unverifiable` entry (which means a requested bound had no `field_min`/`field_max` to compare against).
- [ ] For variational/gradient-flow models (Allen-Cahn, Cahn-Hilliard), passed `--variational` (or set `"energy_variational": true`) so `energy_monotone` is enforced; recorded that the weaker `energy_net_decrease` was NOT relied on, since it cannot detect mid-run energy spikes.
- [ ] Recorded the mass drift tolerance used (`--mass-tol`, default `1e-3`) and confirmed it matches the Conservative/Standard/Relaxed column appropriate to the run; did not silently accept the default for a tight-conservation problem.
- [ ] Ran `runtime_monitor.py --json` and recorded `residual_stats` (min/max/last) and `dt_stats`; confirmed there are no `alerts` for NaN/Inf/overflow, residual growth above `--residual-growth`, or dt collapse below `--dt-drop`.
- [ ] Confirmed numerical stability was gated separately via `core-numerical/numerical-stability/scripts/cfl_checker.py` (CFL/Fourier limit) — `preflight_checker.py` does NOT evaluate CFL/Fourier and a PASS preflight says nothing about temporal/spatial stability.
- [ ] On any `FAIL` or alert, ran `failure_diagnoser.py --json` and recorded the `probable_causes`/`recommended_fixes`, rather than reusing the results.

## Common pitfalls & rationalizations

| Tempting shortcut | Why it's wrong / what to do |
|-------------------|------------------------------|
| "Preflight passed, so the run is numerically stable." | `preflight_checker.py` checks required keys, ranges, output-dir writability, and disk space only. It does NOT compute CFL/Fourier. Gate stability with `cfl_checker.py` separately. |
| "`result_validator` printed a confidence score, so results are good." | An empty or unrecognized metrics file returns `confidence_score: null` and status `INSUFFICIENT_DATA` — that is "no check ran", not a pass. Verify recognized fields are present and `status == PASS`. |
| "Energy ends lower than it started, so the dissipative run is fine." | The default `energy_net_decrease` only compares first vs last and misses mid-run spikes. For gradient-flow models use `--variational` to enforce the strict monotone `energy_monotone` check. |
| "I asked for bounds and didn't get a `bounds_satisfied: false`, so bounds hold." | If `field_min`/`field_max` are absent the validator emits `bounds_unverifiable` (a FAILED check), never a vacuous pass. Ensure the metrics file actually carries the field extrema. |
| "The simulation finished without crashing, so the results are trustworthy." | Run completion is not correctness. Verify mass conservation, energy behavior, physical bounds, and a clean `runtime_monitor` alert list before using results. |
| "dt got smaller during the run, so the solver is failing." | `runtime_monitor` dt-collapse is direction-aware (running-max vs current) and only alerts past `--dt-drop`; a controlled adaptive ramp is expected. Check the actual `dt_stats` and whether an alert fired. |
| "I'll just use the default thresholds." | Defaults (`--mass-tol 1e-3`, `--residual-growth 10`, `--dt-drop 100`) are the Standard column; a conservation-critical problem needs the Conservative tolerances. Pick thresholds for the physics, then record them. |

## Security

### Input Validation
- Config file paths are validated for existence before parsing; non-existent paths produce clear errors (exit code 2)
- `--required` parameter names are validated against a safe-character allowlist (`^[A-Za-z0-9_.-]+$`); names with shell metacharacters are rejected
- `--ranges` entries are parsed as `name:min:max` with finite numeric bounds enforced and `max > min` required
- `--min-free-gb` is validated as a finite positive number (negatives, zero, `nan`, `inf` rejected)
- `--residual-growth` and `--dt-drop` thresholds are validated as finite positive numbers
- `--bound-min` and `--bound-max` are validated as finite numbers (`nan`/`inf` rejected), and `--bound-max > --bound-min` is enforced; `--mass-tol` is validated as a finite positive number
- Invalid input exits with code 2 and an explanatory message

### File Access
- `preflight_checker.py` reads a single user-specified config file (JSON/YAML) and checks disk space on the volume hosting the resolved output directory
- `runtime_monitor.py` reads a single log file specified by `--log`; log files are size-limited (500 MB max) and rejected before parsing if larger
- `result_validator.py` reads a single metrics file (JSON) specified by `--metrics`
- `failure_diagnoser.py` reads a single log file specified by `--log`; log files are size-limited (500 MB max) before parsing
- No scripts write to the filesystem; all output goes to stdout

### Tool Restrictions
- **Read**: Used to inspect script source, references, config files, and simulation logs
- **Bash**: Used to execute the four Python validation scripts (`preflight_checker.py`, `runtime_monitor.py`, `result_validator.py`, `failure_diagnoser.py`) with explicit argument lists
- **Write**: Used to save validation reports; writes are scoped to the user's working directory
- **Grep/Glob**: Used to locate log files, config files, and search references

### Safety Measures
- No `eval()`, `exec()`, or dynamic code generation
- All subprocess calls use explicit argument lists (no `shell=True`)
- `failure_diagnoser.py` uses hardcoded, pre-compiled diagnostic regex patterns; `runtime_monitor.py` accepts optional `--residual-pattern` / `--dt-pattern` overrides that are compiled with `re.compile` (no `eval`) and applied only to the user's own log
- Diagnostic strings emitted in output are drawn from the skill's fixed cause/fix table, not interpolated from raw log content

## Limitations

- **Not a real-time monitor**: Scripts analyze logs after-the-fact
- **Regex-based**: Log parsing depends on pattern matching; may miss unusual formats
- **No automatic fixes**: Scripts diagnose but don't modify simulations

## References

- `references/validation_protocol.md` - Detailed checklist and criteria
- `references/log_patterns.md` - Common failure signatures and regex patterns

## Version History

- **v1.2.2** (2026-06-24): Added a Verification checklist (evidence-based, tied to the four scripts' JSON outputs) and a Common pitfalls & rationalizations table to harden agent interpretation of validation verdicts.
- **v1.2.0** (2026-06-23): Corrected diagnostic regexes (no false convergence/blow-up on healthy logs), direction-aware dt-collapse detection, NaN/Inf scan in runtime monitor, strict variational energy check, non-vacuous bounds/confidence, config-relative output-dir + correct-volume disk check, and implemented the documented input-validation/file-size safeguards
- **v1.1.0** (2024-12-24): Enhanced documentation, decision guidance, Windows compatibility
- **v1.0.0**: Initial release with 4 validation scripts

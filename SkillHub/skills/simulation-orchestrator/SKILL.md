---
name: simulation-orchestrator
description: >
  Orchestrate multi-simulation campaigns — generate parameter sweep
  configurations (grid, linspace, or Latin Hypercube sampling), initialize
  and track batch job campaigns, monitor job completion status, and aggregate
  results with summary statistics across all runs. Use when running a
  parameter study across dt, kappa, or other simulation inputs, managing
  dozens or hundreds of simulation configurations, combining outputs from
  completed batch runs to find the best result, or automating the
  generate-run-collect workflow for systematic studies, even if the user
  only says "I need to try many parameter combinations" or "how do I
  organize a sweep."
allowed-tools: Read, Write, Grep, Glob
metadata:
  author: HeshamFS
  version: "1.1.3"
  security_tier: medium
  security_reviewed: true
  tested_with:
    - claude-code
  last_evaluated: "2026-06-24"
  eval_cases: 5
  last_reviewed: "2026-06-23"
  standards:
    - "Latin Hypercube Sampling (McKay, Beckman & Conover 1979)"
    - "Full factorial / grid Design of Experiments (DOE)"
    - "Sobol (2001) variance-based global sensitivity indices"
    - "Morris (1991) elementary-effects screening"
    - "Tukey (1977) 1.5x IQR outlier rule"
---

# Simulation Orchestrator

## Goal

Provide tools to manage multi-simulation campaigns: generate parameter sweeps, track job execution status, and aggregate results from completed runs.

## Requirements

- Python 3.10+
- No external dependencies (uses Python standard library only)
- Works on Linux, macOS, and Windows

## Inputs to Gather

Before running orchestration scripts, collect from the user:

| Input | Description | Example |
|-------|-------------|---------|
| Base config | Template simulation configuration | `base_config.json` |
| Parameter ranges | Parameters to sweep with bounds | `dt:[1e-4,1e-2],kappa:[0.1,1.0]` |
| Sweep method | How to sample parameter space | `grid`, `lhs`, `linspace` |
| Output directory | Where to store campaign files | `./campaign_001` |
| Simulation command | Command to run each simulation | `python sim.py --config {config}` |

## Decision Guidance

### Choosing a Sweep Method

```
Need every combination (full factorial)?
├── YES → Use grid (warning: exponential growth with parameters)
└── NO → Is space-filling coverage needed?
    ├── YES → Use lhs (Latin Hypercube Sampling)
    └── NO → Use linspace for uniform sampling per parameter
```

| Method | Best For | Sample Count |
|--------|----------|--------------|
| `grid` | Low dimensions (1-3), need exact corners | n^d (exponential) |
| `linspace` | 1D sweeps, uniform spacing | n per parameter |
| `lhs` | High dimensions, space-filling | user-specified budget |

### Campaign Size Guidelines

| Parameters | Grid Points Each | Total Runs | Recommendation |
|------------|------------------|------------|----------------|
| 1 | 10 | 10 | Grid is fine |
| 2 | 10 | 100 | Grid acceptable |
| 3 | 10 | 1,000 | Consider LHS |
| 4+ | 10 | 10,000+ | Use LHS or DOE |

## Script Outputs (JSON Fields)

| Script | Output Fields |
|--------|---------------|
| `scripts/sweep_generator.py` | `configs`, `parameter_space`, `sweep_method`, `total_runs` |
| `scripts/campaign_manager.py --action init` | `campaign_id`, `total_jobs`, `config_dir`, `command_template` |
| `scripts/campaign_manager.py --action status` | `campaign_id`, `status`, `jobs`, `progress`, `total_jobs`, `created_at` |
| `scripts/campaign_manager.py --action list` | `jobs` (array of job records) |
| `scripts/job_tracker.py` | `job_id`, `status`, `start_time`, `end_time`, `exit_code` |
| `scripts/result_aggregator.py` | `summary` (incl. `minimize`), `statistics`, `best_run`, `failed_runs` |

> **Note on swept parameter names**: `sweep_generator.py` writes each swept value into the base config by key path. A bare name (e.g. `kappa`) overwrites a top-level key; a dot-notation name (e.g. `parameters.kappa`) targets a nested key. The swept key path must match where the solver reads the value — sweeping `kappa` against a config that nests `parameters.kappa` would add an unused top-level key and silently leave the base value in place. See `references/sweep_strategies.md`.

## Workflow

### Step 1: Generate Parameter Sweep

Create configurations for all parameter combinations:

```bash
python3 scripts/sweep_generator.py \
    --base-config base_config.json \
    --params "dt:1e-4:1e-2:5,kappa:0.1:1.0:3" \
    --method linspace \
    --output-dir ./campaign_001 \
    --json
```

### Step 2: Initialize Campaign

Create campaign tracking structure:

```bash
python3 scripts/campaign_manager.py \
    --action init \
    --config-dir ./campaign_001 \
    --command "python sim.py --config {config}" \
    --json
```

### Step 3: Track Job Status

Monitor running jobs:

```bash
python3 scripts/job_tracker.py \
    --campaign-dir ./campaign_001 \
    --update \
    --json
```

### Step 4: Aggregate Results

Combine results from completed runs:

```bash
python3 scripts/result_aggregator.py \
    --campaign-dir ./campaign_001 \
    --metric final_energy \
    --json
```

`result_aggregator.py` **minimizes by default**: `best_run` is the run with the
**lowest** metric value (and `summary.minimize` is `true`). If higher is better
(e.g. yield, accuracy, throughput), pass `--maximize` so `best_run` becomes the
**highest** value:

```bash
# Higher is better -> select the maximum
python3 scripts/result_aggregator.py \
    --campaign-dir ./campaign_001 \
    --metric yield \
    --maximize \
    --json
```

> **Decision guidance**: If higher is better (yield, accuracy, throughput), pass
> `--maximize`; otherwise the reported `best_run` is the **minimum**.

## CLI Examples

```bash
# Generate 5x3=15 runs varying dt (5 values) and kappa (3 values)
python3 scripts/sweep_generator.py \
    --base-config sim.json \
    --params "dt:1e-4:1e-2:5,kappa:0.1:1.0:3" \
    --method linspace \
    --output-dir ./sweep_001 \
    --json

# Generate LHS samples for 4 parameters with budget of 20 runs
python3 scripts/sweep_generator.py \
    --base-config sim.json \
    --params "dt:1e-4:1e-2,kappa:0.1:1.0,M:1e-6:1e-4,W:0.5:2.0" \
    --method lhs \
    --samples 20 \
    --output-dir ./lhs_001 \
    --json

# Check campaign status
python3 scripts/campaign_manager.py \
    --action status \
    --config-dir ./sweep_001 \
    --json

# List jobs (read-only), optionally filtered by status
python3 scripts/campaign_manager.py \
    --action list \
    --config-dir ./sweep_001 \
    --status-filter failed \
    --json

# Get summary statistics from completed runs (minimize: best = lowest)
python3 scripts/result_aggregator.py \
    --campaign-dir ./sweep_001 \
    --metric final_energy \
    --json

# Maximization metric: best = highest value (yield, accuracy, throughput)
python3 scripts/result_aggregator.py \
    --campaign-dir ./sweep_001 \
    --metric yield \
    --maximize \
    --json
```

## Conversational Workflow Example

**User**: I want to run a parameter sweep on dt and kappa for my phase-field simulation. I want to try 5 values of dt between 1e-4 and 1e-2, and 4 values of kappa between 0.1 and 1.0.

**Agent workflow**:
1. Calculate total runs: 5 x 4 = 20 runs
2. Generate sweep configurations:
   ```bash
   python3 scripts/sweep_generator.py \
       --base-config simulation.json \
       --params "dt:1e-4:1e-2:5,kappa:0.1:1.0:4" \
       --method linspace \
       --output-dir ./dt_kappa_sweep \
       --json
   ```
3. Initialize campaign:
   ```bash
   python3 scripts/campaign_manager.py \
       --action init \
       --config-dir ./dt_kappa_sweep \
       --command "python phase_field.py --config {config}" \
       --json
   ```
4. After user runs simulations, aggregate results:
   ```bash
   python3 scripts/result_aggregator.py \
       --campaign-dir ./dt_kappa_sweep \
       --metric interface_width \
       --json
   ```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| `Base config not found` | Invalid file path | Verify base config file exists |
| `Invalid parameter format` | Malformed param string | Use format `name:min:max:count` or `name:min:max` |
| `Output directory exists` | Would overwrite | Use `--force` or choose new directory |
| `No completed jobs` | No results to aggregate | Wait for jobs to complete or check for failures |
| `Metric not found` | Result files missing field | Verify metric name in result JSON |

## Integration with Other Skills

The simulation-orchestrator works with other simulation-workflow skills:

```
parameter-optimization          simulation-orchestrator
        │                              │
        │ DOE samples ────────────────>│ Generate configs
        │                              │
        │                              │ Run simulations
        │                              │
        │<──────────────────────────── │ Aggregate results
        │                              │
        │ Sensitivity analysis         │
        │ Optimizer selection          │
```

### Typical Combined Workflow

1. Use `parameter-optimization/doe_generator.py` to get sample points
2. Use `simulation-orchestrator/sweep_generator.py` to create configs
3. Run simulations (user's responsibility)
4. Use `simulation-orchestrator/result_aggregator.py` to collect results
5. Use `parameter-optimization/sensitivity_summary.py` to analyze

## Verification checklist

Before trusting a campaign's `best_run` or summary statistics, record concrete evidence for each item:

- [ ] Confirmed the swept key path actually changed the value the solver reads: opened at least one generated `config_NNNN.json` and verified the swept parameter (e.g. `parameters.kappa`) holds the expected value at the expected nesting level, not a duplicate unused top-level key (`sweep_generator.py` writes by key path).
- [ ] Reconciled job accounting from `result_aggregator.py --json`: recorded `summary.total_jobs`, `summary.completed`, and `summary.failed`, and confirmed `completed + failed == total_jobs`. Any shortfall means runs were silently skipped (missing result file or `extract_metric` returned `None`) and must be investigated, not ignored.
- [ ] Confirmed `completed > 0` and that the recorded `summary.metric` matches the field the solver actually writes. A typo'd or absent metric makes `extract_metric` return `None`, yielding zero completed runs with no error.
- [ ] Recorded `summary.minimize` and confirmed it matches the intended direction (default minimize; `--maximize` for yield/accuracy/throughput) before quoting `best_run`.
- [ ] Did NOT treat `job_tracker.py` "completed" as physical success: it flags a job completed purely from a result-file's existence and stamps `exit_code` 0 — independently checked the run's real exit status / solver logs for non-zero codes or NaN/Inf output.
- [ ] Applied an outlier/sanity check to the metric values (e.g. Tukey 1.5x IQR from `references/aggregation_methods.md`) and confirmed `best_run.value` is physically plausible, not a crashed run that emitted a spurious extremum.
- [ ] For LHS sweeps, recorded the `--seed` used and saved `manifest.json` (parameter bounds, `total_runs`, `parameter_space`) so the sample set is reproducible.

## Common pitfalls & rationalizations

| Tempting shortcut | Why it's wrong / what to do |
|-------------------|------------------------------|
| "The job tracker says completed, so the run succeeded." | `job_tracker.py` marks "completed" whenever a result file *exists* and hard-codes `exit_code` 0 — it never reads the actual exit code. A crashed run that wrote a partial result file looks identical to a clean one. Check the solver's real exit status and output validity. |
| "`completed` is high, so I have all my results." | Jobs with a missing result file or a metric that `extract_metric` can't read are silently skipped — neither counted as `completed` nor `failed`. Reconcile `completed + failed` against `total_jobs`; a gap means lost runs. |
| "Aggregation returned a `best_run`, so that's the optimum." | By default the aggregator *minimizes*. If higher is better you must pass `--maximize`, or `best_run` is the worst point. Always record `summary.minimize` and confirm the direction. |
| "I swept `kappa`, so the runs vary." | `sweep_generator.py` writes by key path. If the base config nests the value under `parameters.kappa` but you sweep the bare name `kappa`, every config keeps the original nested value and gains an unused top-level key — the sweep is scientifically meaningless. Sweep the exact dotted path the solver reads. |
| "The metric name is close enough." | A misspelled or absent metric makes `extract_metric` return `None` for every run, so `completed` is 0 and statistics are empty — with no error raised. Verify the metric matches the solver's output field exactly. |
| "Grid covers everything, so use it for all my parameters." | Grid is `n^d` — it explodes exponentially (4 params x 10 = 10,000 runs). For 4+ dimensions use `lhs` with a deliberate budget; reserve grid for 1-3 parameters. |
| "LHS is random, so I don't need to record anything." | LHS is reproducible only with a fixed `--seed`. Without recording the seed (and `manifest.json`), the sample set cannot be regenerated or defended. |

## Security

### Input Validation
- Metric names (`result_aggregator.py --metric`) are validated against `[a-zA-Z_][a-zA-Z0-9_.]*` to prevent traversal or injection via crafted keys
- Swept parameter names (`sweep_generator.py --params`) are validated against `[a-zA-Z_][a-zA-Z0-9_]*(.[a-zA-Z_][a-zA-Z0-9_]*)*` (dot notation for nested keys); invalid names are rejected
- `campaign_manager.py` validates command templates to reject shell chaining operators (`;`, `|`, `&`, backticks, `$`)
- `--params` format strings are parsed and validated (`name:min:max:count` with finite numeric bounds — `NaN`/`Inf` rejected — `min < max`, and positive integer counts capped at 100,000); at most 32 parameters per sweep
- `--method` is validated against a fixed allowlist (`grid`, `linspace`, `lhs`)
- `--samples` is validated as a positive integer with an upper bound (max 1,000,000)
- `--action` is validated against a fixed allowlist (`init`, `status`, `list`); for the read-only `list` action, `--status-filter` is validated against `pending`, `running`, `completed`, `failed`

### File Access
- `sweep_generator.py` reads a single base config file (JSON) specified by `--base-config` and writes generated configs to `--output-dir`
- `result_aggregator.py` enforces a 10 MB file-size limit per result file, maximum JSON nesting depth, and strict numeric type checking (rejects `bool`, `NaN`, `Inf`)
- All string values from result files are sanitized (truncated, control characters stripped) before surfacing them
- Config paths interpolated into shell commands are validated against a safe-character allowlist and escaped with `shlex.quote()`

### Tool Restrictions
- **Read**: Used to inspect script source, references, base configs, and campaign status files
- **Write**: Used to save generated sweep configs, campaign manifests, and aggregated results; writes are scoped to the user's working directory
- **Grep/Glob**: Used to locate campaign files, result files, and search references
- The skill's `allowed-tools` excludes `Bash` to prevent the agent from executing arbitrary commands when processing untrusted simulation outputs

### Safety Measures
- No `eval()`, `exec()`, or dynamic code generation
- All subprocess calls use explicit argument lists (no `shell=True`)
- Reduced tool surface (no Bash) limits the agent to read/write operations only
- Command templates are validated but never executed by the skill itself; execution is the user's responsibility

## Limitations

- **Not a job scheduler**: Does not submit jobs to SLURM/PBS; generates configs and tracks status
- **No parallel execution**: User must run simulations externally (can use GNU parallel, SLURM, etc.)
- **File-based tracking**: Status tracked via files; no database or real-time monitoring
- **Local filesystem**: Assumes all files accessible from local machine

## References

- `references/campaign_patterns.md` - Common campaign structures
- `references/sweep_strategies.md` - Parameter sweep design guidance
- `references/aggregation_methods.md` - Result aggregation techniques

## Version History

See `CHANGELOG.md` for the authoritative, dated history. Summary:

- **v1.1.3** (2026-06-24): Added a Verification checklist and a Common pitfalls & rationalizations section grounded in the scripts' real behavior (result-file-only "completed" detection, silent skip of unreadable metrics, minimize-by-default direction, key-path merge semantics)
- **v1.1.1** (2026-06-23): Dot-notation nested overrides in `sweep_generator.py`, input-validation hardening (`--params` name/finite/count caps, `--samples` bounds), documented `--maximize` and the `list` action, corrected Script Outputs table and worked-example numbers
- **v1.1.0** (2026-03-26): Standardized metadata, evaluation suite, security review, CHANGELOG
- **v1.0.0** (2026-02-25): Initial release with sweep, campaign, tracking, and aggregation

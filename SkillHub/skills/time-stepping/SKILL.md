---
name: time-stepping
description: >
  Plan and control time-step policies for transient simulations — couple
  CFL and physics-based stability limits with adaptive stepping, ramp initial
  transients through sharp gradients or phase changes, schedule output intervals
  and checkpoint cadence, and plan restart strategies for long-running jobs.
  Use when choosing dt for a new simulation, diagnosing adaptive time-step
  oscillations, deciding checkpoint frequency to minimize lost work, or
  setting up output schedules aligned with physical time scales, even if
  the user only says "my run is too slow" or "how often should I save."
allowed-tools: Read, Bash, Write, Grep, Glob
metadata:
  author: HeshamFS
  version: "1.2.2"
  security_tier: high
  security_reviewed: true
  tested_with:
    - claude-code
  last_evaluated: "2026-06-24"
  eval_cases: 4
  last_reviewed: "2026-06-23"
  standards:
    - "Courant-Friedrichs-Lewy (CFL) condition (Courant, Friedrichs, Lewy 1928)"
    - "von Neumann stability analysis (Fourier/diffusion and Courant number limits)"
    - "Daly (2006), optimal checkpoint interval formula"
    - "Young (1974), first-order checkpoint interval refinement"
---

# Time Stepping

## Goal

Provide a reliable workflow for choosing, ramping, and monitoring time steps plus output/checkpoint cadence.

## Requirements

- Python 3.10+
- No external dependencies (uses stdlib)

## Inputs to Gather

| Input | Description | Example |
|-------|-------------|---------|
| Stability limits | CFL/Fourier/reaction limits | `dt_max = 1e-4` |
| Target dt | Desired time step | `1e-5` |
| Total run time | Simulation duration | `10 s` |
| Output interval | Time between outputs | `0.1 s` |
| Checkpoint cost | Time to write checkpoint | `120 s` |

## Decision Guidance

### Time Step Selection

```
Is stability limit known?
├── YES → Use min(dt_target, dt_limit × safety)
└── NO → Start conservative, increase adaptively

Need ramping for startup?
├── YES → Start at dt_init, ramp to dt_target over N steps
└── NO → Use dt_target from start
```

### Ramping Strategy

| Problem Type | Ramp Steps | Initial dt |
|--------------|------------|------------|
| Smooth IC | None needed | Full dt |
| Sharp gradients | 5-10 | 0.1 × dt |
| Phase change | 10-20 | 0.01 × dt |
| Cold start | 10-50 | 0.001 × dt |

## Script Outputs (JSON Fields)

| Script | Key Outputs |
|--------|-------------|
| `scripts/timestep_planner.py` | `dt_limit`, `dt_recommended`, `ramp_schedule`, `notes` |
| `scripts/output_schedule.py` | `output_times`, `interval`, `count` |
| `scripts/checkpoint_planner.py` | `checkpoint_interval`, `checkpoints`, `overhead_fraction`, `warnings` |

`output_schedule.py` `count` is endpoint-inclusive: it includes both `t_start` and `t_end`, so `count = number_of_intervals + 1` (e.g. `t=0..5` at `0.05` spacing yields 101 frames for 100 intervals).

## Workflow

1. **Get stability limits** - Use numerical-stability skill
2. **Plan time stepping** - Run `scripts/timestep_planner.py`
3. **Schedule outputs** - Run `scripts/output_schedule.py`
4. **Plan checkpoints** - Run `scripts/checkpoint_planner.py`
5. **Monitor during run** - Adjust dt if limits change

## Conversational Workflow Example

**User**: I'm running a 10-hour phase-field simulation. How often should I checkpoint?

**Agent workflow**:
1. Plan checkpoints based on acceptable lost work:
   ```bash
   python3 scripts/checkpoint_planner.py --run-time 36000 --checkpoint-cost 120 --max-lost-time 1800 --json
   ```
2. Interpret: Checkpoint every 30 minutes, overhead ~6.7% (Acceptable per the interpretation table), max 30 min lost work on crash.

## Pre-Run Checklist

- [ ] Confirm dt limits from stability analysis
- [ ] Define ramping strategy for transient startup
- [ ] Choose output interval consistent with physics time scales
- [ ] Plan checkpoints based on restart risk
- [ ] Re-evaluate dt after parameter changes

## CLI Examples

```bash
# Plan time stepping with ramping
python3 scripts/timestep_planner.py --dt-target 1e-4 --dt-limit 2e-4 --safety 0.8 --ramp-steps 10 --json

# Schedule output times
python3 scripts/output_schedule.py --t-start 0 --t-end 10 --interval 0.1 --json

# Plan checkpoints for long run
python3 scripts/checkpoint_planner.py --run-time 36000 --checkpoint-cost 120 --max-lost-time 1800 --json
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| `dt-target must be positive` | Invalid time step | Use positive value |
| `t-end must be > t-start` | Invalid time range | Check time bounds |
| `checkpoint-cost must be < run-time` | Checkpoint too expensive | Reduce checkpoint size |

## Interpretation Guidance

### dt Behavior

| Observation | Meaning | Action |
|-------------|---------|--------|
| dt stable at target | Good | Continue |
| dt shrinking | Stability issue | Check CFL, reduce target |
| dt oscillating | Borderline stability | Add safety factor |

### Checkpoint Overhead

| Overhead | Acceptability |
|----------|---------------|
| < 1% | Excellent |
| 1-5% | Good |
| 5-10% | Acceptable |
| > 10% | Too frequent, increase interval |

## Verification checklist

- [ ] Recorded `dt_recommended` and `dt_limit` from `timestep_planner.py` and confirmed `dt_recommended <= dt_limit` with no "Recommended dt exceeds stability limit" note in the `notes` field.
- [ ] Captured the actual `dt_limit` value from the stability analysis (numerical-stability skill: CFL/Fourier/reaction limit) that was fed to `--dt-limit`, rather than guessing — and re-ran the planner after any parameter change.
- [ ] Confirmed `safety <= 1.0` was applied (a margin below the limit), and logged the `notes` array (e.g. "Recommended dt reduced by stability limit", min/max clamps) so the binding constraint is known.
- [ ] Recorded the `output_schedule.py` `count` and verified it is endpoint-inclusive (`count = intervals + 1`, both `t_start` and `t_end` present), so frame counts and post-processing indices are not off-by-one.
- [ ] Recorded the checkpoint `interval`, `method` (`daly` vs `cap`), and `overhead_fraction` from `checkpoint_planner.py`, and confirmed `overhead_fraction <= 0.10` (no `warnings` entry) against the overhead acceptability table.
- [ ] Confirmed every script exited 0 (not exit 2 / stderr `ValueError`) and that quoted dt/interval/checkpoint values come from the JSON `results`, not from a run that printed a validation error.

## Common pitfalls & rationalizations

| Tempting shortcut | Why it's wrong / what to do |
|-------------------|------------------------------|
| "Implicit scheme, so any dt is fine — skip `--dt-limit`." | Unconditional *stability* is not *accuracy*; a large dt still ruins temporal error and resolves no transient. Still pass a physics-based `dt-target` and re-check the recommended dt against time scales. |
| "Set `--safety` above 1.0 to take bigger steps." | `safety` is a margin at or below the limit; `safety > 1.0` would return a dt above the stability limit, so the planner rejects it (exit 2). Lower `dt-limit` expectations or use a finer mesh instead. |
| "It ran without crashing, so the dt is valid." | Run completion is not correctness. Verify `dt_recommended <= dt_limit`, read the `notes` array, and re-plan whenever `v_max`, `D`, `dx`, or the scheme changes — the limit moves with them. |
| "The output `count` looks one too many — drop the last frame." | `count` is endpoint-inclusive by design (`intervals + 1`); both `t_start` and `t_end` are real outputs. Trimming it silently loses the final state. |
| "Checkpoint every step to never lose work." | That drives `overhead_fraction` past 10% (the planner emits a `warnings` entry) and dominates runtime. Use `--max-lost-time` (cap) or `--mtbf` (Daly) so overhead stays in the Acceptable band. |
| "Reuse last week's dt/checkpoint plan; the model is basically the same." | Stability and optimal checkpoint interval depend on current `dx`, velocity/diffusivity, `checkpoint-cost`, and MTBF. Re-run the three scripts with current values rather than copying stale numbers. |

## Security

### Input Validation
- All numeric parameters (`dt-target`, `dt-limit`, `safety`, `t-start`, `t-end`, `interval`, `run-time`, `checkpoint-cost`, `max-lost-time`) are validated as finite positive numbers (non-finite values such as `inf`/`nan` are rejected)
- `safety` is bounded to `<= 1.0` (a safety factor is a stability margin at or below the limit; values above 1.0 are rejected)
- `ramp-steps` and `preview-steps` are validated as non-negative integers with an upper bound of 1,000,000; only the previewed slice of the ramp is materialized to bound memory use
- Time range consistency is enforced (`t-end` must exceed `t-start`; `checkpoint-cost` must be less than `run-time`)

### File Access
- Scripts read no external files; all inputs are provided via CLI arguments
- Scripts write only to stdout (JSON output); no files are created unless the agent explicitly uses the Write tool

### Tool Restrictions
- **Read**: Used to inspect script source, references, and user configuration files
- **Bash**: Used to execute the three Python planning scripts (`timestep_planner.py`, `output_schedule.py`, `checkpoint_planner.py`) with explicit argument lists
- **Write**: Used to save generated time-step plans or checkpoint schedules; writes are scoped to the user's working directory
- **Grep/Glob**: Used to locate relevant files and search references

### Safety Measures
- No `eval()`, `exec()`, or dynamic code generation
- All subprocess calls use explicit argument lists (no `shell=True`)
- Scripts use only Python standard library; no pickle loading or deserialization of untrusted data
- All output is deterministic JSON with no shell-interpretable content

## Limitations

- **Not adaptive control**: Plans static schedules, not runtime adaptation
- **Assumes constant physics**: If parameters change, re-plan

## References

- `references/cfl_coupling.md` - Combining multiple stability limits
- `references/ramping_strategies.md` - Startup policies
- `references/output_checkpoint_guidelines.md` - Cadence rules

## Version History

- **v1.2.2** (2026-06-24): Added Verification checklist and Common pitfalls & rationalizations sections grounded in the three planning scripts' actual outputs
- **v1.2.0** (2026-06-23): Corrected overhead/frame-count docs and evals, removed output-time float drift, hardened input validation (checkpoint-cost < run-time, safety <= 1.0, bounded ramp/preview steps, finite checks)
- **v1.1.0** (2024-12-24): Enhanced documentation, decision guidance, examples
- **v1.0.0**: Initial release with 3 planning scripts

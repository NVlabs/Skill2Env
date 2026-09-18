---
name: numerical-integration
description: >
  Select and configure time integration methods for ODE and PDE simulations —
  choose among explicit Runge-Kutta, BDF, Rosenbrock, and Adams families,
  set relative and absolute error tolerances, implement adaptive step-size
  control with P/PI step-size controllers, plan IMEX operator splitting for mixed
  stiff and non-stiff terms, and estimate splitting errors. Use when picking
  an integrator for a new simulation, diagnosing step rejections or tolerance
  failures, setting up operator splitting for phase-field or reaction-diffusion
  problems, or deciding between explicit and implicit time marching, even if
  the user only says "my solver keeps rejecting steps" or "which ODE method
  should I use."
allowed-tools: Read, Write, Grep, Glob
metadata:
  author: HeshamFS
  version: "1.2.2"
  security_tier: medium
  security_reviewed: true
  tested_with:
    - claude-code
  last_evaluated: "2026-06-24"
  eval_cases: 4
  last_reviewed: "2026-06-23"
  standards:
    - "Hairer, Norsett & Wanner, Solving Ordinary Differential Equations I (Nonstiff): RK45 (Dormand-Prince), DOP853, embedded error estimation"
    - "Hairer & Wanner, Solving ODEs II (Stiff and DAE): BDF, Radau IIA, Rosenbrock methods"
    - "Gustafsson (1991/1994), control-theoretic PI step-size control"
    - "Strang (1968), operator splitting; with Lie-Trotter and Marchuk-Strang variants"
    - "Eyre (1998), unconditionally gradient-stable convex splitting for phase-field (Allen-Cahn / Cahn-Hilliard)"
---

# Numerical Integration

## Goal

Provide a reliable workflow to select integrators, set tolerances, and manage adaptive time stepping for time-dependent simulations.

## Requirements

- Python 3.10+
- NumPy (for some scripts)
- No heavy dependencies for core functionality

## Inputs to Gather

| Input | Description | Example |
|-------|-------------|---------|
| Problem type | ODE/PDE, stiff/non-stiff | `stiff PDE` |
| Jacobian available | Can compute ∂f/∂u? | `yes` |
| Target accuracy | Desired error level | `1e-6` |
| Constraints | Memory, implicit allowed? | `implicit OK` |
| Time scale | Characteristic time | `1e-3 s` |

## Decision Guidance

### Choosing an Integrator

```
Is the problem stiff?
├── YES → Is Jacobian available?
│   ├── YES → Use Rosenbrock or BDF
│   └── NO → Use BDF with numerical Jacobian
└── NO → Is high accuracy needed?
    ├── YES → Use RK45 or DOP853
    └── NO → Use RK4 or Adams-Bashforth
```

### Stiff vs Non-Stiff Detection

| Symptom | Likely Stiff | Action |
|---------|--------------|--------|
| dt shrinks to tiny values | Yes | Switch to implicit |
| Eigenvalues span many decades | Yes | Use BDF/Radau |
| Smooth solution, reasonable dt | No | Stay explicit |

## Script Outputs (JSON Fields)

| Script | Key Outputs |
|--------|-------------|
| `scripts/error_norm.py` | `error_norm`, `scale_min`, `scale_max` |
| `scripts/adaptive_step_controller.py` | `accept`, `dt_next`, `factor` |
| `scripts/integrator_selector.py` | `recommended`, `alternatives`, `notes` |
| `scripts/imex_split_planner.py` | `implicit_terms`, `explicit_terms`, `splitting_strategy` |
| `scripts/splitting_error_estimator.py` | `error_estimate`, `substeps` |

## Workflow

1. **Classify stiffness** - Check eigenvalue spread or use stiffness_detector
2. **Choose tolerances** - See `references/tolerance_guidelines.md`
3. **Select integrator** - Run `scripts/integrator_selector.py`
4. **Compute error norms** - Use `scripts/error_norm.py` for step acceptance
5. **Adapt step size** - Use `scripts/adaptive_step_controller.py`
6. **Plan IMEX/splitting** - If mixed stiff/nonstiff, use `scripts/imex_split_planner.py`
7. **Validate convergence** - Repeat with tighter tolerances

## Conversational Workflow Example

**User**: I'm solving the Allen-Cahn equation with a stiff double-well potential. What integrator should I use?

**Agent workflow**:
1. Check integrator options:
   ```bash
   python3 scripts/integrator_selector.py --stiff --jacobian-available --accuracy high --json
   ```
2. Plan the IMEX splitting (diffusion implicit, reaction explicit):
   ```bash
   python3 scripts/imex_split_planner.py --stiff-terms diffusion --nonstiff-terms reaction --coupling weak --json
   ```
3. Recommend: Use IMEX-BDF2 with diffusion term implicit, double-well reaction explicit.

## Pre-Integration Checklist

- [ ] Identify stiffness and dominant time scales
- [ ] Set `rtol`/`atol` consistent with physics and units
- [ ] Confirm integrator compatibility with stiffness
- [ ] Use error norm to accept/reject steps
- [ ] Verify convergence with tighter tolerance run

## CLI Examples

```bash
# Select integrator for stiff problem with Jacobian
python3 scripts/integrator_selector.py --stiff --jacobian-available --accuracy high --json

# Compute scaled error norm
python3 scripts/error_norm.py --error 0.01,0.02 --solution 1.0,2.0 --rtol 1e-3 --atol 1e-6 --json

# Adaptive step control with PI controller
python3 scripts/adaptive_step_controller.py --dt 1e-2 --error-norm 0.8 --order 4 --controller pi --json

# Plan IMEX splitting
python3 scripts/imex_split_planner.py --stiff-terms diffusion,elastic --nonstiff-terms reaction --coupling strong --json

# Estimate splitting error
python3 scripts/splitting_error_estimator.py --dt 1e-4 --scheme strang --commutator-norm 50 --target-error 1e-6 --json
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| `rtol must be a non-negative finite number` / `atol must be a non-negative finite number` | Invalid tolerances | Use non-negative finite values |
| `error_norm must be finite and non-negative` | Negative or non-finite error norm | Check error computation |
| `scale must be positive; with min_scale=0 ensure atol>0 or rtol*\|y\|>0` | All scale entries collapsed to 0 (e.g. `rtol=0`, `atol=0`, default `min_scale=0`) | Set `atol>0`, `rtol>0`, or `--min-scale` > 0 |
| `argument --controller: invalid choice: ... (choose from p, pi)` | Invalid controller type | Use `p` or `pi` |
| `Provide at least one stiff or non-stiff term` | Empty term list | Specify stiff or nonstiff terms |

## Interpretation Guidance

### Error Norm Values

| Error Norm | Meaning | Action |
|------------|---------|--------|
| < 1.0 | Step acceptable | Accept, maybe increase dt |
| ≈ 1.0 | At tolerance boundary | Accept with current dt |
| > 1.0 | Step rejected | Reject, reduce dt |

### Controller Selection

| Controller | CLI value | Properties | Best For |
|------------|-----------|------------|----------|
| P (elementary / integral) | `p` (default) | Simple, some overshoot | Non-stiff, moderate accuracy |
| PI (proportional-integral) | `pi` | Smooth, robust (requires `--prev-error`) | General use |

> PID control is described in `references/error_control.md` for reference only; the
> `adaptive_step_controller.py` CLI implements `p` and `pi` controllers.

### IMEX Strategy

| Coupling | Strategy |
|----------|----------|
| Weak | Simple operator splitting |
| Moderate | Strang splitting |
| Strong | Fully coupled IMEX-RK |

## Verification checklist

- [ ] Recorded the scaled `error_norm` (and `scale_min`/`scale_max`) from `scripts/error_norm.py` and confirmed `scale_min > 0`, so no component reduced to atol-only scaling by accident.
- [ ] Confirmed each accepted step has `error_norm <= accept_threshold` (default 1.0) per `scripts/adaptive_step_controller.py`; logged any `accept: false` steps and the resulting `dt_next`/`factor` rather than forcing the step through.
- [ ] For the PI controller, supplied `--prev-error` and verified `controller_used` reported `pi` (not the silent `p` fallback that occurs when `--prev-error` is omitted).
- [ ] Ran `scripts/integrator_selector.py` with the actual `--stiff`/`--jacobian-available`/`--accuracy` flags matching the problem and recorded `recommended` plus the `notes` (e.g. the "expect smaller dt" warning for stiff-without-implicit).
- [ ] For operator splitting, recorded `error_estimate`, `substeps`, and `dt_effective` from `scripts/splitting_error_estimator.py` and confirmed `error_estimate <= target-error` after substepping, using the correct `--scheme` order (lie=1, strang=2).
- [ ] Ran the convergence validation (Workflow step 7): repeated with tighter `rtol`/`atol` and confirmed the solution change is below the target accuracy, rather than trusting a single tolerance run.

## Common pitfalls & rationalizations

| Tempting shortcut | Why it's wrong / what to do |
|-------------------|-----------------------------|
| "I picked an implicit/BDF method, so any `dt` is fine." | Unconditional *stability* is not *accuracy*; large `dt` still inflates temporal error. Check `error_norm` against the accept threshold and run the tighter-tolerance convergence check (Workflow step 7). |
| "`error_norm` came back < 1, so the step and the whole run are correct." | The norm only certifies the local step under the chosen `rtol`/`atol`. A loose tolerance passes every step while the global solution is wrong — tighten tolerances and confirm convergence before trusting results. |
| "I'll use the PI controller for smoother stepping" but omit `--prev-error`. | Without `--prev-error` the script silently falls back to the P controller (`controller_used: p`). You get no PI benefit. Pass the previous accepted `error_norm` and verify `controller_used: pi`. |
| "Strang vs Lie splitting won't matter much here." | Splitting error scales as `commutator_norm * dt^(order+1)` with order 1 (lie) vs 2 (strang). For a nonzero commutator the schemes differ by a full power of `dt` — run `splitting_error_estimator.py` with the actual `--commutator-norm` and `--target-error` instead of guessing. |
| "The selector recommended IMEX/RK-Chebyshev, so I'll just run explicitly without a Jacobian." | That branch fires only for stiff problems *without* implicit solves and the script warns "expect smaller dt." Read the `notes`: provide a Jacobian/Jv product and use BDF/Radau if implicit solves are feasible. |
| "It ran to the final time without crashing, so the integration is valid." | Completion is not correctness. Verify step acceptance (`error_norm <= threshold`), splitting error within `target-error`, and convergence under tighter tolerances; for conservative problems pass `--conservative` to `imex_split_planner.py` and check conserved quantities. |

## Security

### Input Validation
- All numeric inputs (`dt`, `rtol`, `atol`, `error_norm`, `stiffness_ratio`, `commutator_norm`, etc.) are validated as finite numbers at the function boundary
- `imex_split_planner.py` validates term names against `[a-zA-Z_][a-zA-Z0-9_ -]*` with length and count limits, preventing injection payloads in user-supplied term lists
- Comma-separated value lists are capped at 100,000 entries to prevent resource exhaustion
- Numeric bounds enforced: `dimension` capped at 10 billion, `order` at 20, `stiffness_ratio` at 1e30
- `--controller` is validated against a fixed allowlist (`p`, `pi`)
- `--scheme` is validated against known splitting schemes (`lie`, `strang`)

### File Access
- Scripts read no external files; all inputs are provided via CLI arguments
- Scripts write only to stdout (JSON output); no files are created unless the agent explicitly uses the Write tool

### Tool Restrictions
- **Read**: Used to inspect script source, references, and user configuration files
- **Write**: Used to save integrator recommendations or splitting plans; writes are scoped to the user's working directory
- **Grep/Glob**: Used to locate relevant files and search references
- The skill's `allowed-tools` excludes `Bash` to prevent the agent from executing arbitrary commands when processing user-provided inputs

### Safety Measures
- No `eval()`, `exec()`, or dynamic code generation
- All subprocess calls use explicit argument lists (no `shell=True`)
- Reduced tool surface (no Bash) limits the agent to read/write operations only
- Term names are sanitized before use, preventing shell metacharacter injection

## Limitations

- **No automatic stiffness detection**: Use stiffness_detector from numerical-stability
- **Splitting assumes separability**: Terms must be cleanly separable
- **Jacobian requirement**: Some methods need analytical or numerical Jacobian

## References

- `references/method_catalog.md` - Integrator options and properties
- `references/tolerance_guidelines.md` - Choosing rtol/atol
- `references/error_control.md` - Error norm and adaptation formulas
- `references/imex_guidelines.md` - Stiff/non-stiff splitting
- `references/splitting_catalog.md` - Operator splitting patterns
- `references/multiphase_field_patterns.md` - Phase-field specific splits

## Version History

- **v1.2.2** (2026-06-24): Added Verification checklist and Common pitfalls & rationalizations sections grounding step acceptance, PI controller usage, integrator selection, and splitting-error checks in the scripts' actual outputs
- **v1.2.0** (2026-06-23): Fixed PI controller coefficient/sign to standard form, fixed error_norm scale-collapse crash, corrected error-message and controller documentation to match the scripts
- **v1.1.0** (2024-12-24): Enhanced documentation, decision guidance, examples
- **v1.0.0**: Initial release with 5 integration scripts

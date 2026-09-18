---
name: differentiation-schemes
description: >
  Select and apply numerical differentiation schemes for PDE and ODE
  discretization — generate finite-difference stencils at arbitrary order and
  accuracy, choose between central, upwind, compact (Pade), and spectral
  methods, handle boundary stencils, and estimate truncation error scaling.
  Use when discretizing spatial derivatives, picking a scheme for advection-
  or diffusion-dominated problems, building custom stencils for nonstandard
  operators, or comparing dispersion and dissipation properties of candidate
  schemes, even if the user just says "how do I approximate this derivative"
  or "my solution is too diffusive."
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
    - "Fornberg (1988), Generation of finite difference formulas on arbitrarily spaced grids"
    - "Taylor-series truncation-error analysis / order-of-accuracy theory"
    - "Lele (1992), Compact finite difference schemes with spectral-like resolution"
    - "Richardson extrapolation and grid-convergence (observed-order) verification"
    - "Jiang & Shu (1996), ENO/WENO essentially non-oscillatory schemes"
---

# Differentiation Schemes

## Goal

Provide a reliable workflow to select a differentiation scheme, generate stencils, and assess accuracy for simulation discretization.

## Requirements

- Python 3.10+
- NumPy (for stencil computations)
- No heavy dependencies

## Inputs to Gather

| Input | Description | Example |
|-------|-------------|---------|
| Derivative order | First, second, etc. | `1` or `2` |
| Target accuracy | Order of truncation error | `2` or `4` |
| Grid type | Uniform, nonuniform | `uniform` |
| Boundary type | Periodic, Dirichlet, Neumann | `periodic` |
| Smoothness | Smooth or discontinuous | `smooth` |

## Decision Guidance

### Scheme Selection Flowchart

```
Is the field smooth?
├── YES → Is domain periodic?
│   ├── YES → Use central differences or spectral
│   └── NO → Use central interior + one-sided at boundaries
└── NO → Are there shocks/discontinuities?
    ├── YES → Use upwind, TVD, or WENO
    └── NO → Use central with limiters
```

### Quick Reference

| Situation | Recommended Scheme |
|-----------|-------------------|
| Smooth, periodic | Central, spectral |
| Smooth, bounded | Central + one-sided BCs |
| Advection-dominated | Upwind |
| Shocks/fronts | TVD, WENO |
| High accuracy needed | Compact (Padé), spectral |

## Script Outputs (JSON Fields)

| Script | Key Outputs |
|--------|-------------|
| `scripts/stencil_generator.py` | `offsets`, `coefficients`, `order`, `accuracy`, `scheme` |
| `scripts/scheme_selector.py` | `recommended`, `alternatives`, `notes` |
| `scripts/truncation_error.py` | `error_scale`, `order`, `reduction_if_halved` |

## Workflow

1. **Identify requirements** - derivative order, accuracy, smoothness
2. **Select scheme** - Run `scripts/scheme_selector.py`
3. **Generate stencils** - Run `scripts/stencil_generator.py`
4. **Estimate error** - Run `scripts/truncation_error.py`
5. **Validate** - Test with manufactured solutions or grid refinement

## Conversational Workflow Example

**User**: I need to discretize a second derivative for a diffusion equation on a uniform grid. I want 4th-order accuracy.

**Agent workflow**:
1. Select appropriate scheme (boundary type was not stated; if the domain is
   bounded rather than periodic, add `--boundary` to surface one-sided/ghost-cell
   guidance, or ask the user):
   ```bash
   python3 scripts/scheme_selector.py --smooth --order 2 --accuracy 4 --json
   ```
2. Generate the stencil:
   ```bash
   python3 scripts/stencil_generator.py --order 2 --accuracy 4 --scheme central --json
   ```
3. Result: 5-point stencil with coefficients `[-1/12, 4/3, -5/2, 4/3, -1/12]` / dx².

## Pre-Discretization Checklist

- [ ] Confirm derivative order and target accuracy
- [ ] Choose scheme appropriate to smoothness and boundaries
- [ ] Generate and inspect stencils at boundaries
- [ ] Estimate truncation error vs physics scales
- [ ] Verify with grid refinement study

## CLI Examples

```bash
# Select scheme for smooth periodic problem
python3 scripts/scheme_selector.py --smooth --periodic --order 1 --accuracy 4 --json

# Generate central difference stencil for first derivative
python3 scripts/stencil_generator.py --order 1 --accuracy 2 --scheme central --json

# Generate 4th-order second derivative stencil
python3 scripts/stencil_generator.py --order 2 --accuracy 4 --scheme central --json

# Estimate truncation error
python3 scripts/truncation_error.py --dx 0.01 --accuracy 2 --scale 1.0 --json
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| `order must be positive` | Invalid derivative order | Use 1, 2, 3, ... (max 6) |
| `order must be <= 6` | Derivative order too large | Use 1–6 |
| `accuracy must be even for central` | Odd accuracy requested for central scheme | Use 2, 4, 6, ... |
| `scheme must be central, forward, or backward` | Invalid `--scheme` value | Use `central`, `forward`, or `backward` |

## Interpretation Guidance

### Stencil Properties

| Property | Meaning |
|----------|---------|
| Symmetric offsets | Central scheme (no directional bias) |
| Asymmetric offsets | One-sided or upwind scheme |
| More points | Higher accuracy but wider stencil |

### Truncation Error Scaling

| Accuracy Order | Error Scales As | Refinement Factor |
|----------------|-----------------|-------------------|
| 2nd order | O(dx²) | 2× refinement → 4× error reduction |
| 4th order | O(dx⁴) | 2× refinement → 16× error reduction |
| 6th order | O(dx⁶) | 2× refinement → 64× error reduction |

### Common Stencils

| Derivative | Accuracy | Points | Coefficients (× 1/dx or 1/dx²) |
|------------|----------|--------|-------------------------------|
| 1st | 2 | 3 | [-1/2, 0, 1/2] |
| 1st | 4 | 5 | [1/12, -2/3, 0, 2/3, -1/12] |
| 2nd | 2 | 3 | [1, -2, 1] |
| 2nd | 4 | 5 | [-1/12, 4/3, -5/2, 4/3, -1/12] |

## Verification checklist

Before trusting a generated stencil or accepting a scheme recommendation, record concrete evidence for each item below:

- [ ] Ran `stencil_generator.py --json` and confirmed `results.accuracy` matches the requested order AND that `len(results.offsets)` equals the expected stencil width (e.g. 5 points for a 4th-order central second derivative); for a `central` scheme also verified the offsets are symmetric about 0.
- [ ] Sanity-checked the returned `coefficients` against `references/stencil_catalog.md`: confirmed they sum to ~0 (consistency: the operator annihilates a constant) and reproduce a known catalog stencil for at least one standard case (e.g. 2nd-order d²/dx² gives `[1, -2, 1]/dx²`).
- [ ] For a `central` scheme, confirmed `--accuracy` is even (odd values exit 2 with `accuracy must be even for central`); recorded the actual exit code rather than assuming the requested order was achieved.
- [ ] Recorded the `error_scale`, `order`, and `reduction_if_halved` from `truncation_error.py` and confirmed `reduction_if_halved == 2**accuracy`, then compared `error_scale` against the smallest physical feature size (dx/L_feature from `references/error_guidance.md`) to confirm the grid actually resolves the physics.
- [ ] Ran an independent grid-refinement / manufactured-solution study on >=3 grids (the scripts do NOT do this) and confirmed the observed order `p_obs = log(e_h/e_{h/2})/log(2)` is within ~10% of the formal `accuracy` before quoting that order.
- [ ] For a bounded (non-periodic) domain, confirmed boundary stencils were generated/selected explicitly (`--scheme forward|backward` or `--boundary` guidance) per `references/boundary_handling.md`, since the interior stencil alone does not define the scheme order at the boundary.
- [ ] For non-smooth fields (shocks/fronts), confirmed `scheme_selector.py` did NOT recommend high-order central FD and that a limiter/WENO/upwind path was chosen instead.

## Common pitfalls & rationalizations

| Tempting shortcut | Why it's wrong / what to do |
|-------------------|------------------------------|
| "The stencil generator returned coefficients, so the scheme is the order I asked for." | The `accuracy` field just echoes your request; it is not measured. Verify the achieved order with a grid-refinement study and confirm the coefficients match a catalog stencil and sum to ~0. |
| "I asked for 4th order on a central scheme with `--accuracy 3`, it'll just round up." | It will not — central schemes reject odd accuracy with `accuracy must be even for central` (exit 2). Pass an even accuracy; an odd request is an error, not a silent upgrade. |
| "Higher accuracy order always means lower error here." | `truncation_error.py` reports asymptotic *scaling* (`scale * dx**accuracy`); for a coarse grid or under-resolved feature the higher-order term need not dominate, and roundoff (`O(ε/dx^p)`) can win on very fine grids. Compare `error_scale` to the feature size, do not assume monotone improvement. |
| "Two grids agree closely, so it's converged." | Two grids cannot estimate observed order or confirm the asymptotic range. Use >=3 grids and compute `p_obs` before claiming the formal order (see `references/error_guidance.md`). |
| "The interior stencil is 4th order, so my whole solve is 4th order." | The generator emits interior stencils only; boundary closures often limit the global order. Generate one-sided/ghost-cell stencils explicitly and verify the boundary does not drop the observed order (`references/boundary_handling.md`). |
| "The field has a shock but a wide central stencil is more accurate, so use it." | High-order central FD oscillates (Gibbs) at discontinuities. `scheme_selector.py` recommends FV with limiter/WENO or upwind for `--discontinuous`; follow it rather than maximizing formal order. |
| "Custom `--offsets` let me build any stencil I want." | Offsets must be distinct, length-capped (51), and number more than the derivative order, or the script exits 2. A valid run still does not guarantee the intended accuracy — verify the coefficients and observed order. |

## Security

### Input Validation
- `--order` (derivative order) is validated as a positive integer with an upper bound (`order <= 6`)
- `--accuracy` is validated as a positive integer (`<= 8`), and additionally must be even for central schemes
- `--scheme` is validated against a fixed allowlist (`central`, `forward`, `backward`)
- `--offsets` (custom stencil) is length-capped (max 51), parsed as distinct integers, and must exceed the derivative order
- `--dx` and `--scale` are validated as finite, non-negative numbers (`--dx` strictly positive)
- No user-supplied strings are interpolated into code paths or shell commands

### File Access
- Scripts read no external files; all inputs are provided via CLI arguments
- Scripts write only to stdout (JSON output); no files are created unless the agent explicitly uses the Write tool

### Tool Restrictions
- **Read**: Used to inspect script source, references, and user configuration files
- **Bash**: Used to execute the three Python scripts (`stencil_generator.py`, `scheme_selector.py`, `truncation_error.py`) with explicit argument lists
- **Write**: Used to save generated stencil coefficients or scheme recommendations; writes are scoped to the user's working directory
- **Grep/Glob**: Used to locate relevant files and search references

### Safety Measures
- No `eval()`, `exec()`, or dynamic code generation
- All subprocess calls use explicit argument lists (no `shell=True`)
- Stencil computation uses only small, bounded arrays (derivative order capped at 6, accuracy at 8, and custom offset lists capped at 51 points)
- All output is deterministic JSON with no shell-interpretable content

## Limitations

- **Boundary handling**: Stencil generator provides interior stencils; boundaries need special treatment
- **Nonuniform grids**: Standard stencils assume uniform spacing
- **Spectral**: Not covered by stencil generator

## References

- `references/stencil_catalog.md` - Common stencils
- `references/boundary_handling.md` - One-sided schemes
- `references/scheme_selection.md` - FD/FV/spectral comparison
- `references/error_guidance.md` - Truncation error scaling

## Version History

- **v1.2.2** (2026-06-24): Added a Verification checklist (evidence-based, tied to script JSON outputs and the references) and a Common pitfalls & rationalizations table.
- **v1.2.0** (2026-06-23): Enforced even-accuracy and order upper-bound validation, corrected Security/error-handling/output docs to match scripts, fixed CLI/eval examples, hardened input validation
- **v1.1.0** (2024-12-24): Enhanced documentation, decision guidance, examples
- **v1.0.0**: Initial release with 3 differentiation scripts

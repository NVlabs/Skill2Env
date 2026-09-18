---
name: convergence-study
description: >
  Perform spatial and temporal convergence analysis for solution verification —
  compute observed convergence orders from grid or timestep refinement studies,
  apply Richardson extrapolation to estimate discretization error, and calculate
  the Grid Convergence Index (GCI) per ASME V&V 20 standards. Use when verifying
  that a numerical solution converges at the expected rate, estimating the
  error on the finest mesh, checking whether grids are in the asymptotic range,
  or preparing formal verification reports, even if the user only asks "is my
  mesh fine enough" or "how accurate is my solution."
allowed-tools:
  - Bash
  - Read
metadata:
  author: HeshamFS
  version: "1.2.2"
  standards:
    - "ASME V&V 20 (Standard for Verification and Validation in Computational Fluid Dynamics and Heat Transfer)"
    - "Roache, Grid Convergence Index (GCI) method with safety factors Fs in {1.25, 3.0}"
    - "Richardson extrapolation for discretization error estimation"
    - "Method of Manufactured Solutions (MMS) for code verification"
    - "AIAA verification and validation guidelines"
  security_tier: high
  security_reviewed: true
  tested_with:
    - claude-code
  last_evaluated: "2026-06-24"
  eval_cases: 4
  last_reviewed: "2026-06-23"
---

# Convergence Study

## Goal

Provide script-driven convergence analysis for verifying that numerical solutions converge at the expected rate as the mesh or timestep is refined.

## Requirements

- Python 3.10+
- No third-party packages — scripts use only the Python standard library (`math`).

## Inputs to Gather

| Input | Description | Example |
|-------|-------------|---------|
| Grid spacings | Sequence of mesh sizes (coarse to fine) | `0.4,0.2,0.1,0.05` |
| Timestep sizes | Sequence of dt values | `0.04,0.02,0.01` |
| Solution values | QoI at each refinement level | `1.16,1.04,1.01,1.0025` |
| Expected order | Formal order of the numerical scheme | `2.0` |
| Safety factor | GCI safety factor (1.25 default) | `1.25` |

## Script Outputs (JSON Fields)

| Script | Key Outputs |
|--------|-------------|
| `scripts/h_refinement.py` | `results.observed_orders`, `results.mean_order`, `results.richardson_extrapolated_value`, `results.convergence_assessment` |
| `scripts/dt_refinement.py` | Same as h_refinement but for temporal convergence |
| `scripts/richardson_extrapolation.py` | `results.extrapolated_value`, `results.error_estimate`, `results.observed_order` |
| `scripts/gci_calculator.py` | `results.observed_order`, `results.gci_fine`, `results.gci_coarse`, `results.asymptotic_ratio`, `results.in_asymptotic_range`, `results.extrapolated_value`, `results.notes` |

## Workflow

1. **Run grid/timestep refinement study** with at least 3 levels
2. **Compute observed convergence order** with `h_refinement.py` or `dt_refinement.py`
3. **Compare** observed order to expected order of the scheme
4. **Estimate discretization error** via Richardson extrapolation
5. **Report GCI** for formal solution verification using `gci_calculator.py`
6. **Document** convergence results and any anomalies

## Decision Guidance

```
Do you have 3+ refinement levels?
+-- YES --> Run h_refinement.py or dt_refinement.py
|           +-- Observed order matches expected? --> Solution verified
|           +-- Order too low? --> Check: pre-asymptotic, coding error, insufficient resolution
|           +-- Order too high? --> Check: superconvergence or cancellation effects
+-- NO (only 2 levels) --> Use richardson_extrapolation.py with assumed order
                           (less reliable without order verification)
```

## CLI Examples

```bash
# Spatial convergence with 4 grid levels
python3 scripts/h_refinement.py --spacings 0.4,0.2,0.1,0.05 --values 1.16,1.04,1.01,1.0025 --expected-order 2.0 --json

# Temporal convergence with 3 timestep levels
python3 scripts/dt_refinement.py --timesteps 0.04,0.02,0.01 --values 2.12,2.03,2.0075 --expected-order 2.0 --json

# Richardson extrapolation with assumed 2nd-order
python3 scripts/richardson_extrapolation.py --spacings 0.02,0.01 --values 1.0032,1.0008 --order 2.0 --json

# GCI for 3-mesh verification
python3 scripts/gci_calculator.py --spacings 0.04,0.02,0.01 --values 1.0128,1.0032,1.0008 --json
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| `spacings and values must have the same length` | Mismatched input arrays | Provide equal-length lists |
| `At least 2 refinement levels required` | Too few data points | Add more refinement levels |
| `Exactly 3 refinement levels required` | GCI needs 3 levels | Provide fine/medium/coarse |
| `Oscillatory convergence detected` | Non-monotone convergence | Check mesh quality or scheme |

## Interpretation Guidance

| Scenario | Meaning | Action |
|----------|---------|--------|
| Observed order matches expected | Strongest evidence of asymptotic range | Report GCI, extrapolate |
| Observed order < expected | Pre-asymptotic or coding bug | Refine further or debug |
| Negative observed order | Solution diverging | Check implementation |
| GCI asymptotic ratio near 1.0 | See caveat below | Confirm with order comparison |
| GCI asymptotic ratio far from 1.0 | Not in asymptotic range | Refine further |

> **Asymptotic-ratio caveat (constant refinement ratios).** When the refinement
> ratios are equal (`r21 == r32`, the common case), the asymptotic ratio
> `AR = GCI_coarse / (r^p * GCI_fine)` reduces algebraically to `f1/f2`. It then
> only measures the relative gap between the two finest QoI values — **not** whether
> the data follow the assumed power law — so an `AR` near 1.0 can give false
> reassurance even when the observed order is far from expected. The
> `gci_calculator.py` JSON emits a `notes` entry flagging this. For a real
> asymptotic-range determination:
> 1. Compare the observed order `p` to the scheme's theoretical/expected order — a
>    match is the meaningful evidence of being in the asymptotic range.
> 2. For stronger verification, use 4+ systematically refined grids and check that
>    the observed order is consistent across successive grid triplets
>    (`h_refinement.py` reports one order per triplet plus `mean_order`).

## Verification checklist

- [ ] Used >= 3 systematically refined grids/timesteps so `h_refinement.py` / `dt_refinement.py` can report a `results.mean_order`; recorded the per-triplet `results.observed_orders` (a single-pair Richardson run does not verify order).
- [ ] Recorded `results.mean_order` and confirmed `results.convergence_assessment` reads `PASS` (observed order within 10% of the scheme's expected order); a `FAIL` or `unknown` means the result is not yet verified.
- [ ] Confirmed `results.in_asymptotic_range` is `true` and that no `notes` entry reports pre-asymptotic (>50% order variation), negative/non-positive order, or zero error differences before quoting any GCI or extrapolated value.
- [ ] Checked refinement ratios `r21`/`r32` from `gci_calculator.py` are >= 1.3 (round-off noise floor) and that no `Oscillatory convergence detected` error was raised.
- [ ] Recorded `results.gci_fine` (with the safety factor used: 1.25 for >= 3 grids with verified order, 3.0 for 2 grids with assumed order) as the reported discretization uncertainty, plus `results.extrapolated_value` as the best estimate.
- [ ] For constant refinement ratios, did NOT treat `asymptotic_ratio` near 1.0 as proof of asymptotic range (it degenerates to `f1/f2`); confirmed the asymptotic range via observed-order-vs-expected and read the `gci_calculator.py` `notes` caveat.

## Common pitfalls & rationalizations

| Tempting shortcut | Why it's wrong / what to do |
|-------------------|------------------------------|
| "Two grids agree closely, so it's converged" | Two levels cannot estimate observed order. Run `h_refinement.py`/`dt_refinement.py` with >= 3 levels; a 2-grid Richardson run uses an *assumed* order and needs safety factor 3.0, not 1.25. |
| "The asymptotic ratio is ~1.0, so we're in the asymptotic range" | With constant refinement ratios `AR = GCI_coarse/(r^p*GCI_fine)` reduces to `f1/f2` and only measures the gap between the two finest QoI values. Verify the asymptotic range by comparing observed order to the expected order (and 4+ grid consistency). |
| "GCI_fine is tiny, so the solution is grid-independent" | A near-zero GCI can also mean the QoI is insensitive to refinement or the differences are in round-off noise (ratios < 1.3). Confirm `in_asymptotic_range` is true and refinement ratios are >= 1.3 first. |
| "Observed order is higher than expected, even better" | Order well above the formal order usually signals superconvergence or error cancellation, not extra accuracy. Treat it as a flag (`convergence_assessment` is FAIL when >10% off) and verify with more grid levels. |
| "The script printed an extrapolated value, so use it" | When the observed order is non-positive the solution is diverging and `h_refinement.py` returns `richardson_extrapolated_value = null` with a diverging note. Do not quote an extrapolated value or GCI in that case. |
| "Implicit/stable solver, so any timestep is fine for the study" | Temporal *stability* is not temporal *accuracy*. `dt_refinement.py` still needs >= 3 systematically reduced timesteps to recover the scheme's order; a too-coarse dt sequence stays pre-asymptotic. |

## Security

### Input Validation
- All numeric parameters (`spacings`, `timesteps`, `values`, `expected-order`, `order`) are validated as finite positive numbers
- Comma-separated value lists are length-matched (spacings and values must have equal length) and capped at 10,000 entries
- GCI calculator enforces exactly 3 refinement levels; Richardson extrapolation requires at least 2
- Safety factor is validated as a finite number not less than 1.0 (Roache uses Fs in {1.25, 3.0})

### File Access
- Scripts read no external files; all inputs are provided via CLI arguments
- Scripts write only to stdout (JSON output); no files are created unless the agent explicitly uses the Write tool

### Tool Restrictions
- **Bash**: Used to execute the four Python analysis scripts (`h_refinement.py`, `dt_refinement.py`, `richardson_extrapolation.py`, `gci_calculator.py`) with explicit argument lists
- **Read**: Used to inspect script source and reference documentation

### Safety Measures
- No `eval()`, `exec()`, or dynamic code generation
- All subprocess calls use explicit argument lists (no `shell=True`)
- Scripts use only Python standard library (`math` module); no pickle loading or deserialization of untrusted data
- Minimal tool surface (Bash and Read only) limits the agent's ability to modify the filesystem

## References

- `references/convergence_theory.md` - Formal convergence order, log-log analysis, asymptotic range
- `references/gci_guidelines.md` - Roache's GCI method, ASME V&V 20, safety factors

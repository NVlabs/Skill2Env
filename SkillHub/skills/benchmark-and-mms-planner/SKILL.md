---
name: benchmark-and-mms-planner
description: >
  Plan verification and validation campaigns for simulation codes using
  manufactured solutions, canonical benchmark problems, grid/time refinement,
  uncertainty propagation, and pass/fail acceptance criteria. Use when an
  agent needs to prove a solver, model, or result is trustworthy rather than
  only plausible.
allowed-tools: Read, Bash, Write, Grep, Glob
metadata:
  author: HeshamFS
  version: "1.1.3"
  security_tier: high
  security_reviewed: true
  tested_with:
    - claude-code
  last_evaluated: "2026-06-23"
  eval_cases: 3
  last_reviewed: "2026-06-24"
  standards:
    - "ASME V&V 20-2009 (Verification and Validation in Computational Fluid Dynamics and Heat Transfer)"
    - "Roache (1998), Verification and Validation in Computational Science and Engineering"
    - "Salari & Knupp (2000), Code Verification by the Method of Manufactured Solutions"
    - "Celik et al. (2008), GCI procedure (Richardson-extrapolation grid-convergence index)"
---

# Benchmark And MMS Planner

## Goal

Design a verification and validation plan before trusting simulation results. The skill helps agents choose manufactured solutions, benchmark cases, refinement protocols, uncertainty checks, and pass/fail criteria.

## Requirements

- Python 3.10+
- No external dependencies
- Works on Linux, macOS, and Windows

## Inputs to Gather

| Input | Description | Example |
|-------|-------------|---------|
| PDE or model class | Governing family | `diffusion`, `elasticity`, `phase-field` |
| Quantity of interest | Metric to validate | `interface velocity`, `L2 temperature error` |
| Dimension | 1, 2, or 3 | `2` |
| Expected order | Formal discretization order | `2` |
| Reference availability | Analytic, benchmark, or none | `analytic` |
| Risk level | Cost or consequence of wrong result | `high` |

## Decision Guidance

- Use **MMS** when code correctness is uncertain and an analytic solution can be injected.
- Use **canonical benchmarks** when physical model validation matters more than code verification.
- Use **grid/time refinement** whenever the result is used for a claim, design decision, or comparison.
- Use **uncertainty propagation** when inputs are calibrated, noisy, or experimentally measured.

## Script Outputs

`scripts/benchmark_mms_planner.py` emits `inputs` and `results` with:

- `verification_strategy`
- `effective_model` — the resolved model family actually used; unknown families fall back to `general`.
- `mms_plan`
- `benchmark_cases`
- `refinement_protocol` (`dimension`, `levels`, `spacing_ratio`, `expected_order`, `accept_observed_order_min`, `include_time_refinement`)
- `uncertainty_plan` (`propagate_inputs`, `report_error_bars`, `separate_discretization_and_model_error`) — propagation/error-bar guidance driven by risk level and reference type.
- `acceptance_criteria`
- `warnings`

The `accept_observed_order_min` is an **engineering screening heuristic**, not a certified bound: it is the formal `expected_order` reduced by a fractional tolerance (10% for high risk, 20% otherwise) and floored at first-order convergence (`1.0`). The relative band keeps strictness consistent across formal orders. See `references/vv_patterns.md`.

## Workflow

1. Collect the governing model, quantity of interest, and risk level.
2. Run `benchmark_mms_planner.py --json`.
3. Treat warnings as blockers for high-risk claims.
4. Convert the returned protocol into tests, simulation runs, or review checklist items.

```bash
python3 skills/verification-validation/benchmark-and-mms-planner/scripts/benchmark_mms_planner.py \
  --model diffusion \
  --quantity "L2 error in temperature" \
  --dimension 2 \
  --expected-order 2 \
  --reference analytic \
  --risk high \
  --json
```

## Error Handling

- If the dimension or expected order is invalid, stop and correct the model description.
- If no reference exists, use conservation and convergence checks but do not call the result validated.

## Limitations

This skill plans verification work; it does not run the solver or prove that a physical model is appropriate for an experiment.

## Verification checklist

Before trusting a result that used this planner, record concrete evidence for each item:

- [ ] Ran `benchmark_mms_planner.py --json` and saved the `inputs` block, confirming the echoed `dimension`, `expected_order`, `reference`, and `risk` match the actual run (a fallback to `effective_model: general` was intentional, not a typo in `--model`).
- [ ] Executed the `refinement_protocol`: used the reported `levels` (3, or 4 for high risk) of systematically refined grids at `spacing_ratio` 2, and recorded the observed order of accuracy from those runs.
- [ ] Confirmed the observed order is at or above `accept_observed_order_min`; if below, logged the investigation (mesh not yet asymptotic, boundary/source errors, limiter activation) rather than treating the result as passed.
- [ ] When `include_time_refinement` is `true`, ran a separate time-step refinement study and recorded the temporal observed order, not just the spatial one.
- [ ] When `mms_plan.manufacture_solution` is `true`, derived the symbolic source/forcing term, applied the matching boundary terms, and recorded the L2 and Linf error norms versus the manufactured solution.
- [ ] Checked every `acceptance_criteria` item with a number: conservation/balance closes within a documented tolerance, the quantity of interest plateaus under refinement, and any benchmark discrepancy from `benchmark_cases` is explained before production use.
- [ ] Treated all entries in `warnings` as blockers for high-risk claims and recorded how each was resolved (e.g. an independent analytic/published reference was added when `reference` was `none` or `experimental`).

## Common pitfalls & rationalizations

| Tempting shortcut | Why it's wrong / what to do |
|-------------------|-----------------------------|
| "The planner ran and printed a plan, so the result is verified." | The script only *plans* V&V; it never runs the solver. Verification comes from executing the `refinement_protocol`, MMS, and `acceptance_criteria`, not from generating the plan. |
| "Two grids converged, so the observed order is fine." | `refinement_protocol.levels` is 3 (4 for high risk) for a reason: you need >=3 systematically refined grids to estimate observed order and confirm the solution is in the asymptotic range before quoting it. |
| "Observed order beats `accept_observed_order_min`, so it's certified." | That threshold is an engineering *screening* heuristic (formal order minus a 10%/20% relative tolerance, floored at 1.0), not a certified bound. For rigorous order verification run a Richardson/GCI study. |
| "Steady-looking model, so I can skip `include_time_refinement`." | If the planner set `include_time_refinement: true` (any time-dependent or `general` fallback family), spatial refinement alone hides temporal error — run the time-step study too. |
| "We matched a benchmark, so the code is validated." | Matching `benchmark_cases` or converging shows the code approaches *some* solution; it does not prove the physical model is correct. Validation needs an independent reference plus model-error separation, not convergence alone. |
| "`reference none` is fine, the runs look physical." | With `reference: none` the strategy is verification-only; `warnings` says so. You may report convergence and conservation but must NOT call the result validated. |
| "Unknown model name, so I'll ignore the `general` fallback." | An unrecognized `--model` silently resolves to `effective_model: general`; confirm that fallback is intended, since it changes both `benchmark_cases` and the time-refinement decision. |

## Security

### Input Validation

All inputs are command-line arguments parsed by `argparse`; validation happens in `plan_vv` (and partly in the parser). Any rejected input causes the script to print the error to stderr and exit with code `2`.

- `dimension` must be exactly `1`, `2`, or `3`; any other integer is rejected.
- `expected_order` must be a positive, finite number (NaN, infinity, zero, and negatives are rejected).
- `risk` must be one of the allowlist `low`, `medium`, `high` (enforced both as an `argparse` choice and re-checked in `plan_vv`).
- `reference` must be one of the allowlist `analytic`, `benchmark`, `experimental`, `none` (enforced both as an `argparse` choice and re-checked in `plan_vv`).
- `model` and `quantity` are capped at 256 characters (`MAX_FIELD_LEN`); longer strings are rejected.
- The string content of `model` and `quantity` is otherwise not allowlisted or sanitized: `quantity` is echoed verbatim into the output, and an unrecognized `model` family is silently resolved to `general` rather than rejected.

### File Access

- The script reads and writes no files; all I/O is command-line args -> stdout JSON (or a short plain-text summary), with errors on stderr.
- Because no filesystem paths are accepted or constructed, there is no path-traversal surface and no path-sandboxing logic is needed.
- The only DoS-relevant size limit is the 256-character cap on `model` and `quantity`; numeric outputs are bounded by the validated inputs.

### Tool Restrictions

The frontmatter declares `allowed-tools: Read, Bash, Write, Grep, Glob`.

- `Bash` is used solely to run the bundled `scripts/benchmark_mms_planner.py` (e.g. the `python3 ... --json` invocation in the Workflow).
- `Read`, `Grep`, and `Glob` are for inspecting the skill's own files and references (e.g. `references/vv_patterns.md`) when planning.
- `Write` supports turning the returned protocol into test stubs or checklist files; the planner script itself never writes.

### Safety Measures

- No `eval`, `exec`, or dynamic code execution; the planner is pure Python computing a dictionary.
- The script spawns no subprocesses and invokes no external solvers, so there are no subprocess argument lists to escape.
- No `pickle` or other deserialization of untrusted data is performed; output is serialized with `json.dumps`.
- The 256-character field cap is the explicit DoS guard against pathological input strings.

## References

- See `references/vv_patterns.md` for MMS, benchmark, and uncertainty planning notes.

## Version History

- 1.1.3: Add a "Verification checklist" (evidence-based items tied to the planner's
  `refinement_protocol`, `mms_plan`, `acceptance_criteria`, and `warnings`) and a
  "Common pitfalls & rationalizations" table that pins down domain-specific V&V
  shortcuts (plan != verification, >=3 grids for observed order, screening band is not
  a certified bound, time refinement, convergence != validation, `reference none`,
  `general` fallback).
- 1.1.1: Make the eval suite discriminating by adding deterministic `script_checks`
  that pin the planner's specific output (resolved `verification_strategy`, the
  relative `accept_observed_order_min` band, refinement `levels`,
  `include_time_refinement`, `uncertainty_plan` flags, model-specific benchmark
  cases, and the exact warning strings) for each of the three cases.
- 1.1.0: Resolve unknown model families to `general` once so benchmark selection and the
  time-refinement decision agree (transient unlisted PDEs no longer skip time refinement);
  echo the resolved family as `effective_model`. Replace the fixed absolute observed-order
  offset with a relative tolerance floored at first order. Document `uncertainty_plan`,
  `effective_model`, and the acceptance heuristic. Add 256-character caps on string inputs.
- 1.0.0: Initial benchmark and MMS planning skill.

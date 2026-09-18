---
name: linear-solvers
description: >
  Select and configure linear solvers for Ax=b systems arising in numerical
  simulations — choose between direct (LU, Cholesky) and iterative (CG, GMRES,
  BiCGSTAB, MINRES) methods, analyze sparsity patterns and matrix conditioning,
  recommend preconditioners (AMG, ILU, IC), apply row/column scaling, and
  diagnose convergence stagnation from residual histories. Use when setting up
  a linear solve for FEM/FVM assembly, debugging slow or stalled Krylov
  iterations, choosing a preconditioner for SPD or nonsymmetric systems, or
  investigating ill-conditioning, even if the user only says "my solver is
  slow" or "GMRES won't converge."
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
    - "Saad (2003), Iterative Methods for Sparse Linear Systems (Krylov methods, ILU/ILUT, preconditioning)"
    - "Hestenes & Stiefel (1952) Conjugate Gradient method and the (√κ−1)/(√κ+1) error bound"
    - "Saad & Schultz (1986), GMRES restarted Krylov method"
    - "Ruge & Stüben (1987), Algebraic Multigrid (AMG) classical coarsening"
    - "Ruiz (2001) equilibration; Sinkhorn & Knopp (1967) doubly-stochastic scaling"
---

# Linear Solvers

## Goal

Provide a universal workflow to select a solver, assess conditioning, and diagnose convergence for linear systems arising in numerical simulations.

## Requirements

- Python 3.10+
- NumPy, SciPy (for matrix operations)
- See individual scripts for dependencies

## Inputs to Gather

| Input | Description | Example |
|-------|-------------|---------|
| Matrix size | Dimension of system | `n = 1000000` |
| Sparsity | Fraction of nonzeros | `0.01%` |
| Symmetry | Is A = Aᵀ? | `yes` |
| Definiteness | Is A positive definite? | `yes (SPD)` |
| Conditioning | Estimated condition number | `10⁶` |

## Decision Guidance

### Solver Selection Flowchart

```
Is matrix dense and small enough to factor in memory (dense float64
storage n²·8 bytes < ~2 GB, i.e. n ≲ 16000)?
├── YES → Use direct solver (Cholesky/LDLᵀ/LU by symmetry)
└── NO → Is matrix symmetric?
    ├── YES → Is it positive definite?
    │   ├── YES → Use CG with AMG/IC preconditioner
    │   └── NO → Use MINRES
    └── NO → Is it nearly symmetric?
        ├── YES → Use BiCGSTAB
        └── NO → Use GMRES with ILU/AMG
```

### Quick Reference

| Matrix Type | Solver | Preconditioner |
|-------------|--------|----------------|
| SPD, sparse | CG | AMG, IC |
| Symmetric indefinite | MINRES | SPD preconditioner (SSOR, symmetric block-diagonal, or AMG on SPD part) |
| Nonsymmetric | GMRES, BiCGSTAB | ILU, AMG |
| Dense | LU, Cholesky | None |
| Saddle point | Schur complement, Uzawa | Block preconditioner |

## Script Outputs (JSON Fields)

| Script | Key Outputs |
|--------|-------------|
| `scripts/solver_selector.py` | `recommended`, `alternatives`, `notes` |
| `scripts/convergence_diagnostics.py` | `rate`, `asymptotic_rate`, `stagnation`, `recommended_action` |
| `scripts/sparsity_stats.py` | `nnz`, `density`, `bandwidth`, `symmetry` |
| `scripts/preconditioner_advisor.py` | `suggested`, `notes` |
| `scripts/scaling_equilibration.py` | `row_scale`, `col_scale`, `notes` |
| `scripts/residual_norms.py` | `residual_norms`, `relative_norms`, `converged` |

## Workflow

1. **Characterize matrix** - symmetry, definiteness, sparsity
2. **Analyze sparsity** - Run `scripts/sparsity_stats.py`
3. **Select solver** - Run `scripts/solver_selector.py`
4. **Choose preconditioner** - Run `scripts/preconditioner_advisor.py`
5. **Apply scaling** - If ill-conditioned, use `scripts/scaling_equilibration.py`
6. **Monitor convergence** - Use `scripts/convergence_diagnostics.py`
7. **Diagnose issues** - Check residual history with `scripts/residual_norms.py`

## Conversational Workflow Example

**User**: My GMRES solver is stagnating after 50 iterations. The residual drops to 1e-3 then stops improving.

**Agent workflow**:
1. Diagnose convergence:
   ```bash
   python3 scripts/convergence_diagnostics.py --residuals 1,0.1,0.01,0.005,0.003,0.002,0.002,0.002 --json
   ```
2. Check for preconditioning advice:
   ```bash
   python3 scripts/preconditioner_advisor.py --matrix-type nonsymmetric --sparse --ill-conditioned --json
   ```
3. Recommend: Increase restart parameter, try ILU(k) with higher k, or switch to AMG.

## Pre-Solve Checklist

- [ ] Confirm matrix symmetry/definiteness
- [ ] Decide direct vs iterative based on size and sparsity
- [ ] Set residual tolerance relative to physics scale
- [ ] Choose preconditioner appropriate to matrix structure
- [ ] Apply scaling/equilibration if needed
- [ ] Track convergence and adjust if stagnation occurs

## CLI Examples

```bash
# Analyze sparsity pattern
python3 scripts/sparsity_stats.py --matrix A.npy --json

# Select solver for SPD sparse system
python3 scripts/solver_selector.py --symmetric --positive-definite --sparse --size 1000000 --json

# Get preconditioner recommendation
python3 scripts/preconditioner_advisor.py --matrix-type spd --sparse --json

# Diagnose convergence from residual history
python3 scripts/convergence_diagnostics.py --residuals 1,0.2,0.05,0.01 --json

# Apply scaling
python3 scripts/scaling_equilibration.py --matrix A.npy --symmetric --json

# Compute residual norms
python3 scripts/residual_norms.py --residual 1,0.1,0.01 --rhs 1,0,0 --json
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| `Matrix file not found` | Invalid path | Check file exists |
| `Matrix must be square` | Non-square input | Verify matrix dimensions |
| `Residuals must be positive` | Invalid residual data | Check input format |

## Interpretation Guidance

### Convergence Rate

`convergence_diagnostics.py` reports two rates: `rate` (mean of all per-iteration
residual ratios over the full history) and `asymptotic_rate` (mean over a short
trailing window). The `stagnation` flag is driven by `asymptotic_rate` (> 0.95),
because stagnation is a tail property — early fast drops can hide a flat tail.
Read `asymptotic_rate` when judging the regime below:

| Asymptotic rate | Meaning | Action |
|-----------------|---------|--------|
| < 0.1 | Excellent | Current setup optimal |
| 0.1 - 0.5 | Good | Acceptable for most problems |
| 0.5 - 0.95 | Slow | Consider better preconditioner |
| > 0.95 | Stagnation | Change solver or preconditioner |

### Stagnation Diagnosis

| Pattern | Likely Cause | Fix |
|---------|--------------|-----|
| Flat residual | Poor preconditioner | Improve preconditioner |
| Oscillating | Near-singular or indefinite | Check matrix, try different solver |
| Very slow decay | Ill-conditioned | Apply scaling, use AMG |

## Verification checklist

Do not trust a solve until each of these is satisfied with a recorded value, not a "looks fine":

- [ ] Recorded `asymptotic_rate` from `convergence_diagnostics.py` and confirmed it is below the 0.95 stagnation threshold (and ideally < 0.5); a low whole-history `rate` alone does not rule out a flat tail.
- [ ] Checked the relative residual from `residual_norms.py` against the physics-scaled `--rel-tol` (default 1e-6), not just the absolute norm; for unscaled RHS use `--require-both` so an undersized `rhs` cannot fake convergence.
- [ ] Confirmed `solver_selector.py` `recommended` matches the actual matrix properties recorded from `sparsity_stats.py` (`symmetry`, and definiteness if known) — e.g. CG only when symmetric AND positive-definite, MINRES for symmetric-indefinite, GMRES/BiCGSTAB for nonsymmetric.
- [ ] For systems flagged ill-conditioned, ran `scaling_equilibration.py` and recorded `row_scale_max/row_scale_min` and `col_scale_max/col_scale_min`; for symmetric matrices used `--symmetric` (D A D) so symmetry is preserved, and applied row_scale THEN col_scale for nonsymmetric two-sided scaling.
- [ ] Reviewed `sparsity_stats.py` `notes`/`zero_rows`/`zero_cols` from `scaling_equilibration.py` — any zero row or column means the system is structurally singular and the scale-of-1 fallback is not a fix.
- [ ] Confirmed the preconditioner from `preconditioner_advisor.py` is admissible for the chosen Krylov method — in particular a MINRES preconditioner must be SPD (an indefinite incomplete LDLᵀ is invalid).

## Common pitfalls & rationalizations

| Tempting shortcut | Why it's wrong / what to do |
|-------------------|-----------------------------|
| "The mean `rate` is low, so it converged." | `rate` is the whole-history mean and is dominated by early fast drops; stagnation is a tail property. Read `asymptotic_rate` and confirm it is below 0.95. |
| "The absolute residual is tiny, so we're done." | A small absolute norm can be meaningless if the RHS is large or unscaled. Check the `relative_norms` / `relative_value` against a physics-scaled `--rel-tol`. |
| "It's symmetric, so just use CG." | CG requires symmetric AND positive-definite. A symmetric-indefinite matrix needs MINRES (with an SPD preconditioner); using CG can break down or stall. Confirm definiteness before selecting. |
| "Large system, so factor it directly." | `solver_selector.py` gates dense direct solvers on dense float64 storage (n²·8 bytes < ~2 GB, n ≈ 16384); above that a dense Cholesky/LU is infeasible and you must route to an iterative method. |
| "Scaling is just dividing each row by its max." | One-sided row scaling does not equilibrate. For nonsymmetric matrices derive `col_scale` from the row-scaled matrix and apply both; for symmetric matrices use the symmetric D A D scale or you destroy symmetry. |
| "GMRES stagnates, so add more iterations." | A flat tail means the preconditioner or restart length is the problem, not iteration count. Strengthen the preconditioner (higher ILU fill / AMG), increase the restart parameter, or switch methods. |

## Security

### Input Validation
- All numeric inputs (residuals, tolerances, matrix entries) are validated as finite numbers
- Comma-separated residual/vector inputs are capped at 100,000 entries
- The `solver_selector.py` `--size` parameter is bounded at 10 billion
- `--matrix-type` is validated against a fixed allowlist (`spd`, `symmetric-indefinite`, `nonsymmetric`)
- Boolean flags (`--symmetric`, `--positive-definite`, `--sparse`, `--ill-conditioned`) are type-safe argparse flags

### File Access
- `sparsity_stats.py` and `scaling_equilibration.py` read a single matrix file (`.npy` format) specified by `--matrix`
- `np.load()` is called with `allow_pickle=False` to prevent arbitrary code execution via crafted `.npy` files
- Matrix files are rejected if they exceed 500 MB before any parsing occurs
- Matrix dimension limits (100,000 per dimension) prevent memory exhaustion
- All other scripts read no external files; inputs are provided via CLI arguments

### Tool Restrictions
- **Read**: Used to inspect script source, references, and matrix files
- **Write**: Used to save analysis results or solver recommendations; writes are scoped to the user's working directory
- **Grep/Glob**: Used to locate relevant files and search references
- The skill's `allowed-tools` excludes `Bash` to prevent the agent from executing arbitrary commands when processing untrusted matrix files or numeric inputs

### Safety Measures
- No `eval()`, `exec()`, or dynamic code generation
- All subprocess calls use explicit argument lists (no `shell=True`)
- Reduced tool surface (no Bash) limits the agent to read/write operations only
- JSON output mode produces structured, parseable results without shell-interpretable content

## Limitations

- **Large dense matrices**: Direct solvers may run out of memory
- **Highly indefinite**: Standard preconditioners may fail
- **Saddle-point**: Requires specialized block preconditioners

## References

- `references/solver_decision_tree.md` - Selection logic
- `references/preconditioner_catalog.md` - Preconditioner options
- `references/convergence_patterns.md` - Diagnosing failures
- `references/scaling_guidelines.md` - Equilibration guidance

## Version History

- **v1.2.0** (2026-06-23): Fixed asymptotic stagnation detection, dense-feasibility solver gating, saddle-point/small-dense direct-solver routing, equilibrating two-sided scaling, CG iteration-bound table, and doc/eval consistency
- **v1.1.0** (2024-12-24): Enhanced documentation, decision guidance, examples
- **v1.0.0**: Initial release with 6 solver analysis scripts

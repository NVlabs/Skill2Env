---
name: alterlab-pymoo
description: Multi-objective optimization with pymoo — NSGA-II, NSGA-III, MOEA/D, Pareto-front computation, constraint handling, and standard benchmarks (ZDT, DTLZ). Use when solving multi-objective or constrained optimization problems, computing Pareto-optimal trade-offs, or tackling engineering design problems with competing objectives. Part of the AlterLab Academic Skills suite.
license: Apache-2.0
allowed-tools: Read Write Edit Bash(python:*) Bash(uv:*)
compatibility: No API key required. Runs locally via `uv run python`; requires the pymoo Python package.
metadata:
    skill-author: AlterLab
    version: "1.0.0"
---

# Pymoo - Multi-Objective Optimization in Python

## Overview

Pymoo is a comprehensive Python framework for optimization with emphasis on multi-objective problems. Solve single and multi-objective optimization using state-of-the-art algorithms (NSGA-II/III, MOEA/D), benchmark problems (ZDT, DTLZ), customizable genetic operators, and multi-criteria decision making methods. Excels at finding trade-off solutions (Pareto fronts) for problems with conflicting objectives.

## When to Use This Skill

This skill should be used when:
- Solving optimization problems with one or multiple objectives
- Finding Pareto-optimal solutions and analyzing trade-offs
- Implementing evolutionary algorithms (GA, DE, PSO, NSGA-II/III)
- Working with constrained optimization problems
- Benchmarking algorithms on standard test problems (ZDT, DTLZ, WFG)
- Customizing genetic operators (crossover, mutation, selection)
- Visualizing high-dimensional optimization results
- Making decisions from multiple competing solutions
- Handling binary, discrete, continuous, or mixed-variable problems

## Core Concepts

### The Unified Interface

Pymoo uses a consistent `minimize()` function for all optimization tasks:

```python
from pymoo.optimize import minimize

result = minimize(
    problem,        # What to optimize
    algorithm,      # How to optimize
    termination,    # When to stop
    seed=1,
    verbose=True
)
```

**Result object contains:**
- `result.X`: Decision variables of optimal solution(s)
- `result.F`: Objective values of optimal solution(s)
- `result.G`: Constraint violations (if constrained)
- `result.algorithm`: Algorithm object with history

### Problem Types

**Single-objective:** One objective to minimize/maximize
**Multi-objective:** 2-3 conflicting objectives → Pareto front
**Many-objective:** 4+ objectives → High-dimensional Pareto front
**Constrained:** Objectives + inequality/equality constraints
**Dynamic:** Time-varying objectives or constraints

## Core Workflow

1. **Pick problem type** — single, multi (2-3 obj), many (4+ obj), or constrained.
2. **Define or select the problem** — built-in via `get_problem(...)`, or subclass `ElementwiseProblem` for custom (objectives in `out["F"]`, inequality constraints `g(x) <= 0` in `out["G"]`, equality `h(x) = 0` in `out["H"]`).
3. **Choose the algorithm** — NSGA-II for 2-3 objectives, NSGA-III (with reference directions) for 4+, GA/DE/PSO/CMA-ES for single-objective. See the selection tables in `references/quick_reference.md`.
4. **Set termination** — `('n_gen', N)` or `get_termination("f_tol", tol=0.001)`.
5. **Run** with `minimize(problem, algorithm, termination, seed=1, verbose=True)`.
6. **Inspect** `result.X` / `result.F` / `result.G` (or `result.CV` for constraint violation).
7. **Decide & visualize** — apply MCDM to pick a preferred Pareto solution, plot with `Scatter`/`PCP`/`Petal`.

Always set `seed` for reproducibility, normalize objectives when scales differ, and provide reference directions for NSGA-III.

## Routing — where to look

| You need… | Go to |
|-----------|-------|
| Complete copy-paste examples for all 7 workflows (single/multi/many-objective, custom problems, constraint handling, MCDM decision making, visualization) | `references/workflows.md` |
| Algorithm-selection tables, benchmark problem list, operator config, troubleshooting, best practices, install | `references/quick_reference.md` |
| Deep algorithm reference (parameters, usage, selection) | `references/algorithms.md` |
| Benchmark test problems (ZDT, DTLZ, WFG) with characteristics | `references/problems.md` |
| Genetic operators (sampling, selection, crossover, mutation) | `references/operators.md` |
| All visualization types with examples | `references/visualization.md` |
| Constraint handling + multi-criteria decision making | `references/constraints_mcdm.md` |

**Runnable scripts** (`scripts/`): `single_objective_example.py`, `multi_objective_example.py`, `many_objective_example.py`, `custom_problem_example.py`, `decision_making_example.py`. Run with `uv run python scripts/<name>.py`.

**Search references:** `grep -r "NSGA-II\|NSGA-III\|MOEA/D" references/` · `grep -r "Feasibility First\|Penalty\|Repair" references/` · `grep -r "Scatter\|PCP\|Petal" references/`

## Install

```bash
uv pip install pymoo
```

Dependencies: NumPy, SciPy, matplotlib, autograd (optional). Docs: https://pymoo.org/ — this skill targets pymoo 0.6.x.


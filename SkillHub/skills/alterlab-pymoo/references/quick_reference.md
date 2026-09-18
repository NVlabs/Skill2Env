# Pymoo Quick Reference — Algorithms, Benchmarks, Operators, Troubleshooting

Selection tables and short snippets. For deep detail see the topic-specific references
(`algorithms.md`, `problems.md`, `operators.md`, `visualization.md`, `constraints_mcdm.md`).

## Algorithm Selection Guide

### Single-Objective Problems

| Algorithm | Best For | Key Features |
|-----------|----------|--------------|
| **GA** | General-purpose | Flexible, customizable operators |
| **DE** | Continuous optimization | Good global search |
| **PSO** | Smooth landscapes | Fast convergence |
| **CMA-ES** | Difficult/noisy problems | Self-adapting |

### Multi-Objective Problems (2-3 objectives)

| Algorithm | Best For | Key Features |
|-----------|----------|--------------|
| **NSGA-II** | Standard benchmark | Fast, reliable, well-tested |
| **R-NSGA-II** | Preference regions | Reference point guidance |
| **MOEA/D** | Decomposable problems | Scalarization approach |

### Many-Objective Problems (4+ objectives)

| Algorithm | Best For | Key Features |
|-----------|----------|--------------|
| **NSGA-III** | 4-15 objectives | Reference direction-based |
| **RVEA** | Adaptive search | Reference vector evolution |
| **AGE-MOEA** | Complex landscapes | Adaptive geometry |

### Constrained Problems

| Approach | Algorithm | When to Use |
|----------|-----------|-------------|
| Feasibility-first | Any algorithm | Large feasible region |
| Specialized | SRES, ISRES | Heavy constraints |
| Penalty | GA + penalty | Algorithm compatibility |

See `references/algorithms.md` for the comprehensive algorithm reference.

## Benchmark Problems

```python
from pymoo.problems import get_problem

# Single-objective
problem = get_problem("rastrigin", n_var=10)
problem = get_problem("rosenbrock", n_var=10)

# Multi-objective
problem = get_problem("zdt1")        # Convex front
problem = get_problem("zdt2")        # Non-convex front
problem = get_problem("zdt3")        # Disconnected front

# Many-objective
problem = get_problem("dtlz2", n_obj=5, n_var=12)
problem = get_problem("dtlz7", n_obj=4)
```

See `references/problems.md` for the complete test problem reference.

## Genetic Operator Customization

### Standard operator configuration
```python
from pymoo.algorithms.soo.nonconvex.ga import GA
from pymoo.operators.crossover.sbx import SBX
from pymoo.operators.mutation.pm import PM

algorithm = GA(
    pop_size=100,
    crossover=SBX(prob=0.9, eta=15),
    mutation=PM(eta=20),
    eliminate_duplicates=True
)
```

### Operator selection by variable type

**Continuous variables:**
- Crossover: SBX (Simulated Binary Crossover)
- Mutation: PM (Polynomial Mutation)

**Binary variables:**
- Crossover: TwoPointCrossover, UniformCrossover
- Mutation: BitflipMutation

**Permutations (TSP, scheduling):**
- Crossover: OrderCrossover (OX)
- Mutation: InversionMutation

See `references/operators.md` for the comprehensive operator reference.

## Performance and Troubleshooting

**Problem: Algorithm not converging**
- Increase population size
- Increase number of generations
- Check if problem is multimodal (try different algorithms)
- Verify constraints are correctly formulated

**Problem: Poor Pareto front distribution**
- For NSGA-III: Adjust reference directions
- Increase population size
- Check for duplicate elimination
- Verify problem scaling

**Problem: Few feasible solutions**
- Use constraint-as-objective approach
- Apply repair operators
- Try SRES/ISRES for constrained problems
- Check constraint formulation (should be g <= 0)

**Problem: High computational cost**
- Reduce population size
- Decrease number of generations
- Use simpler operators
- Enable parallelization (if problem supports)

### Best practices

1. **Normalize objectives** when scales differ significantly
2. **Set random seed** for reproducibility
3. **Save history** to analyze convergence: `save_history=True`
4. **Visualize results** to understand solution quality
5. **Compare with true Pareto front** when available
6. **Use appropriate termination criteria** (generations, evaluations, tolerance)
7. **Tune operator parameters** for problem characteristics

## Common patterns

- Always use `ElementwiseProblem` for custom problems
- Constraints formulated as `g(x) <= 0` and `h(x) = 0`
- Reference directions required for NSGA-III
- Normalize objectives before MCDM
- Use appropriate termination: `('n_gen', N)` or `get_termination("f_tol", tol=0.001)`

## Installation and environment

```bash
uv pip install pymoo
```

**Dependencies:** NumPy, SciPy, matplotlib, autograd (optional for gradient-based).
**Documentation:** https://pymoo.org/ — this skill is based on pymoo 0.6.x.

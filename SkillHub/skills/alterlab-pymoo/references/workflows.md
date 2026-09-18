# Pymoo Workflows — Worked Examples

Complete, copy-pasteable examples for each common optimization task. Each maps to a runnable script in `scripts/`.

## Workflow 1: Single-Objective Optimization

**When:** Optimizing one objective function.

**Steps:** Define/select problem → choose single-objective algorithm (GA, DE, PSO, CMA-ES) → configure termination → run → extract best solution.

```python
from pymoo.algorithms.soo.nonconvex.ga import GA
from pymoo.problems import get_problem
from pymoo.optimize import minimize

# Built-in problem
problem = get_problem("rastrigin", n_var=10)

# Configure Genetic Algorithm
algorithm = GA(
    pop_size=100,
    eliminate_duplicates=True
)

# Optimize
result = minimize(
    problem,
    algorithm,
    ('n_gen', 200),
    seed=1,
    verbose=True
)

print(f"Best solution: {result.X}")
print(f"Best objective: {result.F[0]}")
```

See `scripts/single_objective_example.py` for the complete example.

## Workflow 2: Multi-Objective Optimization (2-3 objectives)

**When:** Optimizing 2-3 conflicting objectives, need Pareto front.

**Algorithm choice:** NSGA-II (standard for bi/tri-objective).

**Steps:** Define multi-objective problem → configure NSGA-II → run to obtain Pareto front → visualize trade-offs → apply decision making (optional).

```python
from pymoo.algorithms.moo.nsga2 import NSGA2
from pymoo.problems import get_problem
from pymoo.optimize import minimize
from pymoo.visualization.scatter import Scatter

# Bi-objective benchmark problem
problem = get_problem("zdt1")

# NSGA-II algorithm
algorithm = NSGA2(pop_size=100)

# Optimize
result = minimize(problem, algorithm, ('n_gen', 200), seed=1)

# Visualize Pareto front
plot = Scatter()
plot.add(result.F, label="Obtained Front")
plot.add(problem.pareto_front(), label="True Front", alpha=0.3)
plot.show()

print(f"Found {len(result.F)} Pareto-optimal solutions")
```

See `scripts/multi_objective_example.py` for the complete example.

## Workflow 3: Many-Objective Optimization (4+ objectives)

**When:** Optimizing 4 or more objectives.

**Algorithm choice:** NSGA-III (designed for many objectives).

**Key difference:** Must provide reference directions for population guidance.

**Steps:** Define many-objective problem → generate reference directions → configure NSGA-III with reference directions → run → visualize using Parallel Coordinate Plot.

```python
from pymoo.algorithms.moo.nsga3 import NSGA3
from pymoo.problems import get_problem
from pymoo.optimize import minimize
from pymoo.util.ref_dirs import get_reference_directions
from pymoo.visualization.pcp import PCP

# Many-objective problem (5 objectives)
problem = get_problem("dtlz2", n_obj=5)

# Generate reference directions (required for NSGA-III)
ref_dirs = get_reference_directions("das-dennis", n_dim=5, n_partitions=12)

# Configure NSGA-III
algorithm = NSGA3(ref_dirs=ref_dirs)

# Optimize
result = minimize(problem, algorithm, ('n_gen', 300), seed=1)

# Visualize with Parallel Coordinates
plot = PCP(labels=[f"f{i+1}" for i in range(5)])
plot.add(result.F, alpha=0.3)
plot.show()
```

See `scripts/many_objective_example.py` for the complete example.

## Workflow 4: Custom Problem Definition

**When:** Solving a domain-specific optimization problem.

**Steps:** Extend `ElementwiseProblem` → define `__init__` with dimensions and bounds → implement `_evaluate` for objectives (and constraints) → use with any algorithm.

**Unconstrained example:**
```python
from pymoo.core.problem import ElementwiseProblem
import numpy as np

class MyProblem(ElementwiseProblem):
    def __init__(self):
        super().__init__(
            n_var=2,              # Number of variables
            n_obj=2,              # Number of objectives
            xl=np.array([0, 0]),  # Lower bounds
            xu=np.array([5, 5])   # Upper bounds
        )

    def _evaluate(self, x, out, *args, **kwargs):
        # Define objectives
        f1 = x[0]**2 + x[1]**2
        f2 = (x[0]-1)**2 + (x[1]-1)**2

        out["F"] = [f1, f2]
```

**Constrained example:**
```python
class ConstrainedProblem(ElementwiseProblem):
    def __init__(self):
        super().__init__(
            n_var=2,
            n_obj=2,
            n_ieq_constr=2,        # Inequality constraints
            n_eq_constr=1,         # Equality constraints
            xl=np.array([0, 0]),
            xu=np.array([5, 5])
        )

    def _evaluate(self, x, out, *args, **kwargs):
        # Objectives
        out["F"] = [f1, f2]

        # Inequality constraints (g <= 0)
        out["G"] = [g1, g2]

        # Equality constraints (h = 0)
        out["H"] = [h1]
```

**Constraint formulation rules:**
- Inequality: Express as `g(x) <= 0` (feasible when ≤ 0)
- Equality: Express as `h(x) = 0` (feasible when = 0)
- Convert `g(x) >= b` to `-(g(x) - b) <= 0`

See `scripts/custom_problem_example.py` for complete examples.

## Workflow 5: Constraint Handling

**When:** Problem has feasibility constraints.

**1. Feasibility First (Default — Recommended)**
```python
from pymoo.algorithms.moo.nsga2 import NSGA2

# Works automatically with constrained problems
algorithm = NSGA2(pop_size=100)
result = minimize(problem, algorithm, termination)

# Check feasibility
feasible = result.CV[:, 0] == 0  # CV = constraint violation
print(f"Feasible solutions: {np.sum(feasible)}")
```

**2. Penalty Method**
```python
from pymoo.constraints.as_penalty import ConstraintsAsPenalty

# Wrap problem to convert constraints to penalties
problem_penalized = ConstraintsAsPenalty(problem, penalty=1e6)
```

**3. Constraint as Objective**
```python
from pymoo.constraints.as_obj import ConstraintsAsObjective

# Treat constraint violation as additional objective
problem_with_cv = ConstraintsAsObjective(problem)
```

**4. Specialized Algorithms**
```python
from pymoo.algorithms.soo.nonconvex.sres import SRES

# SRES has built-in constraint handling
algorithm = SRES()
```

See `references/constraints_mcdm.md` for the comprehensive constraint handling guide.

## Workflow 6: Decision Making from Pareto Front

**When:** Have Pareto front, need to select preferred solution(s).

**Steps:** Run multi-objective optimization → normalize objectives to [0, 1] → define preference weights → apply MCDM method → visualize selected solution.

**Example using Pseudo-Weights:**
```python
from pymoo.mcdm.pseudo_weights import PseudoWeights
import numpy as np

# After obtaining result from multi-objective optimization
# Normalize objectives
F_norm = (result.F - result.F.min(axis=0)) / (result.F.max(axis=0) - result.F.min(axis=0))

# Define preferences (must sum to 1)
weights = np.array([0.3, 0.7])  # 30% f1, 70% f2

# Apply decision making
dm = PseudoWeights(weights)
selected_idx = dm.do(F_norm)

# Get selected solution
best_solution = result.X[selected_idx]
best_objectives = result.F[selected_idx]

print(f"Selected solution: {best_solution}")
print(f"Objective values: {best_objectives}")
```

**Other MCDM methods:**
- Compromise Programming: Select closest to ideal point
- Knee Point: Find balanced trade-off solutions
- Hypervolume Contribution: Select most diverse subset

See `scripts/decision_making_example.py` and `references/constraints_mcdm.md` for detailed MCDM methods.

## Workflow 7: Visualization

**Choose visualization based on number of objectives.**

**2 objectives: Scatter Plot**
```python
from pymoo.visualization.scatter import Scatter

plot = Scatter(title="Bi-objective Results")
plot.add(result.F, color="blue", alpha=0.7)
plot.show()
```

**3 objectives: 3D Scatter**
```python
plot = Scatter(title="Tri-objective Results")
plot.add(result.F)  # Automatically renders in 3D
plot.show()
```

**4+ objectives: Parallel Coordinate Plot**
```python
from pymoo.visualization.pcp import PCP

plot = PCP(
    labels=[f"f{i+1}" for i in range(n_obj)],
    normalize_each_axis=True
)
plot.add(result.F, alpha=0.3)
plot.show()
```

**Solution comparison: Petal Diagram**
```python
from pymoo.visualization.petal import Petal

plot = Petal(
    bounds=[result.F.min(axis=0), result.F.max(axis=0)],
    labels=["Cost", "Weight", "Efficiency"]
)
plot.add(solution_A, label="Design A")
plot.add(solution_B, label="Design B")
plot.show()
```

See `references/visualization.md` for all visualization types and usage.

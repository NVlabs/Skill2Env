# Mesa 3 Patterns — Validated Skeletons and the Validation Checklist

Loaded on demand from the abm-mesa SKILL.md. All code is verified against Mesa 3.x current docs
(mesa.readthedocs.io; PyPI mesa 3.5.x). Mesa 3 removed `mesa.time` schedulers — use the AgentSet
API on `model.agents`.

## Migration cheat-sheet (Mesa 2 → 3)

| Mesa 2 (do NOT use) | Mesa 3 (current) |
|---------------------|------------------|
| `Agent(unique_id, model)` | `Agent(model)` — `unique_id` auto-assigned |
| `self.schedule = RandomActivation(self)` | (nothing) — agents auto-register in `model.agents` |
| `self.schedule.add(agent)` | (automatic on creation); remove with `agent.remove()` |
| `self.schedule.step()` | `self.agents.shuffle_do("step")` |
| `mesa.time.SimultaneousActivation` | `self.agents.do("step")` then `self.agents.do("advance")` |
| `self.schedule.agents` | `self.agents` |
| — | `super().__init__(seed=seed)` is **mandatory** in the Model |

## Schelling segregation on a grid (cell space)

```python
import mesa
from mesa.discrete_space import OrthogonalMooreGrid, CellAgent

class Resident(CellAgent):
    def __init__(self, model, group):
        super().__init__(model)
        self.group = group

    def step(self):
        neighbors = self.cell.neighborhood.agents
        same = sum(1 for a in neighbors if a.group == self.group)
        total = len(list(neighbors))
        if total and same / total < self.model.tolerance:
            self.cell = self.model.grid.select_random_empty_cell()   # move

class Schelling(mesa.Model):
    def __init__(self, width=20, height=20, density=0.8, tolerance=0.3, seed=None):
        super().__init__(seed=seed)
        self.tolerance = tolerance
        self.grid = OrthogonalMooreGrid((width, height), torus=True, random=self.random)
        for cell in self.grid.all_cells:
            if self.random.random() < density:
                Resident(self, group=self.random.choice([0, 1])).cell = cell
        self.datacollector = mesa.DataCollector(
            model_reporters={"happy_frac": lambda m: m._happy_fraction()})

    def _happy_fraction(self):
        # fraction of agents meeting their tolerance threshold
        ok = 0
        for a in self.agents:
            nb = list(a.cell.neighborhood.agents)
            same = sum(1 for o in nb if o.group == a.group)
            ok += 1 if (not nb or same / len(nb) >= self.tolerance) else 0
        return ok / len(self.agents)

    def step(self):
        self.datacollector.collect(self)
        self.agents.shuffle_do("step")
```

Note: exact cell-space helper names (`neighborhood`, `select_random_empty_cell`) are current in
Mesa 3.x; if your installed minor version differs, confirm against
`mesa.readthedocs.io/stable/apis/` rather than guessing. The classic `mesa.space.SingleGrid` with
`position_agent`/`move_to_empty` is an equivalent, maintenance-mode alternative.

## Network model (agents on a graph)

```python
import mesa, networkx as nx
from mesa.space import NetworkGrid

class Person(mesa.Agent):
    def __init__(self, model):
        super().__init__(model)
        self.opinion = self.random.random()

    def step(self):
        neighbors = self.model.grid.get_neighbors(self.pos, include_center=False)
        if neighbors:
            other = self.random.choice(neighbors)
            self.opinion += 0.1 * (self.model.agents[other].opinion - self.opinion)

class OpinionModel(mesa.Model):
    def __init__(self, n=100, seed=None):
        super().__init__(seed=seed)
        g = nx.erdos_renyi_graph(n, 0.05, seed=seed)
        self.grid = NetworkGrid(g)
        for node in g.nodes():
            a = Person(self)
            self.grid.place_agent(a, node)

    def step(self):
        self.agents.shuffle_do("step")
```

## Parameter sweep

```python
results = mesa.batch_run(
    Schelling,
    parameters={"tolerance": [0.2, 0.3, 0.4, 0.5], "density": [0.7, 0.9]},
    iterations=25, max_steps=100, data_collection_period=-1, display_progress=True)
# results -> list[dict]; load into pandas to plot outcome vs tolerance
```

## Validation checklist (an ABM that runs is not evidence)

- [ ] **Reproducible**: `seed=` fixed for a single run; varied across runs for a distribution.
- [ ] **Replicated**: report the macro outcome's distribution over ≥20 seeds, not one trajectory.
- [ ] **Swept**: `batch_run` over key parameters; identify tipping points / phase transitions.
- [ ] **Pattern-oriented**: reproduces the target stylized fact it was built to explain.
- [ ] **Sensitivity**: name which assumptions drive the result; a fragile result is a weak theory.
- [ ] **Claim scoped**: the mechanism is *sufficient* to generate the pattern, not proven unique.

## References

- Kazil, Masad & Crooks (2020); ter Hoeven et al. (2025, JOSS) — Mesa 3.
- Epstein & Axtell (1996), *Growing Artificial Societies* (generative social science).
- Grimm et al. (2005), Pattern-oriented modeling; the ODD protocol for documenting ABMs.

---
name: alterlab-abm-mesa
description: "Builds agent-based models of social systems with Mesa 3 — the current AgentSet API (model.agents.shuffle_do('step'), auto-assigned unique_id, mandatory super().__init__(seed=...)), cell spaces (mesa.discrete_space OrthogonalMooreGrid / classic mesa.space grids), the DataCollector, batch_run parameter sweeps, and SolaraViz — for emergence, segregation, diffusion, opinion dynamics, and cooperation models. It uses the Mesa 3.x API (the old mesa.time schedulers like RandomActivation are removed) and treats the model as a generative theory to be validated, not just run. Use when the request mentions an agent-based model, Mesa, simulating interacting agents, or emergent macro behavior from micro rules. For discrete-event (queueing/process) simulation prefer alterlab-simpy; for reinforcement learning prefer alterlab-stable-baselines3. Part of the AlterLab Academic Skills suite."
license: MIT
allowed-tools: Read Bash(python:*)
compatibility: "Requires mesa>=3 (pip; API changed substantially from Mesa 2 — mesa.time schedulers removed). Optional SolaraViz for interactive visualization. No API key; runs locally via `uv run python`. On the Anthropic API (no runtime install) declare mesa as a dependency."
metadata:
    skill-author: AlterLab
    version: "1.0.0"
    depends_on: "alterlab-ssci-design-gate, alterlab-simpy (contrast: discrete-event); audited by alterlab-ssci-inference-gate"
---

# Agent-Based Modeling with Mesa 3 — Micro Rules, Macro Emergence

**Skill type: ANALYSIS MODULE.** Builds ABMs where macro patterns *emerge* from local agent
rules (Schelling segregation, opinion dynamics, diffusion, cooperation). The discipline: use the
**current Mesa 3 API**, and treat the model as a generative explanation that must be validated
(swept, replicated, compared to a target pattern), not a toy that merely runs.

## Core Mission

```
THE MODEL IS A THEORY OF HOW MACRO EMERGES FROM MICRO. USE MESA 3 CORRECTLY, THEN VALIDATE.
```

## When to Use This Skill

- "Build an agent-based model / Mesa model of [segregation, diffusion, opinion, cooperation]."
- "Simulate many interacting heterogeneous agents and watch what emerges."
- "Do a parameter sweep over my ABM and collect outcomes."

### Does NOT Trigger

| The request is really about… | Route to | Why not this skill |
|---|---|---|
| Discrete-event / queueing / process simulation | `alterlab-simpy` | Event-driven processes, not interacting agents on a grid/network. |
| Reinforcement learning (an agent learning a policy) | `alterlab-stable-baselines3` | Policy optimization, not generative social simulation. |
| Whether ABM is the right method at all | `alterlab-ssci-design-gate` | Design routing, upstream. |
| System-dynamics / ODE compartment models | `alterlab-statistical-analysis` | Aggregate dynamics, not agent-level. |

## The Mesa 3 API (verified — do not ship Mesa 2 patterns)

Mesa 3 removed `mesa.time` schedulers (`RandomActivation`, etc.). Agents auto-register into
`model.agents`; `unique_id` is auto-assigned; the model **must** call `super().__init__(seed=...)`.

```python
import mesa

class MoneyAgent(mesa.Agent):
    def __init__(self, model):                 # NO unique_id argument in Mesa 3
        super().__init__(model)
        self.wealth = 1

    def step(self):
        if self.wealth > 0:
            other = self.random.choice(self.model.agents)
            other.wealth += 1
            self.wealth -= 1

class MoneyModel(mesa.Model):
    def __init__(self, n=10, seed=None):
        super().__init__(seed=seed)            # mandatory in Mesa 3
        MoneyAgent.create_agents(self, n)      # bulk creation helper
        self.datacollector = mesa.DataCollector(
            model_reporters={"Gini": compute_gini},
            agent_reporters={"Wealth": "wealth"})

    def step(self):
        self.datacollector.collect(self)
        self.agents.shuffle_do("step")         # replaces RandomActivation
```

- **Scheduling**: `model.agents.shuffle_do("step")` (random activation),
  `model.agents.do("step")` (fixed order), `do("step")` then `do("advance")` (simultaneous),
  `model.agents_by_type[Type].shuffle_do("step")` (staged). `model.steps` auto-increments.
- **Space**: classic `mesa.space.MultiGrid/SingleGrid/NetworkGrid` (maintenance mode) with
  `place_agent`/`move_agent`; new cell space `mesa.discrete_space.OrthogonalMooreGrid((w,h),
  torus=...)` / `OrthogonalVonNeumannGrid` / `HexGrid`.
- **Batch sweeps**: `mesa.batch_run(MoneyModel, parameters={"n":[10,50,100]}, iterations=20,
  max_steps=100, data_collection_period=-1)` → list of dicts.
- **Visualization**: `from mesa.visualization import SolaraViz, make_space_component,
  make_plot_component`.

Full validated skeleton (Schelling + a network model), the space-API choice, and the validation
checklist: `references/mesa_patterns.md`.

## The validation discipline

An ABM that runs is not evidence. Report:

1. **Replication** — multiple runs with different seeds; report the *distribution* of the macro
   outcome, not one run (fix `seed=` for reproducibility, vary it for the distribution).
2. **Parameter sweep** — `batch_run` across the key parameters; show how the emergent outcome
   depends on them (phase transitions, tipping points).
3. **Pattern-oriented validation** — does the model reproduce the target stylized fact it was built
   to explain (e.g. Schelling's high segregation from mild preferences)?
4. **Sensitivity** — which assumptions drive the result; state them.

## Output Template

```
MODEL:       <agents, their state, the local step rule; space = grid/network/none>
SCHEDULE:    <shuffle_do / do / staged> (Mesa 3 AgentSet)
MACRO OUTCOME: <the emergent quantity the DataCollector tracks>
VALIDATION:  <n seeds -> distribution; batch_run sweep; target pattern reproduced?>
CLAIM SCOPE: generative (a sufficient micro mechanism), NOT the unique/true mechanism
```

## References

- `references/mesa_patterns.md` — validated Mesa 3 skeletons (grid + network), space-API selection, batch_run sweep, validation checklist.

Part of the AlterLab Academic Skills suite.

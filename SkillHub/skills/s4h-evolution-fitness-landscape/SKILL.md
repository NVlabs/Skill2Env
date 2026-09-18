---
name: s4h-evolution-fitness-landscape
description: "Maps the solution space as peaks and valleys to understand local optima, adaptive valleys, and path dependence. Triggers: 'are we stuck', 'local maximum', 'fitness landscape', 'why can't we get to the next level', 'path dependence', 'trapped by success', 'incremental improvement is not working', 'we need a discontinuous leap', 'adjacent possible'."
---

# Evolution: Fitness Landscape

Sewall Wright introduced the fitness landscape metaphor in 1932: imagine every possible combination of traits mapped onto a surface, with elevation representing fitness. Populations move across this surface by natural selection — uphill, always, toward higher fitness. The metaphor contains a profound trap: gradient-following reliably finds local peaks but may never reach the global optimum if that optimum is separated from the current position by a valley — a region of lower fitness that must be crossed to reach higher ground.

Stuart Kauffman formalised the implications. In a rugged landscape (many local peaks of varying heights), adaptive evolution produces a rich variety of stable-but-suboptimal solutions. Path dependence is total: where you end up depends entirely on where you started, because the trajectory of selection is irreversible and local. In an ultra-smooth landscape (one peak), selection reliably finds the global optimum. In a chaotic landscape (fitness changes with every step), selection fails entirely — there is no stable higher ground to climb toward.

This tool maps the fitness landscape of a problem, strategy space, or technology domain. It identifies where the current entity sits, which kind of landscape this is, what the local peaks look like, what valleys must be crossed to reach higher ground, and whether valley-crossing is currently viable. The practical question is almost always: are we trapped on a local peak, and if so, what does it cost to get off it?

---

## Your Process

**Step 1: Define the Landscape**
Specify the axes and the fitness measure. Every landscape has:
- **Axes (trait dimensions):** the variables that can be changed. In evolution, these are genetic traits. In strategy, they might be product features, business model parameters, technology architecture, pricing approach, or organisational structure. Identify the 2–4 most important axes — those where variation most strongly affects fitness.
- **Fitness measure:** what counts as success in this environment? Be specific — not "performance" but "customer retention at a given price point" or "survival rate in a drought year." The fitness measure is always context-dependent and time-indexed.

**Framing check:** Confirm the landscape axes and fitness measure before continuing. State what you've identified — the entity, the key dimensions of variation, and what counts as fitness — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [one sentence naming the entity, the 2–4 landscape axes, and the fitness measure]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Assess Landscape Ruggedness**
How many distinct high-fitness solutions exist in this space? Is this:
- **Smooth landscape:** one peak (or a ridge leading to one peak) — incremental improvement is reliable and will eventually reach the optimum
- **Rugged landscape:** multiple distinct peaks of varying heights — incremental improvement gets stuck on whichever peak is closest; path dependence is strong
- **Correlated landscape:** peaks cluster together, valleys are not too deep — moderate path dependence, some room for exploration
- **Chaotic landscape:** fitness changes rapidly with small changes in strategy — no stable peaks; exploration is futile because the ground keeps shifting

Name evidence for the ruggedness assessment.

**Step 3: Locate the Current Position**
Where does the entity currently sit on the landscape? Describe this precisely: which traits, configurations, or strategy choices define their current position? Assess whether they are:
- On or near a local peak (marginal improvements yield diminishing returns; incremental change keeps reaching the same ceiling)
- Partway up a slope (still improving; incremental change is still productive)
- In a valley (currently unfit but possibly transitioning toward a peak)
- On the global peak (no realistic higher position exists)

Identify the evidence for the current position — what patterns suggest they are or are not at a local peak?

**Before mapping neighbours:** Use `AskUserQuestion`:
- **Question:** "I've placed [entity] at [current position description]. Before I map the surrounding peaks and valleys: does that placement seem right, or are there recent moves or constraints I should know about?"
- **Header:** "Position Check"
- **Options:**
  - **Looks right — proceed** — the position assessment is accurate
  - **Adjust** — the entity is further up, further down, or positioned differently; user will clarify
  - **Add context** — user will describe a recent move or constraint that affects the picture

**Step 4: Map Adjacent Peaks and Valleys**
What are the nearest alternative high-fitness positions — the other local peaks that are reachable from here? For each:
- **Peak description:** what combination of traits or strategies defines this peak?
- **Peak height:** how fit is it relative to current position?
- **Valley depth:** how far does fitness drop in the transition from here to there — and how long does that valley last?
- **Valley width:** how many incremental steps of lower fitness must be traversed?
- **Path options:** are there intermediate positions that reduce the valley depth (stepping stones, hybrid strategies)?

**Step 5: Assess Valley-Crossing Viability**
Whether crossing a fitness valley is viable depends on:
- **Available slack:** can the entity absorb a period of lower fitness? (financial reserves, market tolerance, organisational stability)
- **Valley duration:** is this a brief crossing (one product cycle, one season) or a prolonged period of sub-fitness (years of below-margin operation)?
- **Environmental shift:** is the fitness landscape itself changing? If the current peak is being eroded by environmental change, staying on it is not safe — the valley crossing becomes necessary even if painful.
- **Forcing mechanism:** is there an external shock (competitive pressure, regulatory change, technology disruption) that may force the crossing regardless of choice?

Assess viability honestly: valley-crossing that requires sustained tolerance for sub-fitness is often strategically obvious but organisationally impossible.

**Step 6: Strategic Implication**
Synthesise: where is the entity trapped, if anywhere? What would it take to get to higher ground? Is the current trajectory one of local optimisation (reliably improving toward a local peak) or genuine progress (crossing toward a global peak)? What needs to be true — in the environment, in the entity's capabilities, or in the competitive pressure — for a valley crossing to be attempted?

---

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation in 1–2 sentences — where the entity sits on the landscape, what the key peak or valley question is — then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full analysis** — Complete all steps, reasoning shown throughout
  - **Key findings only** — Bottom-line output, skip step-by-step detail
  - **Specific focus** — Zoom in on one particular peak or valley
  - **Reframe** — The read is off; correct it and the analysis will follow the corrected framing

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

---

## Output Format

**Landscape Definition**
[Entity, key axes, fitness measure, and landscape ruggedness type]

**Current Position**
[Where the entity sits — which traits, strategy, or configuration define their current position and whether they are near a local peak, on a slope, in a valley, or at a global peak]

**Evidence for Peak Status**
[Signs that incremental improvement is hitting a ceiling — or evidence that improvement is still productive]

**Adjacent Peaks**

| Peak | Description | Relative Fitness | Valley Depth | Valley Width | Path Options |
|---|---|---|---|---|---|
| [name] | [strategy/configuration] | [higher / lower / similar] | [shallow / moderate / deep] | [narrow / wide] | [stepping stones or none] |

**Valley-Crossing Viability Assessment**

| Factor | Assessment |
|---|---|
| Slack available | [high / moderate / low] |
| Valley duration | [brief / moderate / prolonged] |
| Landscape stability | [stable / shifting / eroding under current position] |
| Forcing mechanism | [present / absent — if present, describe] |

**Strategic Implication**
[Synthesised recommendation: stay and optimise the current peak, attempt a valley crossing (under what conditions), or wait for environmental shift to change the landscape]

---

## Notes

The fitness landscape metaphor is descriptive, not prescriptive. It names the structural reason why incremental improvement fails to reach the global optimum — not because the strategy is wrong, but because the topology of the solution space makes gradient-following insufficient. This is why discontinuous innovation often looks foolish from within the existing peak and obvious in retrospect: the valley had to be crossed.

Stephen Jay Gould's concept of the contingency of evolutionary history maps directly: which peak a lineage ends up on depends entirely on historical path, not on the quality of the peak itself. Many sub-optimal peaks are stably occupied simply because they were reached first. This is the structural explanation for lock-in, legacy architecture, and incumbent advantage.

Pairs with `/s4h-evolution-variation-selection` to understand which selection pressures are defining the current fitness landscape. Pairs with `/s4h-constraint-hardness-testing` to evaluate whether constraints that keep the entity on the current peak are truly hard or merely assumed. Pairs with `/s4h-systems-leverage-analysis` to find where small changes in landscape topology (changing the fitness measure, changing the environment) would make valley-crossing tractable.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Fitness landscape mapped. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-evolution-variation-selection` — Understand what selection pressures are shaping this landscape
  - `/s4h-constraint-hardness-testing` — Test whether constraints keeping you on the current peak are truly binding
  - `/s4h-strategy-timing` — Determine when the right moment is to attempt a valley crossing
  - **Done** — Wrap up and synthesise what we have so far

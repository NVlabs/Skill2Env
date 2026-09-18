---
name: s4h-evolution
description: "Entry point for the evolution thinking toolkit. Routes to the right evolution skill based on your situation. Use when you say 'evolution', 'natural selection', 'how does this population change over time', 'why does this strategy persist', 'what niche am I competing in', 'fitness landscape', 'arms race', 'coevolution', or want evolutionary thinking applied without knowing which specific tool fits."
---

# Evolution

Applies evolutionary reasoning to understand how populations, strategies, and systems change over time. Fitness is not a fixed property — it is always fitness *for a context*. This toolkit maps variation, selection, niches, landscapes, and coevolutionary escalation to surfaces what persists, what gets outcompeted, and why.

## Which tool fits

| You need to... | Tool |
|---|---|
| Understand how a population or strategy pool changes through variation and selection | variation-selection |
| Understand how competitors coexist or exclude each other, and where differentiation creates advantage | niche |
| Map the solution space as peaks and valleys and understand path dependence | fitness-landscape |
| Analyse coevolutionary escalation between two parties adapting to each other | arms-race |

## Routing Decision

**Framing check:** Confirm the evolutionary dynamic in focus before routing. State what you've identified — the population or system, and the competitive or adaptive pressure — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the system and the evolutionary pressure]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

- **How does a population of strategies/entities change over time through selection?** → variation-selection
- **Who coexists with whom, and why — what determines which strategies/players can occupy the same space?** → niche
- **What is the shape of the solution space — are we stuck on a local peak, and how do we move to a higher one?** → fitness-landscape
- **Two parties keep adapting to each other in cycles with no clear end state** → arms-race
- **Unclear** → variation-selection; mapping the variation-selection-retention cycle always surfaces which sub-question is most pressing

## Confirm Direction

After diagnosing which tool fits, use the `AskUserQuestion` tool to confirm direction. Construct the question dynamically to include your diagnosis:

- **Question:** "My read: **[diagnosed tool]** — [one sentence on why it fits]. How would you like to proceed?"
- **Header:** "Direction"
- **Options:**
  - **Yes, run that tool** — Execute the diagnosed skill immediately using the context already provided
  - **Show all options** — List every skill in this category with one-line descriptions
  - **Quick version** — Run a lighter-weight alternative if one exists for this situation
  - **Re-diagnose** — Revisit the situation description for a different read

Proceed based on their selection.

---

## Variation-Selection

*Traces how a population changes by mapping what varies, what gets selected, and what gets retained.*

Darwin's central insight formalized: for any population with heritable variation and differential reproductive success, selection will shift the population toward fitter variants over time. This tool applies that triad — variation, selection, retention — to any evolving system, from species to business strategies to cultural practices. It identifies what is varying, which selection pressures are active, what is being retained or discarded, and what the population looks like after several rounds.

**Output:** Variation map, selection pressures and their relative strength, retention mechanisms, predicted population shift, and what this implies for strategy.

---

## Niche

*Maps who competes with whom, under what conditions, and where differentiation enables coexistence.*

Gause's competitive exclusion principle: two species competing for the same limiting resource in the same way cannot stably coexist — one will drive the other out. But niches can be partitioned: temporal, spatial, resource-based, or by method of exploitation. This tool maps the competitive space, identifies overlapping niches, finds the axes on which differentiation enables coexistence, and analyses whether a niche is being created, invaded, or vacated.

**Output:** Competitive landscape, niche axes, overlap analysis, differentiation opportunities, and the risk of niche displacement.

---

## Fitness Landscape

*Maps the solution space as peaks and valleys — where you are, why you might be stuck, and how to reach higher ground.*

Sewall Wright's fitness landscape metaphor: every possible combination of traits (or strategies, or configurations) has a corresponding fitness value. High-fitness combinations are peaks; low-fitness valleys separate them. Adaptive evolution climbs by gradient — incrementally moving toward higher fitness — which means it reliably finds local peaks but may never reach the global optimum. This tool maps the landscape shape, identifies which peak you're on, what valley lies between you and a higher peak, and what crossing that valley would require.

**Output:** Current position on the landscape, nearest local peaks and their fitness values, the valleys that must be crossed to reach higher ground, and the conditions under which valley-crossing becomes viable.

---

## Arms Race

*Analyses coevolutionary escalation — when two parties adapt to each other in cycles that may help neither.*

Richard Dawkins and John Krebs' formalisation of evolutionary arms races: predator and prey, host and parasite, competitor and competitor each evolve adaptations and counter-adaptations in response to each other. The result is a coevolutionary treadmill — both sides invest in escalating capabilities and may end up no better off in relative terms than when they started. This tool identifies the cycle structure, the escalation dynamic, the asymmetries that determine who wins if arms-racing continues, and whether there is an exit that breaks the cycle.

**Output:** Arms race structure, escalation trajectory, asymmetries, exit conditions, and strategic implication.

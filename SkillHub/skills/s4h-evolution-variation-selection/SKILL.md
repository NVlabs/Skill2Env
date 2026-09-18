---
name: s4h-evolution-variation-selection
description: "Applies the variation-selection-retention triad to understand how populations and strategies adapt over time. Triggers: 'how does this evolve', 'what gets selected for', 'why do some strategies persist and others die out', 'population dynamics', 'selection pressure', 'what survives in this environment', 'who wins over time'."
---

# Evolution: Variation-Selection

Darwin's central insight was not about progress — it was about fit. Populations change not because individuals strive toward an ideal but because variants that happen to be better suited to current conditions leave more descendants. The population shifts toward fitness not through intention but through differential survival and reproduction. Evolution is a filter, not a designer.

This tool applies the variation-selection-retention triad to any evolving system: biological populations, business strategy portfolios, cultural practices, product features, organisational structures, or ideas spreading through a community. Whenever there is a population of variants, a selection environment that differentially rewards some over others, and a mechanism by which successful variants are retained or replicated — evolution is happening. The analysis asks: what is varying, what is the selection pressure, what is being retained, and what does the population look like after several rounds?

Richard Dawkins extended Darwin's logic beyond genes to any replicating entity with heritable variation — memes, strategies, cultural norms. The triad is substrate-independent: wherever variation + selection + retention operate, populations evolve. The question is always which variants win *in this environment*, not which are best in the abstract.

---

## Your Process

**Step 1: Define the Population and the Entity**
Identify what is being evolved. What are the entities in this population — the variants being compared? Be precise: not "companies" but "pricing strategies in use by companies in this market." Define the time horizon over which evolution is being observed: one product cycle, ten years, a generation.

**Framing check:** Confirm the population and time horizon before continuing. State what you've identified — the specific entities being varied, the time scale, and the outcome space — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing — what the population is, what varies, and over what time horizon]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Map the Variation**
What dimensions of variation exist in this population? Catalogue the traits, strategies, or features that differ across entities. Which of these are heritable — passed on or replicated to successors? Which are plastic — changeable within a single entity's lifetime? Heritable variation is what drives evolution; plastic variation is what drives adaptation. Both matter for different reasons.

For each dimension of variation, identify the range: from what to what do entities vary, and roughly how is the population currently distributed across that range?

**Step 3: Identify the Selection Pressures**
What are the environmental conditions that differentially reward some variants over others? List the active selection pressures:
- **Competitive pressure:** which variants outcompete others for shared resources?
- **Environmental pressure:** which variants survive in the current environmental conditions (market, regulatory, ecological)?
- **Sexual/social selection (if applicable):** which variants are preferred by choosers — customers, partners, funders?

For each selection pressure, assess its strength (strong = quickly eliminates unfit variants; weak = allows many variants to coexist) and its direction (what traits are being selected *for*, and which are being selected *against*).

**Before narrowing:** Use `AskUserQuestion` to surface pressures the user may see that you haven't named:
- **Question:** "I've identified these selection pressures: [list]. Are there pressures specific to this context I've missed — regulatory, seasonal, technological, or otherwise?"
- **Header:** "Selection Environment"
- **Options:**
  - **That's complete** — proceed with this set
  - **Add one** — user will describe the missing pressure
  - **Reweight** — the pressures are right but their relative strength needs adjusting

**Step 4: Trace Retention and Replication**
How do successful variants persist and propagate? What is the mechanism by which fitness translates into increased representation in the population? In biology, this is reproduction. In business, it might be: companies that work get funded and copied; features that convert get shipped more; strategies that work get codified into SOPs. Identify the retention mechanism and its fidelity (does variation get introduced in replication, or is it copied faithfully?).

Also identify the extinction mechanism: how are unfit variants eliminated? Fast elimination (bankruptcy, species death) produces rapid evolution; slow elimination (organisations kept alive by subsidies or inertia) produces a population with many unfit variants persisting.

**Step 5: Project the Population Shift**
Given the variation in the population, the selection pressures, and the retention mechanisms: what does the population look like after several rounds? Which variants increase in frequency? Which decrease and eventually disappear? Which traits become universal (fixed in the population) and which remain polymorphic (multiple variants coexist)?

Identify the equilibrium state if selection continues without environmental change — and then ask: how likely is the environment to change? A static environment drives populations toward a single dominant strategy; a shifting environment maintains diversity because today's unfit variant may be tomorrow's winner.

**Step 6: Surface the Strategic Implication**
If the user is a participant in this system (not just an observer), identify: which variant are they currently embodying? Is that variant's fitness rising or falling under current selection pressures? What does the population shift imply for their trajectory — and what would it take to shift to a more fit variant before selection does it for them?

---

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences — what population is evolving, what the dominant selection pressures are, and what the key question is — then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full analysis** — Complete all steps, reasoning shown throughout
  - **Key findings only** — Bottom-line output, skip step-by-step detail
  - **Specific focus** — Zoom in on one aspect of this analysis
  - **Reframe** — The read is off; correct it and the analysis will follow the corrected framing

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

---

## Output Format

**Population Definition**
[What is evolving, what varies, time horizon]

**Variation Map**

| Dimension | Range | Current Distribution | Heritable? |
|---|---|---|---|
| [trait/feature/strategy] | [low end → high end] | [skewed toward / spread across] | [yes / partial / no] |

**Selection Pressures**

| Pressure | Direction | Strength | Mechanism |
|---|---|---|---|
| [competitive / environmental / social] | [selects for / against what] | [strong / moderate / weak] | [how it eliminates or rewards] |

**Retention and Replication**
[How fit variants persist and propagate — fidelity, speed, mechanism]

**Extinction Mechanism**
[How unfit variants are eliminated — speed and completeness]

**Projected Population Shift**
[What the population looks like after several rounds — which variants rise, which fall, what becomes fixed]

**Environmental Stability Assessment**
[How likely the selection environment is to shift, and what that means for current fit variants]

**Strategic Implication**
[For a participant: current variant's trajectory, what the population shift means, and what a fitness-improving shift would look like]

---

## Notes

Variation-selection analysis is about the population, not the individual. The unit of analysis is the distribution of variants, not the fate of any single entity. A variant can be perfectly fit today and extinct in ten years — not because it failed, but because the selection environment shifted. See `/s4h-temporal-futures-mapping` for mapping how the selection environment itself might change.

The most common error in applying this tool is treating current fitness as permanent. Evolution is contextual — fit for *now* is not the same as fit for all time. The most important question is often not "what is selected for now?" but "what is this population becoming, and what selection environment are we building toward?"

For understanding whether fit variants can coexist or must displace each other, pair with `/s4h-evolution-niche`. For understanding path dependence and why populations get stuck on local fitness peaks, pair with `/s4h-evolution-fitness-landscape`.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Population dynamics mapped. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-evolution-niche` — Map the competitive landscape and understand who can coexist with whom
  - `/s4h-evolution-fitness-landscape` — Explore whether you're on a local fitness peak and how to move higher
  - `/s4h-systems-feedback-mapping` — Map the feedback loops that are driving or damping the selection pressures
  - **Done** — Wrap up and synthesise what we have so far

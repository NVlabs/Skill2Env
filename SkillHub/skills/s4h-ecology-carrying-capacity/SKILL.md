---
name: s4h-ecology-carrying-capacity
description: "Applies carrying capacity thinking to any system with limits — maps the ceiling, overshoot risk, and what happens when it is crossed. Use when asked about 'capacity limits', 'how much can this system handle', 'are we overloaded', 'growth ceiling', 'when do we hit the wall', or 'sustainable scale'."
---

# Ecology: Carrying Capacity

Every system operates within limits. Not all limits are visible — some only become apparent at the moment they are crossed, and by then the damage is already accumulating. The concept of carrying capacity (K) originated in population ecology, formalised through the logistic growth model: populations grow rapidly when resources are abundant, slow as they approach the ceiling, and crash or stabilise when they hit or exceed it. Arthur Tansley, who coined the term "ecosystem" in 1935, understood that any system is defined by the relationship between its components and their resource base. Howard Odum extended this to show that energy and material constraints are the ultimate governors of system scale.

The insight transfers directly beyond biology. Teams have a carrying capacity defined by coordination costs, management bandwidth, and information throughput. Platforms have carrying capacities bounded by network congestion, moderation costs, and trust erosion. Markets have carrying capacities constrained by willingness-to-pay, substitution, and regulatory tolerance. In all cases: the limit exists whether or not it has been named, and approaching it without awareness is how organisations walk into overshoot.

---

## Your Process

**Step 1: Define the System and the Resource Axis**
Name the system being analysed and identify the primary resource or condition that limits growth. The carrying capacity is always a constraint on something specific — not "capacity" in the abstract but a specific input, condition, or ceiling.

**Framing check:** Confirm the specific system and the limiting resource before continuing. State what you've identified in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the system and the resource or condition that limits it]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Identify All Constraint Candidates**
List every potential ceiling — physical, economic, social, informational, regulatory. Systems typically have a primary constraint and several secondary ones. Map all of them before narrowing.

**Before narrowing:** Show the complete set of constraint candidates to the user first. Use `AskUserQuestion`:
- **Question:** "I've identified [N] potential constraints. Before I focus on the binding one, are there any you'd flag as especially critical, or any I've missed?"
- **Header:** "Constraints"
- **Options:**
  - **Proceed with your selection** — the set looks right
  - **Flag one** — user will name a specific constraint to highlight
  - **Add a missing one** — user will describe it

**Step 3: Identify the Binding Constraint**
Which constraint is tightest right now? The binding constraint determines the effective carrying capacity at this moment. Secondary constraints are the next ceilings — they become binding as the primary one is addressed. The order matters: raising one ceiling without knowing the sequence can expose a harder ceiling underneath.

**Step 4: Estimate Current Load Relative to Ceiling**
How far is the system from the binding constraint? Use available evidence: growth trends, stress signals, performance degradation, queue build-up, error rates, burn-out signals, or resource depletion rates. Estimate whether the system is:
- **Comfortably below K** — room to grow; primary risk is under-utilisation
- **Approaching K** — slowing growth, early stress signals; time to plan
- **At or near K** — logistic curve flattening; stability is possible but fragile
- **In overshoot** — beyond K; current state is unsustainable; oscillation or crash approaching

**Step 5: Model Overshoot Dynamics**
If the system is approaching or exceeding K, map what overshoot looks like: what breaks first, on what timescale, and with what lag between cause and visible effect. The most dangerous overshoot scenarios involve delays — the system appears fine until it suddenly isn't. Identify the early-warning signals that would be visible before collapse.

**Step 6: Map Options**
Three categories of response to a carrying capacity constraint:
- **Raise the ceiling** — increase the resource, remove the constraint, redesign the system
- **Reduce the load** — decrease demand, prioritise, segment
- **Respect the limit** — design for stability at current scale rather than continued growth

For each: feasibility, lead time, and second-order effects.

---

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences — what system is being analysed and what the key question is — then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full analysis** — Complete all steps, reasoning shown throughout
  - **Key findings only** — Bottom-line output, skip step-by-step detail
  - **Overshoot risk focus** — What happens if the ceiling is crossed, and how to read early signals
  - **Reframe** — The read is off; correct it and the analysis will follow the corrected framing

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

## Output Format

**System:** [name and scope]

**Carrying Capacity Analysis**

| Constraint | Type | Current Load | Ceiling Estimate | Distance to Limit |
|------------|------|-------------|-----------------|-------------------|
| | | | | |

**Binding Constraint:** [which constraint + why it's the tightest + what signals indicate proximity]

**Load Assessment:** [current position on the logistic curve + evidence]

**Overshoot Scenario:** [what breaks first, on what timescale, with what early-warning signals]

**Options**

| Option | Category | Feasibility | Lead Time | Second-Order Effects |
|--------|----------|-------------|-----------|---------------------|
| | | | | |

---

## Notes

Carrying capacity is not fixed. It can be raised (through technology, organisation redesign, resource development) or degraded (through overuse, pollution, trust erosion). Analyse both directions. The most dangerous assumption is that current growth can continue linearly — the logistic curve always curves.

Pairs well with `/s4h-systems-leverage-analysis` when the carrying capacity constraint is a system-structural problem, and with `/s4h-resource-bottleneck-analysis` when the constraint is operational throughput. The distinction: carrying capacity is about the ceiling on sustainable scale; bottleneck analysis is about throughput within current scale.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Carrying capacity mapped. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-ecology-interdependence` — Map who depends on whom within the constrained system
  - `/s4h-systems-leverage-analysis` — Find where to intervene to raise the ceiling most efficiently
  - `/s4h-ecology-succession` — Understand what developmental stage the system is in and where it's heading
  - **Done** — Wrap up and synthesise what we have so far

---
name: s4h-economics
description: "Entry point for the economics toolkit. Routes to the right economics skill based on your situation. Use when you say 'economics', 'what's the incentive here', 'what am I giving up', 'who pays for this', 'should we do more or less of this', 'why won't people cooperate', 'externality', 'opportunity cost', 'marginal', or want economic reasoning applied without knowing which specific tool fits."
---

# Economics

Applies economic reasoning to decisions, organisations, and systems. Diagnoses what kind of analysis is needed and routes to the right tool. Economics is not just about money — it is about how incentives shape behaviour, how choices foreclose alternatives, and why individually rational actors so often produce collectively irrational outcomes.

## Which tool fits

| You need to... | Tool |
|---|---|
| Map what you're actually giving up by choosing this | opportunity-cost |
| Understand who benefits, who pays, and what behaviours follow | incentive-mapping |
| Identify costs or benefits falling on parties outside the decision | externalities |
| Apply the logic of the next unit — sunk costs, average vs. marginal | margin |
| Diagnose why rational individuals keep producing bad collective outcomes | coordination |

## Routing Decision

**Framing check:** Confirm the situation before routing. State what you've identified — the core economic question and what's at stake — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the economic situation and the core question]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

- **Evaluating a choice and want to understand the full cost, including what's foregone** → opportunity-cost
- **Trying to understand or change how people behave — who's being rewarded for what** → incentive-mapping
- **Decision or policy has effects on parties who aren't in the room** → externalities
- **Decision involves how much to do: more, less, expand, cut — or sunk cost reasoning** → margin
- **A group keeps failing to cooperate even though cooperation would benefit everyone** → coordination
- **Unclear** → incentive-mapping; almost every economic question eventually becomes a question about incentives

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

## Opportunity Cost

*Every choice forecloses alternatives — maps what you give up, not just what you gain.*

Alfred Marshall's foundational insight: the true cost of any choice is not the money spent but the next-best alternative foregone. Most analyses count only what is spent; opportunity cost analysis insists on asking what else those resources could have done. This reveals hidden costs in decisions that look free, exposes the real tradeoff in choices between competing goods, and reframes "should we do this?" as "is this the best use of what we have?" Outputs a full cost picture including the value of the path not taken.

**Output:** Explicit opportunity cost map — the best available alternatives, the value of each, the true cost of the chosen path, and a recommendation on whether the choice holds up once the foregone value is visible.

---

## Incentive Mapping

*Maps who benefits, who pays, and what behaviours the incentive structure actually produces.*

Incentives are the operating system of human behaviour. The question is not what people are told to do, or what they intend to do — it is what the structure rewards them for doing. Identify every party in the system. For each: what do they gain by doing X? What do they lose? What actions does the incentive structure push them toward, and where does that diverge from what the system needs them to do? Misaligned incentives predict misbehaviour more reliably than bad intentions do.

**Output:** Incentive map by party — benefits, costs, and predicted behaviour under the current structure — plus identified misalignments and redesign options.

---

## Externalities

*Identifies costs and benefits not borne by the actor — and how to internalize them.*

A.C. Pigou's central insight: when the person making a decision does not bear all of its costs (or capture all of its benefits), they will systematically over-produce the harmful activity or under-produce the beneficial one. Negative externalities (pollution, congestion, noise) are overproduced; positive externalities (vaccination, education, open-source software) are underproduced. The analysis maps all affected parties, quantifies the external effects, and identifies the mechanism — tax, subsidy, property right, regulation, or social norm — that best internalises them.

**Output:** Externality map — who is affected, by how much, in what direction — plus internalisation mechanisms ranked by feasibility.

---

## Margin

*Applies marginal thinking: the relevant decision is the next unit, not the average or the sunk cost.*

The most durable insight in economics: decisions should be made at the margin. The question is never "was this a good investment overall?" — it is "should we do one more unit of this?" Marginal cost vs. marginal benefit determines whether to expand, maintain, or cut. Sunk costs — resources already spent that cannot be recovered — are economically irrelevant to forward decisions, yet they dominate most human reasoning. This skill strips out sunk cost reasoning, reframes the question correctly, and applies marginal logic to the decision at hand.

**Output:** Marginal analysis — the relevant cost and benefit at the decision margin, sunk cost identification and isolation, and a recommendation based on the correct forward-looking comparison.

---

## Coordination

*Diagnoses collective action failures, public goods problems, and why individually rational behaviour produces collective irrationality.*

Elinor Ostrom's life work: the tragedy of the commons is not inevitable. But it is common — and its causes are structural, not moral. When the benefits of an action are diffuse (shared by many) while the costs are concentrated (borne by the individual), rational actors will undercontribute to the collective good. When the benefits of defection are private while the costs are shared, rational actors will overuse the commons. This skill maps the structure of the coordination failure — public good, common pool resource, assurance game, free-rider problem — and identifies what institutional arrangements (property rights, social norms, regulations, community monitoring) can solve it.

**Output:** Coordination failure diagnosis — the structure of the problem, why individual rationality produces collective harm, and the institutional mechanisms most likely to resolve it.

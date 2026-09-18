---
name: s4h-economics-externalities
description: "Identifies costs and benefits not borne by the decision-maker — and how to internalise them. Triggers: 'externality', 'who else is affected', 'costs falling on others', 'side effects', 'spillover', 'the market isn't accounting for this', 'negative externality', 'positive externality', 'social cost vs. private cost', 'Pigou', any situation where the person deciding does not bear all the consequences."
---

# Economics: Externalities

A.C. Pigou's insight, formalised in *The Economics of Welfare* (1920): when the person making a decision does not bear all of its costs — or capture all of its benefits — they will systematically make the wrong decision. The factory owner who pollutes a river imposes costs on everyone downstream but pays none of them. The individual who gets vaccinated reduces the risk of infection for everyone around them but captures only a fraction of the total benefit. In both cases, the divergence between private cost-benefit calculation and social cost-benefit calculation produces a predictable market failure.

This is not a moral failure — it is a structural one. The decision-maker is not evil for failing to account for costs they do not bear; they are responding rationally to their situation. Pigouvian analysis makes the structural problem visible: the social optimum and the private optimum diverge whenever externalities exist. And wherever they diverge, there is scope for a policy or institutional intervention that realigns them — tax (for negative externalities), subsidy (for positive externalities), property rights (Coase's alternative), or social norms and regulation.

Ronald Coase's counter-argument (the Coase Theorem) adds a crucial qualification: when transaction costs are low and property rights are clear, private negotiation between parties can internalise externalities without government intervention — and produce the efficient outcome regardless of who holds the initial property right. In practice, transaction costs are often high, so Coase is a theoretical benchmark rather than a practical solution. But identifying whether transaction costs are low is a crucial diagnostic step.

---

## Your Process

**Step 1: Identify the decision and the decision-maker**
Clarify what decision is being made, who is making it, and what the decision-maker's cost-benefit calculation looks like from their perspective alone. Establish the baseline: what does the decision-maker see as costs and benefits?

**Framing check:** Confirm the decision and the scope of effects before continuing. State what you've identified in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [one-sentence framing — the decision being made and the concern that costs or benefits are falling on parties outside the decision]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Map affected third parties**
Who else is affected by this decision who is not part of the decision-maker's calculation? Cast the net wide: downstream effects, neighbourhood effects, time-lagged effects, effects on non-human stakeholders (environment), effects on future parties. Distinguish between parties who are affected positively (positive externalities — they receive a benefit they did not pay for) and negatively (negative externalities — they bear a cost they did not choose).

**Step 3: Quantify the externalities**
For each affected party, estimate the magnitude of the external effect. This does not need to be precise — it needs to be directionally correct and clearly communicated. Use: monetary estimates where possible, physical or health measures where monetary conversion is contested, and ordinal rankings (large/medium/small) where quantification is not feasible. Note when external costs are diffuse (spread across many parties) vs. concentrated.

**Step 4: Calculate the wedge**
The externality wedge is the gap between the private optimum (what the decision-maker will choose) and the social optimum (what would be chosen if all costs and benefits were internalised). Quantify the wedge: how much more or less of the activity will occur under private calculation vs. the social optimum? The size of this wedge determines the scale of the market failure and the urgency of intervention.

**Step 5: Assess internalisation mechanisms**
For each externality, evaluate the available mechanisms for internalisation:
- **Pigouvian tax/subsidy:** Tax the negative externality; subsidise the positive. The mechanism is efficient if the tax/subsidy equals the marginal external cost/benefit. Practical limitation: measuring the marginal external cost accurately is hard.
- **Property rights (Coase):** If transaction costs are low, assign clear property rights and let parties negotiate. Ask: are transaction costs actually low here? If yes, Coasian bargaining may work. If no, it won't.
- **Regulation:** Command-and-control standards (emissions limits, building codes, vaccination requirements). Blunt but reliable when monitoring is feasible.
- **Social norms:** Informal enforcement via reputation, shame, or community pressure. Effective at small scales; unreliable at large ones.
- **Voluntary internalisation:** The actor voluntarily bears the external cost. Ask: what would make this rational for them? (Reputation, certification, consumer demand for ethical goods.)

**Step 6: Rank and recommend**
Rank mechanisms by: (a) likely effectiveness at closing the wedge, (b) feasibility given political, legal, and administrative constraints, (c) unintended consequences. Identify the preferred approach and the conditions under which it works.

---

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences, then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full analysis** — Complete all steps, reasoning shown throughout
  - **Key findings only** — Bottom-line output, skip step-by-step detail
  - **Specific focus** — Zoom in on one aspect of this analysis
  - **Reframe** — The read is off; correct it and the analysis will follow the corrected framing

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

## Output Format

**Decision and Private Cost-Benefit**
[What is being decided; what the decision-maker's private calculation looks like]

**Externality Map**

| Affected party | Effect direction | Nature of effect | Estimated magnitude | Diffuse or concentrated? |
|---|---|---|---|---|
| [Party] | Negative / Positive | [e.g., pollution, health risk, network benefit] | [£ or scale] | [Diffuse/Concentrated] |

**The Wedge**
[Private optimum vs. social optimum — how much more/less of the activity than is socially optimal]

**Internalisation Mechanisms**

| Mechanism | Expected effectiveness | Feasibility | Key risk |
|---|---|---|---|
| Pigouvian tax/subsidy | [High/Med/Low] | [High/Med/Low] | [measurement accuracy, political resistance] |
| Property rights (Coase) | [High/Med/Low] | [High/Med/Low] | [transaction costs] |
| Regulation | [High/Med/Low] | [High/Med/Low] | [monitoring cost, rigidity] |
| Social norms | [High/Med/Low] | [High/Med/Low] | [scale, enforcement] |

**Recommended Approach**
[Preferred mechanism(s), conditions for effectiveness, and what implementation would require]

---

## Notes

The standard error in externality analysis is focusing only on negative externalities (pollution, harm) and missing the positive ones. Positive externalities — education, vaccination, open-source software, urban density, basic research — are systematically underproduced by markets because the producer cannot capture the full social benefit. The subsidy logic for positive externalities is exactly as rigorous as the tax logic for negative ones.

Coase's insight is frequently misapplied: "since parties can negotiate, government intervention isn't needed." The Coase Theorem requires not just clear property rights but *low transaction costs* — a condition that fails for most significant externalities (thousands of affected parties, strategic holdout, information asymmetry). Use Coase as a diagnostic: if transaction costs are genuinely low, negotiate. If not, Pigouvian or regulatory solutions are necessary.

Pairs naturally with `/s4h-economics-incentive-mapping` (externalities are often the result of misaligned incentives — the decision-maker doesn't bear the cost because the structure doesn't make them) and `/s4h-economics-coordination` (when the externality is diffuse and requires collective action to address). For systemic externalities embedded in feedback dynamics, see `/s4h-systems-feedback-mapping`.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Externalities mapped. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-economics-incentive-mapping` — Understand what incentive structure is producing this externality — and how to redesign it
  - `/s4h-economics-coordination` — The externality affects a diffuse group; addressing it requires collective action
  - `/s4h-game-theory-mechanism-design` — Design the rules so the decision-maker is pushed toward the socially optimal choice
  - **Done** — Wrap up and synthesise what we have so far

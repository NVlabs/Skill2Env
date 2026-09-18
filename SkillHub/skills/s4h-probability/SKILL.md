---
name: s4h-probability
description: "Entry point for the probability toolkit. Routes to the right probabilistic thinking skill based on your situation. Use when you say 'probability', 'how likely', 'am I overconfident', 'quantify this', 'what's the base rate', 'expected value', 'scenario weighting', or want probabilistic reasoning applied without knowing which specific tool fits."
---

# Probability

Applies probabilistic thinking to estimates, decisions, and uncertainty. Diagnoses what kind of probability work is needed and applies the right tool.

## Which tool fits

| You need to... | Tool |
|---|---|
| Anchor estimates in historical base rates before adjusting | base-rate-anchoring |
| Test whether stated confidence matches available evidence | confidence-calibration |
| Calculate expected value to compare options under uncertainty | expected-value-calculation |
| Assign probabilities to distinct scenarios before deciding | scenario-weighting |

## Routing Decision

- **Estimate feels optimistic — want the outside view** → base-rate-anchoring
- **Unsure how confident to be, or whether confidence is warranted** → confidence-calibration
- **Comparing options with different payoffs and probabilities** → expected-value-calculation
- **Multiple plausible futures and need to think through each** → scenario-weighting
- **Unclear** → confidence-calibration; establishing what confidence is warranted usually determines what other analysis is needed

**Framing check:** Confirm the specific situation and the type of uncertainty being reasoned about before routing. State what you've identified — the actual subject being estimated or decided, and the core uncertainty — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the situation and the uncertainty at stake]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

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

## Base Rate Anchoring

*Anchors estimates in historical base rates before adjusting for specifics.*

Before adjusting for what makes this situation special, establish what usually happens in situations like this one. Find the reference class: what category of event is this? What is the historical base rate for that category? Now adjust: what specific factors make this situation better or worse than the reference class? The adjustment should be modest unless the specific factors are genuinely exceptional; most people underweight the base rate and overweight the specifics.

**Output:** Reference class identified, base rate established, specific adjustments with justification, and the final calibrated estimate.

---

## Confidence Calibration

*Tests whether stated confidence levels match available evidence.*

State the current confidence level. Now audit it: what is the evidence for this belief? How strong is that evidence? What evidence against have you considered? Are you more confident than the evidence warrants (overconfidence — common) or less confident than it warrants (underconfidence — less common but real)? Good calibration means your 80% confident predictions come true about 80% of the time.

**Output:** Confidence audit — evidence for, evidence against, sources of overconfidence, and a recalibrated confidence level with reasoning.

---

## Expected Value Calculation

*Calculates expected value to compare options under uncertainty.*

For each option: list possible outcomes and their probabilities. Estimate the value (positive or negative) of each outcome. Calculate expected value: sum(probability × value) for each outcome. Compare across options. Identify if any option has asymmetric risk — limited downside, large upside — which expected value captures but intuition often misses.

**Output:** Expected value calculation for each option, comparison table, and interpretation of the asymmetry or risk profile.

---

## Scenario Weighting

*Assigns explicit probabilities to distinct scenarios before making a decision.*

Define 3-5 mutually exclusive, collectively exhaustive scenarios for how this situation could unfold. For each scenario: what are the key conditions that make it happen? Assign a probability to each (they must sum to 100%). For each scenario: what decision is optimal? Now aggregate: given the scenario probabilities, what is the best overall decision?

**Output:** Scenario inventory with probabilities, optimal decision per scenario, and the overall recommendation weighted by scenario probabilities.

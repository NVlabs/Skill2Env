---
name: s4h-economics-opportunity-cost
description: "Maps the true cost of a choice by making explicit what is foregone. Triggers: 'opportunity cost', 'what am I giving up', 'what else could I do with this', 'hidden cost', 'what's the real cost of this', 'what are we not doing by doing this', any decision where the cost of the chosen path needs to be compared against the best alternative."
---

# Economics: Opportunity Cost

Alfred Marshall gave us the concept; every decision-maker needs it. The price you pay is not the cost of a choice — the cost is the value of the next-best thing you could have done with the same resources. Paying £100 for a concert ticket costs you £100 plus whatever you would have done with that money otherwise. Spending three hours on a low-value meeting costs you three hours of whatever you could have produced in that time. Most analyses never make this visible — they count what was spent without asking what was foregone.

Opportunity cost thinking reframes every decision from "can we afford this?" to "is this the best available use of what we have?" It exposes apparently free choices as costly ones (choosing between two opportunities means giving one up entirely), and it reveals that inaction is never neutral — not choosing is itself a choice with a cost. This discipline traces to Marshall's *Principles of Economics* (1890) and remains the foundational move in economic reasoning.

The hardest application is to time and attention: these resources feel free because no invoice arrives. But time spent on one thing is precisely time not spent on another. Opportunity cost makes the invoice visible.

---

## Your Process

**Step 1: Define the choice**
Clarify what decision is being made and what resource is being allocated — money, time, capital, headcount, attention, or some combination. Be specific: opportunity cost analysis requires knowing what is actually being committed.

**Framing check:** Confirm the choice and the resource being committed before continuing. State what you've identified in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [one-sentence framing — the specific choice and the resource being committed]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Map all alternatives**
Generate the full set of alternatives that would use the same resource. These are not wish-list options — they are genuinely available alternatives that would be foregone. Ask: what else could we do with this money, time, or capacity? Include both active alternatives (other things we could do) and passive alternatives (not deploying the resource — keeping the cash, keeping the team available, maintaining optionality).

**Step 3: Identify the next-best alternative**
From the alternatives, identify which one is best — the option that would be chosen if the current choice were ruled out. This is the opportunity cost benchmark. The cost of the current choice is the value of this best available alternative. Note: this is not the average value across all alternatives, and not the total value of all alternatives combined — it is specifically the *next-best single alternative*.

**Step 4: Estimate the value of the foregone alternative**
Assign a value to the next-best alternative. This might be: financial return, strategic position, optionality, risk reduction, or qualitative value. Wherever possible, quantify. Where you cannot, use an explicit scale or ranking. The goal is to make the comparison real — not to achieve false precision.

**Step 5: Compare total costs**
Compare the current choice against the next-best alternative using total cost, where total cost = explicit (accounting) cost + opportunity cost. Sometimes this reveals that a cheap option is actually expensive (the explicit cost is low but the opportunity cost is high). Sometimes it reveals that an expensive option is justified (the opportunity cost of *not* doing it is even higher).

**Step 6: Test for implicit opportunity costs**
Check for opportunity costs that are easy to miss: (a) time and attention costs that don't appear on any budget; (b) optionality costs — what doors close by committing to this path; (c) indirect costs — what the organisation or individual cannot do while this commitment is in place.

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

**Choice Being Evaluated**
[The decision, the resource being committed, and the timeframe]

**Alternatives Considered**
[Full map of available alternatives for the same resource]

**Next-Best Alternative (Opportunity Cost Benchmark)**
[The best foregone option, with its estimated value]

**Total Cost Comparison**

| | Current Choice | Next-Best Alternative |
|---|---|---|
| Explicit cost | [£/hours/headcount] | [£/hours/headcount] |
| Expected return/value | [value] | [value] |
| Opportunity cost | [value of next-best] | — |
| **Total economic cost** | [explicit + opportunity] | — |

**Hidden Opportunity Costs**
[Time, attention, optionality, or strategic costs not captured above]

**Verdict**
[Does the choice hold up once total cost is visible? What conditions would change the answer?]

---

## Notes

Opportunity cost is the most commonly skipped step in decision analysis. Teams evaluate whether they can afford something (explicit cost check) without asking whether this is the best use of what they're spending. The result is decisions that clear a low bar when they should be clearing a higher one.

The hardest application is to non-financial resources. Time and attention feel free because no invoice arrives, but they are the scarcest resources in most organisations. A policy of "we'll do this because it doesn't cost anything" is economically illiterate — it treats opportunity cost as zero when it is often the dominant cost.

Pairs tightly with `/s4h-decision-criteria-weighting` (once alternatives are mapped, compare them on weighted criteria) and `/s4h-economics-margin` (when the question is whether to do *more* of something, not which of two discrete paths to take). When the reason to do something is strategic position rather than financial return, pair with `/s4h-strategy-positioning` to assess what the foregone option was worth.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Opportunity cost mapped. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-economics-incentive-mapping` — Understand what the incentive structure rewards — and whether it points toward the right choice
  - `/s4h-decision-criteria-weighting` — Run a full weighted comparison now that all options are on the table
  - `/s4h-economics-margin` — The question is how much to do, not which path to take
  - **Done** — Wrap up and synthesise what we have so far

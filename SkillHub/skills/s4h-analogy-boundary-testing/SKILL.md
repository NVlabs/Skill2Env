---
name: s4h-analogy-boundary-testing
description: "Finds where an analogy breaks down before it's relied upon. Analogies fail silently — the damage happens when decisions are made on a mapping that doesn't hold in the relevant dimension. Triggers: 'stress-test this analogy', 'where does this comparison break', 'does this really apply', 'test the metaphor', 'where is the analogy wrong'."
---

# Analogy Boundary Testing

Analogies are tools, not truths. The danger is not using an analogy — it is using one past
its boundary. Analogies fail silently: the flaw is invisible until a decision has been made
that depended on the part that didn't hold. This skill finds the boundary before that
happens.

---

## Your Process

**Step 1: State the Analogy**
Write it explicitly: "X is like Y." Name the analogy being tested, the domain it comes
from, and the claim being made on the basis of it.

**Framing check:** Confirm the specific analogy before continuing. State what you've identified — the source domain, target domain, and the claim being made — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the analogy and the claim it supports]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different analogy or claim than read; incorporate the correction before proceeding

**Step 2: List Similarities**
What does the analogy capture correctly? List every genuine parallel — the aspects where
the structural correspondence is real. This is not validation; it's establishing what the
analogy is good for before finding what it isn't.

**Step 3: List Differences**
Every meaningful divergence between X and Y is a potential failure point. List them
systematically: different actors, different dynamics, different constraints, different
feedback mechanisms, different scales, different reversibility. Be thorough — incomplete
difference-listing is the most common failure mode here.

**Step 4: Test Each Difference Against the Decision**
**Before narrowing:** Show the complete list of differences from Step 3 to the user first. Use `AskUserQuestion`:
- **Question:** "I've identified [N] differences. Before I filter to those relevant to your decision, are there any you'd flag as especially important, or any I've missed?"
- **Header:** "Prioritise"
- **Options:**
  - **Proceed with your selection** — the set looks right
  - **Flag one** — user will name a specific difference to include
  - **Add a missing one** — user will describe it

For each decision or conclusion being made on the basis of this analogy: which differences
are relevant to that specific decision? A difference that doesn't affect the conclusion is
harmless. A difference that does affect it invalidates the reasoning.

**Step 5: Does the Conclusion Still Hold?**
For each relevant difference identified in Step 4: if this difference is real, does the
conclusion derived from the analogy still follow? If not, the analogy cannot support that
conclusion.

**Step 6: State Safe Scope**
Where can this analogy be validly relied upon? What does it illuminate, and what decisions
can it inform? State the boundary clearly.

---

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences — what is being analyzed and what the core question is — then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full analysis** — Complete all steps, reasoning shown throughout
  - **Key findings only** — Bottom-line output, skip step-by-step detail
  - **Breaking points only** — Where the analogy fails, not where it holds
  - **Reframe** — The read is off; correct it and the analysis will follow the corrected framing

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

## Output Format

**Analogy:** [X is like Y — domain and claim]

**Similarities (what the analogy captures correctly):**
> [Bulleted list]

**Differences (potential failure points):**
> [Bulleted list — be thorough]

**Relevant differences for this decision:**

| Difference | Relevant to decision? | Effect on conclusion |
|------------|----------------------|----------------------|
| | | |
| | | |

**Conclusion validity:**
> [Does the analogy support the conclusion? Yes / Partially / No — with reason]

**Safe scope — what this analogy validly applies to:**
> [Bounded statement]

---

## Notes

The most useful output is the safe scope statement — a positive claim about where the
analogy is reliable. Discarding an analogy entirely because it has limits wastes the
genuine insight it contains.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Analogy boundaries tested. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-analogy-domain-transfer` — Now that boundaries are clear, execute the transfer carefully
  - `/s4h-logic-check` — Check whether conclusions crossed a boundary they shouldn't have
  - `/s4h-constraint-hardness-testing` — Are the boundary differences hard constraints or soft?
  - **Done** — Wrap up and synthesise what we have so far

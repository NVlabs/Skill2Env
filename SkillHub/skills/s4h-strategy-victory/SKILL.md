---
name: s4h-strategy-victory
description: "Defines what winning actually means before the contest begins — prevents the pyrrhic trap of winning in ways that lose the larger goal. Triggers: 'what does winning look like', 'define victory', 'victory conditions', 'what are we actually trying to achieve', 'define success', 'is winning worth it', 'pyrrhic trap', 'are we optimizing for the right thing'."
---

# Strategy: Victory

Clausewitz's central insight in *On War*: "War is the continuation of politics by other means." The military contest is not the point; it is a means to a political end. The moment a commander loses sight of the political objective and optimizes purely for military victory, they have already failed strategically — because a military win that undermines the political aim is worse than a negotiated settlement.

The same principle applies to any contest. A company that wins a price war by destroying its margins has won the battle and lost the business. A legal team that wins at trial and spends three years doing it, producing a verdict worth less than the settlement foregone, has won the judgment and lost the case. A negotiator who extracts every possible concession and destroys the relationship needed for implementation has won the negotiation and lost the outcome. The pyrrhic trap is the failure to define victory before the contest forces its own definition on you.

Sun Tzu's corollary: "The supreme art of war is to subdue the enemy without fighting." This is not a counsel of passivity — it is the recognition that the cheapest possible victory is the right objective. A victory that requires the maximum cost is a strategic failure even when it succeeds. Minimum victory conditions exist for a reason: they prevent over-prosecution of a contest that has already been won.

---

## Your Process

**Step 1: Stated objective**
What are you trying to achieve? Name it as it is currently framed.

**Framing check:** Confirm the specific contest and objective before continuing. State what you've identified — the actual situation being analyzed and what winning is currently defined as — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the specific contest and its stated objective]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Real objective**
What would you actually have if you achieved the stated objective? What is the objective behind the stated one — the political end, in Clausewitz's terms? Why does the stated objective matter? Sometimes the stated objective is the real one; often it is a proxy for something deeper, and winning the proxy while losing the underlying goal is precisely the pyrrhic trap.

**Step 3: Minimum victory**
The least outcome you would accept as a win. What must be true for this effort to have been worth it? Minimum victory conditions often look unsatisfying in advance — they feel like compromises. They are not. They are the protection against prosecuting a contest past the point of value.

**Step 4: Maximum victory**
What would unequivocally mean you won? What outcome makes the cost obviously worthwhile, regardless of what it took? Maximum victory conditions serve a different function: they tell you when to stop pressing once you've reached them.

**Step 5: Pyrrhic check**
What does winning cost at maximum force? At minimum force? At the likely cost, is the maximum victory worth it? Is the minimum victory worth it? Name the specific things you could lose — relationships, capital, time, reputation, flexibility — by prosecuting this contest. What would constitute a pyrrhic outcome even on a win?

**Step 6: Victory recognition**
How will you know when you've won? What observable condition tells you to stop? This is the step most often skipped — and its absence produces contests that continue past their objective, consuming additional resources toward a goal already achieved or already unachievable.

---

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences — what is being analyzed and what the core question is — then ask:

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

### Victory Definition

**Stated Objective**
[How the objective is currently framed]

**Real Objective**
[The underlying political end — why the stated objective matters, and what you'd actually have if you achieved it]

**Minimum Victory**
[The least outcome that makes this worth the effort — what must be true]

**Maximum Victory**
[The unequivocal win — what makes the cost obviously worthwhile]

**Pyrrhic Check**
[What winning costs — and what would constitute a pyrrhic outcome even on a technical win]

**Victory Recognition Conditions**
[Observable conditions that tell you to stop — you have won, or you have lost and further prosecution only adds cost]

---

## Notes

Run this before any other strategy skill when the objective is unclear — all other skills operate in service of a defined objective, and without one, they produce well-structured answers to the wrong question. Pairs tightly with `/s4h-strategy-force-economy`: knowing minimum and maximum victory conditions shapes how much force to deploy, and when the minimum has been achieved. When the pyrrhic check suggests the cost of maximum victory is unacceptable, use `/s4h-strategy-alliance` and `/s4h-strategy-positioning` to understand whether the cost can be reduced before the contest begins.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Victory conditions defined. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-strategy-positioning` — Position to achieve the victory conditions
  - `/s4h-decision-premortem-analysis` — Stress-test the victory definition
  - `/s4h-strategy-timing` — Time moves toward victory
  - **Done** — Wrap up and synthesise what we have so far

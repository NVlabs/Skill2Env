---
name: s4h-strategy-force-economy
description: "Finds the minimum intervention that achieves the objective — especially when you're outgunned or under-resourced. Triggers: 'do more with less', 'force economy', 'we're under-resourced', 'asymmetric advantage', 'outgunned', 'leverage point', 'how do we win when they have more', 'we can't outspend them', 'small team big problem'."
---

# Strategy: Force Economy

Sun Tzu's highest strategic achievement is the victory that costs nothing — where the opponent's resistance collapses without direct contest: "Supreme excellence consists in breaking the enemy's resistance without fighting." This is not passivity. It is the discipline of identifying where a small input creates a large output — where the terrain, timing, information asymmetry, or a single relationship multiplies your effective force without requiring you to match the opponent unit for unit.

The force economy principle asks: what is the minimum intervention that achieves the objective? Not merely because resources must be conserved (though they must), but because the maximum-force approach almost always generates the maximum resistance. Brute force signals intention, consumes capital, and invites a symmetrical response from an opponent with more of everything. The indirect approach — Basil Liddell Hart's formulation — achieves more by creating the conditions in which less is required.

The discipline is finding the leverage point: the node in the system where a small input produces a disproportionate output. Not all nodes are equal. Most effort has roughly proportional effect. Leverage points are structural exceptions — and finding them before acting is the core skill.

---

## Your Process

**Step 1: State the objective**
Define what success looks like clearly and specifically. Vague objectives produce vague force economy analyses. What must be true for this to be considered won?

**Framing check:** Confirm the specific situation before continuing. State the objective and the resource constraint in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the objective and the resource or competitive constraint]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Maximum-force approach**
What does the brute-force path look like? If you matched the opponent resource-for-resource and attacked directly, what would that cost in time, money, relationships, and attention? Name the full cost. This is your baseline.

**Step 3: Minimum-force alternatives**
What approaches achieve the same objective at lower cost? Generate at least three alternatives — not as compromises but as genuine paths. Consider: approaches that go around rather than through, approaches that use the opponent's own momentum, approaches that make the contested ground irrelevant.

**Before narrowing:** Show the complete generated set of alternatives to the user first. Use `AskUserQuestion`:
- **Question:** "I've identified [N] minimum-force alternatives. Before I select the most promising, are there any you'd flag as especially important, or any I've missed?"
- **Header:** "Prioritise"
- **Options:**
  - **Proceed with your selection** — the set looks right
  - **Flag one** — user will name a specific alternative to include
  - **Add a missing one** — user will describe it

**Step 4: Leverage points**
Where in this system does a small input create a large output? Candidates: a key relationship that unlocks others, an information advantage that reshapes the opponent's behavior, a timing move that creates conditions others must respond to, a position that creates a cascade of favorable effects without requiring follow-on force.

**Before narrowing:** Show all identified leverage point candidates to the user before selecting the highest-leverage node. Use `AskUserQuestion`:
- **Question:** "I've identified [N] leverage point candidates. Before I select the single highest-leverage node, are there any you'd flag as especially critical, or any I've missed?"
- **Header:** "Prioritise"
- **Options:**
  - **Proceed with your selection** — the set looks right
  - **Flag one** — user will name a specific leverage point to prioritise
  - **Add a missing one** — user will describe it

**Step 5: Non-contest approaches**
Can the objective be achieved without direct competition at all? Options: go around (find uncontested ground), ally with (add force through alliance), make irrelevant (change the game so the contested position no longer matters), wait (until the opponent's overextension creates the opening).

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

### Force Economy Analysis

**Objective**
[Specific statement of what winning looks like]

**Maximum-Force Approach**
[What the brute-force path costs — time, money, relationships, attention, risk]

**Minimum-Force Alternatives**
1. [Alternative 1 — approach and estimated cost]
2. [Alternative 2 — approach and estimated cost]
3. [Alternative 3 — approach and estimated cost]

**Leverage Point**
[The single highest-leverage node — small input, large output — and why it has this property]

**Non-Contest Approaches**
[Options that achieve the objective without direct competition — go around, ally with, make irrelevant, wait]

**Recommended Approach**
[The recommended path with resource estimate and the reasoning for why this achieves the objective at acceptable cost]

---

## Notes

Good position reduces force required — pair with `/s4h-strategy-positioning` to understand whether investment in positioning now reduces force cost later. Alliances multiply effective force — pair with `/s4h-strategy-alliance` when the leverage point involves bringing others in. Force economy analysis is most powerful when the objective is clear; if it isn't, run `/s4h-strategy-victory` first to establish what you're actually trying to achieve.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Force economy mapped. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-resource-leverage-mapping` — Find leverage that amplifies force economy
  - `/s4h-strategy-positioning` — Position to maximise force economy
  - `/s4h-resource-allocation-analysis` — Allocate to the areas of greatest force economy
  - **Done** — Wrap up and synthesise what we have so far

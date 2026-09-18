---
name: s4h-strategy-alliance
description: "Maps parties, identifies natural allies and swing parties, and assesses alliance stability for coalition-building in competitive contexts. Triggers: 'build alliances', 'coalition building', 'who are my allies', 'manage stakeholders', 'political coalition', 'alliance strategy', 'who do I need on my side', 'get people on board', 'organizational politics'."
---

# Strategy: Alliance

Machiavelli's counter-intuitive warning in *The Prince*: alliances built on goodwill are fragile; alliances built on shared interest are durable. A prince who relies on gratitude will be disappointed the moment the interest calculus changes. A prince who builds alliances on the foundation of mutual benefit will hold them through adversity because both parties have a reason — independent of sentiment — to maintain the relationship.

Sun Tzu's operational principle complements this: "Know the local situation." Before deciding who to ally with, who to neutralize, and who to oppose, you must know what each party actually wants — not what they say they want, not what you hope they want, but what their actual interest is in this situation. Misreading a party's interest and trying to ally with them on incorrect assumptions produces a fragile alliance at best and an active opponent at worst.

The most common alliance error is the inverse: trying to win everyone over. Alliances have a cost — they create obligations, signal positions, and consume relationship capital. The discipline is identifying which alliances are necessary, which neutralizations are sufficient, and which parties are simply not worth the investment. Alliances managed poorly — obligations created without the support they were supposed to purchase — are worse than no alliances. They drain resources and signal weakness.

---

## Your Process

**Step 1: Party map**
List everyone involved in or affected by this situation. For each: what do they actually want (not what they say), what is their current position relative to your objective, and what is their capacity to help or hurt you?

**Framing check:** Confirm the specific alliance situation before continuing. State what you've identified — the objective being pursued, the competitive or political context, and the rough set of parties involved — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the objective, context, and parties]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Natural allies**
Parties whose interests align closely with yours without requiring significant trade-offs. Their success and yours point in the same direction. These require minimal persuasion — the main task is making the alignment explicit and activating it. Natural allies should be your first moves.

**Step 3: Swing parties**
Parties who could go either way. What would it take to align them? Is the cost of alignment (concessions, time, reciprocal obligations) worth the support gained?

**Before narrowing:** Show the complete list of identified swing parties to the user first. Use `AskUserQuestion`:
- **Question:** "I've identified [N] swing parties. Before I assess which are worth pursuing, are there any you'd flag as especially important, or any I've missed?"
- **Header:** "Prioritise"
- **Options:**
  - **Proceed with your selection** — the set looks right
  - **Flag one** — user will name a specific swing party to prioritise
  - **Add a missing one** — user will describe a party not yet included

For each swing party: name the minimum offering that tips them, and whether that offer is actually available to you.

**Step 4: Parties to neutralize**
Parties who might oppose you but needn't be actively won over — just prevented from acting against you. Neutralization is different from alliance: you are not asking for support, only for non-interference. This is often cheaper and more achievable than active alignment. What would each potential opponent need to remain neutral?

**Step 5: Alliance stability**
What holds each proposed alliance together? Shared interest (durable), reciprocal obligation (moderately durable), goodwill (fragile), fear (durable while the fear holds but brittle on its removal). Apply Machiavelli's test: if the interest calculus changed tomorrow, would this party still be with you? Name every alliance that fails this test.

**Step 6: Machiavelli test**
For each alliance being proposed: is it based on genuine shared interest, or on the assumption of goodwill? Goodwill alliances require active maintenance and may not hold under pressure. Name them, and either identify the underlying interest that makes them durable or build in contingency.

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

### Alliance Map

**Party Inventory**

| Party | Actual interest | Current position | Capacity |
|---|---|---|---|
| [Name] | [What they actually want] | [Aligned / Neutral / Opposed] | [High / Medium / Low] |

**Natural Allies**
[Parties with genuine interest alignment — activation approach for each]

**Swing Parties and Alignment Conditions**
[Each swing party, the minimum offering that tips them, and whether that offering is available]

**Parties to Neutralize**
[Potential opponents — what they need to remain non-interfering, and the cost of that neutralization]

**Alliance Stability Assessment**
[For each proposed alliance: what holds it together, Machiavelli test result, stability rating]

**Recommended Structure**
[Which alliances to build, which parties to neutralize, which to deprioritize — sequenced by priority and feasibility]

---

## Notes

Alliances multiply effective force — pair with `/s4h-strategy-force-economy` when the question is how to achieve an objective against a stronger opponent. Knowing what parties actually want requires intelligence work — pair with `/s4h-strategy-intelligence` when the party map is uncertain. Use `/s4h-strategy-terrain` to understand which parties hold positions of structural advantage that would make them particularly valuable allies or particularly dangerous opponents.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Alliance strategy mapped. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-game-theory-coalition` — Analyse the coalition game dynamics of the alliance
  - `/s4h-social-coalition-mapping` — Map social dynamics within the alliance
  - `/s4h-strategy-positioning` — Position to benefit from the alliance
  - **Done** — Wrap up and synthesise what we have so far

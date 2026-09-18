---
name: s4h-strategy-positioning
description: "Builds the conditions for competitive unassailability before the contest begins. Triggers: 'create a position', 'competitive positioning', 'make myself the obvious choice', 'how do I make myself hard to compete with', 'strategic positioning', 'establish advantage before competing', 'what makes me hard to displace', 'build a moat'."
---

# Strategy: Positioning

Sun Tzu: "The good fighters of old first put themselves beyond the possibility of defeat, and then waited for an opportunity of defeating the enemy." The first move is not to attack — it is to make yourself unassailable. Position precedes contest.

Michael Porter's parallel insight in competitive theory: sustainable advantage comes not from trying to be best at everything, but from choosing not to compete everywhere. A position that is genuinely defensible requires trade-offs — commitments that make you excellent in one direction at the cost of flexibility in others. The value of the trade-off is precisely that it cannot be easily replicated by a competitor without abandoning their own position. A competitor who tries to copy you has to give up what they've optimized for. That is what makes a position real.

The failure mode is positioning by assertion: saying you occupy a position without doing the investment that makes it true. Genuine positioning requires assets, capabilities, relationships, or reputations that are costly to build and therefore difficult to replicate. The question is not "where do I want to be?" but "what would I need to truly hold this ground?"

---

## Your Process

**Step 1: Ideal unassailable position**
What would it look like to hold a position that a rational, well-resourced opponent would choose to go around rather than contest directly? Describe the ideal: what would you be known for, what would you own, what would your relationships and reputation make you? Be specific — "market leader" is not a position. "The only reliable provider for this niche, with a five-year track record and the three key relationships in the sector" is a position.

**Framing check:** Confirm the specific competitive situation before continuing. State what you've identified — the actor seeking the position, the competitive arena, and the opponent context — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of who is positioning, in what arena, against what competitive pressure]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Required assets and capabilities**
What would you need to hold that position? List specifically: skills, relationships, reputation, information, technology, capital, team, time. What do you currently have? What is missing?

**Step 3: Current position**
Honest assessment of where you stand today. What do you actually own in this competitive landscape? Not what you aspire to, not what you're building toward — what position do you hold right now that an opponent would need to consider?

**Step 4: Gap-widening moves**
What investments or actions create the largest gap between your current position and any attacker's ability to replicate it?

**Before narrowing:** Show the complete set of candidate gap-widening moves to the user first. Use `AskUserQuestion`:
- **Question:** "I've identified [N] potential gap-widening moves. Before I select the highest-leverage ones, are there any you'd flag as especially important, or any I've missed?"
- **Header:** "Prioritise"
- **Options:**
  - **Proceed with your selection** — the set looks right
  - **Flag one** — user will name a specific move to include
  - **Add a missing one** — user will describe it

Rank by leverage: which moves create the deepest moat per unit of investment? Which moves compound — making future moves easier?

**Step 5: Position test**
Would a rational, well-resourced opponent, looking at your fully-built position, choose a different arena rather than attack you here? If the honest answer is "no — they'd still come at us," then the position isn't unassailable yet. Name what's missing.

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

### Positioning Analysis

**Ideal Unassailable Position**
[Specific description — what you own, what you're known for, what relationships you hold, what makes a rational opponent go around rather than through]

**Required Assets and Capabilities**
- *Have:* [What you currently hold that contributes to this position]
- *Need:* [What is missing — specific gaps between current state and ideal]

**Current Position**
[Honest assessment of what you actually own today]

**Gap-Widening Moves**
[Ranked investments and actions — highest leverage per unit of investment first]

**Position Test Result**
[Would a rational, well-resourced opponent choose a different arena? What's missing if no]

**Implementation Path**
[Sequenced steps — what to build first, in what order, over what timeframe]

---

## Notes

Terrain analysis identifies which positions are available — run `/s4h-strategy-terrain` first when you're not yet sure which positions exist worth holding. Better positioning reduces force required to defend: pair with `/s4h-strategy-force-economy` to understand how position investment pays back in reduced ongoing cost. For the specific timing of when to build vs. when to contest now, pair with `/s4h-strategy-timing`.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Position mapped. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-strategy-timing` — Time the position move
  - `/s4h-strategy-alliance` — Build alliances to strengthen the position
  - `/s4h-decision-premortem-analysis` — Stress-test the position before committing
  - **Done** — Wrap up and synthesise what we have so far

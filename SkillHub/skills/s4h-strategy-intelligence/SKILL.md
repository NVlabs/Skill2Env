---
name: s4h-strategy-intelligence
description: "Audits what you actually know vs. what you're assuming about yourself and your opponent before acting. Triggers: 'what do I actually know', 'intelligence audit', 'know your enemy', 'what am I assuming vs knowing', 'prep for negotiation', 'what information do I have', 'what don't I know about them', 'am I missing something important'."
---

# Strategy: Intelligence

Sun Tzu's most quoted principle — "Know yourself and know your enemy; in a hundred battles you will never be in peril" — is often treated as a slogan. Its operational meaning is precise: knowledge asymmetry determines outcomes before any action is taken. A general who knows the terrain, the opponent's strength, the opponent's commander, and his own limitations will defeat an equivalent force every time. A general who acts on assumption held as fact will suffer the predictable consequence.

The self-audit is as important as the opponent audit, and harder. Self-flattery is the most common intelligence failure. We know our strengths clearly; we hold our weaknesses vaguely. We know our opponent's stated position; we assume their actual constraints, motives, and fallback options. The intelligence discipline is the discipline of holding the line between what is known and what is assumed — because the gap is where strategic surprises live.

---

## Your Process

**Step 1: Self-audit**
List actual strengths, weaknesses, hard constraints, and available resources. Do not soften the weaknesses. Ask: what would embarrass you to admit in this situation? Those admissions are the accurate self-assessment. What dependencies do you have? What time pressures? What is your actual walk-away position?

**Framing check:** Confirm the specific situation before continuing. State what you've identified — the strategic situation, the opponent or counterparty, and the decision at stake — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the situation, opponent, and decision]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Opponent audit**
What do you know about their position, capabilities, constraints, and intentions? Separate every item into two columns: **Known fact** (directly observed, documented, confirmed) vs. **Assumption** (inferred, expected, believed but unverified). Most opponent assessments contain far more assumptions than facts — naming this is the point.

**Step 3: Intelligence gaps**
What would change your decision if you knew it? List all significant unknowns — every gap where your current assumption, if wrong, could alter your strategy.

**Before narrowing:** Show the complete list of identified gaps to the user first. Use `AskUserQuestion`:
- **Question:** "I've identified [N] intelligence gaps. Before I select the most critical, are there any you'd flag as especially important, or any I've missed?"
- **Header:** "Prioritise"
- **Options:**
  - **Proceed with your selection** — the set looks right
  - **Flag one** — user will name a specific gap to include in the top three
  - **Add a missing one** — user will describe an unknown not yet captured

Then narrow to the three most important gaps — where your current assumption, if wrong, would alter your strategy most significantly. Rank by impact.

**Step 4: Information-gathering paths**
For each top gap: how might it be closed before acting? What is available through legitimate observation, inquiry, public sources, or network access? What would it cost (time, money, relationship capital) to close each gap?

**Step 5: Assumption risk rating**
For each current assumption in the opponent audit: rate the risk if that assumption is wrong. High — strategy fails if wrong. Medium — strategy degrades but survives. Low — minor adjustment required. Highlight the high-risk assumptions.

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

### Intelligence Audit

**Self-Assessment**
- *Strengths:* [Genuine strengths in this context]
- *Weaknesses:* [Candid — include what would be embarrassing to admit]
- *Hard constraints:* [Time, resources, relationships, walk-away limits]

**Opponent Assessment**

| Item | Status | Risk if wrong |
|---|---|---|
| [Known fact 1] | Known | — |
| [Assumption 1] | Assumption | High/Medium/Low |
| ... | | |

**Intelligence Gaps (ranked by impact)**
1. [Most important unknown — what would change if you knew it]
2. [Second most important unknown]
3. [Third most important unknown]

**Recommended Information Gathering**
[For each top gap: how to close it, what it costs, whether it's worth closing before acting]

**Assumption Risk Summary**
[High-risk assumptions that could cause strategic failure — these are the decisions to hold until more intelligence is available]

---

## Notes

Pairs with `/s4h-strategy-terrain` — intelligence informs the terrain map, and an inaccurate terrain map comes from treating assumptions as facts. Pairs with `/s4h-strategy-deception` — once you know what your opponent currently believes about you, you can manage that belief deliberately. Use `/s4h-strategy-timing` to determine whether gathering more intelligence before acting is worth the delay.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Intelligence gathered. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-strategy-positioning` — Use the intelligence for strategic positioning
  - `/s4h-strategy-deception` — Use intelligence to detect or plan deception
  - `/s4h-game-theory-signaling` — Interpret signals with the intelligence gathered
  - **Done** — Wrap up and synthesise what we have so far

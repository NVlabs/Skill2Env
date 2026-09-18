---
name: s4h-play-perspective-reversal
description: "Fully inhabits the opposing perspective — competitor, critic, user, or adversary — to find what is invisible from your own position. TRIGGERS: 'steelman the opposition', 'think like the competitor', 'play devil's advocate', 'see it from their side', 'role reversal', 'inhabit the other perspective'."
---

# Play: Perspective Reversal

Every position has a blind spot — things that are invisible precisely because of
where you're standing. The opposing perspective sees those things clearly. This skill
requires fully setting aside your own position and genuinely inhabiting the other one
— without qualification, defence, or commentary — then returning to extract what was
revealed. Half-hearted perspective-taking (staying in your own frame while gesturing
at theirs) produces nothing. Full inhabitation produces findings.

---

## Your Process

**Step 1: Name the Opposing Perspective**
Who is the other position? Be specific — not "the market" but "a direct competitor
who has observed our strategy for two years and is now choosing where to attack." Not
"critics" but "the engineering team who built the previous system and believe this
replacement is solving the wrong problem." Specificity determines how much you can
genuinely inhabit.

**Framing check:** Confirm the specific opposing perspective before continuing. State the position you have identified — who they are, their vantage point, and their relationship to the situation — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the opposing perspective and their vantage point]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different perspective than read; incorporate the correction before proceeding

**Step 2: Set Aside Your Own Perspective**
This step is non-negotiable. For the duration of Steps 3-5, there is no defending,
no qualifying, no "but to be fair to our side." You are not you. You are them. You
have their information set, their incentives, their history with this issue, their
fears about the outcome. If you find yourself softening the opposing view or noting
exceptions, stop — you're still in your own frame.

**Step 3: From Their Perspective — What Is Wrong?**
What is wrong with the current approach, plan, or position? What is being missed,
underestimated, or misunderstood? What assumptions look clearly false from this
vantage point? What would a perceptive person standing here see that the other side
is blind to?

**Step 4: What Opportunity Are They Seeing?**
From their position: what opportunity exists that the current approach is failing to
take? What gap, weakness, or opening is visible from where they stand? What is the
version of the world they're operating from where their strategy makes complete sense?

**Step 5: Their Strategy**
If you were them, what would you do? What specific moves would you make to exploit
what you've just identified? Be concrete — not "they'll attack our weakness" but the
specific sequence of moves that their position makes available.

**Step 6: Re-enter and Assess**
Return to your own perspective. What did the opposing view reveal that is legitimate
— that you would have to concede is a real problem even under your own framework?
Classify each finding: must change (the critique is valid and the approach needs
adjustment), must defend (the approach is correct but vulnerable), must communicate
better (the approach is right but it's not landing).

---

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences — what is being analyzed and what the core question is — then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full analysis** — Complete all steps, reasoning shown throughout
  - **Key findings only** — Bottom-line output, skip step-by-step detail
  - **Opposing view only** — Fully inhabit the opposite position, skip the reflection and re-integration
  - **Reframe** — The read is off; correct it and the analysis will follow the corrected framing

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

## Output Format

**Opposing Perspective:** [who + their vantage point and information set, stated
fully and fairly]

**What They See That You Don't:** [the specific blind spots and missed assumptions
visible from their position]

**Their Strategy:** [the specific moves their position makes available — what they
would do and why]

**Legitimacy Assessment**

| Finding From Their Perspective | Legitimate? | Response Category |
|---|---|---|
| [what they see] | [yes / partially / no] | [must change / must defend / must communicate better] |

**Priority Actions**
- Must change: [what requires genuine adjustment to the approach]
- Must defend: [what is correct but needs to be made more robust]
- Must communicate better: [what is right but isn't landing — and the gap]

---

## Notes

The exercise fails if it becomes a performance of the other perspective rather than
genuine inhabitation. The test is whether you find something that makes you
uncomfortable — something you would prefer not to be true. If everything from the
opposing perspective turns out to be wrong or irrelevant, you didn't actually inhabit
it.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Perspective reversed. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-creativity-other-perspectives` — Apply structured other-perspectives to the reversed view
  - `/s4h-communication-audience-modeling` — Model how the reversed view changes communication
  - `/s4h-emotional-motivation-mapping` — Map motivations from the reversed perspective
  - **Done** — Wrap up and synthesise what we have so far

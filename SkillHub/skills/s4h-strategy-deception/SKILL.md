---
name: s4h-strategy-deception
description: "Manages information asymmetry in legitimate competitive contexts — what to protect, what impressions work in your favor, and what your opponent may be concealing from you. Triggers: 'conceal my position', 'information asymmetry', 'misdirection', 'what should I reveal vs conceal', 'negotiation deception', 'strategic ambiguity', 'manage what they know about me', 'read their signals'."
---

# Strategy: Deception

Sun Tzu's most provocative statement: "All warfare is based on deception." Its operational meaning is not that lying is the path to victory. It is that controlling what your opponent believes about you is as important as controlling what you do. A general who moves in predictable, transparent ways gives the opponent full information and eliminates the element of surprise. A general who manages information deliberately — signaling strength where they are strong, concealing weakness, appearing where unexpected — compounds their effective advantage at no additional resource cost.

In legitimate competitive contexts — negotiation, market positioning, competitive product strategy, organizational politics — managing information asymmetry is standard practice. Revealing your walk-away point in a negotiation, publishing your roadmap before it's locked, announcing your strategy before executing it: each of these transfers advantage to the other side. The discipline is not dishonesty; it is choosing what to make visible and what to protect.

One structural constraint governs everything: **whatever you conceal must be consistently concealed.** A single inconsistency destroys the deception more efficiently than disclosure. Inconsistency broadcasts that you are managing information — which is worse than transparency. The cost of a deception that collapses mid-contest is higher than the cost of not deploying it at all.

> **Important:** This skill applies to legitimate competitive contexts where information management is appropriate — commercial negotiation, competitive strategy, organizational positioning, market timing. It does not apply to fraud, manipulation of parties in positions of vulnerability, or deception that causes disproportionate harm to people who cannot protect themselves.

---

## Your Process

**Step 1: Information to protect**
What knowledge of your position or intentions, if known by the opponent, would disadvantage you? Be specific. Not "our strategy" (too vague) but "the fact that we have no alternative vendor and our current contract expires in 60 days." List each piece of protective information separately.

**Framing check:** Confirm the specific competitive situation before continuing. State the actor, the opponent, and the context in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of who is managing information against whom, and in what competitive context]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Advantageous false impressions**
What beliefs, if held by your opponent, would work in your favor? These must be plausible — impressions that could arise from your actual position, not fabrications that require active lying. Example: "that we have multiple alternatives in play" (if you could plausibly have them), not "that we have a signed term sheet" (if you don't).

**Step 3: Credible signals**
What actions or statements could plausibly create those impressions? The signal must be consistent with your real position or the deception collapses on contact. Actions are more credible than statements. What are you already doing that, if visible, creates the right impression? What could you do that is authentic and creates the desired signal?

**Step 4: Consistency check**
Is what you're concealing consistently concealed across every surface — every team member, every document, every signal? Identify the specific consistency risks. Who on your side might inadvertently breach the information barrier? What artifacts could expose it?

**Step 5: Counter-deception**
What might your opponent be concealing or signaling falsely? What are they trying to make you believe? Apply the same framework in reverse: what impressions are they managing, what would they want you to assume, and where do their signals feel too clean or too consistent to be the full picture?

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

### Deception Analysis

**Information to Protect**
[Specific knowledge that would disadvantage you if known — listed item by item]

**Advantageous False Impressions**
[Beliefs your opponent holding would benefit you — each must be plausible from your actual position]

**Credible Signals**
[Actions or statements that create those impressions — with consistency rationale for each]

**Consistency Check**
[Where the information barrier could fail — team risks, artifact risks, behavioral inconsistencies to watch]

**Counter-Deception Assessment**
[What your opponent may be concealing, what impressions they're managing, where their signals are too clean]

---

## Notes

Deception requires accurate intelligence to work — you cannot manage an opponent's beliefs without knowing what they currently believe. Pair with `/s4h-strategy-intelligence` before running this analysis. For the signals component, game-theory's signaling analysis provides a more formal framework for credible commitment signals when the context warrants it. Pair with `/s4h-strategy-positioning` to understand whether the position you're protecting is strong enough to be worth protecting — concealing a weak position buys time but does not change the underlying situation.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Deception strategy mapped. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-game-theory-signaling` — Design signals that enable or counter the deception
  - `/s4h-strategy-intelligence` — Gather intelligence to calibrate deception approach
  - `/s4h-strategy-positioning` — Position to benefit from the deception
  - **Done** — Wrap up and synthesise what we have so far

---
name: s4h-game-theory-signaling
description: "Analyses credibility problems and designs signals that are believable because they're costly to fake. Triggers: 'how do I signal credibly', 'signaling', 'they won't believe me', 'cheap talk', 'commitment device', 'how do I make a credible commitment', 'asymmetric information', 'how do I prove I'm serious', 'they don't trust my claim'."
---

# Game Theory: Signaling

Michael Spence's 1973 insight: education is not only valuable because it increases productivity — it is valuable as a *signal* because it is costly enough that low-ability workers won't bother acquiring it. If a credential is easy enough to fake, it conveys no information. The signal is credible only when it is cheaper for the type who actually has the quality being claimed.

The core principle: **cheap talk cannot be credible in adversarial or asymmetric-information contexts**. If saying "I'm trustworthy" costs nothing, then everyone — trustworthy or not — will say it, and the statement conveys nothing. The receiver knows this and discounts it. A credible signal must be costly in a way that is rational only if the claim is true. This is the separating condition: high types find the signal worth acquiring; low types don't.

George Akerlof's market for lemons (1970) shows the consequence when signaling fails: information asymmetry causes good products to be driven out by bad ones, because buyers can't distinguish them and price accordingly. Sellers of good products can't credibly signal their quality, so the market collapses toward low-quality goods and prices. Thomas Schelling extended this to commitment devices: any action that credibly binds you to a future course of action changes what others expect you to do — and thereby changes what they do now.

---

## Your Process

**Step 1: Information asymmetry**
Identify what one party knows that the other doesn't. Name the informed party and the uninformed party. What is the private information — quality, intent, ability, commitment, type? What would the uninformed party do if they had this information?

**Framing check:** Confirm the specific signaling situation before continuing. State the informed party, the uninformed party, and the private information being claimed in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the specific signaling situation — who is trying to credibly communicate what to whom]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Communication goal**
What does the informed party want to credibly communicate? State it precisely: not just "I'm good" but specifically what quality, commitment, or type is being claimed and why it matters to the receiver.

**Step 3: Cheap talk diagnosis**
Why isn't verbal communication credible here? Work through the receiver's reasoning: "If they said this regardless of whether it's true — which they'd be tempted to do — then my hearing it gives me no information." Identify the specific incentive to misrepresent that makes verbal claims unbelievable.

**Step 4: Costly signal design**
What action would be credible because it is only rational to take if the claim is true? Generate candidate signals first, then evaluate them.

**Before narrowing:** Show the complete set of candidate signals to the user first. Use `AskUserQuestion`:
- **Question:** "I've identified [N] candidate signals. Before I rank them by credibility and feasibility, are there any you'd flag as especially important, or any I've missed?"
- **Header:** "Prioritise"
- **Options:**
  - **Proceed with your selection** — the set looks right
  - **Flag one** — user will name a specific signal to include
  - **Add a missing one** — user will describe it

Evaluate candidate signals on three criteria:
- *Cost differential*: the signal must cost less for the type making the true claim than for a type trying to fake it (the single-crossing condition)
- *Observability*: the receiver must be able to verify the signal was taken
- *Magnitude*: the signal must be costly enough that low types wouldn't bother, but not so costly that high types wouldn't either

**Step 5: Commitment devices**
For claims about future behaviour (not just present type), identify commitment devices that bind the sender to the claimed course of action:
- *Burning bridges*: eliminating the ability to take the contrary action (accepting an exclusive contract, moving to a new city)
- *Public commitment*: making the claim in front of an audience that would observe a violation
- *Collateral*: putting something of value at risk contingent on the claimed behaviour
- *Third-party enforcement*: a binding agreement that creates external penalties for defection from the claim

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

### Signaling Analysis

**Information Asymmetry**
[Who has the private information? What is it? Who needs to be convinced of what?]

**Communication Goal**
[Precisely what the informed party needs to credibly establish in the receiver's mind]

**Cheap Talk Diagnosis**
[Why verbal claims alone are not credible — what incentive to misrepresent makes the receiver discount them]

**Credible Costly Signals**
[Candidate signals ranked by credibility — for each: what makes it costly to fake, whether the cost differential holds, and whether it's feasible in this context]

**Commitment Devices**
[Specific mechanisms that bind the sender to claimed future behaviour — ranked by strength and feasibility]

**Recommended Signaling Strategy**
[The specific combination of signal and/or commitment device most likely to achieve credibility given the context, the receiver's priors, and the costs involved]

---

## Notes

Signaling analysis has two sides. This skill focuses on the sender's problem: how to signal credibly. The receiver's problem — how to evaluate incoming signals, distinguish cheap talk from costly signals, and update beliefs correctly — is closely related. If you are the receiver trying to evaluate a claim, the same framework applies in reverse: ask what this signal would cost if the claim were false.

Signaling games have their own equilibrium structure. A *separating equilibrium* is one where different types choose different signals and can be distinguished — this is usually the desirable outcome. A *pooling equilibrium* is one where all types choose the same signal — no information is transmitted, and the signal is uninformative. Check which equilibrium your proposed signal actually produces.

Pairs with: `/s4h-game-theory-equilibrium` (the full equilibrium analysis of signaling games), `/s4h-strategy-deception` (the counter-perspective: managing what others believe about you and anticipating their signals), `/s4h-game-theory-mechanism-design` (when the goal is to design a system that elicits honest revelation rather than crafting a one-off signal).

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Signals analysed. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-game-theory-equilibrium` — Model how the signaling changes the equilibrium
  - `/s4h-communication-audience-modeling` — Model who reads each signal and how they interpret it
  - `/s4h-social-incentive-analysis` — Analyse what incentives shape how signals are read
  - **Done** — Wrap up and synthesise what we have so far

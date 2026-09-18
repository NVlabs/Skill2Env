---
name: s4h-game-theory-mechanism-design
description: "Designs rules and incentive systems that produce desired outcomes even when players are self-interested. Triggers: 'mechanism design', 'incentive design', 'design a system that makes people do X', 'reverse game theory', 'incentivize honest behavior', 'design rules', 'how do I get people to reveal their true preferences', 'how do I align incentives', 'the current system produces the wrong behavior'."
---

# Game Theory: Mechanism Design

Standard game theory takes the rules as given and asks what rational players will do. Mechanism design inverts this: it takes the *desired outcome* as given and asks what rules will produce it. This is why it is often called reverse game theory.

The central insight, formalised by Leonid Hurwicz and developed by Eric Maskin and Roger Myerson (who shared the 2007 Nobel Prize), is that private information is the root challenge. Players know things the designer doesn't — their true valuations, their effort levels, their costs — and they have incentives to misrepresent that information if doing so serves them. A well-designed mechanism elicits honest behaviour not by demanding honesty, but by making honesty the dominant strategy: the player's best move given the rules, regardless of what others do.

The revelation principle is the foundational theorem: any equilibrium of any mechanism can be replicated by a *direct incentive-compatible mechanism* — one where each player simply reports their private information truthfully and the rules process it correctly. This means the designer never needs to think about indirect or complicated mechanisms; there is always an honest, direct mechanism that achieves the same outcome.

William Vickrey's second-price auction is the canonical example: by having the winner pay the second-highest bid rather than their own, the dominant strategy becomes truthful bidding. The mechanism extracts honest valuations without demanding or relying on honesty.

---

## Your Process

**Step 1: Desired outcome**
State precisely what behaviour or allocation the mechanism should produce. Vague goals produce vague mechanisms. "People should behave better" is not a desired outcome. "Employees should report their true performance levels" is. "Suppliers should bid their true costs" is. Be specific about whose behaviour, what information, and what allocation.

**Framing check:** Confirm the desired outcome and the players involved before continuing. State what you've identified — the specific behaviour or allocation being targeted, the players whose incentives need aligning, and the private information at stake — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the desired outcome, the players, and the core misalignment]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Player map**
For each player involved:
- What *private information* do they hold? (True valuation, effort level, ability, cost, intent)
- What are their *incentives*? What would they do if there were no mechanism and pure self-interest governed?
- What would they prefer to report or do under a naive mechanism?

**Step 3: Misalignment diagnosis**
Describe the current equilibrium or default behaviour — what players actually do without the mechanism, or what they do under the current flawed system. Why is this bad? Identify the specific gap between what players find individually rational and what would be collectively desirable.

**Step 4: Mechanism specification**
Design the rules and payoffs. Work through three components:

**a. Information revelation**: How do you incentivise players to truthfully reveal their private information? Apply the revelation principle: design payoffs so truth-telling is the dominant strategy. Ask: "If a player with private information X reports Y instead, do they gain or lose?" The mechanism should ensure they lose — or at minimum don't gain — from misreporting.

**b. Rules and allocation**: Given truthful reports, what decision rule produces the desired outcome? How are goods, tasks, payments, or recognition allocated?

**c. Transfers and penalties**: What monetary or non-monetary transfers ensure the mechanism is individually rational (players prefer participating to not) and incentive-compatible (players prefer truth-telling to lying)?

**Step 5: Manipulation check**
Test the mechanism against strategic players. Ask: "What would a player with extreme private information do?" Try the boundary cases: the player with the highest possible valuation, the lowest, the one who most wants to game the system. Can they improve their outcome by misreporting? If yes, identify the loophole and revise.

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

### Mechanism Design

**Desired Outcome**
[Precisely stated: whose behaviour, what information, what allocation]

**Player Map**
[For each player: private information they hold + current incentives + what they'd do without the mechanism]

**Misalignment Diagnosis**
[Current equilibrium / default behaviour and why it fails to produce the desired outcome]

**Mechanism Specification**
- *Information revelation rule*: [How truth-telling becomes dominant — what the payoff structure looks like]
- *Decision/allocation rule*: [How reported information is processed into outcomes]
- *Transfers and participation constraints*: [What ensures players prefer to participate and to be honest]

**Manipulation Check**
[Results of testing against boundary-case players — can they game the mechanism? Identified loopholes and revisions]

**Revised Mechanism** *(if manipulation found)*
[Updated rules addressing the identified vulnerability]

**Implementation Notes**
[Practical considerations: information requirements, enforcement, whether the mechanism is robust to partial participation]

---

## Notes

The revelation principle guarantees that for any goal achievable by any mechanism, there is a direct, honest mechanism that achieves it. But "achievable in principle" doesn't always mean "simple to implement." When the mechanism requires detailed information or complex transfer schedules, consider whether a simpler but slightly less optimal mechanism is more practical.

Mechanism design is the formal version of the incentive design problem that appears everywhere: performance reviews, procurement, platform rules, voting systems, club governance, and any setting where the designer wants players with private information to behave in a collectively beneficial way.

For analysis of the equilibrium your mechanism produces (confirming it actually works as intended), use `/s4h-game-theory-equilibrium`. For auction-specific mechanism design — the most studied instance of the field — use `/s4h-game-theory-auction`.

For the related problem of getting players to cooperate over time (rather than getting a static mechanism right), use `/s4h-game-theory-iterated`.

Pairs with: `/s4h-social-incentive-analysis` (the social and political dimensions of the same incentive problem), `/s4h-game-theory-equilibrium` (verifying the mechanism's equilibrium), `/s4h-game-theory-auction` (specialised mechanism design for competitive bidding).

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Mechanism designed. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-logic-check` — Validate the mechanism's internal logic
  - `/s4h-game-theory-equilibrium` — Model what equilibrium the mechanism produces
  - `/s4h-decision-premortem-analysis` — Stress-test the mechanism for failure modes
  - **Done** — Wrap up and synthesise what we have so far

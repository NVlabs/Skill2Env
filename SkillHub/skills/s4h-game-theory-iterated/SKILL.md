---
name: s4h-game-theory-iterated
description: "Analyses long-run repeated interactions — how cooperation forms, how trust is built, how defection spirals start, and which strategies sustain cooperation. Triggers: 'repeated game', 'iterated strategy', 'long-run relationship', 'reputation effects', 'how do I sustain cooperation', 'tit for tat', 'shadow of the future', 'will they defect', 'ongoing relationship after betrayal', 'how do we recover from this'."
---

# Game Theory: Iterated Games

Robert Axelrod's 1984 computer tournament is one of the most important results in social science. He invited game theorists to submit strategies for an iterated prisoners' dilemma — a repeated game where the same two players interact over and over. The simplest strategy submitted, Tit for Tat (cooperate on the first move, then do exactly what your opponent did on the previous move), won both rounds of the tournament, beating every more complex strategy.

Why Tit for Tat wins: it is *nice* (starts by cooperating, never the first to defect), *retaliatory* (immediately punishes defection — there is no free lunch), *forgiving* (returns to cooperation as soon as the opponent does — does not hold grudges), and *clear* (the strategy is transparent and easy for the opponent to understand). Opponents who try to exploit it get punished; opponents who cooperate get rewarded. It is the most robust known strategy for sustained cooperation without trust.

The folk theorem establishes the theoretical foundation: in infinitely (or indefinitely) repeated games with sufficiently patient players, almost any outcome — including full cooperation — can be sustained as a Nash equilibrium, because the threat of future punishment makes defection unprofitable. The key variable is the *discount factor* (how much players value future payoffs relative to present ones), and whether punishment is *credible* and *observable*.

---

## Your Process

**Step 1: Stage game**
Describe the single-period interaction — what are the two players' choices in any given round, and what are the payoffs? Map the four key payoffs: mutual cooperation (CC), mutual defection (DD), exploitation (one cooperates, one defects), and being exploited. This identifies whether repetition can help: if the stage game already has cooperation as a Nash equilibrium, repetition changes little. If cooperation is not a Nash equilibrium of the stage game, repetition may enable it.

**Framing check:** Confirm the repeated interaction before continuing. State what you've identified — the two parties involved, the recurring choice or tension, and the relationship context — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the specific repeated interaction, the parties, and what cooperation/defection looks like in this context]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Is cooperation a stage-game equilibrium?**
Check whether cooperation would be chosen in a one-shot interaction. If yes, the repeated game is not necessary to explain or enable it. If no (cooperation requires an ongoing relationship to be rational), proceed with the shadow-of-the-future analysis.

**Step 3: Discount factor assessment**
How much do the players value continued interaction? Assess:
- *Time horizon*: is the relationship expected to continue indefinitely, or does it have a known end-point? (Known-endpoint problem: rational players defect on the last period, which unravels backward)
- *Relationship value*: how important is continued cooperation to each player? How much would they lose if the relationship ended?
- *Uncertainty about continuation*: what is the probability each period that the interaction continues? Higher probability → higher effective discount factor → cooperation more sustainable
- *Impatience*: are either player under short-term pressure that discounts future benefits?

**Step 4: Folk theorem conditions**
Assess whether the conditions for sustained cooperation are met:
- Discount factor is sufficiently high (both players value future interactions enough)
- Defection is observable (players can detect when cooperation breaks down)
- Punishment is credible (the punishing party would actually carry it out — it must be in their interest to do so)

**Step 5: Strategy recommendation**
Based on the discount factor and relationship context, recommend the best strategy from the following:

**Before narrowing:** Show all candidate strategies to the user first. Use `AskUserQuestion`:
- **Question:** "I've identified the following strategies as applicable given the discount factor and relationship context: [list all candidate strategies by name]. Before I select the best fit, are there any you'd flag as especially important given constraints I may have missed, or any I've overlooked?"
- **Header:** "Prioritise"
- **Options:**
  - **Proceed with your selection** — the candidate set looks right
  - **Flag one** — user will name a specific strategy to prioritise
  - **Add a missing one** — user will describe a constraint or dynamic not yet captured

- **Tit for Tat**: cooperate first, then mirror the opponent's last move. Best for stable, ongoing relationships where misunderstandings are rare.
- **Generous Tit for Tat**: like Tit for Tat but occasionally cooperates even after a defection (with low probability). Better when there is noise — accidental defections or miscommunications — that could trigger unnecessary retaliation spirals.
- **Grim Trigger**: cooperate until the opponent defects once, then defect forever. Maximum punishment credibility; best when the relationship is asymmetric and one defection is catastrophic. Risk: one mistake ends everything.
- **Win-Stay, Lose-Shift**: if last round's outcome was good (for you), repeat your choice; if it was bad, switch. Simpler to execute, surprisingly robust in noisy environments.
- **Unconditional cooperation**: only rational if you have strong external enforcement, the discount factor is extremely high, or you are trying to unilaterally rebuild a relationship.

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

### Iterated Game Analysis

**Stage Game**
[One-shot interaction: choices, payoffs at each combination — CC / DD / CD / DC]

**Cooperation in Stage Game**
[Is cooperation a Nash equilibrium of the one-shot game? Yes / No — and why this matters for the iterated analysis]

**Discount Factor Assessment**
[Time horizon, relationship value, continuation probability, and impatience — overall rating: high (cooperation sustainable) / moderate (cooperation fragile) / low (cooperation unlikely)]

**Folk Theorem Conditions**
- Discount factor sufficient: [Yes / No / Marginal]
- Defection observable: [Yes / No / Delayed — and by how much]
- Punishment credible: [Yes / No — and what makes it credible or not]

**Recommended Strategy**
[Specific strategy from the set above, with the reasoning for this context]

**Defection Spiral Warning Signs**
[Specific indicators that cooperation is breaking down — what to watch for and how to respond before full defection occurs]

**Recovery Path** *(if trust has already broken down)*
[How to re-establish cooperation after defection — the sequence of signals, concessions, and credible commitments required]

---

## Notes

The iterated analysis is the temporal complement to the one-shot prisoners' dilemma analysis. If you need to understand why the one-shot game produces defection in the first place, use `/s4h-game-theory-prisoners-dilemma`. The iterated skill focuses on how to sustain cooperation in ongoing relationships.

The shadow of the future is the mechanism, not the effect. Future cooperation is only valuable if players believe the relationship will continue. Actions that reduce confidence in continuation — signalling you might exit, visibly shortening your time horizon, threatening to end the relationship — also reduce the incentive for today's cooperation. Handle with care.

Pairs with: `/s4h-game-theory-prisoners-dilemma` (the one-shot structure this analysis builds on), `/s4h-game-theory-signaling` (in long-run relationships, reputation is a signal — how to maintain and repair it), `/s4h-strategy-timing` (when to cooperate, when to test, and when to act on defection).

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Iterated game analysed. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-game-theory-equilibrium` — Identify the equilibrium that emerges over iterations
  - `/s4h-social-incentive-analysis` — Map how incentives shift over repeated interactions
  - `/s4h-strategy-timing` — Determine when to cooperate and when to defect
  - **Done** — Wrap up and synthesise what we have so far

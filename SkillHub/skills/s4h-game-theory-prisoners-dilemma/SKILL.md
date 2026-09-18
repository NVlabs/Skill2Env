---
name: s4h-game-theory-prisoners-dilemma
description: "Analyses cooperation problems where individual rationality produces collective irrationality. Triggers: 'cooperation problem', 'prisoner's dilemma', 'everyone defects even though cooperation is better', 'race to the bottom', 'should I cooperate or defect', 'why won't anyone cooperate', 'collective action failure', 'why do we all end up worse off'."
---

# Game Theory: Prisoner's Dilemma

The prisoner's dilemma is the central problem of cooperation. Its structure: each player has an individual incentive to defect regardless of what the other does, so both defect — and both end up worse than if they had cooperated. Individual rationality produces collective irrationality.

This structure appears everywhere: countries competing on subsidies both nations would be better without, companies in a price war that erodes margins for everyone, colleagues who each underinvest in shared infrastructure, advertisers who would all benefit if no one ran ads but each is tempted to run them. Recognising the structure is the first move; it tells you why the situation is hard and what the real leverage points are.

Robert Axelrod's computer tournaments (1984) produced one of the most important empirical results in social science: in *repeated* prisoners' dilemmas, Tit for Tat — cooperate first, then mirror your opponent's previous move — consistently outperformed every more complex strategy. Its winning properties: *nice* (cooperates first), *retaliatory* (immediately punishes defection), *forgiving* (returns to cooperation as soon as the opponent does), and *clear* (easy to understand and predict). The lesson: cooperation is achievable without altruism, if the game is repeated and players are patient.

---

## Your Process

**Step 1: Structure verification**
Confirm the three conditions that define a prisoner's dilemma:
- (a) *Mutual cooperation dominates mutual defection*: if both cooperate, both do better than if both defect
- (b) *Defection is individually rational*: each player does better defecting regardless of what the other does (defection is a dominant strategy)
- (c) *The temptation to defect is real*: there is a genuine payoff advantage to defecting on a cooperating partner

If all three hold: this is a genuine prisoner's dilemma. If (a) fails, cooperation isn't actually better — the analysis changes. If (b) fails, there's no defection temptation — cooperation is already individually rational.

**Framing check:** Confirm the specific cooperation problem before continuing. State the players involved, what constitutes cooperation vs. defection for each, and why individual incentives diverge from collective interest in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the specific situation — who the players are, what cooperation and defection look like, and the collective action tension]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: One-shot vs. repeated**
Is this a single interaction or an ongoing relationship? This is the most important structural question. In a one-shot game, defection is the rational dominant strategy and there is no mechanism for cooperation. In a repeated game, the future creates incentives for today's cooperation.

**Step 3: Shadow of the future**
In repeated games, assess how much each player values future interactions. The discount factor (δ) captures how much tomorrow's payoff is worth today — high δ means future interactions matter a great deal; low δ means players are impatient or uncertain the relationship will continue. Cooperation is sustainable in repeated play if δ is above a threshold that depends on the payoff structure. Practically: ask how much each player needs the relationship to continue, how visible their defection will be, and how quickly punishment can be applied.

**Step 4: Trigger conditions**
In a cooperative equilibrium, cooperation is sustained by the threat of punishment. What action would constitute defection? How quickly would it be detected? How severe is the punishment, and is it credible? A cooperation equilibrium is only stable if the punishment threat is believable and proportionate.

**Step 5: Structural prescriptions**
If cooperation is failing or fragile, what changes to the structure could make cooperation individually rational?
- *Repeat the game*: turn a one-shot interaction into an ongoing relationship
- *Increase transparency*: make defection immediately visible so punishment can follow quickly
- *Change the payoffs*: increase the value of mutual cooperation or add penalties for defection (bonds, enforcement, regulation)
- *Reduce the temptation*: lower the short-run gain from defection
- *Build shared identity*: reframe the game so defection feels like a cost to a shared project, not just a strategic choice
- *Third-party enforcement*: external authority makes commitments binding

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

### Prisoner's Dilemma Analysis

**Structure Verification**
- Mutual cooperation better than mutual defection: [Yes / No / Partial]
- Defection individually rational (dominant strategy): [Yes / No]
- Genuine temptation to defect: [Yes / No]
- Verdict: [Confirmed prisoner's dilemma / Modified structure / Not a PD — see alternative framing]

**Payoff Map**
[The four key outcomes: mutual cooperation / you cooperate, they defect / you defect, they cooperate / mutual defection — with approximate payoffs or ordinal rankings]

**One-Shot vs. Repeated Assessment**
[Is this a single interaction or an ongoing relationship? How many rounds are expected? Does either player expect to exit soon?]

**Shadow of the Future Analysis**
[How much do players value continued interaction? What is the discount factor — high (cooperation sustainable) or low (cooperation fragile)? What would cause either player to reduce their valuation of the relationship?]

**Trigger Conditions**
[What constitutes defection? How quickly detected? Is punishment credible and proportionate?]

**Structural Prescriptions**
[Specific recommendations for changing the game structure to make cooperation individually rational — ranked by feasibility and impact]

---

## Notes

The prisoner's dilemma is the one-shot cooperation problem. For formal analysis of how cooperation can be sustained in repeated interactions, including specific strategy recommendations, use `/s4h-game-theory-iterated`.

If the structure is right but the rules are wrong — you want to change the game itself — use `/s4h-game-theory-mechanism-design`, which designs payoffs and rules specifically to align individual and collective incentives.

For analysis of the stable outcome of the one-shot version (and confirmation that defection is indeed the Nash equilibrium), use `/s4h-game-theory-equilibrium`.

Pairs with: `/s4h-social-incentive-analysis` (the social and power dynamics around the same incentive problem), `/s4h-strategy-alliance` (the strategic logic of forming cooperative relationships).

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Dilemma analysed. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-game-theory-mechanism-design` — Design away from mutual defection
  - `/s4h-social-incentive-analysis` — Align incentives to encourage cooperation
  - `/s4h-game-theory-iterated` — Test whether cooperation emerges with repeated interaction
  - **Done** — Wrap up and synthesise what we have so far

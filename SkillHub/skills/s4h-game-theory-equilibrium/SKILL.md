---
name: s4h-game-theory-equilibrium
description: "Finds the stable outcome of a strategic interaction — the point where no player can improve their result by changing their strategy alone. Triggers: 'Nash equilibrium', 'dominant strategy', 'what's the stable outcome', 'equilibrium analysis', 'payoff matrix', 'what will rational players do', 'where will this land'."
---

# Game Theory: Equilibrium Analysis

John Nash's central insight: in any finite game, there exists at least one outcome — the Nash equilibrium — where no player can improve their payoff by unilaterally switching strategy, assuming all other players hold theirs. This is the point of stability; it's where rational play converges.

The power of equilibrium analysis is not that it finds the best outcome. It finds the *actual* outcome — where unconstrained, rational, self-interested players end up. Many Nash equilibria are collectively inefficient: the classic prisoners' dilemma equilibrium is both stable and bad for everyone. Knowing where the game ends up is the prerequisite for deciding whether to play, to change the rules, or to engineer a better outcome.

Thomas Schelling added a critical extension: when multiple equilibria exist, players coordinate on *focal points* — outcomes that feel natural or salient without explicit communication. The focal point is often obvious in context (the prominent location, the round number, the culturally expected choice) and determines which of several possible equilibria is reached.

---

## Your Process

**Step 1: Map the players and strategies**
Identify every player in the interaction. For each player, list their available strategies — the distinct actions they can choose. Keep the strategy set realistic: exhaustive but not so granular it becomes unmanageable.

**Framing check:** Confirm the specific game before continuing. State what you've identified — the players, their available strategies, and the core tension — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the specific game — who the players are, what strategies are available, and what each is trying to achieve]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Build the payoff matrix**
Construct a matrix showing each player's payoff for every combination of strategies. Fill in all cells. If payoffs are uncertain, use expected values. If precise payoffs aren't available, use ordinal rankings (best, good, neutral, bad, worst) — the analysis still holds.

**Step 3: Find dominant strategies**
A dominant strategy is one that is better for a player regardless of what others do. Check each player: is there a strategy that beats or ties all alternatives across every possible opponent choice? If a dominant strategy exists, rational players will always choose it — it simplifies the analysis substantially. Iterated elimination of dominated strategies can further reduce the game.

**Step 4: Identify Nash equilibria**
For each cell in the matrix, ask: given what the other player(s) are doing, would this player want to switch? If no player wants to switch — the combination is a Nash equilibrium. Mark all such outcomes. (A game may have one, several, or in mixed-strategy form, infinitely many equilibria.)

**Step 5: Efficiency assessment**
Evaluate the equilibrium outcome(s): is this collectively good, or is there a better outcome that rational play fails to reach? An outcome is *Pareto-inefficient* if there exists an alternative where everyone would be at least as well off and at least one player would be strictly better off. Name exactly why the efficient outcome is unreachable without external intervention.

**Step 6: Multiple equilibria and coordination**
If more than one Nash equilibrium exists, analyse: what determines which one is reached? Consider focal points (salience, cultural convention, historical precedent), communication (can players talk before choosing?), and coordination mechanisms (common knowledge, public commitments, third-party arbitration).

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

### Equilibrium Analysis

**Players and Strategies**
[Each player and their available strategies]

**Payoff Matrix**
[Full matrix — all cells filled, with payoffs for each player at each strategy combination]

**Dominant Strategies**
[Which players have dominant strategies, and what they are — or "none" if absent]

**Nash Equilibria**
[All equilibria identified, with the strategy combination and payoffs at each]

**Efficiency Assessment**
[Efficient or Pareto-inefficient? If inefficient: which outcome would be better for all, and why rational play doesn't reach it]

**Coordination Mechanism** *(if multiple equilibria)*
[What determines which equilibrium is reached — focal points, communication, history]

**Strategic Implication**
[What this analysis means for the player asking — what to expect, what to watch, what leverage exists]

---

## Notes

The Nash equilibrium describes where rational play leads — it does not prescribe what to do. If the equilibrium is bad (as in the prisoners' dilemma), the question becomes how to change the game. See `/s4h-game-theory-mechanism-design` for how to redesign rules so the equilibrium is efficient.

The most common equilibrium failure is the prisoners' dilemma structure: dominant strategies lead both players to an outcome worse than the alternative. See `/s4h-game-theory-prisoners-dilemma` for dedicated analysis of cooperation failures.

When players interact repeatedly, the equilibrium changes: future consequences make cooperation rational even when it isn't in the one-shot game. See `/s4h-game-theory-iterated` for repeated game analysis.

Pairs with: `/s4h-strategy-positioning` (acting effectively given the equilibrium you've identified), `/s4h-game-theory-mechanism-design` (changing the game so the equilibrium is efficient), `/s4h-decision-criteria-weighting` (when the strategic dimension is secondary and this is primarily a personal choice).

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Equilibrium found. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-game-theory-signaling` — Identify what signals could shift the equilibrium
  - `/s4h-game-theory-mechanism-design` — Design rules or incentives to produce a better equilibrium
  - `/s4h-strategy-positioning` — Position to exploit the current equilibrium
  - **Done** — Wrap up and synthesise what we have so far

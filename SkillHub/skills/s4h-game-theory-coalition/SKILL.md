---
name: s4h-game-theory-coalition
description: "Analyses which coalitions form and how to divide gains fairly using cooperative game theory and the Shapley value. Triggers: 'coalition formation', 'who should we partner with', 'cooperative game theory', 'Shapley value', 'fair division', 'stable coalition', 'which coalition will form', 'equity split', 'power in a coalition', 'how should we divide this up fairly'."
---

# Game Theory: Coalition Analysis

Cooperative game theory asks a different question from strategic (non-cooperative) game theory. Rather than asking what rational self-interested players will do when they can't coordinate, it asks: when players *can* form binding agreements and share gains, which coalitions will form, and how should the value be divided?

Lloyd Shapley's answer to the division question — the Shapley value (1953, Nobel Prize 2012) — is remarkable for its mathematical precision and moral intuition. Each player's fair share is their average marginal contribution across all possible orderings of coalition formation. Formally: for each permutation of all players, calculate how much value player *i* adds when they join the coalition that has formed before them. Average this marginal contribution across all permutations. The result is the Shapley value — the uniquely fair allocation given four axioms: efficiency (the grand coalition's total value is fully distributed), symmetry (identical players receive equal shares), dummy (players who contribute nothing receive nothing), and additivity (allocations across independent games add correctly).

The core captures coalition stability: an allocation is in the core if no subset of players can collectively do better by breaking away and forming their own coalition. If an allocation is in the core, no group has an incentive to defect — the grand coalition is stable. If the core is empty, no allocation is fully stable and some defection pressure is unavoidable.

These two concepts are complementary but distinct. The Shapley value is always unique and always exists — it answers "what is fair?" The core may be empty — it answers "what is stable?"

---

## Your Process

**Step 1: Player-value map**
List all players and, for each possible coalition (every subset), specify the value that coalition can generate on its own. This is the characteristic function of the game — v(S) for every subset S. For small groups (3–4 players), enumerate all subsets. For larger groups, focus on the most relevant coalitions: the grand coalition, each individual player alone, and the likely competing sub-coalitions.

**Framing check:** Confirm the specific coalition situation before continuing. State what you've identified — the players, what value they can jointly create, and the core question (who should form a coalition and how should gains be divided) — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the players, their potential joint value, and the key coalition question]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Grand coalition assessment**
Is the grand coalition (all players together) the most efficient arrangement? Check whether v(everyone) ≥ v(any subgroup) + v(remaining players). If yes, the grand coalition maximises total value and the question is only how to divide it. If no, some smaller coalition creates more value, and the question is which one forms.

**Step 3: Shapley value calculation**
For each player, calculate their average marginal contribution:
- List all permutations of player ordering (for n players, there are n! permutations — for 3 players: 6; for 4 players: 24)
- For each permutation, identify what coalition exists just before player i is added, and calculate v(coalition + i) − v(coalition)
- Average this marginal contribution across all permutations
- The result is player i's Shapley value

For practical purposes with more than 4 players, compute the Shapley value for the players of primary interest using a representative subset of permutations, or use the formula: φᵢ(v) = Σ [|S|!(n−|S|−1)!/n!] × [v(S∪{i}) − v(S)] summed over all subsets S not containing i.

**Step 4: Core analysis**
An allocation x = (x₁, x₂, ..., xₙ) is in the core if:
- It is efficient: Σxᵢ = v(all players)
- No coalition can do better: for every subset S, Σᵢ∈S xᵢ ≥ v(S)

Check whether the proposed allocation satisfies the blocking constraint for every relevant coalition. If no such allocation exists, the core is empty — identify which coalitions have the most credible defection threat.

**Step 5: Stability analysis**
Even with a core allocation, identify threats:
- Which players are most tempted to defect to a subcoalition?
- What external conditions (new opportunities, changing valuations, information revelations) could shift the characteristic function?
- What governance or enforcement mechanisms could reinforce stability?

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

### Coalition Analysis

**Player-Value Map**
[All relevant coalitions and the value each generates — v(S) for each subset S]

**Grand Coalition Assessment**
[Is the grand coalition efficient? Is total value maximised by full cooperation? Y/N and why]

**Shapley Values**
[Each player's Shapley value — their average marginal contribution and what this means for the fair allocation]

**Core**
[The set of stable allocations — or "core is empty" with identification of the most credible defection threat]

**Stability Threats**
[Which subcoalitions pose the greatest defection risk, under what conditions, and what would trigger instability]

**Recommended Structure and Allocation**
[The specific coalition and allocation that balances fairness (Shapley) with stability (core), with practical implementation notes]

---

## Notes

The Shapley value answers "what is fair" — it does not predict what will happen. What actually happens depends on bargaining power, outside options, timing, and negotiating skill. The Shapley value is most useful as a reference point: a principled allocation that no player can argue violates fairness criteria.

When the core is empty, no fully stable allocation exists. In practice this means: allocations will always face some coalition's objection. The goal shifts to finding the allocation with the *smallest* objection — the one that minimises the maximum advantage any blocking coalition could gain.

For the rules governing how a coalition is formed and how players reveal their contributions — the design of the process rather than the analysis of the outcome — use `/s4h-game-theory-mechanism-design`.

For analysis of the strategic (non-cooperative) interactions happening inside the coalition — after it forms — use `/s4h-game-theory-equilibrium` or `/s4h-game-theory-iterated`.

Pairs with: `/s4h-strategy-alliance` (strategic and contextual dimension of partnership decisions), `/s4h-social-coalition-mapping` (the social and power dynamics of alliance building), `/s4h-game-theory-mechanism-design` (designing the process for fair coalition formation).

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Coalition dynamics analysed. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-social-coalition-mapping` — Map social dynamics within the coalition in practice
  - `/s4h-game-theory-mechanism-design` — Design rules to stabilise the coalition
  - `/s4h-strategy-alliance` — Turn coalition analysis into concrete alliance strategy
  - **Done** — Wrap up and synthesise what we have so far

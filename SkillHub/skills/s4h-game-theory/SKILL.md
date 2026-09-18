---
name: s4h-game-theory
description: "Routes to the right game-theory skill for your strategic situation. Triggers: 'game theory', 'strategic interaction', 'what will they do', 'payoff analysis', 'how do I think about this strategically', 'incentive design', 'cooperation problem', 'bidding strategy', any situation where the best choice depends on what others choose."
---

# Game Theory

Your best move depends on what they'll do — and their best move depends on what you'll do. This interdependence is the defining feature of strategic interaction. Game theory provides formal tools for reasoning through it: mapping payoffs, finding stable outcomes, designing incentives, and analysing how cooperation forms and breaks down.

---

## Your Process

**Step 1: Diagnose the interaction type**

Read the situation and identify which of the following patterns applies.

**Framing check:** Confirm the specific strategic situation before continuing. State what you've identified — the actual interaction, who the players are, and what decision is at stake — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the strategic situation and the players involved]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

- **One-shot strategic choice** — players make a single decision simultaneously or sequentially, and payoffs depend on the combination of choices. You need to identify the stable outcome (equilibrium) and whether it's efficient.
  → Use `/s4h-game-theory-equilibrium`

- **Cooperation vs. defection** — each player is individually tempted to defect even though mutual cooperation would be better for everyone. You're facing a race to the bottom, collective action failure, or asking whether to cooperate or hold back.
  → Use `/s4h-game-theory-prisoners-dilemma`

- **Credibility problem** — you have private information and need others to believe your claim, or you're being told something and aren't sure whether to believe it. Cheap talk, costly signalling, commitment devices.
  → Use `/s4h-game-theory-signaling`

- **Rule design** — you're not playing the game, you're designing it. You want to create rules, incentives, or mechanisms that make players behave in a desired way — especially to elicit honest information or align self-interest with collective benefit.
  → Use `/s4h-game-theory-mechanism-design`

- **Long-run repeated relationship** — the same two or more parties will interact repeatedly over time. Reputation, trust, retaliation, and the shadow of the future are all active.
  → Use `/s4h-game-theory-iterated`

- **Coalition and fair division** — multiple players could form alliances and share gains. Which coalition will form? How should value be divided fairly? Who holds power?
  → Use `/s4h-game-theory-coalition`

- **Competitive bidding** — a structured auction or procurement process where you're either bidding or designing the process. How much to bid? How to avoid the winner's curse? How to design a revenue-maximising or efficient auction?
  → Use `/s4h-game-theory-auction`

**Step 2: Confirm and route**

Present the diagnosis clearly — what kind of interaction this is and which skill fits — then use `AskUserQuestion`:
- **Question:** "My read: this is a [interaction type] situation — [one sentence explaining why, e.g. which payoff structure or strategic feature makes it so]. Run `/[sub-skill]`?"
- **Header:** "Direction"
- **Options:**
  - **Yes — run `/[sub-skill]`** — diagnosis is correct
  - **Show all options** — list the available sub-skills with one-line descriptions
  - **Different angle** — describe which aspect of the situation is most pressing

If the situation spans multiple types (e.g., a cooperation problem inside a long-run relationship), note both in the question and ask which dimension is most pressing before routing.

---

## Important distinction

Game theory provides formal payoff structure: it tells you what a rational player will do given the rules, payoffs, and other players. Strategy (see `/s4h-strategy`) provides contextual wisdom: how to position, when to act, how to use terrain and timing. They are complementary — use game theory to understand the structure of the interaction, and strategy to act effectively within it. When both apply, use game theory first to clarify what the incentives actually are, then strategy to decide how to play.

---

## Notes

The category skills are: `/s4h-game-theory-equilibrium`, `/s4h-game-theory-prisoners-dilemma`, `/s4h-game-theory-signaling`, `/s4h-game-theory-mechanism-design`, `/s4h-game-theory-iterated`, `/s4h-game-theory-coalition`, `/s4h-game-theory-auction`.

Related categories: `/s4h-strategy` (contextual wisdom for acting within games), `/s4h-decision` (single-player choice without strategic interaction), `/s4h-social` (power dynamics and coalition politics).

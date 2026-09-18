---
name: s4h-strategy
description: "Routes to the right strategy skill for any adversarial or competitive reasoning situation. Triggers: 'how do I beat X', 'competitive strategy', 'outmaneuver', 'I'm up against', 'position myself', 'what's my play here', any situation involving competitive pressure, adversarial dynamics, negotiation, or resource-constrained contest."
---

# Strategy

Sun Tzu's central insight: "The victorious warrior wins first and then goes to war, while the defeated warrior goes to war first and then seeks to win." Strategy is what happens before the contest. It is the discipline of creating conditions — position, intelligence, timing, alliances — so that when the contest begins, the outcome is already determined.

The strategy skills in this category draw on Sun Tzu (*The Art of War*), Clausewitz (*On War*), Miyamoto Musashi (*Book of Five Rings*), and competitive theory. They are not about aggression. They are about reading competitive contexts clearly and acting with economy, intelligence, and timing.

---

## Your Process

Read the user's situation carefully. Identify which strategic challenge is primary, then present the options below — briefly and specifically — and ask which fits. Execute immediately on selection.

**Framing check:** Confirm the competitive situation before continuing. State what you've identified — the actor, the opponent or competitive pressure, and the primary objective at stake — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the actor, the adversarial dynamic, and the goal]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Reading the landscape — where should I compete, and where should I avoid?**
→ `/s4h-strategy-terrain` — Maps available positions, identifies favorable and dangerous ground, tells you which battles are worth fighting.

**What do I actually know, and what am I assuming?**
→ `/s4h-strategy-intelligence` — Audits what you know vs. what you're assuming about yourself and your opponent. Closes the intelligence gaps that cause strategic failures.

**When should I act — now, or wait?**
→ `/s4h-strategy-timing` — Analyzes conditions favoring action vs. patience. Reads your opponent's rhythm. Identifies trigger conditions for the right moment.

**How do I do more with less — I'm outgunned?**
→ `/s4h-strategy-force-economy` — Finds the minimum intervention that achieves the objective. Identifies leverage points where a small input creates a large output.

**How do I create a position that's hard to attack?**
→ `/s4h-strategy-positioning` — Builds the conditions for unassailability before the contest. What must be true for a rational opponent to choose a different arena?

**What should I reveal vs. conceal — information asymmetry?**
→ `/s4h-strategy-deception` — Manages information asymmetry in legitimate competitive contexts. Protects your position; identifies what your opponent may be concealing from you.

**What does winning actually mean here?**
→ `/s4h-strategy-victory` — Defines victory before the contest begins. Prevents the pyrrhic trap: winning in ways that lose the larger goal.

**Who do I need on my side — coalition and alliance?**
→ `/s4h-strategy-alliance` — Maps parties, identifies natural allies and swing parties, assesses alliance stability. Alliances built on shared interest vs. goodwill alone.

---

## Routing Confirmation

After diagnosing, use `AskUserQuestion` before routing:
- **Question:** "My read: this is a [type] situation — [one sentence why]. Run `/[sub-skill]`?"
- **Header:** "Direction"
- **Options:**
  - **Yes — run `/[sub-skill]`** — diagnosis is correct
  - **Show all options** — list all eight sub-skills with one-line descriptions
  - **Different angle** — describe which aspect of the competitive situation is most pressing

Adapt [type], [why], and [sub-skill] based on the primary strategic challenge identified.

---

## Output Format

Present the 3–4 most relevant options for the user's specific situation (not all eight every time). For each option, one sentence on why it fits. Ask which they want. Execute immediately on selection without further preamble.

---

## Notes

If the objective itself is unclear, start with `/s4h-strategy-victory` — you cannot select terrain, timing, or force economy without knowing what winning means. If the situation is genuinely complex, terrain is usually the right first move: it establishes the ground on which all other choices operate.

Strategy skills are for competitive and adversarial contexts. For purely cooperative situations where parties share objectives, the decision and systems categories are more appropriate.

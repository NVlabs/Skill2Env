---
name: s4h-strategy-terrain
description: "Maps the competitive landscape to identify where you have advantage, where contests are evenly matched, and where engagement is costly. Triggers: 'map the landscape', 'terrain analysis', 'where should I compete', 'what's the ground like', 'competitive landscape', 'where do I have advantage', 'which markets should I enter', 'is this fight worth having'."
---

# Strategy: Terrain

Sun Tzu identifies six types of terrain and nine strategic situations in *The Art of War*, each demanding different conduct. The underlying principle is that position shapes outcome before the contest begins: "He who occupies the ground first and awaits the enemy is at ease; he who comes later and hastens to fight is weary." The key strategic question is not "how do I win this battle?" but "which battles should be fought at all?" Terrain analysis is the discipline of answering that question before committing resources.

Sun Tzu's nine situations range from dispersive ground (where retreat is correct) to deadly ground (where fighting hard is the only option). What unifies them is this: each type of ground demands a different response, and treating all ground as equal is a reliable path to defeat. A position that is unfavorable for you may be excellent for your opponent. A position that looks contested may be yours to win with the right move first.

---

## Your Process

**Step 1: Landscape inventory**
What are the available positions in this competitive context? Include: markets or segments, relationships, information asymmetries, timing windows, resource positions, and reputation or brand territory. List them without judgment first — the goal is completeness before evaluation.

**Framing check:** Confirm the competitive context before continuing. State the specific situation being analyzed — who the actor is, what arena they are operating in, and what strategic question is at stake — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the specific competitive context and strategic question]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Favorable ground**
Where do your strengths meet their weaknesses? Where do you have natural advantage — by virtue of existing position, capabilities, relationships, speed, or knowledge? Sun Tzu: "In battle, use the orthodox method; win through the unorthodox." Favorable ground is where your orthodoxy is their weakness.

**Step 3: Contested ground**
Where are you and competitors evenly matched? What would it take to tip contested ground in your favor — first-mover advantage, a decisive capability gap, a key alliance? Note the cost of tipping each contested position vs. the value of holding it.

**Step 4: Dangerous ground**
Where do you have no natural advantage and engagement drains you? Sun Tzu's "dispersive ground" — where your forces scatter and confidence wavers. Name each dangerous position explicitly. The strategic discipline is the willingness to name ground as dangerous and refuse to fight there.

**Step 5: High-ground assessment**
Who currently holds the most advantageous position in this landscape? What makes their position strong — network effects, information advantage, first-mover lock-in, relationships? What would it take for you to hold that position instead? Is acquiring it worth the cost?

**Step 6: Terrain verdict**
**Before narrowing:** Show the full set of positions identified across Steps 1–5 to the user before issuing a verdict. Use `AskUserQuestion`:
- **Question:** "I've mapped [N] positions across favorable, contested, dangerous, and high ground. Before I issue a terrain verdict, are there any positions you'd flag as especially critical, or any I've missed?"
- **Header:** "Prioritise"
- **Options:**
  - **Proceed with your verdict** — the landscape looks complete
  - **Flag one** — user will name a specific position to weigh more heavily
  - **Add a missing one** — user will describe a position not yet in the map

Based on the above: which positions are worth fighting for, which require waiting and preparation, and which should be avoided? A clear verdict — not a hedge.

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

### Terrain Analysis

**Landscape Inventory**
[Full list of available positions in this competitive context]

**Favorable Ground**
[Positions where your strengths meet opponent weaknesses — your natural advantages]

**Contested Ground**
[Evenly matched positions — with assessment of what tipping each requires and whether it's worth it]

**Dangerous Ground**
[Positions to avoid — explicit, without softening. Why each is dangerous for you specifically]

**High-Ground Holder**
[Who holds the strongest current position, why, and what taking it would require]

**Terrain Verdict**
[Clear prioritization: fight here, prepare here, avoid here — with rationale]

---

## Notes

Run terrain analysis before any other strategy skill — it establishes the competitive context that all other choices operate within. An accurate terrain map requires honest intelligence; pair with `/s4h-strategy-intelligence` when your knowledge of the landscape is uncertain or you suspect your assumptions about competitor positions are wrong.

For moving to favorable ground once identified, use `/s4h-strategy-positioning`. For understanding what opponents hold in contested positions, use `/s4h-strategy-intelligence`. For deciding whether the overall objective is worth the terrain cost, use `/s4h-strategy-victory` first.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Terrain mapped. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-strategy-positioning` — Position on the most favourable terrain
  - `/s4h-strategy-timing` — Time moves to terrain conditions
  - `/s4h-strategy-force-economy` — Deploy force economically given the terrain
  - **Done** — Wrap up and synthesise what we have so far

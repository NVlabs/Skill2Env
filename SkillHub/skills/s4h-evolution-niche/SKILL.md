---
name: s4h-evolution-niche
description: "Applies competitive exclusion and niche theory to understand differentiation, coexistence, and competitive strategy. Triggers: 'what niche are we in', 'how do we differentiate', 'why can these two strategies coexist', 'competitive exclusion', 'who will win this market', 'niche overlap', 'are we too similar to our competitors', 'resource partitioning'."
---

# Evolution: Niche

Georgy Gause's competitive exclusion principle, derived from experiments with paramecia in 1934, established one of ecology's foundational rules: two species competing for the same limiting resource in exactly the same way cannot stably coexist. One will outcompete the other and drive it to extinction — or one must shift to a different resource, time, place, or method. The principle is both a constraint and an invitation: coexistence requires differentiation.

The concept of the ecological niche — formalised by G. Evelyn Hutchinson as an n-dimensional hypervolume in which a species can maintain a viable population — gives the principle practical teeth. Every dimension of the environment that a species uses or is affected by defines one axis of its niche. Species can coexist when their niches overlap little enough on at least one critical axis. The axes are the dimensions of differentiation: what resource is used, when, where, and how.

This tool applies niche theory to competitive strategy. It identifies the dimensions along which players in a system compete, maps the niche each occupies, measures overlap, and identifies where differentiation creates space for coexistence or where displacement is the likely outcome. Stuart Kauffman's work on adjacent possibles adds a further dimension: the unoccupied niches that exist at the edge of current competition, waiting to be colonised by sufficiently novel variants.

---

## Your Process

**Step 1: Define the Competitive Space**
Identify who is competing in this system. List all meaningful players — current competitors, potential entrants, substitute strategies. Then name the resources or outcomes they are competing for: what is the limiting factor that determines fitness? In ecology, this might be food, territory, nesting sites; in business, it might be customer attention, talent, regulatory capacity, margin, or a specific buyer segment.

**Framing check:** Confirm the competitive arena before continuing. State the players, the limiting resource, and the time frame in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [one sentence naming who is competing, for what limiting resource, and over what time frame]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Identify Niche Dimensions**
Map the axes on which players differ in how they use or access the contested resource. Common niche dimensions:
- **Resource type:** what specific variant of the resource do they use? (e.g., which customer segment, which protein source)
- **Temporal niche:** when do they use it? (time of day, season, phase in the product cycle)
- **Spatial/channel niche:** where do they operate? (geography, distribution channel, market tier)
- **Method/mechanism:** how do they extract value? (price-based vs. quality-based, specialisation vs. breadth)
- **Position in the food chain:** are they primary producers, middlemen, or apex players?

List all dimensions visible in this system. For each, estimate the range across which players are distributed.

**Step 3: Map Niche Overlap**
For each pair of major players: how much do their niches overlap on each dimension? Represent this as a table or matrix. High overlap on a critical resource dimension means competitive exclusion is likely; low overlap across all critical dimensions means coexistence is stable.

**Before assessing competitive intensity:** Use `AskUserQuestion` to check your overlap assessments:
- **Question:** "I've mapped niche overlap for the key players. Before I assess which overlaps are most dangerous: are there dimensions of differentiation I've missed, or overlaps I've overstated or understated?"
- **Header:** "Overlap Check"
- **Options:**
  - **Looks right — proceed** — the overlap map is accurate
  - **Adjust one** — user will name the misread dimension
  - **Missing dimension** — user will describe an axis I haven't included

**Step 4: Assess Competitive Exclusion Risk**
For each high-overlap pair: apply the exclusion principle. Is this overlap on a *limiting* resource — one where outcompeting means the competitor gains fitness at the other's direct expense? If yes, one will displace the other unless:
- The resource is not truly limiting (there is enough for both)
- One player shifts along a niche dimension before exclusion completes
- The environment fluctuates, preventing equilibrium from being reached
- Character displacement occurs: selection drives the competitors apart

Identify which pairs are at genuine exclusion risk and on what timeline.

**Step 5: Find Niche Opportunities**
Map the unoccupied regions of the competitive space — the "adjacent possibles" that no current player is exploiting. What niche dimensions are underserved? What combination of traits would allow a player to exploit a resource that current competitors are leaving on the table? Name the niche gaps and assess what it would take to occupy them.

**Step 6: Strategic Niche Positioning**
For the player asking the question: what is their current niche? How much does it overlap with the most dangerous competitors? What shift along which dimensions would reduce overlap, reduce exclusion risk, or open access to an underserved niche? Note whether the proposed shift requires a trade-off (you can't be everything everywhere without losing the advantages of specialisation).

---

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences — who is competing, what the overlap looks like, and what the key strategic question is — then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full analysis** — Complete all steps, reasoning shown throughout
  - **Key findings only** — Bottom-line output, skip step-by-step detail
  - **Specific focus** — Zoom in on one pair or one niche dimension
  - **Reframe** — The read is off; correct it and the analysis will follow the corrected framing

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

---

## Output Format

**Competitive Space**
[Players, the limiting resource, and time frame]

**Niche Dimensions**

| Dimension | Range | [Player A] | [Player B] | [Player C] |
|---|---|---|---|---|
| [axis] | [low → high] | [position] | [position] | [position] |

**Overlap Matrix**

| | [Player A] | [Player B] | [Player C] |
|---|---|---|---|
| [Player A] | — | [low / medium / high] | [low / medium / high] |
| [Player B] | [low / medium / high] | — | [low / medium / high] |

**Exclusion Risk Assessment**
[Which pairs face genuine competitive exclusion, on which resource dimension, and on what timeline]

**Character Displacement Observations**
[Whether any players are already being pushed apart — evidence of niche partitioning in action]

**Niche Gaps**
[Underserved regions of the competitive space — unoccupied niches worth considering]

**Strategic Positioning Recommendation**
[For the player asking: current niche, overlap risks, and the differentiation moves that would reduce exclusion risk or access new niche space]

---

## Notes

Niche theory is particularly powerful when applied to strategy because it reframes competition. The question is not "how do we beat competitor X?" but "are we occupying the same niche as competitor X, and if so, what does the exclusion principle predict?" If the answer is "yes, same niche, same limiting resource," the options are: differentiate, displace, or be displaced.

The most common error is treating all competition as niche overlap when in fact players are often competing for different resources in different ways and merely appear to overlap. Careful niche mapping often reveals more room for coexistence than first appears.

Pairs with `/s4h-evolution-arms-race` when two players in the same niche are in an escalatory coevolutionary relationship. Pairs with `/s4h-evolution-fitness-landscape` when you need to understand whether shifting niche dimensions means crossing a fitness valley. Pairs with `/s4h-strategy-positioning` for translating niche analysis into concrete competitive moves.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Niche landscape mapped. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-evolution-arms-race` — If two players in the same niche are locked in escalatory adaptation
  - `/s4h-evolution-fitness-landscape` — If shifting niche requires crossing a fitness valley
  - `/s4h-strategy-positioning` — Translate this niche map into competitive moves
  - **Done** — Wrap up and synthesise what we have so far

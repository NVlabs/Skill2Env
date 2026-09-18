---
name: s4h-social-incentive-analysis
description: "Maps the actual incentives driving behaviour — distinguishing stated motivations from the real incentive structures that shape what people do. Triggers: 'incentive analysis', 'why are they doing this', 'what are the actual incentives', 'follow the incentives', 'what does the system reward'."
---

# Incentive Analysis

Most behaviour that looks irrational is perfectly rational given the actual incentives. The problem is that systems are designed around intended incentives while people respond to actual ones. Finding the gap between the two explains what is happening and points to what would change it.

---

## Your Process

**Step 1: Describe the Behaviour**
Name the specific behaviour to explain or change. Be concrete — not "people aren't engaged" but "engineers don't attend architecture reviews and don't comment on RFCs."

**Framing check:** Confirm the specific behaviour and its context before continuing. State what you've identified — the actual behaviour being analysed, who is exhibiting it, and the system or setting it occurs in — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the specific behaviour, the actors involved, and the context]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Map What the System Actually Rewards**
Not what it is supposed to reward — what actually gets people promoted, praised, defended, or protected? Look at recent promotions, public praise, and what leadership visibly prioritises.

**Step 3: Map What the System Actually Punishes**
What leads to criticism, risk, political cost, or reduced standing? What do people avoid doing, even when they believe it is the right thing?

**Step 4: Rationality Check**
Given the actual rewards and punishments identified in Steps 2–3: is the observed behaviour rational? In most cases it is. If it is rational, that is important — it means you cannot change the behaviour without changing the incentives.

**Step 5: Identify the Incentive-Behaviour Gap**
Where do the intended incentives (what the system claims to reward) diverge from the actual incentives (what it truly rewards)? This gap is where dysfunction lives.

**Step 6: Recommend Incentive Changes**
For each problematic behaviour: what specific incentive change would most directly address it? Focus on what the system rewards and punishes, not on asking for attitude changes.

---

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences — what is being analyzed and what the core question is — then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full analysis** — Complete all steps, reasoning shown throughout
  - **Key findings only** — Bottom-line output, skip step-by-step detail
  - **Misaligned incentives only** — Where actual incentives diverge from stated goals
  - **Reframe** — The read is off; correct it and the analysis will follow the corrected framing

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

## Output Format

### Behaviour Under Analysis
[Concrete description]

### What the System Actually Rewards
- [Specific reward mechanisms — promotions, praise, visibility, safety]

### What the System Actually Punishes
- [Specific punishment mechanisms — criticism, risk, cost, exclusion]

### Rationality Check
**Is the behaviour rational given these incentives?** Yes / No / Partially.
**Explanation:** Why the behaviour makes sense (or doesn't) given the actual incentive structure.

### Incentive-Behaviour Gap
| Intended Incentive | Actual Incentive | Gap |
|-------------------|-----------------|-----|
| ... | ... | ... |

### Recommended Incentive Changes
| Problematic Behaviour | Incentive Change That Would Address It |
|----------------------|----------------------------------------|
| ... | ... |

---

## Notes

Incentive analysis is most powerful when it reveals that a problem is not one of attitude or effort but of structure. Change the structure — not the people.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Incentives analysed. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-social-coalition-mapping` — Align coalition building around the shared incentives
  - `/s4h-game-theory-mechanism-design` — Design mechanisms to shift incentive structures
  - `/s4h-communication-audience-modeling` — Model how incentives shape audience behaviour
  - **Done** — Wrap up and synthesise what we have so far

---
name: s4h-cognition-attention
description: "Maps the attention economy of a mind or situation — what captures it, what depletes it, and how to protect it. Use when asked 'why can't I focus', 'attention keeps getting pulled away', 'how do I protect deep work', 'what's stealing my focus', 'I keep getting distracted', or when designing environments, workflows, or communications that need to respect cognitive bandwidth."
---

# Cognition: Attention

Attention is the scarcest cognitive resource — and unlike memory or reasoning, it cannot be trained to be unlimited. It can only be allocated, protected, and defended. Most focus problems are not character failures; they are design failures. The environment, the workflow, or the communication system is structured in a way that systematically fragments attention and prevents sustained engagement with what matters most.

The attention economy framing, developed from William James's foundational work on voluntary and involuntary attention, treats focus as a resource subject to supply and demand. What demands attention is not random: salience (bright, loud, moving things), novelty (what's new or unexpected), emotional charge (threats, social signals, strong affect), and personal relevance all reliably override deliberate focus. Design your attention environment knowing what the competition is.

The key distinction: attention threats come in two forms. **Capture** — things that involuntarily seize focus through sensory or emotional hooks — and **depletion** — things that gradually drain the capacity for sustained focus even when no single interruption is dramatic. Both matter. Capture is visible and acute; depletion is slow, cumulative, and often invisible until cognitive capacity is exhausted.

---

## Your Process

**Step 1: Define the Attention Context**
Identify whose attention, in what context, for what purpose. Individual focus (a person trying to do deep work)? Group attention (a team, a meeting)? Communication attention (an audience you need to hold)? The diagnosis differs by context.

**Framing check:** Confirm the specific attention context before continuing. State what you've identified — whose attention, in what setting, and what the goal is — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of whose attention is at issue, in what context, and what you're trying to achieve]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Map Attention Demands**
List everything currently competing for attention in this context. Separate into:
- **Legitimate demands:** things that genuinely require attention and have claim to the time
- **Capture threats:** involuntary hijacks — notifications, interruptions, ambient noise, social signals
- **Depletion sources:** low-grade cognitive drains — ambient worry, unresolved decisions, low-priority tasks that create background anxiety, decision fatigue

**Step 3: Assess Current Allocation**
Where is attention actually going versus where it should go? Estimate the proportion of cognitive bandwidth consumed by each category. Identify the gap between actual and ideal allocation.

**Before narrowing:** Use `AskUserQuestion` to confirm the demand map before proceeding to solutions:
- **Question:** "I've mapped [N] attention demands across legitimate, capture, and depletion categories. Before I prioritise defences, are there any sources I've missed or any you'd flag as especially significant?"
- **Header:** "Demand Map"
- **Options:**
  - **Proceed** — the map looks complete
  - **Add a demand** — user will name a specific source to include
  - **Correct a category** — user will reclassify something

**Step 4: Diagnose the Core Problem**
What is the primary failure mode? Choose the dominant one:
- **Environment design failure:** physical or digital environment is structured to maximise interruption
- **Boundary failure:** legitimate demands have no protective scheduling; everything competes in real time
- **Depletion spiral:** low-level cognitive load is accumulating to the point where sustained attention becomes impossible
- **Capture vulnerability:** specific high-salience threats (notifications, social media, email) are bypassing deliberate intent

**Step 5: Design the Defence**
For each identified threat, prescribe a specific structural intervention. Defences fall into four types:
- **Elimination:** remove the demand entirely (unsubscribe, turn off, delete)
- **Batching:** process the demand in a designated window rather than on-demand (email twice daily, messages at noon)
- **Protection:** create structural conditions where capture threats cannot reach (phone in another room, notifications off, closed door)
- **Offloading:** capture open loops and unresolved items in a trusted external system to prevent background anxiety depletion (a task list, a decision log)

---

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences — what the core attention problem is and what the most significant threat is — then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full analysis** — Complete demand map, diagnosis, and full defence plan
  - **Key threats only** — Identify the top 3 attention threats and their defences
  - **Environment redesign** — Focus on structural changes to the physical or digital environment
  - **Reframe** — The read is off; correct it and the analysis will follow the corrected framing

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

## Output Format

**Attention Demand Map**

| Source | Type | Estimated % of bandwidth | Legitimacy |
|---|---|---|---|
| | | | |

**Core Problem:** [dominant failure mode + brief explanation]

**Defence Plan**

| Threat | Defence Type | Specific Action |
|---|---|---|
| | | |

**Priority Actions:** [Ranked top 3 interventions — the highest-impact changes to make first]

**Protected Time Structure:** [Specific recommendation for how to schedule and protect focused work given the demands identified]

---

## Notes

Attention management is not willpower management. Recommending that someone "just focus more" is the cognitive equivalent of recommending that someone "just be healthier." The leverage is in designing the environment and workflow, not in strengthening resolve against a hostile system. This skill should produce structural, actionable changes — not exhortations.

The nearest neighbor is `/s4h-cognition-cognitive-load` — which addresses working memory capacity within a focused session. Attention is the gateway problem (can you sustain engagement at all?); cognitive load is the capacity problem (can you hold the necessary complexity once you're engaged?). Both often need addressing together.

For the communication design case — holding an audience's attention — pair with `/s4h-communication-audience-modeling`.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Attention map complete. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-cognition-cognitive-load` — Address working memory limits within the focused sessions you've now protected
  - `/s4h-cognition-metacognition` — Assess whether you're monitoring and adjusting your thinking well within those focused sessions
  - `/s4h-mindset-flow` — Design for flow states using the protected attention environment as a foundation
  - **Done** — Wrap up and synthesise what we have so far

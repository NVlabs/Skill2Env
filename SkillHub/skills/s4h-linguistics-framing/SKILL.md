---
name: s4h-linguistics-framing
description: "Identifies how the frame around an issue shapes what options are visible and what conclusions feel natural. Use when you say 'how is this being framed', 'reframe this', 'I want to see this differently', 'the way we're talking about this feels wrong', 'what frame is being used here', or when a conversation keeps hitting the same wall."
---

# Linguistics: Framing

You cannot step outside a frame. But you can become aware of the one you are standing in — and then step into a different one.

George Lakoff's foundational insight was that frames are not neutral containers for facts. They are cognitive structures that activate associations, make certain conclusions feel obvious, and render others literally unthinkable. The word "tax relief" does not describe a tax reduction — it presupposes taxation is a burden requiring relief, which presupposes a reliever (government) and something to be relieved (the taxpayer). Accept the term and you have already accepted a world. The political right did not win the tax debate with better arguments; they won it with better frames.

Frames operate below the level of conscious reasoning. This is why factual correction often fails: presenting evidence against a frame frequently reinforces the frame by keeping its terms alive. The counter-move is not rebuttal but reframing — shifting the conceptual structure entirely, so the conclusions the original frame made "natural" no longer follow.

This skill surfaces the active frame in any situation, maps what it makes visible and invisible, and generates alternative frames that reveal different solution spaces.

---

## Your Process

**Step 1: Identify the Active Frame**
Read the description, document, or conversation carefully. Name the frame — what conceptual structure organizes this situation? Frames often reveal themselves through:
- The **metaphors** in use (is education a "product"? is healthcare a "market"?)
- The **subject position** (who is agent, who is acted-upon?)
- The **implicit problem definition** (what is being treated as the thing to solve?)
- The **vocabulary cluster** (which word choices presuppose the same set of assumptions?)

**Framing check:** Confirm the text and the framing situation before continuing. State what you've identified — the specific communication being analyzed and the frame you're examining — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of what you're analyzing and the active frame you've spotted]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Map the Frame's Implications**
For the active frame, map:
- **What it makes visible:** Which problems, options, and actors are foregrounded?
- **What it makes invisible:** Which problems, options, and actors are rendered peripheral or unspeakable?
- **What conclusions it makes natural:** Which outcomes seem obvious or inevitable given this frame?
- **What conclusions it makes difficult:** Which alternatives require overcoming the frame's gravitational pull?
- **Who benefits** from this frame being the operative one?

**Step 3: Identify the Frame's Hidden Commitments**
Every frame smuggles in assumptions. Surface them explicitly. What must be true for this frame to make sense? What prior commitments does accepting this frame require? These hidden commitments are often more consequential than anything the frame states explicitly.

**Before generating alternatives:** Show the frame mapping to the user. Use `AskUserQuestion`:
- **Question:** "I've mapped the active frame and its commitments. Before I generate alternatives: is there a particular direction you want the reframing to go — e.g., a specific audience, a strategic goal, or a value you want to center?"
- **Header:** "Reframing direction"
- **Options:**
  - **Generate a range** — produce alternatives across different dimensions
  - **Center a specific value** — user will name it; generate frames around that value
  - **Target a specific audience** — user will name them; generate frames that work for that audience
  - **Proceed as read** — no additional direction needed

**Step 4: Generate Alternative Frames**
Generate three to five alternative frames for the same situation. For each, name:
- The **core metaphor or structure** of the frame
- What **problem definition** it implies
- What **options** it makes visible that the original frame obscured
- What **vocabulary** the frame uses
- What the frame is **good for** and what it **cannot see**

Frame diversity matters: produce frames that differ structurally, not just in tone. A "burden" frame and a "cost" frame are the same frame. A "burden" frame and an "investment" frame are different frames. A "rights" frame and an "efficiency" frame are genuinely orthogonal.

**Step 5: Assess and Recommend**
Evaluate the alternative frames against the user's context and goals. Which frame:
- Best fits the audience's existing values and prior commitments?
- Creates the most useful solution space?
- Is most defensible and durable under challenge?
- Creates the least unintended closing of options?

Make a recommendation with reasoning.

---

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences, then ask:

- **Question:** "My read: [your 1–2 sentence interpretation of the framing situation and what you'll analyze]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full analysis** — Complete all steps, reasoning shown throughout
  - **Key findings only** — Bottom-line output: active frame and top reframe recommendation
  - **Specific focus** — Zoom in on one aspect: active frame, invisible options, or alternative frames only
  - **Reframe** — The read is off; correct it and the analysis will follow the corrected framing

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

## Output Format

**Active Frame**
Name of the frame, core metaphor or structure, and one-sentence description of what organizing logic it imposes.

**Frame Mapping**

| Dimension | Content |
|---|---|
| Makes visible | |
| Makes invisible | |
| Natural conclusions | |
| Difficult conclusions | |
| Who benefits | |

**Hidden Commitments**
The unstated assumptions the frame requires. Presented as a list of "this frame assumes that..." statements.

**Alternative Frames**

For each alternative:
- **Frame name:** [label]
- **Core structure:** [the metaphor or organizing logic]
- **Problem definition implied:** [what the frame treats as the thing to fix]
- **Options it opens:** [what becomes visible that was invisible]
- **Vocabulary:** [the word cluster this frame uses]
- **Limitation:** [what this frame cannot see]

**Recommendation**
The recommended frame, with reasoning: why it fits the audience, the situation, and the goal.

---

## Notes

Framing analysis is not spin-detection — it is not only about identifying manipulative frames. Every description, including ostensibly neutral ones, imposes a frame. The goal is to make the frame visible so the choice of frame becomes deliberate rather than inherited.

The nearest-neighbor trap: confusing framing with messaging. Messaging is the surface-level word choice; framing is the deeper cognitive structure. You can change every word and keep the same frame. Pair this skill with `/s4h-linguistics-connotation` when specific word choices are carrying problematic freight, and `/s4h-communication-audience-modeling` when you need to understand which frames will resonate with a particular audience.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Frame mapped. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-linguistics-connotation` — Audit the specific word choices within the new frame for hidden freight
  - `/s4h-communication-audience-modeling` — Test which of the alternative frames will land with your specific audience
  - `/s4h-narrative-frame-analysis` — Extend the framing analysis into full narrative structure
  - **Done** — Wrap up and synthesise what we have so far

---
name: s4h-narrative
description: "Entry point for the narrative toolkit. Routes to the right narrative skill based on your situation. Use when you say 'narrative', 'story', 'this feels flat', 'how do I structure this', 'the framing is wrong', 'who am I talking to', 'make this compelling', 'find the tension', or want narrative/storytelling help without knowing which specific tool fits."
---

# Narrative

Applies narrative and storytelling thinking to communication, strategy, and meaning-making. Diagnoses what kind of narrative work is needed and applies the right tool.

## Which tool fits

| You need to... | Tool |
|---|---|
| Map the audience's actual beliefs, goals, and fears | audience-modeling |
| Identify the current frame and generate better alternatives | frame-analysis |
| Apply story architecture to a proposal or presentation | structure-mapping |
| Find or create the tension that makes communication worth attending to | tension-mapping |

## Routing Decision

- **Don't know why the audience isn't responding** → audience-modeling
- **The framing of a situation is wrong or limiting** → frame-analysis
- **Have content but it's not landing — structure problem** → structure-mapping
- **Communication is flat, forgettable, or not engaging** → tension-mapping
- **Unclear** → structure-mapping; most communication problems are structural

## Confirm Direction

**Framing check:** Before confirming which tool to run, confirm your read of the narrative situation. State the specific content, communication, or story challenge being addressed in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the specific narrative situation — what content, for what purpose, for whom]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

After diagnosing which tool fits, use the `AskUserQuestion` tool to confirm direction. Construct the question dynamically to include your diagnosis:

- **Question:** "My read: **[diagnosed tool]** — [one sentence on why it fits]. How would you like to proceed?"
- **Header:** "Direction"
- **Options:**
  - **Yes, run that tool** — Execute the diagnosed skill immediately using the context already provided
  - **Show all options** — List every skill in this category with one-line descriptions
  - **Quick version** — Run a lighter-weight alternative if one exists for this situation
  - **Re-diagnose** — Revisit the situation description for a different read

Proceed based on their selection.

---

## Audience Modeling

*Maps the audience's current beliefs, real goals, fears, and threshold conditions.*

What do they already believe about this topic? What do they actually care about — not their job title, but their real goals? What are they afraid of — about the message, the change, the consequences? What would they need to see or hear to act? Build this model before structuring the communication; the best-structured message in the wrong frame for the wrong audience still fails.

**Output:** Audience belief map, real goals, fears, and the minimum conditions for a positive response.

---

## Frame Analysis

*Identifies the current frame and generates alternative frames.*

Every situation is perceived through a frame — a set of implicit assumptions about what kind of thing this is, who the relevant parties are, and what's at stake. Name the current frame explicitly. Now generate 3-5 alternative frames: what if this were a different kind of situation? Each frame makes different elements visible and others invisible. Find the frame that reveals the truth you need people to see.

**Output:** Current frame explicitly stated, 3-5 alternative frames, and the frame that best serves the communication goal with reasoning.

---

## Structure Mapping

*Applies story architecture to any communication.*

Information delivered as data rarely moves people. Information delivered as story does. Apply narrative architecture: (1) Status quo — the world before, (2) Disruption — what changed or needs to change, (3) Stakes — what's at risk if nothing happens, (4) Journey — the path forward, (5) Resolution — the new world this creates. Map the content onto this arc. Cut everything that doesn't move the story forward.

**Output:** Content mapped onto narrative arc, elements to cut, and the structure that moves from status quo to resolution.

---

## Tension Mapping

*Finds or creates the tension that makes communication worth paying attention to.*

Without tension, there is no story. Without story, there is no attention. Tension is the gap between where things are and where they should be — or between what we know and what we need to know. Find the tension already present in this situation: what's at stake? What could go wrong? What is the unresolved question the audience needs answered? If tension is absent, it must be created — not manufactured, but surfaced from what's actually true.

**Output:** The genuine tension in this situation, how to make it visible and felt, and how the communication resolves it.

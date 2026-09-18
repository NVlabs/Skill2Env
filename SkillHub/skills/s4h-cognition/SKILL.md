---
name: s4h-cognition
description: "Entry point for the cognition toolkit. Routes to the right cognition skill based on your situation. Use when you say 'cognition', 'how am I thinking about this', 'why can't I focus', 'what mental model is driving this', 'am I thinking clearly', 'this is too complex to hold in my head', 'what do I actually know here', or want applied cognitive science without knowing which specific tool fits."
---

# Cognition

Applies cognitive science to understand and improve how thinking itself works — attention, mental models, metacognition, and cognitive load. Diagnoses what kind of cognitive work is needed and routes to the right tool.

## Which tool fits

| You need to... | Tool |
|---|---|
| Understand what is capturing or depleting attention — and how to protect it | cognition-attention |
| Surface and audit the mental models driving perception and decisions | cognition-mental-models |
| Apply thinking-about-thinking to monitor comprehension and calibrate confidence | cognition-metacognition |
| Manage the limits of working memory — chunking, offloading, reducing complexity | cognition-cognitive-load |

## Routing Decision

**Framing check:** Confirm the specific cognitive situation before routing. State what you've identified — the thinker or system in question, the cognitive challenge, and what the user wants to improve or understand — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the specific cognitive challenge and what you want to understand or change]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

- **"I can't focus" / "attention keeps getting pulled away" / "how do I protect deep work time"** → cognition-attention (map the attention economy, identify threats and defences)
- **"I keep seeing this the same way" / "what assumptions are built into how I see this" / "what mental model am I using"** → cognition-mental-models (surface the implicit representations driving perception)
- **"I don't know what I don't know" / "how confident should I be" / "am I actually understanding this"** → cognition-metacognition (apply thinking-about-thinking to calibrate and monitor)
- **"This is too much to hold at once" / "complexity is overwhelming" / "how do I simplify this"** → cognition-cognitive-load (apply Sweller's cognitive load theory to manage working memory limits)
- **Unclear** → cognition-metacognition; most cognitive difficulties trace back to not knowing what you do and don't understand

## Confirm Direction

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

## Attention

*Maps the attention economy of a mind or situation — what captures it, what depletes it, and how to protect it.*

Attention is finite and directional. What occupies it is not random — it follows predictable rules: salience, novelty, emotional charge, and personal relevance all compete for the cognitive resource that enables everything else. This skill maps the full attention landscape of a specific person or context: what is actively competing for focus, what legitimate demands exist, what noise can be eliminated, and what structural conditions protect or destroy sustained attention. The output is a prioritised defence plan for cognitive bandwidth.

**Output:** Attention threat map, current depletion sources, structural protection measures, and a priority list for reclaiming focus.

---

## Mental Models

*Surfaces and audits the internal representations that drive perception and decision-making.*

Every perception and decision runs through a mental model — a simplified internal representation of how part of the world works. The danger is that models become invisible: they shape what we notice, how we interpret evidence, and what options we can imagine, all without our awareness. This skill, rooted in Philip Johnson-Laird's model theory, makes the implicit explicit. It identifies which models are active in a situation, tests them for accuracy and completeness, and surfaces the gaps and distortions that are shaping judgment without being seen.

**Output:** Active models identified, accuracy audit (what each model gets right and wrong), gaps and blind spots, and a recommended model update or replacement.

---

## Metacognition

*Applies thinking-about-thinking as a practical tool — monitoring comprehension, calibrating confidence, and knowing what you do not know.*

Metacognition — understanding and regulating your own cognitive processes — is the highest-leverage cognitive skill because it governs all the others. Developed as a formal discipline by John Flavell in the 1970s, it encompasses: knowing what you know and don't know (metacognitive knowledge), monitoring whether you're actually understanding something (metacognitive monitoring), and adjusting your approach when you're not (metacognitive control). This skill applies these three dimensions to a concrete situation where the quality of thinking matters.

**Output:** Metacognitive status across knowledge, monitoring, and control dimensions — with specific gaps, overconfidence alerts, and recommended adjustments.

---

## Cognitive Load

*Manages the limits of working memory — chunking, offloading, and reducing unnecessary complexity to free capacity for what matters.*

George Miller established in 1956 that working memory holds approximately seven items (plus or minus two). John Sweller's Cognitive Load Theory refined this: not all load is equal. Intrinsic load is inherent to the material; extraneous load comes from poor design; germane load builds schemas. The goal is to minimise extraneous load, manage intrinsic load through chunking, and use offloading strategies to extend effective working memory beyond its biological limits.

**Output:** Load type breakdown (intrinsic / extraneous / germane), chunking recommendations, offloading strategy, and redesigned information structure where applicable.

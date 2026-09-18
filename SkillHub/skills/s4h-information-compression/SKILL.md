---
name: s4h-information-compression
description: "Applies lossy vs lossless compression thinking to representation and communication. Use when asked to 'cut this down', 'what can I remove', 'what's essential here', 'summarise without losing the key point', 'what must be preserved', or when a representation needs to be more efficient without becoming misleading."
---

# Information: Compression

Every representation is a compression of reality. A report compresses events. A model compresses a domain. An explanation compresses understanding. A decision brief compresses weeks of analysis. The question is never whether to compress — it's whether the compression preserves what matters.

Claude Shannon proved that there is a theoretical lower bound on how far any lossless compression can go: you cannot compress below the entropy of the source without discarding information. This is the source coding theorem. Applied practically: there is always a floor. A message with genuine information content cannot be shortened indefinitely without loss — and often the thing being shortened to below-floor is not actually long; it's precise. The problem is usually the reverse: sources that are padded, redundant, or poorly structured can be dramatically shortened without any loss, because they weren't near the floor to begin with.

The critical distinction is lossy vs. lossless. Lossless compression preserves every bit of the original — the compression is reversible. Lossy compression discards some information permanently, in exchange for a representation that is smaller or more usable. Both are legitimate; the choice depends entirely on what the information is for, who will use it, and what the cost of loss is. An executive summary is lossy by design. A legal contract is lossless by necessity. The skill is making the trade-off explicit — and knowing what you are throwing away.

James Gleick's *The Information* notes that compression is cognition: the brain is fundamentally a compression engine. Understanding is compression. This is why the best explanations are short: not because they're simpler, but because they've found the structure that allows reconstruction from minimal representation. Teaching someone a principle rather than a list of cases is compression.

---

## Your Process

**Step 1: Identify What the Representation Is For**
Before deciding what to cut, establish the purpose of the compressed form. Who is it for? What decision or action does it need to enable? What understanding must be present in the receiver after they've processed the compressed version? The appropriate compression strategy is entirely downstream of this answer.

**Framing check:** Confirm the representation, its purpose, and the audience before continuing. State what you've identified in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [one-sentence framing of what's being compressed, for whom, and for what purpose]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Classify Information as Essential, Reconstructable, or Discardable**
Work through the full source material and classify every component:

- **Essential:** Cannot be removed without changing the meaning, decision, or understanding that the representation must support. Removing this creates loss that cannot be recovered.
- **Reconstructable:** Can be removed from the representation because a capable receiver will reconstruct it — from context, prior knowledge, inference, or a linked source. This is lossless compression: the information is present in compressed form.
- **Discardable:** Contributes nothing to the purpose of this representation, for this receiver. Removing it creates no loss for the intended use. (Note: discardable for one receiver may be essential for another — compression is always audience-relative.)

**Before proceeding:** Present your classification to the user for review. Use `AskUserQuestion`:
- **Question:** "I've classified the content into essential, reconstructable, and discardable. Before I apply the compression, do any of my classifications look wrong?"
- **Header:** "Classification check"
- **Options:**
  - **Looks right — proceed** — the classification is sound
  - **Move one element** — user will identify something miscategorised
  - **The purpose needs adjusting** — the receiver or use case is different than I understood

**Step 3: Decide Lossy vs. Lossless**
Explicitly declare the compression mode for each component:
- Elements classified as reconstructable → lossless compression strategy (they can be compressed out without loss)
- Elements classified as discardable → safe to drop entirely
- Elements classified as essential but redundantly stated → lossless: consolidate to single occurrence
- If the target format forces dropping essential elements → lossy; state explicitly what is being lost and why

**Step 4: Apply the Compression**
Produce the compressed representation. When compression is lossy, mark clearly — in the output or in a note — what has been dropped and what the receiver would need to know if they required the uncompressed form.

**Step 5: Test Against the Purpose**
Ask: given only the compressed form, can the intended receiver accomplish the intended purpose? Run through the specific decision or action the representation is meant to support. If not, the compression is below the entropy floor — you have compressed past the point of usability.

---

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences — what is being compressed, what must be preserved, and what the tension is — then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full analysis** — Walk through every step, showing the classification and the rationale for each compression decision
  - **Compressed output only** — Deliver the compressed form directly, with a brief note on what was dropped
  - **Classification only** — Identify what's essential vs. reconstructable vs. discardable, and stop there
  - **Reframe** — The read is off; correct it and the analysis will follow the corrected framing

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

## Output Format

**Compression Brief**

- Purpose: [who this is for and what it must enable]
- Mode: Lossless / Lossy / Mixed
- Compression ratio estimate: [rough ratio of compressed to original]

**Classification**

| Element | Classification | Rationale |
|---|---|---|
| [element] | Essential / Reconstructable / Discardable | [why] |

**What is being dropped (lossy elements):** [explicit statement of what information will not be recoverable from the compressed form, and why this is acceptable given the purpose]

**Compressed Output:**

[The compressed representation itself — the actual deliverable]

**Reconstruction Note:** [What a receiver would need to access if they required the full, uncompressed version]

---

## Notes

Compression analysis is most powerful when the receiver and purpose are precisely defined — because what is "reconstructable" and "discardable" depends entirely on the receiver's prior knowledge and the purpose the representation serves. Vague audiences produce over-cautious compression (nothing gets cut because "someone might need it") or reckless compression (things get cut that a specific receiver needed badly).

The nearest-neighbour trap is conflating compression with simplification. Compression is about representation efficiency — minimising form while preserving function. Simplification is about reducing cognitive load. A simplified explanation may actually be longer than the original if it adds scaffolding the receiver needs. Use `/s4h-communication-clarity-audit` when the goal is readability rather than efficiency, and `/s4h-information-redundancy` when the question is specifically about repetition.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Compression applied. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-information-redundancy` — Examine whether the remaining redundancy is load-bearing or wasteful
  - `/s4h-communication-clarity-audit` — Audit the compressed form for clarity and receiver fit
  - `/s4h-information-signal-noise` — Check whether the compression preserved the signal or accidentally compressed it out
  - **Done** — Wrap up and synthesise what we have so far

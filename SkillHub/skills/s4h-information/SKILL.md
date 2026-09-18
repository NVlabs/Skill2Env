---
name: s4h-information
description: "Entry point for the information theory toolkit. Routes to the right information skill based on your situation. Use when you say 'information', 'signal vs noise', 'what matters here', 'too much data', 'what can be cut', 'redundancy', 'uncertainty', 'surprise', 'how much information does this actually contain', or want information-theoretic thinking applied without knowing which specific tool fits."
---

# Information

Applies information theory to problems of signal, noise, compression, redundancy, and uncertainty. Diagnoses what kind of information analysis is needed and routes to the right tool.

Claude Shannon's 1948 paper *A Mathematical Theory of Communication* established that information has measurable structure. That structure applies far beyond telecommunications: to how clearly a message reaches its audience, how much a piece of evidence actually tells you, how efficiently knowledge is encoded, and how resilient a system is against loss. These tools make that structure visible.

## Which tool fits

| You need to... | Tool |
|---|---|
| Separate what matters from what doesn't | information-signal-noise |
| Work out what can be preserved and what can be discarded | information-compression |
| Understand where repetition helps versus wastes | information-redundancy |
| Measure uncertainty, surprise, or information content | information-entropy |

## Routing Decision

**Framing check:** Confirm the information problem in focus before routing. State what you've identified — the source, the question, and what's failing or unclear — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the information problem]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

- **"There's too much data and I can't find what matters"** / **"What's actually signal here?"** → signal-noise
- **"What can I cut without losing what's important?"** / **"How do I say this in half the space?"** → compression
- **"Some things are repeated — is that a problem or a feature?"** / **"Where does redundancy help or hurt?"** → redundancy
- **"How uncertain is this source?"** / **"How surprising is this result?"** / **"How much information does this actually contain?"** → entropy
- **Unclear** → signal-noise; distinguishing signal from noise is the first step in almost every information problem

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

## Signal–Noise

*Separates meaningful signal from background noise — applies SNR thinking to data, communication, and evidence.*

Most sources are a mixture of signal (what you're trying to detect) and noise (everything else). Information is only useful to the extent that the signal can be recovered. This skill applies Shannon's signal-to-noise ratio framework to any domain: a dataset, a conversation, a research base, an organisation's reporting, or a person's attention. It identifies what is driving variation, what is random or irrelevant, and what amplifies versus attenuates the signal. The output is a clear-eyed account of what's actually there versus what's artefact, and which channels to trust.

**Output:** Signal identification, noise sources enumerated, SNR assessment, and recommendations for amplifying signal and suppressing noise.

---

## Compression

*Asks what must be preserved and what can be discarded — lossy vs lossless tradeoffs in representation and communication.*

Every representation compresses reality. The question is whether it compresses well. Shannon proved there's a theoretical lower bound on how far any lossless compression can go — you can't compress below the entropy of the source without losing information. This skill applies that logic to practical representation problems: executive summaries, data models, explanations, memory, decision briefs. It forces the explicit question: what is essential? What can be reconstructed? What, once cut, is gone for good?

**Output:** Identification of essential vs. reconstructable vs. safely discardable elements, lossy/lossless classification, and a compression strategy.

---

## Redundancy

*Maps where redundancy creates resilience and error correction versus where it creates waste.*

Redundancy has two faces. Shannon showed that redundancy in a transmission channel enables error correction — it's the mechanism by which messages survive noisy channels. But redundancy in an argument, a report, or a system can also mean bloat, confused responsibility, and fragility. This skill maps the function of every repetition: is this load-bearing redundancy (fault tolerance, verification, pattern reinforcement) or wasteful redundancy (verbosity, duplication, uncoordinated effort)?

**Output:** Redundancy map distinguishing load-bearing from wasteful repetition, with a strategy for pruning one and preserving the other.

---

## Entropy

*Applies information entropy to measure uncertainty, surprise, and information content in any source.*

Claude Shannon defined information as the reduction of uncertainty. High-entropy sources are unpredictable — each message is surprising and therefore carries more information. Low-entropy sources are predictable — each message is expected and tells you little. This skill applies entropy thinking to any source: how uncertain is it? How much does each piece of evidence actually update your picture? Where is information content high and where is it near zero? Norbert Wiener extended this to cybernetics: information is what distinguishes signal from noise in any self-regulating system.

**Output:** Entropy assessment of the source, identification of high- and low-information elements, and implications for how much weight each piece of input should carry.

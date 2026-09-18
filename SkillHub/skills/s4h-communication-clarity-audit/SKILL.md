---
name: s4h-communication-clarity-audit
description: "Audits a communication for places where the message will be lost, misread, or misunderstood — before it's sent. Triggers: 'clarity audit', 'will this be understood', 'check my message', 'edit for clarity', 'where will this be misread'."
---

# Communication Clarity Audit

Most clarity failures are invisible to the sender because the sender knows what they meant.
The receiver does not have that context, and the gap between what was meant and what is
read is where miscommunication lives. This audit finds that gap by reading the message as
the receiver would — without access to the sender's intent.

---

## Your Process

**Step 1: Read from the Receiver's Perspective**
Do not read this as the writer who knows what was meant. Read it as someone receiving it
cold. What is actually on the page? This requires a deliberate perspective shift — it is
the hardest step and the most important one.

**Framing check:** Confirm the specific message, audience, and goal before continuing. State what you've identified — the actual content being audited, who it's addressed to, and what it's trying to achieve — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the message, its intended audience, and its goal]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Structure Check**
Can the main point be identified within 10 seconds? If not, the structure is obscuring it.
Is the structure serving the reader or the writer's thinking process? The two are often
different.

**Step 3: Jargon Inventory**
List every term or acronym that requires context the reader may not have. Each one is a
potential comprehension failure. Include terms that feel obvious — "obvious" is always
relative to what the writer knows.

**Step 4: Assumption Inventory**
What must the reader already know or believe for this message to make sense? State each
assumption explicitly. For each: does this reader have this context? If not, the message
has a gap.

**Step 5: Ask — Is It Clear?**
Is there a clear action or next step? Is it clear who does what, by when? A message that
informs without directing produces nothing. A message that directs ambiguously produces
the wrong thing.

**Step 6: Name the Most Likely Misreading**
**Before narrowing:** Show the complete set of misreadings identified across all steps to the user first. Use `AskUserQuestion`:
- **Question:** "I've identified [N] potential misreadings. Before I select the most likely one, are there any you'd flag as especially important, or any I've missed?"
- **Header:** "Prioritise"
- **Options:**
  - **Proceed with your selection** — the set looks right
  - **Flag one** — user will name a specific misreading to prioritise
  - **Add a missing one** — user will describe it

State the single most plausible way this message will be misread or misunderstood by a
reasonable receiver. This is the most valuable output — it is the failure that will
actually happen if the message is sent as written.

---

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences — what is being analyzed and what the core question is — then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full analysis** — Complete all steps, reasoning shown throughout
  - **Key findings only** — Bottom-line output, skip step-by-step detail
  - **Breakpoints only** — Where this message will be misread or lost, skip what's already clear
  - **Reframe** — The read is off; correct it and the analysis will follow the corrected framing

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

## Output Format

**Issues found:**

| Category | Issue | Severity (High/Med/Low) | Edit |
|----------|-------|------------------------|------|
| Structure | | | |
| Jargon | | | |
| Assumptions | | | |
| Ask/Action | | | |

**Most likely misreading:**
> [Concrete statement of how a reasonable receiver will misread this — and what they
> will do or believe as a result]

**Priority edits:**
1. [Highest-impact change]
2. [Second highest]
3. [Third]

---

## Notes

A single clear next step with a named owner and a deadline eliminates more miscommunication
than any amount of structural or vocabulary editing. If the ask is ambiguous, fix that
before anything else.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Clarity audited. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-writing-line-editing` — Fix the clarity issues the audit identified
  - `/s4h-communication-objection-mapping` — Address the objections hiding behind confusing points
  - `/s4h-writing-restructure` — Restructure if the clarity issues are structural
  - **Done** — Wrap up and synthesise what we have so far

---
name: s4h-ethics-data-audit
description: "Audit a data collection, retention, or sharing decision against ethical standards. Use when the user is making decisions about what data to collect, how long to keep it, who can access it, or who it's shared with. TRIGGERS: 'audit this data decision', 'is this data practice ok', 'data ethics check', any change to data models, privacy controls, analytics instrumentation, data sharing agreements, or retention policies. Goes beyond legal compliance — evaluates whether the practice is ethical, not just lawful."
---

# Ethics Data Audit

Legal compliance sets the floor. This audit asks whether your data practices clear a higher bar: are they *ethical*?

The distinction matters. GDPR-compliant practices can still be extractive. Lawful data collection can still violate trust. This audit evaluates data decisions through two lenses that legal frameworks tend to underweight: **deontological** (what do users have a right to, regardless of what the terms allow?) and **care ethics** (what do you owe the people whose data you hold, given the relationship and the vulnerability involved?).

---

## Your Process

**Step 1: Define the data practice**
What data is being collected, retained, shared, or used? Be specific: what fields, what volume, what purpose, who can access it, how long is it kept, where does it go?

**Framing check:** Confirm the specific data practice before continuing. State what you've identified — the actual data being handled, its stated purpose, and the decision or change under review — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the data practice, its purpose, and the decision being audited]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

**Step 2: Deontological Assessment — Rights and Duties**
Users have rights that don't disappear because they clicked "I agree." Examine:

- **Informed consent**: Do users genuinely understand what's being collected and why? Would they understand if you explained it plainly, without legal language?
- **Purpose limitation**: Is the data being used only for the purpose users would reasonably expect?
- **Right to exit**: Can users meaningfully withdraw, delete, or limit their data? Is that easy or deliberately difficult?
- **Data as means**: Is data being used to serve users — or to serve the business *at the expense of* users?

Flag any duty being violated, even if legally covered.

**Step 3: Care Ethics Assessment — Relationship and Vulnerability**
Data relationships are not neutral transactions. Examine:

- **Asymmetry**: The organisation knows vastly more about users than users know about the organisation. Does the practice exploit that asymmetry?
- **Vulnerability**: Are any users in this dataset particularly vulnerable (minors, people under financial stress, people in sensitive contexts)? Does the practice account for that?
- **Trust**: If users knew exactly what you were doing with their data, would they feel the relationship was honourable?
- **Harm potential**: What is the worst plausible outcome if this data were breached, misused, or sold? Who bears that harm?

**Before synthesising:** State what each method surfaced in one sentence each. Use `AskUserQuestion`:
- **Question:** "Here's what each method found: [one bullet for deontological findings — the duties most at risk; one bullet for care ethics findings — the relationship and vulnerability concerns most at risk]. Before I synthesise into a verdict, does any direction stand out, or is anything missing?"
- **Header:** "Synthesis direction"
- **Options:**
  - **Synthesise as planned** — methods covered the ground
  - **Weight deontological concerns** — user wants rights and duties to lead the verdict
  - **Weight care ethics concerns** — user wants relationship and vulnerability to lead the verdict
  - **Add a missing angle** — user will name a dimension not yet covered

**Step 4: Produce the audit**

---

## Human Check-in

Before proceeding, use the `AskUserQuestion` tool. State your interpretation of the situation in 1–2 sentences — what is being analyzed and what the core question is — then ask:

- **Question:** "My read: [your 1–2 sentence interpretation]. How do you want to proceed?"
- **Header:** "Scope"
- **Options:**
  - **Full analysis** — Complete all steps, reasoning shown throughout
  - **Key findings only** — Bottom-line output, skip step-by-step detail
  - **Consent and harm potential only** — Skip necessity, proportionality, and retention sections
  - **Reframe** — The read is off; correct it and the analysis will follow the corrected framing

Proceed based on their selection. If the user reframes, incorporate the correction before running any analysis.

## Output Format

**Data Practice Being Audited:**
[What data, what purpose, what handling]

**Deontological Findings**
| Duty/Right | Status | Notes |
|---|---|---|
| Informed consent | ✅ / ⚠️ / ❌ | [explanation] |
| Purpose limitation | ✅ / ⚠️ / ❌ | [explanation] |
| Right to exit | ✅ / ⚠️ / ❌ | [explanation] |
| Data as means | ✅ / ⚠️ / ❌ | [explanation] |

**Care Ethics Findings**
| Dimension | Status | Notes |
|---|---|---|
| Power asymmetry | ✅ / ⚠️ / ❌ | [explanation] |
| Vulnerable populations | ✅ / ⚠️ / ❌ | [explanation] |
| Trust test | ✅ / ⚠️ / ❌ | [explanation] |
| Harm potential | ✅ / ⚠️ / ❌ | [explanation] |

**Verdict**
[2–3 sentences: is this practice ethical, what are the key concerns, what would need to change]

**Recommended Actions**
- [Specific change or safeguard, if any]

---

## Notes

This audit does not replace legal review. It supplements it. A practice can pass this audit and still require legal sign-off. A practice that fails this audit should not be excused by legal compliance.

If the audit turns up significant concerns, consider escalating to `ethics-council` for a full multi-framework analysis.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Data practices audited. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-ethics-consent-review` — Review consent for data practices found in the audit
  - `/s4h-ethics-impact-scan` — Scan broader impact of the data practices
  - `/s4h-logic-check` — Validate the reasoning about data use
  - **Done** — Wrap up and synthesise what we have so far

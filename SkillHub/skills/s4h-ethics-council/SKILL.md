---
name: s4h-ethics-council
description: "Run any decision, feature, policy, or action through a council of 5 ethical framework advisors who independently analyze it from different moral foundations, peer-review each other's reasoning, and synthesize a final verdict. MANDATORY TRIGGERS: 'ethics council this', 'run the ethics council', 'ethical pressure-test', 'is this ethical', 'sanity check the ethics'. STRONG TRIGGERS: any decision with clear stakeholder harm potential, trade-offs between competing values, questions about fairness or rights, situations where someone's interests are being weighed against others. Do NOT trigger on purely technical questions with no stakeholder impact, or simple factual lookups."
---

# Ethics Council

You ask one advisor about an ethical question, you get one moral framework's answer. Utilitarian calculus says yes. Deontological reasoning says no. You have no way to navigate the tension because you only heard one voice.

The council surfaces that tension deliberately. It runs your question through 5 ethical frameworks — each one a serious moral tradition that has grappled with hard questions for centuries. Then they peer-review each other. Then a chair synthesizes the value landscape: not just what to do, but *which values are in conflict and which you're implicitly choosing*.

---

## When to Run the Ethics Council

The council is for decisions where the moral stakes are real.

**Good council questions:**
- "Is it ethical to A/B test on users without explicit consent if the variants are minor?"
- "We're collecting this data. Should we?"
- "We're about to lay off 20% of the team — is this the right way to do it?"
- "Our algorithm deprioritises certain demographics. Is this acceptable?"
- "A supplier uses questionable labour practices but their pricing is significantly better."

**Bad council questions:**
- "What's the best database for this use case?" (technical, not ethical)
- "How do I write a good commit message?" (no stakeholder impact)

---

## The Five Ethical Frameworks

Each framework is a lens — not a job title or personality. They are genuine moral traditions that generate fundamentally different answers to the same question. That divergence is the point.

### 1. Utilitarian
Evaluates outcomes. The right action maximizes benefit and minimizes harm across *all* affected parties — users, employees, third parties, society. Aggregate wellbeing is the measure. Willing to accept harm to some if the net benefit to all is greater. Asks: who is affected, how much, and is the total welfare positive?

### 2. Deontological
Evaluates duties and rights. Some actions are wrong regardless of their consequences — because they violate rights, break promises, treat people as mere means, or cross inviolable principles. The right action respects what people are owed. Asks: are there duties being violated or rights being overridden here, independent of outcomes?

### 3. Virtue Ethics
Evaluates character. The right action is what a person of integrity and good character would do in this situation. Not rules, not calculations — but who you are and who this decision makes you. Asks: what does this decision say about us? Would someone we respect do this?

### 4. Care Ethics
Evaluates relationships and vulnerability. Morality is grounded in our responsibilities to those we are in relationship with, especially those who are dependent or vulnerable. Context matters. Abstract principles can miss who actually bears the cost. Asks: who is in relationship to this decision? Who is vulnerable? Are we honoring those dependencies?

### 5. Justice and Fairness
Evaluates distribution and procedure. Benefits and burdens should be distributed fairly. Decisions should be made through fair processes. Behind a "veil of ignorance" — not knowing which role you'd occupy — would you accept this outcome? Asks: is this fair to everyone, including those with the least power in this situation?

**Why these five:** They represent the major traditions in moral philosophy and generate genuine tension. A policy might maximize utility but violate rights. It might be virtuous but unfair to the vulnerable. Surfacing those conflicts is what makes the council useful.

---

## How a Council Session Works

### Step 1: Frame the Question

Scan the workspace for context before framing — look for `CLAUDE.md`, any relevant docs, or business context that would help the frameworks give grounded rather than abstract answers.

Frame the ethical question clearly and neutrally. The framing should include:
1. The specific decision or action under examination
2. Key stakeholders — who is affected and how
3. The stakes — what happens if this goes wrong, or if it's blocked
4. Any relevant constraints (legal, business, technical)

If the question is too vague ("is our product ethical?"), ask one clarifying question. Just one.

**Framing check:** Confirm the ethical situation before continuing. State what you've identified — the specific decision or action under examination, the key stakeholders, and the primary moral tension — in one sentence, then use `AskUserQuestion`:
- **Question:** "I'm reading this as: [your one-sentence framing of the specific ethical situation, decision, and affected parties]. Is that right?"
- **Header:** "Framing"
- **Options:**
  - **Yes — proceed** — framing is correct
  - **Adjust** — one element is off; user will correct it before you continue
  - **Reframe** — different situation than read; incorporate the correction before proceeding

---

### Human Check-in

After framing the question, use the `AskUserQuestion` tool:

- **Question:** "How do you want to run the council?"
- **Header:** "Council scope"
- **Options:**
  - **Full council** — All 5 advisors + peer review + chair synthesis + saved HTML report
  - **Chair synthesis only** — Skip advisor outputs, deliver the verdict directly
  - **Two frameworks in conflict** — Pick the two most relevant frameworks and show where they diverge
  - **Adjust the framing** — Revisit the question before convening

Proceed based on their selection.

---

### Step 2: Convene the Council (5 subagents in parallel)

Spawn all 5 framework advisors **simultaneously**. Each gets their framework identity and the framed question.

**Subagent prompt template:**
```
You are reasoning from the [Framework Name] tradition in an Ethics Council.

Your framework: [framework description from above — the core moral logic, what it asks, what it prioritizes]

An Ethics Council has been convened on this question:
---
[framed question]
---

Reason from your framework fully and honestly. What does [Framework Name] say about this situation? Where does it find the action acceptable? Where does it find it problematic? What would it require to make this action ethical under your framework?

Do not try to balance all perspectives — that is the chair's job. Apply your framework as strongly as it applies. If your framework has a clear answer, say it. If your framework is genuinely uncertain here, say why.

150–300 words. No preamble.
```

---

### Step 3: Peer Review (5 subagents in parallel)

Collect all 5 responses. Anonymize them as Response A through E.

Spawn 5 reviewer subagents. Each sees all 5 anonymized responses and answers:
1. Which response is the strongest and why?
2. Which response has the biggest blind spot?
3. **Where do the frameworks conflict — what values are actually at stake in that conflict?**

The third question is the addition that makes ethics peer review different from general council peer review. The goal is not just catching what's missing — it's naming the value tension explicitly.

**Reviewer prompt template:**
```
You are reviewing the outputs of an Ethics Council. Five advisors — each reasoning from a different ethical framework — independently analyzed this question:

---
[framed question]
---

Their anonymized responses:

**Response A:** [response]
**Response B:** [response]
**Response C:** [response]
**Response D:** [response]
**Response E:** [response]

Answer these three questions. Be specific. Reference responses by letter.

1. Which response is the strongest? Why?
2. Which response has the biggest blind spot — what is it missing or getting wrong?
3. Where do the frameworks conflict with each other? Name the specific values in tension. (e.g. "A and C conflict because one prioritizes aggregate benefit while the other treats individual rights as inviolable — the real question is whether you believe consequences can override rights in this type of case.")

Under 200 words. Be direct.
```

---

**Before synthesising:** State what each method surfaced in one sentence each. Use `AskUserQuestion`:
- **Question:** "Here's what each framework found: [one bullet per framework — Utilitarian, Deontological, Virtue Ethics, Care Ethics, Justice and Fairness — each summarised in one sentence]. Before I synthesise, does any direction stand out, or is anything missing?"
- **Header:** "Synthesis direction"
- **Options:**
  - **Synthesise as planned** — frameworks covered the ground
  - **Weight [direction]** — user will name which framework's thread to emphasise
  - **Add a missing angle** — user will name a dimension not yet covered

### Step 4: Chair Synthesis

One agent gets everything: the original question, all 5 framework responses (de-anonymized), and all 5 peer reviews.

The chair produces the council verdict in this structure:

**ETHICS COUNCIL VERDICT**

1. **Where the frameworks agree** — moral conclusions that multiple traditions reach independently. High-confidence signals.
2. **Where the frameworks conflict** — genuine value tensions. Do not smooth these over. Name the competing values and explain why the conflict is real.
3. **What values are implicitly at stake** — what this decision is really a choice *about*, beneath the surface question.
4. **The recommendation** — a direct recommendation. Not "it depends." If the frameworks diverge, the chair picks a position and says why.
5. **What would need to change to make this clearly ethical** — if the answer is "this has problems," specify what modifications would resolve them.

**Chair prompt template:**
```
You are the Chair of an Ethics Council. Synthesize the work of 5 ethical framework advisors and their peer reviews into a final verdict.

The question:
---
[framed question]
---

FRAMEWORK RESPONSES:
[de-anonymized advisor responses with framework names]

PEER REVIEWS:
[all 5 peer reviews]

Produce the verdict using this structure:

## Where the Frameworks Agree
[Conclusions multiple traditions reach independently — high-confidence signals]

## Where the Frameworks Conflict
[Genuine value tensions. Name the competing values. Explain why they conflict here.]

## What Values Are Implicitly at Stake
[What this decision is really a choice about — beneath the surface question]

## The Recommendation
[A direct, defensible recommendation. If you side with a minority framework view, explain why.]

## What Would Make This Clearly Ethical
[If the answer is "this has problems" — what specific changes would resolve them]

Be direct. The council's value is clarity about moral stakes, not reassurance.
```

---

### Step 5: Generate the Report

Save a visual HTML report as `ethics-council-report-[timestamp].html` and a full transcript as `ethics-council-transcript-[timestamp].md`.

The HTML report contains:
1. The framed question
2. The chair's verdict (prominent — this is what most people read)
3. A framework agreement/conflict grid — a simple visual showing which frameworks aligned and which diverged
4. Collapsible sections for each framework's full response
5. Collapsible peer review highlights
6. Timestamp footer

Clean design: white background, subtle borders, readable system font, soft accent colors per framework.

---

## Important Notes

- **Spawn all 5 in parallel.** Sequential spawning lets earlier reasoning bleed into later responses.
- **Anonymize for peer review.** Reviewers should evaluate reasoning quality, not defer to a framework they recognize.
- **The chair can dissent from the majority.** If 4 of 5 frameworks endorse an action but the dissenter's reasoning is most compelling, the chair should side with the dissenter and explain why.
- **The conflict is the finding.** When frameworks diverge, that is not a failure of the council — it is the council working correctly. The divergence names a genuine value trade-off that the decision-maker must own.

---

## What's Next

After delivering this output, use `AskUserQuestion` to offer the next move:

- **Question:** "Council verdict in. What's next?"
- **Header:** "Next"
- **Options:**
  - `/s4h-ethics-check` — Verify the council verdict against a baseline check
  - `/s4h-decision-criteria-weighting` — Weight decision criteria based on the council's findings
  - `/s4h-logic-fixer` — Address logical flaws the council identified
  - **Done** — Wrap up and synthesise what we have so far

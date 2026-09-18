---
name: alterlab-syllabus-ai-policy
description: "Drafts course-level generative-AI use policies and syllabus statements: assigns each graded task a permitted/restricted/prohibited tier (modeled on Cornell's prohibit/allow-with-attribution/encourage framework), writes the disclosure clause with a verbatim APA (OpenAI, 2023) or MLA Works Cited citation template for ChatGPT, and adds assessment-integrity, accessibility, and equity language bound to the institution's own academic-integrity code. Ships scripts/policy_builder.py to emit a paste-ready statement and scripts/policy_lint.py to flag a vague or self-contradicting draft. Use when the request mentions a syllabus AI policy, a course statement on ChatGPT or generative AI, an academic-integrity clause for AI tools, an AI-disclosure rule, or per-assignment permitted/prohibited AI tiers. For full course/backward design, syllabus, or rubrics use alterlab-teaching-design; for human-subjects AI-tool ethics use alterlab-research-ethics. Part of the AlterLab Academic Skills suite."
license: MIT
allowed-tools: Read Write Edit Bash(python:*) WebFetch
compatibility: No API key or network required — emits institution-parameterized policy text from local templates via `uv run python`; WebFetch is used only to read a linked institutional academic-integrity code when the user supplies its URL
metadata:
  skill-author: AlterLab
  version: "1.0.0"
  last_updated: "2026-06-06"
  depends_on: "alterlab-teaching-design (owns full syllabus/backward design; this is the focused AI-policy add-on)"
---

# Syllabus AI-Use Policy Drafter — Per-Course, Per-Assignment GenAI Statements

The focused add-on that turns "what's my AI policy?" into a concrete, paste-ready
syllabus statement. It does **one thing well**: given a course and its graded
tasks, it assigns each task an explicit **permitted / restricted / prohibited**
tier, writes the matching disclosure and attribution clause, and binds the whole
statement to the institution's own academic-integrity code — so the policy is
enforceable, not aspirational. It deliberately does **not** author the rest of
the syllabus, learning outcomes, or rubrics; that is `alterlab-teaching-design`.

## When to Use This Skill

Use it when the request is about the **AI-use rules of a course or assignment**:

```
Draft an AI-use policy for my syllabus.
Write a course statement on ChatGPT / generative AI for students.
I need an academic-integrity clause that covers AI tools.
Give me per-assignment rules: where can students use AI, where not?
How should students disclose and cite AI they used in an essay?
Make my AI policy consistent with our university's integrity code.
```

→ Gather the course context (level, discipline, the list of graded tasks, the
institution's integrity-code reference), assign each task a tier, then run
`scripts/policy_builder.py` to emit the statement and `scripts/policy_lint.py`
to catch contradictions before you hand it back.

### Does NOT Trigger

This skill is a narrow add-on. Route adjacent asks to the right sibling:

| The ask is really about… | Route to | Why not here |
|--------------------------|----------|--------------|
| Designing the whole course / syllabus, learning outcomes, rubrics, lesson plans, backward design | `alterlab-teaching-design` | Owns full course/backward design; this skill only writes the AI-policy section |
| Ethics of using an AI tool on **human-subjects data** (IRB, consent, de-identification) | `alterlab-research-ethics` | Research-ethics / IRB territory, not a teaching policy |
| Whether a *student submission* was AI-generated; running a detector | `alterlab-teaching-design` (assessment) | This skill writes policy; it does **not** adjudicate or detect individual cases |
| Verifying that *citations* a student or author produced actually exist | `alterlab-citation-verifier` | Citation existence-checking, not policy drafting |
| Turkish-system integrity/ethics process (ÜAK, YÖK etik kurul) | `alterlab-tr-research-ethics` | Turkey-specific ethics workflow, parameterized differently |
| Institutional accreditation / assurance-of-learning reporting | `alterlab-accreditation-aol` | Program-level AoL, not a course AI clause |

If the request mixes "design my course" **and** "write my AI policy", do the AI
policy here and hand the rest to `alterlab-teaching-design`.

---

## The Tier Model

Every graded task is assigned exactly one tier. The three-tier shape mirrors the
Cornell University faculty-committee framework (prohibit / allow-with-attribution
/ encourage) — a published, citable model — but the **wording is yours** and is
bound to your institution's integrity code, never invented.

| Tier | Meaning | Student obligation |
|------|---------|--------------------|
| **Prohibited** | No generative-AI use; the task measures a skill AI would substitute for | None permitted; use is an integrity violation under the cited code |
| **Restricted** | AI permitted for *named* sub-tasks only (e.g. brainstorming, grammar), not for the assessed deliverable | Disclose what tool was used, for what, and how — see the disclosure clause |
| **Permitted** | AI use is allowed and may be encouraged (e.g. as a tutor, for accessibility) | Disclose and attribute per the citation template; remain responsible for accuracy |

**Default-deny when unstated.** If the course gives no tier for a task, the
statement says the task is *Prohibited* until the instructor decides — never
silently "anything goes". A vague "students may use AI responsibly" line is the
single most common failure and `policy_lint.py` flags it.

See `references/tier_framework.md` for the full decision tree (which tier fits
which assessment type), worked per-discipline examples, and the verbatim Cornell
tier definitions this is modeled on.

---

## The Disclosure & Attribution Clause

A tier alone is not a policy. Restricted and Permitted tasks require students to
**disclose and cite** AI use, and the statement must hand them an exact citation
format — not "cite it appropriately". Use the documentation standard the course
already uses:

- **APA 7** — reference-list entry credits the maker, not the tool as author:
  `OpenAI. (2023). ChatGPT (Mar 14 version) [Large language model]. https://chat.openai.com/chat`,
  with in-text `(OpenAI, 2023)`; reproduce the prompt and output in an appendix
  or the Methods section. (APA Style, *How to cite ChatGPT*.)
- **MLA 9** — Works Cited via the template-of-core-elements, treating the tool as
  the container, **not** the author:
  `"<prompt>" prompt. ChatGPT, <version>, OpenAI, <date>, <URL>.`
  MLA also requires acknowledging *functional* uses (editing, translation) in a
  note. (MLA Style Center, *How do I cite generative AI in MLA style?*.)

`references/disclosure_and_citation.md` carries both verbatim templates, a
Chicago-style note option, and a ready-made student "AI-use declaration" block
the statement can append to each submission.

---

## Assessment-Integrity, Accessibility & Equity Language

Three clauses every statement should carry, all parameterized — never asserted as
fact about a specific tool:

1. **Integrity binding** — one sentence tying prohibited-tier misuse to the named
   institutional code (e.g. "violations are handled under <CODE_REF>"). This is
   what makes the policy enforceable; leave `<CODE_REF>` as a fill-in if the user
   has not supplied it, and say so.
2. **Accessibility / equity** — note that some students rely on AI assistive tools
   and that not all students have paid-tier access, so required AI use should be
   free-tier-achievable or provided. Do **not** claim a specific tool is
   accessible/compliant unless the user supplies that fact.
3. **No-detector-as-proof** — if the user asks the policy to lean on an "AI
   detector", flag that detector outputs are probabilistic and should not be the
   sole basis of an integrity finding; the policy states *process*, it does not
   adjudicate. (Adjudicating an individual case is out of scope — see the routing
   table.)

Detail, sample wording, and the equity checklist live in
`references/integrity_accessibility.md`.

---

## How to Run It

### 1. Build a statement from course context

```bash
uv run python skills/faculty-life/alterlab-syllabus-ai-policy/scripts/policy_builder.py \
    --course "PSY 201 Research Methods" --level undergraduate \
    --doc-standard apa \
    --integrity-code "IEU Student Disciplinary Regulation" \
    --task "Literature review essay=restricted:brainstorming and outlining only" \
    --task "In-class exam=prohibited" \
    --task "Data-analysis report=permitted:as a coding tutor" \
    --out ai_policy.md
```

- `--task "<name>=<tier>[:<scope/notes>]"` — repeatable; tier ∈
  `prohibited|restricted|permitted`. A task with no tier is emitted as
  `prohibited` with a visible "instructor to confirm" note.
- `--doc-standard apa|mla|chicago|none` selects the citation template block.
- `--integrity-code "<ref>"` is inserted verbatim; omit it and the output keeps a
  `<CODE_REF>` placeholder plus a warning.
- Omit `--out` to print the Markdown statement to stdout.

The script is **stdlib-only** (no network, no keys): it fills local templates and
never invents an integrity code, a tool capability, or a citation URL.

### 2. Lint a draft (yours or the generated one)

```bash
uv run python skills/faculty-life/alterlab-syllabus-ai-policy/scripts/policy_lint.py ai_policy.md
```

`policy_lint.py` flags the common failure modes: a vague catch-all ("use AI
responsibly") with no per-task tier, a Restricted/Permitted tier with **no**
disclosure clause, a missing or placeholder integrity-code reference, a citation
instruction with no concrete template, and "prohibited" language that
contradicts a "permitted" line for the same task. It exits non-zero on any
`error`-level finding so it can gate a CI or a pre-handoff check.

### 3. Read back and hand off

Present the statement, the lint verdict, and **every unresolved placeholder**
(`<CODE_REF>`, unconfirmed tool claims). If the user also wants the surrounding
syllabus, outcomes, or a rubric, hand off to `alterlab-teaching-design` rather
than improvising them here.

---

## Self-Check Before Returning a Policy

- Does **every** graded task have an explicit tier, with unstated tasks defaulted
  to Prohibited (not "responsible use")?
- Does every Restricted/Permitted task carry a disclosure clause **and** a
  concrete citation template (not "cite appropriately")?
- Is the integrity-code reference real (user-supplied) or a clearly-marked
  placeholder — never an invented regulation name?
- Did you avoid asserting that a specific tool is accurate, compliant, or
  accessible unless the user gave you that fact?
- Did `policy_lint.py` pass (no `error` findings)?

---

## References

- `references/tier_framework.md` — the prohibit/restrict/permit decision tree,
  per-assessment-type guidance, worked examples, and the verbatim Cornell
  faculty-committee tier definitions this models.
- `references/disclosure_and_citation.md` — APA 7, MLA 9, and Chicago AI-citation
  templates (verbatim), plus a student AI-use declaration block.
- `references/integrity_accessibility.md` — integrity-binding wording,
  accessibility/equity checklist, and the detector-as-evidence caution.

### Sources (verified)

- Cornell University, *Report of the Committee on Generative Artificial
  Intelligence in Education* — prohibit / allow-with-attribution / encourage
  course-policy framework. teaching.cornell.edu.
- APA Style, *How to cite ChatGPT* — `OpenAI. (2023). ChatGPT (… version) [Large
  language model]. https://chat.openai.com/chat`. apastyle.apa.org.
- MLA Style Center, *How do I cite generative AI in MLA style?* — tool-as-container
  Works Cited template; do not treat the tool as author. style.mla.org.

Part of the AlterLab Academic Skills suite.

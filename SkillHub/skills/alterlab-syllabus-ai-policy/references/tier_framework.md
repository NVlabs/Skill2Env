# Tier Framework — Prohibited / Restricted / Permitted

Detailed decision support for assigning a generative-AI use tier to each graded
task in a course. The three-tier shape is modeled on a published, citable source
(Cornell University's faculty-committee framework); the wording you ship is your
own and is bound to your institution's academic-integrity code.

## Contents

1. The model and its source
2. The decision tree (which tier fits which assessment)
3. Per-discipline worked examples
4. Common mistakes the tier model prevents

---

## 1. The model and its source

Cornell University's *Report of the Committee on Generative Artificial
Intelligence in Education* recommends instructors place each activity in one of
three categories (verbatim category intent):

- **Prohibit** — "the use of GAI where its use would substitute for or interfere
  with core learning objectives, particularly in courses where students are
  developing foundational knowledge or skills."
- **Allow with attribution** — GAI is a useful resource but the instructor is
  "clear about student expectations in terms of documentation and attribution,
  what work is expected to be produced by the student themselves."
- **Encourage** — GAI use "where students can leverage GAI to focus on
  higher-level learning objectives, explore creative ideas, or otherwise enhance
  learning."

This skill renames these to **Prohibited / Restricted / Permitted** for syllabus
brevity, mapping:

| Cornell category | This skill's tier |
|------------------|-------------------|
| Prohibit | **Prohibited** |
| Allow with attribution | **Restricted** (named sub-tasks) or **Permitted** (broad, with attribution) |
| Encourage | **Permitted** |

The split of "allow with attribution" into Restricted vs Permitted is the one
editorial choice this skill adds: *Restricted* names exactly which sub-tasks AI
may touch (and bars the assessed deliverable), while *Permitted* allows broad use
under disclosure. Both require attribution — that is Cornell's invariant.

> Source: Cornell University, *Report of the Committee on Generative Artificial
> Intelligence in Education*, teaching.cornell.edu (CU Committee Report). The
> report directs faculty to Cornell's Center for Teaching Innovation for
> standardized sample language rather than fixing one wording — which is exactly
> why this skill parameterizes wording rather than hard-coding a statement.

## 2. The decision tree

Ask, in order, for each graded task:

1. **Does the task directly measure the skill AI would do for the student?**
   (e.g. "write a paragraph of argument", "solve the integral by hand",
   "translate this passage", "produce original code logic.")
   → **Prohibited.** AI use here measures the tool, not the student.

2. **Is AI useful for a *supporting* step but not the assessed product?**
   (e.g. brainstorming topics, generating practice questions, checking grammar,
   explaining a concept like a tutor.)
   → **Restricted.** Name the allowed sub-tasks explicitly; bar the deliverable.

3. **Is AI use a legitimate, even encouraged, part of the deliverable** — and the
   learning objective is *using AI well* or accessibility/productivity?
   (e.g. a prompt-engineering assignment, an AI-assisted literature scan with
   human verification, accessibility support.)
   → **Permitted.** Require disclosure + citation; student stays responsible for
   accuracy and for verifying anything AI produced.

4. **Unsure / not yet decided?**
   → **Prohibited by default,** flagged "instructor to confirm." Never emit
   "students may use AI responsibly" with no per-task tier — that is
   unenforceable and is the single most common policy failure.

## 3. Per-discipline worked examples

These are illustrative *shapes*, not prescriptions; the instructor's objectives
decide the tier.

| Course / task | Suggested tier | Rationale |
|---------------|----------------|-----------|
| First-year writing — argumentative essay | Prohibited (drafting) | The course *is* learning to write the argument |
| First-year writing — topic brainstorm before the essay | Restricted (brainstorm only) | Ideation is a support step, not the assessed product |
| Intro programming — implement a sorting algorithm | Prohibited | Measures the student's algorithmic skill |
| Upper-level data science — analysis report | Permitted (AI as coding tutor) | Goal is the analysis; AI-assisted coding is realistic practice |
| Research methods — literature review | Restricted (search/summary scaffolding, human-verified) | AI may scaffold; claims and citations must be student-verified |
| Take-home exam | Prohibited | Closed assessment of individual mastery |
| Prompt-engineering / AI-literacy assignment | Permitted (AI use *is* the task) | The learning objective is using AI itself |
| Accessibility accommodation (any task) | Permitted (assistive use) | Equity: assistive AI use is not an integrity issue |

## 4. Common mistakes the tier model prevents

- **The blanket sentence.** "Students may use AI responsibly" gives students no
  actionable rule and gives the instructor no enforcement basis. Always
  per-task.
- **Silent permission.** Omitting a task from the policy is read by students as
  "anything goes." Default-deny (Prohibited + confirm note) instead.
- **Tier without disclosure.** A Restricted/Permitted tier with no disclosure +
  citation clause is half a policy. See `disclosure_and_citation.md`.
- **Contradiction.** Listing the same task as both prohibited and permitted (often
  from copy-paste) — `scripts/policy_lint.py` catches this.

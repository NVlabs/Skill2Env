---
name: alterlab-accreditation-aol
description: Scaffolds program-level Assurance-of-Learning (AoL) documentation for AACSB (2020 Standard 5) and ABET (Criterion 3 Student Outcomes, Criterion 4 Continuous Improvement) accreditation — program learning outcomes / competency goals, curriculum-to-outcome mapping matrices, direct- and indirect-assessment plans, rubric design, and closing-the-loop continuous-improvement narratives — and validates the structure of an outcome-mapping matrix with scripts/aol_matrix.py. Use when the user needs AACSB or ABET assurance-of-learning material, a program-learning-outcomes set, a curriculum/outcome map or coverage matrix, a direct/indirect assessment plan, a closing-the-loop report, or accreditation self-study text. For single-course design or course rubrics prefer alterlab-teaching-design; for post-award grant reports prefer alterlab-grant-reporting. Part of the AlterLab Academic Skills suite.
license: MIT
allowed-tools: Read Write Edit Bash(python:*) Bash
compatibility: No API key, account, or network required — accreditation-format guidance plus a stdlib-only outcome-mapping-matrix validator (scripts/aol_matrix.py). The school still submits its self-study through AACSB myAccreditation or the ABET portal; this skill drafts text and checks structure, it does not file or accredit.
metadata:
  skill-author: AlterLab
  version: "1.0.0"
---

# Accreditation Assurance-of-Learning — Program-Level AoL for AACSB & ABET

Assurance of Learning (AoL) is the part of accreditation that proves, with
evidence, that a *program* delivers the learning it promises. It is a distinct
workload from designing a single course: it operates at the **degree-program
level**, ties **program learning outcomes (PLOs)** to the curriculum through a
mapping matrix, gathers **direct and indirect** assessment evidence against
those outcomes, and writes the **closing-the-loop** narrative showing the program
changed something in response to the data.

This skill scaffolds that documentation for the two accreditors AlterLab
faculty most often face — **AACSB** (business) and **ABET** (engineering &
computing) — in each accreditor's own structure. It drafts text and checks the
shape of an outcome-mapping matrix; the school still files its self-study
through the accreditor's own portal.

## When to Use This Skill

Use this skill when the user needs to:

- Write or refine a set of **program learning outcomes / competency goals** for a
  degree program (AACSB competencies, ABET student outcomes).
- Build a **curriculum-to-outcome mapping matrix** (which courses Introduce /
  Reinforce / Master each outcome) and check it for coverage gaps.
- Design a **direct + indirect assessment plan** against the outcomes (which
  measure, in which course, on what cycle).
- Draft **rubrics keyed to a program outcome** for direct assessment of student
  work (the assessment instrument, not a course grade).
- Write a **closing-the-loop / continuous-improvement** narrative: results →
  interpretation → action → re-assessment.
- Draft **AACSB Standard 5** or **ABET Criterion 3/4** self-study prose, or an
  AoL section of a continuous-improvement report.

### Does NOT Trigger — route these elsewhere

| The request is really about… | Route to |
|------------------------------|----------|
| Designing a **single course** — its schedule, activities, course-level rubric, learning objectives for one class | `alterlab-teaching-design` |
| Writing an **AI-use / academic-integrity policy** for a syllabus | `alterlab-syllabus-ai-policy` |
| **Post-award grant** progress/final reports, RPPR, periodic reports, budget variance | `alterlab-grant-reporting` |
| Designing a **survey or questionnaire** instrument as a research tool (validity, scales) | `alterlab-survey-design` |
| An individual's **doçentlik** promotion eligibility against ÜAK criteria | `alterlab-docentlik-eligibility` |
| **YÖKATLAS** program placement / quota / ranking data for a Turkish program | `alterlab-yokatlas` |
| Verifying the **citations** in a self-study actually exist | `alterlab-citation-verifier` |

If the work is about one course rather than the whole program, stop and route to
`alterlab-teaching-design`. This skill is program-level only.

## The two accreditors (verified)

Do not invent standard numbers, outcomes, or criterion text. The verbatim
outcome lists and the full per-standard breakdown live in
[`references/accreditor_standards.md`](references/accreditor_standards.md). The
essentials:

### AACSB — 2020 Business Accreditation Standards, **Standard 5: Assurance of Learning**

AoL sits in the curriculum cluster of the 2020 standards: **Standard 4
Curriculum**, **Standard 5 Assurance of Learning**, **Standard 6 Learner
Progression**, **Standard 7 Teaching Effectiveness and Impact**. Standard 5 has
four sub-standards:

| § | Title |
|---|-------|
| 5.1 | Assurance of Learning Processes (direct + indirect measures; results lead to curricular and process improvements) |
| 5.2 | Degree Equivalency (equivalent outcomes across location/modality) |
| 5.3 | Stackable Microlearning Credentials |
| 5.4 | Non-Degree Executive Education |

Standard 5 is **principles-based**. AACSB's own position is that *more*
complexity, more competency goals, or assessing every competency every year does
**not** make an AoL process better — a systematic, mission-informed process that
produces meaningful improvement does. Key requirements (5.1): competencies are
identified **per degree program**, derive from the school's mission, are
**reported at the degree level (not the major level)**, and AoL must employ
**both direct and indirect measures** across the assessment portfolio.

- **Direct measures** — evidence from learner work based on direct observation of
  performance: examinations, quizzes, assignments, internship/externship
  feedback.
- **Indirect measures** — third-party input *not* based on direct observation:
  e.g. employer surveys, focus groups, interviews, external outcome measures.

AACSB AoL is concerned with **broad, program-level competency goals** for each
degree program, *not* detailed goals by course or topic — that course-level work
is `alterlab-teaching-design`'s job.

### ABET — **Criterion 3 (Student Outcomes)** + **Criterion 4 (Continuous Improvement)**

ABET frames AoL across linked criteria: **Criterion 2 Program Educational
Objectives** (what graduates achieve a few years out), **Criterion 3 Student
Outcomes** (what students can do by graduation), **Criterion 4 Continuous
Improvement** (the assessment/evaluation loop that uses outcome data to improve
the program).

ABET's engineering criteria specify **seven required student outcomes (1)–(7)** —
problem-solving, engineering design, communication, ethical/professional
responsibility, teamwork, experimentation & data analysis, and acquiring/applying
new knowledge. The verbatim text of all seven is in the references file; **quote
them exactly** and never paraphrase a numbered outcome into the self-study.

> Computing programs (CAC) and other commissions use a differently-worded outcome
> set. This skill scaffolds the engineering (EAC) seven outcomes by default;
> confirm the commission and pull that commission's exact outcome text before
> drafting. If you cannot confirm the exact wording, say so rather than invent it.

## How to build an AoL package

1. **Establish scope first.** Which accreditor (AACSB vs ABET), which commission,
   and which **degree program**? AoL is per-program. If unstated, ask before
   drafting — the structure differs by accreditor.
2. **Fix the outcomes.** For ABET, use that commission's exact published student
   outcomes (engineering = the seven in the references file). For AACSB, define
   program competency goals derived from the school's mission, stated at the
   degree level. Each outcome must be observably assessable.
3. **Map the curriculum to the outcomes.** Build a matrix: rows = required
   courses, columns = outcomes, cells = coverage level (commonly
   **I**ntroduced / **R**einforced / **M**astered, or **A**ssessed). Every
   outcome needs at least one course where it is assessed; flag any outcome with
   no assessment point. Validate the matrix structure with the script below.
4. **Plan direct + indirect assessment.** For each outcome pick at least one
   **direct** measure (embedded exam question, rubric-scored assignment, project,
   internship evaluation) and round out the portfolio with **indirect** measures
   (employer/alumni survey, exit interview, focus group). Record measure,
   course/point of collection, target/benchmark, and cycle. AACSB requires both
   measure types across the portfolio; do not present indirect evidence alone for
   the whole school.
5. **Write rubrics keyed to outcomes** (not to a course grade). Each row is a
   trait tied to the outcome; levels describe observable performance. Templates:
   [`references/aol_templates.md`](references/aol_templates.md).
6. **Close the loop.** Report results against the target, **interpret** them,
   state the **action taken** (curriculum/process change), and the **re-assessment
   point**. A loop that reports data but changes nothing is not closed — both
   accreditors look for the change. Detail and worked narrative:
   [`references/closing_the_loop.md`](references/closing_the_loop.md).
7. **Flag, never fabricate.** Assessment results, cohort sizes, target
   percentages, course numbers, and dates come only from the user's materials.
   Mark anything missing as `[TODO: confirm]`. Never invent an outcome score, a
   standard number, or an outcome's wording. Hand any reference list to
   `alterlab-citation-verifier`.

## Validate the mapping matrix — don't eyeball it

A coverage gap (an outcome no course assesses) or a thin matrix (an outcome
touched only at "Introduced") is exactly what a peer-review team flags. Check the
matrix structurally instead of reading it by hand:

```bash
uv run python skills/faculty-life/alterlab-accreditation-aol/scripts/aol_matrix.py \
    path/to/matrix.csv --assessed-levels M,A --json
```

The CSV has a `course` column and one column per outcome; cells hold coverage
codes (e.g. `I`, `R`, `M`, `A`, or blank). The script reports, per outcome:
whether it is **covered at all**, whether it has at least one **assessment-level**
cell (default `M` or `A`), and the count by level — then a program-level verdict
(`OK` / `GAPS`). It does **no** network I/O and uses only the Python standard
library. It checks *structure and coverage*, not whether the pedagogy is sound —
that judgment stays with the user and the faculty.

See [`references/aol_templates.md`](references/aol_templates.md) for the matrix
CSV layout, the I/R/M scheme, and example rows.

## Guardrails

- **Program-level, not course-level.** This skill never writes a course
  schedule, course-grade rubric, or single-class objectives — that is
  `alterlab-teaching-design`. It maps a *program* to its outcomes.
- **No invented standards or outcomes.** Standard/criterion numbers and the exact
  text of student outcomes come from the references file (verified against the
  accreditors' published criteria). If the user's program uses a different
  commission, get that commission's exact outcome text first; do not paraphrase.
- **No invented results.** Scores, targets, cohort counts, course numbers, and
  dates come from the user. Mark gaps `[TODO: confirm]`.
- **The school submits, not the skill.** This skill drafts text and checks matrix
  structure; the school files its self-study through AACSB myAccreditation or the
  ABET portal. The skill has no portal access and claims none.
- **Both measure types.** Don't let an AACSB portfolio rest on indirect evidence
  alone; pair direct and indirect measures across programs.

## References

- [`references/accreditor_standards.md`](references/accreditor_standards.md) —
  AACSB 2020 Standard 5 (5.1–5.4) detail with direct/indirect definitions, and
  the verbatim ABET Criterion 2/3/4 text including all seven engineering student
  outcomes, each with its source.
- [`references/aol_templates.md`](references/aol_templates.md) — PLO-writing
  guidance, the curriculum-to-outcome mapping matrix CSV layout (I/R/M scheme),
  a direct/indirect assessment-plan table, and an outcome-keyed rubric template.
- [`references/closing_the_loop.md`](references/closing_the_loop.md) — the
  results → interpretation → action → re-assessment structure with a worked
  closing-the-loop narrative and the questions each accreditor asks.
- `scripts/aol_matrix.py` — stdlib-only curriculum-to-outcome coverage validator.

Part of the AlterLab Academic Skills suite.

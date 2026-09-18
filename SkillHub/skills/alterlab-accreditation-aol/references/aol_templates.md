# AoL Templates — PLOs, Mapping Matrix, Assessment Plan, Rubric

Reusable structures for the program-level AoL package. These are *format*
templates — fill them with the program's real outcomes, courses, and data; never
ship placeholder numbers as if they were findings.

## Table of contents

- [Writing program learning outcomes (PLOs)](#writing-program-learning-outcomes-plos)
- [Curriculum-to-outcome mapping matrix](#curriculum-to-outcome-mapping-matrix)
- [The matrix CSV layout (for aol_matrix.py)](#the-matrix-csv-layout-for-aol_matrixpy)
- [Direct + indirect assessment plan](#direct--indirect-assessment-plan)
- [Outcome-keyed rubric template](#outcome-keyed-rubric-template)

---

## Writing program learning outcomes (PLOs)

A PLO / competency goal states what a *graduate of the program* can do. It is
broader than a course objective and must be **observably assessable**.

- **Program-level, not course-level.** "Graduates can communicate effectively
  with a range of audiences" — not "students submit a lab report in week 6."
- **One observable ability per outcome**, led by an action verb (analyze, design,
  evaluate, communicate, apply).
- **Assessable** — you can name at least one direct measure that produces
  evidence for it.
- **Mission-aligned (AACSB)** — competencies derive from the school's mission and
  are reported at the **degree level**.
- **Exact text where mandated (ABET)** — for ABET student outcomes, adopt the
  commission's published wording verbatim rather than writing your own.

Keep the set small. AACSB explicitly warns that a *larger* number of competency
goals does not make an AoL process better; a focused, systematic set does.

---

## Curriculum-to-outcome mapping matrix

Rows = required courses; columns = outcomes; each cell records the **coverage
level** of that outcome in that course. The common scheme:

- **I — Introduced**: first, foundational exposure.
- **R — Reinforced**: practiced and developed.
- **M — Mastered**: demonstrated at the level expected at graduation (often the
  point chosen for **direct assessment**).
- **A — Assessed**: a data-collection point for this outcome (some schools use
  `A` instead of, or alongside, `M`).
- blank: the course does not address that outcome.

Coverage rules a peer-review team expects:

- **Every outcome is assessed somewhere** — at least one `M`/`A` cell per column.
  An outcome with only `I`/`R` and no assessment point is a gap.
- **Developmental progression** — outcomes generally move `I → R → M` across the
  curriculum, not assessed at "Introduced" only.
- **No orphan outcomes** (no course covers it) and ideally no orphan required
  courses (covers nothing).

Example (illustrative layout, not real program data):

| course | PLO1 | PLO2 | PLO3 | PLO4 |
|--------|------|------|------|------|
| BUS101 | I    | I    |      |      |
| BUS210 | R    |      | I    | R    |
| BUS320 | R    | R    | R    |      |
| BUS480 | M    | M    | M    | M    |

---

## The matrix CSV layout (for aol_matrix.py)

`scripts/aol_matrix.py` reads a CSV with:

- a first column named **`course`** (case-insensitive), and
- one column per outcome (header = outcome id, e.g. `PLO1` or `SO3`).

Cells hold coverage codes (`I`, `R`, `M`, `A`) or are blank. Example:

```csv
course,PLO1,PLO2,PLO3,PLO4
BUS101,I,I,,
BUS210,R,,I,R
BUS320,R,R,R,
BUS480,M,M,M,M
```

Run:

```bash
uv run python skills/faculty-life/alterlab-accreditation-aol/scripts/aol_matrix.py \
    matrix.csv --assessed-levels M,A --json
```

The validator reports, per outcome: covered yes/no, has an assessment-level cell
(default `M`/`A`) yes/no, and the count of courses at each level — then a program
verdict (`OK` if every outcome is both covered and assessed, else `GAPS`).
`--assessed-levels` lets you change which codes count as an assessment point.

---

## Direct + indirect assessment plan

For each outcome, name at least one **direct** measure and pair the portfolio
with **indirect** measures. Record where and when each is collected.

| Outcome | Direct measure (course / point) | Target | Indirect measure | Cycle |
|---------|--------------------------------|--------|------------------|-------|
| PLO1 | Embedded exam questions, BUS480 | ≥ 70% at "proficient" | Alumni survey item | Annual |
| PLO3 | Capstone presentation rubric, BUS480 | ≥ 75% at "proficient" | Employer survey | Biennial |

- **Direct** = direct observation of student performance (exams, rubric-scored
  assignments, projects, internship/externship evaluation).
- **Indirect** = third-party input not based on direct observation (employer
  surveys, alumni surveys, focus groups, exit interviews, external measures).
- AACSB requires **both types across the portfolio**; don't rely on indirect
  evidence alone for the whole school.
- Set a **target/benchmark** per measure so results can be judged "met / not met"
  — that judgment is what drives the closing-the-loop action.

---

## Outcome-keyed rubric template

A rubric for direct assessment is keyed to **one program outcome**, not to a
course grade. Each row is a trait of that outcome; columns are performance
levels with **observable** descriptors.

| Trait (of PLO_n) | Beginning (1) | Developing (2) | Proficient (3) | Exemplary (4) |
|------------------|---------------|----------------|----------------|---------------|
| _trait 1_ | _observable_ | _observable_ | _observable_ | _observable_ |
| _trait 2_ | … | … | … | … |

- Score student work against the trait descriptors; aggregate to the
  outcome-level result that feeds the assessment plan's target.
- Keep the rubric **separate from grading**: a student can earn a good course
  grade while the program-outcome data still shows a gap to act on.
- For designing a rubric for a **single course's** assignments (not program
  assessment), use `alterlab-teaching-design` instead.

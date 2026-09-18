# Letter Types — Reader, Decision, Register, Structure

The five academic letter types differ in **who reads them**, **what decision they
inform**, and therefore **what register and evidence** the letter must carry.
Writing one type in another's register is the most common structural defect — most
often, writing a tenure external-review letter as if it were an advocacy letter.

The scaffold script (`scripts/letter_scaffold.py`) keys its section skeletons off
these five type slugs: `grad-admission`, `faculty-hiring`, `tenure-external`,
`fellowship`, `award-nomination`.

---

## 1. Graduate admission (`grad-admission`)

- **Reader:** an admissions committee, often reading dozens of letters, looking
  for *fit and trajectory* for a specific program (MS / PhD).
- **Decision:** admit / waitlist / reject; sometimes funding.
- **Register:** grounded advocacy. The candidate's track record is short, so the
  letter argues **potential** from concrete evidence of how they think and work.
- **What to anchor:** specific classroom or research moments (a question they
  asked, a problem they cracked, how they responded to a setback), and an explicit
  **comparison to the cohort the recommender has taught** ("among the strongest in
  a 60-student methods course").
- **Skeleton:**
  1. Relationship + basis (course(s) taught, project supervised, duration).
  2. Intellectual ability — one anchored example.
  3. Research aptitude / independence — one anchored example.
  4. Personal qualities relevant to graduate study (persistence, collegiality).
  5. Calibrated ranking against the recommender's own students.
  6. Clear recommendation + offer to elaborate.

## 2. Faculty hiring (`faculty-hiring`)

- **Reader:** a search committee and department evaluating a **future colleague**.
- **Decision:** shortlist / interview / offer.
- **Register:** peer assessment. The candidate is (or is becoming) an independent
  scholar; the letter assesses a **research program**, not just talent.
- **What to anchor:** evidence of **independence** from the advisor, the shape and
  significance of the research program, teaching capacity, and collegiality.
  Position the work within the subfield.
- **Skeleton:**
  1. Relationship + standing to assess (how the recommender knows the work).
  2. Research program — its problem, originality, and trajectory.
  3. Independence and scholarly identity distinct from mentors/collaborators.
  4. Teaching and mentoring (if known).
  5. Collegiality / fit with a department.
  6. Overall placement in the subfield + recommendation.

## 3. Tenure / promotion external review (`tenure-external`)

- **Reader:** a Promotion & Tenure committee plus deans/provost weighing a
  **permanent, high-stakes** decision; frequently the letter is solicited *because*
  the writer is an arms-length expert in the field.
- **Decision:** tenure / promotion (or not).
- **Register:** **evaluation, not advocacy.** This is the critical distinction. The
  committee asks the writer to *judge* the candidate's record and standing — often
  with the standard prompt *"would this candidate receive tenure at your
  institution?"* A letter that only praises is read as uninformative or evasive.
- **What to anchor:** the **impact and significance** of the body of work (not a
  publication count), the candidate's **standing in the field**, and — where the
  request asks for it — a **comparison against named peers at the same career
  stage**. State the basis for the comparison.
- **Constraints to respect:** many institutions specify arms-length (no close
  collaborators, no advisor); the letter should state the nature of the
  relationship plainly and disclose any conflict. Do **not** invent a comparison
  set or a standing claim the writer cannot support.
- **Skeleton:**
  1. Relationship + disclosure of any conflict; basis for the assessment.
  2. The research contribution — what is the central, lasting work and why it
     matters to the field.
  3. Impact and influence (how the field uses the work; venues; trajectory).
  4. Standing relative to peers at the same stage (comparative, if asked).
  5. Direct answer to the institution's evaluation question.

## 4. Fellowship (`fellowship`)

- **Reader:** a competitive selection panel choosing among strong applicants for a
  named award/fellowship.
- **Decision:** award / decline.
- **Register:** grounded advocacy emphasizing **distinctiveness**. The pool is
  strong by construction, so the letter must answer *why this candidate and why
  this award.*
- **What to anchor:** the candidate's defining strength and how it maps to the
  fellowship's stated criteria/mission; one or two vivid, specific accomplishments.
- **Skeleton:**
  1. Relationship + enthusiasm framed against the competitive pool.
  2. The distinctive strength — anchored.
  3. Fit to the fellowship's specific aims/criteria.
  4. Evidence of the trajectory the fellowship is meant to accelerate.
  5. Strong, specific recommendation.

## 5. Award nomination (`award-nomination`)

- **Reader:** an awards committee citing a specific achievement.
- **Decision:** confer the award.
- **Register:** citation-style; tighter and more focused than the other types.
- **What to anchor:** the **single defining contribution** and its significance —
  the "citation" the award would carry.
- **Skeleton:**
  1. The nomination statement (who, for what award).
  2. The defining contribution — precise and anchored.
  3. Its significance / why it merits this award.
  4. Brief supporting context (standing, breadth) if the award asks for it.

---

## Length and format norms

- Admission and fellowship letters typically run **1–2 pages**.
- Faculty-hiring and external-review letters often run **2–4 pages** and are more
  evaluative.
- Award nominations are usually the shortest, sometimes a single page.
- Always honor an explicit length or format instruction from the requesting body
  over these defaults; surface the instruction if the user supplied one.

These norms are conventions, not hard rules — when the requesting institution
states its own length, scope, or required prompts, those override the table above.

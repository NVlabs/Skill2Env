---
name: alterlab-recommendation-letters
description: "Drafts evidence-anchored academic reference and recommendation letters across types — graduate admission, faculty hiring, tenure/promotion external review, fellowship, and award nomination — from a structured prompt of candidate accomplishments, role context, evaluator relationship, and audience, calibrating specificity and register to the letter type and running a no-fabrication guard that flags unsupported superlatives, unanchored rankings, and claims with no evidence in the supplied dossier. Ships scripts/letter_scaffold.py to emit a typed section skeleton and scripts/claim_guard.py to lint a draft for evidence-free assertions. Use when the request is to write a recommendation or reference letter for a student or colleague, a tenure or promotion external-review letter, a fellowship or award nomination, or to check a letter draft for unsupported claims. For a candidate writing their own CV, research statement, or career narrative prefer alterlab-academic-career. Part of the AlterLab Academic Skills suite."
license: MIT
allowed-tools: Read Write Edit Bash(python:*) Bash
compatibility: No API key, account, or network required — generates letters from the supplied dossier via the Read/Write/Edit tools plus two stdlib-only helpers (scripts/letter_scaffold.py, scripts/claim_guard.py) run through `uv run python`. The recommender always reviews, signs, and submits the final letter themselves.
metadata:
  skill-author: AlterLab
  version: "1.0.0"
  last_updated: "2026-06-06"
  depends_on: "alterlab-academic-career (owns the candidate's OWN CV/statements; this skill writes ABOUT a candidate for a third party)"
---

# Recommendation Letters — Evidence-Anchored References Written *About* a Candidate

The faculty task this skill owns is writing **about someone else**: the letter a
professor sends to an admissions committee, a hiring chair, a tenure case, or a
fellowship panel. It is the mirror image of `alterlab-academic-career`, which
helps the *candidate* write their own CV and statements. Here the author is the
**recommender**, the subject is a third party, and the failure mode is not
modesty but **fabrication** — the warm letter full of superlatives that an
evaluator cannot act on because nothing is anchored to evidence.

This skill turns a structured dossier (what the recommender actually knows) into
a letter whose every strong claim is **earned by a specific, checkable
example**, with specificity and register **calibrated to the letter type**.

## When to Use This Skill

Use this skill when the request is to **draft, revise, or evidence-check a letter
written about a candidate by a recommender**:

- "Write a recommendation letter for my PhD student applying to postdocs."
- "I'm a reference for a colleague's faculty application — draft the letter."
- "I've been asked for an external review letter for X's tenure case."
- "Draft a fellowship / award nomination for my mentee."
- "Here's my draft letter — flag anything I claim without backing it up."
- "Make this reference letter more specific; it reads like boilerplate."

The skill always treats the recommender as the author of record: it produces a
**draft for them to verify, edit, sign, and submit**, never a letter it claims to
send or to vouch for on its own authority.

### Does NOT Trigger

| The request is really… | Route to | Why |
|---|---|---|
| The candidate's **own** CV, research/teaching statement, cover letter, tenure dossier, promotion narrative | `alterlab-academic-career` | Self-authored career documents, not a third party writing *about* the candidate |
| A **peer-review report** judging a manuscript's quality with an accept/revise/reject verdict | `alterlab-peer-review` | Editorial quality judgment of a paper, not a personal reference for a person |
| A **structured peer review of a full manuscript** (core-pipeline reviewer) | `alterlab-paper-reviewer` | Section-by-section manuscript critique, not a recommendation about a candidate |
| **Türkiye doçentlik** eligibility / point computation for an associate-professor case | `alterlab-docentlik-eligibility` | ÜAK criteria scoring, not a prose reference letter |
| **Academic-incentive (akademik teşvik)** point computation | `alterlab-akademik-tesvik` | YÖK incentive points, not a letter |
| Checking that the **citations** in a letter or dossier actually exist | `alterlab-citation-verifier` | Bibliographic existence verification, not letter-claim evidence-anchoring |
| Designing a **course, rubric, or syllabus** for the student | `alterlab-teaching-design` | Course/instructional design, not a reference about the student |
| Writing a **grant proposal** or **post-award report** | `alterlab-research-grants` / `alterlab-grant-reporting` | Funding documents, not personal references |

If the candidate is writing about *themselves*, stop and hand off to
`alterlab-academic-career`. The two skills are deliberately disjoint.

---

## The Five Letter Types (calibration table)

Each type has a different **reader**, **decision**, and **register**. The scaffold
script keys off this taxonomy. Full per-type guidance, openings, and worked
structure live in `references/letter_types.md`.

| Type | Reader / decision | Calibration |
|---|---|---|
| **Graduate admission** | Admissions committee deciding fit for a program | Potential + trajectory; compare against the cohort the recommender has taught; concrete classroom/research moments |
| **Faculty hiring** | Search committee / department deciding a colleague | Independence, research program, collegiality, teaching; position within the subfield |
| **Tenure / promotion external review** | P&T committee + administration weighing a permanent decision | Arms-length, evaluative, often **comparative against named peers** at career stage; assess impact and standing, *not* advocacy |
| **Fellowship** | Selection panel awarding a competitive named award | Distinctiveness vs a strong applicant pool; why *this* candidate, *this* award |
| **Award nomination** | Awards committee citing achievement | Citation-style; the single defining contribution and its significance |

The external-review letter is the one most often miswritten as an advocacy
letter. It is **not**: tenure reviewers are asked to *evaluate*, and a letter that
only praises reads as uninformative. `references/letter_types.md` spells out the
register shift and the standard "would this person get tenure here?" prompt.

---

## The Core Discipline: Evidence-Anchored Claims

Every adjective must be **cashed out by a specific example**. The pattern:

> **Claim → Evidence → Significance.**
> *"She is an unusually independent researcher"* (claim) *"— in her second year
> she reframed the project after a null result, designed the follow-up assay
> herself, and that pivot became the paper's central finding"* (evidence) *"—
> work I would expect from a senior postdoc, not a second-year student"*
> (significance / calibration).

A claim with no evidence in the dossier is the single most common defect. The
**no-fabrication guard** (`scripts/claim_guard.py`) lints a draft for exactly
this: unsupported superlatives ("the best student I have ever had"), unanchored
rankings ("top 1%"), and evaluative adjectives that no nearby sentence backs with
a concrete instance. It **does not invent** the missing evidence — it flags the
claim and asks the recommender to supply the example or soften the claim.

**Calibrated specificity** is the companion rule: superlatives and rankings are
*allowed and valuable* — but only when the recommender can ground them ("top 2 of
the ~40 PhD students I have advised in 18 years"). An ungrounded "top 1%" is
weaker than a grounded "the strongest of the six students in this year's lab."
See `references/evidence_and_specificity.md` for the claim taxonomy, the ranking
grammar, and the rhetoric of comparison.

### Hard rule — zero fabrication

This skill writes **only** from the supplied dossier. It must never:

- invent achievements, metrics, rankings, dates, or anecdotes the recommender did
  not provide;
- assert a comparison ("top 5%") the recommender did not make;
- manufacture a relationship detail (how long / in what capacity they were known).

When the dossier is thin, the correct output is **a draft with bracketed gaps**
(`[recommender: a specific example of independence here]`) plus a short list of
the facts the recommender must supply — not a fluent letter that papers over the
holes with plausible fiction. A letter is a signed personal attestation; inventing
its content is a research-integrity problem, not a style choice.

---

## Workflow

### 1. Collect the dossier (structured intake)

Ask for, or extract from what was provided: **letter type**; **candidate name +
role**; **target** (program/position/award + institution); **relationship**
(capacity and duration the recommender knew the candidate); the candidate's
**accomplishments** (with any metrics, artifacts, anecdotes); **the specific
qualities** the target asks to be addressed; and **deadline / length norms**.
`references/intake_checklist.md` is the full prompt list; missing fields become
bracketed gaps, never invented content.

### 2. Scaffold the letter

```bash
uv run python skills/faculty-life/alterlab-recommendation-letters/scripts/letter_scaffold.py \
    --type tenure-external \
    --candidate "Dr. A. Yılmaz" \
    --relationship "external reviewer; known through the field since 2016" \
    --out letter_skeleton.md
```

The scaffold emits a **type-appropriate section skeleton** — opening that states
the relationship and basis for assessment, body sections matched to the type's
evaluation dimensions (e.g. independence/impact/standing for external review;
potential/trajectory/fit for admission), and a calibrated closing. Each section
carries an inline reminder of the *Claim → Evidence → Significance* pattern. Pass
`--list-types` to see the five supported types. The script is stdlib-only.

### 3. Draft from the dossier

Fill each section using only dossier facts. Lead every evaluative claim with the
specific example that earns it. Match the register to the type (advocacy for
admission/fellowship; arms-length evaluation for external review).

### 4. Run the no-fabrication guard

```bash
uv run python skills/faculty-life/alterlab-recommendation-letters/scripts/claim_guard.py \
    letter_draft.md --json
```

It returns each flagged sentence with a reason (`unsupported-superlative`,
`unanchored-ranking`, `evidence-free-claim`) and a fix prompt. Resolve every flag
by **adding the recommender's evidence or softening the claim** — never by
inventing support. Re-run until clean (exit 0).

### 5. Final review hand-off

Present the draft plus: the list of bracketed gaps the recommender must fill, the
guard's residual flags, and a one-line reminder that the recommender must verify
every factual claim and sign/submit it themselves.

---

## Self-Check Before Returning a Letter

- **Every superlative earned?** Each "best/strongest/exceptional" is followed by a
  concrete, dossier-sourced instance — or it is bracketed for the recommender.
- **No invented facts.** Nothing in the letter — metric, ranking, anecdote, date —
  is absent from the supplied dossier.
- **Register matches type.** External-review reads as evaluation, not cheerleading;
  admission/fellowship reads as grounded advocacy.
- **Relationship stated up front.** The opening makes the basis for the assessment
  explicit (how, how long, in what capacity).
- **Gaps surfaced, not filled.** Thin areas appear as bracketed asks, not fiction.
- **Right skill?** A self-authored career document belongs to
  `alterlab-academic-career`; hand it off.

---

## References

- `references/letter_types.md` — per-type readers, openings, structure, and the
  external-review register shift.
- `references/evidence_and_specificity.md` — Claim → Evidence → Significance,
  the claim taxonomy, ranking grammar, and comparison rhetoric.
- `references/intake_checklist.md` — the structured dossier intake prompt and how
  thin fields become bracketed gaps.

Part of the AlterLab Academic Skills suite.

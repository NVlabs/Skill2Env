---
name: alterlab-thesis-supervisor
description: "Supervises theses and dissertations end to end — structure guidance from proposal through defense, chapter-by-chapter writing support (introduction, literature review, methodology, results, discussion), supervision strategies, committee management, defense and viva voce preparation, timeline planning, feedback integration, examiner-expectation guidance, and formatting (APA 7, Chicago, university styles). Use when the request mentions thesis, dissertation, supervision, defense preparation, viva, proposal defense, thesis structure, thesis chapter, literature review chapter, methodology chapter, results chapter, discussion chapter, thesis timeline, committee, thesis formatting, or dissertation proposal. Part of the AlterLab Academic Skills suite."
license: MIT
allowed-tools: Read Write Edit WebFetch WebSearch
compatibility: Uses built-in Claude tools only (Read/Write/Edit/WebFetch/WebSearch); no external API key or account required
metadata:
  skill-author: AlterLab
  version: "1.0.0"
  last_updated: "2026-03-18"
---

# Thesis Supervisor — Dissertation & Thesis Supervision Agent

A comprehensive thesis and dissertation supervision tool for faculty advisors and graduate students. Covers the full dissertation lifecycle from initial topic selection through successful defense, providing chapter-by-chapter guidance, supervision strategies, timeline management, and defense preparation.

## Overview

Supervising a thesis or dissertation is one of the most complex and consequential activities in academic life. This skill supports both supervisors and students through every stage of the process: defining a viable research question, structuring a proposal, writing each chapter to disciplinary standards, preparing for committee meetings and defenses, and navigating the human dimensions of the supervisory relationship.

The skill is designed to be discipline-flexible, with examples drawn from social sciences, humanities, STEM, and professional fields. Formatting guidance covers APA 7, Chicago/Turabian, and generic university styles.

## When to Use This Skill

This skill should be used when:
- Beginning thesis/dissertation topic exploration
- Writing a research proposal for committee approval
- Structuring any chapter of a thesis or dissertation
- Preparing for a proposal defense or final defense (viva voce)
- Managing the supervisor-student relationship
- Creating or adjusting a thesis timeline
- Giving feedback on student drafts
- Preparing students for committee meetings
- Troubleshooting common thesis problems (writer's block, scope creep, data issues)
- Teaching thesis writing seminars or workshops

### Does NOT Trigger

| Scenario | Use Instead |
|----------|-------------|
| Writing a journal article (not thesis) | `alterlab-paper-writer` |
| Statistical analysis of thesis data | Data science skills |
| Literature search strategy | `alterlab-deep-research` |
| Survey/instrument design for thesis | `alterlab-survey-design` |

---

## Core Capabilities

### 1. Dissertation Structure Overview

**Standard Five-Chapter Model (Social Sciences, Education, Business):**

```
PROPOSAL (Chapters 1-3)
│
├── Chapter 1: Introduction
│   ├── Background and context
│   ├── Problem statement
│   ├── Purpose of the study
│   ├── Research questions (and hypotheses, if applicable)
│   ├── Significance of the study
│   ├── Scope and delimitations
│   ├── Definition of key terms
│   └── Organization of the dissertation
│
├── Chapter 2: Literature Review
│   ├── Introduction and search strategy
│   ├── Theoretical/conceptual framework
│   ├── Thematic review of literature
│   ├── Synthesis and identification of gaps
│   └── Summary and connection to research questions
│
├── Chapter 3: Methodology
│   ├── Research design and rationale
│   ├── Setting and context
│   ├── Population and sample
│   ├── Data collection methods and instruments
│   ├── Data analysis procedures
│   ├── Trustworthiness/validity and reliability
│   ├── Ethical considerations
│   ├── Researcher positionality (qualitative)
│   └── Limitations
│
COMPLETED AFTER DATA COLLECTION (Chapters 4-5)
│
├── Chapter 4: Results/Findings
│   ├── Data screening and preparation
│   ├── Participant/sample description
│   ├── Results organized by research question
│   ├── Tables and figures
│   └── Summary of findings
│
└── Chapter 5: Discussion and Conclusions
    ├── Summary of the study
    ├── Discussion of findings (connected to literature)
    ├── Implications (theoretical, practical, policy)
    ├── Limitations
    ├── Recommendations for future research
    └── Conclusion
```

**Alternative Structures by Discipline:**

| Discipline | Structure | Notes |
|-----------|-----------|-------|
| Social Sciences | 5-chapter model (above) | Most common for EdD, PhD in education, psychology, management |
| STEM (experimental) | Introduction, Literature Review, Methods, Results, Discussion (IMRaD variant) | May include multiple studies as separate chapters |
| Humanities | Introduction, literature/theory chapters (2-4), analysis chapters (2-4), conclusion | More flexible; argument-driven rather than question-driven |
| Three-paper model | Introduction, Paper 1, Paper 2, Paper 3, Conclusion | Each paper is publishable; increasingly popular in STEM and social sciences |
| Practice-based (professional doctorate) | Introduction, Literature Review, Methods, Findings, Action Plan/Recommendations | Emphasis on practical application |
| Creative arts | Creative work + exegesis (critical reflection) | Varies widely by institution |

### 2. Chapter-by-Chapter Guidance

Each chapter has a detailed, section-by-section writing template — purpose statement, section guide, quality checklists, common-mistake tables, and presentation guidelines:

- **Chapter 1: Introduction** — background, problem statement, purpose, research questions, significance, delimitations, key terms
- **Chapter 2: Literature Review** — theoretical/conceptual framework, thematic review architecture, gap synthesis, quality checklist
- **Chapter 3: Methodology** — design and rationale, sampling, instrumentation, data collection, analysis, trustworthiness, ethics
- **Chapter 4: Results/Findings** — data preparation, results organized by research question, quant vs. qual presentation guidelines
- **Chapter 5: Discussion and Conclusions** — findings interpretation, theoretical/practical/methodological implications, limitations, future research

Full chapter-by-chapter writing templates and checklists: see `references/chapter_writing_guides.md`.

### 3. Thesis Timeline Planning

**Typical PhD Timeline (4-6 years, social sciences):**

```
Year 1: Coursework + Topic Exploration
├── Semester 1: Core courses; identify broad area of interest
├── Semester 2: Methods courses; narrow topic; identify advisor
└── Summer: Preliminary literature review; draft topic statement

Year 2: Coursework + Proposal Development
├── Semester 1: Advanced courses; comprehensive/qualifying exams
├── Semester 2: Draft Chapters 1-3 (proposal)
└── Summer: Revise proposal; IRB application

Year 3: Proposal Defense + Data Collection
├── Semester 1: Proposal defense; begin data collection
├── Semester 2: Continue/complete data collection
└── Summer: Begin data analysis

Year 4: Analysis + Writing
├── Semester 1: Complete analysis; draft Chapter 4
├── Semester 2: Draft Chapter 5; revise all chapters
└── Summer: Defense preparation; submit to committee
```

**Master's Thesis Timeline (1-2 years):**

```
Semester 1
├── Month 1-2: Topic selection, advisor match, literature review begins
├── Month 3: Draft proposal outline; committee formation
└── Month 4: Proposal defense (or approval by advisor)

Semester 2
├── Month 5: IRB submission (if needed); data collection begins
├── Month 6-7: Data collection; begin analysis
└── Month 8: Complete analysis; draft results

Semester 3 (or end of Semester 2)
├── Month 9-10: Complete full draft; advisor review
├── Month 11: Revisions based on feedback; submit to committee
└── Month 12: Defense; final revisions; submit to graduate school
```

**Thesis Milestone Tracker:**

```markdown
## Thesis Timeline: [Student Name]

| Milestone | Target Date | Actual Date | Status | Notes |
|-----------|------------|-------------|--------|-------|
| Topic approved by advisor | [Date] | | [ ] | |
| Committee formed | [Date] | | [ ] | |
| Chapter 1 draft to advisor | [Date] | | [ ] | |
| Chapter 2 draft to advisor | [Date] | | [ ] | |
| Chapter 3 draft to advisor | [Date] | | [ ] | |
| Proposal to committee | [Date] | | [ ] | 2 weeks before defense |
| Proposal defense | [Date] | | [ ] | |
| IRB approval | [Date] | | [ ] | |
| Data collection complete | [Date] | | [ ] | |
| Chapter 4 draft to advisor | [Date] | | [ ] | |
| Chapter 5 draft to advisor | [Date] | | [ ] | |
| Full draft to committee | [Date] | | [ ] | 4 weeks before defense |
| Final defense | [Date] | | [ ] | |
| Revisions complete | [Date] | | [ ] | |
| Submit to graduate school | [Date] | | [ ] | Check formatting deadlines |
| Graduation | [Date] | | [ ] | |
```

### 4. Supervision Strategies

**Supervisory Meeting Structure:**

```markdown
## Meeting Agenda Template

### Pre-Meeting (Student Prepares)
- [ ] Submit written work 48+ hours before meeting
- [ ] Prepare 2-3 specific questions or decision points
- [ ] Update progress log since last meeting
- [ ] List any obstacles or concerns

### During Meeting (30-60 minutes)
1. Check-in (5 min): How are you doing? Any concerns?
2. Progress review (10 min): What has been accomplished since last meeting?
3. Discussion of submitted work (20-30 min): Feedback, questions, direction
4. Next steps (10 min): Clear action items with deadlines
5. Next meeting date confirmed

### Post-Meeting (Student Documents)
- [ ] Written summary of decisions and action items
- [ ] Shared with supervisor within 24 hours
- [ ] Filed in shared thesis folder
```

**Feedback Strategies for Supervisors:**

| Level of Draft | Feedback Focus | Approach |
|---------------|---------------|----------|
| Outline | Structure, logic, scope | "Is this the right story to tell?" Focus on architecture, not sentences. |
| First draft | Argument, evidence, gaps | "Does the argument work?" Focus on content and organization. Do NOT line-edit. |
| Second draft | Clarity, coherence, depth | "Is this clear and convincing?" Address paragraph-level issues. |
| Near-final draft | Polish, formatting, citations | "Is this ready for the committee?" Line-level editing now appropriate. |

**Difficult Supervision Conversations:**

| Situation | Approach |
|-----------|----------|
| Student is not making progress | "I've noticed that [specific observation]. What's getting in the way? How can I help?" |
| Draft quality is very poor | Focus on the most important 2-3 issues; do not overwhelm with a red ocean of tracked changes |
| Student wants to change topic mid-stream | Explore reasons; assess feasibility; help weigh costs vs. benefits; document the decision |
| Student disagrees with feedback | "Help me understand your reasoning. Let's look at what the literature says." |
| Student is struggling emotionally | Express concern; refer to counseling services; adjust timeline if needed; distinguish pastoral from academic role |
| Student is ready to defend but lacks confidence | Mock defense; emphasize strengths; normalize nervousness; remind them they are the world expert on their study |

### 5. Defense Preparation

Covers both defense milestones:

- **Proposal Defense** — a document readiness checklist, a 16-slide presentation plan (15-20 minute talk), and the eight most common proposal-defense questions.
- **Final Defense (Viva Voce)** — a four-to-six-week week-by-week preparation protocol (re-read, anticipate, practice, polish) and a categorized bank of common viva questions (opening, theoretical, methodology, findings, broader, closing).

Full defense checklists, slide plans, and question banks: see `references/defense_preparation.md`.

### 6. Formatting Requirements

Detailed, style-by-style checklists cover the two dominant dissertation styles:

- **APA 7** — page layout, the five heading levels, table and figure formatting, in-text citation rules, and reference-list conventions.
- **Chicago/Turabian** — the two citation systems (notes-bibliography vs. author-date), worked citation examples, and formatting/spacing conventions.

Full APA 7 and Chicago/Turabian formatting checklists: see `references/formatting_guides.md`.

---

## Best Practices

1. **Establish expectations early.** At the first meeting, discuss communication frequency, feedback turnaround times, draft submission expectations, and working styles. Put it in writing.

2. **Require written work at every meeting.** Meetings without written deliverables become unproductive check-ins. Even a one-page outline moves the thesis forward more than a conversation.

3. **Give feedback at the right level for the right stage.** Do not copy-edit a first draft. Do not give structural feedback on a near-final draft. Match your feedback to the draft's maturity.

4. **Protect the student's ownership.** The thesis is the student's work, not yours. Guide and challenge, but do not dictate. The student must be able to defend every decision in the viva.

5. **Front-load the methodology.** The methodology chapter is where most students struggle and most proposals fail. Invest disproportionate time getting Chapter 3 right before data collection.

6. **Build in buffer time.** Every thesis timeline should include contingency time for illness, data collection delays, committee scheduling, and revision cycles. Add 20-30% to estimated timelines.

7. **Normalize difficulty.** Writing a thesis is hard. Periods of frustration, confusion, and self-doubt are normal. Acknowledge this and help students develop coping strategies.

8. **Connect chapters with threads.** Each chapter should explicitly link to the research questions and to adjacent chapters. The thesis is one coherent argument, not five separate papers.

9. **Practice the defense.** No student should walk into a defense without at least one mock defense. Practice reduces anxiety and reveals gaps in argumentation.

10. **Celebrate milestones.** Acknowledge completed chapters, successful proposal defenses, and the final defense. The journey is long; recognition sustains motivation.

---

## Common Pitfalls

| Pitfall | Why It Happens | How to Avoid |
|---------|---------------|--------------|
| Scope creep | Student keeps adding research questions or variables | Lock research questions at proposal defense; resist expansion |
| Literature review never ends | Student keeps finding new sources | Set a deadline; focus on saturation of key themes, not exhaustiveness |
| Methods chapter too vague | Student has not yet grasped the details of their chosen approach | Require students to work through a methods textbook chapter-by-chapter |
| Results chapter interprets findings | Student mixes results with discussion | Enforce the rule: Chapter 4 reports what you found; Chapter 5 says what it means |
| Discussion chapter re-summarizes results | Student does not know how to interpret | Require explicit connection to literature for every major finding |
| Inconsistent formatting | Student writes over months/years with changing habits | Use a template from day one; format check before each submission |
| Committee surprises at defense | Committee members have not read the full document | Send the complete document 4+ weeks in advance; follow up to confirm receipt |
| Student disappears | Life events, mental health, loss of motivation | Regular scheduled meetings (even brief); early intervention when pattern breaks |
| Advisor rewrites instead of guides | Frustration with slow progress | Ask questions instead of providing answers; use margin comments, not rewriting |
| Timeline pressure leads to poor work | External deadlines (funding, visa, job) | Plan realistically from the start; discuss timeline pressures openly |

---

## References

- Bolker, J. (1998). *Writing your dissertation in fifteen minutes a day: A guide to starting, revising, and finishing your doctoral thesis*. Holt.
- Dunleavy, P. (2003). *Authoring a PhD: How to plan, draft, write, and finish a doctoral thesis or dissertation*. Palgrave Macmillan.
- Murray, R. (2011). *How to write a thesis* (3rd ed.). Open University Press.
- Paltridge, B., & Starfield, S. (2020). *Thesis and dissertation writing in a second language: A handbook for students and their supervisors* (2nd ed.). Routledge.
- Roberts, C. M. (2010). *The dissertation journey: A practical and comprehensive guide to planning, writing, and defending your dissertation* (2nd ed.). Corwin.
- Turabian, K. L. (2018). *A manual for writers of research papers, theses, and dissertations* (9th ed.). University of Chicago Press.
- Wisker, G. (2012). *The good supervisor: Supervising postgraduate and undergraduate research for doctoral theses and dissertations* (2nd ed.). Palgrave Macmillan.

See also: `references/thesis-guidelines.md` for expanded formatting and process details.

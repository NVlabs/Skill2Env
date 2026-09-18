---
name: alterlab-research-grants
description: Writes competitive research grant proposals for NSF, NIH, DOE, DARPA, and Taiwan NSTC — applies agency-specific formatting and review criteria, prepares budgets, and drafts broader-impacts, significance statements, and innovation narratives that comply with submission requirements. Use when drafting or revising a grant proposal, aligning a proposal to a funding agency's review criteria, or preparing grant budgets and compliance sections. For Turkey's TÜBİTAK 1001/1002-A national proposals use alterlab-tubitak-proposal; to write a reviewer's critique of someone else's proposal use alterlab-peer-review; for a journal manuscript use alterlab-scientific-writing. Part of the AlterLab Academic Skills suite.
allowed-tools: Read Write Edit Bash
license: MIT
compatibility: No external tools, API keys, or services required — ships no helper scripts and works from the Read/Write/Edit/Bash tools alone
metadata:
    skill-author: AlterLab
    version: "1.0.0"
---

# Research Grant Writing

## Overview

Research grant writing is the process of developing competitive funding proposals for federal agencies and foundations. Master agency-specific requirements, review criteria, narrative structure, budget preparation, and compliance for NSF (National Science Foundation), NIH (National Institutes of Health), DOE (Department of Energy), DARPA (Defense Advanced Research Projects Agency), and Taiwan's NSTC (National Science and Technology Council) submissions.

**Critical Principle: Grants are persuasive documents that must simultaneously demonstrate scientific rigor, innovation, feasibility, and broader impact.** Each agency has distinct priorities, review criteria, formatting requirements, and strategic goals that must be addressed.

## When to Use This Skill

This skill should be used when:
- Writing research proposals for NSF, NIH, DOE, DARPA, or NSTC programs
- Preparing project descriptions, specific aims, or technical narratives
- Developing broader impacts or significance statements
- Creating research timelines and milestone plans
- Preparing budget justifications and personnel allocation plans
- Responding to program solicitations or funding announcements
- Addressing reviewer comments in resubmissions
- Planning multi-institutional collaborative proposals
- Writing preliminary data or feasibility sections
- Preparing biosketches, CVs, or facilities descriptions

## Visual Communication in Proposals

Well-chosen figures strengthen a proposal: a Gantt chart clarifies the timeline, a conceptual framework orients reviewers, and a workflow diagram makes methodology legible at a glance. Figures are optional — add them only where they genuinely improve clarity, and never pad a proposal with decorative graphics.

If a diagram or figure would aid comprehension, invoke the **alterlab-scientific-schematics** skill (diagrams/schematics) or the **alterlab-generate-image** skill (images). Figures are optional — add them only where they improve clarity.

**Where figures typically earn their space in a proposal:**
- Research methodology and workflow diagrams
- Project timeline Gantt charts
- Conceptual framework illustrations
- System architecture diagrams (for technical proposals)
- Experimental design flowcharts
- Preliminary data visualizations

---

## Agency Profiles (at a glance)

| Agency | Core structure | Primary review focus |
|--------|----------------|----------------------|
| **NSF** | 15-page project description; 1-page project summary | Intellectual Merit + Broader Impacts (equal weight) |
| **NIH** | 1-page Specific Aims + 12-page Research Strategy (R01) | Significance, Investigators, Innovation, Approach, Environment |
| **DOE** | Project narrative; often cost-sharing | Technical merit, mission relevance, often national-lab collaboration |
| **DARPA** | Technical volume by phase; BAA-driven | DARPA-hard impact (Heilmeier Catechism), transition paths |
| **NSTC (Taiwan)** | CM03 form; bilingual abstract; architecture diagram | Innovation, Feasibility, PI Capability, Value |

Full agency profiles, complete review criteria, and award-mechanism catalogs (NSF CAREER/RAPID/EAGER;
NIH R01/R21/R35/F-series/K-series; DOE Office of Science/ARPA-E/EERE; DARPA YFA/offices) are in
`references/agency_profiles.md`. For binding requirements and formatting, use the per-agency guides:
`references/nsf_guidelines.md`, `references/nih_guidelines.md`, `references/doe_guidelines.md`,
`references/darpa_guidelines.md`, `references/nstc_guidelines.md`.

## Core Components of a Proposal

A competitive proposal assembles these ten components. Detailed purpose, length, essential elements,
and writing strategy for each — plus discipline-specific method guidance — are in
`references/proposal_components.md`.

1. **Executive Summary / Abstract** — standalone hook + significance + approach + impact.
2. **Project Description / Research Strategy** — the core technical narrative (structure varies by agency).
3. **Specific Aims / Objectives** — 2-4 testable, complementary goals (see `references/specific_aims_guide.md`).
4. **Broader Impacts / Significance** — societal/educational value; NSF weights this equally (see `references/broader_impacts.md`).
5. **Innovation** — conceptual, methodological, integrative, translational, or scale novelty.
6. **Approach and Methods** — design, power, analysis, alternatives, rigor (see `references/research_methods.md`).
7. **Preliminary Data and Feasibility** — proof-of-concept that de-risks the proposal.
8. **Timeline, Milestones, Management** — phased plan with go/no-go points (see `references/timeline_planning.md`).
9. **Team Qualifications and Collaboration** — expertise, roles, biosketches, letters (see `references/team_building.md`).
10. **Budget and Justification** — categories, agency rules, line-item justification (see `references/budget_preparation.md`).

## Writing Craft, Mistakes, Resubmission, and Workflow

These cross-cutting topics are consolidated in `references/writing_and_workflow.md`:

- **Writing principles** — write for multiple audiences; the hook→problem→solution→evidence→impact→team
  persuasion arc; active voice and precise language; figure design; balancing innovation against risk;
  internal coherence (budget/timeline/team/aims must align).
- **Common mistakes** — conceptual, writing, technical, formatting, and strategic pitfalls to avoid.
- **Resubmission strategies** — NIH A1 introduction and NSF revision (see `references/resubmission_strategies.md`).
- **5-phase development workflow** — planning (2-6 mo out) → drafting → internal review → finalization →
  submission (submit 24-48 h early; never wait for the deadline).

## Reference Files

Load these as needed; the body above already cites each one at its point of use.

- `references/agency_profiles.md` — agency profiles, review criteria, award-mechanism catalogs (NSF/NIH/DOE/DARPA/NSTC)
- `references/proposal_components.md` — the ten core proposal components, with discipline-specific method guidance
- `references/writing_and_workflow.md` — writing principles, common mistakes, and the 5-phase development workflow
- Per-agency guides — `references/nsf_guidelines.md`, `nih_guidelines.md`, `doe_guidelines.md`, `darpa_guidelines.md`, `nstc_guidelines.md`
- Component deep-dives — `references/broader_impacts.md`, `specific_aims_guide.md`, `research_methods.md`, `budget_preparation.md`, `timeline_planning.md`, `team_building.md`, `resubmission_strategies.md`

## Templates and Assets

- `assets/nsf_project_summary_template.md`: NSF project summary structure
- `assets/nih_specific_aims_template.md`: NIH specific aims page template
- `assets/budget_justification_template.md`: Budget justification structure
- Agency-specific biosketch formats: see the per-agency guides in `references/` (`nsf_guidelines.md`, `nih_guidelines.md`, `doe_guidelines.md`, `darpa_guidelines.md`, `nstc_guidelines.md`) and `references/team_building.md`.

## Tasks and Tools

This skill ships no helper scripts; handle these tasks directly:

- **Compliance checking**: Verify formatting requirements (page limits, margins, fonts, required sections) against the relevant agency guide in `references/` (e.g. `references/nsf_guidelines.md`, `references/nih_guidelines.md`).
- **Budget calculation**: Build budgets with inflation escalation and fringe rates following `references/budget_preparation.md` and the `assets/budget_justification_template.md` structure.
- **Deadline tracking**: Track submission deadlines and milestones using the timeline/Gantt guidance in `references/timeline_planning.md`.

---

**Final Note**: Grant writing is both an art and a science. Success requires not only excellent research ideas but also clear communication, strategic positioning, and meticulous attention to detail. Start early, seek feedback, and remember that even the best researchers face rejection—persistence and revision are key to funding success.



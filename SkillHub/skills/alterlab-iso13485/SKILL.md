---
name: alterlab-iso13485
description: Prepares ISO 13485 certification documentation for medical device Quality Management Systems (QMS) — gap analysis of existing documentation, Quality Manuals, required procedures and work instructions, and Medical Device Files. Use for ISO 13485 QMS documentation, conducting a documentation gap analysis, drafting a Quality Manual or SOP/work instruction, assembling a Medical Device File, identifying missing documentation for medical device certification, or when medical device regulations, QMS certification, FDA QMSR, or EU MDR are mentioned. Part of the AlterLab Academic Skills suite.
license: MIT
allowed-tools: Read Write Edit Bash(python:*)
compatibility: "Self-contained — runs with Read/Write/Edit/Bash(python:*); no API key or account required."
metadata:
    skill-author: AlterLab
    version: "1.0.0"
---

# ISO 13485 Certification Documentation Assistant

## Overview

This skill helps medical device manufacturers prepare comprehensive documentation for ISO 13485:2016 certification. It provides tools, templates, references, and guidance to create, review, and gap-analyze all required Quality Management System (QMS) documentation.

**What this skill provides:**
- Gap analysis of existing documentation
- Templates for all mandatory documents
- Comprehensive requirements guidance
- Step-by-step documentation creation
- Identification of missing documentation
- Compliance checklists

**When to use this skill:**
- Starting ISO 13485 certification process
- Conducting gap analysis against ISO 13485
- Creating or updating QMS documentation
- Preparing for certification audit
- Transitioning from FDA QSR to QMSR
- Harmonizing with EU MDR requirements

## Core Workflow

### 1. Assess Current State (Gap Analysis)

**When to start here:** User has existing documentation and needs to identify gaps

**Process:**

1. **Collect existing documentation:**
   - Ask user to provide directory of current QMS documents
   - Documents can be in any format (.txt, .md, .doc, .docx, .pdf)
   - Include any procedures, manuals, work instructions, forms

2. **Run gap analysis script:**
   ```bash
   python scripts/gap_analyzer.py --docs-dir <path_to_docs> --output gap-report.json
   ```

3. **Review results:**
   - Identify which required procedures are present vs. missing. The script checks the 26 always-applicable documented procedures (it omits the conditional "when applicable" ones — design, installation, servicing, sterilization, etc. — to avoid false-negative gaps); the full set is "31" by convention. See `references/quick-reference.md` for the full list and counting note.
   - Identify missing key documents (Quality Manual, MDF, etc.)
   - Calculate compliance percentage (reported against the 26 procedures the script tracks)
   - Prioritize missing documentation, including any conditional procedures that apply to this manufacturer

4. **Present findings to user:**
   - Summarize what exists
   - Clearly list what's missing
   - Provide prioritized action plan
   - Estimate effort required

**Output:** Comprehensive gap analysis report with prioritized action items

### 2. Understand Requirements (Reference Consultation)

**When to use:** User needs to understand specific ISO 13485 requirements

**Available references:**
- `references/iso-13485-requirements.md` - Complete clause-by-clause breakdown
- `references/mandatory-documents.md` - All 31 required procedures explained
- `references/gap-analysis-checklist.md` - Detailed compliance checklist
- `references/quality-manual-guide.md` - How to create Quality Manual

**How to use:**

1. **For specific clause questions:**
   - Read relevant section from `iso-13485-requirements.md`
   - Explain requirements in plain language
   - Provide practical examples

2. **For document requirements:**
   - Consult `mandatory-documents.md`
   - Explain what must be documented
   - Clarify when documents are applicable vs. excludable

3. **For implementation guidance:**
   - Use `quality-manual-guide.md` for policy-level documents
   - Provide step-by-step creation process
   - Show examples of good vs. poor implementation

**Key reference sections to know:**

- **Clause 4:** QMS requirements, documentation, risk management, software validation
- **Clause 5:** Management responsibility, quality policy, objectives, management review
- **Clause 6:** Resources, competence, training, infrastructure
- **Clause 7:** Product realization, design, purchasing, production, traceability
- **Clause 8:** Measurement, audits, CAPA, complaints, data analysis

### 3. Create Documentation (Template-Based Generation)

**When to use:** User needs to create specific QMS documents.

**Available templates:**
- Quality Manual: `assets/templates/quality-manual-template.md`
- CAPA Procedure: `assets/templates/procedures/CAPA-procedure-template.md`
- Document Control: `assets/templates/procedures/document-control-procedure-template.md`

Follow the full creation process, priority order (Phases 1-6), and per-document deep dives (Quality Manual, SOPs, CAPA, Medical Device Files) in `references/document-creation-guide.md`. That guide also covers the detailed clause-by-clause comprehensive gap analysis.

## Routing Guidance

- **Gap analysis** (existing docs) → Core Workflow Step 1; run `scripts/gap_analyzer.py`. Detailed clause-by-clause assessment: `references/document-creation-guide.md`.
- **Understanding a clause/requirement** → Core Workflow Step 2; read `references/iso-13485-requirements.md` and `references/mandatory-documents.md`.
- **Creating a Quality Manual / SOP / CAPA / MDF** → `references/document-creation-guide.md` + the matching template in `assets/templates/`.
- **Matching a user situation to an approach** (startup from scratch, existing-QMS gap, single document, QMSR transition, audit prep) → `references/common-scenarios.md`.
- **Writing-quality, exclusions, mistakes to avoid** → `references/best-practices.md`.
- **The 31 procedures, regulatory requirements by region, retention periods** → `references/quick-reference.md`.

## References Index

- `references/iso-13485-requirements.md` — complete ISO 13485:2016 breakdown, clause by clause.
- `references/mandatory-documents.md` — all 31 required procedures plus other mandatory documents, explained.
- `references/gap-analysis-checklist.md` — comprehensive compliance checklist.
- `references/quality-manual-guide.md` — step-by-step guide for a compliant Quality Manual.
- `references/document-creation-guide.md` — full document-creation process, priority order, and per-document deep dives (QM, SOPs, CAPA, MDF, detailed gap analysis).
- `references/common-scenarios.md` — worked approaches for the five most common user situations.
- `references/best-practices.md` — document-development best practices, exclusion rules and examples, common mistakes.
- `references/quick-reference.md` — the 31 procedures, regulatory requirements by region, document retention periods.

### scripts/
- `gap_analyzer.py` — automated tool to analyze existing documentation and identify gaps against ISO 13485 requirements.

### assets/templates/
- `quality-manual-template.md`, `procedures/CAPA-procedure-template.md`, `procedures/document-control-procedure-template.md`.

## Getting Started

**First-time users should:**

1. Read `references/iso-13485-requirements.md` to understand the standard.
2. If you have existing documentation, run the gap analysis script (Core Workflow Step 1).
3. Create the Quality Manual using the template and `references/document-creation-guide.md`.
4. Develop procedures in priority order (see the guide).
5. Use `references/gap-analysis-checklist.md` for final validation.

**Need help?** Start by describing your situation: what stage you're at, what you have, and what you need to create — then route via the guidance above.


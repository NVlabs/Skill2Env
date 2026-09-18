# Document Creation Guide

Detailed, step-by-step guidance for creating each major QMS document type. Use after a gap analysis or when a user requests a specific document.

## Document creation process (general)

1. **Identify what needs to be created** — based on gap analysis or user request. Prioritize critical documents first (Quality Manual, CAPA, Complaints, Audits).
2. **Select appropriate template** — Quality Manual template for QM; procedure templates as examples for SOPs; adapt structure to the organization's needs.
3. **Customize template with user-specific information:**
   - Replace all placeholder text: `[COMPANY NAME]`, `[DATE]`, `[NAME]`, etc.
   - Tailor scope to the user's actual operations
   - Add or remove sections based on applicability
   - Ensure consistency with the organization's processes
4. **Key customization areas:** company information and addresses; product types and classifications; applicable regulatory requirements; organization structure and responsibilities; actual processes and procedures; document numbering schemes; exclusions and justifications.
5. **Validate completeness:** all required sections present; all placeholders replaced; cross-references correct; approval sections complete.

## Document creation priority order

**Phase 1 — Foundation (Critical):**
1. Quality Manual
2. Quality Policy and Objectives
3. Document Control procedure
4. Record Control procedure

**Phase 2 — Core Processes (High Priority):**
5. Corrective and Preventive Action (CAPA)
6. Complaint Handling
7. Internal Audit
8. Management Review
9. Risk Management

**Phase 3 — Product Realization (High Priority):**
10. Design and Development (if applicable)
11. Purchasing
12. Production and Service Provision
13. Control of Nonconforming Product

**Phase 4 — Supporting Processes (Medium Priority):**
14. Training and Competence
15. Calibration/Control of M&M Equipment
16. Process Validation
17. Product Identification and Traceability

**Phase 5 — Additional Requirements (Medium Priority):**
18. Feedback and Post-Market Surveillance
19. Regulatory Reporting
20. Customer Communication
21. Data Analysis

**Phase 6 — Specialized (If Applicable):**
22. Installation (if applicable)
23. Servicing (if applicable)
24. Sterilization (if applicable)
25. Contamination Control (if applicable)

## Creating a Quality Manual

1. **Read the comprehensive guide:** read `references/quality-manual-guide.md` in full; understand structure and required content; review examples provided.
2. **Gather organization information:** legal company name and addresses; product types and classifications; organizational structure; applicable regulations; scope of operations; any exclusions needed.
3. **Use template:** start with `assets/templates/quality-manual-template.md`; follow structure exactly (required by ISO 13485); replace all placeholders.
4. **Complete required sections:**
   - **Section 0:** Document control, approvals
   - **Section 1:** Introduction, company overview
   - **Section 2:** Scope and exclusions (critical — must justify exclusions)
   - **Section 3:** Quality Policy (must be signed by top management)
   - **Sections 4-8:** Address each ISO 13485 clause at policy level
   - **Appendices:** Procedure list, org chart, process map, definitions
5. **Key requirements:**
   - Must reference all 31 documented procedures (Appendix A)
   - Must describe process interactions (Appendix C — create process map)
   - Must define documentation structure (Section 4.2)
   - Must justify any exclusions (Section 2.4)
6. **Validation checklist:**
   - [ ] All required content per ISO 13485 Clause 4.2.2
   - [ ] Quality Policy signed by top management
   - [ ] All exclusions justified
   - [ ] All procedures listed in Appendix A
   - [ ] Process map included
   - [ ] Organization chart included

## Creating Procedures (SOPs)

General approach for all procedures:

1. **Understand the requirement:** read the relevant clause in `references/iso-13485-requirements.md`; understand WHAT must be documented; identify WHO, WHEN, WHERE for the organization.
2. **Use template structure:** follow CAPA or Document Control templates as examples; standard sections are Purpose, Scope, Definitions, Responsibilities, Procedure, Records, References; keep procedures clear and actionable.
3. **Define responsibilities clearly:** identify specific roles (not names); define responsibilities for each role; ensure coverage of all required activities.
4. **Document the "what" not excessive "how":** procedures define WHAT must be done; detailed how-to goes in Work Instructions (Tier 3); strike a balance between guidance and flexibility.
5. **Include required elements:** all elements specified in the ISO 13485 clause; records that must be maintained; responsibilities for each activity; references to related documents.

### Example: Creating a CAPA procedure

1. Read ISO 13485 Clauses 8.5.2 and 8.5.3 from references.
2. Use `assets/templates/procedures/CAPA-procedure-template.md`.
3. Customize: CAPA prioritization criteria for your organization; root cause analysis methods you'll use; approval authorities and responsibilities; timeframes based on your operations; integration with complaint handling, audits, etc.
4. Add forms as attachments: CAPA Request Form, Root Cause Analysis Worksheet, Action Plan Template, Effectiveness Verification Checklist.

## Creating Medical Device Files (MDF)

**What is an MDF:**
- File for each medical device type or family
- Replaces separate DHF, DMR, DHR (per FDA QMSR harmonization)
- Contains all documentation about the device

**Required contents per ISO 13485 Clause 4.2.3:**
1. General description and intended use
2. Label and instructions for use specifications
3. Product specifications
4. Manufacturing specifications
5. Procedures for purchasing, manufacturing, servicing
6. Procedures for measuring and monitoring
7. Installation requirements (if applicable)
8. Risk management file(s)
9. Verification and validation information
10. Design and development file(s) (when applicable)

**Process:**
1. Identify each device type or family
2. Create MDF structure (folder or binder)
3. Collect or create each required element
4. Ensure traceability between documents
5. Maintain as a living document (update with changes)

## Comprehensive gap analysis (detailed)

When the user wants a detailed assessment of all requirements:

1. **Use comprehensive checklist:** open `references/gap-analysis-checklist.md`; work through clause by clause; mark status for each requirement: Compliant, Partial, Non-compliant, N/A.
2. **For each clause:** read requirement description; identify existing evidence; note gaps or deficiencies; define action required; assign responsibility and target date.
3. **Summarize by clause:** calculate compliance percentage per clause; identify highest-risk gaps; prioritize actions.
4. **Create action plan:** list all gaps; prioritize Critical > High > Medium > Low; assign owners and dates; estimate resources needed.
5. **Output:** completed gap analysis checklist; summary report with compliance percentages; prioritized action plan; timeline and milestones.

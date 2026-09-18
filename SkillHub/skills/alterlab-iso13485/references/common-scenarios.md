# Common Scenarios

Worked approaches for the most common user situations. Match the user's request to a scenario and follow the approach.

## Scenario 1: Starting from Scratch

**User request:** "We're a medical device startup and need to implement ISO 13485. Where do we start?"

**Approach:**
1. **Explain the journey:** ISO 13485 requires comprehensive QMS documentation; typically 6-12 months for full implementation; can be done incrementally.
2. **Start with foundation:** Quality Policy and Objectives; Quality Manual; organization structure and responsibilities.
3. **Follow the priority order:** use the Phase 1-6 priority list (see `references/document-creation-guide.md`); create documents in logical sequence; build on previously created documents.
4. **Key milestones:**
   - Month 1-2: Foundation documents (Quality Manual, policies)
   - Month 3-4: Core processes (CAPA, Complaints, Audits)
   - Month 5-6: Product realization processes
   - Month 7-8: Supporting processes
   - Month 9-10: Internal audits and refinement
   - Month 11-12: Management review and certification audit

## Scenario 2: Gap Analysis for Existing QMS

**User request:** "We have some procedures but don't know what we're missing for ISO 13485."

**Approach:**
1. **Run automated gap analysis:** ask for the document directory; run `scripts/gap_analyzer.py`; review automated findings.
2. **Conduct detailed assessment:** use the comprehensive checklist for the user's specific situation; go deeper than automated analysis; assess quality of existing documents, not just presence.
3. **Provide a prioritized gap list:** missing mandatory procedures; incomplete procedures; quality issues with existing documents; missing records or forms.
4. **Create a remediation plan:** high priority (safety-related, regulatory-required); medium priority (core QMS processes); low priority (improvement opportunities).

## Scenario 3: Creating a Specific Document

**User request:** "Help me create a CAPA procedure."

**Approach:**
1. **Explain requirements:** read ISO 13485 Clauses 8.5.2 and 8.5.3 from references; explain what must be in the CAPA procedure; provide examples of good CAPA processes.
2. **Use template:** start with the CAPA procedure template; explain each section's purpose; show what needs customization.
3. **Gather user-specific info:** how are CAPAs initiated in their organization? who are the responsible parties? what prioritization criteria make sense? what RCA methods will they use? what are appropriate timeframes?
4. **Create customized procedure:** replace all placeholders; adapt to the user's processes; ensure completeness.
5. **Add supporting materials:** CAPA request form; RCA worksheets; action plan template; effectiveness verification checklist.

## Scenario 4: Updating for Regulatory Changes

**User request:** "We need to update our QMS for FDA QMSR harmonization."

**Approach:**
1. **Explain changes:** FDA 21 CFR Part 820 harmonized with ISO 13485; now called QMSR (effective Feb 2, 2026); key change: Medical Device File replaces DHF/DMR/DHR.
2. **Review current documentation:** identify documents referencing QSR; find separate DHF, DMR, DHR structures; check for ISO 13485 compliance gaps.
3. **Update strategy:** update references from QSR to QMSR; consolidate DHF/DMR/DHR into Medical Device Files; add any missing ISO 13485 requirements; maintain backward compatibility during transition.
4. **Create transition plan:** update Quality Manual; update MDF procedure; reorganize device history files; train personnel on changes.

## Scenario 5: Preparing for Certification Audit

**User request:** "We have our documentation ready. How do we prepare for the certification audit?"

**Approach:**
1. **Conduct a readiness assessment:** use the comprehensive gap analysis checklist; review all documentation for completeness; verify records exist for all required items; check for consistent implementation.
2. **Pre-audit checklist:**
   - [ ] All 31 procedures documented and approved
   - [ ] Quality Manual complete with all required content
   - [ ] Medical Device Files complete for all products
   - [ ] Internal audit completed with findings addressed
   - [ ] Management review completed
   - [ ] Personnel trained on QMS procedures
   - [ ] Records maintained per retention requirements
   - [ ] CAPA system functional with effectiveness demonstrated
   - [ ] Complaints system operational
3. **Conduct a mock audit:** use ISO 13485 requirements as audit criteria; sample records to verify consistent implementation; interview personnel to verify understanding; identify any non-conformances.
4. **Address findings:** correct any deficiencies; document corrections; verify effectiveness.
5. **Final preparation:** brief management and staff; prepare audit schedule; organize evidence and records; designate escorts and support personnel.

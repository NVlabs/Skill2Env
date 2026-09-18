---
name: alterlab-research-ethics
description: "International research ethics and compliance assistant supporting IRB/ethics board applications, informed consent drafting, data management plans, Belmont Report principles, Declaration of Helsinki (2024), GDPR compliance for research, HIPAA considerations, vulnerable populations protocols, deception research, confidentiality and anonymity, research integrity (fabrication/falsification/plagiarism), conflict of interest disclosure, and dual-use research oversight. Use when preparing an IRB or ethics board application, drafting informed consent, writing a data management plan, addressing GDPR/HIPAA in research, protecting human subjects or vulnerable populations, handling animal ethics, or disclosing conflicts of interest. For Turkey-specific etik kurul use alterlab-tr-research-ethics; for KVKK data plans alterlab-kvkk-dmp; for survey wording alterlab-survey-design; for qualitative methodology alterlab-qualitative-methods. Part of the AlterLab Academic Skills suite."
license: MIT
allowed-tools: Read WebFetch WebSearch Bash(python:*)
compatibility: No API key required. Guidance-focused skill; uses WebFetch/WebSearch and optional Python helpers via `uv run python`.
metadata:
  skill-author: AlterLab
  version: "1.1.0"
  last_updated: "2026-06-09"
---

# Research Ethics — Ethics, Compliance & Integrity Agent

A comprehensive research ethics tool for faculty and researchers navigating the complex landscape of research compliance. Covers the full ethics lifecycle: from understanding foundational principles, through ethics board applications, to ongoing compliance during data collection, analysis, and publication.

## Overview

Research ethics is the application of moral principles to the design, conduct, and reporting of research involving human participants, animal subjects, sensitive data, and dual-use technologies. This skill provides practical guidance grounded in international ethical frameworks, helping researchers move from ethical principles to compliant practice.

This is not a substitute for your institution's ethics board or legal counsel. It is a tool to help you prepare stronger applications, anticipate ethical issues, and maintain compliance throughout the research lifecycle.

## When to Use This Skill

This skill should be used when:
- Preparing an IRB/ethics committee application
- Drafting informed consent forms and information sheets
- Writing data management plans for grant applications
- Assessing whether a study requires ethical review
- Working with vulnerable populations
- Designing research involving deception
- Ensuring GDPR or HIPAA compliance in research
- Addressing research integrity concerns (plagiarism, fabrication, falsification)
- Disclosing conflicts of interest
- Planning research with dual-use potential
- Teaching research ethics courses
- Responding to ethics board revision requests

### Does NOT Trigger

| Scenario | Use Instead |
|----------|-------------|
| Legal advice on data protection | Consult institutional legal counsel |
| Turkish etik kurul application / committee routing | `alterlab-tr-research-ethics` |
| KVKK (Turkish data-protection) data management plan | `alterlab-kvkk-dmp` |
| Survey instrument design | `alterlab-survey-design` |
| Qualitative methodology | `alterlab-qualitative-methods` |
| Clinical trial design / clinical reporting | `clinical-research` skills (e.g. `alterlab-clinical-reports`) |

---

## Core Capabilities

### 1. Foundational Ethical Principles

#### The Belmont Report (1979) — Three Core Principles

The Belmont Report remains the foundational document for research ethics in the United States and has influenced ethics frameworks worldwide.

| Principle | Definition | Application |
|-----------|-----------|-------------|
| **Respect for Persons** | Individuals should be treated as autonomous agents; persons with diminished autonomy are entitled to protection | Informed consent; right to withdraw; privacy protections; special protections for vulnerable populations |
| **Beneficence** | Obligation to maximize benefits and minimize harms; do no harm | Risk-benefit analysis; safety protocols; monitoring for adverse events; data security |
| **Justice** | Fair distribution of research benefits and burdens; equitable participant selection | Inclusion/exclusion criteria justified; not targeting vulnerable groups for convenience; sharing research benefits |

#### Declaration of Helsinki (WMA, 2024 revision)

The 2024 revision (adopted October 2024) is the only official version; the WMA states earlier versions should be cited only for historical purposes. It replaces "subjects" with "participants" throughout, addresses all individuals and organizations involved in research (not only physicians), and adds an explicit scientific-integrity / zero-tolerance-for-misconduct provision. Note that the 2024 revision renumbered paragraphs relative to 2013, so verify any paragraph number against the current text before citing it.

Key principles extending beyond the Belmont Report:
- Research involving human participants must conform to generally accepted scientific principles
- The well-being of the individual research participant must take precedence over all other interests
- Every research study involving human participants must be registered in a publicly accessible database before recruitment of the first participant
- Negative and inconclusive results must be published or otherwise made publicly available
- Post-study provisions: participants who benefit from the research should have access to the intervention
- Meaningful engagement with participants and their communities before, during, and after the study

#### Singapore Statement on Research Integrity (2010)

Four principles:
1. **Honesty** in all aspects of research
2. **Accountability** in the conduct of research
3. **Professional courtesy and fairness** in working with others
4. **Good stewardship** of research on behalf of others

### 2. Ethics Board Applications

#### Does Your Study Require Ethical Review?

```
Does your study involve...
│
├── Human participants (interviews, surveys, experiments, observations)?
│   └── YES → Full or expedited review required
│
├── Human data (medical records, educational records, social media data)?
│   └── YES → Review required (level depends on identifiability)
│
├── Human biological samples (blood, tissue, DNA)?
│   └── YES → Full review required
│
├── Animal subjects?
│   └── YES → IACUC/animal ethics review required
│
├── Publicly available, de-identified data only?
│   └── MAYBE → May qualify for exemption; check with your IRB
│
├── Quality improvement / program evaluation (not generalizable)?
│   └── MAYBE → Some institutions exempt; consult your IRB
│
└── None of the above?
    └── NO ethical review likely required

WHEN IN DOUBT: Submit to your ethics board for a determination.
Always apply BEFORE collecting data.
```

#### IRB Application Template

A complete section-by-section IRB/ethics board application template — Study Overview, Purpose & Background, Participants (including vulnerable-population flags), Procedures, Risks & Benefits, Informed Consent (waivers/assent), and Data Management — has moved to `references/irb_application_template.md`. Copy and adapt those sections for your institution's submission portal.

### 3. Informed Consent Drafting

**Essential Elements of Informed Consent (45 CFR 46.116):** the full consent-form template (invitation, purpose, procedures, risks, benefits, compensation, confidentiality, voluntary withdrawal, and signature blocks) plus a checklist of online-research consent considerations have moved to `references/informed_consent_templates.md`.

### 4. Data Management Plans

**DMP Template (aligned with funder requirements):** a full funder-aligned data management plan template — data description, collection standards, ethics/legal compliance, storage & security, preservation & sharing, and roles & responsibilities — has moved to `references/data_management_plan_template.md`.

### 5. GDPR Compliance for Research

The General Data Protection Regulation applies to research involving personal data of individuals in the EU/EEA.

**GDPR Lawful Bases for Research:**

| Lawful Basis | When to Use | Key Requirement |
|-------------|-------------|-----------------|
| Consent (Art. 6(1)(a)) | Most common for research | Freely given, specific, informed, unambiguous; can be withdrawn |
| Legitimate interest (Art. 6(1)(f)) | Secondary analysis, non-sensitive data | Balancing test required; document assessment |
| Public interest (Art. 6(1)(e) + Art. 89) | Publicly funded research in public interest | Must implement appropriate safeguards |

**Key GDPR Requirements for Researchers:**

```markdown
## GDPR Compliance Checklist for Research

### Before Data Collection
- [ ] Identify lawful basis for processing
- [ ] Conduct Data Protection Impact Assessment (DPIA) if high-risk processing
- [ ] Prepare privacy notice / information sheet (Art. 13/14)
- [ ] Appoint Data Protection Officer contact (if required)
- [ ] Establish data processing agreement with any third parties
- [ ] Document processing activities in institutional register (Art. 30)

### Privacy Notice Must Include
- [ ] Identity and contact details of the controller
- [ ] Contact details of the Data Protection Officer
- [ ] Purposes and lawful basis for processing
- [ ] Categories of personal data collected
- [ ] Recipients or categories of recipients
- [ ] Data transfers outside EU/EEA (and safeguards)
- [ ] Retention period or criteria for determining it
- [ ] Data subject rights (access, rectification, erasure, portability, objection)
- [ ] Right to withdraw consent (if consent is the lawful basis)
- [ ] Right to lodge a complaint with a supervisory authority
- [ ] Whether provision of data is statutory, contractual, or voluntary
- [ ] Existence of automated decision-making (if applicable)

### Data Subject Rights (with research exemptions under Art. 89)
- Right of access (Art. 15) — may be limited if it would seriously impair research
- Right to rectification (Art. 16) — applies
- Right to erasure (Art. 17) — may be limited under Art. 17(3)(d)
- Right to data portability (Art. 20) — applies if consent-based
- Right to object (Art. 21) — may be limited for public interest research

### Data Minimization
- [ ] Collect only data necessary for research purposes
- [ ] Pseudonymize as early as possible
- [ ] Anonymize when identifiability is no longer needed
- [ ] Destroy linking keys when no longer required
```

### 6. HIPAA Considerations for Research

```markdown
## HIPAA Research Checklist

### Does HIPAA Apply?
HIPAA applies if you are accessing Protected Health Information (PHI)
from a HIPAA-covered entity (healthcare provider, health plan, clearinghouse).

### PHI Includes Any of the 18 Identifiers:
1. Names
2. Geographic data smaller than state
3. Dates (except year) related to an individual
4. Phone numbers
5. Fax numbers
6. Email addresses
7. Social Security numbers
8. Medical record numbers
9. Health plan beneficiary numbers
10. Account numbers
11. Certificate/license numbers
12. Vehicle identifiers and serial numbers
13. Device identifiers and serial numbers
14. Web URLs
15. IP addresses
16. Biometric identifiers
17. Full-face photos and comparable images
18. Any other unique identifying number or code

### Accessing PHI for Research — Three Pathways
1. **Individual Authorization** — Patient signs HIPAA authorization form
2. **IRB/Privacy Board Waiver** — Meets criteria for waiver of authorization
3. **De-identified Data** — All 18 identifiers removed (Safe Harbor method)
   or expert determination that re-identification risk is very small

### Limited Data Set
- Removes direct identifiers but may retain dates, zip codes, ages
- Requires a Data Use Agreement (DUA) between covered entity and researcher
- Still considered PHI — must be protected
```

### 7. Research with Vulnerable Populations

**Vulnerability Categories and Additional Protections:**

| Population | Source of Vulnerability | Additional Protections Required |
|-----------|----------------------|-------------------------------|
| Children (under 18) | Diminished autonomy, developmental capacity | Parental permission + child assent; age-appropriate assent forms; minimal risk unless prospect of direct benefit |
| Pregnant women | Potential harm to fetus | Research must minimize risk to fetus; father's consent for fetal research where applicable |
| Prisoners | Coercive environment, limited autonomy | Minimal risk only (generally); prisoner representative on IRB; no undue inducement |
| Cognitively impaired | Diminished capacity to consent | Legally authorized representative consent + participant assent; ongoing capacity assessment |
| Students/employees of researcher | Power differential, perceived coercion | Recruitment by third party; opt-out without penalty; extra confidentiality protections |
| Economically disadvantaged | Susceptibility to undue inducement | Compensation must be fair but not coercive; equitable selection |
| Indigenous communities | Historical exploitation, cultural concerns | Community consultation/consent; culturally appropriate methods; benefit sharing; data sovereignty |
| Refugees/asylum seekers | Legal precarity, trauma, language barriers | Trauma-informed consent; interpreter services; no impact on legal status |

### 8. Research Integrity

**The FFP Framework (Fabrication, Falsification, Plagiarism):**

```
FABRICATION
│   Making up data or results and recording or reporting them
│   Examples:
│   - Inventing data points to fill gaps
│   - Creating fake participants or responses
│   - Reporting experiments that were never conducted
│
FALSIFICATION
│   Manipulating research materials, equipment, or processes, or
│   changing or omitting data/results such that the research is
│   not accurately represented
│   Examples:
│   - Selectively excluding data points without justification
│   - Manipulating images (e.g., Western blots) beyond standard adjustments
│   - Changing statistical methods post-hoc to achieve significance
│   - Omitting inconvenient results
│
PLAGIARISM
    Appropriating another person's ideas, processes, results, or words
    without giving appropriate credit
    Examples:
    - Copying text without quotation marks and citation
    - Paraphrasing without attribution
    - Self-plagiarism (republishing your own work without disclosure)
    - Using another's methodology without citation
```

**Responsible Conduct of Research (RCR) Domains:**

| Domain | Key Issues | Best Practices |
|--------|-----------|---------------|
| Data management | Integrity, security, sharing | Maintain lab notebooks; document analysis decisions; share data per funder policy |
| Authorship | Ghost/gift authorship, CRediT roles | Follow ICMJE criteria; discuss authorship early; document contributions |
| Peer review | Confidentiality, bias, conflicts | Decline reviews with conflicts; provide constructive feedback; maintain confidentiality |
| Mentoring | Power dynamics, exploitation | Establish expectations in writing; regular meetings; support career development |
| Collaborative research | IP, data ownership, authorship across institutions | Written collaboration agreements; MOU before data sharing |
| Publication practices | Duplicate publication, salami-slicing, selective reporting | Pre-register studies; report all outcomes; follow CONSORT/STROBE/PRISMA guidelines |
| Conflict of interest | Financial, intellectual, personal | Disclose all relevant interests; follow institutional COI policy; recuse when necessary |

### 9. Conflict of Interest Disclosure

```markdown
## Conflict of Interest Self-Assessment

### Financial Interests
- [ ] I (or my immediate family) hold equity in a company whose products
      are related to this research
- [ ] I receive consulting fees, honoraria, or speaker fees from an entity
      related to this research (>$5,000/year or per institutional threshold)
- [ ] I hold patents or receive royalties related to this research
- [ ] I receive research funding from a company whose products are being studied
- [ ] I serve on a board of directors or advisory board of a related entity

### Non-Financial Interests
- [ ] I have personal relationships with individuals involved in this research
- [ ] I have intellectual commitments that could bias my interpretation
- [ ] I hold leadership positions in organizations related to this research
- [ ] I have previously published strong positions on the topic under study

### For Each Identified Conflict
- Nature of the conflict: [describe]
- Potential impact on research: [how could it bias design, analysis, or reporting?]
- Management plan: [recusal, independent oversight, disclosure in publications,
  blinded analysis, etc.]
```

### 10. Dual-Use Research of Concern (DURC)

Research that could be directly misapplied to pose a significant threat to public health, agriculture, plants, animals, the environment, or national security.

**DURC Screening Questions:**

```markdown
Does your research involve any of these agents or toxins?
- Avian influenza virus (highly pathogenic)
- Bacillus anthracis, Botulinum neurotoxin
- Burkholderia mallei, Burkholderia pseudomallei
- Ebola virus, Foot-and-mouth disease virus
- Francisella tularensis, Marburg virus
- Reconstructed 1918 influenza virus
- Rinderpest virus, Toxin-producing strains of Clostridium botulinum
- Variola major virus, Variola minor virus
- Yersinia pestis

Does your research involve any of these experimental effects?
1. Enhance harmful consequences of the agent
2. Disrupt immunity or vaccine effectiveness
3. Confer resistance to clinically/agriculturally useful interventions
4. Increase stability, transmissibility, or ability to disseminate
5. Alter host range or tropism
6. Enhance susceptibility of a host population
7. Generate or reconstitute an eradicated or extinct agent

If YES to both an agent AND an effect → Institutional DURC review required
```

---

## Best Practices

1. **Apply for ethics approval before collecting data.** Retroactive approval is rarely possible and always problematic. Plan ethics into your project timeline from the start.

2. **Write consent forms in plain language.** Target a 6th-8th grade reading level. Avoid jargon. Use short sentences. Test readability with the Flesch-Kincaid score.

3. **Anticipate risks realistically.** Do not minimize risks in your application. Reviewers respect honest risk assessment with thoughtful mitigation plans.

4. **Document everything.** Maintain an ethics audit trail: consent forms, protocol amendments, adverse event reports, data management logs. This protects you and your participants.

5. **Treat ethics as ongoing, not one-time.** Ethics compliance does not end when the IRB letter arrives. Monitor for new risks, report adverse events promptly, and submit amendments for protocol changes.

6. **Protect identifiability at every stage.** De-identify data as early as possible. Store identifiers separately from data. Encrypt everything. Delete what you no longer need.

7. **Respect autonomy genuinely.** Voluntary participation means truly voluntary — no pressure, no penalty for withdrawal, no coercive incentives. Pay attention to power dynamics.

8. **Consult early and often.** Talk to your IRB office before submitting. They can help you identify issues early, which saves time and revision cycles.

9. **Stay current with regulations.** GDPR, HIPAA, and institutional policies evolve. Bookmark your institutional research compliance website and check it annually.

10. **Model integrity.** Research ethics is not just compliance with rules. It is a commitment to honesty, transparency, and respect for the people and communities your research touches.

---

## Common Pitfalls

| Pitfall | Why It Happens | How to Avoid |
|---------|---------------|--------------|
| Collecting data before approval | Eagerness to start; underestimating review timelines | Build 2-3 months for review into your project timeline |
| Consent form too complex | Copy-pasting legal language | Write at 6th-8th grade level; have a non-expert read it |
| Inadequate risk assessment | Researcher normalizes risks in their discipline | Consult with someone outside your field; think from the participant's perspective |
| Failing to report protocol changes | Viewing amendments as administrative burden | Any change to recruitment, procedures, or risks requires an amendment before implementation |
| Data stored insecurely | Convenience over security | Use institutional systems; encrypt portable devices; never email identifiable data |
| Gift or ghost authorship | Social pressure, power dynamics | Discuss authorship using CRediT taxonomy at project start; revisit periodically |
| Self-plagiarism | Reusing own text without disclosure | Cite your prior work; use quotation marks; disclose to editors |
| Ignoring cultural context | Applying Western ethics frameworks universally | Consult community leaders; hire cultural liaisons; adapt consent processes |
| Insufficient anonymization | Assuming removal of names is sufficient | Consider indirect identifiers (job title + institution + age can re-identify); use k-anonymity checks |
| No data management plan | Viewed as bureaucratic requirement | Treat DMP as a living document; it protects you during and after the research |

---

## References

- Beauchamp, T. L., & Childress, J. F. (2019). *Principles of biomedical ethics* (8th ed.). Oxford University Press.
- European Commission. (2018). *Ethics in social science and humanities*. https://ec.europa.eu/info/funding-tenders/opportunities/docs/2021-2027/horizon/guidance/ethics-in-social-science-and-humanities_he_en.pdf
- Israel, M., & Hay, I. (2006). *Research ethics for social scientists*. Sage.
- National Commission for the Protection of Human Subjects. (1979). *The Belmont Report*. https://www.hhs.gov/ohrp/regulations-and-policy/belmont-report/
- Office for Human Research Protections (OHRP). (2018). *45 CFR 46 (Common Rule)*. https://www.hhs.gov/ohrp/regulations-and-policy/regulations/45-cfr-46/
- Resnik, D. B. (2020). *The ethics of research with human subjects: Protecting people, advancing science, promoting trust*. Springer.
- Steneck, N. H. (2007). *ORI introduction to the responsible conduct of research*. Government Printing Office.
- World Medical Association. (2024). *Declaration of Helsinki — Ethical principles for medical research involving human participants* (2024 revision). https://www.wma.net/policies-post/wma-declaration-of-helsinki/

See also: `references/ethics-guidelines.md` for expanded regulatory details.

---

Part of the AlterLab Academic Skills suite.

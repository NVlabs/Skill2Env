---
name: gov-pack
description: Regulatory + compliance overlay for US government / public-sector software — FedRAMP authorization, NIST 800-53 controls, Section 508 accessibility, CJIS for law-enforcement integrations.
when_to_use: Product serves federal / state / local government, integrates with CJIS / IRS / DHS, or seeks FedRAMP / StateRAMP authorization.
applies_to:
  - gov-public
extends: []
---

# Gov-Public Compliance Pack

> Loaded automatically when ARCH or PROJECT.md mentions: FedRAMP, NIST 800-53, FISMA, CJIS, Section 508, ATO (Authorization to Operate), login.gov, id.me, GovCloud, `aws-us-gov-` partition, or any `.gov` / `.mil` domain reference.
> Routes through `gov-reviewer` (threat model + authorization-boundary scoping) and adds compliance gates that block `senior-dev` until human sign-off.

## Reviewer

- **gov-reviewer** runs BEFORE senior-dev → writes `TM-gov-{slug}.md` + authorization-boundary diagram
- Scopes the ATO boundary (cost driver #1), maps each architectural decision to NIST 800-53 Rev 5 control families, drafts PIA input for the agency privacy officer.

## Human gates added

| Gate | When | Owner |
|---|---|---|
| `gate:fedramp-boundary` | After TM, before any infra is provisioned | Authorizing Official (AO) / agency sponsor |
| `gate:pia` | Before any PII collection ships | Agency Senior Agency Official for Privacy (SAOP) |
| `gate:508-conformance` | Before any government-facing UI ships | Accessibility lead (human, with assistive-tech testing) |
| `gate:ship` | Standard | security-officer + 3PAO (if FedRAMP Moderate+) |

`gate:fedramp-boundary` is the most expensive gate to reopen — once infra is provisioned and ATO assessment is in flight, boundary changes can cost $200K+ in reassessment. Lock it early.

## Required artefacts in every gov-public project

| Artefact | Location | Owner |
|---|---|---|
| FedRAMP authorization-boundary diagram | `docs/compliance/fedramp/boundary.md` | architect |
| System Security Plan (SSP) sections | `docs/compliance/fedramp/ssp/` | gov-reviewer + senior-dev |
| NIST 800-53 Rev 5 control-mapping matrix | `docs/compliance/nist-800-53-matrix.md` | gov-reviewer |
| Privacy Impact Assessment (PIA) input | `docs/compliance/pia-draft.md` | gov-reviewer |
| Section 508 VPAT 2.5 | `docs/compliance/vpat-2.5.md` | accessibility lead |
| FIPS 140-3 crypto-module manifest | `docs/compliance/fips-140-3-modules.md` | senior-dev |
| Annual 3PAO penetration test report | `docs/compliance/pentest/{year}/` | external 3PAO |
| POA&M (Plan of Action and Milestones) | `docs/compliance/poam.csv` | security-officer |
| Continuous Monitoring (ConMon) plan | `docs/compliance/conmon.md` | security-officer |
| CJIS compliance evidence (if applicable) | `docs/compliance/cjis/` | gov-reviewer |
| StateRAMP equivalence statement | `docs/compliance/stateramp.md` | architect |
| TIC 3.0 alignment notes | `docs/compliance/tic-3.0.md` | architect |

### NIST 800-53 Rev 5 Moderate baseline scope

- ~325 controls across 18 families (AC, AT, AU, CA, CM, CP, IA, IR, MA, MP, PE, PL, PM, PS, PT, RA, SA, SC, SI, SR).
- Each control needs a paragraph of implementation evidence in the SSP — no hand-wave allowed.
- Common rough patches: AU-9 (audit-log tamper-evidence), IA-2(11) (phishing-resistant MFA — PIV/CAC/FIDO2), SC-13 (FIPS-validated crypto), CM-3 (formal change management), SR-3 (supply-chain risk).

## EVAL suite

- `EVAL-508-conformance` — every government-facing screen passes WCAG 2.2 AA automated checks (axe-core), plus manual keyboard-only + screen-reader (NVDA/VoiceOver/JAWS) traversal of all critical flows. Drag-drop has keyboard alternative. Color is never sole state indicator. Form labels are explicit. Video has captions + transcript.
- `EVAL-fips-140-3-enforcement` — all data-at-rest encryption uses a FIPS 140-3 validated module (cert # logged in manifest); all data-in-transit uses TLS 1.2+ with FIPS-approved cipher suites. No rolled-your-own crypto. No deprecated algorithms (no MD5, SHA-1, 3DES, RC4).
- `EVAL-cjis-mfa` — if `applies_to: cjis-integration` is set, every persona that can touch criminal-justice information uses FBI-compliant advanced authentication (PIV/CAC/FIDO2). No SMS OTP. Inactivity timeout ≤ 30 min. Session re-auth after privileged action.
- `EVAL-pia-workflow-completeness` — PIA draft answers all E-Government Act § 208 questions: what PII, why, source, sharing, retention, individual rights (access/correction/redress), security measures (NIST control IDs cited).
- `EVAL-il4-il5-data-handling` — if DoD impact level (IL4 = CUI, IL5 = NSS-adjacent) is in scope, data residency is `aws-us-gov-` partition only; no commercial-region failover; FedRAMP+ DoD overlay controls applied; CSP personnel are US-citizens-only where required.
- `EVAL-audit-log-immutability` — AU-9 / AU-12: audit logs are WORM-stored or cryptographically chained (hash-chain or signed append-only). Deletion attempts produce a tamper-evident alert. Retention ≥ 3 years (or longer per data classification).
- `EVAL-supply-chain-sbom` — SR-3 / SR-4 / SR-11: SBOM (CycloneDX or SPDX) generated per build; no components from prohibited-vendor list (Kaspersky, Huawei networking, ZTE, etc. per FAR 52.204-25); transitive dependency provenance is signed (Sigstore / cosign).
- `EVAL-conmon-cadence` — monthly authenticated vulnerability scans, monthly POA&M update, annual control re-assessment, ongoing significant-change reviews. ConMon evidence captured in artefacts/.

## Detection signals

When the scanner sees any of these, this pack auto-attaches:

**Domain / hosting:**
- `.gov`, `.mil`, `.fed.us`, `state.<XX>.us` domain references in code or docs
- `aws-us-gov-east-1`, `aws-us-gov-west-1` region references
- `azure-us-gov-virginia`, `azure-us-gov-arizona` references
- GovCloud SDK imports (`@aws-sdk/*` with GovCloud endpoint config)
- Login.gov / id.me OIDC client config

**Framework references in ARCH/PROJECT.md:**
- "FedRAMP", "StateRAMP"
- "NIST 800-53", "NIST SP 800-53", "NIST 800-171" (CUI)
- "CJIS", "FBI CJIS", "NCIC", "NLETS", "NICS"
- "FISMA", "FISMA-Moderate", "FISMA-High"
- "ATO", "Authorization to Operate", "P-ATO", "JAB"
- "Section 508", "508 compliance", "VPAT", "WCAG 2.2 AA" (in gov context)
- "PIA", "Privacy Impact Assessment", "E-Government Act"
- "PIV", "CAC", "FIPS 201", "phishing-resistant MFA"
- "FIPS 140-2", "FIPS 140-3", "validated cryptographic module"
- "Trusted Internet Connections", "TIC 3.0"
- "OMB Circular A-130", "OMB M-22-09" (Zero Trust)
- "IL4", "IL5", "IL6", "DoD impact level"
- "CUI", "Controlled Unclassified Information"

**Persona references:**
- "federal employee", "state employee", "law enforcement officer", "FBI", "DHS", "IRS agent", "VA clinician", "Medicare contractor"

## Framework reference quick-card

| Framework | Authority | Latest version | Applies when |
|---|---|---|---|
| FedRAMP | OMB / GSA | Rev 5 baselines (Moderate ~325 ctrls, High ~421) | Selling SaaS to federal agencies |
| NIST SP 800-53 | NIST | Rev 5 (2020, errata 2023) | Foundation for FedRAMP + FISMA |
| NIST SP 800-171 | NIST | Rev 3 (2024) | Contractors handling CUI |
| FISMA | Congress (2014 modernization) | — | All federal info systems |
| CJIS Security Policy | FBI | v5.9 (2023) | Any criminal-justice info touch |
| Section 508 ICT Refresh | US Access Board | 2018 update | Federal procurement of EIT |
| WCAG | W3C | 2.2 AA (default) | Section 508 conformance target |
| E-Government Act § 208 | Congress (2002) | — | PIA requirement for new fed IT |
| TIC 3.0 | CISA | 2019 | Federal network connections |
| OMB Circular A-130 | OMB | 2016 | Federal info management baseline |
| OMB M-22-09 | OMB | 2022 | Federal Zero Trust strategy |
| StateRAMP | StateRAMP.org | — | ~25 US states adopted |

## Cost & timeline expectations

Set realistic expectations with the founder before architectural commitments:

- **FedRAMP Tailored** (low-risk SaaS, minimal data): $100K–$300K, ~6 months
- **FedRAMP Moderate Agency ATO**: $500K–$1M, 6–12 months (single sponsoring agency)
- **FedRAMP Moderate JAB P-ATO**: $1M–$2M, 12–24 months (reusable across all agencies)
- **FedRAMP High**: $1.5M–$3M, 18–24+ months (national-security-adjacent data)
- **StateRAMP**: ~50–70% of FedRAMP equivalent cost
- **Annual ConMon + reassessment**: $150K–$400K/year ongoing

If `cost-cap` in PROJECT.md is below these floors, gov-reviewer flags the gap before architectural work begins.

## What NOT to scope into this pack

- General OWASP Top 10 → handled by security-officer / senior-dev base review
- Cloud cost optimization → pm / cost-guard
- HIPAA → `healthcare-pack` (overlays separately if VA / HHS scope)
- PCI DSS → `commerce-pack` / `fintech-pack`
- GDPR / CCPA → `privacy-pack` (state-level PII outside the gov context)

## References

See `agents/gov-reviewer.md` for full regulatory citations, workflow steps, and handoff format.

Key external references:
- FedRAMP marketplace + templates: https://marketplace.fedramp.gov/
- NIST 800-53 Rev 5: https://csrc.nist.gov/publications/detail/sp/800-53/rev-5/final
- NIST 800-171 Rev 3: https://csrc.nist.gov/publications/detail/sp/800-171/rev-3/final
- CJIS Security Policy v5.9: https://www.fbi.gov/services/cjis/cjis-security-policy-resource-center
- Section 508 ICT Refresh: https://www.section508.gov/
- E-Government Act PIA guidance: https://www.justice.gov/opcl/privacy-impact-assessments
- TIC 3.0: https://www.cisa.gov/trusted-internet-connections
- OMB Circular A-130: https://www.whitehouse.gov/wp-content/uploads/legacy_drupal_files/omb/circulars/A130/a130revised.pdf
- StateRAMP: https://stateramp.org/

---
name: edtech-pack
description: Regulatory + compliance overlay for K-12 / higher-ed / online learning products handling student data.
when_to_use: Product collects student PII, processes grades/transcripts, targets users under 18, or operates in US/EU school systems.
applies_to:
  - edtech
extends: []
---

# Edtech Compliance Pack

> Loaded automatically when ARCH or PROJECT.md mentions: kindergarten, school, student, lms, canvas, blackboard, google classroom, clever, classlink, coppa, ferpa, sopipa, or `@studentsfirst/` / `@common-curriculum/` npm scopes.
> Routes through `edtech-reviewer` (threat model) + adds compliance gates specific to products serving minors and integrating with educational institutions.

## Reviewer

- **edtech-reviewer** runs BEFORE senior-dev → writes `TM-edtech-{slug}.md`
- Covers: COPPA (15 USC § 6501), FERPA (20 USC § 1232g), GDPR Article 8, Section 508 ICT Refresh, WCAG 2.2 AA, SOPIPA-CA, NY Ed Law 2-D, CSAM/NCMEC reporting (18 USC § 2258A).

## Human gates added

| Gate | When | Owner |
|---|---|---|
| `gate:coppa-consent` | After TM, before any under-13 account-creation path lands | Privacy/Regulatory lead (human) |
| `gate:ferpa-disclosure` | Before any K-12 / higher-ed integration ships, before student data is transmitted to subprocessors | Privacy/Regulatory lead (human) |
| `gate:ship` | Standard | security-officer |

## Required artefacts in every edtech project

| Artefact | Location | Owner |
|---|---|---|
| COPPA verifiable parental consent workflow (FTC-approved method) | `src/auth/coppa-vpc/` + `docs/compliance/coppa-vpc.md` | senior-dev |
| FERPA directory-information opt-out interface | `src/privacy/ferpa-directory/` | senior-dev |
| GDPR-K (Article 8) age-of-consent geo-router | `src/auth/age-gate/` (per-member-state thresholds) | senior-dev |
| Section 508 + WCAG 2.2 AA accessibility report | `docs/compliance/a11y-report.md` (axe-core + manual NVDA/VoiceOver) | senior-dev + a11y-reviewer |
| Student-data deletion workflow (SOPIPA / NY 2-D / state laws) | `src/privacy/student-deletion/` + `jobs/data-purge/` | senior-dev |
| Vendor Data Protection Addendum (DPA) template for districts | `docs/compliance/dpa-template.md` | architect |
| Subprocessor inventory + flow-down DPAs | `docs/compliance/subprocessors.md` | architect |
| Parents' Bill of Rights (NY 2-D § 2-d) | `public/legal/parents-bill-of-rights.md` | architect |
| Annual privacy + security training attestation | `docs/compliance/training-log.md` | security-officer |

## COPPA Verifiable Parental Consent — accepted methods

FTC-approved per 16 CFR § 312.5(b). Pick at least one:

| Method | Cost/UX | Notes |
|---|---|---|
| Credit-card / debit-card transaction ($0.50+ verification charge, refundable) | Low friction | Most common SaaS path |
| Government-issued ID + facial match (e.g. via Persona, Veriff) | Medium | Delete ID image after verification |
| Signed consent form (mail/fax/email PDF scan) | High friction | Common for school enrolment |
| Toll-free monitored phone call | Medium | Trained staff verify caller |
| Video-conference verification by trained personnel | Medium | Approved 2020 in response to COVID |
| Knowledge-based authentication (KBA) | Medium | Must use out-of-wallet questions |

**NEVER acceptable:** unchecked "I am over 13" checkbox alone, parent-email-confirmation alone (sliding-scale exception only applies if data use is internal-only).

## GDPR Article 8 — digital age-of-consent by member state

Default in regulation: 16. Member states permitted to lower to 13.

| Threshold | Countries |
|---|---|
| 13 | UK (UK GDPR), Belgium, Denmark, Estonia, Finland, Latvia, Malta, Norway, Portugal, Spain, Sweden |
| 14 | Austria, Bulgaria, Cyprus, Italy, Lithuania, Spain (educational context) |
| 15 | Czech Republic, France, Greece, Slovenia |
| 16 (default) | Germany, Hungary, Ireland, Luxembourg, Netherlands, Poland, Romania, Slovakia |

**Implementation:** geo-detect by IP + account-declared country; on conflict, use higher threshold (fail safe). UK ICO has separate guidance under UK GDPR — track separately post-Brexit.

## EVAL suite

| Eval | Target | Pass criterion |
|---|---|---|
| `EVAL-under13-detection` | Age-screen precision/recall on synthetic + real signups | ≥ 0.95 precision, ≥ 0.90 recall against labelled set |
| `EVAL-vpc-flow-integrity` | COPPA VPC workflow end-to-end | No path bypasses verification; revocation propagates within 24h |
| `EVAL-ferpa-directory-roundtrip` | Directory-info opt-out write → read consistency | Opt-out flag honoured on next request; audit log present |
| `EVAL-wcag22-aa-student-screens` | axe-core + pa11y on student-facing routes | ≥ 95% pass rate; zero Critical violations; manual screen-reader spot-check |
| `EVAL-csam-hash-upload` | PhotoDNA / NCMEC hash list check on every user upload | 100% of upload paths covered; NCMEC CyberTipline report drafted within 24h on hit |
| `EVAL-grooming-pattern-flagging` | Adult ↔ minor messaging surfaces (if applicable) | Pattern detector flags known grooming heuristics; human-review queue staffed |
| `EVAL-student-data-deletion` | SOPIPA / NY 2-D student-deletion workflow | Request → confirmed purge across primary + analytics + backups within contractual SLA |
| `EVAL-subprocessor-flowdown` | Every subprocessor handling student PII has signed DPA | 100% coverage; expiration calendar present |

## WCAG 2.2 AA — common edtech failure modes

- **Drag-and-drop interactions** (matching, sorting exercises) without keyboard alternative — violates 2.5.7
- **Math/equation rendering** without ARIA labels or MathML — screen-readers cannot parse
- **Video lessons** without captions or transcripts — violates 1.2.2
- **Colour-only correctness indicators** (red wrong / green right) — violates 1.4.1
- **Custom quiz widgets** with non-visible focus rings — violates 2.4.7 / 2.4.11
- **Timed assessments** without extended-time accommodation — violates 2.2.1 + IDEA accommodations
- **Target size** on tablet/phone < 24×24 CSS px — violates 2.5.8 (new in WCAG 2.2)

## State student-privacy quick matrix

| State | Statute | Key requirement |
|---|---|---|
| California | SOPIPA (BPC § 22584) | No targeted ads, no profiling, no sale of K-12 student PII |
| New York | Ed Law § 2-d | Published Parents' Bill of Rights; specific data-security commitments in contract |
| Connecticut | Pub. Act 16-189 | Public list of contractors + DPA on file |
| Colorado | C.R.S. § 22-16-101 | Annual data-inventory disclosure to districts |
| Utah | Utah Code § 53E-9-301 | Restrictions on metadata + biometric data |
| Maryland | Ed. Article § 4-131 | Operator transparency; opt-out for non-essential uses |
| Illinois | SOPPA (105 ILCS 85) | District contract registry; breach notification within 30 days |

**Default if unknown:** assume California SOPIPA + NY 2-D apply (most restrictive baseline).

## Detection signals (auto-attach triggers)

Pack auto-loads when ANY of the following appears in `ARCH-*.md`, `PROJECT.md`, `README.md`, or `package.json`:

- Keywords: `kindergarten`, `k-12`, `school`, `student`, `teacher`, `classroom`, `curriculum`, `assignment`, `grade`, `transcript`, `lms`, `learning management`
- Platforms: `canvas`, `blackboard`, `google classroom`, `schoology`, `clever`, `classlink`, `powerschool`, `infinite campus`
- Regulatory keywords: `coppa`, `ferpa`, `sopipa`, `ed law 2-d`, `gdpr-k`, `parental consent`
- NPM scopes: `@studentsfirst/`, `@common-curriculum/`, `@instructure/`, `@cleverinc/`, `@google/classroom`
- App-store category: Apple Kids Category / Google Designed for Families
- Age signals: declared target audience under 18 in PROJECT.md `audience:` field

## References

- **COPPA Rule** — 16 CFR Part 312 (15 USC § 6501 et seq.): https://www.ftc.gov/legal-library/browse/rules/childrens-online-privacy-protection-rule-coppa
- **FERPA** — 20 USC § 1232g; 34 CFR Part 99: https://studentprivacy.ed.gov/
- **GDPR Article 8** — digital age of consent: https://gdpr-info.eu/art-8-gdpr/
- **Section 508 ICT Refresh (2018)** — https://www.access-board.gov/ict/
- **WCAG 2.2 (W3C Recommendation, Oct 2023)** — https://www.w3.org/TR/WCAG22/
- **SOPIPA (California)** — Cal. Bus. & Prof. Code § 22584
- **NY Education Law § 2-d + Part 121 regulations** — http://www.nysed.gov/data-privacy-security
- **NCMEC CyberTipline** (18 USC § 2258A reporting): https://report.cybertip.org/
- **PhotoDNA** (Microsoft CSAM hash matching): https://www.microsoft.com/photodna
- **FPF Student Privacy Compass** — state-by-state tracker: https://studentprivacycompass.org/
- Full regulatory citations: `agents/edtech-reviewer.md`

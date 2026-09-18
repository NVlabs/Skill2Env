# TM-hrai-{slug} — HR-AI Threat Model

**Owner:** hr-ai-reviewer  |  **ARCH:** docs/architecture/ARCH-{slug}.md  |  **Date:** {YYYY-MM-DD}  |  **Verdict:** signed-off | blocked

## 1. Scope
- Use case: resume screening · video interview · chatbot recruiting · workforce scheduling · performance review · promotion
- Population (NYC | Illinois | Colorado | EU | other): …
- Biometric data: yes (face / voice / gait) | no

## 2. Applicability matrix
| Regulation | In scope? | Reason |
|---|---|---|
| NYC LL 144 AEDT | | |
| Illinois AIVIA | | |
| Colorado SB 205 (Feb 2026) | | |
| Maryland HB 1202 | | |
| EU AI Act Annex III (Aug 2026) | | |
| GDPR Art. 22 | | |
| Illinois BIPA / Texas CUBI / WA biometric | | |

## 3. Findings
| ID | Finding | Mitigation | Gate |
|---|---|---|---|

## 4. Required artefacts before senior-dev
- [ ] AEDT applicability assessment (in/out)
- [ ] Bias-audit pipeline (4/5-rule, intersectional, annual)
- [ ] Candidate 10-day pre-use notice template + delivery log
- [ ] Per-decision explainability record
- [ ] Disability-accommodation alternative path
- [ ] Resume PDF prompt-injection guardrail
- [ ] GDPR Art. 22 human-review request workflow
- [ ] Annual third-party auditor engaged

## 5. EVAL required
- EVAL-bias-by-protected-class · EVAL-explainability-completeness · EVAL-resume-injection · EVAL-opt-out-honored · EVAL-disability-accommodation

## 6. Gates
- gate:aedt-audit (annual)
- gate:ship

<!-- HANDOFF -->
hr-ai-reviewer-verdict: signed-off
aedt-scope: in | out
critical-findings: 0

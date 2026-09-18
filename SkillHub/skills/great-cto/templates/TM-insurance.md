# TM-insurance-{slug} — Insurance (Claims & Underwriting) Threat Model

**Owner:** insurance-reviewer  |  **ARCH:** docs/architecture/ARCH-{slug}.md  |  **Date:** {YYYY-MM-DD}  |  **Verdict:** signed-off | blocked

> Claims adjudication and underwriting are regulated professional activities; the dominant failure mode
> is **bad-faith / unfair-claims liability and disparate-impact pricing**, not patient harm. This model
> forces a licensed-adjuster/underwriter sign-off into the pipeline.

## 1. Scope
- Pipeline: FNOL / application → coverage check → adjudication / underwriting → pay / deny / bind / price → insured / payer
- Autonomy: suggest-to-adjuster (assistant) · autonomous-above-confidence (autopilot)
- Line of business: p&c · life · health · disability · reinsurance · mga · broker
- Jurisdictions: us-{state(s)} · eu-{country} · uk …
- AI-driven pricing/underwriting? yes | no

## 2. Applicability matrix
| Regime | In scope? | Notes |
|---|---|---|
| State unfair-claims-practices acts (timelines) | | acknowledge/investigate/decide/pay clocks; bad-faith |
| Bad-faith liability (denial/delay/low-ball) | | extra-contractual / punitive, beyond policy limits |
| NAIC Model #170 (Unfair Trade Practices) | | broad anti-discrimination |
| NAIC AI Model Bulletin (AIS Program) | | governance, vendor due-diligence, DOI-exam-ready docs |
| Disparate impact / proxy variables (ZIP/credit) | | CO SB 21-169, NY DFS circular |
| Adjuster / underwriter licensing | | licensee-of-record must be human |
| ERISA / ACA health-claim review | | full-and-fair review, adverse-determination notice, appeals |
| State filing / form / rate filing | | per state DOI |

## 3. Coverage-verification trace (the bad-faith / payment defence)
| Action | Evidence required | Present? |
|---|---|---|
| Pay claim | policy in force + peril covered + within limits | |
| Deny claim | policy term / exclusion + completed investigation + reasonable basis | |
| Bind policy | eligibility + underwriting result + no prohibited proxy | |
| Price / rate | rating factors disparate-impact-clean + ASOP-documented | |

## 4. Edits & guardrails
- State unfair-claims timelines applied pre-action (acknowledge/investigate/decide/pay): …
- Bad-faith guardrail (reasonable-basis + investigation completeness on denial/low-ball): …
- Disparate-impact + proxy-variable (ZIP/credit) testing on pricing/underwriting: …
- ERISA/ACA adverse-benefit-determination notice content + appeal path (if health/disability): …

## 5. Autonomy boundary
- Confidence floor below which an action escalates to a licensed adjuster/underwriter: …
- Bad-faith-high patterns always escalated (denial, low-ball, late decision, autonomous bind): …
- Adjuster/underwriter-of-record audit trail (who/what decided each action): … (composes with service-autopilot audit trail)

## 6. AI governance & filings
- AIS Program + model inventory + DOI-market-conduct-exam-ready documentation (NAIC AI Bulletin): …
- State-by-state filing / licensing tracker (which states in scope, what's filed): …

## 7. Findings
| # | Severity | Finding | Mitigation | Status |
|---|---|---|---|---|
| 1 | | | | open |

## 8. Required gates
- `gate:adjuster-signoff` — licensed adjuster/underwriter signs off below the confidence floor and on every bad-faith-high pattern (denial, low-ball, late decision, autonomous bind).
- `gate:ship` — standard (security-officer).

<!-- HANDOFF -->
insurance-reviewer-verdict: signed-off | blocked
line-of-business: [p&c | life | health | disability | reinsurance | mga | broker]
jurisdictions: [us-<st> | eu-<country> | uk]
bad-faith-high-risk-paths: <count>
critical-findings: <count>
high-findings: <count>
must-implement-before-senior-dev:
  - Coverage-verification trace before any pay/deny (the bad-faith / payment defence)
  - State unfair-claims timeline engine (acknowledge/investigate/decide/pay), pre-action
  - Bad-faith guardrail (reasonable-basis + investigation completeness)
  - Disparate-impact + proxy-variable (ZIP/credit) testing on pricing/underwriting
  - AIS Program + model inventory + DOI-exam-ready documentation (NAIC AI Bulletin)
  - Confidence floor → licensed adjuster/underwriter sign-off (gate:adjuster-signoff)
  - ERISA/ACA adverse-determination notice + appeal path (if health/disability)
gate: gate:adjuster-signoff

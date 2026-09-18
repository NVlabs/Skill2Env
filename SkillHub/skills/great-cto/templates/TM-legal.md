# TM-legal-{slug} — Legal Services / Legal-Tech Threat Model

**Owner:** legal-reviewer  |  **ARCH:** docs/architecture/ARCH-{slug}.md  |  **Date:** {YYYY-MM-DD}  |  **Verdict:** signed-off | blocked

> Practicing law is a licensed activity; the dominant failure mode is **unauthorized practice of law (UPL)
> and breach of fiduciary/trust obligations**, not a security exploit. This model forces an attorney-review
> gate into any client-facing output and a structural trust-accounting guardrail into any client-funds flow.

## 1. Scope
- Pipeline: intake → conflict check → engagement → matter work → client communication / e-filing → closure
- Autonomy: suggest-to-attorney (assistant) · autonomous-above-confidence (autopilot)
- Practice area: litigation · family · immigration · ip · corporate · estate · criminal-defense · general
- Jurisdictions: us-{state(s)} (UPL + trust-accounting rules are state-bar-specific)
- Touches client trust funds (IOLTA)? yes | no
- AI-driven drafting / advice surface? yes | no

## 2. Applicability matrix
| Regime | In scope? | Notes |
|---|---|---|
| Unauthorized practice of law (state bar rules) | | information vs. advice line; structural attorney gate |
| ABA Model Rule 1.15 / state IOLTA rules | | trust vs. operating account separation, no pre-invoice withdrawal |
| ABA Model Rule 1.6 (confidentiality) | | encryption, access control, third-party AI DPA |
| ABA Model Rules 1.7-1.9 (conflicts) | | adverse-party screening before intake finalized |
| FRCP 5.2 / state e-filing redaction rules | | SSN/financial-account/DOB/minor-name redaction pre-submission |
| Records retention & legal hold | | matter-type-specific retention; hold overrides auto-purge |

## 3. UPL surface trace (the information-vs-advice line)
| Output | Client-fact-specific? | Attorney-review gate present? |
|---|---|---|
| Template document fill | | |
| Deadline / docket calculation from published rule | | |
| Recommended course of action / strategy | | |
| Draft legal argument / correspondence | | |

## 4. Trust-accounting trace (if IOLTA in scope)
- Trust account modeled distinct from operating account: …
- Per-client ledger sums reconcilable against trust bank balance: …
- Any withdrawal-before-invoice code path blocked or override-audited: …
- Monthly three-way reconciliation (bank statement / check register / client ledgers) scheduled: …

## 5. Edits & guardrails
- Structural attorney-review gate on client-specific-fact outputs (not just a disclaimer): …
- Conflict-of-interest check blocking intake until conflicts-partner clearance: …
- Matter-level access control (not just firm-level) + outbound metadata scrubbing: …
- Rule 1.6 encryption at rest/in transit + DPA for any third-party AI/vector-store touching matter content: …
- FRCP 5.2 (or state equivalent) redaction gate pre-e-filing-submission (if e-filing in scope): …
- Legal-hold override on auto-purge/retention-expiry jobs: …

## 6. Autonomy boundary
- Confidence floor below which drafting/advice output escalates to a supervising attorney: …
- UPL-high patterns always escalated (strategy recommendation, bespoke argument, fee-structure change): …
- Attorney-of-record audit trail (who/what decided each client-facing output): …

## 7. Findings
| # | Severity | Finding | Mitigation | Status |
|---|---|---|---|---|
| 1 | | | | open |

## 8. Required gates
- `gate:upl-review` — supervising attorney signs off below the confidence floor and on every UPL-high pattern.
- `gate:ship` — standard (security-officer).

<!-- HANDOFF -->
legal-reviewer-verdict: signed-off | blocked
practice-area: [litigation | family | immigration | ip | corporate | estate | criminal-defense | general]
jurisdictions: [us-<state(s)>]
upl-gated-surfaces: <count>
critical-findings: <count>
high-findings: <count>
must-implement-before-senior-dev:
  - Structural attorney-review gate on every client-facing AI/automation output that touches client-specific facts (UPL)
  - Trust vs. operating account separation, per-client ledgers, no pre-invoice fee withdrawal (IOLTA)
  - Monthly three-way reconciliation job (bank statement / check register / client ledgers)
  - Conflict-of-interest check blocking intake until cleared (Model Rules 1.7-1.9)
  - Matter-level access control + metadata scrubbing on outbound documents
  - Rule 1.6 encryption at rest/in transit + DPA for any third-party AI/vector-store touching matter content
  - FRCP 5.2 (or state equivalent) redaction gate before e-filing submission (if e-filing in scope)
  - Legal-hold override on auto-purge/retention-expiry jobs
  - Engagement letter on file required before matter proceeds past intake
gate: gate:upl-review

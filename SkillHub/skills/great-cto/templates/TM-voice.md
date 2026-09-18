# TM-voice-{slug} — Voice/Telephony Threat Model

**Owner:** voice-ai-reviewer
**ARCH ref:** docs/architecture/ARCH-{slug}.md
**Date:** {YYYY-MM-DD}
**Verdict:** signed-off | blocked

---

## 1. Scope

- **Channels:** [ ] outbound voice  [ ] inbound voice  [ ] SMS  [ ] synth TTS  [ ] STT/transcripts  [ ] voice biometric
- **Geography:** US states served / EU member states / CA / UK / other
- **Provider stack:** telephony (Twilio/Bandwidth/…), STT (Deepgram/Whisper/…), TTS (ElevenLabs/Azure/…)
- **Persona of caller:** consumer / business / patient / employee

## 2. Compliance applicability matrix

| Regime | Applies? | Reason |
|---|---|---|
| TCPA (US auto-dialer / pre-recorded) | yes / no | … |
| STIR/SHAKEN attestation | yes / no | … |
| State 2-party recording consent | states: … | … |
| 2024 FCC AI-voice rule | yes / no | synth voice in scope |
| EU AI Act Art. 50 (deepfake disclosure) | yes / no | … |
| CRTC CASL (Canada) | yes / no | … |
| Ofcom CLI (UK) | yes / no | … |
| HIPAA (PHI in voice) | yes / no | … |
| Voice biometrics (BIPA / CUBI / WA) | yes / no | … |

## 3. Findings

### Critical

| ID | Finding | Mitigation | Gate |
|---|---|---|---|
| V-C-1 | … | … | gate:voice-compliance |

### High

| ID | Finding | Mitigation | Gate |
|---|---|---|---|

### Medium / Low

| ID | Finding | Mitigation | Gate |
|---|---|---|---|

## 4. Required artefacts before senior-dev claims tasks

- [ ] Consent schema (`consents` table) with: phone, ts_utc, ip, disclosure_text_sha256, channel, revoked_at
- [ ] Recording-consent geo-router (defaults to two-party if unknown)
- [ ] AI-disclosure script in first 5s of synth-voice call
- [ ] PII-redactor between STT output and LLM context
- [ ] Tool-call confirmation flow for destructive operations
- [ ] STIR/SHAKEN attestation level documented per call source
- [ ] DNC scrub before outbound campaigns (federal + state + internal, ≤31 days fresh)
- [ ] Recording retention policy + encryption-at-rest

## 5. EVAL suite required

- EVAL-voice-pii-leakage
- EVAL-call-handoff-safety
- EVAL-synth-voice-disclosure
- EVAL-multilingual-parity (if non-English in scope)

## 6. Human gates

| Gate | Owner | Trigger |
|---|---|---|
| gate:voice-compliance | regulatory lead | after TM, before senior-dev |
| gate:ship | security-officer | standard |

<!-- HANDOFF -->
voice-ai-reviewer-verdict: signed-off
critical-findings: 0
high-findings: 0

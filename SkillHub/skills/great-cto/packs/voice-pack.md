---
name: voice-pack
description: Regulatory + compliance overlay for voice/telephony products. Pairs with ai-pack (QA extras for ASR/TTS) and voice-ai-reviewer (threat model).
when_to_use: Product places or receives phone calls, runs IVR, uses synthesized voice, or stores audio recordings.
applies_to:
  - ai-system
  - agent-product
extends:
  - ai-pack    # QA: wer / ttfb / barge-in / dtmf
---

# Voice Compliance Pack

> Loaded automatically when ARCH or PROJECT.md mentions: twilio, vonage, livekit, deepgram, elevenlabs, ivr, telephony, phone, tts/stt, voice-agent.
> Routes through `voice-ai-reviewer` (threat model) + adds compliance gates.

## Reviewer

- **voice-ai-reviewer** runs BEFORE senior-dev → writes `TM-voice-{slug}.md`

## Human gates added

| Gate | When | Owner |
|---|---|---|
| `gate:voice-compliance` | After TM, before senior-dev claims tasks | Regulatory lead (human) |
| `gate:ship` | Standard | security-officer |

## Required artefacts in every voice project

| Artefact | Location | Owner |
|---|---|---|
| Consent schema (TCPA PEWC) | `migrations/` | senior-dev |
| Recording-consent geo-router | `src/voice/consent/` | senior-dev |
| AI disclosure script (first 5s) | `src/voice/prompts/disclosure.ts` | ai-prompt-architect |
| PII redactor (STT → LLM) | `src/voice/redact/` | senior-dev |
| DNC scrub job | `jobs/dnc-scrub/` (≤31 days fresh) | senior-dev |
| STIR/SHAKEN attestation log | `docs/compliance/stir-shaken.md` | architect |
| Retention + deletion policy | `docs/compliance/recording-retention.md` | architect |

## EVAL suite (in addition to ai-pack QA)

- `EVAL-voice-pii-leakage` — SSN/CC/DOB not echoed into logs or recordings
- `EVAL-call-handoff-safety` — escalation to human on medical-emergency / suicidal-ideation / fraud cues
- `EVAL-synth-voice-disclosure` — model verifiably says "this is an AI assistant" within first 5s
- `EVAL-multilingual-parity` — quality parity across non-English languages claimed in scope
- `EVAL-prompt-injection-via-voice` — caller dictates "ignore previous instructions" — agent does not comply

## State recording-consent quick matrix

**Two-party (all-party):** CA, CT, DE, FL, IL, MD, MA, MI, MT, NV, NH, PA, WA.
**Default if unknown:** treat as two-party (fail safe).

## Telephony provider HIPAA-eligible matrix

| Provider | HIPAA-eligible product | Notes |
|---|---|---|
| Twilio | Programmable Voice (with BAA) | BAA via Sales; default account NOT eligible |
| Bandwidth | Numbers + Voice (with BAA) | Healthcare-specific tier |
| Vonage | Voice API (with BAA) | Healthcare add-on |
| Telnyx | Voice (with BAA) | |
| LiveKit Cloud | yes (with BAA) | self-host = your own BAA chain |

## References

See `agents/voice-ai-reviewer.md` for full regulatory citations.

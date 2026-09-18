# TM-api-{slug} — API Platform Threat Model

**Owner:** api-platform-reviewer  |  **ARCH:** docs/architecture/ARCH-{slug}.md  |  **Date:** {YYYY-MM-DD}  |  **Verdict:** signed-off | blocked

## 1. Surface
- Style: REST · GraphQL · gRPC · SSE · WebSocket · webhook
- Audience: public · partner · internal
- SDK: auto-gen from OpenAPI/GraphQL? yes / no

## 2. Design checklist
| Item | Status |
|---|---|
| Versioning strategy decided (URL / header / date) | |
| Rate-limit tier matrix | |
| OAuth 2.1 + PKCE for public clients | |
| Granular scopes (no mega-scope) | |
| Idempotency-Key on mutating endpoints | |
| Webhook HMAC-SHA256 + timestamp + 5-min skew | |
| Webhook retry + DLQ policy documented | |
| Sunset header (RFC 8594) policy | |
| Cursor pagination (max page size) | |
| Problem Details (RFC 9457) error envelope | |
| OpenAPI/GraphQL lint in CI | |

## 3. Findings
| ID | Finding | Mitigation | Gate |
|---|---|---|---|

## 4. SLA targets
| Endpoint class | p50 | p95 | p99 | Avail. |
|---|---|---|---|---|
| Read | | | | 99.95% |
| Write | | | | 99.9% |
| Heavy (LLM/upload) | | | | 99.5% |

## 5. EVAL required
- EVAL-rate-limit-fairness · EVAL-webhook-idempotency · EVAL-oauth-scope-leak · EVAL-deprecation-warn · EVAL-pagination-stability

## 6. Gates
- gate:api-contract (v1 surface sign-off)
- gate:ship

<!-- HANDOFF -->
api-platform-reviewer-verdict: signed-off
critical-findings: 0

---
name: api-platform-pack
description: API platform / dev-API overlay. Pairs api-platform-reviewer.
when_to_use: Product exposes public or partner API (REST / GraphQL / gRPC / webhooks) as a primary surface.
applies_to:
  - devtools
  - library
  - ai-system
  - agent-product
  - web-service
extends:
  - devtools-pack
---

# API Platform Pack

> Loaded when ARCH mentions: public API, partner API, REST, GraphQL, gRPC, webhook, SDK, OpenAPI, developer portal.

## Reviewer

- **api-platform-reviewer** → `TM-api-{slug}.md`

## Human gates added

| Gate | When | Owner |
|---|---|---|
| `gate:api-contract` | Before v1 GA — sign-off on public surface | architect + DX-lead |
| `gate:ship` | Standard | security-officer |

## Required artefacts

| Artefact | Owner |
|---|---|
| Versioning strategy doc (URL / header / date-based) | architect |
| Rate-limit tier matrix per resource | senior-dev |
| OAuth 2.1 + PKCE for public clients | senior-dev |
| Idempotency-Key support on mutating endpoints | senior-dev |
| Webhook spec (HMAC-SHA256 + timestamp + 5min skew + retry) | senior-dev |
| Sunset header (RFC 8594) + ≥6-month deprecation policy | architect |
| OpenAPI / GraphQL spec lint in CI (Spectral / graphql-inspector) | senior-dev |
| Cursor pagination (max page size) | senior-dev |
| Problem Details (RFC 9457) error envelope | senior-dev |
| Status page + machine-readable changelog | devops |

## EVAL suite

- `EVAL-rate-limit-fairness` (per-tenant noise isolation)
- `EVAL-webhook-idempotency` (duplicate delivery doesn't double side-effects)
- `EVAL-oauth-scope-leak` (token from tenant A can't access tenant B)
- `EVAL-deprecation-warn` (Sunset header present on deprecated routes)
- `EVAL-pagination-stability` (concurrent inserts don't break pagination)

## Anti-patterns to block in review

- Global rate-limit across all tenants (noisy-neighbor blast radius)
- Mega-scope `api:*` instead of granular scopes
- JWT with `alg: none` accepted
- Offset pagination on growing collections
- Wildcard CORS `*` with credentials

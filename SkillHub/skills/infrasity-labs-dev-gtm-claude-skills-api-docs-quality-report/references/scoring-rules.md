# Scoring Rules Reference

Complete PASS / WARN / FAIL criteria for each of the 5 audit checks.
Read this file before scoring any endpoint.

---

## CHECK 1 — Endpoint Description

Evaluates the **prose text** above the OpenAPI block on the page.
This is the human-written description — not the OpenAPI `summary` or `description` field.

| Status | Criteria |
|---|---|
| ✅ PASS | ≥ 2 sentences of real context. Explains **what** the endpoint does, **when** to use it, and any **important behaviour** (async, side effects, prerequisites, auth requirements). |
| ⚠️ WARN | 1 sentence or only restates the endpoint title. Covers what it does but misses context, prerequisites, or important behaviour. |
| ❌ FAIL | No prose description at all. Or description is copy-pasted from another API (e.g. OpenAI docs text on a proxy endpoint). Or only the OpenAPI `summary` repeated. |

**Worked examples:**

```
PASS: "Execute an agent by submitting to Temporal workflow. This creates an execution
record and starts a Temporal workflow. The actual execution happens asynchronously on
the Temporal worker. The runner_name should come from the Composer UI where user selects
from available runners."

WARN: "Create a new agent in the organization."

FAIL: (no text above OpenAPI block)
FAIL: (text is verbatim copy of OpenAI documentation)
```

**Special cases:**
- Health check endpoints with "no auth required" and no params: PASS for minimal descriptions
- Deprecated endpoints: always WARN if no deprecation callout, regardless of description quality

---

## CHECK 2 — OpenAPI Spec

Evaluates whether a machine-parseable API spec is present and accessible.

| Status | Criteria |
|---|---|
| ✅ PASS | Inline OpenAPI YAML or JSON block is present on the page AND is valid (has `paths`, `components` or `schemas` sections). Canonical spec URL (if referenced) is accessible and returns valid JSON/YAML. |
| ⚠️ WARN | Inline spec is present but incomplete (references `$ref` components not defined on the page, or missing `components/schemas`). OR canonical spec URL is referenced but returns a non-200 status. |
| ❌ FAIL | No inline spec block on the page. No canonical spec accessible. Page is docs-only with no machine-readable schema. |

**Notes:**
- If the canonical spec is 404 but inline YAML is present on every page: Check 2 = PASS on
  individual pages, but flag the 404 canonical spec as a TOP ISSUE (it blocks SDK generation).
- OpenAPI 3.0.x and 3.1.x are both valid. Swagger 2.0 is WARN (outdated format).

---

## CHECK 3 — Body Param Descriptions

Evaluates how well the **request body fields and parameters** are documented.

Applies to: all fields in `requestBody.content.application/json.schema`, all path params,
all query params.

| Status | Criteria |
|---|---|
| ✅ PASS | Every field has a `description` string. Required vs optional is explicit (`required: true/false` or listed in `required: []`). Enum values are explained. Nested objects have their children described. No fields typed as `additionalProperties: true` without explanation. |
| ⚠️ WARN | ≥ 70% of fields have descriptions, but some are missing. OR at least one key field uses `additionalProperties: true` but other fields are well-documented. OR an important parameter's valid values / format are not documented (e.g. a UUID field with no hint it's a UUID). |
| ❌ FAIL | The entire request body is `additionalProperties: true` (free-form object). OR < 50% of fields have descriptions. OR a required field has no description at all. OR the request body schema is `type: object` with no properties defined. |

**Common patterns that trigger FAIL:**
```yaml
# FAIL — free-form body
requestBody:
  content:
    application/json:
      schema:
        type: object
        additionalProperties: true

# FAIL — required field with no description
properties:
  worker_queue_id:
    type: string
    title: Worker Queue Id
    # no description field
    required: true

# WARN — important nested object opaque
properties:
  configuration:
    type: object
    additionalProperties: true   ← no children documented
    description: Agent configuration
```

**Special cases:**
- Endpoints with no request body (GET, DELETE with path params only):
  Still check path/query params. If all are described → PASS. If missing → WARN/FAIL.
- If a field references another endpoint for valid values, the description should
  say so (e.g. "Use GET /api/v1/worker-queues to get valid IDs"). Missing this = WARN.

---

## CHECK 4 — Response Codes

Evaluates whether the **HTTP error responses** are documented in the spec.

| Status | Criteria |
|---|---|
| ✅ PASS | Documents `200`/`201` AND all applicable error codes for the endpoint type (see table below). Each error code has a description and ideally an error schema. |
| ⚠️ WARN | Documents `200`/`201` AND `422` only (FastAPI auto-generated). OR documents 2-3 error codes but misses important ones for the endpoint type. |
| ❌ FAIL | Documents `200`/`201` only, with no error codes. OR documents only `200` (not even 422). |

**Required error codes by endpoint type:**

| Endpoint type | Minimum required error codes |
|---|---|
| Any authenticated endpoint | 401 (auth failure) |
| Resource by ID (GET/PUT/DELETE) | 401, 404 (not found) |
| Create resource (POST) | 400 (invalid input), 401, 409 (conflict/duplicate) |
| Any endpoint | 500 (internal error) |
| Rate-limited endpoint | 429 |
| Auth-changing operations | 403 (forbidden) |
| Temporal/async operations | 503 (no workers) |
| Streaming (SSE) endpoints | 404 (resource not found before streaming) |

**Notes:**
- `422` (FastAPI validation) alone does NOT count as having error codes — it's auto-generated
  and doesn't communicate business logic errors
- Error codes mentioned **only in prose** but not in the spec responses block = WARN
  (better than nothing, but not machine-readable)

---

## CHECK 5 — Response Schema

Evaluates whether the **successful response body** is documented.

| Status | Criteria |
|---|---|
| ✅ PASS | The `200`/`201` response has a full typed schema — either inline or via `$ref` to a defined component. All response fields have types. Key fields have descriptions. Nested objects have their children defined. |
| ⚠️ WARN | Schema exists but is incomplete. Uses `additionalProperties: true` for significant portions of the response. References `$ref` that is not resolvable on this page. OR partial schema — top-level fields defined but nested objects opaque. |
| ❌ FAIL | `schema: {}` — completely empty schema. OR `schema: {type: object}` with no properties. OR no response schema at all. OR `additionalProperties: true` at the top level (entire response is a free-form object). |

**Worked examples:**

```yaml
# FAIL — empty schema
responses:
  '200':
    description: Successful Response
    content:
      application/json:
        schema: {}

# FAIL — additionalProperties at top level  
responses:
  '200':
    description: Response
    content:
      application/json:
        schema:
          type: object
          additionalProperties: true

# WARN — partial schema
responses:
  '200':
    content:
      application/json:
        schema:
          type: object
          properties:
            result:
              type: object
              additionalProperties: true   ← nested object opaque

# PASS
responses:
  '201':
    content:
      application/json:
        schema:
          $ref: '#/components/schemas/AgentResponse'
# ...where AgentResponse has all fields defined
```

**Special cases:**
- Streaming (SSE) endpoints: FAIL if `schema: {}` even if SSE format is documented in prose.
  The prose docs need to be reflected in a formal schema.
- DELETE endpoints that return 204 No Content: PASS (no body is correct).
- Health check endpoints returning minimal `{status: string}`: PASS if that schema is defined.
- Validate Token with `additionalProperties: true` when 7 fields are documented in prose: WARN
  (the info exists but not in the schema).

---

## COMPOSITE SCORING

After all 5 checks are scored for an endpoint, assign the endpoint's **overall status**:

| Overall | Rule |
|---|---|
| ✅ PASS | All 5 checks are PASS |
| ⚠️ WARN | At least one WARN, zero FAILs |
| ❌ FAIL | At least one FAIL |

**Category score** = count of endpoint-level PASS / WARN / FAIL within that category.

**Overall score** = sum across all categories.

---

## SITE-WIDE PATTERN DETECTION THRESHOLDS

| Pattern | FAIL threshold | WARN threshold |
|---|---|---|
| Missing error codes | ≥ 80% of endpoints only have 200+422 | 60–79% |
| Empty response schemas | ≥ 50% of endpoints have `schema: {}` | 30–49% |
| Free-form request bodies | ≥ 40% have `additionalProperties: true` at body root | 20–39% |
| One-liner descriptions | ≥ 60% have descriptions ≤ 10 words | 40–59% |
| Spec unavailable | Canonical spec 404 AND inline spec missing on ≥ 30% of pages | |

Only report a site-wide pattern if it meets the threshold. Do not fabricate patterns.
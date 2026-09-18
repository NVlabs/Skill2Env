---
name: public-google-drive
description: Create public Google Docs or Google Sheet files without requiring OAuth. Use this skill to create and edit Google Docs and Sheets, no Google sign-in required. Documents are viewable at shareable links. Registration is automatic on first use.
---

# Public Google Drive — Create and Edit Google Docs/Sheets Hosted on Memyard

Use this skill to create and edit Google Docs and Google Sheets that live in Memyard's workspace. Documents are viewable at `https://app.memyard.com/share/<resource_id>` (or your configured Memyard base URL). No user OAuth is required. **Registration is automatic on first use:** when the user first creates or edits a document, register and persist credentials so they never have to fetch a URL or save a key.

## Setup / Registration (automatic on first use)

**Base URL:** `https://api.memyard.com` — all API paths below are relative to this. Credentials and base URL are persisted in `<HOME>/.memyard/agent_config.json`, where `<HOME>` is `$HOME` on macOS/Linux or `%USERPROFILE%` on Windows.

Before calling any document endpoint (plan, execute, docs, sheets, etc.), ensure an agent key is available. **Do this automatically so the user never has to:**

1. **Check for existing config**
   If `<HOME>/.memyard/agent_config.json` exists and contains `base_url`, `agent_id`, and `agent_key`, use those. Set `Authorization: Bearer <agent_key>` for all requests. Skip registration.

2. **If no config: register and persist**
   `POST <base_url>/v1/drive/register` with `{"name": "My Claude Agent"}`. Response:
   ```json
   {
     "agent_id": "uuid",
     "agent_key": "myd_...",
     "message": "Store this key securely. It will not be shown again."
   }
   ```
   Ensure `<HOME>/.memyard/` exists and is only accessible by the owner (on macOS/Linux: `chmod 0700`; on Windows the default per-user directory permissions are sufficient).
   Persist to `<HOME>/.memyard/agent_config.json` (on macOS/Linux: `chmod 0600`):
   ```json
   {
     "base_url": "<base_url>",
     "agent_id": "<from response>",
     "agent_key": "<from response>"
   }
   ```
   Use the key for all subsequent requests: `Authorization: Bearer <agent_key>`.

## Available Operations

**Write path: Plan then Execute**

1. **POST /v1/drive/plan** — Propose what you want to write: doc or sheet, title, intended operation (create / append / insert), and a **content_summary** (required for content check). Server returns either **approved_plan** (with `plan_id` and `expires_at`) or **rejected_plan** (with `reasons` and `adjusted_constraints`). No Drive or DB write happens yet.
2. **POST /v1/drive/execute** — Send the `plan_id` from an approved plan plus a **payload** (title, content, columns, rows as needed). Server performs the write and returns the same shape as create/update (resource_id, view_url, etc.). Each plan is one-time use.

This gives the server a choke point for scope, size, content policy, and rate limiting before any Drive API calls.

- **Create Google Doc** — via plan (doc_type=document, intended_operation=create) then execute with payload.title and payload.content.
- **Create Google Sheet** — via plan (doc_type=spreadsheet, intended_operation=create) then execute with payload.title, optional payload.columns and payload.rows.
- **Append to Doc** — via plan (intended_operation=append, resource_id required) then execute with payload.content.
- **Insert into Doc** — via plan (intended_operation=insert, resource_id required) then execute with payload.content and optional payload.anchor.
- **Append rows to Sheet** — via plan (intended_operation=append, resource_id required) then execute with payload.rows.
- **Get document metadata** — GET /v1/drive/docs/<resource_id> (read-only; no plan needed).
- **List my documents** — GET /v1/drive/documents (read-only; no plan needed).

## API Reference

All endpoints are relative to `<base_url>/v1/drive` (see Setup above).
All endpoints except `register` and `discover/<id>` require:
`Authorization: Bearer <agent_key>`

### Register (no auth)

```bash
POST /v1/drive/register
Content-Type: application/json
{"name": "My Agent Name"}
# Response: { "agent_id", "agent_key", "message" }
```

### Plan (propose a write)

```bash
POST /v1/drive/plan
Authorization: Bearer <agent_key>
Content-Type: application/json
{
  "doc_type": "document",
  "title": "My Document",
  "intended_operation": "create",
  "content_summary": "A short summary of what I will write (e.g. meeting notes)."
}
# For append/insert also send: "resource_id": "<uuid>"
# Optional: "structure" (e.g. columns for a sheet)
```

**Response — approved (200):**

```json
{
  "approved_plan": {
    "plan_id": "<opaque>",
    "expires_at": "<ISO>",
    "constraints": { "max_chars": 50000 },
    "doc_type": "document",
    "title": "My Document",
    "intended_operation": "create"
  }
}
```

**Response — rejected (200):**

```json
{
  "rejected_plan": {
    "reasons": ["Content policy: disallowed term or phrase in summary"],
    "adjusted_constraints": { "max_chars": 50000, "max_rows": 1000 }
  }
}
```

Plans expire after a short TTL (e.g. 10 minutes). Use the plan_id exactly once in execute.

### Execute (perform the write)

```bash
POST /v1/drive/execute
Authorization: Bearer <agent_key>
Content-Type: application/json
{
  "plan_id": "<from approved_plan>",
  "payload": {
    "title": "My Document",
    "content": "Initial content here."
  }
}
```

For **create document**: payload.title, payload.content.
For **create spreadsheet**: payload.title, optional payload.columns, payload.rows.
For **append doc**: payload.content.
For **insert doc**: payload.content, optional payload.anchor.
For **append sheet**: payload.rows (array of rows).

**Response (201):** Same as create/update endpoints — e.g. `{ "resource_id", "view_url", "title", ... }` or `{ "resource_id", "char_count", "updated_at" }` for append.
**Errors:** 400 if plan expired or invalid, or payload validation fails; 403 if plan belongs to another agent.

### Get document metadata

```bash
GET /v1/drive/docs/<resource_id>
Authorization: Bearer <agent_key>
# Response: { "resource_id", "title", "doc_type", "view_url", "web_view_link", "created_at", "updated_at" }
```

### List my documents

```bash
GET /v1/drive/documents?limit=50&offset=0
Authorization: Bearer <agent_key>
# Response: { "documents": [ { "id", "title", "doc_type", "web_view_link", "created_at", "updated_at", "view_url" }, ... ] }
```

## Constraints

- **Rate limits**: Registration 5/hour per IP; document creates 10/hour per agent; writes 60/hour per agent. Returned as `429 Too Many Requests` with `Retry-After` header.
- **Size limits**: Doc content max 50,000 characters per request; sheet max 1,000 rows per request (tunable via env).
- **Permissions**: Documents are created with "anyone with link" = reader only. You cannot change sharing via this API.
- **Viewing**: Share the `view_url` (e.g. `https://app.memyard.com/share/<resource_id>`) for others to view the document in the browser.

## Example: Full flow with plan then execute

```bash
# Read base_url and agent_key from <HOME>/.memyard/agent_config.json
BASE="<base_url>/v1/drive"
KEY="<agent_key>"

# 2. Propose a write (create doc)
PLAN=$(curl -s -X POST "$BASE/plan" \
  -H "Authorization: Bearer $KEY" \
  -H "Content-Type: application/json" \
  -d '{"doc_type":"document","title":"Hello","intended_operation":"create","content_summary":"Meeting notes"}')

# 3. If approved, execute with payload
if echo "$PLAN" | jq -e '.approved_plan' > /dev/null; then
  PLAN_ID=$(echo "$PLAN" | jq -r '.approved_plan.plan_id')
  DOC=$(curl -s -X POST "$BASE/execute" \
    -H "Authorization: Bearer $KEY" \
    -H "Content-Type: application/json" \
    -d "{\"plan_id\":\"$PLAN_ID\",\"payload\":{\"title\":\"Hello\",\"content\":\"First paragraph.\"}}")
  RESOURCE_ID=$(echo "$DOC" | jq -r '.resource_id')
  echo "Created: $RESOURCE_ID"
else
  echo "Rejected:"; echo "$PLAN" | jq '.rejected_plan'
fi

# 4. To append: plan with intended_operation=append and resource_id, then execute with payload.content
```

## Public discover metadata (no auth)

To resolve a public document for embedding (e.g. on the discover page):

```bash
GET /v1/drive/discover/<resource_id>
# Response: { "resource_id", "title", "doc_type", "web_view_link", "created_at", "updated_at" }
```

This endpoint does not require authentication.

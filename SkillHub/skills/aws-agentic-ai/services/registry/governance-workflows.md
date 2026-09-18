# Agent Registry - Governance Workflows

Agent Registry provides a governance layer with configurable approval workflows to ensure only reviewed, curated resources are discoverable across your organization.

## Record Lifecycle

```
Create → DRAFT → Submit → PENDING_APPROVAL → Approve → APPROVED
                                │                         │
                                │ Reject                  │ Edit (new DRAFT revision;
                                ▼                         │ approved stays in search)
                           REJECTED ── Approve (direct) ──┘
                                │
                                └── Edit → DRAFT

Any status → DEPRECATED (terminal, irreversible)
```

### Status Details

| Status | Visible in Search | Can Edit | Can Submit | Notes |
|--------|-------------------|----------|------------|-------|
| **Draft** | No | Yes (in place) | Yes | Initial state after create |
| **Pending Approval** | No | Yes (creates new DRAFT; pending revision discarded) | No | Awaiting curator review |
| **Approved** | **Yes** | Yes (creates new DRAFT; approved stays active) | No | Discoverable by consumers |
| **Rejected** | No | Yes (creates new DRAFT) | Via new DRAFT | Curator can directly approve |
| **Deprecated** | No | **No** | **No** | Terminal — irreversible |

### Dual-Revision Behavior

When editing an **Approved** record, the system creates a new DRAFT revision while the approved revision **remains visible in search**. The new DRAFT must go through the normal submit-and-approve flow. This ensures consumers always have access to the last approved version during updates.

### Visibility Rules

| API | What It Returns |
|-----|-----------------|
| `SearchRegistryRecords` | Only approved revisions |
| `InvokeRegistryMcp` | Only approved revisions |
| `GetRegistryRecord` | Latest revision (any status) |
| `ListRegistryRecords` | Latest revision (any status) |

## Approval Modes

### Auto-Approval

Records are automatically approved upon submission. Suitable for development environments or trusted teams.

```bash
aws bedrock-agentcore-control create-registry \
  --name "dev-registry" \
  --description "Development registry with auto-approval" \
  --approval-configuration '{"autoApproval": true}' \
  --region us-east-1
```

> **Note**: Switching auto-approval from OFF to ON only affects records submitted after the change. Existing `PENDING_APPROVAL` records must still be manually approved or rejected.

### Manual Approval (Default)

Records require curator review. Suitable for production registries and organization-wide catalogs.

## Curator Workflows

### Review Pending Records

```bash
# List all records (filter output for pending status)
aws bedrock-agentcore-control list-registry-records \
  --registry-id <REGISTRY_ID> \
  --region us-east-1
```

```bash
# Get full details of a pending record
aws bedrock-agentcore-control get-registry-record \
  --registry-id <REGISTRY_ID> \
  --record-id <RECORD_ID> \
  --region us-east-1
```

### Approve a Record

```bash
aws bedrock-agentcore-control update-registry-record-status \
  --registry-id <REGISTRY_ID> \
  --record-id <RECORD_ID> \
  --status APPROVED \
  --status-reason "Schema validated, tool descriptions are clear, team ownership confirmed" \
  --region us-east-1
```

> **Note**: Curators can directly approve a **Rejected** record without the publisher needing to resubmit.

### Reject a Record

```bash
aws bedrock-agentcore-control update-registry-record-status \
  --registry-id <REGISTRY_ID> \
  --record-id <RECORD_ID> \
  --status REJECTED \
  --status-reason "Tool descriptions are too vague - please add input/output examples" \
  --region us-east-1
```

### Deprecate a Record

Deprecation is available from **any status** and is a **terminal, irreversible** operation. The record cannot be edited or un-deprecated. It remains visible via `GetRegistryRecord` and `ListRegistryRecords` for auditing but is removed from search.

```bash
aws bedrock-agentcore-control update-registry-record-status \
  --registry-id <REGISTRY_ID> \
  --record-id <RECORD_ID> \
  --status DEPRECATED \
  --status-reason "Replaced by payments-mcp-server-v3 (rec-newid). Migrate by 2026-06-01." \
  --region us-east-1
```

## EventBridge Automation

Agent Registry emits events to the default EventBridge bus (source: `aws.bedrock-agentcore`).

### Event Types

| Detail Type | Trigger |
|-------------|---------|
| `Registry Record State changed to Pending Approval` | `submit-registry-record-for-approval` called |
| `Registry State transitions from Creating to Ready` | Registry provisioning completes |

### Event Schema

```json
{
  "version": "0",
  "detail-type": "Registry Record State changed to Pending Approval",
  "source": "aws.bedrock-agentcore",
  "account": "<account-id>",
  "region": "us-west-2",
  "resources": [
    "arn:aws:bedrock-agentcore:us-west-2:<account-id>:registry/REG_ID/record/REC_ID"
  ],
  "detail": {
    "registryRecordId": "REC_ID",
    "registryId": "REG_ID"
  }
}
```

### Pattern 1: Slack Notification on Submission

```json
{
  "source": ["aws.bedrock-agentcore"],
  "detail-type": ["Registry Record State changed to Pending Approval"],
  "detail": {
    "registryId": ["reg-abc123def456"]
  }
}
```

**Lambda Handler** (Python):
```python
import json
import urllib3
import boto3

SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/T.../B.../xxx"
client = boto3.client("bedrock-agentcore-control")

def handler(event, context):
    detail = event["detail"]
    registry_id = detail["registryId"]
    record_id = detail["registryRecordId"]

    # Fetch record details for the notification
    record = client.get_registry_record(
        registryId=registry_id,
        recordId=record_id
    )

    message = {
        "text": f":clipboard: New registry record pending approval\n"
                f"*Record*: {record['name']}\n"
                f"*Type*: {record['descriptorType']}\n"
                f"*Registry*: {registry_id}\n"
                f"*Record ID*: {record_id}"
    }
    http = urllib3.PoolManager()
    http.request("POST", SLACK_WEBHOOK_URL,
                 body=json.dumps(message),
                 headers={"Content-Type": "application/json"})
```

### Pattern 2: Automated Schema Validation

Automatically validate MCP server schemas before curator review.

**EventBridge Rule** (target: Lambda):
```json
{
  "source": ["aws.bedrock-agentcore"],
  "detail-type": ["Registry Record State changed to Pending Approval"]
}
```

**Lambda Handler** (Python):
```python
import json
import boto3

client = boto3.client("bedrock-agentcore-control")

def handler(event, context):
    detail = event["detail"]
    registry_id = detail["registryId"]
    record_id = detail["registryRecordId"]

    # Get the full record
    record = client.get_registry_record(
        registryId=registry_id,
        recordId=record_id
    )

    # Only auto-validate MCP records
    if record.get("descriptorType") != "MCP":
        return  # Leave non-MCP records for manual review

    # Validate MCP schema has required fields
    descriptors = record.get("descriptors", {})
    mcp = descriptors.get("mcp", {})
    tools_content = mcp.get("tools", {}).get("inlineContent", "{}")
    tools_data = json.loads(tools_content)

    issues = []
    tools = tools_data.get("tools", [])
    if not tools:
        issues.append("No tools defined in MCP server schema")

    for tool in tools:
        if not tool.get("description"):
            issues.append(f"Tool '{tool.get('name', 'unnamed')}' missing description")
        if not tool.get("inputSchema"):
            issues.append(f"Tool '{tool.get('name', 'unnamed')}' missing inputSchema")

    if issues:
        client.update_registry_record_status(
            registryId=registry_id,
            recordId=record_id,
            status="REJECTED",
            statusReason=f"Auto-validation failed: {'; '.join(issues)}"
        )
    else:
        client.update_registry_record_status(
            registryId=registry_id,
            recordId=record_id,
            status="APPROVED",
            statusReason="Auto-validated: all tools have descriptions and input schemas"
        )
```

### Pattern 3: Step Functions Review Pipeline

For complex multi-step review processes:

```
┌──────────────┐     ┌───────────────┐     ┌──────────────┐
│ EventBridge  │ ──> │ Step Function │ ──> │ Auto-validate│
│ (submission) │     │ (orchestrate) │     │ (Lambda)     │
└──────────────┘     └───────────────┘     └──────┬───────┘
                                                   │
                                          ┌────────┴────────┐
                                          │                 │
                                     Pass ▼            Fail ▼
                              ┌──────────────┐   ┌──────────────┐
                              │ Notify Slack │   │ Reject with  │
                              │ for human    │   │ feedback     │
                              │ review       │   └──────────────┘
                              └──────────────┘
```

## Governance Best Practices

### For Administrators
- Use **manual approval** for production registries
- Use **auto-approval** only for dev/sandbox environments
- Set up EventBridge rules for all submission events
- Assign dedicated curator IAM roles per registry (use `bedrock-agentcore:UpdateRegistryRecordStatus` scoped to specific registry ARN)

### For Publishers
- Write detailed, searchable descriptions
- Include all tool descriptions and input schemas for MCP servers
- Use semantic versioning for record versions
- Include migration notes when deprecating records

### For Curators
- Always provide actionable `statusReason` when rejecting
- Verify schema completeness (tools have descriptions, inputs documented)
- Check for duplicate resources before approving
- **Deprecate** rather than delete when replacing records (preserves audit trail)
- Use **direct approve** for rejected records when the publisher has fixed issues out-of-band

### Review Checklist

Before approving a record, verify:

- [ ] **Description** is clear and searchable (max 4,096 chars)
- [ ] **Version** follows semantic versioning
- [ ] **Schema** (for MCP/A2A types) is valid and complete
- [ ] **Tool descriptions** are specific enough for AI agents to understand
- [ ] **No duplicates** of existing approved records
- [ ] **Team ownership** is identifiable from the record name/description

## CloudTrail Audit

All approval actions are logged in CloudTrail:

```bash
aws cloudtrail lookup-events \
  --lookup-attributes AttributeKey=EventName,AttributeValue=UpdateRegistryRecordStatus \
  --region us-east-1
```

## Related

- [Registry Overview](README.md)
- [Getting Started](getting-started.md)
- [Record Lifecycle (AWS Docs)](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/registry-record-lifecycle.html)
- [EventBridge Notifications (AWS Docs)](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/registry-eventbridge.html)

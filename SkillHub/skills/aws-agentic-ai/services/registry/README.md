# Agent Registry Service

> **Status**: Preview (launched April 9, 2026)

## Overview

AWS Agent Registry is a fully managed discovery service within Amazon Bedrock AgentCore. It provides a private, governed catalog for organizing, curating, and discovering AI agents, MCP servers, tools, agent skills, and custom resources across an organization.

**Problem it solves**: As organizations scale AI agents and tools, resources become siloed across teams. Teams build MCP servers, deploy agents, and create specialized tools, but without a central catalog, duplication of effort occurs because builders cannot discover what already exists.

## Regional Availability

| Region | Code |
|--------|------|
| US East (N. Virginia) | `us-east-1` |
| US West (Oregon) | `us-west-2` |
| Europe (Ireland) | `eu-west-1` |
| Asia Pacific (Tokyo) | `ap-northeast-1` |
| Asia Pacific (Sydney) | `ap-southeast-2` |

## Core Concepts

### Registries

Top-level catalogs in your AWS account. Each registry has its own:
- Name and description
- Authorization configuration (IAM or JWT) — **cannot be changed after creation**
- Approval settings (auto-approve or manual review)
- Set of registry records

**Naming**: Must start alphanumeric. Valid characters: `a-z`, `A-Z`, `0-9`, `_`, `-`, `.`, `/`. Max 64 characters.

Organize registries by resource type, environment stage (prod/QA/dev), team, or use a single org-wide registry.

### Registry Records

Metadata entries describing individual resources. Each record has:
- **Name** (max 255 chars) and **description** (max 4,096 chars)
- **Version** (semantic versioning recommended)
- **Descriptor type** (`MCP`, `A2A`, `SKILL`, `CUSTOM`)
- **Type-specific metadata** (protocol definitions, tool schemas, etc.)

### Resource Types

| Descriptor Type | Description | Validation |
|-----------------|-------------|------------|
| **`MCP`** | MCP server + tool definitions | Validated against MCP protocol schema (multiple schema versions supported) |
| **`A2A`** | Agent cards per A2A protocol spec | Validated against A2A agent card schema (version `0.3`) |
| **`SKILL`** | Reusable capabilities with markdown documentation | Optional structured definition (schema `0.1.0`) |
| **`CUSTOM`** | Any JSON metadata for resources that don't fit standard types | No validation (free-form JSON) |

### Record Lifecycle

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

- **Draft**: Initial state. Not visible in search.
- **Pending Approval**: Submitted for review. Not visible in search.
- **Approved**: Visible in search results. Editing creates a new DRAFT revision while the approved revision stays active.
- **Rejected**: Curator can directly approve, or publisher can edit (creates new DRAFT) and resubmit.
- **Deprecated**: Terminal state — cannot be undone or edited. Removed from search but visible via `GetRegistryRecord` and `ListRegistryRecords` for auditing.

### Key Personas

| Persona | Responsibilities |
|---------|-----------------|
| **Administrator** | Creates registries, configures auth/approval, manages IAM permissions |
| **Publisher** | Creates records for their resources, submits for approval, configures sync |
| **Curator/Approver** | Reviews pending records, approves/rejects/deprecates based on org standards |
| **Consumer** | Searches for and discovers approved resources (human or agent) |

## Key Capabilities

### Hybrid Search

Combines semantic (vector-based, natural language) search with keyword matching. Both run simultaneously on every query with results ranked by weighted combination.

**Ranking**: Name has strongest keyword influence, followed by description and descriptor content (equal weight).

**Metadata filters** constrain results using operators:
- `$eq`, `$ne` — Equals / not equals
- `$in` — In list
- `$and`, `$or` — Logical combinators

Filterable fields: `name`, `descriptorType`, `version`.

### MCP-Native Access

Each registry exposes an MCP-compatible endpoint (MCP spec 2025-11-25):

```
https://bedrock-agentcore.<region>.amazonaws.com/registry/<registryId>/mcp
```

The endpoint provides one tool: `search_registry_records` with parameters:
- `searchQuery` (required) — Natural language or keyword query (1-256 chars)
- `maxResults` (1-20, default 10) — Number of results to return
- `filter` (optional) — Metadata filter object

Any MCP-compatible client (Claude Code, Kiro, etc.) can connect directly.

See [MCP Endpoint Guide](mcp-endpoint.md) for detailed configuration.

### Governance and Curation

Configurable approval workflow with auto-approval or manual curator review.

See [Governance Workflows](governance-workflows.md) for details.

### Record Synchronization

Pull metadata from live external MCP servers or A2A agent endpoints via URL-based discovery. Supports OAuth and IAM credential providers for outbound authorization. Creates new revisions automatically when upstream changes.

See [Sync Configuration](sync-configuration.md) for details.

### EventBridge Notifications

Events sent to default EventBridge bus (source: `aws.bedrock-agentcore`) when:
- Records are submitted for approval (`detail-type: "Registry Record State changed to Pending Approval"`)
- Registries finish provisioning (`detail-type: "Registry State transitions from Creating to Ready"`)

Enables automated review pipelines via Lambda, SNS, SQS, or Step Functions.

### CloudTrail Audit

All control plane API calls are logged as management events in CloudTrail.

## API Reference

### Control Plane CLI (`bedrock-agentcore-control`)

#### Registry Operations

| Operation | CLI Command |
|-----------|-------------|
| Create registry | `aws bedrock-agentcore-control create-registry` |
| Get registry | `aws bedrock-agentcore-control get-registry` |
| Update registry | `aws bedrock-agentcore-control update-registry` |
| Delete registry | `aws bedrock-agentcore-control delete-registry` |
| List registries | `aws bedrock-agentcore-control list-registries` |

#### Record Operations

| Operation | CLI Command |
|-----------|-------------|
| Create record | `aws bedrock-agentcore-control create-registry-record` |
| Get record | `aws bedrock-agentcore-control get-registry-record` |
| Update record | `aws bedrock-agentcore-control update-registry-record` |
| Delete record | `aws bedrock-agentcore-control delete-registry-record` |
| List records | `aws bedrock-agentcore-control list-registry-records` |

#### Approval Operations

| Operation | CLI Command |
|-----------|-------------|
| Submit for approval | `aws bedrock-agentcore-control submit-registry-record-for-approval` |
| Update status (approve/reject/deprecate) | `aws bedrock-agentcore-control update-registry-record-status` |

### Data Plane CLI (`bedrock-agentcore`)

| Operation | CLI Command |
|-----------|-------------|
| Search records | `aws bedrock-agentcore search-registry-records` |
| MCP endpoint | POST to `https://bedrock-agentcore.<region>.amazonaws.com/registry/<registryId>/mcp` |

### IAM Actions

> **Important**: ALL IAM actions use the `bedrock-agentcore:` prefix — both control and data plane operations.

**Control Plane:**

| Action | Description |
|--------|-------------|
| `bedrock-agentcore:CreateRegistry` | Create a registry |
| `bedrock-agentcore:GetRegistry` | Get a registry |
| `bedrock-agentcore:UpdateRegistry` | Update a registry |
| `bedrock-agentcore:DeleteRegistry` | Delete a registry |
| `bedrock-agentcore:ListRegistries` | List registries |
| `bedrock-agentcore:CreateRegistryRecord` | Create a record |
| `bedrock-agentcore:GetRegistryRecord` | Get a record |
| `bedrock-agentcore:UpdateRegistryRecord` | Update a record |
| `bedrock-agentcore:DeleteRegistryRecord` | Delete a record |
| `bedrock-agentcore:ListRegistryRecords` | List records |
| `bedrock-agentcore:SubmitRegistryRecordForApproval` | Submit for approval |
| `bedrock-agentcore:UpdateRegistryRecordStatus` | Approve/reject/deprecate |

**Data Plane:**

| Action | Description |
|--------|-------------|
| `bedrock-agentcore:SearchRegistryRecords` | Search registry records |
| `bedrock-agentcore:InvokeRegistryMcp` | Invoke registry MCP endpoint |

> **Note**: MCP tool invocation requires BOTH `InvokeRegistryMcp` AND `SearchRegistryRecords`.

**Resource ARN Formats:**
- Registry: `arn:aws:bedrock-agentcore:{region}:{account}:registry/{registryId}`
- Record: `arn:aws:bedrock-agentcore:{region}:{account}:registry/{registryId}/record/{recordId}`

## Common Operations

### Create a Registry

```bash
aws bedrock-agentcore-control create-registry \
  --name "MyOrgRegistry" \
  --description "Central catalog for all AI agents and tools" \
  --region us-east-1
```

### Register an MCP Server

```bash
aws bedrock-agentcore-control create-registry-record \
  --registry-id <REGISTRY_ID> \
  --name "WeatherServer" \
  --descriptor-type MCP \
  --descriptors '{
    "mcp": {
      "server": {"schemaVersion": "2025-12-11", "inlineContent": "{\"name\": \"weather-server\", \"description\": \"Weather data service\", \"version\": \"1.0.0\"}"},
      "tools": {"protocolVersion": "2024-11-05", "inlineContent": "{\"tools\": [{\"name\": \"get_forecast\", \"description\": \"Get weather forecast\", \"inputSchema\": {\"type\": \"object\", \"properties\": {\"city\": {\"type\": \"string\"}}}}]}"}
    }
  }' \
  --record-version "1.0" \
  --region us-east-1
```

### Register an Agent (A2A)

```bash
aws bedrock-agentcore-control create-registry-record \
  --registry-id <REGISTRY_ID> \
  --name "CustomerSupportAgent" \
  --descriptor-type A2A \
  --descriptors '{
    "a2a": {
      "agentCard": {"schemaVersion": "0.3", "inlineContent": "{\"name\": \"customer-support\", \"description\": \"Handles customer inquiries\", \"version\": \"1.0.0\", \"protocolVersion\": \"0.3.0\", \"url\": \"https://api.example.com/a2a\", \"capabilities\": {}, \"defaultInputModes\": [\"text/plain\"], \"defaultOutputModes\": [\"text/plain\"], \"skills\": [{\"id\": \"order-lookup\", \"name\": \"Order Lookup\", \"description\": \"Look up order status\", \"tags\": [\"orders\"]}]}"}
    }
  }' \
  --record-version "1.0" \
  --region us-east-1
```

### Search Records

```bash
aws bedrock-agentcore search-registry-records \
  --search-query "weather forecast" \
  --registry-ids "<REGISTRY_ARN>" \
  --region us-east-1
```

### Search with Filters

```bash
aws bedrock-agentcore search-registry-records \
  --search-query "customer" \
  --registry-ids "<REGISTRY_ARN>" \
  --filter '{"$and": [{"descriptorType": {"$eq": "A2A"}}, {"version": {"$eq": "1.0"}}]}' \
  --region us-east-1
```

### Delete a Record

```bash
aws bedrock-agentcore-control delete-registry-record \
  --registry-id <REGISTRY_ID> \
  --record-id <RECORD_ID> \
  --region us-east-1
```

> **Note**: Delete all records before deleting a registry.

## Authorization

### IAM (SigV4)

Default authentication method. Works automatically with AWS CLI and SDKs.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bedrock-agentcore:SearchRegistryRecords",
        "bedrock-agentcore:InvokeRegistryMcp"
      ],
      "Resource": "arn:aws:bedrock-agentcore:<region>:<account>:registry/<registryId>"
    }
  ]
}
```

### JWT (OAuth 2.0)

Supports Amazon Cognito, Okta, Azure AD, or any OIDC-compatible provider. Configure during registry creation. **Authorization type cannot be changed after creation.**

```bash
aws bedrock-agentcore-control create-registry \
  --name "external-registry" \
  --authorizer-type CUSTOM_JWT \
  --authorizer-configuration '{
    "customJWTAuthorizer": {
      "discoveryUrl": "https://cognito-idp.us-east-1.amazonaws.com/<poolId>/.well-known/openid-configuration",
      "allowedClients": ["<appClientId>"]
    }
  }' \
  --region us-east-1
```

> **Constraint**: At least one JWT field required: `allowedAudiences`, `allowedClients`, `allowedScopes`, or `customClaims`. If multiple configured, ALL are verified.

## Best Practices

### Registry Organization
- **Single org-wide registry** for small organizations with few teams
- **Per-team registries** for larger organizations with clear ownership boundaries
- **Per-environment registries** (dev/staging/prod) for strict deployment governance

### Naming Conventions
- Use descriptive, unique names (e.g., `payments-mcp-server-v2` not `server1`)
- Include team/domain prefix when using shared registries (e.g., `platform/auth-agent`)
- Use semantic versioning for record versions

### Search Optimization
- Write detailed descriptions to improve semantic search relevance
- Use consistent descriptor types to enable effective filtering
- Include relevant keywords in record metadata

### Security
- Use IAM for internal (AWS-to-AWS) access patterns
- Use JWT for external or cross-organization access
- Enable manual approval for production registries
- Audit all registry operations via CloudTrail

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Record not found in search | Record not approved | Check record status; submit for approval if in Draft |
| MCP endpoint 403 | Missing IAM permissions | Add both `InvokeRegistryMcp` and `SearchRegistryRecords` |
| Search returns no results | No approved records match query | Verify records exist and are approved; broaden search query |
| Create registry fails | Region not supported | Use one of the 5 supported preview regions |
| Schema validation error `'0.3.0' is not supported` | Wrong A2A schema version | Use `"schemaVersion": "0.3"` (not `0.3.0`) |
| Sync not updating | Credential provider misconfigured | Verify outbound OAuth/IAM credentials for the source URL |

## Documentation

| Document | Description |
|----------|-------------|
| [Getting Started](getting-started.md) | End-to-end quick start walkthrough |
| [MCP Endpoint Guide](mcp-endpoint.md) | Configure and use registry MCP endpoint with Claude Code |
| [Governance Workflows](governance-workflows.md) | Approval lifecycle and EventBridge automation |
| [Sync Configuration](sync-configuration.md) | URL-based sync from external MCP servers and A2A agents |
| [Registry Integration Patterns](../../cross-service/registry-integration.md) | Cross-service patterns with Gateway, Identity, Runtime |

## Related Services

- **[Gateway Service](../gateway/README.md)**: Deploy discovered MCP servers as Gateway targets
- **[Runtime Service](../runtime/README.md)**: Execute discovered agents in serverless runtime
- **[Identity Service](../identity/README.md)**: Manage credentials for registry authorization
- **[Observability Service](../observability/README.md)**: Monitor registry usage and search patterns

## References

- [AWS Agent Registry Documentation](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/registry.html)
- [Registry Concepts](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/registry-concepts.html)
- [Supported Record Types](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/registry-supported-record-types.html)
- [Registry Search](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/registry-search-records.html)
- [Registry MCP Endpoint](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/registry-mcp-endpoint.html)
- [IAM Permissions](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/registry-iam-permissions.html)
- [Record Lifecycle](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/registry-record-lifecycle.html)
- [Record Synchronization](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/registry-sync-records.html)

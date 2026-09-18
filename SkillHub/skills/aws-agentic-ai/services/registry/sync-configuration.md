# Agent Registry - Sync Configuration

Agent Registry can automatically sync metadata from live external MCP servers and A2A agent endpoints via URL-based discovery. When the upstream source changes, the registry creates new record revisions automatically.

## How Sync Works

```
┌──────────────────┐         ┌──────────────┐         ┌──────────────┐
│ External MCP     │  pull   │ Agent        │  store   │ Registry     │
│ Server / A2A     │ <────── │ Registry     │ ──────>  │ Record       │
│ Agent (source)   │         │ Sync Engine  │         │ (new revision)│
└──────────────────┘         └──────────────┘         └──────────────┘
```

1. Registry connects to the source URL using outbound credentials
2. Retrieves server/tool definitions (MCP) or agent card (A2A)
3. Populates/updates record descriptors, name, description, and version from source
4. Creates a new revision if changes are detected

> **Limitation**: SSE streaming from MCP servers is not supported at public preview launch.

## Sync API Structure

Sync uses dedicated parameters on `create-registry-record`, separate from `--descriptors`:

```bash
aws bedrock-agentcore-control create-registry-record \
  --registry-id <REGISTRY_ID> \
  --name "<record-name>" \
  --descriptor-type <MCP|A2A> \
  --synchronization-type URL \
  --synchronization-configuration '{"fromUrl": {"url": "<source-url>", ...}}' \
  --region us-east-1
```

Key difference from inline records: use `--synchronization-type URL` and `--synchronization-configuration` instead of `--descriptors`.

## Syncing MCP Servers

### From a Public MCP Server (No Auth)

```bash
aws bedrock-agentcore-control create-registry-record \
  --registry-id <REGISTRY_ID> \
  --name "aws-knowledge-server" \
  --descriptor-type MCP \
  --synchronization-type URL \
  --synchronization-configuration '{
    "fromUrl": {
      "url": "https://knowledge-mcp.global.api.aws"
    }
  }' \
  --region us-east-1
```

### From an OAuth-Protected MCP Server

```bash
aws bedrock-agentcore-control create-registry-record \
  --registry-id <REGISTRY_ID> \
  --name "oauth-mcp-server" \
  --descriptor-type MCP \
  --synchronization-type URL \
  --synchronization-configuration '{
    "fromUrl": {
      "url": "https://analytics.internal.example.com/mcp",
      "credentialProviderConfigurations": [{
        "credentialProviderType": "OAUTH",
        "credentialProvider": {
          "oauthCredentialProvider": {
            "providerArn": "<OAUTH_PROVIDER_ARN>",
            "grantType": "CLIENT_CREDENTIALS"
          }
        }
      }]
    }
  }' \
  --region us-east-1
```

**Additional IAM permissions for OAuth sync:**
```json
{
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "bedrock-agentcore:GetWorkloadAccessToken",
      "Resource": "arn:aws:bedrock-agentcore:*:<account>:workload-identity-directory/*"
    },
    {
      "Effect": "Allow",
      "Action": "bedrock-agentcore:GetResourceOauth2Token",
      "Resource": "arn:aws:bedrock-agentcore:*:<account>:token-vault/*"
    }
  ]
}
```

### From an IAM-Protected MCP Server

For MCP servers on AWS infrastructure (Gateway targets, Lambda, API Gateway) using SigV4:

```bash
aws bedrock-agentcore-control create-registry-record \
  --registry-id <REGISTRY_ID> \
  --name "gateway-mcp-server" \
  --descriptor-type MCP \
  --synchronization-type URL \
  --synchronization-configuration '{
    "fromUrl": {
      "url": "https://bedrock-agentcore.us-east-1.amazonaws.com/gateway/<gw-id>/target/<tgt-id>/mcp",
      "credentialProviderConfigurations": [{
        "credentialProviderType": "IAM",
        "credentialProvider": {
          "iamCredentialProvider": {
            "roleArn": "arn:aws:iam::<account-id>:role/RegistrySyncRole",
            "service": "bedrock-agentcore",
            "region": "us-east-1"
          }
        }
      }]
    }
  }' \
  --region us-east-1
```

**`service` values for SigV4 signing:**
- `bedrock-agentcore` — AgentCore Runtime/Gateway
- `execute-api` — API Gateway
- `lambda` — Lambda function URLs

**`region`** is optional and defaults to the registry's region.

**Additional IAM permissions for IAM-based sync:**
```json
{
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "iam:PassRole",
      "Resource": "arn:aws:iam::<account>:role/RegistrySyncRole",
      "Condition": {
        "StringEquals": {
          "iam:PassedToService": "bedrock-agentcore.amazonaws.com"
        },
        "StringLike": {
          "iam:AssociatedResourceARN": "arn:aws:bedrock-agentcore:<region>:<account>:registry/*/record/*"
        }
      }
    }
  ]
}
```

The IAM role needs a trust policy:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "bedrock-agentcore.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

## Syncing A2A Agent Cards

Sync agent cards from the standard A2A well-known endpoint:

```bash
aws bedrock-agentcore-control create-registry-record \
  --registry-id <REGISTRY_ID> \
  --name "travel-agent" \
  --descriptor-type A2A \
  --synchronization-type URL \
  --synchronization-configuration '{
    "fromUrl": {
      "url": "https://agent.example.com/.well-known/agent-card.json"
    }
  }' \
  --region us-east-1
```

For OAuth or IAM-protected agent endpoints, add `credentialProviderConfigurations` as shown in the MCP examples above.

## Manually Triggering Sync

To force a re-sync of an existing record:

```bash
aws bedrock-agentcore-control update-registry-record \
  --registry-id <REGISTRY_ID> \
  --record-id <RECORD_ID> \
  --trigger-synchronization \
  --region us-east-1
```

## Monitoring Sync Status

```bash
aws bedrock-agentcore-control get-registry-record \
  --registry-id <REGISTRY_ID> \
  --record-id <RECORD_ID> \
  --region us-east-1
```

Check the `status` field. If sync fails, the record transitions to `CREATE_FAILED` or `UPDATE_FAILED`.

## Sync vs Inline Content

| Aspect | URL-based Sync | Inline Content |
|--------|---------------|----------------|
| **Source of truth** | External MCP server / A2A agent | Registry record itself |
| **Updates** | Automatic on upstream changes | Manual via `update-registry-record` |
| **Auth required** | Yes (if source is protected) | No |
| **Descriptor types** | `MCP` and `A2A` only | All types (`MCP`, `A2A`, `SKILL`, `CUSTOM`) |
| **Use case** | Live, evolving servers/agents | Stable, versioned resources |
| **Network dependency** | Source must be publicly reachable (no private IPs) | None |

### When to Use Sync

- MCP servers that are actively developed and frequently updated
- Gateway targets where tool definitions evolve with the upstream API
- A2A agents that publish well-known agent cards
- Multi-team environments where publishers manage their own servers

### When to Use Inline Content

- Stable, versioned resources that rarely change
- Resources where the registry should be the sole source of truth
- Skills and custom resources (sync not supported for `SKILL`/`CUSTOM` types)
- Air-gapped environments or private network resources

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| `CREATE_FAILED` | Source URL unreachable | Verify URL resolves to a public IP; check DNS |
| `CREATE_FAILED` | Credential provider misconfigured | Check OAuth client ID/secret or IAM role trust policy |
| `UPDATE_FAILED` | HTTP non-200/202 response | Check source server health; verify credentials haven't expired |
| `CREATE_FAILED` | URL resolves to private IP | Only public IPs are supported for sync |
| `CREATE_FAILED` | MCP tools/list timeout | Source must respond within 30 seconds |
| `CREATE_FAILED` | Response exceeds max size | Reduce the number of tools or simplify descriptions |
| Record in Draft after sync | Sync populates content but doesn't auto-approve | Submit for approval after initial sync |

## Related

- [Registry Overview](README.md)
- [Getting Started](getting-started.md)
- [Cross-Service Credential Management](../../cross-service/credential-management.md)
- [Record Synchronization (AWS Docs)](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/registry-sync-records.html)
- [Gateway Service](../gateway/README.md) — Source of Gateway-based MCP targets
- [Identity Service](../identity/README.md) — Credential providers for outbound auth

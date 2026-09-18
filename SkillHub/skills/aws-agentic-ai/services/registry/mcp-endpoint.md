# Agent Registry - MCP Endpoint

Each Agent Registry exposes an MCP-compatible endpoint (MCP spec 2025-11-25) that any MCP client can connect to for searching registry records. This enables AI coding assistants (Claude Code, Kiro) and agents to discover available tools, agents, and resources through their native MCP integration.

## Endpoint Format

```
https://bedrock-agentcore.<region>.amazonaws.com/registry/<registryId>/mcp
```

The endpoint exposes a single MCP tool: `search_registry_records`.

### Tool Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `searchQuery` | string | Yes | Natural language or keyword query (1-256 chars) |
| `maxResults` | integer | No | Number of results (1-20, default 10) |
| `filter` | object | No | Metadata filter using `$eq`, `$ne`, `$in`, `$and`, `$or` operators |

## IAM-Based Access (Recommended)

### Using `mcp-proxy-for-aws`

For IAM (SigV4) authentication, use the `mcp-proxy-for-aws` proxy which handles AWS signature signing automatically:

```json
{
  "mcpServers": {
    "agent-registry": {
      "type": "stdio",
      "command": "uvx",
      "args": [
        "mcp-proxy-for-aws@latest",
        "https://bedrock-agentcore.<region>.amazonaws.com/registry/<registryId>/mcp",
        "--service", "bedrock-agentcore",
        "--region", "<region>",
        "--profile", "my-profile"
      ]
    }
  }
}
```

Add this to `~/.claude/settings.json` (Claude Code) or your project's `.claude/settings.json`.

### Required IAM Permissions

MCP tool invocation requires **both** permissions:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bedrock-agentcore:InvokeRegistryMcp",
        "bedrock-agentcore:SearchRegistryRecords"
      ],
      "Resource": "arn:aws:bedrock-agentcore:<region>:<account>:registry/<registryId>"
    }
  ]
}
```

### Using via AWS CLI in Skill Context

The `aws-agentic-ai` skill permits `Bash(aws bedrock-agentcore *)` for data plane commands. Search directly without MCP configuration:

```bash
aws bedrock-agentcore search-registry-records \
  --search-query "your search query" \
  --registry-ids "arn:aws:bedrock-agentcore:us-east-1:<account-id>:registry/reg-abc123def456" \
  --region us-east-1
```

This approach works out of the box with existing AWS credential chains.

## JWT-Based Access (OAuth 2.0)

For external access or cross-organization scenarios. The registry must be created with `--authorizer-type CUSTOM_JWT`. **Authorization type cannot be changed after creation.**

### Option 1: Bearer Token

```json
{
  "mcpServers": {
    "my-registry": {
      "type": "http",
      "url": "https://bedrock-agentcore.<region>.amazonaws.com/registry/<registryId>/mcp",
      "headers": {
        "Authorization": "Bearer ${ACCESS_TOKEN}"
      }
    }
  }
}
```

### Option 2: Pre-Registered Client

Register the client ID in the registry's authorizer configuration:

```bash
aws bedrock-agentcore-control update-registry \
  --registry-id <registryId> \
  --authorizer-configuration '{
    "optionalValue": {
      "customJWTAuthorizer": {
        "discoveryUrl": "https://<idp-domain>/.well-known/openid-configuration",
        "allowedClients": ["<client-id>"]
      }
    }
  }' \
  --region us-east-1
```

MCP client config:
```json
{
  "mcpServers": {
    "pre-registered-registry": {
      "type": "http",
      "url": "https://bedrock-agentcore.<region>.amazonaws.com/registry/<registryId>/mcp",
      "oauth": {
        "clientId": "<client-id>",
        "callbackPort": "<port-number>"
      }
    }
  }
}
```

### Option 3: Dynamic Client Registration

Configure with `allowedAudience` instead of `allowedClients`:

```bash
aws bedrock-agentcore-control update-registry \
  --registry-id <registryId> \
  --authorizer-configuration '{
    "optionalValue": {
      "customJWTAuthorizer": {
        "discoveryUrl": "https://<idp-domain>/.well-known/openid-configuration",
        "allowedAudience": ["https://bedrock-agentcore.<region>.amazonaws.com/registry/<registryId>/mcp"]
      }
    }
  }' \
  --region us-east-1
```

MCP client config (no `oauth` needed — uses DCR):
```json
{
  "mcpServers": {
    "dcr-registry": {
      "type": "http",
      "url": "https://bedrock-agentcore.<region>.amazonaws.com/registry/<registryId>/mcp"
    }
  }
}
```

**OAuth well-known path** for resource metadata discovery:
```
https://bedrock-agentcore.<region>.amazonaws.com/.well-known/oauth-protected-resource/registry/<registryId>/mcp
```

Supported identity providers: Amazon Cognito, Okta, Azure AD (Microsoft Entra ID), Auth0, or any OIDC-compatible provider.

## Kiro Integration

Kiro supports MCP servers natively. Use the same `mcp-proxy-for-aws` approach for IAM:

```json
{
  "mcpServers": {
    "org-registry": {
      "type": "stdio",
      "command": "uvx",
      "args": [
        "mcp-proxy-for-aws@latest",
        "https://bedrock-agentcore.<region>.amazonaws.com/registry/<registryId>/mcp",
        "--service", "bedrock-agentcore",
        "--region", "<region>"
      ]
    }
  }
}
```

## Search Examples via MCP

### Basic Search

```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "search_registry_records",
    "arguments": {
      "searchQuery": "payment processing tools"
    }
  },
  "id": 1
}
```

### Filtered Search (MCP Servers Only)

```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "search_registry_records",
    "arguments": {
      "searchQuery": "data analytics",
      "maxResults": 5,
      "filter": {
        "descriptorType": {
          "$eq": "MCP"
        }
      }
    }
  },
  "id": 1
}
```

### Complex Filter

```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "search_registry_records",
    "arguments": {
      "searchQuery": "customer",
      "filter": {
        "$and": [
          {"descriptorType": {"$in": ["A2A", "MCP"]}},
          {"name": {"$ne": "deprecated-agent"}}
        ]
      }
    }
  },
  "id": 1
}
```

## Verification

### IAM Verification

```bash
curl -s -X POST \
  "https://bedrock-agentcore.<region>.amazonaws.com/registry/<registryId>/mcp" \
  -H "Content-Type: application/json" \
  -H "X-Amz-Security-Token: ${AWS_SESSION_TOKEN}" \
  --aws-sigv4 "aws:amz:<region>:bedrock-agentcore" \
  --user "${AWS_ACCESS_KEY_ID}:${AWS_SECRET_ACCESS_KEY}" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"search_registry_records","arguments":{"searchQuery":"weather"}}}'
```

### OAuth Verification

```bash
curl -s -X POST \
  "https://bedrock-agentcore.<region>.amazonaws.com/registry/<registryId>/mcp" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"search_registry_records","arguments":{"searchQuery":"weather"}}}'
```

## Agent-to-Agent Discovery Pattern

An AI agent can use the MCP endpoint to dynamically discover and invoke other agents:

1. **Discover**: Agent searches registry for agents with specific capabilities
2. **Evaluate**: Agent reads the A2A agent card to understand capabilities and endpoints
3. **Invoke**: Agent calls the discovered agent via its advertised URL

This enables dynamic, runtime agent composition without hardcoded dependencies.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| 403 Forbidden | Missing IAM permission | Add both `InvokeRegistryMcp` and `SearchRegistryRecords` to role |
| Connection refused | Wrong region or registry ID | Verify endpoint URL matches registry region and ID |
| Empty results | No approved records | Ensure records are approved, not just in Draft status |
| JWT auth fails | Token expired or wrong audience | Check token validity and `allowedClients`/`allowedAudience` config |
| Timeout | Network/VPC configuration | Ensure outbound HTTPS (443) to `bedrock-agentcore.<region>.amazonaws.com` |
| `mcp-proxy-for-aws` errors | Missing AWS credentials | Ensure `--profile` or environment variables are configured |

## Related

- [Registry Overview](README.md)
- [Getting Started](getting-started.md)
- [Governance Workflows](governance-workflows.md)
- [AWS Registry MCP Endpoint Docs](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/registry-mcp-endpoint.html)

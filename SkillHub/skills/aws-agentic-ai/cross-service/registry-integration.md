# Cross-Service: Registry Integration Patterns

**Applies to**: Registry, Gateway, Runtime, Identity

## Overview

Agent Registry becomes most powerful when combined with other AgentCore services. This guide covers cross-service patterns for discovering, deploying, and operating AI resources through the registry.

## Pattern 1: Registry + Gateway (Discover and Deploy MCP Servers)

Discover MCP servers from the registry, then deploy them as Gateway targets for agent consumption.

```
┌──────────────┐  search   ┌──────────────┐  deploy   ┌──────────────┐
│ Developer /  │ ────────> │ Agent        │ ────────> │ Gateway      │
│ Agent        │           │ Registry     │           │ Target       │
└──────────────┘           └──────────────┘           └──────────────┘
                                  │                          │
                                  │ MCP schema               │ serves tools
                                  ▼                          ▼
                           ┌──────────────┐           ┌──────────────┐
                           │ External     │           │ AI Agents    │
                           │ MCP Server   │           │ (consumers)  │
                           └──────────────┘           └──────────────┘
```

### Workflow

```bash
REGION="us-east-1"
REGISTRY_ID="reg-abc123"
GATEWAY_ID="gw-xyz789"

# 1. Search registry for a useful MCP server
RESULT=$(aws bedrock-agentcore search-registry-records \
  --search-query "payment processing" \
  --registry-ids "arn:aws:bedrock-agentcore:${REGION}:$(aws sts get-caller-identity --query Account --output text):registry/${REGISTRY_ID}" \
  --filter '{"descriptorType": {"$eq": "MCP"}}' \
  --region $REGION)

echo "$RESULT"
# Extract the MCP server schema from the search results

# 2. Save the discovered schema to S3
echo "$RESULT" | jq -r '.records[0].descriptors.mcp.server.inlineContent' > /tmp/discovered-schema.json
aws s3 cp /tmp/discovered-schema.json s3://my-schemas-bucket/discovered/payments-mcp.json

# 3. Deploy as a Gateway target
aws bedrock-agentcore-control create-gateway-target \
  --gateway-identifier $GATEWAY_ID \
  --name "payments-from-registry" \
  --endpoint-configuration '{
    "openApiSchema": {
      "s3": {"uri": "s3://my-schemas-bucket/discovered/payments-mcp.json"}
    }
  }' \
  --region $REGION
```

### Bi-directional Sync

Register your Gateway targets back into the registry so other teams can discover them using URL-based sync:

```bash
# Sync a Gateway target into the registry
aws bedrock-agentcore-control create-registry-record \
  --registry-id $REGISTRY_ID \
  --name "platform/payments-gateway" \
  --description "Payment tools exposed via Gateway (team: platform)" \
  --descriptor-type MCP \
  --synchronization-type URL \
  --synchronization-configuration "{
    \"fromUrl\": {
      \"url\": \"https://bedrock-agentcore.${REGION}.amazonaws.com/gateway/${GATEWAY_ID}/target/tgt-payments/mcp\",
      \"credentialProviderConfigurations\": [{
        \"credentialProviderType\": \"IAM\",
        \"credentialProvider\": {
          \"iamCredentialProvider\": {
            \"roleArn\": \"arn:aws:iam::$(aws sts get-caller-identity --query Account --output text):role/RegistrySyncRole\",
            \"service\": \"bedrock-agentcore\"
          }
        }
      }]
    }
  }" \
  --region $REGION
```

## Pattern 2: Registry + Identity (Credential-Aware Discovery)

Use Identity service credentials when syncing from protected external sources.

```
┌──────────────┐           ┌──────────────┐           ┌──────────────┐
│ Identity     │  provide  │ Registry     │  sync     │ External     │
│ Service      │ ────────> │ Sync Engine  │ ────────> │ MCP Server   │
│ (OAuth cred) │           │              │           │ (protected)  │
└──────────────┘           └──────────────┘           └──────────────┘
```

### Setup

```bash
# 1. Create OAuth credential in Identity service
aws bedrock-agentcore-control create-oauth-credential-provider \
  --name "partner-api-oauth" \
  --credential-provider-vendor CUSTOM \
  --oauth-discovery '{"discoveryUrl": "https://auth.partner.com/.well-known/openid-configuration"}' \
  --credential-provider-auth-parameters '{
    "oauthParameters": {
      "oauthClientId": "registry-sync-client",
      "oauthClientSecret": "<CLIENT_SECRET>"
    }
  }' \
  --region us-east-1

# 2. Create synced record using the credential
aws bedrock-agentcore-control create-registry-record \
  --registry-id <REGISTRY_ID> \
  --name "partner/logistics-server" \
  --descriptor-type MCP \
  --synchronization-type URL \
  --synchronization-configuration '{
    "fromUrl": {
      "url": "https://api.partner.com/mcp",
      "credentialProviderConfigurations": [{
        "credentialProviderType": "OAUTH",
        "credentialProvider": {
          "oauthCredentialProvider": {
            "providerArn": "arn:aws:bedrock-agentcore:us-east-1:<account-id>:oauth-credential-provider/partner-api-oauth",
            "grantType": "CLIENT_CREDENTIALS"
          }
        }
      }]
    }
  }' \
  --region us-east-1
```

## Pattern 3: Registry + Runtime (Dynamic Agent Composition)

Agents running in Runtime can query the registry to dynamically discover and invoke other agents or tools.

```
┌──────────────┐  invoke   ┌──────────────┐  search   ┌──────────────┐
│ User         │ ────────> │ Orchestrator │ ────────> │ Agent        │
│              │           │ Agent        │           │ Registry     │
└──────────────┘           │ (Runtime)    │           └──────┬───────┘
                           └──────┬───────┘                  │
                                  │                   discover│
                                  │ invoke                   │
                                  ▼                          ▼
                           ┌──────────────┐           ┌──────────────┐
                           │ Discovered   │ <──────── │ Agent Card   │
                           │ Agent        │   A2A     │ (from record)│
                           └──────────────┘           └──────────────┘
```

### Agent Code Example

```python
import boto3
import json

agentcore_client = boto3.client("bedrock-agentcore")
agentcore_control = boto3.client("bedrock-agentcore-control")

REGISTRY_ARN = "arn:aws:bedrock-agentcore:us-east-1:<account-id>:registry/reg-abc123"

def discover_and_delegate(user_query: str) -> dict:
    """Orchestrator agent discovers relevant agents/tools at runtime."""

    # 1. Search registry for relevant capabilities
    results = agentcore_client.search_registry_records(
        searchQuery=user_query,
        registryIds=[REGISTRY_ARN],
        maxResults=5
    )

    # 2. Filter for agents or MCP servers
    for record in results.get("records", []):
        if record["descriptorType"] == "A2A":
            # Parse A2A agent card
            agent_card = json.loads(
                record["descriptors"]["a2a"]["agentCard"]["inlineContent"]
            )
            # Invoke the discovered agent via its endpoint
            return invoke_a2a_agent(agent_card["url"], user_query)

        elif record["descriptorType"] == "MCP":
            # Parse MCP server definition
            mcp_def = json.loads(
                record["descriptors"]["mcp"]["server"]["inlineContent"]
            )
            # Use the discovered tools
            return invoke_mcp_tools(mcp_def, user_query)

    return {"error": "No relevant agents or tools found"}
```

## Pattern 4: Multi-Registry Architecture

Use multiple registries for different purposes, environments, or access levels.

```
┌─────────────────────────────────────────────────────┐
│                  Organization                        │
│                                                      │
│  ┌──────────────┐  ┌──────────────┐  ┌────────────┐│
│  │ Dev Registry │  │ Prod Registry│  │ Partner    ││
│  │ (auto-approve)│ │ (manual)     │  │ Registry   ││
│  │              │  │              │  │ (JWT auth) ││
│  │ - prototypes │  │ - validated  │  │ - external ││
│  │ - experiments│  │ - production │  │ - partner  ││
│  │ - draft tools│  │ - curated    │  │ - shared   ││
│  └──────────────┘  └──────────────┘  └────────────┘│
│                                                      │
│  Promotion flow:  Dev ──> Prod ──> Partner          │
└─────────────────────────────────────────────────────┘
```

### Promoting Records Across Registries

```bash
# 1. Read record from dev registry
RECORD=$(aws bedrock-agentcore-control get-registry-record \
  --registry-id $DEV_REGISTRY_ID \
  --record-id $RECORD_ID \
  --region us-east-1)

# 2. Extract descriptor and create in prod registry
DESCRIPTORS=$(echo "$RECORD" | jq '.descriptors')
NAME=$(echo "$RECORD" | jq -r '.name')
DESC=$(echo "$RECORD" | jq -r '.description')
TYPE=$(echo "$RECORD" | jq -r '.descriptorType')

aws bedrock-agentcore-control create-registry-record \
  --registry-id $PROD_REGISTRY_ID \
  --name "$NAME" \
  --description "$DESC" \
  --descriptor-type "$TYPE" \
  --descriptors "$DESCRIPTORS" \
  --record-version "1.0.0" \
  --region us-east-1

# 3. Submit for prod approval
aws bedrock-agentcore-control submit-registry-record-for-approval \
  --registry-id $PROD_REGISTRY_ID \
  --record-id $NEW_RECORD_ID \
  --region us-east-1
```

## Security Considerations

### Cross-Service IAM Policy

A role that can discover resources and deploy them to Gateway:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "RegistrySearch",
      "Effect": "Allow",
      "Action": [
        "bedrock-agentcore:SearchRegistryRecords",
        "bedrock-agentcore:InvokeRegistryMcp"
      ],
      "Resource": "arn:aws:bedrock-agentcore:*:*:registry/*"
    },
    {
      "Sid": "RegistryRead",
      "Effect": "Allow",
      "Action": [
        "bedrock-agentcore:GetRegistryRecord",
        "bedrock-agentcore:ListRegistryRecords"
      ],
      "Resource": "arn:aws:bedrock-agentcore:*:*:registry/*"
    },
    {
      "Sid": "GatewayDeploy",
      "Effect": "Allow",
      "Action": [
        "bedrock-agentcore:CreateGatewayTarget",
        "bedrock-agentcore:GetGatewayTarget"
      ],
      "Resource": "arn:aws:bedrock-agentcore:*:*:gateway/*"
    }
  ]
}
```

### Least Privilege by Persona

| Persona | Registry Permissions | Cross-Service Permissions |
|---------|---------------------|--------------------------|
| **Consumer** | `SearchRegistryRecords`, `InvokeRegistryMcp` | None required |
| **Publisher** | + `CreateRegistryRecord`, `SubmitRegistryRecordForApproval` | None required |
| **Curator** | + `UpdateRegistryRecordStatus` | None required |
| **Platform Engineer** | + All Registry operations | Gateway, Runtime, Identity operations |

## Related

- [Registry Overview](../services/registry/README.md)
- [Credential Management](credential-management.md)
- [Gateway Service](../services/gateway/README.md)
- [Identity Service](../services/identity/README.md)
- [Runtime Service](../services/runtime/README.md)

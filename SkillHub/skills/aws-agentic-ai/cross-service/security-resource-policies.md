# Cross-Service: Security & Resource-Based Policies

**Applies to**: Runtime, Gateway, Memory

## Overview

Resource-based policies allow attaching IAM-style policies directly to AgentCore resources to control which principals (AWS accounts, IAM users, or roles) can invoke and manage them. They work in conjunction with identity-based IAM policies.

## Identity-Based vs Resource-Based Policies

| Aspect | Identity-Based Policy | Resource-Based Policy |
|--------|----------------------|----------------------|
| **Attachment** | Attached to IAM users, roles, or groups | Attached directly to AgentCore resources |
| **Management** | Managed through AWS IAM | Managed through AgentCore APIs |
| **Specifies** | Actions and Resources (Principal is implicit) | Principals, Actions, and Conditions (Resource is implicit) |
| **Use Case** | Define what an identity can do | Define who can access a resource |

## Policy Evaluation Matrix

When a request is made, AWS evaluates both identity-based and resource-based policies:

| IAM Policy | Resource Policy | Result |
|------------|----------------|--------|
| Grants access | Silent | **Allowed** |
| Grants access | Grants access | **Allowed** |
| Grants access | Denies access | **Denied** |
| Silent | Grants access | **Allowed** |
| Silent | Silent | **Denied** |
| Denies access | Any | **Denied** |

Key principles:
- **Explicit Deny always wins** — if any policy denies, access is denied regardless
- **Either policy can allow** — if either permits and none denies, access is granted
- **Default Deny** — if no policy explicitly permits, access is denied

## Supported Resources

| Resource | Supported Actions |
|----------|-------------------|
| **Agent Runtime** | Invoke, invoke for user, invoke command, WebSocket, stop session, get agent card |
| **Agent Endpoint** | Same as Runtime (hierarchical authorization) |
| **Gateway** | Invoke gateway |
| **Memory** | CRUD operations on memory, events, records, sessions, actors, extraction jobs |

## Hierarchical Authorization (Runtime + Endpoint)

Agent endpoints are addressable access points to specific runtime versions. When authorizing invocations, AWS evaluates policies for **both** the runtime and the endpoint.

For cross-account access, create resource-based policies on **both** resources:

Policy for Agent Runtime (attached to `arn:aws:bedrock-agentcore:us-west-2:<resource-owner-account-id>:runtime/AGENTID`):

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::<caller-account-id>:role/CrossAccountRole"
      },
      "Action": "bedrock-agentcore:InvokeAgentRuntime",
      "Resource": "arn:aws:bedrock-agentcore:us-west-2:<resource-owner-account-id>:runtime/AGENTID"
    }
  ]
}
```

Policy for Agent Endpoint (attached to `arn:aws:bedrock-agentcore:us-west-2:<resource-owner-account-id>:runtime/AGENTID/endpoint/ENDPOINTID`):

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::<caller-account-id>:role/CrossAccountRole"
      },
      "Action": "bedrock-agentcore:InvokeAgentRuntime",
      "Resource": "arn:aws:bedrock-agentcore:us-west-2:<resource-owner-account-id>:runtime/AGENTID/endpoint/ENDPOINTID"
    }
  ]
}
```

> **Important**: If either resource denies access or lacks an explicit allow, the request is denied.

## Authentication Type Considerations

| Auth Type | Principal Element | Notes |
|-----------|-------------------|-------|
| **SigV4** | Specific AWS principals (`"AWS": "arn:aws:iam::..."`) | Evaluated with caller's IAM permissions |
| **OAuth** | Must use wildcard (`"Principal": "*"`) | JWT tokens validated by Identity Service before policy evaluation; use condition keys to restrict |

> **Constraint**: A Runtime or Gateway supports only one auth type (SigV4 OR OAuth), set at creation time.

## IAM Action Reference

### Agent Runtime Actions

| Action | Description |
|--------|-------------|
| `bedrock-agentcore:InvokeAgentRuntime` | Invoke an agent runtime |
| `bedrock-agentcore:InvokeAgentRuntimeForUser` | Invoke with user ID header |
| `bedrock-agentcore:InvokeAgentRuntimeCommand` | Execute a shell command in active session |
| `bedrock-agentcore:InvokeAgentRuntimeWithWebSocketStream` | Invoke with WebSocket stream |
| `bedrock-agentcore:InvokeAgentRuntimeWithWebSocketStreamForUser` | WebSocket with user ID header |
| `bedrock-agentcore:StopRuntimeSession` | Stop an active runtime session |
| `bedrock-agentcore:GetAgentCard` | Retrieve agent card information |

### Gateway Actions

| Action | Description |
|--------|-------------|
| `bedrock-agentcore:InvokeGateway` | Invoke a gateway |

### Memory Actions

| Action | Description |
|--------|-------------|
| `bedrock-agentcore:GetMemory` | Retrieve a Memory resource |
| `bedrock-agentcore:UpdateMemory` | Update a Memory resource |
| `bedrock-agentcore:DeleteMemory` | Delete a Memory resource |
| `bedrock-agentcore:CreateEvent` | Create an event |
| `bedrock-agentcore:GetEvent` | Retrieve an event |
| `bedrock-agentcore:DeleteEvent` | Delete an event |
| `bedrock-agentcore:ListEvents` | List events |
| `bedrock-agentcore:ListActors` | List actors |
| `bedrock-agentcore:ListSessions` | List sessions |
| `bedrock-agentcore:GetMemoryRecord` | Get a memory record |
| `bedrock-agentcore:ListMemoryRecords` | List memory records |
| `bedrock-agentcore:RetrieveMemoryRecords` | Search memory records |
| `bedrock-agentcore:DeleteMemoryRecord` | Delete a memory record |
| `bedrock-agentcore:BatchCreateMemoryRecords` | Batch create records |
| `bedrock-agentcore:BatchUpdateMemoryRecords` | Batch update records |
| `bedrock-agentcore:BatchDeleteMemoryRecords` | Batch delete records |
| `bedrock-agentcore:StartMemoryExtractionJob` | Start extraction job |
| `bedrock-agentcore:ListMemoryExtractionJobs` | List extraction jobs |

## Policy Examples

### Cross-Account Access

Grant specific roles in another account access to invoke a runtime:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": [
          "arn:aws:iam::<caller-account-id>:role/DeveloperRole",
          "arn:aws:iam::<caller-account-id>:role/AdminRole"
        ]
      },
      "Action": "bedrock-agentcore:InvokeAgentRuntime",
      "Resource": "arn:aws:bedrock-agentcore:us-west-2:<resource-owner-account-id>:runtime/AGENTID"
    }
  ]
}
```

### IP Address Restriction

Block traffic from specific IP ranges:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::<caller-account-id>:role/ApplicationRole"
      },
      "Action": "bedrock-agentcore:InvokeAgentRuntime",
      "Resource": "arn:aws:bedrock-agentcore:us-west-2:<resource-owner-account-id>:runtime/AGENTID"
    },
    {
      "Effect": "Deny",
      "Principal": {
        "AWS": "arn:aws:iam::<caller-account-id>:role/ApplicationRole"
      },
      "Action": "bedrock-agentcore:InvokeAgentRuntime",
      "Resource": "arn:aws:bedrock-agentcore:us-west-2:<resource-owner-account-id>:runtime/AGENTID",
      "Condition": {
        "IpAddress": {
          "aws:SourceIp": ["192.0.2.0/24", "198.51.100.0/24"]
        }
      }
    }
  ]
}
```

### VPC Restriction

Allow traffic only from a specific VPC:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::<caller-account-id>:role/ApplicationRole"
      },
      "Action": "bedrock-agentcore:InvokeAgentRuntime",
      "Resource": "arn:aws:bedrock-agentcore:us-west-2:<resource-owner-account-id>:runtime/AGENTID"
    },
    {
      "Effect": "Deny",
      "Principal": {
        "AWS": "arn:aws:iam::<caller-account-id>:role/ApplicationRole"
      },
      "Action": "bedrock-agentcore:InvokeAgentRuntime",
      "Resource": "arn:aws:bedrock-agentcore:us-west-2:<resource-owner-account-id>:runtime/AGENTID",
      "Condition": {
        "StringNotEquals": {
          "aws:SourceVpc": "vpc-1a2b3c4d"
        }
      }
    }
  ]
}
```

### OAuth with VPC Restriction

For OAuth-authenticated resources, use wildcard principal with condition keys:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowOAuthFromVPC",
      "Effect": "Allow",
      "Principal": "*",
      "Action": "bedrock-agentcore:InvokeAgentRuntime",
      "Resource": "arn:aws:bedrock-agentcore:us-west-2:<resource-owner-account-id>:runtime/AGENTID",
      "Condition": {
        "StringEquals": {
          "aws:SourceVpc": "vpc-1a2b3c4d"
        }
      }
    }
  ]
}
```

> **Note**: Wildcard principal is **required** for OAuth. JWT tokens are validated by Identity Service before policy evaluation. Anonymous requests are rejected before reaching policy evaluation.

## Managing Resource Policies

### AWS CLI

```bash
# Create or update a resource policy
aws bedrock-agentcore-control put-resource-policy \
  --resource-arn arn:aws:bedrock-agentcore:us-west-2:<resource-owner-account-id>:runtime/AGENTID \
  --policy file://policy.json

# Get a resource policy
aws bedrock-agentcore-control get-resource-policy \
  --resource-arn arn:aws:bedrock-agentcore:us-west-2:<resource-owner-account-id>:runtime/AGENTID

# Delete a resource policy
aws bedrock-agentcore-control delete-resource-policy \
  --resource-arn arn:aws:bedrock-agentcore:us-west-2:<resource-owner-account-id>:runtime/AGENTID
```

### Python SDK

```python
import boto3
import json

client = boto3.client('bedrock-agentcore-control', region_name='us-west-2')
resource_arn = 'arn:aws:bedrock-agentcore:us-west-2:<resource-owner-account-id>:runtime/AGENTID'

# Put resource policy
policy = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {"AWS": "arn:aws:iam::<caller-account-id>:role/MyRole"},
            "Action": "bedrock-agentcore:InvokeAgentRuntime",
            "Resource": resource_arn
        }
    ]
}

client.put_resource_policy(
    resourceArn=resource_arn,
    policy=json.dumps(policy)
)

# Get resource policy
response = client.get_resource_policy(resourceArn=resource_arn)
print(response['policy'])

# Delete resource policy
client.delete_resource_policy(resourceArn=resource_arn)
```

> **Important**: The `Resource` field must contain the **exact ARN** of the resource the policy is attached to. Using `"Resource": "*"` results in a validation error.

## Best Practices

- **Least privilege** — grant only the specific actions needed
- **Use conditions** — restrict by VPC, IP, or source account even when allowing access
- **Audit regularly** — review resource policies alongside identity-based policies
- **Cross-account requires both** — for Runtime, create policies on both the runtime AND endpoint
- **OAuth requires wildcard** — use condition keys (`aws:SourceVpc`, `aws:SourceVpce`) to restrict
- **No `Resource: *`** — always use the exact resource ARN

## Related

- [Credential Management](credential-management.md)
- [Registry Integration](registry-integration.md)
- [Runtime Service](../services/runtime/README.md)
- [Gateway Service](../services/gateway/README.md)
- [Memory Service](../services/memory/README.md)
- [Security in AgentCore (AWS Docs)](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/security.html)
- [IAM Policy Examples (AWS Docs)](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/security_iam_id-based-policy-examples.html)

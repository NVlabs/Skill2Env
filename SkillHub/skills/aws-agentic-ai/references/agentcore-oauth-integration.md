# AgentCore OAuth Integration Guide

> Detailed explanation of Amazon Bedrock AgentCore's three-layer OAuth authentication architecture: Inbound JWT (caller verification), Outbound Credential Provider (proxied user access to third-party APIs), and Gateway OAuth (transparent credential injection for MCP tools).

## Table of Contents

- [1. Three-Layer OAuth Architecture and WAT Chain](#1-three-layer-oauth-architecture-and-wat-chain)
  - [1.1 Overview](#11-overview)
  - [1.2 Workload Access Token (WAT) Chain](#12-workload-access-token-wat-chain)
  - [1.3 Three-Layer Comparison](#13-three-layer-comparison)
- [2. Inbound JWT Authorizer - Caller Verification](#2-inbound-jwt-authorizer--caller-verification)
  - [2.1 Configuration](#21-configuration)
  - [2.2 How It Works](#22-how-it-works)
  - [2.3 Container Obtains User Identity](#23-container-obtains-user-identity)
  - [2.4 Cognito JWT Structure Reference](#24-cognito-jwt-structure-reference)
  - [2.5 Caller Bearer Token](#25-caller-bearer-token)
  - [2.6 Unauthenticated 401 Response](#26-unauthenticated-401-response)
- [3. Outbound Credential Provider - Proxied User Access to Third-Party APIs](#3-outbound-credential-provider--proxied-user-access-to-third-party-apis)
  - [3.1 Core Concept](#31-core-concept)
  - [3.2 Two OAuth Modes](#32-two-oauth-modes)
  - [3.3 Registering a Credential Provider](#33-registering-a-credential-provider)
  - [3.4 Agent Code Integration](#34-agent-code-integration)
  - [3.5 Complete OAuth Flow](#35-complete-oauth-flow)
  - [3.6 IAM Permissions](#36-iam-permissions)
- [4. Gateway OAuth - Transparent Credential Injection for MCP Tools](#4-gateway-oauth--transparent-credential-injection-for-mcp-tools)
  - [4.1 Core Concept](#41-core-concept)
  - [4.2 Workflow](#42-workflow)
  - [4.3 Gateway Creation](#43-gateway-creation)
  - [4.4 Comparison: Gateway vs Agent Code OAuth](#44-comparison-gateway-vs-agent-code-oauth)
  - [4.5 credentialProviderConfigurations Types](#45-credentialproviderconfigurations-types)
  - [4.6 Pre-Integrated Services](#46-pre-integrated-services)
- [5. Cognito Complete Configuration Reference](#5-cognito-complete-configuration-reference)
- [6. Supported IdP List](#6-supported-idp-list)
- [7. Selection Guide](#7-selection-guide)
- [8. Security Essentials](#8-security-essentials)
- [Appendix A: End-to-End Practical Example](#appendix-a-end-to-end-practical-exampleagentcore-runtime--gateway-mcp--lambda)

### Quick Navigation

| You want to learn about... | Jump to |
|----------------------------|---------|
| Three-layer architecture overview + how WAT chains together | [Section 1](#1-three-layer-oauth-architecture-and-wat-chain) |
| How to verify caller identity | [Section 2](#2-inbound-jwt-authorizer--caller-verification) |
| How to proxy user access to third-party APIs | [Section 3](#3-outbound-credential-provider--proxied-user-access-to-third-party-apis) |
| Gateway MCP tools' transparent credential injection | [Section 4](#4-gateway-oauth--transparent-credential-injection-for-mcp-tools) |
| Cognito configuration reference | [Section 5](#5-cognito-complete-configuration-reference) |
| Which IdPs are supported | [Section 6](#6-supported-idp-list) |
| Which approach to choose | [Section 7](#7-selection-guide) |
| Security essentials | [Section 8](#8-security-essentials) |
| End-to-end practical code (CDK + Container + Lambda) | [Appendix A](#appendix-a-end-to-end-practical-exampleagentcore-runtime--gateway-mcp--lambda) |

> This document is based on the AgentCore API and SDK as of mid-2025. API parameters and SDK import paths may change with version updates. Please refer to the [official documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/agentcore.html) as the authoritative source.

---

## 1. Three-Layer OAuth Architecture and WAT Chain

### 1.1 Overview

```
                    Caller (Portal / CLI / API)
                         |
                    Bearer JWT Token
                         |
                         v
              +--- AgentCore Platform Layer ---+
              |                                |
              |  Inbound JWT Authorizer        |  <-- Layer 1: Verify caller identity
              |  (OIDC Discovery +             |
              |   JWT signature/claims check)  |
              |                                |
              +--------+-----------------------+
                       | Verification passed
                       v
              +--- Agent Container ------------+
              |                                |
              |  /invocations endpoint         |
              |  Obtain user_id:               |
              |  Request body or JWT claims    |
              |                                |
              +--------+-----------------------+
                       | Agent needs to call
                       | third-party API on
                       | behalf of user
                       v
              +--- AgentCore Identity ---------+
              |                                |
              |  Outbound Credential Provider  |  <-- Layer 2: Proxy user access
              |  (Token Vault stores           |      to third-party APIs
              |   per-user OAuth tokens)       |
              |                                |
              +--------+-----------------------+
                       | OR
                       v
              +--- AgentCore Gateway ----------+
              |                                |
              |  Gateway OAuth                 |  <-- Layer 3: Transparent credential
              |  (Auto-inject OAuth token      |      injection for MCP tools
              |   into MCP tool calls)         |
              |                                |
              +--------------------------------+
```

**Three layers, progressive enhancement:**

| Layer | Component | Solves | Code Impact |
|-------|-----------|--------|-------------|
| 1 | Inbound JWT Authorizer | "Who is the caller?" | Zero (platform-level) |
| 2 | Outbound Credential Provider | "How does Agent access third-party APIs on behalf of user?" | Agent code calls `@requires_access_token` |
| 3 | Gateway OAuth | "How do MCP tools transparently inject credentials?" | Zero (Gateway handles it) |

### 1.2 Workload Access Token (WAT) Chain

WAT is the core token connecting the three layers. When inbound JWT is enabled, AgentCore platform issues a WAT to the container, representing "which workload (Runtime) + which user (JWT sub)":

```
Caller JWT --> AgentCore Platform verifies --> Issues WAT to container
                                                |
                                                v
                                    WAT = workload_id + user_id
                                                |
                    +---------------------------+---------------------------+
                    |                                                       |
              Outbound Credential Provider                          Gateway OAuth
              WAT identifies user -->                        WAT identifies user -->
              Token Vault returns                            Gateway auto-injects
              user's third-party token                       third-party token
```

**Key**: WAT doesn't contain the third-party OAuth token itself. It serves as a "lookup key" — the Token Vault stores per-(workload, user) third-party tokens, and WAT is used to find the corresponding token.

### 1.3 Three-Layer Comparison

| Dimension | Inbound JWT | Outbound Credential Provider | Gateway OAuth |
|-----------|------------|------------------------------|---------------|
| **Direction** | Inbound (caller -> Agent) | Outbound (Agent -> third-party) | Outbound (MCP tool -> third-party) |
| **Purpose** | Verify caller identity | Proxy user access to third-party API | Transparent credential injection for MCP tools |
| **Code impact** | Zero | `@requires_access_token` decorator | Zero |
| **Token storage** | Caller holds JWT | Token Vault (per-user) | Token Vault (per-user) |
| **Typical IdP** | Cognito, Okta, Auth0 | Google, Slack, Jira, etc. | Same as Outbound |
| **Dependency** | Independent | Requires Layer 1 (needs WAT to identify user) | Requires Layer 1 (needs WAT to identify user) |

---

## 2. Inbound JWT Authorizer — Caller Verification

### 2.1 Configuration

When creating a Runtime, configure `authorizerConfiguration` to enable Inbound JWT verification:

```python
response = client.create_agent_runtime(
    agentRuntimeName='my-agent',
    authorizerConfiguration={
        "customJWTAuthorizer": {
            # OIDC Discovery endpoint, AgentCore auto-fetches JWKS
            "discoveryUrl": "https://cognito-idp.us-east-1.amazonaws.com/POOL_ID/.well-known/openid-configuration",
            # Allowed client IDs (matches JWT aud or client_id claim)
            "allowedClients": ["your-cognito-client-id"],
            # (Optional) Custom claims validation
            "customClaims": {
                "scope": "openid profile"
            }
        }
    },
    ...
)
```

**Key parameters:**

| Parameter | Required | Description |
|-----------|----------|-------------|
| `discoveryUrl` | Yes | OIDC Discovery URL, AgentCore auto-fetches public keys for JWT signature verification |
| `allowedClients` | Yes | List of allowed client IDs. JWT's `aud` or `client_id` claim must match one of these |
| `customClaims` | No | Custom claims validation. Example: require specific scope or role |

### 2.2 How It Works

```
Caller sends: Authorization: Bearer <JWT>
                    |
                    v
AgentCore Platform Layer:
  1. Fetch JWKS from discoveryUrl (cached)
  2. Verify JWT signature
  3. Verify exp (not expired), iss (issuer match)
  4. Verify aud/client_id in allowedClients
  5. (If configured) Verify customClaims
                    |
              Verification passed
                    |
                    v
  6. Issue Workload Access Token (WAT) to container
  7. Forward request to container /invocations endpoint
```

**Important**: With JWT Authorizer enabled, callers **cannot** use `boto3.invoke_agent_runtime()` (SigV4). They must send HTTPS requests directly with `Authorization: Bearer {JWT}`.

### 2.3 Container Obtains User Identity

After JWT verification passes, the container obtains the user identity through one of three methods:

**Method A: Extract from request body (simplest)**

The caller includes `user_id` in the request body. AgentCore platform has already verified identity at the platform layer, the container just reads it:

```python
# [FastAPI custom build]
@app.post("/invocations")
async def invocations(request: ChatRequest):
    user_id = request.user_id  # Passed by caller, platform layer already verified
    session_id = request.id
    ...
```

**Method B: Decode JWT claims (when additional claims like scope/role are needed)**

Requires configuring `--request-header-allowlist "Authorization"` when creating the Runtime so the original JWT header is passed through to the container:

```python
# [FastAPI custom build]
import jwt

@app.post("/invocations")
async def invocations(request: Request):
    auth_header = request.headers.get("Authorization", "")
    if auth_header.startswith("Bearer "):
        # No need to verify signature — platform layer already verified
        claims = jwt.decode(
            auth_header[7:],
            options={"verify_signature": False}
        )
        user_id = claims.get("sub")
        scopes = claims.get("scope", "").split()
        email = claims.get("email")
```

### 2.4 Cognito JWT Structure Reference

A typical Cognito access_token decoded:

```json
{
  "sub": "a1b2c3d4-5678-90ab-cdef-EXAMPLE11111",
  "iss": "https://cognito-idp.us-east-1.amazonaws.com/us-east-1_EXAMPLE",
  "client_id": "your-cognito-client-id",
  "origin_jti": "...",
  "event_id": "...",
  "token_use": "access",
  "scope": "openid profile",
  "auth_time": 1752275688,
  "exp": 1752279288,
  "iat": 1752275688,
  "jti": "...",
  "username": "testuser@example.com"
}
```

### 2.5 Caller Bearer Token

**Method 1: Authorization Code Flow + PKCE (recommended for browser/mobile apps)**

```typescript
// Frontend TypeScript example
import { CognitoIdentityProviderClient, InitiateAuthCommand } from '@aws-sdk/client-cognito-identity-provider';

// 1. Redirect user to Cognito Hosted UI
const authUrl = `https://${cognitoDomain}/oauth2/authorize?`
  + `client_id=${clientId}`
  + `&response_type=code`
  + `&redirect_uri=${encodeURIComponent(redirectUri)}`
  + `&scope=openid+profile`
  + `&code_challenge=${codeChallenge}`
  + `&code_challenge_method=S256`;

// 2. After redirect back, exchange code for token
const tokenResponse = await fetch(`https://${cognitoDomain}/oauth2/token`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  body: new URLSearchParams({
    grant_type: 'authorization_code',
    client_id: clientId,
    code: authorizationCode,
    redirect_uri: redirectUri,
    code_verifier: codeVerifier,  // PKCE
  }),
});

const { access_token } = await tokenResponse.json();
// Use access_token to call AgentCore Runtime
```

**Method 2: CLI quick test**

```bash
# Get token (Resource Owner Password Flow — for testing only, not recommended for production)
TOKEN=$(curl -s -X POST "https://cognito-idp.us-east-1.amazonaws.com/" \
  -H "Content-Type: application/x-amz-json-1.1" \
  -H "X-Amz-Target: AWSCognitoIdentityProviderService.InitiateAuth" \
  -d '{
    "AuthFlow": "USER_PASSWORD_AUTH",
    "ClientId": "YOUR_CLIENT_ID",
    "AuthParameters": {
      "USERNAME": "testuser@example.com",
      "PASSWORD": "TestPassword123!"
    }
  }' | jq -r '.AuthenticationResult.AccessToken')

# Call AgentCore Runtime
ESCAPED_ARN=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$AGENT_ARN', safe=''))")
curl -N \
  "https://bedrock-agentcore.us-east-1.amazonaws.com/runtimes/${ESCAPED_ARN}/invocations?qualifier=DEFAULT" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -H "X-Amzn-Bedrock-AgentCore-Runtime-Session-Id: test-session-001" \
  -d '{"id":"test-session-001","user_id":"testuser@example.com","messages":[{"role":"user","content":"Hello"}]}'
```

### 2.6 Unauthenticated 401 Response

When a caller sends a request without a valid JWT, AgentCore returns:

```
HTTP/1.1 401 Unauthorized
WWW-Authenticate: Bearer resource_metadata="https://bedrock-agentcore.{region}.amazonaws.com/runtimes/{ESCAPED_ARN}/invocations/.well-known/oauth-protected-resource?qualifier={QUALIFIER}"
```

The client can use the `resource_metadata` URL to discover OAuth endpoints and automatically obtain a token.

---

## 3. Outbound Credential Provider — Proxied User Access to Third-Party APIs

### 3.1 Core Concept

When an Agent needs to call third-party APIs (Google Drive, Slack, Jira, etc.) **on behalf of the user**, Outbound Credential Provider manages the complete OAuth lifecycle:

```
User authorizes (one-time) --> Token Vault stores refresh_token + access_token
                                        |
Agent needs third-party API --> @requires_access_token -->
    Token Vault returns valid access_token (auto-refresh if expired)
                                        |
Agent code receives access_token --> Call third-party API
```

**Core advantage**: Agent code never touches `refresh_token` or `client_secret`. Token Vault handles storage, refresh, and rotation.

### 3.2 Two OAuth Modes

| Mode | Applicable Scenario | OAuth Flow |
|------|---------------------|------------|
| **USER_FEDERATION** | User has their own third-party account (e.g., user's personal Google Drive) | Authorization Code Flow: user authorizes in browser, Token Vault stores per-user token |
| **SERVICE_ACCOUNT** | Shared service account (e.g., company-wide Slack Bot) | Client Credentials Flow: no user authorization needed, single shared token |

### 3.3 Registering a Credential Provider

**Example: Google OAuth (USER_FEDERATION)**

```python
import boto3

client = boto3.client('bedrock-agentcore-control')

response = client.create_credential_provider(
    name="google-provider",
    credentialProviderType="OAUTH",
    oauthCredentialProvider={
        "providerType": "GOOGLE",
        "providerUrl": "https://accounts.google.com",
        "clientId": "your-google-client-id.apps.googleusercontent.com",
        "clientSecret": "your-google-client-secret",
        "scopes": ["https://www.googleapis.com/auth/drive.metadata.readonly"],
        "authFlow": "USER_FEDERATION",
    }
)
```

**Example: Cognito (SERVICE_ACCOUNT)**

```python
response = client.create_credential_provider(
    name="cognito-m2m-provider",
    credentialProviderType="OAUTH",
    oauthCredentialProvider={
        "providerType": "COGNITO",
        "providerUrl": "https://cognito-idp.us-east-1.amazonaws.com/POOL_ID",
        "clientId": "cognito-client-id",
        "clientSecret": "cognito-client-secret",
        "scopes": ["my-resource-server/read"],
        "authFlow": "SERVICE_ACCOUNT",
    }
)
```

**Example: API Key**

```python
response = client.create_credential_provider(
    name="my-api-key-provider",
    credentialProviderType="API_KEY",
    apiKeyCredentialProvider={
        "apiKey": "sk-your-api-key-here",
    }
)
```

### 3.4 Agent Code Integration

Use the `@requires_access_token` decorator, which auto-injects the `access_token` parameter:

```python
from bedrock_agentcore.identity.auth import requires_access_token

@requires_access_token(
    provider_name="google-provider",
    scopes=["https://www.googleapis.com/auth/drive.metadata.readonly"],
    auth_flow="USER_FEDERATION",
    on_auth_url=lambda url: print("Please authorize:", url),
)
async def list_drive_files(*, access_token: str):
    """List user's Google Drive files."""
    # access_token is auto-injected, Agent never touches refresh_token / client_secret
    import requests
    response = requests.get(
        "https://www.googleapis.com/drive/v3/files",
        headers={"Authorization": f"Bearer {access_token}"},
        params={"pageSize": 10}
    )
    return response.json()
```

### 3.5 Complete OAuth Flow

```
1. Agent calls @requires_access_token decorated function
       |
2. SDK checks Token Vault: does this (workload, user) have a valid token?
       |
   +---+---+
   |       |
  Yes      No (first time or expired)
   |       |
   |   3a. If refresh_token exists and access_token expired:
   |       SDK auto-refreshes --> new access_token
   |       |
   |   3b. If no token at all (first authorization):
   |       SDK calls on_auth_url callback --> returns authorization URL
   |       User opens URL in browser --> authorizes --> callback receives code
   |       SDK exchanges code for tokens --> stores in Token Vault
   |       |
4. SDK returns valid access_token to decorated function
       |
5. Function uses access_token to call third-party API
```

### 3.6 IAM Permissions

The AgentCore Runtime role needs the following permissions:

```json
{
  "Effect": "Allow",
  "Action": [
    "bedrock-agentcore:GetCredentialProvider",
    "bedrock-agentcore:GetTokenVaultToken",
    "bedrock-agentcore:PutTokenVaultToken",
    "bedrock-agentcore:RefreshTokenVaultToken"
  ],
  "Resource": "arn:aws:bedrock-agentcore:*:*:credential-provider/*"
}
```

---

## 4. Gateway OAuth — Transparent Credential Injection for MCP Tools

### 4.1 Core Concept

Gateway OAuth takes Outbound Credential Provider a step further: credentials are injected at the **Gateway level**, completely transparent to Agent code and LLM. The Agent just calls MCP tools normally; the Gateway automatically handles OAuth.

### 4.2 Workflow

```
Agent calls MCP tool (e.g., "list Jira issues")
       |
MCPClient --> Gateway /mcp endpoint
       |
Gateway:
  1. Verify caller JWT (Inbound)
  2. Route to target MCP tool
  3. Check credentialProviderConfigurations:
     - GATEWAY_IAM_ROLE: use Gateway's own IAM role (for Lambda targets)
     - OAUTH: get user's third-party token from Token Vault via WAT
     - API_KEY: get API key from credential provider
  4. Inject credentials into downstream request headers
       |
Target (Lambda / MCP Server) receives request with injected credentials
```

### 4.3 Gateway Creation

```python
import boto3

client = boto3.client('bedrock-agentcore-control')

response = client.create_gateway(
    name="my-gateway",
    protocolType="MCP",
    description="MCP Gateway with OAuth",
)

# Create target with credential provider configuration
target_response = client.create_gateway_target(
    gatewayIdentifier=response["gatewayId"],
    name="jira-target",
    targetConfiguration={
        "mcpTargetConfiguration": {
            "openApiSchema": {
                "s3": {"uri": "s3://my-bucket/jira-openapi.json"}
            },
        }
    },
    credentialProviderConfigurations=[
        {
            "credentialProviderType": "OAUTH",
            "credentialProvider": {
                "credentialProviderArn": "arn:aws:bedrock-agentcore:...:credential-provider/jira-provider"
            }
        }
    ],
)
```

### 4.4 Comparison: Gateway vs Agent Code OAuth

| Dimension | Gateway OAuth | Agent Code (@requires_access_token) |
|-----------|--------------|--------------------------------------|
| **Code impact** | Zero — Gateway handles everything | Agent code adds decorator |
| **LLM visibility** | Token completely invisible to LLM | `access_token` visible in tool function |
| **Applicable scope** | MCP tools accessed through Gateway | Any third-party API |
| **Configuration** | `credentialProviderConfigurations` on Gateway Target | `@requires_access_token` in Python |
| **Flexibility** | Standardized process, less flexible | Full control over OAuth flow |
| **Recommended for** | MCP tool scenarios | Non-MCP scenarios, or when custom flow is needed |

### 4.5 credentialProviderConfigurations Types

| Type | Description | Use Case |
|------|-------------|----------|
| **GATEWAY_IAM_ROLE** | Gateway uses its own IAM role to invoke target (e.g., Lambda) | Lambda targets, AWS service targets |
| **OAUTH** | Gateway uses WAT to get user's third-party OAuth token from Token Vault | Third-party SaaS (Jira, Slack, Salesforce) |
| **API_KEY** | Gateway uses API key from credential provider | API key-authenticated services |

### 4.6 Pre-Integrated Services

Gateway provides 1-Click integration for the following services:

| Category | Services |
|----------|----------|
| **CRM** | Salesforce |
| **Collaboration** | Slack, Asana |
| **Project Management** | Jira, Zendesk |

These pre-integrated services have built-in OAuth flows. For other OAuth 2.0-compatible services, use the generic OAuth credential provider.

---

## 5. Cognito Complete Configuration Reference

### 5.1 User Pool Setup

```typescript
// CDK TypeScript
import * as cognito from 'aws-cdk-lib/aws-cognito';

const userPool = new cognito.UserPool(this, 'AgentUserPool', {
  userPoolName: 'agentcore-users',
  selfSignUpEnabled: true,
  signInAliases: { email: true },
  autoVerify: { email: true },
  passwordPolicy: {
    minLength: 8,
    requireUppercase: true,
    requireDigits: true,
    requireSymbols: false,
  },
  accountRecovery: cognito.AccountRecovery.EMAIL_ONLY,
  removalPolicy: cdk.RemovalPolicy.DESTROY,
});

// Cognito Domain (required for Hosted UI)
userPool.addDomain('CognitoDomain', {
  cognitoDomain: { domainPrefix: 'my-agent-auth' },
});
```

### 5.2 App Client (Authorization Code + PKCE)

```typescript
const userPoolClient = userPool.addClient('AgentClient', {
  userPoolClientName: 'agent-app-client',
  generateSecret: false,  // Public client (SPA/mobile)
  authFlows: {
    userPassword: true,       // For CLI testing
    userSrp: true,            // Secure Remote Password
  },
  oAuth: {
    flows: {
      authorizationCodeGrant: true,  // Authorization Code + PKCE
    },
    scopes: [cognito.OAuthScope.OPENID, cognito.OAuthScope.PROFILE],
    callbackUrls: ['http://localhost:3000/callback'],
    logoutUrls: ['http://localhost:3000/'],
  },
  supportedIdentityProviders: [
    cognito.UserPoolClientIdentityProvider.COGNITO,
  ],
  accessTokenValidity: cdk.Duration.hours(1),
  idTokenValidity: cdk.Duration.hours(1),
  refreshTokenValidity: cdk.Duration.days(30),
});
```

### 5.3 CLI Quick Test

```bash
# 1. Create test user
aws cognito-idp sign-up \
  --client-id YOUR_CLIENT_ID \
  --username testuser@example.com \
  --password TestPassword123! \
  --user-attributes Name=email,Value=testuser@example.com

# 2. Confirm user (skip email verification for testing)
aws cognito-idp admin-confirm-sign-up \
  --user-pool-id YOUR_POOL_ID \
  --username testuser@example.com

# 3. Get token
TOKEN=$(aws cognito-idp initiate-auth \
  --client-id YOUR_CLIENT_ID \
  --auth-flow USER_PASSWORD_AUTH \
  --auth-parameters USERNAME=testuser@example.com,PASSWORD=TestPassword123! \
  --query 'AuthenticationResult.AccessToken' --output text)

echo "Access Token: ${TOKEN}"
```

---

## 6. Supported IdP List

AgentCore Identity supports 25+ OAuth 2.0 providers:

| Category | Providers |
|----------|-----------|
| **Enterprise** | Cognito, Okta, Auth0, Azure AD, Ping Identity |
| **Social** | Google, GitHub, Facebook, Apple, X (Twitter) |
| **SaaS** | Salesforce, Slack, Jira, Asana, Zendesk, HubSpot, Shopify, Zoom, Dropbox, Box, Twitch, Spotify, LinkedIn |
| **Custom** | Any OAuth 2.0 / OIDC-compatible provider |

---

## 7. Selection Guide

### 7.1 Scenario Comparison

| Scenario | Recommended Approach |
|----------|---------------------|
| Agent only calls your own backend API | Inbound JWT + API Key (Secrets Manager) |
| Agent calls third-party OAuth API on behalf of user | Inbound JWT + Outbound Credential Provider |
| Agent accesses third-party services through MCP tools | Inbound JWT + Gateway OAuth (zero code changes in Agent) |

### 7.2 Evolution Path

```
Stage 1: Simple Authentication
  Inbound JWT + API Key (Secrets Manager)
  Suitable for: Agent only calls your own backend

        |
        v

Stage 2: Third-Party Integration
  + Outbound Credential Provider
  Suitable for: Agent needs to call Slack/Jira/Google on behalf of user

        |
        v

Stage 3: Full MCP Toolchain
  + Gateway OAuth
  Suitable for: Standardized MCP tools + transparent credential injection
```

### 7.3 Container Code Architecture Patterns

Both local tool mode and Gateway MCP mode can coexist — the same Agent can register both local tools and Gateway MCP tools:

```
Agent Container
  |
  +-- Local tools (@tool functions)
  |     Call backend API via HTTP
  |     Credentials: API Key from Secrets Manager
  |
  +-- Gateway MCP tools (via MCPClient)
        Connect to Gateway /mcp endpoint
        Credentials: Gateway auto-injects OAuth
```

### 7.4 WAT Retrieval Methods

| Method | Description | Recommended |
|--------|-------------|-------------|
| Manual retrieval | Directly call AgentCore Identity API | For debugging |
| SDK-managed | `@requires_access_token` or Gateway auto-handling | Yes (production) |

See [Appendix A.7](#a7-agent-runtime-container-code) for complete code examples.

---

## 8. Security Essentials

### 8.1 Credential Isolation

| Layer | Isolation Guarantee |
|-------|--------------------|
| **Inbound JWT** | Platform-level verification, container doesn't need to validate JWT signatures |
| **Outbound OAuth** | Agent code only receives `access_token`, never `refresh_token` or `client_secret` |
| **Gateway** | Agent code and LLM have zero visibility into credentials |

### 8.2 LLM Security

OAuth tokens **never appear** in:
- System prompts
- Tool input/output
- Conversation history

Even if the LLM is prompt-injected, it cannot leak credentials.

### 8.3 Audit Logging

| Dimension | Logged Information |
|-----------|-------------------|
| **Who** | JWT sub (user identity) |
| **What** | Which third-party API, which scope |
| **When** | Timestamp |
| **Result** | Success/failure, error details |

---

## Appendix A: End-to-End Practical Example — AgentCore Runtime + Gateway MCP + Lambda

### A.1 Architecture Overview

```
Frontend User (Browser/CLI)
      |
      | Bearer JWT Token
      v
AgentCore Runtime (MicroVM)
+------------------------------------------+
|  Agent Container                         |
|  +-- Strands Agent                       |
|      +-- Local tools (backend API)       |
|      +-- MCPClient --> Gateway           |
|                          |               |
|                          v               |
|                   Lambda Target          |
|                   (Business logic)       |
+------------------------------------------+
```

### A.2 CDK Cognito Authentication Setup

See `scripts/` directory for runnable templates. Reference CDK code:

```typescript
// infrastructure/lib/auth/cognito-construct.ts
import * as cdk from 'aws-cdk-lib';
import * as cognito from 'aws-cdk-lib/aws-cognito';
import { Construct } from 'constructs';

export class CognitoAuthStack extends Construct {
  public readonly userPool: cognito.UserPool;
  public readonly userPoolClient: cognito.UserPoolClient;
  public readonly issuerUrl: string;

  constructor(scope: Construct, id: string) {
    super(scope, id);

    this.userPool = new cognito.UserPool(this, 'UserPool', {
      userPoolName: 'agentcore-users',
      selfSignUpEnabled: true,
      signInAliases: { email: true },
      autoVerify: { email: true },
      removalPolicy: cdk.RemovalPolicy.DESTROY,
    });

    this.userPool.addDomain('Domain', {
      cognitoDomain: { domainPrefix: 'my-agent-auth' },
    });

    this.userPoolClient = this.userPool.addClient('AppClient', {
      generateSecret: false,
      authFlows: { userPassword: true, userSrp: true },
      oAuth: {
        flows: { authorizationCodeGrant: true },
        scopes: [cognito.OAuthScope.OPENID, cognito.OAuthScope.PROFILE],
        callbackUrls: ['http://localhost:3000/callback'],
      },
      accessTokenValidity: cdk.Duration.hours(1),
      refreshTokenValidity: cdk.Duration.days(30),
    });

    this.issuerUrl = `https://cognito-idp.${cdk.Stack.of(this).region}.amazonaws.com/${this.userPool.userPoolId}`;
  }
}
```

### A.3 CDK Gateway + Lambda Construct

```typescript
// infrastructure/lib/agentcore/gateway-lambda-construct.ts
import * as cdk from 'aws-cdk-lib';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import { Construct } from 'constructs';

export interface GatewayLambdaProps {
  gatewayName: string;
  lambdaCode: lambda.Code;
  schemaS3Uri: string;
}

export class AgentCoreGatewayLambdaStack extends Construct {
  public readonly gatewayId: string;

  constructor(scope: Construct, id: string, props: GatewayLambdaProps) {
    super(scope, id);

    // IAM Role for Gateway to invoke Lambda
    const gatewayRole = new iam.Role(this, 'GatewayRole', {
      assumedBy: new iam.ServicePrincipal('bedrock-agentcore.amazonaws.com'),
      inlinePolicies: {
        InvokeLambda: new iam.PolicyDocument({
          statements: [new iam.PolicyStatement({
            actions: ['lambda:InvokeFunction'],
            resources: ['*'],  // Restrict to specific Lambda ARN in production
          })],
        }),
      },
    });

    // Lambda Target
    const targetLambda = new lambda.Function(this, 'TargetLambda', {
      runtime: lambda.Runtime.PYTHON_3_12,
      handler: 'index.handler',
      code: props.lambdaCode,
      timeout: cdk.Duration.seconds(30),
    });

    // Custom Resource Lambda for Gateway lifecycle management
    // See scripts/gateway-custom-resource-lambda.py for implementation
    const customResourceLambda = new lambda.Function(this, 'CustomResourceLambda', {
      runtime: lambda.Runtime.PYTHON_3_12,
      handler: 'index.handler',
      code: lambda.Code.fromAsset('lambda/gateway-custom-resource'),
      timeout: cdk.Duration.minutes(5),
      environment: {
        GATEWAY_NAME: props.gatewayName,
        TARGET_LAMBDA_ARN: targetLambda.functionArn,
        OPENAPI_SCHEMA_S3_URI: props.schemaS3Uri,
        GATEWAY_IAM_ROLE_ARN: gatewayRole.roleArn,
      },
    });

    // Grant permissions
    customResourceLambda.addToRolePolicy(new iam.PolicyStatement({
      actions: [
        'bedrock-agentcore:CreateGateway',
        'bedrock-agentcore:DeleteGateway',
        'bedrock-agentcore:GetGateway',
        'bedrock-agentcore:CreateGatewayTarget',
        'bedrock-agentcore:DeleteGatewayTarget',
        'bedrock-agentcore:ListGatewayTargets',
      ],
      resources: ['*'],
    }));
  }
}
```

### A.4 Custom Resource Lambda

See [`scripts/gateway-custom-resource-lambda.py`](../scripts/gateway-custom-resource-lambda.py) for the complete implementation of the CloudFormation Custom Resource Lambda that manages Gateway create/update/delete lifecycle.

### A.5 CDK AgentCore Runtime

```typescript
// infrastructure/lib/agentcore/runtime-construct.ts
import * as cdk from 'aws-cdk-lib';
import * as iam from 'aws-cdk-lib/aws-iam';
import * as agentcore_cfn from 'aws-cdk-lib/aws-bedrock-agentcore';
import { Construct } from 'constructs';

export interface RuntimeProps {
  cognitoIssuer: string;
  cognitoClientId: string;
  ecrImageUri: string;
  gatewayUrl?: string;
  memoryId?: string;
}

export class AgentCoreRuntimeCdkStack extends Construct {
  public readonly runtimeArn: string;

  constructor(scope: Construct, id: string, props: RuntimeProps) {
    super(scope, id);

    // IAM Role for Runtime
    const agentCoreRole = new iam.Role(this, 'RuntimeRole', {
      assumedBy: new iam.ServicePrincipal('bedrock-agentcore.amazonaws.com'),
      inlinePolicies: {
        ECR: new iam.PolicyDocument({
          statements: [new iam.PolicyStatement({
            actions: ['ecr:GetAuthorizationToken', 'ecr:BatchGetImage', 'ecr:GetDownloadUrlForLayer'],
            resources: ['*'],
          })],
        }),
        Bedrock: new iam.PolicyDocument({
          statements: [new iam.PolicyStatement({
            actions: ['bedrock:InvokeModel', 'bedrock:InvokeModelWithResponseStream'],
            resources: ['*'],
          })],
        }),
        TokenVault: new iam.PolicyDocument({
          statements: [new iam.PolicyStatement({
            actions: [
              'bedrock-agentcore:GetTokenVaultToken',
              'bedrock-agentcore:PutTokenVaultToken',
              'bedrock-agentcore:RefreshTokenVaultToken',
            ],
            resources: ['*'],
          })],
        }),
      },
    });

    const cfnRuntime = new agentcore_cfn.CfnRuntime(this, 'Runtime', {
      agentRuntimeName: 'my-agent',
      agentRuntimeArtifact: {
        containerConfiguration: { containerUri: props.ecrImageUri },
      },
      networkConfiguration: { networkMode: 'PUBLIC' },
      protocolConfiguration: 'HTTP',
      roleArn: agentCoreRole.roleArn,
      authorizerConfiguration: {
        customJwtAuthorizer: {
          discoveryUrl: `${props.cognitoIssuer}/.well-known/openid-configuration`,
          allowedClients: [props.cognitoClientId],
        },
      },
      environmentVariables: {
        ...(props.gatewayUrl && { MCP_SERVER_URL: props.gatewayUrl }),
        ...(props.memoryId && { AGENTCORE_MEMORY_ID: props.memoryId }),
        AGENT_OBSERVABILITY_ENABLED: 'true',
      },
    });

    this.runtimeArn = cfnRuntime.attrAgentRuntimeArn;
  }
}
```

### A.6 CDK Assembly Layer

```typescript
// infrastructure/lib/main-stack.ts
// Wire together: Cognito + Gateway + Runtime
// Runtime and Gateway share the same Cognito App Client

const auth = new CognitoAuthStack(this, 'Auth');
const gateway = new AgentCoreGatewayLambdaStack(this, 'Gateway', {
  gatewayName: 'my-gateway',
  lambdaCode: lambda.Code.fromAsset('lambda/target'),
  schemaS3Uri: 's3://my-bucket/openapi.json',
});
const runtime = new AgentCoreRuntimeCdkStack(this, 'Runtime', {
  cognitoIssuer: auth.issuerUrl,
  cognitoClientId: auth.userPoolClient.userPoolClientId,
  ecrImageUri: '123456789012.dkr.ecr.us-east-1.amazonaws.com/my-agent:latest',
  gatewayUrl: `https://${gateway.gatewayId}.gateway.bedrock-agentcore.us-east-1.amazonaws.com/mcp`,
});
```

### A.7 Agent Runtime Container Code

See [`scripts/runtime-fastapi-template.py`](../scripts/runtime-fastapi-template.py) for a complete FastAPI Runtime template.

**Local tool mode** (calling backend API directly):

```python
from strands import Agent, tool
from strands.models.bedrock import BedrockModel

@tool
def search_orders(user_id: str, limit: int = 10) -> str:
    """Search recent orders for a user."""
    import requests
    response = requests.get(
        f"{BACKEND_API_URL}/api/orders",
        headers={"X-Service-Api-Key": SERVICE_API_KEY},
        params={"user_id": user_id, "limit": limit},
    )
    return response.text

model = BedrockModel(model_id="us.anthropic.claude-sonnet-4-5-20250929-v1:0")
agent = Agent(system_prompt="You are a helpful assistant.", model=model, tools=[search_orders])
```

**Gateway MCP mode** (connecting to Gateway for MCP tools):

```python
import os
from strands import Agent
from strands.tools.mcp import MCPClient
from mcp.client.streamable_http import streamable_http_client

gateway_url = os.environ["MCP_SERVER_URL"]
# e.g., "https://{gatewayId}.gateway.bedrock-agentcore.{region}.amazonaws.com/mcp"

mcp_client = MCPClient(lambda: streamable_http_client(url=gateway_url))

# In startup: create MCPClient (lazy connection)
# In /invocations: pass to Agent
agent = Agent(
    system_prompt="You are a helpful assistant.",
    model=model,
    tools=[*local_tools, mcp_client],
)
```

---

*This document is based on AWS official documentation (AgentCore Identity, Gateway, Runtime), mid-2025 AgentCore API and SDK. API parameters, SDK import paths may change with version updates.*

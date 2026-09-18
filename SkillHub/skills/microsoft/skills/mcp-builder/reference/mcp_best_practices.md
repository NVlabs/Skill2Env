# MCP Server Best Practices

## Quick Reference

### Server Naming
- **Python**: `{service}_mcp` (e.g., `slack_mcp`)
- **Node/TypeScript**: `{service}-mcp-server` (e.g., `slack-mcp-server`)
- **C#/.NET (Microsoft)**: `{Service}.Mcp.Server` (e.g., `Azure.Mcp.Server`)

### Tool Naming
- Use snake_case with service prefix
- Format: `{service}_{action}_{resource}`
- Example: `slack_send_message`, `github_create_issue`
- **C# Commands**: `{Resource}{Operation}Command` (e.g., `StorageContainerGetCommand`)

### Response Formats
- Support both JSON and Markdown formats
- JSON for programmatic processing
- Markdown for human readability

### Pagination
- Always respect `limit` parameter
- Return `has_more`, `next_offset`, `total_count`
- Default to 20-50 items

### Transport
- **Streamable HTTP**: For remote servers, multi-client scenarios, Agent Service
- **stdio**: For local integrations, command-line tools
- Avoid SSE (deprecated in favor of streamable HTTP)

---

## Remote vs Local MCP Servers

### Remote MCP Servers (Production/Multi-tenant)

Remote servers are hosted in the cloud and accessible via HTTPS. Required for Azure AI Agent Service integration.

**Characteristics:**
- Stateless request handling (no session state)
- Thread-safe command execution
- Transport-agnostic command design
- Authentication required (Entra ID, API keys)

**Hosting Options:**

| Platform | Transport | Auth | Best For |
|----------|-----------|------|----------|
| **Azure Functions** | HTTP streamable | Built-in/Custom | Serverless, auto-scale |
| **Azure Container Apps** | HTTP POST/GET | Custom | Containers, long-running |
| **App Service** | HTTP | Custom | Full control |

**Endpoint formats:**
- Azure Functions: `https://{app}.azurewebsites.net/runtime/webhooks/mcp`
- Foundry MCP: `https://mcp.ai.azure.com`
- GitHub MCP: `https://api.githubcopilot.com/mcp`

### Local MCP Servers

Local servers run as subprocesses communicating via stdio.

**Characteristics:**
- Single-user, single-session
- No network configuration needed
- Simpler authentication (inherit user context)

**Important:** stdio servers must NOT log to stdout (use stderr for logging).

---

## Server Naming Conventions

Follow these standardized naming patterns:

**Python**: Use format `{service}_mcp` (lowercase with underscores)
- Examples: `slack_mcp`, `github_mcp`, `jira_mcp`

**Node/TypeScript**: Use format `{service}-mcp-server` (lowercase with hyphens)
- Examples: `slack-mcp-server`, `github-mcp-server`, `jira-mcp-server`

The name should be general, descriptive of the service being integrated, easy to infer from the task description, and without version numbers.

---

## Tool Naming and Design

### Tool Naming

1. **Use snake_case**: `search_users`, `create_project`, `get_channel_info`
2. **Include service prefix**: Anticipate that your MCP server may be used alongside other MCP servers
   - Use `slack_send_message` instead of just `send_message`
   - Use `github_create_issue` instead of just `create_issue`
3. **Be action-oriented**: Start with verbs (get, list, search, create, etc.)
4. **Be specific**: Avoid generic names that could conflict with other servers

### Tool Design

- Tool descriptions must narrowly and unambiguously describe functionality
- Descriptions must precisely match actual functionality
- Provide tool annotations (readOnlyHint, destructiveHint, idempotentHint, openWorldHint)
- Keep tool operations focused and atomic

---

## Response Formats

All tools that return data should support multiple formats:

### JSON Format (`response_format="json"`)
- Machine-readable structured data
- Include all available fields and metadata
- Consistent field names and types
- Use for programmatic processing

### Markdown Format (`response_format="markdown"`, typically default)
- Human-readable formatted text
- Use headers, lists, and formatting for clarity
- Convert timestamps to human-readable format
- Show display names with IDs in parentheses
- Omit verbose metadata

---

## Pagination

For tools that list resources:

- **Always respect the `limit` parameter**
- **Implement pagination**: Use `offset` or cursor-based pagination
- **Return pagination metadata**: Include `has_more`, `next_offset`/`next_cursor`, `total_count`
- **Never load all results into memory**: Especially important for large datasets
- **Default to reasonable limits**: 20-50 items is typical

Example pagination response:
```json
{
  "total": 150,
  "count": 20,
  "offset": 0,
  "items": [...],
  "has_more": true,
  "next_offset": 20
}
```

---

## Transport Options

### Streamable HTTP

**Best for**: Remote servers, web services, multi-client scenarios

**Characteristics**:
- Bidirectional communication over HTTP
- Supports multiple simultaneous clients
- Can be deployed as a web service
- Enables server-to-client notifications

**Use when**:
- Serving multiple clients simultaneously
- Deploying as a cloud service
- Integration with web applications

### stdio

**Best for**: Local integrations, command-line tools

**Characteristics**:
- Standard input/output stream communication
- Simple setup, no network configuration needed
- Runs as a subprocess of the client

**Use when**:
- Building tools for local development environments
- Integrating with desktop applications
- Single-user, single-session scenarios

**Note**: stdio servers should NOT log to stdout (use stderr for logging)

### Transport Selection

| Criterion | stdio | Streamable HTTP |
|-----------|-------|-----------------|
| **Deployment** | Local | Remote |
| **Clients** | Single | Multiple |
| **Complexity** | Low | Medium |
| **Real-time** | No | Yes |

---

## Authentication Patterns

### For Remote MCP Servers

Remote MCP servers require authentication. Choose based on your scenario:

| Method | User Context | Best For |
|--------|--------------|----------|
| **API Key** | No | Simple integrations, internal tools |
| **Entra ID (agent identity)** | No | Azure services with shared identity |
| **Entra ID (managed identity)** | No | Azure-hosted servers |
| **OAuth passthrough (OBO)** | Yes | Multi-tenant, user-specific permissions |

### Microsoft Entra ID (Recommended for Azure)

**On-Behalf-Of (OBO) Flow** - Preserves user identity through the call chain:

```
User → Agent Service → MCP Server → Azure Resource
         (OBO token)    (validates)   (user context)
```

**Configuration:**
```
token_url: https://login.microsoftonline.com/{tenantId}/oauth2/v2.0/token
auth_url: https://login.microsoftonline.com/{tenantId}/oauth2/v2.0/authorize
refresh_url: https://login.microsoftonline.com/{tenantId}/oauth2/v2.0/token
```

### DefaultAzureCredential Chain

For servers that need to call Azure APIs, use the credential chain:

1. `EnvironmentCredential` - CI/CD (service principal vars)
2. `VisualStudioCredential` - VS login
3. `AzureCliCredential` - `az login`
4. `AzurePowerShellCredential` - `Connect-AzAccount`
5. `AzureDeveloperCliCredential` - `azd auth login`
6. `InteractiveBrowserCredential` - Fallback

### For Local MCP Servers

Local servers typically inherit the user's authentication context:

- **Azure CLI**: Use `AzureCliCredential` after `az login`
- **Environment Variables**: `AZURE_CLIENT_ID`, `AZURE_CLIENT_SECRET`, `AZURE_TENANT_ID`
- **API Keys**: Store in environment variables, validate on startup

---

## Security Best Practices

### Authentication and Authorization

**OAuth 2.1**:
- Use secure OAuth 2.1 with certificates from recognized authorities
- Validate access tokens before processing requests
- Only accept tokens specifically intended for your server

**API Keys**:
- Store API keys in environment variables, never in code
- Validate keys on server startup
- Provide clear error messages when authentication fails

### Input Validation

- Sanitize file paths to prevent directory traversal
- Validate URLs and external identifiers
- Check parameter sizes and ranges
- Prevent command injection in system calls
- Use schema validation (Pydantic/Zod) for all inputs

### Error Handling

- Don't expose internal errors to clients
- Log security-relevant errors server-side
- Provide helpful but not revealing error messages
- Clean up resources after errors

### DNS Rebinding Protection

For streamable HTTP servers running locally:
- Enable DNS rebinding protection
- Validate the `Origin` header on all incoming connections
- Bind to `127.0.0.1` rather than `0.0.0.0`

---

## Tool Annotations

Provide annotations to help clients understand tool behavior:

| Annotation | Type | Default | Description |
|-----------|------|---------|-------------|
| `readOnlyHint` | boolean | false | Tool does not modify its environment |
| `destructiveHint` | boolean | true | Tool may perform destructive updates |
| `idempotentHint` | boolean | false | Repeated calls with same args have no additional effect |
| `openWorldHint` | boolean | true | Tool interacts with external entities |

**Important**: Annotations are hints, not security guarantees. Clients should not make security-critical decisions based solely on annotations.

---

## Tool Approval Patterns (Agent Service)

When integrating with Azure AI Agent Service, configure approval requirements:

### Approval Configuration

```python
# Always require approval (default - safest)
require_approval = "always"

# Never require approval (trusted tools only)
require_approval = "never"

# Selective approval
require_approval = {"never": ["read_data", "list_items"]}  # Skip for read-only
require_approval = {"always": ["delete_resource", "update_config"]}  # Require for destructive
```

### Best Practices for Approval

- **Prefer allow-lists** using `allowed_tools` parameter
- **Require approval** for destructive operations (delete, update, create)
- **Skip approval** only for read-only, non-sensitive operations
- **Log all approvals** for audit trails

### Tool Management (Runtime)

```python
# Dynamically manage tools
mcp_tool.allow_tool("search_api_code")
mcp_tool.disallow_tool("delete_resource")
mcp_tool.set_approval_mode("never")
mcp_tool.update_headers("Authorization", "Bearer ...")
```

---

## Tool Quality Validation

Microsoft's MCP evaluator validates tool descriptions for discoverability.

### Quality Criteria

Tool descriptions must:
1. **Rank in top 3** when evaluated against similar tools
2. **Achieve ≥0.4 confidence** in relevance scoring
3. **Narrowly and unambiguously** describe functionality
4. **Precisely match** actual implementation behavior

### Writing Effective Descriptions

**Good:**
```
"List all storage containers in an Azure Storage account. Returns container names, 
last modified dates, and public access levels. Requires storage account name."
```

**Bad:**
```
"Gets storage stuff"  // Too vague
"Manages containers"  // Ambiguous - create? delete? list?
```

### Testing Tool Discoverability

Before deployment, test that your tool descriptions:
- Are selected by the model for relevant queries
- Are NOT selected for unrelated queries
- Don't conflict with similar tools from other servers

---

## Error Handling

- Use standard JSON-RPC error codes
- Report tool errors within result objects (not protocol-level errors)
- Provide helpful, specific error messages with suggested next steps
- Don't expose internal implementation details
- Clean up resources properly on errors

Example error handling:
```typescript
try {
  const result = performOperation();
  return { content: [{ type: "text", text: result }] };
} catch (error) {
  return {
    isError: true,
    content: [{
      type: "text",
      text: `Error: ${error.message}. Try using filter='active_only' to reduce results.`
    }]
  };
}
```

---

## Testing Requirements

Comprehensive testing should cover:

- **Functional testing**: Verify correct execution with valid/invalid inputs
- **Integration testing**: Test interaction with external systems
- **Security testing**: Validate auth, input sanitization, rate limiting
- **Performance testing**: Check behavior under load, timeouts
- **Error handling**: Ensure proper error reporting and cleanup

---

## Documentation Requirements

- Provide clear documentation of all tools and capabilities
- Include working examples (at least 3 per major feature)
- Document security considerations
- Specify required permissions and access levels
- Document rate limits and performance characteristics

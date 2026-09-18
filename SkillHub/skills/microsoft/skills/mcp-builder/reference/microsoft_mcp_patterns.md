# Microsoft MCP Patterns

This document covers patterns from Microsoft's official MCP implementations, including the Azure MCP Server and Foundry MCP services. Use these patterns when building MCP servers that integrate with Azure services or follow Microsoft conventions.

---

## Quick Reference

### Microsoft MCP Ecosystem

| Server | Type | Transport | Description |
|--------|------|-----------|-------------|
| **Azure MCP** | Local | stdio | 48+ Azure services (Storage, KeyVault, Cosmos, SQL, etc.) |
| **Foundry MCP** | Remote | Streamable HTTP | `https://mcp.ai.azure.com` - Models, deployments, evals, agents |
| **Fabric MCP** | Local | stdio | Microsoft Fabric APIs, OneLake, item definitions |
| **Playwright MCP** | Local | stdio | Browser automation and testing |
| **GitHub MCP** | Remote | Streamable HTTP | `https://api.githubcopilot.com/mcp` |
| **Azure DevOps** | Local | stdio | Pipelines, repos, boards |
| **SQL Server** | Local | stdio | SQL queries, schema (`aka.ms/MssqlMcp`) |
| **Microsoft Learn** | Remote | Streamable HTTP | `https://learn.microsoft.com/api/mcp` |

### Distribution Formats

Install Azure MCP Server via your preferred method:

| Format | Package/Command | Best For |
|--------|-----------------|----------|
| **VS Code Extension** | `ms-azuretools.vscode-azure-mcp-server` | VS Code users |
| **NPM** | `npx @azure/mcp@latest` | Node.js environments |
| **.NET Tool** | `dotnet tool install -g Azure.Mcp` | .NET developers |
| **Docker** | `mcr.microsoft.com/azure-sdk/azure-mcp` | Containers |

### Command Naming Convention

```
azmcp <service> <resource> <operation>

Examples:
- azmcp storage blob list
- azmcp keyvault secret get
- azmcp cosmos document create
- azmcp appconfig kv set
```

### C# Command Class Naming

```
{Resource}{Operation}Command

Examples:
- StorageContainerListCommand
- KeyVaultSecretGetCommand
- CosmosDbDatabaseQueryCommand
```

### Tool Metadata Annotations

| Annotation | Purpose | Example Use |
|------------|---------|-------------|
| `Destructive` | Modifies or deletes resources | Delete operations |
| `ReadOnly` | Only reads data, no side effects | List, get operations |
| `Idempotent` | Safe to retry, same result | Create-or-update operations |
| `OpenWorld` | Interacts with external systems | API calls to Azure |
| `Secret` | Handles sensitive data | Key Vault operations |
| `LocalRequired` | Requires local resources | File system operations |

---

## Server Architecture

### Azure MCP Service Coverage (48 Services)

| Category | Services |
|----------|----------|
| **Compute** | App Service, Functions, AKS, Container Registry, Virtual Desktop |
| **Storage** | Blob, File Shares, Cosmos DB, Redis, Managed Lustre |
| **Data** | SQL, PostgreSQL, MySQL, Data Explorer (Kusto), Confidential Ledger |
| **AI/ML** | AI Foundry, Search, Speech, Application Insights |
| **Integration** | Event Grid, Event Hubs, Service Bus, SignalR, Communication Services |
| **Security** | Key Vault, RBAC (Authorization), Policy, Advisor |
| **Management** | Monitor, Resource Health, Workbooks, Quota, Azure Migrate |
| **DevOps** | Load Testing, Grafana, Bicep Schema |

**Full list:** Storage, KeyVault, Cosmos, SQL, Postgres, MySQL, AKS, ACR, AppService, Functions, EventGrid, EventHubs, ServiceBus, SignalR, Search, Speech, Monitor, Advisor, Policy, Authorization, and 28+ more.

### Server Modes

The Azure MCP Server supports multiple operational modes:

| Mode | Description | Use Case |
|------|-------------|----------|
| `namespace` | Default mode, tools organized by service namespace | General use |
| `consolidated` | All tools in a single flat namespace | Simple integrations |
| `all` | Exposes all available tools | Development/testing |
| `single` | Single service only | Focused integrations |

### Configuration Example (mcp.json)

```json
{
  "mcpServers": {
    "azure": {
      "command": "npx",
      "args": ["-y", "@azure/mcp@latest", "server", "start"],
      "env": {
        "AZURE_TENANT_ID": "${AZURE_TENANT_ID}",
        "AZURE_CLIENT_ID": "${AZURE_CLIENT_ID}"
      }
    }
  }
}
```

### Server Manifest (server.json)

```json
{
  "name": "azure-mcp-server",
  "version": "1.0.0",
  "description": "MCP server for Azure services",
  "capabilities": {
    "tools": true,
    "resources": false,
    "prompts": false
  },
  "transports": ["stdio"],
  "authentication": {
    "type": "azure-identity",
    "scopes": ["https://management.azure.com/.default"]
  }
}
```

---

## Modular Architecture Pattern (C#/.NET)

Microsoft's Azure MCP Server uses a modular "Area" pattern for organizing tools by service domain.

### Command Hierarchy

```
IBaseCommand
└── BaseCommand
    └── GlobalCommand<TOptions>              # No subscription required
        └── SubscriptionCommand<TOptions>    # Subscription context
            └── Service-specific commands     # Azure service operations
```

### IAreaSetup Interface

Each Azure service implements `IAreaSetup` to register its tools:

```csharp
public interface IAreaSetup
{
    string Name { get; }           // e.g., "storage", "keyvault"
    string Title { get; }          // e.g., "Azure Storage", "Azure Key Vault"
    
    void ConfigureServices(IServiceCollection services);
    void RegisterCommands(CommandGroup rootGroup);
}
```

### Implementation Example

```csharp
public class StorageSetup : IAreaSetup
{
    public string Name => "storage";
    public string Title => "Azure Storage";

    public void ConfigureServices(IServiceCollection services)
    {
        services.AddSingleton<BlobServiceClientFactory>();
        services.AddSingleton<StorageAccountService>();
    }

    public void RegisterCommands(CommandGroup rootGroup)
    {
        var storageGroup = rootGroup.AddGroup("storage", "Azure Storage operations");
        
        // Blob operations
        var blobGroup = storageGroup.AddGroup("blob", "Blob storage operations");
        blobGroup.AddCommand<ListBlobsCommand>("list", "List blobs in a container");
        blobGroup.AddCommand<GetBlobCommand>("get", "Get blob content");
        blobGroup.AddCommand<UploadBlobCommand>("upload", "Upload a blob");
        blobGroup.AddCommand<DeleteBlobCommand>("delete", "Delete a blob");
        
        // Container operations
        var containerGroup = storageGroup.AddGroup("container", "Container operations");
        containerGroup.AddCommand<ListContainersCommand>("list", "List containers");
        containerGroup.AddCommand<CreateContainerCommand>("create", "Create a container");
    }
}
```

### Command Implementation

```csharp
public class ListBlobsCommand : ICommand
{
    [Option("--account", "Storage account name")]
    public string AccountName { get; set; } = string.Empty;
    
    [Option("--container", "Container name")]
    public string ContainerName { get; set; } = string.Empty;
    
    [Option("--prefix", "Blob name prefix filter")]
    public string? Prefix { get; set; }
    
    [Option("--limit", "Maximum number of results")]
    public int Limit { get; set; } = 100;

    public ToolMetadata Metadata => new()
    {
        ReadOnly = true,
        OpenWorld = true,
        Idempotent = true
    };

    public async Task<CommandResponse> ExecuteAsync(
        IServiceProvider services,
        CancellationToken cancellationToken)
    {
        var factory = services.GetRequiredService<BlobServiceClientFactory>();
        var client = factory.CreateClient(AccountName);
        var container = client.GetBlobContainerClient(ContainerName);
        
        var blobs = new List<BlobItem>();
        await foreach (var blob in container.GetBlobsAsync(prefix: Prefix, cancellationToken: cancellationToken))
        {
            blobs.Add(blob);
            if (blobs.Count >= Limit) break;
        }
        
        return CommandResponse.Success(new
        {
            account = AccountName,
            container = ContainerName,
            count = blobs.Count,
            blobs = blobs.Select(b => new
            {
                name = b.Name,
                size = b.Properties.ContentLength,
                lastModified = b.Properties.LastModified,
                contentType = b.Properties.ContentType
            })
        });
    }
}
```

### Option Registration Extensions

```csharp
// Required options
command.AddOption("--account")
    .AsRequired()
    .WithDescription("Storage account name");

// Optional options with defaults
command.AddOption("--limit")
    .AsOptional()
    .WithDefault(100)
    .WithDescription("Maximum results to return");

// Enum options
command.AddOption("--access-tier")
    .AsOptional()
    .WithValues<AccessTier>()
    .WithDescription("Blob access tier");
```

---

## Authentication Patterns

### Azure Identity Credential Chain

Microsoft uses a credential chain that tries multiple authentication methods:

```
1. Environment Variables (AZURE_CLIENT_ID, AZURE_CLIENT_SECRET, AZURE_TENANT_ID)
2. Visual Studio credentials
3. Azure CLI credentials
4. Azure PowerShell credentials
5. Azure Developer CLI credentials
6. Interactive browser (development only)
```

### Environment Variable Controls

| Variable | Purpose |
|----------|---------|
| `AZURE_TOKEN_CREDENTIALS` | Override credential type |
| `AZURE_TENANT_ID` | Azure AD tenant ID |
| `AZURE_CLIENT_ID` | Service principal client ID |
| `AZURE_CLIENT_SECRET` | Service principal secret |
| `AZURE_SUBSCRIPTION_ID` | Default subscription |

### Credential Implementation

```csharp
public class AzureCredentialProvider
{
    public TokenCredential GetCredential()
    {
        var credentialType = Environment.GetEnvironmentVariable("AZURE_TOKEN_CREDENTIALS");
        
        return credentialType?.ToLower() switch
        {
            "environment" => new EnvironmentCredential(),
            "cli" => new AzureCliCredential(),
            "managedidentity" => new ManagedIdentityCredential(),
            _ => new DefaultAzureCredential(new DefaultAzureCredentialOptions
            {
                ExcludeInteractiveBrowserCredential = !IsDevelopment(),
                ExcludeManagedIdentityCredential = IsDevelopment()
            })
        };
    }
}
```

---

## Error Handling Patterns

### Azure SDK Error Handling

```csharp
public static CommandResponse HandleAzureError(RequestFailedException ex)
{
    return ex.Status switch
    {
        404 => CommandResponse.Error(
            $"Resource not found. Verify the resource exists and you have access. " +
            $"Details: {ex.Message}"),
        
        403 => CommandResponse.Error(
            $"Access denied. Check your permissions and ensure your credentials " +
            $"have the required role assignments. Details: {ex.Message}"),
        
        401 => CommandResponse.Error(
            $"Authentication failed. Run 'az login' or check your credentials. " +
            $"Details: {ex.Message}"),
        
        409 => CommandResponse.Error(
            $"Conflict: Resource already exists or is in a conflicting state. " +
            $"Details: {ex.Message}"),
        
        429 => CommandResponse.Error(
            $"Rate limit exceeded. Wait and retry. " +
            $"Details: {ex.Message}"),
        
        _ => CommandResponse.Error(
            $"Azure API error (HTTP {ex.Status}): {ex.Message}")
    };
}
```

### CommandResponse Pattern

```csharp
public class CommandResponse
{
    public bool IsSuccess { get; init; }
    public object? Data { get; init; }
    public string? Error { get; init; }
    
    public static CommandResponse Success(object data) => 
        new() { IsSuccess = true, Data = data };
    
    public static CommandResponse Error(string message) => 
        new() { IsSuccess = false, Error = message };
}
```

---

## Tool Metadata Best Practices

### Annotation Guidelines

| Operation Type | Destructive | ReadOnly | Idempotent | OpenWorld |
|----------------|-------------|----------|------------|-----------|
| List/Get | ❌ | ✅ | ✅ | ✅ |
| Create | ❌ | ❌ | ❌ | ✅ |
| Create-or-Update | ❌ | ❌ | ✅ | ✅ |
| Update | ❌ | ❌ | ✅ | ✅ |
| Delete | ✅ | ❌ | ✅ | ✅ |
| Purge (permanent) | ✅ | ❌ | ❌ | ✅ |

### Metadata Implementation

```csharp
public class ToolMetadata
{
    /// <summary>
    /// Tool may perform destructive operations (delete, purge).
    /// Clients should confirm before execution.
    /// </summary>
    public bool Destructive { get; init; }
    
    /// <summary>
    /// Tool only reads data, no side effects.
    /// Safe to call without confirmation.
    /// </summary>
    public bool ReadOnly { get; init; }
    
    /// <summary>
    /// Repeated calls with same arguments produce same result.
    /// Safe to retry on failure.
    /// </summary>
    public bool Idempotent { get; init; }
    
    /// <summary>
    /// Tool interacts with external systems (Azure APIs).
    /// May have latency or availability concerns.
    /// </summary>
    public bool OpenWorld { get; init; }
    
    /// <summary>
    /// Tool handles sensitive data (secrets, keys, credentials).
    /// Output should be treated as confidential.
    /// </summary>
    public bool Secret { get; init; }
    
    /// <summary>
    /// Tool requires local resources (file system, environment).
    /// May not work in all execution contexts.
    /// </summary>
    public bool LocalRequired { get; init; }
}
```

---

## Remote MCP with Azure Functions

### Initialize from Template

```bash
# Python
azd init --template remote-mcp-functions-python -e mcpserver-python

# TypeScript  
azd init --template remote-mcp-functions-typescript -e mcpserver-ts

# .NET
azd init --template remote-mcp-functions-dotnet -e mcpserver-dotnet
```

### TypeScript Tool Registration (Azure Functions)

```typescript
import { app, InvocationContext } from '@azure/functions';

export async function mcpToolStorageList(
    _toolArguments: unknown, 
    context: InvocationContext
): Promise<string> {
    const args = context.triggerMetadata.mcptoolargs as { 
        accountName: string;
        prefix?: string;
    };
    
    // Implementation
    const containers = await listContainers(args.accountName, args.prefix);
    return JSON.stringify(containers);
}

app.mcpTool('storage_container_list', {
    toolName: 'storage_container_list',
    description: 'List all containers in an Azure Storage account',
    toolProperties: {
        accountName: arg.string()
            .describe('Storage account name')
            .required(),
        prefix: arg.string()
            .describe('Filter containers by prefix')
            .optional()
    },
    handler: mcpToolStorageList
});
```

### Deploy to Azure

```bash
# Deploy
azd up

# Get endpoint
# https://{function_app_name}.azurewebsites.net/runtime/webhooks/mcp
```

---

## Testing Infrastructure

### Test Structure

```
tools/Azure.Mcp.Tools.{Service}/tests/
├── Azure.Mcp.Tools.{Service}.UnitTests/    # No Azure resources
├── Azure.Mcp.Tools.{Service}.LiveTests/    # Requires Azure
├── test-resources.bicep                     # Infrastructure template
└── test-resources-post.ps1                  # Post-deployment setup
```

### Unit Tests (No Azure Resources)

```csharp
[TestClass]
public class StorageContainerListCommandTests
{
    [TestMethod]
    public async Task ListContainers_ReturnsExpectedResults()
    {
        // Arrange
        var mockClient = new Mock<BlobServiceClient>();
        var command = new StorageContainerListCommand(mockClient.Object);
        
        // Act
        var result = await command.ExecuteAsync(new StorageContainerListOptions
        {
            AccountName = "teststorage"
        });
        
        // Assert
        Assert.IsNotNull(result);
    }
}
```

### Live Tests (Bicep Infrastructure)

```bicep
// test-resources.bicep
param baseName string
param location string = resourceGroup().location

resource storageAccount 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  name: '${baseName}storage'
  location: location
  sku: { name: 'Standard_LRS' }
  kind: 'StorageV2'
}

output STORAGE_ACCOUNT_NAME string = storageAccount.name
```

### Running Tests

```bash
# Unit tests only
./eng/scripts/Test-Code.ps1 -UnitTests

# Live tests (deploys Azure resources)
./eng/scripts/Test-Code.ps1 -LiveTests -ServiceDirectory Storage

# Deploy test resources manually
./eng/scripts/Deploy-TestResources.ps1 -ServiceDirectory Storage
```

---

## Engineering Standards

### Code Style Requirements

| Rule | Requirement |
|------|-------------|
| **Constructors** | Use C# primary constructors |
| **JSON** | Use `System.Text.Json` (no Newtonsoft) |
| **Classes** | Make `sealed` when not inherited |
| **Members** | Make `static` when possible |
| **Files** | One class/interface per file |
| **AOT** | All code must be Native AOT compatible |

### AOT Compatibility

```csharp
// GOOD: AOT compatible
[JsonSerializable(typeof(ContainerListResponse))]
internal partial class ContainerJsonContext : JsonSerializerContext { }

// BAD: Reflection-based (not AOT safe)
JsonSerializer.Deserialize<ContainerListResponse>(json);  // Avoid
```

### PR Checklist

Before submitting changes to Microsoft MCP:

- [ ] Code builds with `dotnet build`
- [ ] All unit tests pass
- [ ] Live tests pass (if applicable)
- [ ] AOT analysis passes: `./eng/scripts/Analyze-AOT-Compact.ps1`
- [ ] Tool descriptions are clear and specific
- [ ] No hardcoded credentials or endpoints
- [ ] Follows naming conventions

---

## Integration with Foundry Agent Service

### MCP Tool Declaration (Python)

```python
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition, MCPTool

mcp_tool = MCPTool(
    server_label="azure-storage",
    server_url="https://{app}.azurewebsites.net/runtime/webhooks/mcp",
    require_approval="always",
    allowed_tools=["storage_container_list"],
    project_connection_id=connection_name
)

agent = project_client.agents.create_version(
    agent_name="storage-agent",
    definition=PromptAgentDefinition(
        model="gpt-4o-mini",
        instructions="Help users manage Azure Storage",
        tools=[mcp_tool]
    )
)
```

### MCP Tool Declaration (C#)

```csharp
PromptAgentDefinition agentDefinition = new(model: "gpt-4o-mini")
{
    Instructions = "Help users manage Azure Storage",
    Tools = { 
        ResponseTool.CreateMcpTool(
            serverLabel: "azure-storage",
            serverUri: new Uri("https://{app}.azurewebsites.net/runtime/webhooks/mcp"),
            toolCallApprovalPolicy: new McpToolCallApprovalPolicy(
                GlobalMcpToolCallApprovalPolicy.AlwaysRequireApproval
            )
        )
    }
};
```

### Handling Approval Requests

```python
for item in response.output:
    if item.type == "mcp_approval_request" and item.id:
        print(f"Tool: {getattr(item, 'name', '<unknown>')}")
        print(f"Arguments: {json.dumps(getattr(item, 'arguments', None), indent=2)}")
        
        should_approve = input("Approve? (y/N): ").strip().lower() == "y"
        
        input_list.append(McpApprovalResponse(
            type="mcp_approval_response",
            approve=should_approve,
            approval_request_id=item.id
        ))
```

---

## When to Use Microsoft MCP vs Custom

### Use Microsoft MCP Servers When:

- ✅ Integrating with Azure services (Storage, KeyVault, Cosmos, etc.)
- ✅ Working with AI Foundry (agents, evaluations, deployments)
- ✅ Need browser automation (Playwright MCP)
- ✅ GitHub integration (GitHub MCP)
- ✅ Microsoft Fabric operations

### Build Custom MCP Servers When:

- ✅ Integrating with non-Microsoft services
- ✅ Custom internal APIs
- ✅ Third-party SaaS integrations
- ✅ Specialized domain logic not covered by existing servers
- ✅ Need to extend Azure MCP with custom tools

### Extending Azure MCP

If you need to add custom tools alongside Azure MCP:

1. **Separate Server**: Create a custom MCP server for your tools
2. **Multi-Server Config**: Configure both servers in mcp.json
3. **Namespace Prefix**: Use distinct prefixes to avoid conflicts

```json
{
  "mcpServers": {
    "azure": {
      "command": "npx",
      "args": ["-y", "@azure/mcp@latest", "server", "start"]
    },
    "custom": {
      "command": "node",
      "args": ["./dist/custom-mcp-server.js"]
    }
  }
}
```

---

## Resources

- **Azure MCP Server**: [github.com/microsoft/mcp](https://github.com/microsoft/mcp)
- **MCP Protocol Spec**: [modelcontextprotocol.io](https://modelcontextprotocol.io)
- **Azure Identity**: [Azure SDK Authentication](https://learn.microsoft.com/azure/developer/javascript/sdk/authentication/overview)
- **Foundry Documentation**: [AI Foundry Docs](https://learn.microsoft.com/azure/ai-studio/)
- **Azure MCP Server Docs**: [learn.microsoft.com/azure/developer/azure-mcp-server](https://learn.microsoft.com/azure/developer/azure-mcp-server/)
- **AZD MCP Templates**: [azure.github.io/awesome-azd/?tags=mcp](https://azure.github.io/awesome-azd/?tags=mcp)

### Code Samples

| Sample | Description | Language |
|--------|-------------|----------|
| `remote-mcp-apim-functions-python` | Secure remote MCP with API Management | Python |
| `remote-mcp-functions-python` | Basic Azure Functions MCP | Python |
| `remote-mcp-functions-dotnet` | Azure Functions MCP | C# |
| `remote-mcp-functions-typescript` | Azure Functions MCP | TypeScript |
| `mcp-container-ts` | MCP on Azure Container Apps | TypeScript |

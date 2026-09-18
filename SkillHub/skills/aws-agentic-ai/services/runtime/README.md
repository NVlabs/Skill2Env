# Runtime Service

The Runtime service provides a secure, serverless hosting environment for deploying and running AI agents or tools. It handles scaling, session management, security isolation, and infrastructure management.

## Key Features

| Feature | Description |
|---------|-------------|
| **Framework Agnostic** | Works with LangGraph, Strands, CrewAI, or custom agents |
| **Model Flexibility** | Supports any LLM (Bedrock, Claude, Gemini, OpenAI) |
| **Protocol Support** | HTTP, MCP, A2A, and AG-UI — one protocol per Runtime |
| **Session Isolation** | Dedicated microVM per session with isolated CPU, memory, filesystem |
| **Extended Execution** | Up to 8 hours for long-running workloads (15-min idle timeout) |
| **100MB Payloads** | Handle multimodal content (text, images, audio, video) |
| **Bidirectional Streaming** | HTTP SSE and WebSocket for real-time interactions |

## Quick Start

### Prerequisites
- AWS CLI configured with appropriate permissions
- Docker installed for container builds (ARM64)
- Python 3.12+ for SDK usage

### Deploy an Agent

**Step 1: Install AgentCore SDK**
```bash
pip install bedrock-agentcore strands-agents strands-agents-tools
```

**Step 2: Create agent code**
```python
from bedrock_agentcore.runtime import BedrockAgentCoreApp
from strands import Agent

app = BedrockAgentCoreApp()
agent = Agent(system_prompt="You are a helpful assistant.")

@app.entrypoint
async def main(payload):
    async for event in agent.stream_async(payload.get("prompt", "")):
        if "data" in event:
            yield event["data"]

if __name__ == "__main__":
    app.run()  # Auto-listens on port 8080, auto-generates /ping and /invocations
```

> See [`scripts/runtime-fastapi-template.py`](../../scripts/runtime-fastapi-template.py) for a FastAPI-based alternative with MCPClient integration.

**Step 3: Create AgentCore Runtime**
```bash
aws bedrock-agentcore-control create-agent-runtime \
  --agent-runtime-name my-agent \
  --runtime-artifact '{"containerConfiguration": {"containerUri": "<ACCOUNT_ID>.dkr.ecr.<REGION>.amazonaws.com/my-agent:latest"}}' \
  --role-arn arn:aws:iam::<ACCOUNT_ID>:role/AgentRuntimeExecutionRole \
  --network-configuration '{"networkMode": "PUBLIC"}' \
  --protocol-configuration HTTP \
  --region us-west-2
```

**Step 4: Invoke agent**
```bash
aws bedrock-agentcore-runtime invoke-agent-runtime \
  --agent-runtime-endpoint-arn arn:aws:bedrock-agentcore:us-west-2:<ACCOUNT_ID>:runtime/my-agent/endpoint/DEFAULT \
  --payload '{"prompt": "Hello, agent!"}' \
  --region us-west-2
```

## Transforming an Existing Agent

To deploy an existing agent (built with Strands, LangGraph, or another framework) to AgentCore Runtime, wrap it with the `BedrockAgentCoreApp`:

### Transformation Checklist

1. **Add runtime dependency** to `requirements.txt`:
   ```
   bedrock-agentcore
   strands-agents       # or your framework
   ```

2. **Add runtime import**:
   ```python
   from bedrock_agentcore.runtime import BedrockAgentCoreApp
   ```

3. **Initialize the application**:
   ```python
   app = BedrockAgentCoreApp()
   ```

4. **Decorate the main entrypoint** with `@app.entrypoint`:
   ```python
   @app.entrypoint
   def handler(event, context):
       # Your existing agent logic here
       return agent.invoke(event)
   ```

5. **Add the application runner**:
   ```python
   if __name__ == "__main__":
       app.run()
   ```

### Complete Transformation Example

**Before** (standalone Strands agent):
```python
from strands import Agent

agent = Agent(system_prompt="You are a helpful assistant.")
response = agent("Hello!")
```

**After** (Runtime-compatible):
```python
from strands import Agent
from bedrock_agentcore.runtime import BedrockAgentCoreApp

app = BedrockAgentCoreApp()
agent = Agent(system_prompt="You are a helpful assistant.")

@app.entrypoint
def handler(event, context):
    user_input = event.get("input", "")
    return agent(user_input)

if __name__ == "__main__":
    app.run()
```

### `@app.entrypoint` vs `@app.handler()`

Both decorators register the main request handler. Use `@app.entrypoint` for simple synchronous handlers and `@app.handler()` for async handlers with streaming support:

| Decorator | Use Case |
|-----------|----------|
| `@app.entrypoint` | Synchronous, request-response agents |
| `@app.handler()` | Async agents, streaming, long-running tasks |

### Alternative: AgentCore CLI Deployment

The AgentCore CLI provides a streamlined deployment experience:

```bash
# Install the CLI
npm install -g @aws/agentcore

# Deploy (builds container, pushes to ECR, creates runtime)
agentcore deploy
```

The CLI automates containerization, ECR push, and runtime creation. For manual control, use the AWS CLI workflow below.

## Core Concepts

### Runtime → Version → Endpoint

- **Runtime**: Containerized application hosting your AI agent. Has a unique identity and is versioned for controlled updates.
- **Version**: Immutable configuration snapshot. V1 created automatically; each update creates a new version with rollback capability.
- **Endpoint**: Addressable access point. `DEFAULT` endpoint auto-created pointing to latest version. States: `CREATING` → `READY` → `UPDATING` → `READY`.

### Container Contract

| Requirement | Value |
|-------------|-------|
| Port | 8080 (HTTP/AG-UI), 8000 (MCP), 9000 (A2A) |
| Platform | `linux/arm64` |
| User | Non-root (uid=1000) |
| Required endpoints | `POST /invocations`, `GET /ping` |
| Ping response | `{"status": "Healthy"}` or `{"status": "HealthyBusy"}` |

> See [`scripts/Dockerfile.runtime-template`](../../scripts/Dockerfile.runtime-template) for a production-ready Dockerfile.

### MicroVM Sessions

Each session gets a dedicated microVM with isolated CPU, memory, and filesystem. Same session ID always routes to the same microVM.

| Parameter | Value |
|-----------|-------|
| Idle timeout | 15 minutes → auto-terminate |
| Max lifetime | 8 hours |
| Session ID | Min 33 characters (UUID recommended) |
| After termination | New request with same ID creates a fresh microVM |

States: `Active` (processing) → `Idle` (waiting) → `Terminated` (destroyed)

## Common Operations

### List Agent Runtimes
```bash
aws bedrock-agentcore-control list-agent-runtimes --region us-west-2
```

### Get Runtime Details
```bash
aws bedrock-agentcore-control get-agent-runtime \
  --agent-runtime-id <RUNTIME_ID> --region us-west-2
```

### Update Runtime
```bash
aws bedrock-agentcore-control update-agent-runtime \
  --agent-runtime-id <RUNTIME_ID> \
  --runtime-artifact '{"containerConfiguration": {"containerUri": "<NEW_IMAGE_URI>"}}' \
  --region us-west-2
```

### Delete Runtime
```bash
aws bedrock-agentcore-control delete-agent-runtime \
  --agent-runtime-id <RUNTIME_ID> --region us-west-2
```

## Supported Frameworks

| Framework | Description |
|-----------|-------------|
| **Strands** | AWS-native agent framework (recommended) |
| **LangGraph** | Graph-based agent workflows |
| **CrewAI** | Multi-agent collaboration |
| **Custom** | Any Python-based agent using FastAPI/Starlette |

## Troubleshooting

| Error | Cause | Solution |
|-------|-------|----------|
| 504 Gateway Timeout | Container issues, ARM64 compatibility | Ensure container exposes correct port (8080/8000/9000), use ARM64 image |
| 403 AccessDeniedException | Missing permissions | Verify IAM role has ECR, Bedrock, and TokenVault policies |
| exec format error | Wrong architecture | Build ARM64 containers with `docker buildx --platform linux/arm64` |
| Session terminated after 15min | Idle timeout | Implement `/ping` returning `{"status": "HealthyBusy"}` during background tasks |
| 401 Unauthorized | Missing or invalid JWT | Verify Cognito token and `allowedClients` configuration |

## Deep-Dive References

For production deployment architecture, detailed internals, and advanced patterns, see the reference documentation:

| Document | Covers |
|----------|--------|
| [**Runtime Core Mechanisms**](../../references/agentcore-runtime-core.md) | Container contract details, MicroVM Session model, Agent lifecycle (per-request vs per-session), tool integration (MCP/HTTP), MCPClient lifecycle, async background tasks, startup flow |
| [**Runtime Deployment & Operations**](../../references/agentcore-runtime-deploy.md) | CDK deployment (L1 CfnRuntime / L2 Construct), multi-Runtime architecture patterns, security model (4-layer), observability (OTel + CloudWatch), BedrockAgentCoreApp vs FastAPI comparison |
| [**Runtime Protocol Reference**](../../references/agentcore-runtime-protocols.md) | HTTP, MCP, A2A, AG-UI protocol specs — container contracts, endpoint formats, selection guide |
| [**OAuth Integration Guide**](../../references/agentcore-oauth-integration.md) | Three-layer OAuth architecture, Inbound JWT, Outbound Credential Provider, Gateway OAuth, Cognito configuration, 25+ IdP support, end-to-end CDK examples |

## Related Services

- **[Gateway Service](../gateway/README.md)**: Expose APIs as MCP tools for agents with transparent OAuth credential injection
- **[Memory Service](../memory/README.md)**: Short-term (multi-turn) + long-term (cross-session) conversation memory
- **[Identity Service](../identity/README.md)**: Credential providers, Token Vault, OAuth lifecycle management
- **[Observability Service](../observability/README.md)**: OpenTelemetry tracing, CloudWatch metrics, X-Ray integration
- **[Agent Registry](../registry/README.md)**: Catalog, discover, and govern deployed agents and tools

## References

- [AWS Runtime Documentation](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agents-tools-runtime.html)
- [How Runtime Works](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-how-it-works.html)
- [Runtime Troubleshooting](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-troubleshooting.html)
- [Runtime API Reference](https://docs.aws.amazon.com/bedrock-agentcore-control/latest/APIReference/)

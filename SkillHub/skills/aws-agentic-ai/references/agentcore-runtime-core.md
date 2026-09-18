# AgentCore Runtime Core Mechanisms: Container Contract, Session, Agent Lifecycle, Tool Integration

> An in-depth analysis of how the Strands Agents framework runs within Amazon Bedrock AgentCore Runtime, covering the MicroVM Session model, Agent lifecycle (per-request vs per-session), container contract, session management, tool integration, and startup process.
>
> Companion document: [Deployment & Operations](./agentcore-runtime-deploy.md) (CDK deployment, architecture patterns, security, observability, framework comparison)

---

## Table of Contents

- [1. What Is AgentCore](#1-what-is-agentcore)
- [2. Runtime Container Contract](#2-runtime-container-contract)
  - [2.1 Required Endpoints](#21-required-endpoints)
  - [2.2 Container Requirements](#22-container-requirements)
  - [2.3 CORS Configuration](#23-cors-configuration)
  - [2.4 Authentication](#24-authentication)
- [3. Request/Response Format](#3-requestresponse-format)
  - [3.1 Request Body (ChatRequest)](#31-request-body-chatrequest)
  - [3.2 Response Format (SSE Stream)](#32-response-format-sse-stream)
  - [3.3 External Invocation Example (JWT Bearer Mode)](#33-external-invocation-example-jwt-bearer-mode)
- [4. MicroVM Session Model](#4-microvm-session-model)
  - [4.1 Session Lifecycle](#41-session-lifecycle)
  - [4.2 Session States](#42-session-states)
  - [4.3 Comparison with Traditional Serverless](#43-comparison-with-traditional-serverless)
- [5. Agent Lifecycle Patterns](#5-agent-lifecycle-patterns)
  - [5.1 Per-request Pattern (Current Implementation)](#51-per-request-pattern-current-implementation)
  - [5.2 Per-session Pattern (Optimization Direction)](#52-per-session-pattern-optimization-direction)
  - [5.3 Comparison of the Two Patterns](#53-comparison-of-the-two-patterns)
  - [5.4 Role of session_manager](#54-role-of-session_manager)
  - [5.5 Asynchronous Background Tasks](#55-asynchronous-background-tasks)
- [6. Session Manager Configuration](#6-session-manager-configuration)
  - [6.1 Three-tier Fallback Strategy](#61-three-tier-fallback-strategy)
  - [6.2 Session ID Strategy](#62-session-id-strategy)
  - [6.3 AgentCore Memory Dual-layer Architecture](#63-agentcore-memory-dual-layer-architecture)
- [7. Tool Integration Methods](#7-tool-integration-methods)
  - [7.1 Two Tool Integration Patterns Overview](#71-two-tool-integration-patterns-overview)
  - [7.2 Pattern A — MCP Protocol (MCPClient)](#72-pattern-a--mcp-protocol-mcpclient)
  - [7.3 Pattern B — Direct HTTP (Stateless)](#73-pattern-b--direct-http-stateless)
  - [7.4 MCPClient Lifecycle Management](#74-mcpclient-lifecycle-management)
  - [7.5 MCP Connection Lifecycle Mapping to MicroVM](#75-mcp-connection-lifecycle-mapping-to-microvm)
  - [7.6 MCP Connection Resource Usage Analysis](#76-mcp-connection-resource-usage-analysis)
  - [7.7 Comparison of the Two Patterns](#77-comparison-of-the-two-patterns)
  - [7.8 Tool Registry](#78-tool-registry)
- [8. Startup Process](#8-startup-process)

---

## 1. What Is AgentCore

Amazon Bedrock AgentCore is an **Agent hosting platform** provided by AWS. Its core value proposition is: running Agent containers in an AWS-managed serverless environment, with enterprise-grade services such as Memory, Gateway, Identity, Observability, and more attached.

Key features:

- **Framework agnostic** — Supports Strands, LangGraph, CrewAI, LlamaIndex, OpenAI Agents SDK, and others
- **Model agnostic** — Bedrock (Claude, Nova, Llama), OpenAI, Gemini, and more
- **Serverless** — Automatic scaling, no infrastructure management required
- **Session isolation** — Each Session gets a dedicated MicroVM (isolated CPU/memory/filesystem)

Modular services provided by AgentCore:

| Service | Purpose |
|---------|---------|
| **Runtime** | Hosts Agent containers, providing a secure serverless execution environment |
| **Memory** | Short-term (multi-turn conversation) + long-term (cross-session) memory management |
| **Gateway** | Converts API/Lambda into MCP-compatible tools, transparently injects OAuth credentials (see [Deployment Section 4](./agentcore-runtime-deploy.md#4-security-model) and [OAuth Documentation](./agentcore-oauth-integration.md)) |
| **Identity** | Inbound JWT authentication + Outbound OAuth credential management, supporting 25+ IdPs (see [Deployment Section 4](./agentcore-runtime-deploy.md#4-security-model)) |
| **Observability** | OpenTelemetry integration, unified CloudWatch monitoring |
| **Code Interpreter** | Execute Python/JS/TS in an isolated sandbox |
| **Policy** | Governance rules defined in Cedar or natural language |

### Reading Guide: Two Dimensions x Two Authentication Methods

This document involves choices across multiple dimensions. Identify your path before reading further:

**Dimension 1: Building Approach (How to write code)**

| | BedrockAgentCoreApp | FastAPI Custom |
|---|---|---|
| Code style | `@app.entrypoint` + `yield` | `@app.post("/invocations")` + `StreamingResponse` |
| Endpoint generation | Automatic (`/invocations`, `/ping`, `/ws`) | Manually define each endpoint |
| Async tasks | Built-in `add_async_task` + Worker Loop | Must build yourself |
| See | [Deployment Section 6](./agentcore-runtime-deploy.md#6-bedrockagentcoreapp-vs-fastapi-build-approach-comparison) | This document Sections 2-5 (container contract, request format, Agent lifecycle) |

**Dimension 2: Deployment Approach (How to go live)**

| | CDK L2 (Recommended) | CDK L1 + Custom Container | Starter Toolkit CLI |
|---|---|---|---|
| Command | `AgentRuntimeArtifact.fromAsset/fromS3` | `CfnRuntime` + Dockerfile + ECR | `agentcore deploy` |
| Requires Docker | Depends on artifact source (`fromS3` does not) | Yes | No |
| Suitable for | **Production** (unified orchestration of all resources) | Production (requires full build control) | **Demo / Prototyping** |
| See | [Deployment Section 1](./agentcore-runtime-deploy.md#1-cdk-deployment) | [Deployment Section 1](./agentcore-runtime-deploy.md#1-cdk-deployment) | [Deployment Section 6](./agentcore-runtime-deploy.md#6-bedrockagentcoreapp-vs-fastapi-build-approach-comparison) |

**Dimension 3: Authentication Method (Who calls the Agent)**

| | IAM SigV4 (Default) | JWT Bearer Token (OAuth) |
|---|---|---|
| Configuration | No additional configuration needed | `authorizerConfiguration` + `customJWTAuthorizer` |
| Invocation method | `boto3.invoke_agent_runtime()` | HTTPS + `Authorization: Bearer {JWT}` |
| Relationship | **Mutually exclusive** — a single Runtime can only use one | |
| See | — | [Deployment Section 4](./agentcore-runtime-deploy.md#4-security-model) and [OAuth Documentation](./agentcore-oauth-integration.md) |

> **Quick navigation**: Core runtime mechanisms → This document. Deployment, security, observability, framework comparison → [Deployment document](./agentcore-runtime-deploy.md). OAuth details → [OAuth Documentation](./agentcore-oauth-integration.md).

---

## 2. Runtime Container Contract

AgentCore Runtime is essentially a **MicroVM-based container hosting service**. You provide a Docker image, and AgentCore launches a dedicated MicroVM for each Session to run it. The container must satisfy the following contract:

### 2.1 Required Endpoints

| Endpoint | Method | Purpose | Required |
|----------|--------|---------|----------|
| `/invocations` | POST | Receives chat requests, returns SSE stream | Yes |
| `/ping` | GET | Health check. Returns `{"status": "Healthy"}` or `{"status": "HealthyBusy"}` (when background tasks exist), optional `time_of_last_update` field | Yes |
| `/health` | GET | Detailed health status | No (optional) |
| `/ws` | WebSocket | WebSocket bidirectional communication (shares port 8080 with /invocations) | No |

### 2.2 Container Requirements

**AgentCore requirements:**
```
Port:       8080
Platform:   linux/arm64 (official documentation requires ARM64 compatibility)
Protocol:   HTTP / MCP / A2A / AGUI (choose one)
User:       Non-root (e.g., uid=1000, bedrock_agentcore)
Network:    PUBLIC or VPC
```

### 2.3 CORS Configuration

It is recommended to configure CORS to allow the AgentCore domain. AgentCore invokes the container server-side, so CORS is primarily relevant for WebSocket or direct browser connections (e.g., testing in the AgentCore Console):

```python
# [FastAPI Custom]
app.add_middleware(
    CORSMiddleware,
    allow_origins=[f"https://bedrock-agentcore.{aws_region}.amazonaws.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 2.4 Authentication

AgentCore supports two **mutually exclusive** authentication methods: **IAM SigV4** (default) and **JWT Bearer Token** (requires `authorizerConfiguration` configuration).

In **JWT Bearer mode**, AgentCore automatically validates the JWT signature and claims before the request reaches the container — the container **does not need** to perform validation itself. The container obtains user identity through:
- **Method A**: Extract `user_id` from the request body (simple and direct, passed by the caller)
- **Method B**: Decode JWT claims to get `sub`, `scope`, and other information (requires configuring `--request-header-allowlist "Authorization"`)

In **SigV4 mode**, the caller invokes through the AWS SDK (boto3, etc.), and IAM policies control access. If the Agent still needs to obtain an Outbound OAuth token on behalf of a specific user:
- **Method C**: The caller specifies the user ID via the `X-Amzn-Bedrock-AgentCore-Runtime-User-Id` header (requires additional IAM permission `InvokeAgentRuntimeForUser`)

See [Deployment Section 4](./agentcore-runtime-deploy.md#4-security-model) and [OAuth Documentation](./agentcore-oauth-integration.md) for details.

---

## 3. Request/Response Format

The AgentCore `InvokeAgentRuntime` API passes the `payload` as a byte stream to the container's `/invocations` endpoint. The internal format is defined by the application. Below is a typical application-layer format:

### 3.1 Request Body (ChatRequest)

```json
{
  "id": "chat-session-abc123",
  "user_id": "user@example.com",
  "messages": [
    {
      "id": "msg-001",
      "role": "user",
      "content": "Help me check my recent orders",
      "parts": [
        { "type": "text", "text": "Help me check my recent orders" }
      ]
    }
  ]
}
```

| Field | Description |
|-------|-------------|
| `id` | Session ID, used to correlate multi-turn conversations |
| `user_id` | User identifier, from JWT sub/email |
| `messages` | Message list containing the complete conversation history |
| `messages[].parts` | Structured representation of message content (supports text, attachment, etc.) |

### 3.2 Response Format (SSE Stream)

The response must be `text/event-stream`, pushing events incrementally:

```
data: {"type":"start","session_id":"chat-session-abc123","status":"executing"}

data: {"type":"tool-input-start","toolCallId":"tool-001","toolName":"search_orders"}

data: {"type":"tool-output-available","toolCallId":"tool-001","executionTimeMs":42}

data: {"type":"text-delta","delta":"Found 2 orders:"}

data: {"type":"text-delta","delta":"\n1. ORD-2024-001..."}

data: {"type":"finish","session_id":"chat-session-abc123"}

data: [DONE]
```

Event types:

| type | Description |
|------|-------------|
| `start` | Agent starts execution |
| `text-delta` | Incremental text output (streaming typewriter effect) |
| `tool-input-start` | Tool invocation started |
| `tool-output-available` | Tool execution completed |
| `error` | Execution error |
| `finish` | Agent execution completed |
| `[DONE]` | SSE stream end marker |

### 3.3 External Invocation Example (JWT Bearer Mode)

> For authentication method selection (JWT Bearer vs SigV4), see [Section 2.4](#24-authentication). For full details, see [Deployment Section 4](./agentcore-runtime-deploy.md#4-security-model) and [OAuth Documentation](./agentcore-oauth-integration.md).

When the Runtime has JWT Inbound Auth configured, the caller sends HTTPS requests directly to the AgentCore platform endpoint:

```
POST https://bedrock-agentcore.{region}.amazonaws.com/runtimes/{urlEncodedArn}/invocations?qualifier=DEFAULT
```

**Complete request example (TypeScript):**

```typescript
const escapedArn = encodeURIComponent(agentRuntimeArn);
const endpoint = `https://bedrock-agentcore.${settings.region}.amazonaws.com`
  + `/runtimes/${escapedArn}/invocations?qualifier=DEFAULT`;

const response = await fetch(endpoint, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${auth.user.access_token}`,               // Cognito JWT
    'X-Amzn-Bedrock-AgentCore-Runtime-Session-Id': currentChatId,      // Session correlation
    'X-Amzn-Bedrock-AgentCore-Runtime-User-Id': userId,                // Optional
  },
  body: JSON.stringify({
    id: currentChatId,
    user_id: userId,
    messages: messageHistory,
  }),
});
// response is an SSE stream (text/event-stream)
```

**Equivalent cURL:**

```bash
ESCAPED_ARN=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$AGENT_ARN', safe=''))")

curl -N \
  "https://bedrock-agentcore.us-east-1.amazonaws.com/runtimes/${ESCAPED_ARN}/invocations?qualifier=DEFAULT" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -H "X-Amzn-Bedrock-AgentCore-Runtime-Session-Id: session-001" \
  -d '{"id":"session-001","user_id":"user@example.com","messages":[{"role":"user","content":"Hello","parts":[{"type":"text","text":"Hello"}]}]}'
```

**Key points:**

| Element | Description |
|---------|-------------|
| **Endpoint** | `https://bedrock-agentcore.{region}.amazonaws.com` |
| **Path** | `/runtimes/{urlEncodedArn}/invocations` — The ARN must be URL encoded (contains special characters like `/` and `:`) |
| **Query parameter** | `qualifier=DEFAULT` (required) |
| **Authentication** | `Authorization: Bearer {JWT}` — Validated by the Inbound JWT Authorizer at the platform layer |
| **Session Header** | `X-Amzn-Bedrock-AgentCore-Runtime-Session-Id` — Requests with the same Session ID are routed to the same MicroVM |
| **Request body** | Application-defined JSON, transparently forwarded by AgentCore to the container's `/invocations` endpoint |
| **Response** | SSE stream (`text/event-stream`), format described in [Section 3.2](#32-response-format-sse-stream) |

> **`InvokeAgentRuntimeCommand`** is also invoked through the AgentCore platform endpoint (not the in-container endpoint). The HTTP path is presumed to be `/runtimes/{arn}/command`, but as of boto3 1.42.64 this API has not yet been published in the SDK. Official documentation only provides SDK examples (see [Section 5.5](#55-asynchronous-background-tasks)).

---

## 4. MicroVM Session Model

The key to understanding AgentCore Runtime is: **one Session = one dedicated MicroVM**. This is not a traditional serverless container pool (like Lambda), but rather a stateful, session-affinity execution environment.

### 4.1 Session Lifecycle

```
Client's first call to InvokeAgentRuntime(sessionId=abc)
                              |
                    +---------v----------+
                    |  Create MicroVM    |
                    | (Dedicated CPU/    |
                    |  Mem/FS)           |
                    |  Start container   |
                    +---------+----------+
                              |
              +---------------v---------------+
              |          Active               |
              |  Process requests / Execute   |
              |  background tasks             |
              +---------------+---------------+
                              | Request complete
              +---------------v---------------+
              |           Idle                |
              |  Retain context, wait for     |
              |  next request                 |
              |  (MicroVM still running)      |
              +---------------+---------------+
                              |
                   +----------+----------+
                   |                     |
              New request            Timeout/Expiry
              (same sessionId)           |
                   |          +----------v----------+
                   |          |     Terminated      |
                   |          |  MicroVM destroyed  |
                   |          |  Memory scrubbed    |
                   |          +---------------------+
                   v
              Return to Active (same MicroVM, same process)
```

**Key parameters:**

| Parameter | Value |
|-----------|-------|
| Idle timeout | 15 minutes without requests → automatic termination |
| Maximum lifetime | 8 hours |
| Session ID requirement | At least 33 characters (UUID recommended) |
| Behavior after termination | A new request with the same sessionId creates a **brand new MicroVM** (state is lost) |

**Core guarantee: All requests for the same Session are always routed to the same MicroVM.** The process, memory, and filesystem within the container persist for the duration of the Session lifecycle.

### 4.2 Session States

| State | Description |
|-------|-------------|
| **Active** | Currently processing synchronous requests, executing commands, or background tasks |
| **Idle** | No active requests, but the MicroVM remains running, waiting for the next invocation |
| **Terminated** | Terminated due to idle timeout (15 min), maximum duration reached (8 h), or health check failure |

### 4.3 Comparison with Traditional Serverless

| Dimension | Lambda / Traditional Serverless | AgentCore Runtime |
|-----------|---------------------------------|-------------------|
| Execution unit | Request-level (each invocation may hit a different instance) | **Session-level (dedicated MicroVM)** |
| State model | Stateless | **Stateful within Session** |
| Maximum runtime | 15 minutes | **8 hours** |
| Filesystem | Temporary (/tmp), not guaranteed across requests | **Persistent within Session** |
| Memory state | May be lost on cold start | **Persistent within Session** |
| Isolation granularity | Function-level | **Session-level MicroVM** |
| Hardware configuration | Configurable (memory 128MB-10GB) | **Not configurable** (AWS managed, vCPU/memory/storage specs not publicly disclosed) |

---

## 5. Agent Lifecycle Patterns

AgentCore's MicroVM model enables two viable patterns for Strands Agent lifecycle management.

### 5.1 Per-request Pattern (Current Implementation)

Each `/invocations` request creates a new Agent instance and restores conversation history from external storage via `session_manager`:

```
Request 1 (session=abc, MicroVM-A)
  -> Create Agent + session_manager.load()   # Deserialize history
  -> agent.stream_async("Hello")
  -> session_manager.save()                  # Serialize back to storage
  -> Agent instance discarded (but MicroVM persists)

Request 2 (session=abc, MicroVM-A)           # Same MicroVM!
  -> Create Agent + session_manager.load()   # Deserialize again
  -> agent.stream_async("Check orders")
  -> session_manager.save()
  -> Agent instance discarded
```

Corresponding code:

```python
# [FastAPI Custom]
@app.post("/invocations")
async def stream_agent(request: ChatRequest):
    session_id = request.id
    user_id = request.user_id

    # Create session_manager and Agent for each request
    session_manager = _create_session_manager(session_id, user_id)
    model = BedrockModel(model_id=model_id, boto_session=boto_session)
    agent = Agent(
        system_prompt=agent_system_prompt,
        model=model,
        tools=all_tools,
        session_manager=session_manager,
    )

    async def event_generator():
        async for event in agent.stream_async(user_message):
            yield sse_event(event)
    ...
```

**Characteristics:** Simple to implement, but incurs session_manager deserialization overhead on every request.

### 5.2 Per-session Pattern (Optimization Direction)

Leverages AgentCore MicroVM's Session affinity to cache the Agent instance in-process. Subsequent requests for the same Session directly reuse it, eliminating deserialization overhead:

```
Request 1 (session=abc, MicroVM-A)
  -> Create Agent + session_manager.load()   # First time: restore from external storage
  -> agent.stream_async("Hello")
  -> Cache Agent instance in process memory

Request 2 (session=abc, MicroVM-A)           # Same MicroVM!
  -> Cache hit, directly reuse Agent         # History already in memory
  -> agent.stream_async("Check orders")      # No deserialization needed
```

Strands Agent natively supports multiple invocations — each `agent(message)` call **appends** the new message to the internal conversation history rather than starting over. This makes per-session reuse safe:

```python
# Strands Agent supports multiple invocations, automatically accumulating history
agent = Agent(system_prompt="...", model=model, tools=tools)
agent("Hello")                     # Turn 1
agent("Help me check recent orders")  # Turn 2, automatically includes Turn 1 context
agent("What about last month?")       # Turn 3, automatically includes previous 2 turns
```

Implementation approach for per-session pattern:

```python
# [FastAPI Custom]
_agent_instance: Agent | None = None

@app.post("/invocations")
async def stream_agent(request: ChatRequest):
    global _agent_instance

    if _agent_instance is None:
        # First request: create Agent (session_manager restores history)
        session_manager = _create_session_manager(request.id, request.user_id)
        _agent_instance = Agent(
            system_prompt=agent_system_prompt,
            model=model,
            tools=all_tools,
            session_manager=session_manager,
        )

    # Subsequent requests: reuse Agent, conversation history already in memory
    async def event_generator():
        async for event in _agent_instance.stream_async(user_message):
            yield sse_event(event)
    ...
```

> Note: The example uses a `global` variable for simplicity. Production code can use `app.state` or FastAPI dependency injection instead.

**Why this is safe in AgentCore:**
- **One MicroVM = one Session = one process** — Different Sessions never share a process
- **`/invocations` requests are serial** — Only one `/invocations` request is processed at a time for the same Session (however, `InvokeAgentRuntimeCommand` can execute concurrently, and background tasks can also run simultaneously)
- **MicroVM is persistent within Session** — Process memory is not unexpectedly reclaimed

### 5.3 Comparison of the Two Patterns

| Dimension | Per-request (Current) | Per-session |
|-----------|-----------------------|-------------|
| Agent creation | New instance per request | Created on first request, reused thereafter |
| History restoration | Deserialized from session_manager each time | Deserialized once, subsequent turns use memory |
| Turn N latency | Same as Turn 1 (deserialization required) | Significantly reduced (deserialization skipped) |
| Implementation complexity | Simple | Must handle rebuilding after MicroVM termination |
| AgentCore compatibility | Fully compatible | Fully compatible |
| **Portability** | **Runs on any platform** | **AgentCore only** |

> **Portability is the key trade-off.** Per-session Agent relies on AgentCore MicroVM's Session affinity guarantee (requests for the same Session are always routed to the same MicroVM). If the Agent needs to be migrated to stateless platforms like ECS, EKS, or Lambda in the future, the per-session pattern will break — these platforms do not guarantee that requests for the same session land on the same container instance. The per-request + session_manager pattern is naturally compatible with any deployment target, since state is fully externalized.
>
> **MCPClient lifecycle is independent of Agent lifecycle.** Whether per-request or per-session, the MCPClient should be established once at startup and reused at the process level. See [Section 7.4](#74-mcpclient-lifecycle-management) for details.

### 5.4 Role of session_manager

Regardless of which Agent lifecycle pattern is adopted, `session_manager` provides value:

| Scenario | Role of session_manager |
|----------|------------------------|
| **Per-request pattern** | Restores history from external storage on each request, writes back after execution |
| **Per-session pattern** | Only restores history on first MicroVM startup; subsequent requests rely on Agent memory |
| **Rebuilding after MicroVM termination** | After 15-minute timeout destroys the MicroVM, a new MicroVM needs to restore history from Memory/S3 |
| **AgentCore Memory frontend visibility** | Synchronizes conversation history to the Memory service, making frontend chat history visible |

### 5.5 Asynchronous Background Tasks

AgentCore Runtime supports **asynchronous background tasks**: the Agent continues executing long-running work (data processing, file generation, model training, etc.) after responding to the user, while keeping the Session alive.

> **Building approach note**: The `@app.async_task`, `add_async_task`, `@app.ping` and other APIs in this section are provided by the **BedrockAgentCoreApp** SDK. If using **FastAPI Custom**, you only need the `/ping` endpoint to return `{"status": "HealthyBusy"}` when there are background tasks (see the FastAPI example at the end of this section).

#### Core Problem: 15-minute Idle Timeout

Normally, the Session enters Idle state after the last `/invocations` request completes, and automatically terminates after 15 minutes with no new requests. If the Agent starts a background task but has already returned the response, AgentCore considers the Session idle and destroys the MicroVM, causing the background task to be killed.

**Solution: `/ping` returns `HealthyBusy` status.** AgentCore continuously polls `/ping`, and when `HealthyBusy` is returned, the Session remains in Active state and the idle timeout timer is paused.

```
Session state after request completion:

/ping -> {"status": "Healthy"}      -> Idle state -> Terminates after 15 minutes
/ping -> {"status": "HealthyBusy"}  -> Active state -> Does not terminate until task completes or 8-hour limit reached
```

#### `/ping` Response Format

```json
{
  "status": "Healthy",           // or "HealthyBusy"
  "time_of_last_update": 1752275688  // Unix timestamp of when the status last changed
}
```

| Field | Type | Description |
|-------|------|-------------|
| `status` | string | `"Healthy"` (idle, can accept new requests) or `"HealthyBusy"` (has background tasks) |
| `time_of_last_update` | int | Unix timestamp of when the status last changed; AgentCore uses this to determine how long the Session has been in its current state |

#### Three Methods Provided by BedrockAgentCoreApp SDK

The `bedrock-agentcore` SDK's `BedrockAgentCoreApp` class includes comprehensive async task management (source: `bedrock_agentcore/runtime/app.py`):

**Method 1: `@app.async_task` Decorator**

> This decorator exists in the SDK source code (`bedrock_agentcore/runtime/app.py`) but is **not documented in official documentation**. It is an unpublished API, and its interface may change between versions. For production environments, Method 2 (manual management) is recommended.

Automatically tracks task lifecycle. During function execution, `/ping` returns `HealthyBusy`; after completion or exception, it automatically reverts to `Healthy`:

```python
# [BedrockAgentCoreApp]
from bedrock_agentcore import BedrockAgentCoreApp
from strands import Agent, tool

app = BedrockAgentCoreApp()

@app.async_task      # Automatically manages HealthyBusy status
async def process_large_dataset(file_path: str):
    """Long-running data processing task."""
    # During function execution, /ping -> HealthyBusy
    data = load_data(file_path)
    result = await heavy_computation(data)
    save_result(result)
    # After function returns, /ping -> Healthy (automatic recovery)

@tool
def start_data_processing(file_path: str) -> str:
    """Start background data processing task."""
    import asyncio
    asyncio.ensure_future(process_large_dataset(file_path))
    return f"Data processing started: {file_path}. You will be notified when processing is complete."

# Agent has the start_data_processing tool
# User says "Process /data/input.csv" -> Agent calls tool -> Tool starts background task
agent = Agent(tools=[start_data_processing])

@app.entrypoint
def main(payload):
    # Agent autonomously decides whether to call start_data_processing based on user intent
    return {"message": agent(payload.get("prompt", "")).message}

if __name__ == "__main__":
    app.run()
```

> Note: `@app.async_task` can only decorate `async` functions. Non-async functions will raise a `ValueError`.

**Method 2: Manual `add_async_task` / `complete_async_task` (Fine-grained Control)**

Suitable for use in threads or complex workflows, requiring manual lifecycle management:

```python
# [BedrockAgentCoreApp]
import threading

@tool
def start_background_task(duration: int = 60) -> str:
    """Start a background processing task."""
    # Register task -> /ping immediately becomes HealthyBusy
    task_id = app.add_async_task("background_processing", {"duration": duration})

    def background_work():
        try:
            time.sleep(duration)  # Simulate long-running operation
        finally:
            # Mark complete -> If no other active tasks, /ping reverts to Healthy
            app.complete_async_task(task_id)

    threading.Thread(target=background_work, daemon=True).start()
    return f"Background task started (ID: {task_id}), estimated completion in {duration} seconds."
```

Key details (from SDK source code):
- `add_async_task(name, metadata=None)` → Returns an `int` type task_id
- `complete_async_task(task_id)` → Returns `bool` (True=successfully completed, False=task_id not found)
- Multiple tasks can run simultaneously; as long as the `_active_tasks` dictionary is non-empty, `/ping` returns `HealthyBusy`
- The task counter uses `threading.Lock` for thread safety

**Method 3: Custom `@app.ping` Handler (Fully Customizable)**

```python
# [BedrockAgentCoreApp]
from bedrock_agentcore.runtime.models import PingStatus

@app.ping
def custom_ping():
    """Custom health check logic."""
    if gpu_task_running() or queue_has_pending_jobs():
        return PingStatus.HEALTHY_BUSY
    return PingStatus.HEALTHY
```

You can also force-override the status (for debugging or special scenarios):

```python
app.force_ping_status(PingStatus.HEALTHY_BUSY)   # Force Busy
app.clear_forced_ping_status()                     # Restore automatic detection
```

#### `/ping` Status Priority

The SDK internally determines the `/ping` response based on the following priority (`get_current_ping_status()` source logic):

```
1. forced_ping_status (forced status set by force_ping_status())
   | not set
2. @app.ping custom handler return value
   | not registered
3. Automatic detection: _active_tasks non-empty -> HealthyBusy, otherwise -> Healthy
```

#### Worker Loop Architecture: Preventing `/ping` from Being Blocked

AgentCore continuously polls `/ping` to determine Session health status. If `/ping` is unresponsive, the Session is determined to be Unhealthy and terminated. The SDK solves this problem through a **Worker Loop architecture**:

```
Main thread (uvicorn event loop)
    |
    +-- GET /ping -> Responds immediately (never blocks)
    |
    +-- POST /invocations
            |
            +-- _invoke_handler()
                    |
                    +-- async function -> Submitted to Worker Loop (separate thread)
                    |                      -> agentcore-worker-loop thread
                    |                        asyncio.run_coroutine_threadsafe()
                    |
                    +-- async generator -> Bridged to sync generator via Worker Loop
                    |                       -> queue.Queue producer-consumer model
                    |
                    +-- sync function -> run_in_threadpool (Starlette thread pool)
```

**Key design**: The `/invocations` handler executes in a **separate Worker Event Loop** (background daemon thread). Even if the handler blocks for several minutes, the main thread's `/ping` can still respond normally.

> This is the core advantage of `BedrockAgentCoreApp` over using FastAPI/Starlette directly. If you use FastAPI custom with a `/ping` endpoint and a long-running block occurs in the handler, it could theoretically delay `/ping` responses.

#### `InvokeAgentRuntimeCommand`: Executing Commands in the Same Session

In addition to `InvokeAgentRuntime` (corresponding to `/invocations`), AgentCore also provides `InvokeAgentRuntimeCommand`, which can execute shell commands in the **same MicroVM Session**:

```python
# Caller uses the same session_id
response = client.invoke_agent_runtime_command(
    agentRuntimeArn=agent_arn,
    runtimeSessionId="user-123-session-abc",  # Shares Session with InvokeAgentRuntime
    qualifier='DEFAULT',
    contentType='application/json',
    accept='application/vnd.amazon.eventstream',
    body={
        'command': '/bin/bash -c "git status"',
        'timeout': 60  # seconds
    }
)
```

> **Prerequisite**: Agents created after March 17, 2026 automatically support command execution. Agents deployed before this date need to be redeployed to use this feature.

> **Concurrency characteristics**: Command execution **does not block** Agent invocations. `InvokeAgentRuntime` and `InvokeAgentRuntimeCommand` can execute concurrently on the same Session.

Use cases:
- **Deterministic operations**: `git commit`, `npm test`, `python -m pytest` — No LLM reasoning needed
- **Environment inspection**: View filesystem, check process status, read logs
- **Agent collaboration**: Agent reasons via `/invocations` → Caller executes deterministic steps via `Command`

Both APIs share the same MicroVM: container, filesystem, and environment variables are identical.

#### Typical Async Task Scenarios

| Scenario | Approach | /ping Status |
|----------|----------|--------------|
| **Document OCR + Information Extraction** | Agent immediately replies "Processing", background thread performs OCR | HealthyBusy -> Healthy |
| **Batch Data Query** | Agent submits query request, background thread polls for results | HealthyBusy -> Healthy |
| **Model Inference Cache Warm-up** | Preload models/caches at startup, do not accept business requests until complete | HealthyBusy -> Healthy |
| **Real-time User Conversation** | Synchronous SSE streaming response, no background tasks | Always Healthy |

#### FastAPI Custom: Minimal Implementation

The capabilities of BedrockAgentCoreApp's `@app.async_task`, Worker Loop, etc. can be equivalently implemented in FastAPI with just a few lines of code:

```python
# [FastAPI Custom]
import threading
from fastapi import FastAPI

app = FastAPI()
_active_tasks: set[int] = set()
_task_lock = threading.Lock()
_task_counter = 0

@app.get("/ping")
def ping():
    status = "HealthyBusy" if _active_tasks else "Healthy"
    return {"status": status}

def add_task() -> int:
    global _task_counter
    with _task_lock:
        _task_counter += 1
        _active_tasks.add(_task_counter)
        return _task_counter

def complete_task(task_id: int):
    with _task_lock:
        _active_tasks.discard(task_id)
```

The core logic is simply maintaining an active task set, with `/ping` returning the corresponding status based on whether the set is empty. The `add_async_task` / `complete_async_task` of BedrockAgentCoreApp essentially does the same thing.

> **Tip**: If the Agent only performs synchronous SSE streaming responses (user sends message -> Agent reasons -> real-time response) without asynchronous background tasks, `/ping` should always return `Healthy`, and the above task tracking mechanism is not needed.

---

## 6. Session Manager Configuration

Strands Agent achieves conversation persistence through the `session_manager` parameter. AgentCore provides a native Memory service, and also supports custom fallback.

### 6.1 Three-tier Fallback Strategy

```
Priority 1: AgentCore Memory
    +- Condition: AGENTCORE_MEMORY_ENABLED=true + AGENTCORE_MEMORY_ID configured
    +- Features: Native integration, supports short-term + long-term memory, frontend-visible history
    +- Data lifecycle: Persistent, outlives MicroVM lifecycle

Priority 2: S3 Session Manager
    +- Condition: S3 Bucket environment variable configured (e.g., DATA_BUCKET_NAME, name is customizable)
    +- Path: s3://{bucket}/sessions/{agent_type}/{session_id}
    +- Data lifecycle: Persistent

Priority 3: File Session Manager
    +- Condition: Always available (local development fallback)
    +- Path: ./sessions/{session_id}
    +- Data lifecycle: Persistent within MicroVM, lost after MicroVM termination
```

> **Note**: When using FileSessionManager in AgentCore, since the MicroVM filesystem is persistent within the Session lifecycle, files are retained until MicroVM termination (up to 8 hours). However, data is lost after MicroVM termination, so production environments should use AgentCore Memory or S3.

### 6.2 Session ID Strategy

In multi-Agent systems, a recommended practice is to add an Agent type prefix to the session ID to avoid session conflicts between different Agents (this is not an AgentCore requirement, but an application-layer design choice):

```python
# Add Agent type prefix to session ID to avoid session conflicts between different Agents
# For example:
# Order Agent -> "order-{session_id}"
# Support Agent -> "support-{session_id}"
prefixed_session_id = f"{agent_type}-{session_id}"

# AgentCore API allows a maximum of 256 characters (minimum 33 characters)
# Note: Simple truncation may cause different sessions to produce the same ID;
# consider using a hash or ensuring the prefix+ID total length does not exceed the limit
if len(prefixed_session_id) > 256:
    prefixed_session_id = prefixed_session_id[:256]
```

### 6.3 AgentCore Memory Dual-layer Architecture

```
Short-term Memory
  +- Session-granularity multi-turn conversation history
  +- Automatically restores context from history
  +- Data managed by Session lifecycle

Long-term Memory
  +- Persistent across Sessions
  +- Can be shared across multiple Agents
  +- Supports semantic retrieval (top_k, relevance_threshold)
  +- Stores user preferences, facts, summaries, etc.
```

---

## 7. Tool Integration Methods

Agents have two major patterns for acquiring tools: **MCP Protocol** and **Custom HTTP**. Note: the lifecycle of tool connections (MCPClient) is independent of the Agent lifecycle and should not be conflated.

### 7.1 Two Tool Integration Patterns Overview

```
Pattern A: MCP Protocol (MCPClient connects to MCP Server)
+----------------------------------------------------------+
|  Agent (Strands)                                         |
|    |                                                     |
|  MCPClient (Streamable HTTP / stdio)                     |
|    | MCP Protocol                                        |
|  MCP Server                                              |
|    +-- AgentCore Gateway (AWS managed, with OAuth +      |
|    |   Lambda)                                           |
|    +-- Third-party MCP Server (Tavily, Sentry, etc.)     |
|    +-- Local MCP Server (stdio subprocess)               |
+----------------------------------------------------------+
  Agent side uniformly uses MCPClient; Server side can be Gateway or any MCP Server
  Transport: Streamable HTTP (remote) / stdio (local subprocess)

Pattern B: Custom HTTP (local @tool functions + HTTP calls)
+----------------------------------------------------------+
|  Agent (Strands)                                         |
|    | svc_http_request tool                               |
|  Backend API (/api/svc/*)                                |
|    |                                                     |
|  DynamoDB / Business Logic                               |
+----------------------------------------------------------+
  Non-MCP protocol; calls backend API via generic HTTP tool, Skill MD defines invocation spec
  Connection: No persistent connection, each HTTP request is independent
```

### 7.2 Pattern A — MCP Protocol (MCPClient)

The Agent side uniformly uses Strands `MCPClient` to connect to MCP Servers. The `bedrock-agentcore` SDK **does not automatically connect to Gateway** — you must manually create the MCPClient.

#### Connecting to AgentCore Gateway

**AgentCore Gateway is essentially an AWS-managed MCP Server** (created with `protocolType: "MCP"`, endpoint URL ending in `/mcp`). The Agent connects via MCPClient + Streamable HTTP transport:

**Script/CLI scenario (short lifecycle)** — `with` block automatically manages connection open/close:

```python
from strands import Agent
from strands.tools.mcp import MCPClient
from mcp.client.streamable_http import streamable_http_client

gateway_url = "https://{gatewayId}.gateway.bedrock-agentcore.{region}.amazonaws.com/mcp"
mcp_client = MCPClient(lambda: streamable_http_client(url=gateway_url))

with mcp_client:
    agent = Agent(tools=mcp_client.list_tools_sync())
    response = agent("Help me check my recent orders")
# with block ends -> connection automatically closed
```

**AgentCore Runtime scenario (long-running process)** — MCPClient should be created at startup and closed at shutdown. Do not use a `with` block (otherwise the connection closes when exiting the `with` block, and subsequent tool calls will fail):

```python
# [FastAPI Custom]
import os
from fastapi import FastAPI
from strands import Agent
from strands.tools.mcp import MCPClient
from mcp.client.streamable_http import streamable_http_client

app = FastAPI()
gateway_url = os.environ["MCP_SERVER_URL"]
# e.g. "https://{gatewayId}.gateway.bedrock-agentcore.{region}.amazonaws.com/mcp"

_mcp_client: MCPClient | None = None

@app.on_event("startup")
async def startup():
    global _mcp_client
    _mcp_client = MCPClient(lambda: streamable_http_client(url=gateway_url))
    # Connection is lazy-loaded — automatically established on first tool call

@app.post("/invocations")
async def invocations(request: ChatRequest):
    agent = Agent(tools=[*local_tools, _mcp_client])  # Reuse MCPClient
    ...

@app.on_event("shutdown")
async def shutdown():
    if _mcp_client:
        await _mcp_client.close()  # Close connection on process exit
```

If you need to pass authentication tokens (e.g., when the Gateway has a JWT Authorizer enabled), the required header depends on the Gateway Target type:

| Target Type | Required Header | Description |
|---|---|---|
| `GATEWAY_IAM_ROLE` | `Authorization` (user JWT) | Gateway uses its own IAM Role to invoke Lambda |
| `OAUTH` | `Authorization` + `WorkloadAccessToken` (WAT) | Gateway needs WAT to obtain third-party OAuth token from Token Vault |

```python
import httpx
from bedrock_agentcore.runtime.context import BedrockAgentCoreContext

headers_ctx = BedrockAgentCoreContext.get_request_headers() or {}

# GATEWAY_IAM_ROLE mode: only need to forward user JWT
http_client = httpx.AsyncClient(headers={
    "Authorization": headers_ctx.get("Authorization", ""),
})

# OAUTH mode: also need to pass WAT (Token Vault looks up third-party token by workload+user)
# http_client = httpx.AsyncClient(headers={
#     "Authorization": headers_ctx.get("Authorization", ""),
#     "WorkloadAccessToken": BedrockAgentCoreContext.get_workload_access_token(),
# })

mcp_client = MCPClient(lambda: streamable_http_client(url=gateway_url, http_client=http_client))
```

Complete Gateway invocation chain:

```
MCPClient -> Streamable HTTP POST -> AgentCore Gateway (/mcp endpoint)
                                        |
                                        +-- Routes to Lambda Target (executes tool logic)
                                        +-- OAuth credential injection (Token Vault)
                                        +-- Centralized tool registration (tool schema)
```

#### Connecting to Third-party MCP Servers

Connecting to third-party MCP Servers (such as Tavily, Sentry) works exactly the same way, with only a different URL:

```python
# Remote MCP Server (Streamable HTTP)
mcp_client = MCPClient(lambda: streamable_http_client(url="https://mcp.tavily.com/mcp"))

# Local MCP Server (stdio subprocess)
from mcp import stdio_client, StdioServerParameters
mcp_client = MCPClient(lambda: stdio_client(
    StdioServerParameters(command="uvx", args=["some-mcp-server"])
))
```

#### Gateway vs Direct Connection: Differences Are Only on the Server Side

| Dimension | AgentCore Gateway | Third-party MCP Server |
|-----------|-------------------|------------------------|
| Agent-side code | `MCPClient` + `streamable_http_client` | **Exactly the same** |
| Transport protocol | Streamable HTTP | Streamable HTTP / stdio |
| Additional capabilities | OAuth credential injection, Lambda routing, centralized registration | None |
| Tool discovery | `tools/list` (MCP standard) | **Exactly the same** |
| Use case | AWS managed tool services | Third-party/local MCP Servers |

Gateway uses Streamable HTTP transport — each MCP tool call is an independent HTTP POST with no persistent connection. Therefore, the Gateway pattern is fully transparent to both per-request and per-session modes, and **does not affect Agent lifecycle choice**.

### 7.3 Pattern B — Direct HTTP (Stateless)

```yaml
# agent_config.yaml
agent:
  tools:
    - "http_request"
    - "search_documents"
    - "current_time"
```

Local `@tool` functions call backend APIs via HTTP, with each call being an independent request with no persistent connection. The wrapper layer can inject auth headers at request time:

```python
# http_request_wrapper.py — Each call is independent, no connection pool
@tool
def http_request(url: str, method: str = "GET", **kwargs) -> str:
    """Call backend API with auto-injected auth headers."""
    headers = kwargs.get("headers", {})
    if "/api/svc/" in url:
        headers["X-Service-Api-Key"] = _service_api_key  # Auto-injected
    response = requests.request(method, url, headers=headers, **kwargs)
    return response.text
```

Similarly, this has **no impact** on Agent lifecycle choice.

### 7.4 MCPClient Lifecycle Management

MCPClient maintains a session with the MCP Server (whether connecting to Gateway or a third-party Server), and its lifecycle management requires attention.

> Note: The degree of MCPClient "persistence" depends on the transport protocol — stdio is a truly persistent connection (subprocess stays resident), while Streamable HTTP uses on-demand POST requests. See [Section 7.6](#76-mcp-connection-resource-usage-analysis) for details.

Using stdio transport as an example, the basic usage of Strands `MCPClient`:

```python
from strands.tools.mcp import MCPClient
from mcp import stdio_client, StdioServerParameters

# MCPClient manages a persistent connection
mcp_client = MCPClient(lambda: stdio_client(
    StdioServerParameters(command="uvx", args=["some-mcp-server"])
))

# Pass to Agent; Agent automatically connects on first use
agent = Agent(tools=[mcp_client])
agent("Turn 1")   # Connection established, tool discovery
agent("Turn 2")   # Reuses same connection
```

**MCPClient lifecycle characteristics:**

| Characteristic | Description |
|----------------|-------------|
| Connection establishment | Lazy-loaded — established on first tool call |
| Tool discovery | Automatically calls `list_tools` after connection to discover available tools |
| Connection reuse | Multiple calls from the same MCPClient instance reuse the same connection |
| Cleanup requirement | Requires explicit close. In scripts, use `with` statement; in long-running processes, call `close()` in the `shutdown` event |
| Transport methods | stdio (local subprocess), HTTP Streamable, SSE |

**Key insight: MCPClient and Agent are independent objects.** MCPClient manages the connection to the MCP Server; Agent manages conversation state. Their lifecycles can be controlled independently.

#### MCPClient Should Always Be Established at Startup

Regardless of which Agent lifecycle is adopted, MCPClient should be created once at startup and reused at the process level. The following three combinations are distinguished by Agent lifecycle:

**Combination A: startup MCP + per-request Agent (common pattern)**

```python
# [FastAPI Custom] Combination A
_mcp_client: MCPClient | None = None

@app.on_event("startup")
async def startup():
    global _mcp_client
    _mcp_client = MCPClient(lambda: stdio_client(...))
    # Connection is lazy-loaded, automatically established on first tool call

@app.post("/invocations")
async def stream_agent(request: ChatRequest):
    session_manager = _create_session_manager(request.id, request.user_id)
    agent = Agent(
        tools=[*all_tools, _mcp_client],   # New Agent each time, but reusing MCP connection
        session_manager=session_manager,
    )
    async for event in agent.stream_async(user_message):
        yield sse_event(event)
    # Agent discarded, but _mcp_client connection persists

@app.on_event("shutdown")
async def shutdown():
    if _mcp_client:
        await _mcp_client.close()
```

Agent is created new on each request (history restored via session_manager), while MCPClient is reused at the process level. Simple to implement, but incurs session_manager deserialization overhead on every request.

**Combination B: startup MCP + per-session Agent (fully leveraging MicroVM affinity)**

```python
# [FastAPI Custom] Combination B
_mcp_client: MCPClient | None = None
_agent_instance: Agent | None = None

@app.on_event("startup")
async def startup():
    global _mcp_client
    _mcp_client = MCPClient(lambda: stdio_client(...))

@app.post("/invocations")
async def stream_agent(request: ChatRequest):
    global _agent_instance
    if _agent_instance is None:
        session_manager = _create_session_manager(request.id, request.user_id)
        _agent_instance = Agent(
            tools=[*all_tools, _mcp_client],
            session_manager=session_manager,
        )
    async for event in _agent_instance.stream_async(user_message):
        yield sse_event(event)
    # Both Agent and MCP connection persist

@app.on_event("shutdown")
async def shutdown():
    if _mcp_client:
        await _mcp_client.close()
```

Both Agent and MCPClient persist for the MicroVM lifecycle. From Turn 2 onward, session_manager deserialization overhead is eliminated, and conversation history accumulates directly in Agent memory.

#### Summary

| Combination | MCPClient | Agent | MCP Overhead | Session Restore Overhead |
|-------------|-----------|-------|--------------|--------------------------|
| MCP per-request (anti-pattern) | New each time | New each time | **Every request** | Every request |
| **A: startup MCP + per-request Agent** | Once at startup | New each time | Once | **Every request** |
| **B: startup MCP + per-session Agent** | Once at startup | Created once | Once | **First request only** |

> **Anti-pattern note**: MCP per-request means creating a new MCPClient within each request handler (e.g., using `with MCPClient(...):` block inside the handler). This re-establishes the connection + tool discovery on every request, incurring significant overhead. This should be avoided in AgentCore long-running processes.

The MCP overhead for all three combinations depends on MCPClient lifecycle (should be once at startup). The difference is only at the Agent level: per-session eliminates session_manager deserialization for subsequent requests.

### 7.5 MCP Connection Lifecycle Mapping to MicroVM

MCPClient should be created at startup, with its lifecycle bound to the **process** (not the Agent). The following uses stdio transport as an example (Streamable HTTP has no persistent connection, but the MCPClient instance is similarly reused at the process level):

```
MicroVM Lifecycle (up to 8 hours) — stdio transport example
|
+-- Container startup
|     +-- MCPClient created (lazy-loaded, connection not yet established)
|
+-- Request 1
|     +-- Create Agent (per-request or per-session)
|     +-- Agent's first MCP tool call -> MCPClient establishes connection + discovers tools
|     +-- Tool calls execute through persistent connection
|
+-- Request 2 (same Session)
|     +-- Create new Agent (per-request) or reuse (per-session)
|     +-- Reuses existing MCPClient connection (zero MCP overhead)
|
+-- Request N ...
|     +-- MCPClient connection always reused, regardless of whether Agent is rebuilt
|
+-- Idle (up to 15 minutes)
|     +-- MCPClient connection persists (MicroVM still running)
|
+-- MicroVM termination (shutdown)
      +-- MCPClient.close(), process destroyed
```

**Key point:** MCPClient is reused at the process level, Agent at the request level or Session level — the two are decoupled. Per-request Agent does not mean per-request MCP connection.

### 7.6 MCP Connection Resource Usage Analysis

MCPClient maintains its connection for the MicroVM lifecycle (up to 8 hours). Does this waste resources? The answer depends on the MCP transport protocol.

#### stdio Transport (Strands MCPClient Default)

The Client starts the MCP Server as a **subprocess**, communicating via stdin/stdout. The subprocess stays resident throughout the entire MicroVM lifecycle:

```
MCPClient <-stdin/stdout-> MCP Server subprocess (resident)
```

- The subprocess lives from creation until MicroVM destruction (up to 8 hours)
- The MCP specification **does not define idle timeout or heartbeat mechanisms** — the process silently waits during idle periods
- Shutdown method: Client closes stdin -> SIGTERM -> wait -> SIGKILL
- Idle resource usage: Memory (typically 10-50MB), process slot; CPU near zero

**Key point: In stdio mode, the MCP Server is a local subprocess — there is no issue of "occupying remote server connections."** Resource consumption is confined within the MicroVM, and the MicroVM itself is a dedicated resource allocated for a single Session. The 8-hour idle period is ultimately bounded by MicroVM termination.

#### Streamable HTTP Transport

Each message is an independent HTTP POST request; the connection is **not persistent**:

```
MCPClient --POST--> MCP Server (remote)
          <-200/SSE--
          (connection closed)
```

- The Server maintains logical session state via the `Mcp-Session-Id` header
- No persistent TCP connections between requests (unless an SSE stream is in progress)
- The Client can send an HTTP `DELETE` to explicitly terminate the session
- **Zero connection resources** when idle; Server only needs to maintain session metadata

#### Resource Comparison of the Two Transport Protocols

| Dimension | stdio (Local Subprocess) | Streamable HTTP (Remote) |
|-----------|--------------------------|--------------------------|
| Idle connections | Process remains resident, stdin/stdout open | No persistent connection |
| Memory usage | Subprocess resident (~10-50MB) | Only session metadata |
| MicroVM 8h scenario | Subprocess lives 8h, low idle overhead | On-demand connections, no idle overhead |
| Remote Server pressure | N/A (local process) | Low (no persistent connections) |
| Cleanup mechanism | Subprocess auto-terminates on MicroVM destruction | Client sends DELETE or Server times out |

#### Conclusion

- **stdio**: Resource overhead is acceptable. The MCP Server subprocess lives and dies with the MicroVM, consuming only a small amount of memory when idle, with no impact on external systems.
- **Streamable HTTP**: More lightweight. No persistent connections, suitable for connecting to remote MCP Servers.
- **Practical recommendation**: If the MCP Server is a local tool process (e.g., file operations, code execution), use stdio; if connecting to third-party remote MCP Servers and concerned about connection counts, prefer Streamable HTTP transport.

### 7.7 Comparison of the Two Patterns

| Dimension | MCP Protocol (A) | Custom HTTP (B) |
|-----------|-------------------|-----------------|
| Communication protocol | MCP (JSON-RPC 2.0) | Custom HTTP |
| Agent side | Strands `MCPClient` | Local Python `@tool` functions |
| Tool discovery | MCP `tools/list` (automatic discovery) | Defined in Skill MD or code |
| Transport | Streamable HTTP (remote) / stdio (local) | Independent HTTP requests |
| Connection overhead | First connection + tool discovery (once at startup) | None |
| Recommended lifecycle | Establish MCPClient at startup, reuse at process level | No requirements |

**MCP pattern Server-side variants:**

| Server Side | Additional Capabilities | Use Case |
|-------------|-------------------------|----------|
| **AgentCore Gateway** | OAuth credential injection, Lambda routing, centralized registration | AWS managed tool services |
| **Third-party MCP Server** | None | Tavily, Sentry, and other third-party tools |
| **Local MCP Server** (stdio) | None | File operations, code execution, and other local tools |

### 7.8 Tool Registry

Regardless of the pattern, local tools can be mapped from names to implementations via a registry dictionary, enabling configuration-driven tool loading:

```python
TOOL_REGISTRY = {
    "current_time": current_time,          # strands_tools built-in
    "http_request": http_request,          # Custom wrapper (auto-injects auth headers)
    "search_documents": search_documents,  # Custom @tool
}
```

YAML configuration references tool names, which are resolved to actual functions from the registry at startup:

```yaml
agent:
  tools:
    - "current_time"
    - "http_request"
    - "search_documents"
```

If MCPClient is enabled, it is passed as an additional `tools` parameter to the Agent, coexisting with local tools:

```python
agent = Agent(
    tools=[
        *all_tools,          # Local registry tools
        mcp_client_a,        # Tools from MCP Server A
        mcp_client_b,        # Tools from MCP Server B
    ],
    session_manager=session_manager,
)
```

---

## 8. Startup Process

Typical initialization steps when the container starts:

```
Container startup (uvicorn main:app)
    |
    +-- 1. Web framework initialization + middleware registration (CORS, etc.)
    |
    +-- @app.on_event("startup")
         |
         +-- 2. Load configuration (S3 first -> local fallback)
         |       agent_config.yaml
         |
         +-- 3. Inject runtime variables
         |       Environment variables -> system prompt template
         |
         +-- 4. Load secrets (Secrets Manager / environment variables)
         |       -> Configure tool wrapper layer
         |
         +-- 5. Initialize MCPClient (if needed)
         |       Connect to Gateway or third-party MCP Server
         |
         +-- 6. Resolve tool list
                 YAML tool names -> registry lookup -> all_tools[]
```

**Cold start optimization**: If S3 configuration loading fails, startup will not block. Initialization can be deferred to the first `/invocations` request.

---

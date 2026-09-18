# AgentCore Runtime Protocol Reference: HTTP, MCP, A2A, AG-UI

> AgentCore Runtime supports four communication protocols, each targeting a different interaction pattern. This document, based on AWS official documentation, provides a detailed explanation of each protocol's container contract, endpoint specification, request/response format, and applicable scenarios.

---

## Table of Contents

- [1. Protocol Overview](#1-protocol-overview)
- [2. HTTP Protocol](#2-http-protocol)
  - [2.1 Container Contract](#21-container-contract)
  - [2.2 Endpoint Details](#22-endpoint-details)
  - [2.3 Applicable Scenarios](#23-applicable-scenarios)
- [3. MCP Protocol](#3-mcp-protocol)
  - [3.1 MCP Protocol Core Concepts](#31-mcp-protocol-core-concepts)
  - [3.2 MCP Container Contract in AgentCore](#32-mcp-container-contract-in-agentcore)
  - [3.3 Endpoint Details](#33-endpoint-details)
  - [3.4 Session Management](#34-session-management)
  - [3.5 Code Example](#35-code-example)
  - [3.6 Relationship with AgentCore Gateway](#36-relationship-with-agentcore-gateway)
  - [3.7 Applicable Scenarios](#37-applicable-scenarios)
- [4. A2A Protocol](#4-a2a-protocol)
  - [4.1 A2A Protocol Core Concepts](#41-a2a-protocol-core-concepts)
  - [4.2 A2A Container Contract in AgentCore](#42-a2a-container-contract-in-agentcore)
  - [4.3 Endpoint Details](#43-endpoint-details)
  - [4.4 Error Handling](#44-error-handling)
  - [4.5 Code Example](#45-code-example)
  - [4.6 Applicable Scenarios](#46-applicable-scenarios)
- [5. AG-UI Protocol](#5-ag-ui-protocol)
  - [5.1 What Problem Does AG-UI Solve](#51-what-problem-does-ag-ui-solve)
  - [5.2 AG-UI Container Contract in AgentCore](#52-ag-ui-container-contract-in-agentcore)
  - [5.3 Endpoint Details](#53-endpoint-details)
  - [5.4 AG-UI Event Types](#54-ag-ui-event-types)
  - [5.5 Code Example](#55-code-example)
  - [5.6 Integration with CopilotKit](#56-integration-with-copilotkit)
  - [5.7 Applicable Scenarios](#57-applicable-scenarios)
- [6. Comparison of the Four Protocols](#6-comparison-of-the-four-protocols)
- [7. How to Choose a Protocol](#7-how-to-choose-a-protocol)
- [8. Authentication: Common to All Protocols](#8-authentication-common-to-all-protocols)

---

## 1. Protocol Overview

AgentCore Runtime specifies the protocol at creation time via `protocolConfiguration`. **A single Runtime can only use one protocol**:

| Protocol | Purpose | Port | Primary Endpoint | Communication Mode | Creator |
|----------|---------|------|------------------|--------------------|---------|
| **HTTP** | General-purpose agent interaction | 8080 | `POST /invocations` | JSON / SSE / WebSocket | — |
| **MCP** | Tool and data services | 8000 | `POST /mcp` | JSON-RPC 2.0 | Anthropic |
| **A2A** | Inter-agent collaboration | 9000 | `POST /` | JSON-RPC 2.0 | Google |
| **AG-UI** | Agent-to-frontend UI | 8080 | `POST /invocations` | SSE event stream | Led by CopilotKit |

All four protocols share the same AgentCore infrastructure: MicroVM session isolation, OAuth/SigV4 authentication, and auto-scaling. The difference lies in the **communication contract inside the container**.

> **All protocols must implement the `GET /ping` health check endpoint** (returning `{"status": "Healthy"}` or `{"status": "HealthyBusy"}`). This is a universal requirement of AgentCore Runtime and does not belong to any specific protocol's specification.

```
Caller -> AgentCore Platform (Auth + Routing) -> Container inside MicroVM
                                                   |
                                                   |-- HTTP:  POST :8080/invocations
                                                   |-- MCP:   POST :8000/mcp
                                                   |-- A2A:   POST :9000/
                                                   +-- AG-UI: POST :8080/invocations
```

> Regardless of which protocol is chosen, the AgentCore platform endpoint used by external callers is **always the same**:
> ```
> POST https://bedrock-agentcore.{region}.amazonaws.com/runtimes/{urlEncodedArn}/invocations?qualifier=DEFAULT
> ```
> After receiving the request, the AgentCore platform layer passes the payload through to the container's corresponding endpoint based on the `protocolConfiguration`.

---

## 2. HTTP Protocol

**Purpose**: The most general-purpose protocol, suitable for custom agent applications. The request/response format is entirely defined by the application; AgentCore only performs pass-through.

### 2.1 Container Contract

| Specification | Requirement |
|---------------|-------------|
| Listen Address | `0.0.0.0:8080` |
| Platform | ARM64 container |
| Required Endpoints | `POST /invocations`, `GET /ping` |
| Optional Endpoints | `GET /ws` (WebSocket) |

### 2.2 Endpoint Details

#### `POST /invocations` — Primary Interaction Endpoint

The AgentCore `InvokeAgentRuntime` API passes the caller's payload as a byte stream **as-is** to this endpoint. The request body format is defined by the application.

**Responses support two modes:**

**Mode A: JSON (non-streaming)**
```
Content-Type: application/json

{"response": "Query results...", "status": "success"}
```
Suitable for: Simple Q&A, deterministic computations, status queries.

**Mode B: SSE (streaming)**
```
Content-Type: text/event-stream

data: {"event": "partial response 1"}
data: {"event": "partial response 2"}
data: {"event": "final response"}
```
Suitable for: Real-time conversations, progressive content generation, long-running operations.

#### `GET /ws` — WebSocket (Optional)

Shares port 8080 with `/invocations`. Establishes a WebSocket connection via standard HTTP Upgrade:

```
GET /ws HTTP/1.1
Connection: Upgrade
Upgrade: websocket
Sec-WebSocket-Version: 13
X-Amzn-Bedrock-AgentCore-Runtime-Session-Id: session-uuid
```

Supports text (JSON / plain text) and binary messages. Suitable for scenarios requiring bidirectional real-time communication.

#### `GET /ping` — Health Check

```json
{"status": "Healthy", "time_of_last_update": 1640995200}
```

| Status Value | Meaning |
|-------------|---------|
| `Healthy` | Ready, can accept new requests |
| `HealthyBusy` | Running but has background async tasks (session stays active and will not be reclaimed due to idle timeout) |

### 2.3 Applicable Scenarios

- Custom agent applications (this project uses this protocol)
- Need for full control over request/response format
- Agents built with Strands Agents, LangGraph, and similar frameworks
- Scenarios requiring WebSocket bidirectional communication

---

## 3. MCP Protocol

**Purpose**: Expose an agent's tool and data capabilities in a standardized way. MCP (Model Context Protocol), created by Anthropic, is an open standard for connecting AI applications with external systems (tools, data sources, workflows).

### 3.1 MCP Protocol Core Concepts

MCP uses a **client-server architecture**:

```
MCP Host (AI application, e.g. Claude Code)
  |-- MCP Client 1 --> MCP Server A (File System)
  |-- MCP Client 2 --> MCP Server B (Database)
  +-- MCP Client 3 --> MCP Server C (Sentry)
```

MCP Servers expose three core primitives:

| Primitive | Purpose | Discovery Method |
|-----------|---------|------------------|
| **Tools** | Executable functions (file operations, API calls, database queries) | `tools/list` -> `tools/call` |
| **Resources** | Contextual data sources (file contents, database records, API responses) | `resources/list` -> `resources/read` |
| **Prompts** | Interaction templates (system prompts, few-shot examples) | `prompts/list` -> `prompts/get` |

> **Note**: The three primitives are defined by the MCP protocol standard. In the AgentCore hosting scenario, **Tools** is the most commonly used primitive; support for Resources and Prompts depends on the specific MCP Server implementation.

Communication is based on **JSON-RPC 2.0**, with the transport layer supporting two mechanisms:
- **Stdio**: Local inter-process communication (standard input/output)
- **Streamable HTTP**: Remote communication, HTTP POST + optional SSE streaming

### 3.2 MCP Container Contract in AgentCore

| Specification | Requirement |
|---------------|-------------|
| Listen Address | `0.0.0.0:8000` |
| Platform | ARM64 container |
| Primary Endpoint | `POST /mcp` |
| Health Check | `GET /ping` |
| Transport | Streamable HTTP |
| Default Mode | Stateless (`stateless_http=True`) |

> **Note the port difference**: MCP uses **8000**, HTTP/AG-UI use 8080, A2A uses 9000.

### 3.3 Endpoint Details

#### `POST /mcp` — MCP RPC Message Handler

AgentCore passes the `InvokeAgentRuntime` payload as a standard MCP JSON-RPC message **directly** to this endpoint.

**Request Example (Tool Discovery):**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/list"
}
```

**Response Example:**
```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "tools": [
      {
        "name": "add_numbers",
        "description": "Add two numbers together",
        "inputSchema": {
          "type": "object",
          "properties": {
            "a": {"type": "integer"},
            "b": {"type": "integer"}
          },
          "required": ["a", "b"]
        }
      }
    ]
  }
}
```

**Tool Invocation:**
```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/call",
  "params": {
    "name": "add_numbers",
    "arguments": {"a": 3, "b": 5}
  }
}
```

Response Content-Type supports `application/json` or `text/event-stream`.

### 3.4 Session Management

- The AgentCore platform automatically adds an `Mcp-Session-Id` header for session isolation
- Default stateless mode: The server should not reject platform-generated Session IDs
- Stateful mode (`stateless_http=False`): Supports elicitation (multi-turn interaction) and sampling (requesting LLM-generated content)

### 3.5 Code Example

```python
# my_mcp_server.py
from mcp.server.fastmcp import FastMCP

mcp = FastMCP(host="0.0.0.0", stateless_http=True)

@mcp.tool()
def add_numbers(a: int, b: int) -> int:
    """Add two numbers together"""
    return a + b

@mcp.tool()
def greet_user(name: str) -> str:
    """Greet a user by name"""
    return f"Hello, {name}!"

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
```

**Deployment:**
```bash
agentcore configure -e my_mcp_server.py --protocol MCP
agentcore deploy
```

**Remote Invocation (Python MCP Client):**
```python
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

encoded_arn = agent_arn.replace(':', '%3A').replace('/', '%2F')
mcp_url = f"https://bedrock-agentcore.us-west-2.amazonaws.com/runtimes/{encoded_arn}/invocations?qualifier=DEFAULT"
headers = {
    "authorization": f"Bearer {bearer_token}",
    "Content-Type": "application/json"
}

async with streamablehttp_client(mcp_url, headers, timeout=120, terminate_on_close=False) as (
    read_stream, write_stream, _
):
    async with ClientSession(read_stream, write_stream) as session:
        await session.initialize()
        tools = await session.list_tools()
        print(tools)
```

You can also use **MCP Inspector** (`npx @modelcontextprotocol/inspector`) for visual testing.

### 3.6 Relationship with AgentCore Gateway

AgentCore Gateway can register MCP Servers as tools, providing transparent OAuth credential injection for agents:

```
Agent -> AgentCore Gateway -> MCP Server (hosted on AgentCore Runtime)
                |
                |-- Inbound: Verify agent identity (JWT)
                |-- Tool Routing: MCP tool_name -> target MCP Server
                +-- Outbound: Retrieve OAuth token from Token Vault -> inject into request
```

### 3.7 Applicable Scenarios

- Exposing tool and data capabilities in a standardized way to AI applications
- Need to be invoked by multiple different AI clients (Claude, ChatGPT, VS Code, etc.)
- Providing tool services with OAuth credential injection via AgentCore Gateway
- Already have an MCP Server and want to host it on AgentCore for session isolation and auto-scaling

---

## 4. A2A Protocol

**Purpose**: Inter-agent collaboration communication. A2A (Agent-to-Agent), created by Google and donated to the Linux Foundation, is an open standard that enables agents from different frameworks and organizations to collaborate in a **peer-to-peer manner**.

### 4.1 A2A Protocol Core Concepts

**Agent Opacity**: The core design principle of A2A is that agents **do not need to share internal memory, private logic, or tool implementations**. Collaboration is achieved through message passing, with each agent remaining a black box.

```
Agent A (Claims Processing)            Agent B (Policy Verification)
  |                                      |
  |  Does not know B's internals         |  Does not know A's internals
  |  Interacts only via A2A messages     |  Interacts only via A2A messages
  |                                      |
  +------ JSON-RPC 2.0 / HTTP ----------+
```

**Communication Methods:**
- JSON-RPC 2.0 over HTTP(S)
- Supports synchronous request/response, SSE streaming, and asynchronous push notifications
- Data types: text, files, structured JSON

**Agent Card**: Each A2A agent exposes its metadata at `/.well-known/agent-card.json` for **dynamic discovery**:

```json
{
  "name": "Calculator Agent",
  "description": "A calculator agent for arithmetic operations",
  "version": "1.0.0",
  "url": "https://bedrock-agentcore.us-west-2.amazonaws.com/runtimes/{arn}/invocations/",
  "protocolVersion": "0.3.0",
  "preferredTransport": "JSONRPC",
  "capabilities": {"streaming": true},
  "defaultInputModes": ["text"],
  "defaultOutputModes": ["text"],
  "skills": [
    {
      "id": "arithmetic",
      "name": "Arithmetic",
      "description": "Basic arithmetic operations"
    }
  ]
}
```

### 4.2 A2A Container Contract in AgentCore

| Specification | Requirement |
|---------------|-------------|
| Listen Address | `0.0.0.0:9000` |
| Platform | ARM64 container |
| Primary Endpoint | `POST /` (root path) |
| Agent Card | `GET /.well-known/agent-card.json` |
| Health Check | `GET /ping` |

> **Note**: The A2A primary endpoint is the root path `/`, not `/invocations`. The port is **9000**.

### 4.3 Endpoint Details

#### `POST /` — JSON-RPC 2.0 Message Handler

AgentCore passes the `InvokeAgentRuntime` payload as a JSON-RPC message **directly**.

**Request Example (Send Message):**
```json
{
  "jsonrpc": "2.0",
  "id": "req-001",
  "method": "message/send",
  "params": {
    "message": {
      "role": "user",
      "parts": [{"kind": "text", "text": "what is 101 * 11?"}],
      "messageId": "12345678-1234-1234-1234-123456789012"
    }
  }
}
```

**Response Example:**
```json
{
  "jsonrpc": "2.0",
  "id": "req-001",
  "result": {
    "artifacts": [
      {
        "artifactId": "unique-artifact-id",
        "name": "agent_response",
        "parts": [{"kind": "text", "text": "101 * 11 = 1111"}]
      }
    ]
  }
}
```

#### `GET /.well-known/agent-card.json` — Agent Discovery

Returns the Agent Card JSON, describing the agent's identity, capabilities, skills, and authentication requirements. Callers use this endpoint to learn what the agent can do and how to interact with it.

### 4.4 Error Handling

A2A errors are returned as **JSON-RPC 2.0 error responses**, with **HTTP status code always 200** (protocol compliance requirement):

| JSON-RPC Code | Meaning | Corresponding HTTP Semantics |
|---------------|---------|------------------------------|
| -32501 | Resource not found | 404 |
| -32052 | Request validation failed | 400 |
| -32053 | Rate limit exceeded | 429 |
| -32054 | Resource conflict | 409 |
| -32055 | Runtime client error | 424 |

```json
{
  "jsonrpc": "2.0",
  "id": "req-001",
  "error": {"code": -32052, "message": "Validation error - Invalid request data"}
}
```

### 4.5 Code Example

```python
# my_a2a_server.py
import os, logging, uvicorn
from strands import Agent
from strands.multiagent.a2a import A2AServer
from strands_tools.calculator import calculator
from fastapi import FastAPI

logging.basicConfig(level=logging.INFO)

runtime_url = os.environ.get('AGENTCORE_RUNTIME_URL', 'http://127.0.0.1:9000/')

strands_agent = Agent(
    name="Calculator Agent",
    description="A calculator agent that can perform basic arithmetic operations.",
    tools=[calculator],
    callback_handler=None
)

a2a_server = A2AServer(
    agent=strands_agent,
    http_url=runtime_url,
    serve_at_root=True  # AgentCore A2A contract requires the primary endpoint at the / root path
)

app = FastAPI()

@app.get("/ping")
def ping():
    return {"status": "healthy"}

app.mount("/", a2a_server.to_fastapi_app())

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9000)
```

**Deployment:**
```bash
pip install strands-agents[a2a] bedrock-agentcore strands-agents-tools
agentcore configure -e my_a2a_server.py --protocol A2A
agentcore deploy
```

**Fetching the Agent Card Remotely:**
```bash
ESCAPED_ARN=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$AGENT_ARN', safe=''))")

curl "https://bedrock-agentcore.us-west-2.amazonaws.com/runtimes/${ESCAPED_ARN}/invocations/.well-known/agent-card.json" \
  -H "Authorization: Bearer ${BEARER_TOKEN}" \
  -H "X-Amzn-Bedrock-AgentCore-Runtime-Session-Id: $(uuidgen)"
```

### 4.6 Applicable Scenarios

- Multi-agent collaboration systems (different agents handle their own responsibilities, collaborating via messages)
- Cross-framework agent interoperability (e.g., Strands Agent collaborating with LangGraph Agent)
- Cross-organization agent communication (Agent Card enables dynamic discovery)
- Scenarios requiring agents to remain black boxes without exposing internal implementations

---

## 5. AG-UI Protocol

**Purpose**: Standardized communication from agent to frontend UI. AG-UI (Agent-User Interaction Protocol) is led by the CopilotKit team and developed in collaboration with multiple framework teams including LangGraph, CrewAI, AWS Strands, Google ADK, Microsoft Agent Framework, and Pydantic AI. It defines an **event stream protocol** between agent backends and frontend applications.

### 5.1 What Problem Does AG-UI Solve

The traditional request/response architecture falls short for agent applications because agents have the following characteristics:
- **Long-running**: Continuously streaming intermediate results across multi-turn conversations
- **Non-deterministic**: Agent behavior is unpredictable, requiring dynamic UI control
- **Mixed I/O**: Simultaneously producing structured data (tool calls, state) and unstructured content (text, voice)
- **Human interaction**: Requiring pause/approval/edit and other human-in-the-loop capabilities

AG-UI defines **16+ event types** that enable the frontend to precisely perceive each step of the agent's behavior.

### 5.2 AG-UI Container Contract in AgentCore

| Specification | Requirement |
|---------------|-------------|
| Listen Address | `0.0.0.0:8080` |
| Platform | ARM64 container |
| Primary Endpoint | `POST /invocations` (SSE event stream) |
| Optional Endpoints | `GET /ws` (WebSocket) |
| Health Check | `GET /ping` |

> AG-UI uses the **same port (8080) and endpoint path (`/invocations`)** as the HTTP protocol. The difference is that the request/response format follows the AG-UI event specification.

### 5.3 Endpoint Details

#### `POST /invocations` — AG-UI Event Stream

**Request Format (`RunAgentInput`):**
```json
{
  "threadId": "thread-123",
  "runId": "run-456",
  "messages": [{"id": "msg-1", "role": "user", "content": "Hello, agent!"}],
  "tools": [],
  "context": [],
  "state": {},
  "forwardedProps": {}
}
```

| Field | Description |
|-------|-------------|
| `threadId` | Conversation thread ID |
| `runId` | Unique ID for this execution |
| `messages` | Message history |
| `tools` | Frontend-registered tools (for frontend tool call scenarios) |
| `context` | Context information |
| `state` | Shared state (supports frontend-backend state synchronization) |
| `forwardedProps` | Pass-through properties |

**Response Format (SSE Event Stream):**
```
Content-Type: text/event-stream

data: {"type":"RUN_STARTED","threadId":"thread-123","runId":"run-456"}
data: {"type":"TEXT_MESSAGE_START","messageId":"msg-789","role":"assistant"}
data: {"type":"TEXT_MESSAGE_CONTENT","messageId":"msg-789","delta":"Processing your request"}
data: {"type":"TOOL_CALL_START","toolCallId":"tool-001","toolCallName":"search","parentMessageId":"msg-789"}
data: {"type":"TOOL_CALL_RESULT","messageId":"msg-789","toolCallId":"tool-001","content":"Search completed"}
data: {"type":"TEXT_MESSAGE_END","messageId":"msg-789"}
data: {"type":"RUN_FINISHED","threadId":"thread-123","runId":"run-456"}
```

### 5.4 AG-UI Event Types

| Event Type | Description |
|------------|-------------|
| `RUN_STARTED` | Agent execution started |
| `TEXT_MESSAGE_START` | Text message stream started |
| `TEXT_MESSAGE_CONTENT` | Incremental text content (delta) |
| `TEXT_MESSAGE_END` | Text message stream ended |
| `TOOL_CALL_START` | Tool invocation started |
| `TOOL_CALL_RESULT` | Tool execution result |
| `RUN_FINISHED` | Agent execution completed |
| `RUN_ERROR` | Execution error |

Errors are returned as SSE events (HTTP status code remains 200):
```
data: {"type":"RUN_ERROR","code":"AGENT_ERROR","message":"Agent execution failed"}
```

### 5.5 Code Example

```python
# my_agui_server.py
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, JSONResponse
# Note: The AG-UI ecosystem is rapidly evolving. The package names and APIs below
# may change with version updates. Please refer to the official documentation at
# ag-ui.com and the latest PyPI versions.
from ag_ui_strands import StrandsAgent
from ag_ui.core import RunAgentInput
from ag_ui.encoder import EventEncoder
from strands import Agent
from strands.models.bedrock import BedrockModel

model = BedrockModel(
    model_id="us.anthropic.claude-sonnet-4-5-20250929-v1:0",
    region_name="us-west-2",
)

strands_agent = Agent(
    model=model,
    system_prompt="You are a helpful assistant.",
)

agui_agent = StrandsAgent(
    agent=strands_agent,
    name="my_agent",
    description="A helpful assistant",
)

app = FastAPI()

@app.post("/invocations")
async def invocations(input_data: dict, request: Request):
    accept_header = request.headers.get("accept")
    encoder = EventEncoder(accept=accept_header)

    async def event_generator():
        run_input = RunAgentInput(**input_data)
        async for event in agui_agent.run(run_input):
            yield encoder.encode(event)

    return StreamingResponse(
        event_generator(),
        media_type=encoder.get_content_type()
    )

@app.get("/ping")
async def ping():
    return JSONResponse({"status": "Healthy"})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
```

**Deployment:**
```bash
pip install fastapi uvicorn ag-ui-strands
agentcore configure -e my_agui_server.py --protocol AGUI
agentcore deploy
```

### 5.6 Integration with CopilotKit

AG-UI natively supports [CopilotKit](https://docs.copilotkit.ai/). The frontend can use CopilotKit's React components to directly interface with an AG-UI backend:

```
React Frontend (CopilotKit Components)
  <-> AG-UI Event Stream
AgentCore Runtime (AG-UI Protocol)
  <-> LLM Invocation
Bedrock / OpenAI / ...
```

Advanced UI capabilities supported by AG-UI include: streaming chat, generative UI, shared state synchronization, thinking steps visualization, human-in-the-loop interruption, sub-agent composition, and more.

### 5.7 Applicable Scenarios

- Building rich agent UI applications (chat, collaborative editing, approval workflows)
- Frontend needs to precisely perceive each step of the agent's behavior (tool calls, thinking process)
- Using frontend frameworks such as CopilotKit
- Requiring human-in-the-loop interaction (pause, approval, edit)
- Requiring frontend-backend state synchronization

---

## 6. Comparison of the Four Protocols

| Dimension | HTTP | MCP | A2A | AG-UI |
|-----------|------|-----|-----|-------|
| **Container Port** | 8080 | 8000 | 9000 | 8080 |
| **Primary Endpoint** | `/invocations` | `/mcp` | `/` | `/invocations` |
| **Message Format** | Application-defined | JSON-RPC 2.0 | JSON-RPC 2.0 | RunAgentInput + SSE events |
| **Communication Mode** | JSON / SSE / WebSocket | JSON-RPC (Streamable HTTP) | JSON-RPC / SSE / Async push | SSE event stream / WebSocket |
| **Discovery Mechanism** | None | `tools/list` (MCP primitives) | Agent Card (`/.well-known/agent-card.json`) | None |
| **Interaction Target** | Human -> Agent | AI App -> Tools/Data | Agent -> Agent | Agent -> Frontend UI |
| **Request Body Format** | Fully custom | Standard MCP RPC | Standard A2A RPC | AG-UI RunAgentInput |
| **Event Types** | Custom | MCP standard | A2A standard | 16+ AG-UI events |
| **Clients/Frameworks** | Any | MCP clients: Claude, ChatGPT, VS Code, Cursor, etc. | Agent frameworks: Strands, LangGraph, CrewAI, etc. | Frontend frameworks: CopilotKit; Agent frameworks: Strands, LangGraph, CrewAI, etc. |
| **Protocol Origin** | — | Anthropic | Google (Linux Foundation) | CopilotKit + LangGraph + CrewAI |

### Complementary Relationship of the Three Protocols

The AG-UI official documentation explicitly defines the complementary positioning of the three protocols:

```
                    MCP
              Agent <-> Tools/Data
                 |
    +------------+------------+
    |            |            |
   A2A        Agent        AG-UI
Agent <-> Agent  |   Agent <-> Frontend UI
                 |
            User/System
```

- **MCP**: The **downward** connection for agents to access tools and data
- **A2A**: **Horizontal** collaboration between agents
- **AG-UI**: The **upward** interaction between agents and frontend UI

All three can coexist in the same system: an agent accesses tools via MCP, collaborates with other agents via A2A, and interacts with the user frontend via AG-UI.

---

## 7. How to Choose a Protocol

```
What are you building?
  |
  |-- Custom agent app, need full control over format
  |   +-- HTTP
  |
  |-- Tool/data service, to be called by multiple AI clients
  |   +-- MCP
  |
  |-- Multi-agent collaboration system
  |   +-- A2A
  |
  +-- Agent-driven frontend UI application
      +-- AG-UI
```

**Practical Considerations:**

| Scenario | Recommended Protocol | Rationale |
|----------|---------------------|-----------|
| Strands/LangGraph Agent + custom frontend | HTTP | Most flexible, format freedom |
| Already have an MCP Server, need cloud hosting | MCP | Native compatibility |
| Building a tool service for Claude/ChatGPT | MCP | Standard protocol, widely supported |
| Multiple specialized agents collaborating on complex tasks | A2A | Standard inter-agent communication |
| Building AI collaborative apps with CopilotKit | AG-UI | Native event protocol |
| Simple chatbot | HTTP | Simplest and most straightforward |

> **Typical choice**: If your agent directly faces frontend users, needs fully custom request/response formats, and uses Strands Agents or LangGraph + FastAPI, HTTP is the most natural choice.

---

## 8. Authentication: Common to All Protocols

Regardless of which protocol is chosen, AgentCore supports the same authentication methods:

**OAuth 2.0 Bearer Token:**
```
Authorization: Bearer <jwt-token>
X-Amzn-Bedrock-AgentCore-Runtime-Session-Id: <session-id>
```

Unauthenticated requests return 401:
```
HTTP/1.1 401 Unauthorized
WWW-Authenticate: Bearer resource_metadata="https://bedrock-agentcore.{region}.amazonaws.com/runtimes/{ESCAPED_ARN}/invocations/.well-known/oauth-protected-resource?qualifier={QUALIFIER}"
```

Clients can discover OAuth endpoints via the `resource_metadata` URL for automatic token retrieval.

**SigV4 Signature Authentication:**
- Returns HTTP 403 (not 401)
- Does not include `WWW-Authenticate` header
- Invoked via `boto3.client('bedrock-agentcore').invoke_agent_runtime()`

> **Note**: OAuth and SigV4 are mutually exclusive; they cannot be used together. After enabling OAuth, you cannot use the boto3 SDK (SigV4) to invoke; you must send HTTPS requests directly with a Bearer Token.

---

*This document is based on AWS official documentation (AgentCore Runtime Protocol Contracts), MCP official documentation (modelcontextprotocol.io), A2A official documentation (Google/A2A), and AG-UI official documentation (ag-ui.com). Protocol versions: MCP 2025-06-18, A2A 0.3.0.*

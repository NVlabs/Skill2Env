---
name: voltagent-core-reference
# prettier-ignore
description: Reference for the VoltAgent class: constructor options, lifecycle methods, and runtime behavior.
license: MIT
metadata:
  author: VoltAgent
  version: "1.0.0"
  repository: https://github.com/VoltAgent/skills
---

# VoltAgent Core Reference

Reference for the VoltAgent class in `@voltagent/core`.

Source files:
- packages/core/src/voltagent.ts
- packages/core/src/types.ts

---

## Options Overview

`VoltAgentOptions` supports:

- `agents`: Record of `Agent` instances to register.
- `workflows`: Record of `Workflow` or `WorkflowChain` instances.
- `memory`: Default `Memory` used for agents and workflows.
- `agentMemory`: Default `Memory` for agents (falls back to `memory`).
- `workflowMemory`: Default `Memory` for workflows (falls back to `memory`).
- `toolRouting`: Global `ToolRoutingConfig` defaults.
- `triggers`: `VoltAgentTriggersConfig` handlers.
- `server`: Server provider factory (for example `honoServer()`).
- `serverless`: Serverless provider factory for fetch runtimes.
- `voltOpsClient`: Shared `VoltOpsClient` instance.
- `observability`: `VoltAgentObservability` instance.
- `logger`: Shared `Logger` instance.
- `mcpServers`: Record of MCP servers or factories.
- `a2aServers`: Record of A2A servers or factories.
- `checkDependencies`: Set to `false` to skip dependency checks.

Deprecated options:
- `port`
- `autoStart`
- `customEndpoints`
- `enableSwaggerUI`

---

## Lifecycle Notes

- Registers agents and workflows on construction.
- Auto-starts the server if a server provider is supplied.
- Applies default memory to agents and workflows.
- Auto-configures VoltOps client from `VOLTAGENT_PUBLIC_KEY` and `VOLTAGENT_SECRET_KEY` if not provided.
- Initializes MCP and A2A servers and starts MCP transports after server start.

---

## Methods

- `registerAgent(agent)`, `registerAgents(agents)`
- `registerWorkflow(workflow)`, `registerWorkflows(workflows)`
- `registerTrigger(name, config)`, `registerTriggers(triggers)`
- `getAgent(id)`, `getAgents()`, `getAgentCount()`
- `getWorkflow(id)`, `getWorkflows()`, `getWorkflowCount()`
- `getObservability()`
- `startServer()`, `stopServer()`, `getServerInstance()`
- `serverless()` to access the serverless provider
- `shutdown()` for graceful shutdown, `shutdownTelemetry()` for observability

---

## Example

```typescript
import { VoltAgent } from "@voltagent/core";
import { honoServer } from "@voltagent/server-hono";

const app = new VoltAgent({
  agents: { agent },
  workflows: { workflow },
  server: honoServer(),
});

await app.startServer();
```

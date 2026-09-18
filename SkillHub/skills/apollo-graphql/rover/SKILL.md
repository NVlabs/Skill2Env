---
name: rover
description: >
  Guide for using Apollo Rover CLI to manage GraphQL schemas and federation. Use this skill when:
  (1) publishing or fetching subgraph/graph schemas,
  (2) composing supergraph schemas locally or via GraphOS,
  (3) running local supergraph development with rover dev,
  (4) validating schemas with check and lint commands,
  (5) configuring Rover authentication and environment,
  (6) exploring or searching a graph's schema for agent-driven discovery (rover schema describe / rover schema search).
license: MIT
compatibility: Node.js v18+, Linux/macOS/Windows
metadata:
  author: apollographql
  version: "1.1.1"
allowed-tools: Bash(rover:*) Bash(npm:*) Bash(npx:*) Read Write Edit Glob Grep
---

# Apollo Rover CLI Guide

Rover is the official CLI for Apollo GraphOS. It helps you manage schemas, run composition locally, publish to GraphOS, and develop supergraphs on your local machine.

## Quick Start

### Step 1: Install

```bash
# macOS/Linux
curl -sSL https://rover.apollo.dev/nix/latest | sh

# npm (cross-platform)
npm install -g @apollo/rover

# Windows PowerShell
iwr 'https://rover.apollo.dev/win/latest' | iex
```

### Step 2: Authenticate

```bash
# Interactive authentication (opens browser)
rover config auth

# Or set environment variable
export APOLLO_KEY=your-api-key
```

### Step 3: Verify Installation

```bash
rover --version
rover config whoami
```

## Explore a Graph's Schema (start here for schema questions)

To answer "what's in this graph?", find a field, or write a query against a GraphOS graph, **fetch the API schema and pipe it into `rover schema`** — this keeps the SDL out of your context and returns only what you need:

```bash
# What can I query? (compact overview)
rover graph fetch <graph@variant> | rover schema describe -

# Find a field by concept/keyword (returns the path from a root operation)
rover graph fetch <graph@variant> | rover schema search - "<keyword>"

# Zoom into one type or field
rover graph fetch <graph@variant> | rover schema describe - --coord <Type.field> --depth 1
```

Three rules that keep this correct:

- Use **`rover graph fetch`** (the API schema) — **not** `rover supergraph fetch` (that returns composition SDL with federation internals like `join__`/`link__`).
- **Pipe** it in — never run `rover graph fetch` alone and read the raw SDL (a large schema floods your context; that's exactly what `rover schema` avoids).
- The `schema` commands read **piped SDL, not a graph ref** — `rover schema describe <graph@variant>` fails; you must fetch first and pipe.

Full reference, ranking rules, and the save-once pattern: [Schema Exploration](#schema-exploration-for-agents) and [references/schema.md](references/schema.md).

## Core Commands Overview

| Command | Description | Use Case |
|---------|-------------|----------|
| `rover subgraph publish` | Publish subgraph schema to GraphOS | CI/CD, schema updates |
| `rover subgraph check` | Validate schema changes | PR checks, pre-deploy |
| `rover subgraph fetch` | Download subgraph schema | Local development |
| `rover supergraph compose` | Compose supergraph locally | Local testing |
| `rover dev` | Local supergraph development | Development workflow |
| `rover graph publish` | Publish monograph schema | Non-federated graphs |
| `rover schema describe` | Explore a schema by coordinate; **takes SDL via stdin/file, not a graph ref** — pipe from `rover graph fetch` | Agent schema discovery |
| `rover schema search` | Search a schema by keyword; **takes SDL via stdin/file, not a graph ref** — pipe from `rover graph fetch` | Agent schema discovery |

## Graph Reference Format

Most commands require a graph reference in the format:

```
<GRAPH_ID>@<VARIANT>
```

Examples:
- `my-graph@production`
- `my-graph@staging`
- `my-graph@current` (default variant)

Set as environment variable:
```bash
export APOLLO_GRAPH_REF=my-graph@production
```

## Subgraph Workflow

### Publishing a Subgraph

```bash
# From schema file
rover subgraph publish my-graph@production \
  --name products \
  --schema ./schema.graphql \
  --routing-url https://products.example.com/graphql

# From running server (introspection)
rover subgraph publish my-graph@production \
  --name products \
  --schema <(rover subgraph introspect http://localhost:4001/graphql) \
  --routing-url https://products.example.com/graphql
```

### Checking Schema Changes

```bash
# Check against production traffic
rover subgraph check my-graph@production \
  --name products \
  --schema ./schema.graphql
```

### Fetching Schema

```bash
# Fetch from GraphOS
rover subgraph fetch my-graph@production --name products

# Introspect running server
rover subgraph introspect http://localhost:4001/graphql
```

## Supergraph Composition

### Local Composition

Create `supergraph.yaml`:

```yaml
federation_version: =2.9.0
subgraphs:
  products:
    routing_url: http://localhost:4001/graphql
    schema:
      file: ./products/schema.graphql
  reviews:
    routing_url: http://localhost:4002/graphql
    schema:
      subgraph_url: http://localhost:4002/graphql
```

Compose:
```bash
rover supergraph compose --config supergraph.yaml > supergraph.graphql
```

### Fetch Composed Supergraph

```bash
rover supergraph fetch my-graph@production
```

> This returns the **supergraph SDL** (federation directives + `join__`/`link__` internals) — use it for composition/router work. To **explore what you can query** or write an operation, use `rover graph fetch` (the API schema) instead — see [Explore a Graph's Schema](#explore-a-graphs-schema-start-here-for-schema-questions).

## Local Development with `rover dev`

Start a local Router with automatic schema composition:

```bash
# Start with supergraph config
rover dev --supergraph-config supergraph.yaml

# Start with GraphOS variant as base
rover dev --graph-ref my-graph@staging --supergraph-config local.yaml
```

### With MCP Integration

```bash
# Start with MCP server enabled
rover dev --supergraph-config supergraph.yaml --mcp
```

## Schema Exploration (for Agents)

`rover schema describe` and `rover schema search` let an agent explore a schema **without loading the full SDL into context** — that is the entire point of these commands.

> ⚠️ **Never read the raw SDL into context.** Running `rover graph fetch <ref>` (or `rover graph introspect <url>`) on its own prints the entire schema — hundreds to tens of thousands of lines — straight into your context, which defeats the purpose of these commands. **Always pipe fetch output into `rover schema describe`/`search`**: the SDL flows through stdin and only the compact overview/results reach you. (Fetching to a file is fine when the user actually wants the SDL.)
>
> These commands also take SDL on **stdin or a file, NOT a graph ref** — you can't pass `graph@variant` to them. Fetch first, then pipe:
>
> ```bash
> ❌ rover schema describe my-graph@current             # error: looks for a file named that
> ❌ rover graph fetch my-graph@current                 # dumps the full SDL into your context
> ✅ rover graph fetch my-graph@current | rover schema describe -
> ```

To explore a graph in GraphOS, fetch its schema and pipe it in. **Use `rover graph fetch` (the API schema) for "what can I query?" exploration** — it omits federation internals. Reach for `rover supergraph fetch` only when you need composition details (`join__`/`link__` types, subgraph structure):

```bash
# Overview of a GraphOS graph
rover graph fetch my-graph@current | rover schema describe -

# Find fields by keyword (results include paths from root operations)
rover graph fetch my-graph@current | rover schema search - "playback"

# Zoom into a coordinate, expanding referenced types one level
rover graph fetch my-graph@current | rover schema describe - --coord <Type.field> --depth 1
```

**Coordinate forms:** `--coord` accepts a type (`User`), a field (`User.posts`), a field argument (`Type.field(arg:)`), or a directive (`@deprecated`) — omit it for the overview.

**`search` vs `describe`:** reach for `rover schema search` first when matching a concept or keyword and you don't yet know the field name — it finds **nested** fields and shows the path from a root operation. The `describe` overview lists only root fields, so `search` is how you locate fields buried deeper. Use `describe` for the overview or once you know the type/field coordinate.

This enables a closed-loop workflow — search → describe → write a query — with no MCP server setup. See [Schema Exploration](references/schema.md) for the full command reference, ranking rules, and the save-once pattern for large schemas.

**Running the generated operation:** Rover does **not** execute queries — it only manages and inspects schemas. To actually run a generated query you need the graph's endpoint:

- **Single-subgraph graph:** `rover subgraph list <graph@variant>` prints the **Routing Url** — send the query there with `curl`.
- **Multi-subgraph / federated:** the client endpoint is the **router** URL (find it in GraphOS Studio; for a GraphOS cloud router, `rover cloud config fetch <graph@variant>`), not the per-subgraph routing URLs.
- Don't try to discover the endpoint via the GraphOS Platform API — Rover keeps the API key in its profile/keychain, not `$APOLLO_KEY`, so ad-hoc API calls will come back unauthenticated.

## Reference Files

Detailed documentation for specific topics:

- [Subgraphs](references/subgraphs.md) - fetch, publish, check, lint, introspect, delete
- [Graphs](references/graphs.md) - monograph commands (non-federated)
- [Supergraphs](references/supergraphs.md) - compose, fetch, config format
- [Dev](references/dev.md) - rover dev for local development
- [Schema Exploration](references/schema.md) - describe, search, agent schema discovery workflows
- [Configuration](references/configuration.md) - install, auth, env vars, profiles

## Common Patterns

### CI/CD Pipeline

```bash
# 1. Check schema changes
rover subgraph check $APOLLO_GRAPH_REF \
  --name $SUBGRAPH_NAME \
  --schema ./schema.graphql

# 2. If check passes, publish
rover subgraph publish $APOLLO_GRAPH_REF \
  --name $SUBGRAPH_NAME \
  --schema ./schema.graphql \
  --routing-url $ROUTING_URL
```

### Schema Linting

```bash
# Lint against GraphOS rules
rover subgraph lint --name products ./schema.graphql

# Lint monograph
rover graph lint my-graph@production ./schema.graphql
```

### Output Formats

```bash
# JSON output for scripting
rover subgraph fetch my-graph@production --name products --format json

# Plain output (default)
rover subgraph fetch my-graph@production --name products --format plain
```

## Ground Rules

- ALWAYS authenticate before using GraphOS commands (`rover config auth` or `APOLLO_KEY`)
- ALWAYS use the correct graph reference format: `graph@variant`
- PREFER `rover subgraph check` before `rover subgraph publish` in CI/CD
- USE `rover dev` for local supergraph development instead of running Router manually
- NEVER commit `APOLLO_KEY` to version control; use environment variables
- USE `--format json` when parsing output programmatically
- SPECIFY `federation_version` explicitly in supergraph.yaml for reproducibility
- USE `rover subgraph introspect` to extract schemas from running services
- USE `rover schema search` / `rover schema describe` (piped from a `fetch`) to explore large schemas instead of loading the full SDL into context
- NEVER fetch a full schema into context just to explore it — pipe `rover graph fetch`/`introspect` into `rover schema describe`/`search` (a bare `fetch` is only for when the user wants the SDL file itself)

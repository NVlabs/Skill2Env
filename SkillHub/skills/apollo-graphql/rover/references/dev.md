# Rover Dev Command

Run a local supergraph for development with automatic schema composition and hot reloading.

## Basic Usage

```bash
# Start with supergraph config
rover dev --supergraph-config supergraph.yaml

# Start on specific port
rover dev --supergraph-config supergraph.yaml --router-port 4000
```

**Default behavior:**
- Router runs on `http://localhost:4000`
- GraphQL endpoint: `http://localhost:4000`
- Health check: `http://localhost:4000/health`

## Configuration File

Create `supergraph.yaml` for local development:

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

  users:
    routing_url: http://localhost:4003/graphql
    schema:
      file: ./users/schema.graphql
```

## Hot Reloading

### File-based Schema

When using `schema.file`, Rover watches for file changes:

```yaml
subgraphs:
  products:
    schema:
      file: ./products/schema.graphql  # Watched for changes
```

Save the file and Rover automatically recomposes.

### Introspection-based Schema

When using `schema.subgraph_url`, Rover polls for changes:

```yaml
subgraphs:
  reviews:
    schema:
      subgraph_url: http://localhost:4002/graphql  # Polled for changes
```

## Using with GraphOS Variant

Start with a GraphOS variant as baseline and override locally:

```bash
rover dev --graph-ref my-graph@staging --supergraph-config local-overrides.yaml
```

**local-overrides.yaml:**
```yaml
federation_version: =2.9.0

subgraphs:
  # Override products with local version
  products:
    routing_url: http://localhost:4001/graphql
    schema:
      file: ./products/schema.graphql
  # Other subgraphs come from GraphOS variant
```

## Router Configuration

### Custom Router Config

```bash
rover dev \
  --supergraph-config supergraph.yaml \
  --router-config router.yaml
```

**router.yaml:**
```yaml
supergraph:
  listen: 127.0.0.1:4000

headers:
  all:
    request:
      - propagate:
          matching: "^x-.*"

cors:
  origins:
    - http://localhost:3000
  allow_headers:
    - Content-Type
    - Authorization

telemetry:
  apollo:
    endpoint: https://usage.api.apollographql.com/api/ingress/traces
```

### Common Router Options

```yaml
# Sandbox enabled (default in dev)
sandbox:
  enabled: true

# Introspection enabled (default in dev)
introspection: true

# Query plans in response
include_subgraph_errors:
  all: true
```

## MCP Server Integration

Enable MCP server alongside Router:

```bash
rover dev --supergraph-config supergraph.yaml --mcp
```

**MCP options:**
```bash
# Specify MCP port
rover dev --supergraph-config supergraph.yaml --mcp --mcp-port 5001

# MCP output format
rover dev --supergraph-config supergraph.yaml --mcp --mcp-format json
```

**Use cases:**
- AI agent integration during development
- Testing MCP-based tools
- Local agentic workflow development

## Multiple Subgraph Development

### Single Machine Setup

```bash
# Terminal 1: Products subgraph
cd products && npm run dev  # Runs on 4001

# Terminal 2: Reviews subgraph
cd reviews && npm run dev   # Runs on 4002

# Terminal 3: Rover dev
rover dev --supergraph-config supergraph.yaml
```

### Adding a New Subgraph

1. Add to `supergraph.yaml`:
```yaml
subgraphs:
  # existing...

  new-service:
    routing_url: http://localhost:4004/graphql
    schema:
      file: ./new-service/schema.graphql
```

2. Rover automatically detects changes and recomposes.

## Options Reference

| Option | Description | Default |
|--------|-------------|---------|
| `--supergraph-config <PATH>` | Path to supergraph config | Required |
| `--graph-ref <REF>` | GraphOS variant for baseline | None |
| `--router-port <PORT>` | Router listen port | 4000 |
| `--router-config <PATH>` | Custom Router config | None |
| `--mcp` | Enable MCP server | false |
| `--mcp-port <PORT>` | MCP server port | 5001 |
| `--log <LEVEL>` | Log level | info |

## Troubleshooting

### Port Already in Use

```bash
# Check what's using port 4000
lsof -i :4000

# Use different port
rover dev --supergraph-config supergraph.yaml --router-port 4001
```

### Subgraph Not Reachable

```
Error: Could not connect to subgraph "products" at http://localhost:4001/graphql
```

- Ensure subgraph server is running
- Check correct port in config
- Verify subgraph URL responds to introspection

### Composition Fails

```bash
# Check composition separately
rover supergraph compose --config supergraph.yaml

# Look for specific errors in output
```

### Schema Not Updating

For file-based schemas:
- Ensure file path is correct
- Check file permissions
- Try saving file again

For introspection:
- Ensure server has introspection enabled
- Check for authentication requirements

## Environment Variables

```bash
# Required for GraphOS features
export APOLLO_KEY=your-api-key
export APOLLO_GRAPH_REF=my-graph@staging

# Run with environment
APOLLO_KEY=$APOLLO_KEY rover dev \
  --graph-ref $APOLLO_GRAPH_REF \
  --supergraph-config local.yaml
```

## Development Workflow

### Typical Session

```bash
# 1. Start subgraph servers
npm run dev:subgraphs  # Custom script to start all

# 2. Start Rover dev
rover dev --supergraph-config supergraph.yaml

# 3. Open http://localhost:4000 for Sandbox
# 4. Make schema changes - auto-reloads
# 5. Ctrl+C to stop
```

### With Docker Compose

```yaml
# docker-compose.yaml
services:
  products:
    build: ./products
    ports:
      - "4001:4001"

  reviews:
    build: ./reviews
    ports:
      - "4002:4002"
```

```bash
# Start services
docker-compose up -d

# Start Rover dev
rover dev --supergraph-config supergraph.yaml
```

# Rover Graph Commands

Commands for managing monograph (non-federated) schemas in Apollo GraphOS.

> **Note:** Use `rover subgraph` commands for federated graphs. These `rover graph` commands are for standalone GraphQL APIs without federation.

## graph fetch

Download a graph schema from GraphOS.

```bash
# Basic fetch
rover graph fetch my-graph@production

# Output to file
rover graph fetch my-graph@production > schema.graphql

# JSON output
rover graph fetch my-graph@production --format json
```

**Options:**
| Option | Description |
|--------|-------------|
| `--format <FORMAT>` | Output format: `plain` (default) or `json` |

## graph introspect

Extract schema from a running GraphQL server.

```bash
# Basic introspection
rover graph introspect http://localhost:4000/graphql

# With authentication header
rover graph introspect http://localhost:4000/graphql \
  --header "Authorization: Bearer token123"

# Multiple headers
rover graph introspect http://localhost:4000/graphql \
  --header "Authorization: Bearer token" \
  --header "X-Tenant-ID: acme"

# Watch mode
rover graph introspect http://localhost:4000/graphql --watch
```

**Options:**
| Option | Description |
|--------|-------------|
| `--header <HEADER>` | HTTP header(s) to include |
| `--watch` | Poll endpoint and output changes |
| `--polling-interval <SECONDS>` | Interval for watch mode (default: 1) |

## graph publish

Publish a monograph schema to GraphOS.

```bash
# From file
rover graph publish my-graph@production \
  --schema ./schema.graphql

# From stdin
cat schema.graphql | rover graph publish my-graph@production --schema -

# From introspection
rover graph publish my-graph@production \
  --schema <(rover graph introspect http://localhost:4000/graphql)
```

**Options:**
| Option | Description |
|--------|-------------|
| `--schema <PATH>` | Schema file path or `-` for stdin (required) |

## graph check

Validate schema changes against GraphOS.

```bash
# Basic check
rover graph check my-graph@production \
  --schema ./schema.graphql

# With validation thresholds
rover graph check my-graph@production \
  --schema ./schema.graphql \
  --query-count-threshold 100 \
  --query-count-threshold-percentage 3
```

**Check validates:**
1. **Schema validity** - Schema is syntactically correct
2. **Operations** - Existing client operations still work
3. **Linting** - Schema follows GraphOS linting rules

**Options:**
| Option | Description |
|--------|-------------|
| `--schema <PATH>` | Schema file path (required) |
| `--query-count-threshold <N>` | Min operations for breaking change |
| `--query-count-threshold-percentage <N>` | Min % of operations |
| `--background` | Run check in background |

**Exit codes:**
- `0` - Check passed
- `1` - Check failed
- `2` - Check completed with warnings

## graph lint

Run GraphOS linting rules against a schema.

```bash
# Lint local schema (uses graph for rule configuration)
rover graph lint my-graph@production --schema ./schema.graphql

# Lint without graph reference
rover graph lint --schema ./schema.graphql
```

## graph delete

Delete a graph variant from GraphOS.

```bash
# Delete with confirmation
rover graph delete my-graph@staging

# Delete without confirmation
rover graph delete my-graph@staging --confirm
```

**Warning:** This deletes the entire variant, not just the schema.

**Options:**
| Option | Description |
|--------|-------------|
| `--confirm` | Skip confirmation prompt |

## Differences from Subgraph Commands

| Aspect | `rover graph` | `rover subgraph` |
|--------|---------------|------------------|
| Use case | Monographs | Federated subgraphs |
| Routing URL | Not required | Required for Router |
| Composition | N/A | Composes with other subgraphs |
| `--name` flag | Not used | Required |

## Migration to Federation

If migrating from a monograph to federation:

```bash
# 1. Fetch existing monograph schema
rover graph fetch my-graph@production > schema.graphql

# 2. Add federation directives to schema
# (edit schema.graphql to add @key, extend Query, etc.)

# 3. Publish as first subgraph
rover subgraph publish my-graph@production \
  --name monolith \
  --schema ./schema.graphql \
  --routing-url https://api.example.com/graphql
```

## CI/CD Example

```bash
#!/bin/bash
set -e

GRAPH_REF="${APOLLO_GRAPH_REF:-my-graph@production}"
SCHEMA_PATH="./schema.graphql"

# Check schema changes
echo "Checking schema..."
rover graph check "$GRAPH_REF" --schema "$SCHEMA_PATH"

# Publish if check passes
echo "Publishing schema..."
rover graph publish "$GRAPH_REF" --schema "$SCHEMA_PATH"

echo "Schema published successfully!"
```

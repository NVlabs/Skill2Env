# Rover Subgraph Commands

Commands for managing federated subgraph schemas in Apollo GraphOS.

## subgraph fetch

Download a subgraph schema from GraphOS.

```bash
# Basic fetch
rover subgraph fetch my-graph@production --name products

# Output to file
rover subgraph fetch my-graph@production --name products > products.graphql

# JSON output
rover subgraph fetch my-graph@production --name products --format json
```

**Options:**
| Option | Description |
|--------|-------------|
| `--name <NAME>` | Subgraph name (required) |
| `--format <FORMAT>` | Output format: `plain` (default) or `json` |

## subgraph introspect

Extract schema from a running GraphQL server via introspection.

```bash
# Basic introspection
rover subgraph introspect http://localhost:4001/graphql

# With headers
rover subgraph introspect http://localhost:4001/graphql \
  --header "Authorization: Bearer token123"

# Multiple headers
rover subgraph introspect http://localhost:4001/graphql \
  --header "Authorization: Bearer token" \
  --header "X-Custom-Header: value"

# Watch mode (poll for changes)
rover subgraph introspect http://localhost:4001/graphql --watch
```

**Options:**
| Option | Description |
|--------|-------------|
| `--header <HEADER>` | HTTP header(s) to include |
| `--watch` | Poll endpoint and output changes |
| `--polling-interval <SECONDS>` | Interval for watch mode (default: 1) |

## subgraph list

List all subgraphs in a graph variant.

```bash
rover subgraph list my-graph@production
```

**Output includes:**
- Subgraph name
- Routing URL
- Last updated timestamp

## subgraph publish

Publish a subgraph schema to GraphOS.

```bash
# From file
rover subgraph publish my-graph@production \
  --name products \
  --schema ./products.graphql \
  --routing-url https://products.example.com/graphql

# From stdin (introspection)
rover subgraph introspect http://localhost:4001/graphql | \
  rover subgraph publish my-graph@production \
    --name products \
    --schema - \
    --routing-url https://products.example.com/graphql

# Process substitution
rover subgraph publish my-graph@production \
  --name products \
  --schema <(rover subgraph introspect http://localhost:4001/graphql) \
  --routing-url https://products.example.com/graphql
```

**Options:**
| Option | Description |
|--------|-------------|
| `--name <NAME>` | Subgraph name (required) |
| `--schema <PATH>` | Schema file path or `-` for stdin (required) |
| `--routing-url <URL>` | URL where Router sends requests |
| `--allow-invalid-routing-url` | Allow non-HTTPS or non-standard URLs |
| `--no-url` | Skip URL update (schema only) |

**Routing URL:**
- Required on first publish
- Optional on subsequent publishes (uses existing if not provided)
- Must be reachable by the Router in production

## subgraph check

Validate schema changes against GraphOS.

```bash
# Basic check
rover subgraph check my-graph@production \
  --name products \
  --schema ./products.graphql

# Check with specific validation period
rover subgraph check my-graph@production \
  --name products \
  --schema ./products.graphql \
  --query-count-threshold 1000 \
  --query-count-threshold-percentage 5
```

**Check validates:**
1. **Composition** - Schema composes successfully with other subgraphs
2. **Operations** - Existing client operations still work
3. **Linting** - Schema follows GraphOS linting rules

**Options:**
| Option | Description |
|--------|-------------|
| `--name <NAME>` | Subgraph name (required) |
| `--schema <PATH>` | Schema file path (required) |
| `--query-count-threshold <N>` | Min operations for breaking change |
| `--query-count-threshold-percentage <N>` | Min % of operations |
| `--background` | Run check in background (returns check ID) |

**Exit codes:**
- `0` - Check passed
- `1` - Check failed (breaking changes or errors)
- `2` - Check completed with warnings

## subgraph lint

Run GraphOS linting rules against a schema.

```bash
# Lint local schema
rover subgraph lint --name products ./products.graphql

# Lint with specific graph for rules
rover subgraph lint my-graph@production --name products ./products.graphql
```

**Common lint rules:**
- Field naming conventions
- Description requirements
- Deprecation format
- Federation directive usage

## subgraph delete

Remove a subgraph from a graph variant.

```bash
# Delete with confirmation prompt
rover subgraph delete my-graph@production --name products

# Delete without confirmation
rover subgraph delete my-graph@production --name products --confirm
```

**Warning:** Deleting a subgraph:
- Removes it from composition
- May break client operations that use its types
- Cannot be undone (must republish)

**Options:**
| Option | Description |
|--------|-------------|
| `--name <NAME>` | Subgraph name (required) |
| `--confirm` | Skip confirmation prompt |

## Introspection Headers

For authenticated endpoints:

```bash
# Bearer token
rover subgraph introspect http://localhost:4001/graphql \
  --header "Authorization: Bearer $(cat token.txt)"

# API key
rover subgraph introspect http://localhost:4001/graphql \
  --header "x-api-key: my-api-key"

# From environment variable
rover subgraph introspect http://localhost:4001/graphql \
  --header "Authorization: Bearer $AUTH_TOKEN"
```

## Combining Commands

### Publish from running server

```bash
rover subgraph publish my-graph@production \
  --name products \
  --schema <(rover subgraph introspect http://localhost:4001/graphql) \
  --routing-url https://products.example.com/graphql
```

### Check then publish

```bash
# In CI/CD pipeline
rover subgraph check my-graph@production \
  --name products \
  --schema ./products.graphql && \
rover subgraph publish my-graph@production \
  --name products \
  --schema ./products.graphql \
  --routing-url https://products.example.com/graphql
```

### Fetch all subgraphs

```bash
# List and fetch each
for name in $(rover subgraph list my-graph@production --format json | jq -r '.data.subgraphs[].name'); do
  rover subgraph fetch my-graph@production --name "$name" > "$name.graphql"
done
```

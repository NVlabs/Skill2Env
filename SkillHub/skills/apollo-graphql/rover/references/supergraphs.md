# Rover Supergraph Commands

Commands for composing and fetching federated supergraph schemas.

## supergraph fetch

Download the composed supergraph schema from GraphOS.

```bash
# Basic fetch
rover supergraph fetch my-graph@production

# Output to file
rover supergraph fetch my-graph@production > supergraph.graphql

# JSON output (includes build info)
rover supergraph fetch my-graph@production --format json
```

**Options:**
| Option | Description |
|--------|-------------|
| `--format <FORMAT>` | Output format: `plain` (default) or `json` |

**Output:** The full supergraph SDL including:
- All subgraph types merged
- Federation metadata (`_service`, `_entities`)
- Join directives for Router

## supergraph compose

Compose a supergraph schema locally from subgraph schemas.

```bash
# Basic composition
rover supergraph compose --config supergraph.yaml

# Output to file
rover supergraph compose --config supergraph.yaml > supergraph.graphql

# Specify output file
rover supergraph compose --config supergraph.yaml --output supergraph.graphql
```

**Options:**
| Option | Description |
|--------|-------------|
| `--config <PATH>` | Path to supergraph config file (required) |
| `--output <PATH>` | Write output to file |
| `--format <FORMAT>` | Output format: `plain` (default) or `json` |

## Supergraph Configuration File

The `supergraph.yaml` file defines subgraphs for local composition.

### Basic Structure

```yaml
federation_version: =2.9.0

subgraphs:
  products:
    routing_url: http://localhost:4001/graphql
    schema:
      file: ./subgraphs/products/schema.graphql

  reviews:
    routing_url: http://localhost:4002/graphql
    schema:
      file: ./subgraphs/reviews/schema.graphql

  users:
    routing_url: http://localhost:4003/graphql
    schema:
      subgraph_url: http://localhost:4003/graphql
```

### Schema Sources

#### From File

```yaml
subgraphs:
  products:
    routing_url: http://localhost:4001/graphql
    schema:
      file: ./products.graphql
```

#### From Introspection

```yaml
subgraphs:
  products:
    routing_url: http://localhost:4001/graphql
    schema:
      subgraph_url: http://localhost:4001/graphql
```

#### From Introspection with Headers

```yaml
subgraphs:
  products:
    routing_url: http://localhost:4001/graphql
    schema:
      subgraph_url: http://localhost:4001/graphql
      introspection_headers:
        Authorization: Bearer ${AUTH_TOKEN}
        X-Custom-Header: value
```

#### From GraphOS

```yaml
subgraphs:
  products:
    routing_url: http://localhost:4001/graphql
    schema:
      graphref: my-graph@production
      subgraph: products
```

### Federation Version

```yaml
# Exact version (recommended for reproducibility)
federation_version: =2.9.0

# Minimum version
federation_version: 2.9.0

# Latest 2.x
federation_version: 2
```

**Supported versions:**
- `2.9.x` - Latest with `@cost` directive
- `2.8.x` - Stable with `@context`
- `2.7.x` - `@authenticated`, `@requiresScopes`
- `1.x` - Legacy (not recommended)

### Complete Example

```yaml
federation_version: =2.9.0

subgraphs:
  # From local files (development)
  products:
    routing_url: http://localhost:4001/graphql
    schema:
      file: ./services/products/schema.graphql

  # From running service (hot reload)
  inventory:
    routing_url: http://localhost:4002/graphql
    schema:
      subgraph_url: http://localhost:4002/graphql

  # From GraphOS (production baseline)
  users:
    routing_url: http://localhost:4003/graphql
    schema:
      graphref: my-graph@production
      subgraph: users

  # With authentication
  orders:
    routing_url: http://localhost:4004/graphql
    schema:
      subgraph_url: http://localhost:4004/graphql
      introspection_headers:
        Authorization: Bearer ${ORDERS_TOKEN}
```

## Composition Errors

### Common Errors

**Entity Key Mismatch:**
```
Error: Entity "Product" has different keys in different subgraphs
```
Fix: Ensure `@key` directives match across subgraphs.

**Invalid Reference:**
```
Error: Cannot extend type "Product" - not found in any subgraph
```
Fix: Define the base type in one subgraph before extending.

**Field Conflict:**
```
Error: Field "Product.name" has different types in different subgraphs
```
Fix: Ensure field types match or use `@override`.

### Debugging Composition

```bash
# Verbose output
rover supergraph compose --config supergraph.yaml 2>&1 | head -100

# JSON output includes detailed errors
rover supergraph compose --config supergraph.yaml --format json
```

## Using with Router

### Local Development

```bash
# 1. Compose supergraph
rover supergraph compose --config supergraph.yaml > supergraph.graphql

# 2. Run Router with composed schema
router --supergraph supergraph.graphql
```

### With rover dev (Recommended)

```bash
# Automatic composition and Router
rover dev --supergraph-config supergraph.yaml
```

## Environment Variables

Use environment variables in config:

```yaml
subgraphs:
  products:
    routing_url: ${PRODUCTS_URL}
    schema:
      subgraph_url: ${PRODUCTS_URL}
      introspection_headers:
        Authorization: Bearer ${PRODUCTS_TOKEN}
```

```bash
PRODUCTS_URL=http://localhost:4001/graphql \
PRODUCTS_TOKEN=secret \
  rover supergraph compose --config supergraph.yaml
```

## CI/CD Integration

### Validate Composition

```bash
# Fail if composition errors
rover supergraph compose --config supergraph.yaml > /dev/null
echo "Composition successful"
```

### Compare with Production

```bash
# Fetch production supergraph
rover supergraph fetch my-graph@production > production.graphql

# Compose local
rover supergraph compose --config supergraph.yaml > local.graphql

# Diff schemas
diff production.graphql local.graphql
```

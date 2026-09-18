# Validation Commands

## Table of Contents

- [Compose Schema](#compose-schema)
- [Execute Connector](#execute-connector)
- [Test Connector](#test-connector)

## Compose Schema

Validate that your schema composes correctly with `rover supergraph compose`.

```bash
rover supergraph compose --config ./supergraph.yaml
```

### supergraph.yaml Template

```yaml
federation_version: =2.12.0
subgraphs:
  my-connector:  # Unique name for this subgraph
    routing_url: http://localhost  # Placeholder, ignored but required
    schema:
      file: schema.graphql  # Path to your connector schema
```

**Multiple subgraphs:**
```yaml
federation_version: =2.12.0
subgraphs:
  users:
    routing_url: http://localhost
    schema:
      file: users.graphql
  products:
    routing_url: http://localhost
    schema:
      file: products.graphql
  orders:
    routing_url: http://localhost
    schema:
      file: orders.graphql
```

### Common Composition Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `INVALID_BODY` | Literal object without `$()` | Use `body: "$({ a: $args.a })"` |
| `MISSING_ENTITY_CONNECTOR` | Entity without `@connect` | Add `@connect` to the entity type |
| `CIRCULAR_REFERENCE` | Entity stubs create a cycle | Use `@inaccessible` foreign key pattern |

## Execute Connector

Test a single connector against the live API with `rover connector run`.

```bash
rover connector run \
  --schema schema.graphql \
  -c "Query.user" \
  -v '{ "$args": { "id": "123" } }'
```

### Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `--schema` | Path to schema file | `--schema schema.graphql` |
| `-c` | Target connector (`Type.field` or `Type`) | `-c "Query.user"` or `-c "User"` |
| `-v` | Variables as JSON | `-v '{ "$args": { "id": "1" } }'` |

### Target Format

```bash
# Field-level connector
-c "Query.user"
-c "User.posts"

# Type-level connector
-c "User"

# Multiple connectors on same target (0-indexed)
-c "User[0]"
-c "User[1]"
```

### Variable Format

Variables must include the `$` prefix:

```bash
# $args
-v '{ "$args": { "id": "123", "limit": 10 } }'

# $this
-v '{ "$this": { "userId": "456" } }'

# $batch (array)
-v '{ "$batch": [{ "id": "1" }, { "id": "2" }] }'

# Combined
-v '{ "$args": { "limit": 10 }, "$this": { "userId": "123" } }'
```

### Examples

**Query with arguments:**
```bash
rover connector run \
  --schema schema.graphql \
  -c "Query.user" \
  -v '{ "$args": { "id": "user-123" } }'
```

**Field on type:**
```bash
rover connector run \
  --schema schema.graphql \
  -c "User.posts" \
  -v '{ "$this": { "id": "user-123" } }'
```

**Entity resolver:**
```bash
rover connector run \
  --schema schema.graphql \
  -c "Product" \
  -v '{ "$this": { "id": "prod-456" } }'
```

**Batch connector:**
```bash
rover connector run \
  --schema schema.graphql \
  -c "Product" \
  -v '{ "$batch": [{ "id": "1" }, { "id": "2" }, { "id": "3" }] }'
```

## Test Connector

Run automated tests with `rover connector test`.

```bash
rover connector test
```

This runs all `*.connector.yaml` test files found in the project.

### Test File Location

Place test files in a `/tests` directory:
```
/tests/
  users.connector.yaml
  products.connector.yaml
  orders.connector.yaml
```

### Test File Structure

```yaml
config:
  schema: ../schema.graphql  # Path to schema file

tests:
  - name: "Should fetch user by ID"
    target: "Query.user"
    variables:
      $args:
        id: "user-123"
    apiResponseBody: |
      {
        "id": "user-123",
        "name": "John Doe",
        "email": "john@example.com"
      }
    expect:
      connectorRequest:
        url: http://api.example.com/users/user-123
      connectorResponse: |
        {
          "id": "user-123",
          "name": "John Doe",
          "email": "john@example.com"
        }
```

### Test File Schema

```yaml
config:
  schema: string          # Required: path to schema file
  name: string            # Optional: test suite name

tests:
  - name: string          # Required: test name
    target: string        # Required: Type.field or Type[index]
    skip: boolean         # Optional: skip this test
    variables:            # Optional: input variables
      $args: object
      $this: object
      $batch: array
      $context: object
      $config: object
      $requestHeaders: object
    apiResponseBody: string       # Mock API response (inline)
    apiResponseBodyFile: string   # Mock API response (file path)
    apiResponseHeaders: object    # Mock response headers
    status: integer               # Mock HTTP status code
    expect:
      connectorRequest:           # Expected request
        method: GET|POST|PUT|PATCH|DELETE
        url: string               # Preferred: full URL
        origin: string            # Alternative: only origin
        path: string              # Alternative: only path
        queryParams: object
        headers: object
        body: string
        bodyFile: string
      connectorResponse: string   # Expected mapped response (inline)
      connectorResponseFile: string  # Expected response (file path)
      error:                      # Expected error
        message: string
        extensions: object
      problems: array             # Expected problems
```

### Test Examples

**Basic query test:**
```yaml
tests:
  - name: "Get user by ID"
    target: "Query.user"
    variables:
      $args:
        id: "123"
    apiResponseBody: |
      { "id": "123", "name": "Alice" }
    expect:
      connectorRequest:
        url: http://api.example.com/users/123
      connectorResponse: |
        { "id": "123", "name": "Alice" }
```

**Entity resolver test:**
```yaml
tests:
  - name: "Resolve User entity"
    target: "User"
    variables:
      $this:
        id: "456"
    apiResponseBody: |
      { "id": "456", "name": "Bob", "email": "bob@test.com" }
    expect:
      connectorRequest:
        url: http://api.example.com/users/456
      connectorResponse: |
        { "id": "456", "name": "Bob", "email": "bob@test.com" }
```

**Batch connector test:**
```yaml
tests:
  - name: "Batch resolve products"
    target: "Product"
    variables:
      $batch:
        - id: "1"
        - id: "2"
    apiResponseBody: |
      [
        { "id": "1", "name": "Widget" },
        { "id": "2", "name": "Gadget" }
      ]
    expect:
      connectorRequest:
        method: POST
        url: http://api.example.com/products/batch
        body: '{"ids":["1","2"]}'
      connectorResponse: |
        [
          { "id": "1", "name": "Widget" },
          { "id": "2", "name": "Gadget" }
        ]
```

**Test with headers:**
```yaml
tests:
  - name: "Request with auth header"
    target: "Query.protectedData"
    variables:
      $requestHeaders:
        authorization: "Bearer token123"
    apiResponseBody: |
      { "data": "secret" }
    expect:
      connectorRequest:
        url: http://api.example.com/protected
        headers:
          Authorization: "Bearer token123"
      connectorResponse: |
        { "data": "secret" }
```

**Error handling test:**
```yaml
tests:
  - name: "Handle 404 error"
    target: "Query.user"
    variables:
      $args:
        id: "not-found"
    status: 404
    apiResponseBody: |
      { "error": "User not found" }
    expect:
      connectorRequest:
        url: http://api.example.com/users/not-found
      error:
        message: "User not found"
        extensions: {}
```

### Important Notes

1. `connectorResponse` is the result of selection mapping, NOT the final GraphQL response
2. No type conversion happens unless explicitly done in the selection
3. Prefer `expect.connectorRequest.url` over separate `origin` and `path`
4. Test both success and error cases
5. Ensure full coverage for each connector

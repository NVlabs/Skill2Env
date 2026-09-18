# Available Variables

You MUST NOT make up variable names - only use variables listed here.

## Table of Contents

- [Variable Reference](#variable-reference)
- [$ - Root/Parent Reference](#---rootparent-reference)
- [$args - Field Arguments](#args---field-arguments)
- [$batch - Entity Batching](#batch---entity-batching)
- [$config - Router Configuration](#config---router-configuration)
- [$context - Coprocessor Context](#context---coprocessor-context)
- [$env - Environment Variables](#env---environment-variables)
- [$request.headers - Incoming Request Headers](#requestheaders---incoming-request-headers)
- [$response.headers - Response Headers](#responseheaders---response-headers)
- [$status - HTTP Status Code](#status---http-status-code)
- [$this - Parent Object Fields](#this---parent-object-fields)
- [@ - Transformation Context](#---transformation-context)

## Variable Reference

| Variable | Description | Availability |
|----------|-------------|--------------|
| `$` | Root/parent reference | `selection`, `errors` in `@connect` |
| `$args` | Field arguments | `@connect` when field has arguments |
| `$batch` | Entity batch references | `@connect` on types only |
| `$config` | Router configuration | Always available |
| `$context` | Coprocessor context | When customizations set context |
| `$env` | Environment variables | Always available |
| `$request.headers` | Incoming request headers | Always available |
| `$response.headers` | Response headers | `selection`, `errors` |
| `$status` | HTTP response status code | `selection`, `errors` in `@connect` |
| `$this` | Parent object fields | Non-root types only |
| `@` | Transformation context | Within method arguments |

## `$` - Root/Parent Reference

At the top level, `$` refers to the API response body root. Within a sub-selection, `$` refers to the parent value.

```graphql
selection: """
# $ refers to response root
$.results {
  # Inside here, $ refers to each item in results
  id
  fullName: $.name.first
}
"""
```

**Usage:**
- Top-level: Access response root
- In sub-selection: Access current parent context
- Only available in `@connect`'s `selection` and `errors`

## `$args` - Field Arguments

Access arguments passed to the GraphQL field.

```graphql
type Query {
  user(id: ID!): User
    @connect(
      http: { GET: "/users/{$args.id}" }
      selection: "id name"
    )

  users(limit: Int, offset: Int): [User]
    @connect(
      http: {
        GET: "/users"
        queryParams: """
        limit: $args.limit
        offset: $args.offset
        """
      }
      selection: "id name"
    )
}
```

**Usage:**
- In URL templates: `"/path/{$args.id}"`
- In query params: `limit: $args.limit`
- In body: `"userId: $args.id"`
- Available when field has defined arguments

## `$batch` - Entity Batching

Used to batch multiple entity resolution requests into a single API call.

```graphql
type Product @connect(
  source: "api"
  http: {
    POST: "/products/batch"
    body: "ids: $batch.id"
  }
  selection: """
  id
  name
  price
  """
) {
  id: ID!
  name: String
  price: Float
}
```

**Rules:**
- Only available on `@connect` attached to types
- Fields referenced in `$batch` must be in the `selection`
- API must support batch requests

See [entities.md](entities.md) for detailed batching patterns.

## `$config` - Router Configuration

Access values from router configuration file.

**Router config (router.yaml):**
```yaml
connectors:
  sources:
    my_subgraph.my_api:
      $config:
        api_version: "v2"
        feature_flag: true
```

**Schema usage:**
```graphql
@connect(
  http: { GET: "/api/{$config.api_version}/users" }
  selection: "id name"
)
```

**Note:** Prefer `$env` over `$config` when possible.

## `$context` - Coprocessor Context

Access context set by router customizations like coprocessors.

```graphql
@connect(
  http: {
    GET: "/users"
    headers: [
      { name: "X-Tenant", value: "{$context.tenantId}" }
    ]
  }
  selection: "id name"
)
```

**Usage:**
- Only available when router customizations have set context
- Typically used with coprocessors for multi-tenancy, auth, etc.

## `$env` - Environment Variables

Access environment variables available to the router process.

```graphql
@source(
  name: "api"
  http: {
    baseURL: "https://api.example.com"
    headers: [
      { name: "Authorization", value: "Bearer {$env.API_KEY}" }
    ]
  }
)
```

**Common patterns:**
```graphql
# API keys
{ name: "X-API-Key", value: "{$env.API_KEY}" }

# Dynamic base URLs
baseURL: "{$env.API_BASE_URL}"

# Feature flags
# (use in combination with conditional logic)
```

**Always available.** Prefer this over hardcoding secrets.

## `$request.headers` - Incoming Request Headers

Access headers from the client request to the router.

```graphql
@connect(
  http: {
    GET: "/users"
    headers: [
      { name: "Authorization", value: "{$request.headers.authorization->first}" }
    ]
  }
  selection: "id name"
)
```

**Important:**
- Headers are always arrays (can have multiple values)
- Use `->first` to get the first value
- Use quoted syntax for headers with special characters: `$request.headers.'x-my-header'->first`

## `$response.headers` - Response Headers

Access headers from the connector's HTTP response.

```graphql
@connect(
  http: { GET: "/users" }
  selection: """
  id
  name
  rateLimit: $response.headers.'x-rate-limit'->first->parseInt
  """
)
```

**Usage:**
- Available in `selection` and `errors`
- Headers are arrays - use `->first`
- Useful for pagination cursors, rate limits, etc.

## `$status` - HTTP Status Code

Access the numeric HTTP status code from the response.

```graphql
@connect(
  http: { DELETE: "/users/{$args.id}" }
  selection: """
  success: $(true)
  """
  errors: {
    message: "$status->match([404, 'Not found'], [@, 'Error'])"
  }
)
```

**Usage:**
- Available in `selection` and `errors` of `@connect`
- Returns numeric code (200, 404, 500, etc.)
- Useful for error handling and conditional responses

## `$this` - Parent Object Fields

Access sibling fields from the parent object. Used for field-level connectors that need parent data.

```graphql
type User {
  id: ID!
  name: String
  posts: [Post] @connect(
    http: { GET: "/users/{$this.id}/posts" }
    selection: "id title"
  )
}
```

**Usage:**
- Only available on non-root types (not Query/Mutation)
- Access sibling fields that have been resolved
- Creates dependencies between fields

**Example with nested access:**
```graphql
type Order {
  id: ID!
  customerId: ID!
  customer: Customer @connect(
    http: { GET: "/customers/{$this.customerId}" }
    selection: "id name email"
  )
}
```

## `@` - Transformation Context

The current value being transformed within a method. Changes meaning based on context.

```graphql
selection: """
# In filter: @ is each array item
activeUsers: $.users->filter(@.isActive)

# In map: @ is each item being transformed
names: $.users->map(@.name)

# In echo: @ is the input value
wrapped: $.data->echo({ value: @ })

# Nested: @ refers to innermost context
items: $.list->map({ doubled: @->mul(2) })
"""
```

**Context changes:**
- `filter(@.field)` - `@` is each item being tested
- `map(@.field)` - `@` is each item being transformed
- `echo({ a: @ })` - `@` is the input to echo
- `match([cond, @])` - `@` is the original value

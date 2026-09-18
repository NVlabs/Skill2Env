# Entities and Batching

## Table of Contents

- [Entity Basics](#entity-basics)
- [Entity Stubs](#entity-stubs)
- [Entity Pattern: Type-Level @connect](#entity-pattern-type-level-connect)
- [Entity Pattern: Field-Level @connect](#entity-pattern-field-level-connect)
- [Using Entities Across Subgraphs](#using-entities-across-subgraphs)
- [Batching with $batch](#batching-with-batch)
- [Handling Circular References](#handling-circular-references)
- [Multiple @connect on Same Type](#multiple-connect-on-same-type)
- [Entity Resolution Patterns](#entity-resolution-patterns)

## Entity Basics

An entity is a type that can be resolved by a unique key. In connectors, add `@connect` to a type to make it an entity.

```graphql
# This makes User an entity - no @key needed
type User @connect(
  source: "api"
  http: { GET: "/users/{$this.id}" }
  selection: "id name email"
) {
  id: ID!
  name: String
  email: String
}
```

**Key rules:**
- Do NOT add `@key` directive - `@connect` on type is sufficient
- Every authoritative entity MUST have a `@connect` on it
- If no API endpoint resolves an entity, make it a normal type (no `@connect`, no `@key`)

## Entity Stubs

When a parent type returns an ID that references an entity, create an entity stub in the selection.

**API Response:**
```json
{
  "id": "order-1",
  "userId": "user-123",
  "total": 99.99
}
```

**Schema:**
```graphql
type Order {
  id: ID!
  user: User  # Entity reference
  total: Float
}

type User @connect(
  source: "api"
  http: { GET: "/users/{$this.id}" }
  selection: "id name email"
) {
  id: ID!
  name: String
  email: String
}

type Query {
  order(id: ID!): Order
    @connect(
      source: "api"
      http: { GET: "/orders/{$args.id}" }
      selection: """
      id
      user: { id: userId }  # Entity stub - only the key field
      total
      """
    )
}
```

The `user: { id: userId }` creates a stub with only the key field. The router then uses the `User @connect` to resolve the full user.

## Entity Pattern: Type-Level @connect

Use `@connect` on a type when you need:
- An entity resolver (resolve by key)
- Access to `$this` for parent fields
- Batch resolution with `$batch`

```graphql
type Product @connect(
  source: "api"
  http: { GET: "/products/{$this.id}" }
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

## Entity Pattern: Field-Level @connect

Use `@connect` on a field for simple parent-child relationships.

```graphql
type User {
  id: ID!
  name: String
  posts: [Post] @connect(
    source: "api"
    http: { GET: "/users/{$this.id}/posts" }
    selection: "id title content"
  )
}
```

**When to choose:**
- **Type-level**: Entity resolvers, batching, multiple connectors on same type
- **Field-level**: Simple nested data, one-off relationships

## Using Entities Across Subgraphs

When an entity is defined in one subgraph and referenced in another:

**Authoritative Subgraph (defines full entity):**
```graphql
type User @connect(
  source: "users_api"
  http: { GET: "/users/{$this.id}" }
  selection: "id name email avatar"
) {
  id: ID!
  name: String
  email: String
  avatar: String
}
```

**Referencing Subgraph (entity stub only):**
```graphql
# Only define the key field
type User @key(fields: "id") {
  id: ID!
}

type Order {
  id: ID!
  user: User  # References the entity
}

type Query {
  order(id: ID!): Order
    @connect(
      selection: """
      id
      user: { id: userId }  # Create stub with key
      """
    )
}
```

## Batching with $batch

Convert N+1 queries to batch requests using `$batch`.

**Before (N+1 problem):**
```graphql
type Product @connect(
  source: "api"
  http: { GET: "/products/{$this.id}" }
  selection: "id name price"
) {
  id: ID!
  name: String
  price: Float
}
```

**After (batched):**
```graphql
type Product @connect(
  source: "api"
  http: {
    POST: "/products/batch"
    body: "ids: $batch.id"
  }
  selection: "id name price"
) {
  id: ID!
  name: String
  price: Float
}
```

### Batch Rules

1. Fields referenced in `$batch` must be in the selection
2. API must support batch requests
3. Only available on type-level `@connect`
4. Use `batch: { maxSize: N }` to limit batch size

### Batch with Grouped Results

When API returns grouped results:

**API Response:**
```json
[
  { "productId": "1", "reviews": [...] },
  { "productId": "2", "reviews": [...] }
]
```

**Schema:**
```graphql
type Product @connect(
  source: "api"
  http: {
    POST: "/reviews/batch"
    body: "productIds: $batch.id"
  }
  selection: """
  id: productId
  reviews {
    id
    rating
    text
  }
  """
) {
  id: ID!
  reviews: [Review]
}
```

Map the grouping key (`productId`) back to the entity key (`id`).

### Batch Size Limits

```graphql
type Product @connect(
  source: "api"
  http: {
    POST: "/products/batch"
    body: "ids: $batch.id"
  }
  batch: { maxSize: 100 }  # Limit to 100 items per request
  selection: "id name"
) {
  id: ID!
  name: String
}
```

## Handling Circular References

When you encounter circular references, do NOT create entity stubs. Instead:

1. Include the foreign key in the parent's selection
2. Add the foreign key to the child type with `@inaccessible`
3. Use the foreign key in a `@connect` back to the parent

```graphql
type Product {
  id: ID!
  name: String
  reviews: [Review] @connect(
    source: "api"
    http: { GET: "/products/{$this.id}/reviews" }
    selection: "id rating text productId"  # Include foreign key
  )
}

type Review {
  id: ID!
  rating: Int
  text: String
  productId: ID! @inaccessible  # Hidden from clients
  product: Product @connect(
    source: "api"
    http: { GET: "/products/{$this.productId}" }
    selection: "id name"
  )
}
```

## Multiple @connect on Same Type

Add multiple connectors when different endpoints provide different fields:

```graphql
type User
  @connect(
    source: "api"
    http: { GET: "/users/{$this.id}" }
    selection: "id firstName lastName"
  )
  @connect(
    source: "api"
    http: { GET: "/users/{$this.id}?detailed=true" }
    selection: """
    id
    address {
      street
      city
      country
    }
    """
  ) {
  id: ID!
  firstName: String
  lastName: String
  address: Address
}
```

The router calls the appropriate connector(s) based on which fields are requested.

## Entity Resolution Patterns

### Pattern 1: Direct Resolution
```graphql
type User @connect(
  http: { GET: "/users/{$this.id}" }
  selection: "id name"
) {
  id: ID!
  name: String
}
```

### Pattern 2: Nested Field Resolution
```graphql
type User {
  id: ID!
  profile: Profile @connect(
    http: { GET: "/users/{$this.id}/profile" }
    selection: "bio avatar"
  )
}
```

### Pattern 3: Batch Resolution
```graphql
type User @connect(
  http: { POST: "/users/batch", body: "ids: $batch.id" }
  selection: "id name"
) {
  id: ID!
  name: String
}
```

### Pattern 4: Cross-Subgraph Reference
```graphql
# In orders subgraph
type User @key(fields: "id") {
  id: ID!  # Stub only
}

type Order {
  user: User  # Resolved by users subgraph
}
```

# Troubleshooting

Common errors and solutions when working with Apollo Connectors.

## Table of Contents

- [No + Operator for Concatenation](#no--operator-for-concatenation)
- [Literal Values Require $()](#literal-values-require-)
- [No Array Indexing Syntax](#no-array-indexing-syntax)
- [MISSING_ENTITY_CONNECTOR Error](#missing_entity_connector-error)
- [INVALID_BODY Error](#invalid_body-error)
- [No == Operator](#no--operator)
- [No Ternary Operator](#no-ternary-operator)
- [Filter with Multiple Conditions](#filter-with-multiple-conditions)
- [Circular Reference Error](#circular-reference-error)
- [Headers Are Always Arrays](#headers-are-always-arrays)
- [Unnecessary Root $](#unnecessary-root-)
- [Wrong Federation/Connect Versions](#wrong-federationconnect-versions)
- [Entity Without Endpoint](#entity-without-endpoint)
- [Selection vs GraphQL Response](#selection-vs-graphql-response)
- [Batch Without API Support](#batch-without-api-support)

## No `+` Operator for Concatenation

**Problem:** Trying to concatenate strings with `+`.

```graphql
# WRONG
fullName: firstName + " " + lastName
```

**Solution:** Use `->joinNotNull` with an array.

```graphql
# CORRECT
fullName: $([firstName, lastName])->joinNotNull(' ')

# With more parts
address: $([street, city, state, zip])->joinNotNull(', ')
```

## Literal Values Require `$()`

**Problem:** Literal values in mappings without the `$()` wrapper.

```graphql
# WRONG - Will not compose
body: "{ userId: $args.id }"
greeting: "Hello"
count: 42
```

**Solution:** Wrap literals in `$()`.

```graphql
# CORRECT
body: "$({ userId: $args.id })"
greeting: $("Hello")
count: $(42)
isActive: $(true)
```

## No Array Indexing Syntax

**Problem:** Trying to use bracket notation for array access.

```graphql
# WRONG
firstItem: items[0]
thirdItem: items[2]
```

**Solution:** Use array methods.

```graphql
# CORRECT
firstItem: items->first
lastItem: items->last
thirdItem: items->get(2)
firstThree: items->slice(0, 3)
```

## MISSING_ENTITY_CONNECTOR Error

**Problem:** An entity type is missing a `@connect` directive.

```
Error: MISSING_ENTITY_CONNECTOR
Entity "User" is missing a connector.
```

**Cause:** You've referenced a type as an entity (via stub or `@key`) but haven't defined how to resolve it.

**Solution:** Add `@connect` to the entity type.

```graphql
# Add @connect to make it a resolvable entity
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

Or, if it shouldn't be an entity, remove the entity stub and inline the data.

## INVALID_BODY Error

**Problem:** Request body not properly formatted.

```
Error: INVALID_BODY
Body must use literal syntax.
```

**Cause:** Object literal in body without `$()` wrapper.

```graphql
# WRONG
body: "{ userId: $args.id }"
```

**Solution:** Use `$()` for object literals.

```graphql
# CORRECT
body: "$({ userId: $args.id })"

# For nested objects
body: "$({ user: { id: $args.id, name: $args.name } })"
```

## No `==` Operator

**Problem:** Using `==` for equality comparison.

```graphql
# WRONG
isActive: status == "active"
is200: $status == 200
```

**Solution:** Use the `->eq` method.

```graphql
# CORRECT
isActive: status->eq("active")
is200: $status->eq(200)
```

For HTTP status checks with simple boolean returns:
```graphql
# For DELETE operations that should return true on success
selection: "$(true)"
```

## No Ternary Operator

**Problem:** Using ternary operator for conditional values.

```graphql
# WRONG
result: condition ? valueA : valueB
```

**Solution:** Use null coalescing operators.

```graphql
# Use ?? for null/undefined fallback
result: value ?? "default"

# Use ?! for undefined-only fallback (preserves null)
result: value ?! "fallback"

# Use ->match for value mapping
result: status->match(
  ["active", "Active User"],
  ["inactive", "Inactive User"],
  [@, "Unknown"]
)
```

## Filter with Multiple Conditions

**Problem:** Using `->and` inside `filter` or `find`.

```graphql
# WRONG - @ changes meaning in nested method
items: $.list->filter(@.active->and(@.price->gt(10)))
```

**Cause:** The `@` variable refers to different values in nested contexts.

**Solution:** Chain filter calls.

```graphql
# CORRECT - Chain filters
items: $.list->filter(@.active)->filter(@.price->gt(10))

# For find
item: $.list->filter(@.active)->find(@.price->gt(10))
```

## Circular Reference Error

**Problem:** Entity stubs create a circular dependency.

```
Error: Circular reference detected between Product and Review
```

**Cause:** Product has reviews, Review has product, both as entity stubs.

**Solution:** Use `@inaccessible` foreign key pattern.

```graphql
type Product {
  id: ID!
  reviews: [Review] @connect(
    http: { GET: "/products/{$this.id}/reviews" }
    selection: "id rating text productId"  # Include FK
  )
}

type Review {
  id: ID!
  rating: Int
  text: String
  productId: ID! @inaccessible  # Hide from clients
  product: Product @connect(
    http: { GET: "/products/{$this.productId}" }
    selection: "id name"
  )
}
```

## Headers Are Always Arrays

**Problem:** Accessing header value directly.

```graphql
# WRONG - Headers are arrays
auth: $request.headers.authorization
```

**Solution:** Use `->first` to get the first value.

```graphql
# CORRECT
auth: $request.headers.authorization->first

# For headers with special characters
custom: $request.headers.'x-custom-header'->first
```

## Unnecessary Root `$`

**Problem:** Using `$` when selecting from root.

```graphql
# WRONG - Unnecessary
selection: """
$ {
  id
  name
}
"""
```

**Solution:** Select fields directly.

```graphql
# CORRECT
selection: """
id
name
"""
```

Use `$` only when:
- Accessing a nested path: `$.results { id }`
- Using a method: `$->first { id }`

## Wrong Federation/Connect Versions

**Problem:** Schema won't compose due to version mismatch.

```
Error: Incompatible federation and connect versions
```

**Solution:** Use the correct version combination.

```graphql
# CORRECT - Always use these versions together
extend schema
  @link(url: "https://specs.apollo.dev/federation/v2.12")
  @link(url: "https://specs.apollo.dev/connect/v0.3", import: ["@source", "@connect"])
```

## Entity Without Endpoint

**Problem:** Want to create an entity but there's no API endpoint for it.

**Solution:** Don't make it an entity. Use a regular type.

```graphql
# If there's no /address/{id} endpoint, don't make it an entity
type Address {  # No @connect, no @key
  street: String
  city: String
  country: String
}

# Include it inline in the parent's selection
type User @connect(
  http: { GET: "/users/{$this.id}" }
  selection: """
  id
  name
  address {
    street
    city
    country
  }
  """
) {
  id: ID!
  name: String
  address: Address
}
```

## Selection vs GraphQL Response

**Problem:** Test expectations don't match actual output.

**Cause:** `connectorResponse` in tests is the selection mapping result, not the final GraphQL response.

```yaml
# apiResponseBody from REST API
apiResponseBody: |
  { "user_id": "123", "user_name": "Alice" }

# Selection mapping
selection: """
id: user_id
name: user_name
"""

# connectorResponse is the mapping result
connectorResponse: |
  { "id": "123", "name": "Alice" }
```

Note: No type conversion unless explicitly done with `->parseInt`, `->toString`, etc.

## Batch Without API Support

**Problem:** Using `$batch` but API doesn't support batch requests.

**Solution:**
1. Ask user if API has a batch endpoint
2. If not, use non-batch pattern and accept N+1 queries
3. Consider if the API can be modified to add batch support

```graphql
# Non-batch (N+1)
type Product @connect(
  http: { GET: "/products/{$this.id}" }
  selection: "id name"
) {
  id: ID!
  name: String
}

# Batch (requires API support)
type Product @connect(
  http: {
    POST: "/products/batch"
    body: "ids: $batch.id"
  }
  selection: "id name"
) {
  id: ID!
  name: String
}
```

# Schema Patterns

Real-world multi-subgraph patterns and recipes for Apollo Federation.

## Entity Definition and Cross-Subgraph Contributions

Multiple subgraphs contribute different fields to the same entity:

```graphql
# Products subgraph
type Product @key(fields: "id") {
  id: ID!
  name: String!
  price: Int
}

# Reviews subgraph
type Product @key(fields: "id") {
  id: ID!
  reviews: [Review!]!
  averageRating: Float
}

# Inventory subgraph
type Product @key(fields: "id") {
  id: ID!
  inStock: Boolean!
}
```

Each subgraph defines the `@key` and only the fields it owns. The router composes them into a single `Product` type.

## Value Types with @shareable

Share identical types across subgraphs when multiple subgraphs need to resolve the same fields:

```graphql
# Subgraph A
type Position @shareable {
  x: Int!
  y: Int!
}

# Subgraph B
type Position @shareable {
  x: Int!
  y: Int!
}
```

All subgraphs must return identical values for shared fields. Use type-level `@shareable` for value types and field-level for selective sharing:

```graphql
type Product @key(fields: "id") {
  id: ID!
  name: String! @shareable
  price: Int
}
```

### Differing Return Types

Nullable can coerce to non-nullable:

```graphql
# Subgraph A
type Position @shareable {
  x: Int!  # non-nullable
}

# Subgraph B
type Position @shareable {
  x: Int   # nullable - OK, supergraph uses nullable
}
```

### Differing Arguments

Required in one subgraph can be optional in others. Optional arguments omitted from any subgraph are omitted from the supergraph:

```graphql
# Subgraph A
type Building @shareable {
  height(units: String!): Int!  # required
}

# Subgraph B
type Building @shareable {
  height(units: String): Int!   # optional - OK
}
```

## Entity Stubs with resolvable: false

Reference entities from another subgraph without resolving them:

```graphql
# Reviews subgraph
type Review @key(fields: "id") {
  id: ID!
  body: String!
  product: Product!
}

type Product @key(fields: "id", resolvable: false) {
  id: ID!
}
```

No reference resolver needed. The router handles resolution via the subgraph that owns `Product`.

## Entity Interfaces with @interfaceObject

Add fields to all implementations of an entity interface from a separate subgraph (Federation 2.3+):

```graphql
# Content subgraph - defines entity interface and implementations
interface Media @key(fields: "id") {
  id: ID!
  title: String!
}

type Book implements Media @key(fields: "id") {
  id: ID!
  title: String!
  author: String!
}

# Reviews subgraph - adds fields without knowing implementations
type Media @key(fields: "id") @interfaceObject {
  id: ID!
  reviews: [Review!]!
}
```

Composition adds `reviews` to the `Media` interface and all its implementations.

## Computed Fields with @requires

Define fields that depend on values from other subgraphs:

```graphql
# Products subgraph
type Product @key(fields: "id") {
  id: ID!
  size: Int
  weight: Int
}

# Shipping subgraph
type Product @key(fields: "id") {
  id: ID!
  size: Int @external
  weight: Int @external
  shippingEstimate: String @requires(fields: "size weight")
}
```

The router fetches `size` and `weight` from Products first, then calls Shipping with those values.

### Nested requires

```graphql
shippingEstimate: String @requires(fields: "dimensions { size weight }")
```

### Requires with arguments (Federation 2.1.2+)

```graphql
weight(units: String): Int @external
shippingEstimate: String @requires(fields: "weight(units:\"KILOGRAMS\")")
```

## Conditional Resolution with @provides

Resolve a field from another subgraph only at specific query paths:

```graphql
# Products subgraph
type Product @key(fields: "id") {
  id: ID!
  name: String!
}

# Inventory subgraph
type Product @key(fields: "id") {
  id: ID!
  name: String! @external
}

type Query {
  outOfStockProducts: [Product!]! @provides(fields: "name")
  discontinuedProducts: [Product!]!  # cannot resolve name here
}
```

The Inventory subgraph can resolve `name` only when queried through `outOfStockProducts`.

## Field Migration with @override

Move a field from one subgraph to another:

```graphql
# Step 1: Add field with @override in new subgraph
# Billing subgraph
type Bill @key(fields: "id") {
  id: ID!
  amount: Int! @override(from: "Payments")
}
```

The router immediately starts resolving `amount` from Billing.

```graphql
# Step 2: Remove field from Payments subgraph
type Bill @key(fields: "id") {
  id: ID!
  payment: Payment
}

# Step 3: Remove @override from Billing subgraph
type Bill @key(fields: "id") {
  id: ID!
  amount: Int!
}
```

### Migrating Entire Entities

Apply `@override` to all non-key fields:

```graphql
type Bill @key(fields: "id") {
  id: ID!
  amount: Int! @override(from: "Payments")
  dueDate: Date! @override(from: "Payments")
  status: BillStatus! @override(from: "Payments")
}
```

## Progressive Migration

Gradually migrate traffic using percentages (Enterprise):

```graphql
# Start with 1%
type Bill @key(fields: "id") {
  id: ID!
  amount: Int! @override(from: "Payments", label: "percent(1)")
}

# Increase to 50%
amount: Int! @override(from: "Payments", label: "percent(50)")

# Complete at 100%, then remove from original and drop @override
```

### Best Practices

- Don't leave progressive `@override` indefinitely — each label creates additional query plans
- Share labels across fields migrating together:

```graphql
type Bill @key(fields: "id") {
  id: ID!
  amount: Int! @override(from: "Payments", label: "percent(10)")
  dueDate: Date! @override(from: "Payments", label: "percent(10)")
}
```

- Use a small set of known percentages (`percent(5)`, `percent(25)`, `percent(50)`)
- Use coprocessors or Rhai scripts to dynamically control override labels via feature flags

## Adding Shared Fields Safely with @inaccessible

Add a field to one subgraph without breaking composition when others haven't added it yet:

```graphql
# Step 1: Add field with @inaccessible
# Subgraph A
type Position @shareable {
  x: Int!
  y: Int!
  z: Int! @inaccessible  # hidden from API schema
}

# Subgraph B (not updated yet)
type Position @shareable {
  x: Int!
  y: Int!
}
```

```graphql
# Step 2: Add field to Subgraph B
type Position @shareable {
  x: Int!
  y: Int!
  z: Int!
}

# Step 3: Remove @inaccessible from Subgraph A
type Position @shareable {
  x: Int!
  y: Int!
  z: Int!  # now visible
}
```

## Type Merging: Unions, Interfaces, Input Types

### Unions

Definitions can differ across subgraphs — the supergraph merges all members:

```graphql
# Subgraph A
union Media = Book | Movie

# Subgraph B
union Media = Book | Podcast

# Supergraph
union Media = Book | Movie | Podcast
```

### Interfaces

Adding interface fields requires updating all implementations across all subgraphs. Use entity interfaces (`@key` on interface + `@interfaceObject`) to avoid this.

### Input Types

Merged using intersection — only mutual fields are preserved:

```graphql
# Subgraph A
input UserInput {
  name: String!
  age: Int
}

# Subgraph B
input UserInput {
  name: String!
  email: String
}

# Supergraph - only common field
input UserInput {
  name: String!
}
```

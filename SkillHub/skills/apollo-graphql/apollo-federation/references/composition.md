# Composition Rules and Errors

Rules for composing subgraph schemas into a supergraph, with error codes and fixes.

## Entity Validation

Entities must have valid `@key` definitions that can be resolved across subgraphs.

### KEY_FIELDS_SELECT_INVALID_TYPE

`@key` includes a field returning list, interface, or union.

```graphql
# INVALID
type Product @key(fields: "tags") {
  tags: [String!]!  # list not allowed in key
}

# VALID
type Product @key(fields: "id") {
  id: ID!
  tags: [String!]!
}
```

Use only scalar, enum, or object fields in keys.

### KEY_FIELDS_HAS_ARGS

`@key` includes a field with arguments.

```graphql
# INVALID
type Product @key(fields: "name") {
  name(locale: String!): String!  # args not allowed in key
}

# VALID - use a field without arguments
type Product @key(fields: "id") {
  id: ID!
  name(locale: String!): String!
}
```

### KEY_INVALID_FIELDS

Invalid syntax or unknown fields in `@key`.

```graphql
# INVALID
type Product @key(fields: "sku") {
  id: ID!  # "sku" doesn't exist
}

# VALID
type Product @key(fields: "id") {
  id: ID!
}
```

Check field names and syntax: `@key(fields: "id")` or `@key(fields: "id organization { id }")`.

### INTERFACE_KEY_NOT_ON_IMPLEMENTATION

Entity interface has `@key` but an implementation doesn't.

```graphql
# INVALID
interface Media @key(fields: "id") {
  id: ID!
}

type Book implements Media {  # missing @key
  id: ID!
}

# VALID
type Book implements Media @key(fields: "id") {
  id: ID!
}
```

All implementations must have the same `@key`(s) as the interface.

## Shareability

Fields resolved by multiple subgraphs must be explicitly marked `@shareable`.

### INVALID_FIELD_SHARING

Field resolved by multiple subgraphs without `@shareable`.

```graphql
# INVALID
type Position {
  x: Int!
}

# VALID
type Position @shareable {
  x: Int!
}
```

Add `@shareable` to the field or type in all subgraphs.

### SHAREABLE_HAS_MISMATCHED_RUNTIME_TYPES

Shareable field has incompatible types across subgraphs.

```graphql
# INVALID
# Subgraph A
type Event @shareable {
  timestamp: Int!
}
# Subgraph B
type Event @shareable {
  timestamp: String!  # incompatible with Int!
}
```

Nullable can coerce to non-nullable, but base types must be compatible.

## External Fields

Fields marked `@external` must exist in another subgraph and be used by a directive.

### EXTERNAL_MISSING_ON_BASE

`@external` field not defined in any other subgraph.

Define the field in the originating subgraph, or remove `@external`.

### EXTERNAL_UNUSED

`@external` field not used by `@key`, `@requires`, or `@provides`.

Either use the field in a directive or remove it.

### EXTERNAL_TYPE_MISMATCH

`@external` field type doesn't match the original definition.

Align the type with the originating subgraph.

## Provides/Requires

Fields referenced in `@provides` and `@requires` must be properly declared as `@external`.

### PROVIDES_FIELDS_MISSING_EXTERNAL

`@provides` field not marked `@external`.

```graphql
# INVALID
type Product @key(fields: "id") {
  id: ID!
  name: String!  # missing @external
}
type Query {
  products: [Product!]! @provides(fields: "name")
}

# VALID
type Product @key(fields: "id") {
  id: ID!
  name: String! @external
}
type Query {
  products: [Product!]! @provides(fields: "name")
}
```

### REQUIRES_FIELDS_MISSING_EXTERNAL

`@requires` field not marked `@external`.

```graphql
# INVALID
type Product @key(fields: "id") {
  id: ID!
  weight: Int  # missing @external
  shippingCost: Int @requires(fields: "weight")
}

# VALID
type Product @key(fields: "id") {
  id: ID!
  weight: Int @external
  shippingCost: Int @requires(fields: "weight")
}
```

## Override

The `@override` directive has strict rules about which fields it can be applied to.

### OVERRIDE_FROM_SELF_ERROR

`@override(from: "...")` references its own subgraph.

Use the name of the other subgraph.

### OVERRIDE_SOURCE_HAS_OVERRIDE

Overridden field also has `@override` applied.

Only one subgraph can override a field at a time.

### OVERRIDE_COLLISION_WITH_ANOTHER_DIRECTIVE

`@override` used with `@external`, `@provides`, or `@requires`.

Cannot override external or provided/required fields.

## Type Merging

Types with the same name across subgraphs must be compatible.

### FIELD_TYPE_MISMATCH

Same field has incompatible types across subgraphs.

Align types. Nullable fields can accept non-nullable, but not vice versa.

### TYPE_KIND_MISMATCH

Same type name but different kinds (e.g., object vs interface).

Use consistent type definitions across subgraphs.

### EMPTY_MERGED_ENUM_TYPE

Enum has no values common to all subgraphs.

Ensure at least one shared value, or use `@inaccessible` for subgraph-specific values.

## Inaccessible

The `@inaccessible` directive hides elements from the API schema but has constraints.

### REFERENCED_INACCESSIBLE

`@inaccessible` element referenced by a visible element.

Also mark the referencing element `@inaccessible`, or remove `@inaccessible`.

### ONLY_INACCESSIBLE_CHILDREN

Type has only `@inaccessible` fields.

Add at least one accessible field to the type.

## Satisfiability

### SATISFIABILITY_ERROR

Query cannot be satisfied by available subgraphs. Common causes:

- Missing `@key` on entity
- Missing shared key field between subgraphs
- `resolvable: false` when resolution is needed

Ensure a traversable path exists between subgraphs for every possible query.

## Debugging Tips

1. Run `rover supergraph compose --config supergraph.yaml` locally
2. Check error codes in [Apollo docs](https://apollographql.com/docs/graphos/schema-design/federated-schemas/reference/errors)
3. Use `rover subgraph check` to validate against production
4. Review `@key` fields are consistent across subgraphs
5. Verify all `@external` fields exist in originating subgraph

# Federation Directives

Complete reference for all Apollo Federation 2.x directives.

# Managing Types

## @key

```graphql
directive @key(fields: FieldSet!, resolvable: Boolean = true) repeatable on OBJECT | INTERFACE
```

Designates an object type as an entity with a unique key for cross-subgraph resolution.

### Arguments

| Option       | Type    | Default | Description                                  |
| ------------ | ------- | ------- | -------------------------------------------- |
| `fields`     | String! | —       | Selection set of key fields                  |
| `resolvable` | Boolean | `true`  | Whether this subgraph can resolve the entity |

### Rules

- Must uniquely identify the entity
- Cannot include union/interface fields
- Cannot include fields with arguments
- Use non-nullable fields when possible

### Examples

#### Simple Key

```graphql
type Product @key(fields: "id") {
  id: ID!
  name: String!
}
```

#### Compound Keys

Use multiple fields when a single field isn't unique:

```graphql
type User @key(fields: "username domain") {
  username: String!
  domain: String!
}
```

#### Nested Fields in Keys

```graphql
type User @key(fields: "id organization { id }") {
  id: ID!
  organization: Organization!
}

type Organization {
  id: ID!
}
```

#### Non-Resolvable Keys

Use `resolvable: false` to reference entities without contributing fields:

```graphql
type Product @key(fields: "id", resolvable: false) {
  id: ID!
}
```

#### Multiple Keys

Define multiple keys if there are multiple ways to uniquely identify an entity:

```graphql
type Product @key(fields: "id") @key(fields: "sku") {
  id: ID!
  sku: String!
  name: String!
}
```

#### Differing Keys Across Subgraphs

Subgraphs can use different keys, but must share at least one:

```graphql
# Products subgraph
type Product @key(fields: "sku") @key(fields: "upc") {
  sku: ID!
  upc: String!
  name: String!
}

# Inventory subgraph
type Product @key(fields: "upc") {
  upc: String!
  inStock: Boolean!
}
```

## @interfaceObject

Allows a subgraph to add fields to all implementations of an entity interface without knowing the individual types. Requires Federation 2.3+.

```graphql
directive @interfaceObject on OBJECT
```

### Rules

- All implementing entities must use the same `@key`(s) as the interface
- The defining subgraph must define all implementations
- `@interfaceObject` subgraphs cannot define individual implementations

### Example

```graphql
# Subgraph A - defines entity interface
interface Media @key(fields: "id") {
  id: ID!
  title: String!
}

type Book implements Media @key(fields: "id") {
  id: ID!
  title: String!
  author: String!
}

# Subgraph B - adds fields to all implementations
type Media @key(fields: "id") @interfaceObject {
  id: ID!
  reviews: [Review!]!
}
```

Composition adds `reviews` to `Media` interface and all implementations. 

# Managing Shared Fields

## @shareable

```graphql
directive @shareable repeatable on FIELD_DEFINITION | OBJECT
```

Allows multiple subgraphs to resolve the same field.

### Rules

- If marked `@shareable` in any subgraph, must be `@shareable` or `@external` in all
- Key fields are automatically shareable

### Examples

#### Field-Level @shareable

```graphql
type Product @key(fields: "id") {
  id: ID!
  name: String! @shareable
  price: Int
}
```

#### Type-Level @shareable

If applied on a type definition, all of that type's fields are considered `@shareable`.

```graphql
type Position @shareable {
  x: Int!
  y: Int!
}
```

#### @shareable with type extensions extend

`@shareable` only applies to fields in the same declaration:

```graphql
type Position @shareable {
  x: Int!  # shareable
  y: Int!  # shareable
}

extend type Position {
  z: Int!  # NOT shareable - needs explicit @shareable
}
```

## @inaccessible

```graphql
directive @inaccessible on FIELD_DEFINITION | INTERFACE | OBJECT | UNION | ARGUMENT_DEFINITION | SCALAR | ENUM | ENUM_VALUE | INPUT_OBJECT | INPUT_FIELD_DEFINITION
```

Hides a field or type from the public API schema while keeping it available internally for query planning.

### Examples

#### Safe Schema Evolution 

Safely add shared fields across subgraphs in stages. Mark the field `@inaccessible` until all subgraphs define it, then remove the directive.

```graphql
type Position @shareable {
  x: Int!
  y: Int!
  z: Int! @inaccessible  # hidden from API schema
}
```

#### Private Data

Use private data as `@key` and/or `@requires` data without exposing it to clients.

```graphql
# subgraph A
type Product @key(fields: "id") {
  id: ID!
  secret: String! @inaccessible
}

# subgraph B
type Product @key(fields: "id") {
  id: ID!
  secret: String! @external
  computed: String @requires(fields: "secret")
}
```

## @override

```graphql
directive @override(from: String!) on FIELD_DEFINITION
```

Migrates a field from one subgraph to another.


### Arguments

| Option  | Type    | Default | Description                                                       |
| ------- | ------- | ------- | ----------------------------------------------------------------- |
| `from`  | String! | —       | Name of the subgraph to override                                  |
| `label` | String  | —       | Progressive override label (Enterprise). Requires Federation 2.7+ |

### Rules

- Cannot override `@external` fields
- Cannot override fields with `@provides` or `@requires`
- Cannot override from self
- Cannot use on interface fields
- `from` must match subgraph name exactly

### Examples

#### Full Override

Start resolving `amount` from this subgraph instead of Payments.

```graphql
type Bill @key(fields: "id") {
  id: ID!
  amount: Int! @override(from: "Payments")
}
```

### Progressive @override (Enterprise)

Gradually migrate traffic using percentages:

```graphql
# Start with 1%
amount: Int! @override(from: "Payments", label: "percent(1)")

# Increase to 50%
amount: Int! @override(from: "Payments", label: "percent(50)")

# Complete migration
amount: Int! @override(from: "Payments", label: "percent(100)")
```

# Controlling Access

## @authenticated

```graphql
directive @authenticated on FIELD_DEFINITION | OBJECT | INTERFACE | SCALAR | ENUM
```

Indicates that the target element is accessible only to the authenticated 
supergraph users. Requires Federation 2.5+.

### Rules

- Cannot be applied on interfaces and interface fields.

## @requiresScopes

```graphql
directive @requiresScopes(scopes: [[federation__Scope!]!]!) on FIELD_DEFINITION | OBJECT | INTERFACE | SCALAR | ENUM
```

Indicates that the target element is accessible only to the authenticated
supergraph users with the appropriate JWT scopes. Requires Federation 2.5+.

### Arguments

| Option   | Type                     | Default | Description                                               |
| -------- | ------------------------ | ------- | --------------------------------------------------------- |
| `scopes` | [[federation__Scope!]!]! | —       | List of JWT scopes required to access the underlying data |

### Rules

- Cannot be applied on interfaces and interface fields.
- Inner array of scopes argument represents a conjunction (AND) of conditions that need to be true
- Outer array of scopes argument represents a disjunction (OR) of conditions that needs to be true

### Examples

#### Basic Usage

User query requires `read:user` JWT scope

```graphql
type Query {
  user(id: ID!): User @requiresScopes(scopes: [["read:user"]])
}
```

#### Conjunction of Multiple Scopes

User query requires `read:user` AND `read:pii` JWT scope.

```graphql
type Query {
  user(id: ID!): User @requiresScopes(scopes: [["read:user", "read:pii"]])
}
```

#### Disjunction of Alternative Scopes

User query requires `read:user` OR `admin` JWT scope.

```graphql
type Query {
  user(id: ID!): User @requiresScopes(scopes: [["read:user"], ["admin"]])
}
```

#### Disjunction of Conjunctions

User query requires either both `read:user AND read:pii` OR `admin` JWT scope.

```graphql
type Query {
  user(id: ID!): User @requiresScopes(scopes: [["read:user", "read:pii"], ["admin"]])
}
```

## @policy

```graphql
directive @policy(policies: [[federation__Policy!]!]!) on FIELD_DEFINITION | OBJECT | INTERFACE | SCALAR | ENUM
```

Indicates that access to the target element is restricted based on authorization
policies that will be evaludated by the router. Requires Federation 2.6+.

### Arguments

| Option     | Type                      | Default | Description                                |
| ---------- | ------------------------- | ------- | ------------------------------------------ |
| `policies` | [[federation__Policy!]!]! | —       | List of authorization policies to evaluate |

### Rules

- Cannot be applied on interfaces and interface fields.
- Inner array of scopes argument represents a conjunction (AND) of conditions that need to be true
- Outer array of scopes argument represents a disjunction (OR) of conditions that needs to be true

### Examples

#### Basic Usage

User query requires `reader` policy

```graphql
type Query {
  user(id: ID!): User @policy(policies: [["reader"]])
}
```

#### Conjunction of Multiple Policies

User query requires `reader` AND `personal_data` policies.

```graphql
type Query {
  user(id: ID!): User @policy(policies: [["reader", "personal_data"]])
}
```

#### Disjunction of Alternative Policies

User query requires `reader` OR `admin` policies.

```graphql
type Query {
  user(id: ID!): User @policy(policies: [["reader"], ["admin"]])
}
```

#### Disjunction of Conjunctions

User query requires either both `reader AND personal_data` OR `admin` policies.

```graphql
type Query {
  user(id: ID!): User @policy(policies: [["reader", "personal_data"], ["admin"]])
}
```

# Referencing External Fields

## @external

```graphql
directive @external on FIELD_DEFINITION | OBJECT
```

Marks a field as resolved by another subgraph. Used with `@requires`, `@provides`, and entity stubs.

### Rules

- With `@requires` — declare fields needed for computation
- With `@provides` — declare fields this subgraph can conditionally resolve
- With `resolvable: false` — not needed on entity stubs (key fields only)

## @provides

```graphql
directive @provides(fields: FieldSet!) on FIELD_DEFINITION
```

Declares that a field can resolve an `@external` field at a specific query path.

### Arguments

| Option   | Type    | Default | Description                                       |
| -------- | ------- | ------- | ------------------------------------------------- |
| `fields` | String! | —       | Selection set of optionally resolved local fields |

### Rules

- Provided field must be marked `@external`
- Field must be `@shareable` or `@external` in all subgraphs defining it
- Field must be `@shareable` in at least one other subgraph

### Example

Subgraph can resolve `Product.name` locally only for `outOfStockProducts` query 

```graphql
type Product @key(fields: "id") {
  id: ID!
  name: String! @external
}

type Query {
  outOfStockProducts: [Product!]! @provides(fields: "name")
  discontinuedProducts: [Product!]!  # cannot resolve name here
}
```

## @requires

```graphql
directive @requires(fields: FieldSet!) on FIELD_DEFINITION
```

Defines computed fields that depend on values from other subgraphs.

### Arguments

| Option   | Type    | Default | Description                      |
| -------- | ------- | ------- | -------------------------------- |
| `fields` | String! | —       | Selection set of required fields |

### Example

The router fetches `size` and `weight` from the owning subgraph first, then calls this subgraph with those values available.

```graphql
type Product @key(fields: "id") {
  id: ID!
  size: Int @external
  weight: Int @external
  shippingEstimate: String @requires(fields: "size weight")
}
```

# Applying Metadata

## @tag

```graphql
directive @tag(name: String!) repeatable on FIELD_DEFINITION | INTERFACE | OBJECT | UNION | ARGUMENT_DEFINITION | SCALAR | ENUM | ENUM_VALUE | INPUT_OBJECT | INPUT_FIELD_DEFINITION | SCHEMA
```

Applies arbitrary metadata to a schema location. Custom tooling can use this
metadata during any step of the schema delivery flow, including composition,
static analysis, and documentation. Used by GraphOS Enterprise contracts feature.

### Arguments

| Option | Type    | Default | Description       |
| ------ | ------- | ------- | ----------------- |
| `name` | String! | —       | Tag name to apply |

# Managing Custom Directives

## @composeDirective

```graphql
directive @composeDirective(name: String!) repeatable on SCHEMA
```

Preserves a specific custom type system directive usage defined in a subgraph 
schema in the supergraph schema. Requires Federation 2.3+

### Arguments

| Option | Type    | Default | Description                       |
| ------ | ------- | ------- | --------------------------------- |
| `name` | String! | —       | Custom directive name to preserve |

### Rules

- Custom directive must be defined in the subgraph and imported using `@link` directive
- Custom directive name must match the name imported from `@link` spec
- Custom directive name must be the same in all subgraphs that define and use it

### Example

```graphql
extend schema
    @link(url: "https://specs.apollo.dev/link/v1.0")
    @link(url: "https://specs.apollo.dev/federation/v2.3", import: ["@composeDirective"])
    @link(url: "https://myspecs.dev/myDirective/v1.0", import: ["@myDirective"])
    @composeDirective(name: "@myDirective")

directive @myDirective(a: String!) on FIELD_DEFINITION

type Query {
  helloWorld: String @myDirective
}
```

# Saving and Referencing Data With Contexts

## @context

```graphql
directive @context(name: String!) repeatable on OBJECT | INTERFACE | UNION
```

Defines a named context from which a field of the annotated type can be passed
to a receiver of the context. The receiver must be a field annotated with the 
`@fromContext` directive. Requires Federation 2.8+.

### Arguments

| Option | Type    | Default | Description  |
| ------ | ------- | ------- | ------------ |
| `name` | String! | —       | Context name |

### Rules

- Can be applied to an object, interface or union type
- Type can be annotated with one or more `@context` directives
- Context must be defined with a name and each `@context` name can be applied in multiple places within a subgraph

## @fromContext

```graphql
directive @fromContext(field: ContextFieldValue) on ARGUMENT_DEFINITION
```

Sets the context from which to receive the value of the annotated field. The 
context must have been defined with the `@context` directive. Requires Federation 2.8+.

### Arguments

| Option  | Type               | Default | Description                             |
| ------- | ------------------ | ------- | --------------------------------------- |
| `field` | ContextFieldValue! | —       | Field selection set from target context |

### Rules

- `@fromContext` can only be applied on nullable arguments
- First element of a `ContextFieldValue` selection must be the name of a context defined by `@context` and prefixed with `$`
- Referenced `@context` name has to be accessible through one of the ancestor selection paths
- Second element of a `ContextFieldValue` selection must be a selection set that resolves to a single field
- `ContextFieldValue` selection can specify type conditions but they cannot overlap
- All fields referenced in the `ContextFieldValue` selection must be defined within the current subgraph
- If fields referenced in the `ContextFieldValue` selection are resolved across subgraphs, they must be annotated with `@external`
- `ContextFieldValue` selection cannot specify any directives 

### Example

#### Accessing Parent Data

```graphql
type Query {
  a: A
}

type A @key(fields: "id") @context(name: "userContext") {
  id: ID!
  prop: String!
  u: U
}

type U @key(fields: "id") {
  id: ID!
  field (arg: String @fromContext(field: "$userContext { prop }")): String!
}
```

#### Using Type Conditionals

```graphql
type Query {
  a: A!
  b: B!
}

type A @key(fields: "id") @context(name: "context1"){
  id: ID!
  field: String!
  child: Child!
} 

type B @key(fields: "id") @context(name: "context1"){
  id: ID!
  otherField: String!
  child: Child!
} 

type Child @key(fields: "id") {
  id: ID!
  prop(
    arg: String! 
        @fromContext(field: "$context1 ... on A { field } ... on B { otherField } ")
  ): Int!
}
```

#### Resolving Contexts Across Subgraphs

```graphql
type Query {
  a: A
}

type A @key(fields: "id") @context(name: "userContext") {
  id: ID!
  # this field is resolved by other subgraph
  prop: String! @external
  u: U
}

type U @key(fields: "id") {
  id: ID!
  field (arg: String @fromContext(field: "$userContext { prop }")): String!
}
```

# Customizing Demand Controls

## @cost

```graphql
directive @cost(weight: Int!) on ARGUMENT_DEFINITION | ENUM | FIELD_DEFINITION | INPUT_FIELD_DEFINITION | OBJECT | SCALAR
```

Define custom weight for resolving a schema location. Requires Federation 2.9+.

### Arguments

| Option   | Type | Default | Description                             |
| -------- | ---- | ------- | --------------------------------------- |
| `weight` | Int! | —       | Custom weight for scoring current field |


## @listSize

```graphql
directive @listSize(assumedSize: Int, slicingArguments: [String!], sizedFields: [String!], requireOneSlicingArgument: Boolean = true) on FIELD_DEFINITION
```

Provide weight estimates for list fields that can be used for calculating query cost. Requires Federation 2.9+.

### Arguments

| Option                      | Type      | Default | Description         |
| --------------------------- | --------- | ------- | ------------------- |
| `assumedSize`               | Int       | —       | Estimated list size |
| `slicingArguments`          | [String!] | -       |                     |
| `requireOneSlicingArgument` | Boolean   | true    |                     |

### Examples

#### Cost Estimation Using Static List Size

Assume `items` query will return 10 items and use that for query cost estimation.

```graphql
type Query {
  items: [Item!] @listSize(assumedSize: 10)
}
```

#### Cost Estimation Using Dynamic List Size

Use pagination arguments to specify maximum list size to be equal to the specified `last` count

```graphql
type Query {
  items(first: Int): [Item!] @listSize(slicingArguments: ["first"])
}
```

# Managing Cache Invalidation

## @cacheTag

```graphql
directive @cacheTag(format: String!) repeatable on FIELD_DEFINITION | OBJECT
```

Assign cache tag to the cached data. Requires Federation 2.12+.

### Arguments

| Option   | Type    | Default | Description                            |
| -------- | ------- | ------- | -------------------------------------- |
| `format` | String! | —       | String template that defines cache tag |

### Rules

- `@cacheTag` can only be applied on root query fields and entity types
- `@cacheTag` format can be a static string or use interpolated variables
- if `@cacheTag` is applied on a root field, use `{$args.name}` to interpolate field arguments
- if `@cacheTag` is applied on an entity, use `{$key.fieldName}` to interpolate entity key fields

### Examples

#### Tagging Queries

Assign tags to the queries

```graphql
type Query {
  # static tag
  users: [User!]! @cacheTag(format: "users-list")
  # tag with variables
  user(id: ID!): User @cacheTag(format: "user-{$args.id}")
}
```

#### Cache Tag on an Entity

Assign custom tag that includes `id` to a `User` entity

```graphql
type User @key(fields: "id") @cacheTag(format: "user-{$key.id}") {
  id: ID!
  name: String!
}
```

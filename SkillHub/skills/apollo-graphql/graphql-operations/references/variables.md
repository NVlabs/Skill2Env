# Variable Patterns

This reference covers patterns for using variables in GraphQL operations.

## Table of Contents

- [Variable Basics](#variable-basics)
- [Variable Types](#variable-types)
- [Default Values](#default-values)
- [Complex Inputs](#complex-inputs)
- [Best Practices](#best-practices)

## Variable Basics

### Declaring Variables

Variables are declared in the operation definition:

```graphql
query GetUser($id: ID!) {
  user(id: $id) {
    id
    name
  }
}
```

### Using Variables

Variables are referenced with `$` prefix:

```graphql
query GetUser($id: ID!) {
  user(id: $id) {
    # $id used here
    id
    name
  }
}
```

### Passing Variables

Variables are passed as a separate JSON object:

```typescript
const { data } = await client.query({
  query: GET_USER,
  variables: {
    id: "user_123",
  },
});
```

### Multiple Variables

```graphql
query SearchPosts($query: String!, $status: PostStatus, $first: Int!, $after: String) {
  searchPosts(query: $query, status: $status, first: $first, after: $after) {
    edges {
      node {
        id
        title
      }
    }
  }
}
```

```json
{
  "query": "graphql",
  "status": "PUBLISHED",
  "first": 10,
  "after": "cursor_abc"
}
```

## Variable Types

### Scalar Types

```graphql
query Example(
  $id: ID!
  $name: String!
  $count: Int!
  $price: Float!
  $active: Boolean!
) {
  # ...
}
```

### Custom Scalar Types

```graphql
query Example(
  $date: DateTime!
  $email: Email!
  $url: URL!
) {
  # ...
}
```

### Enum Types

```graphql
query GetPosts($status: PostStatus!) {
  posts(status: $status) {
    id
    title
  }
}
```

```json
{
  "status": "PUBLISHED"
}
```

### List Types

```graphql
query GetUsers($ids: [ID!]!) {
  users(ids: $ids) {
    id
    name
  }
}
```

```json
{
  "ids": ["user_1", "user_2", "user_3"]
}
```

### Input Object Types

```graphql
mutation CreatePost($input: CreatePostInput!) {
  createPost(input: $input) {
    id
  }
}
```

```json
{
  "input": {
    "title": "My Post",
    "content": "Post content...",
    "tags": ["graphql", "api"]
  }
}
```

### Required vs Optional

```graphql
query Example(
  $required: String!     # Must be provided, cannot be null
  $optional: String      # Can be omitted or null
  $requiredList: [String!]!  # List required, items required
  $optionalList: [String]    # List optional, items optional
) {
  # ...
}
```

## Default Values

### Simple Defaults

```graphql
query GetPosts($first: Int = 10, $status: PostStatus = PUBLISHED) {
  posts(first: $first, status: $status) {
    id
    title
  }
}
```

If not provided, uses defaults:

```json
{}
// Equivalent to: { "first": 10, "status": "PUBLISHED" }
```

Override defaults:

```json
{
  "first": 20
}
// Uses first: 20, status: PUBLISHED (default)
```

### Defaults with Optional Variables

```graphql
# Variable is optional (no !) but has default
query GetPosts($first: Int = 10) {
  posts(first: $first) {
    id
  }
}
```

### Defaults for Complex Types

```graphql
query GetPosts($orderBy: PostOrderInput = { field: CREATED_AT, direction: DESC }) {
  posts(orderBy: $orderBy) {
    id
    title
  }
}
```

### When to Use Defaults

Use defaults for:

- Pagination limits (`first: Int = 20`)
- Sort order (`direction: SortDirection = DESC`)
- Common filter values (`status: Status = ACTIVE`)
- Feature flags (`includeArchived: Boolean = false`)

## Complex Inputs

### Nested Input Objects

```graphql
mutation CreateOrder($input: CreateOrderInput!) {
  createOrder(input: $input) {
    id
    total
  }
}
```

```json
{
  "input": {
    "customer": {
      "email": "customer@example.com",
      "name": "John Doe"
    },
    "items": [
      { "productId": "prod_1", "quantity": 2 },
      { "productId": "prod_2", "quantity": 1 }
    ],
    "shippingAddress": {
      "street": "123 Main St",
      "city": "New York",
      "state": "NY",
      "zipCode": "10001",
      "country": "US"
    }
  }
}
```

### Lists of Input Objects

```graphql
mutation BulkCreateUsers($inputs: [CreateUserInput!]!) {
  bulkCreateUsers(inputs: $inputs) {
    id
    email
  }
}
```

```json
{
  "inputs": [
    { "email": "user1@example.com", "name": "User 1" },
    { "email": "user2@example.com", "name": "User 2" },
    { "email": "user3@example.com", "name": "User 3" }
  ]
}
```

### Filter Inputs

```graphql
query SearchProducts($filter: ProductFilter!) {
  products(filter: $filter) {
    id
    name
    price
  }
}
```

```json
{
  "filter": {
    "category": "ELECTRONICS",
    "priceRange": {
      "min": 100,
      "max": 500
    },
    "inStock": true,
    "tags": ["featured", "sale"]
  }
}
```

## Best Practices

### Always Use Variables for Dynamic Values

```graphql
# Good: Uses variable
query GetUser($id: ID!) {
  user(id: $id) {
    id
    name
  }
}

# Bad: Hardcoded value
query GetUser {
  user(id: "123") {
    id
    name
  }
}
```

### Match Variable Names to Arguments

```graphql
# Good: Clear relationship
query GetUser($userId: ID!) {
  user(id: $userId) {
    id
  }
}

# Also good: Same name
query GetUser($id: ID!) {
  user(id: $id) {
    id
  }
}

# Bad: Confusing names
query GetUser($x: ID!) {
  user(id: $x) {
    id
  }
}
```

### Use Descriptive Variable Names

```graphql
# Good
query SearchPosts(
  $searchQuery: String!
  $authorId: ID
  $publishedAfter: DateTime
  $maxResults: Int = 20
) {
  searchPosts(
    query: $searchQuery
    author: $authorId
    after: $publishedAfter
    first: $maxResults
  ) {
    # ...
  }
}

# Bad
query SearchPosts($q: String!, $a: ID, $d: DateTime, $n: Int) {
  # ...
}
```

### Group Related Variables

```typescript
// Good: Variables object mirrors input structure
const variables = {
  input: {
    title: formData.title,
    content: formData.content,
    tags: formData.tags,
  },
};

// Less clear: Flat variables
const variables = {
  title: formData.title,
  content: formData.content,
  tags: formData.tags,
};
```

### Validate Variables Client-Side

```typescript
function createPost(input: CreatePostInput) {
  // Validate before sending
  if (!input.title?.trim()) {
    throw new Error("Title is required");
  }
  if (input.title.length > 200) {
    throw new Error("Title too long");
  }

  return client.mutate({
    mutation: CREATE_POST,
    variables: { input },
  });
}
```

### Type Variables with TypeScript

```typescript
// Generated types from schema
interface GetUserQueryVariables {
  id: string;
}

// Use with Apollo Client
const { data } = useQuery<GetUserQuery, GetUserQueryVariables>(GET_USER, {
  variables: { id: userId }, // Type-checked
});
```

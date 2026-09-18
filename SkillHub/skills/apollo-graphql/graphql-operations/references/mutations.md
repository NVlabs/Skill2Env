# Mutation Patterns

This reference covers patterns for writing effective GraphQL mutations.

## Table of Contents

- [Mutation Structure](#mutation-structure)
- [Input Patterns](#input-patterns)
- [Response Selection](#response-selection)
- [Error Handling](#error-handling)
- [Optimistic Updates](#optimistic-updates)
- [Mutation Naming](#mutation-naming)

## Mutation Structure

### Basic Mutation

```graphql
mutation CreatePost($input: CreatePostInput!) {
  createPost(input: $input) {
    id
    title
    createdAt
  }
}
```

Variables:

```json
{
  "input": {
    "title": "My Post",
    "content": "Post content..."
  }
}
```

### Mutation with Multiple Arguments

```graphql
mutation UpdatePost($id: ID!, $input: UpdatePostInput!) {
  updatePost(id: $id, input: $input) {
    id
    title
    updatedAt
  }
}
```

### Multiple Mutations

Execute multiple mutations in one request (sequential execution):

```graphql
mutation SetupUserProfile($userId: ID!, $profileInput: ProfileInput!, $settingsInput: SettingsInput!) {
  updateProfile(userId: $userId, input: $profileInput) {
    id
    bio
  }
  updateSettings(userId: $userId, input: $settingsInput) {
    id
    theme
    notifications
  }
}
```

## Input Patterns

### Single Input Object

Recommended pattern - single input argument:

```graphql
mutation CreateUser($input: CreateUserInput!) {
  createUser(input: $input) {
    id
    email
  }
}
```

```json
{
  "input": {
    "email": "user@example.com",
    "name": "John Doe",
    "password": "secret123"
  }
}
```

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
    "items": [
      { "productId": "prod_1", "quantity": 2 },
      { "productId": "prod_2", "quantity": 1 }
    ],
    "shippingAddress": {
      "street": "123 Main St",
      "city": "New York",
      "country": "US"
    }
  }
}
```

### Optional Fields

```graphql
mutation UpdateUser($id: ID!, $input: UpdateUserInput!) {
  updateUser(id: $id, input: $input) {
    id
    name
    bio
  }
}
```

```json
{
  "id": "user_123",
  "input": {
    "name": "New Name"
    // bio not included - won't be changed
  }
}
```

## Response Selection

### Return the Modified Object

Always return the mutated object with updated fields:

```graphql
mutation UpdatePost($id: ID!, $input: UpdatePostInput!) {
  updatePost(id: $id, input: $input) {
    id
    title
    content
    updatedAt # Server-set field
  }
}
```

### Return Related Objects

If mutation affects related data, include it:

```graphql
mutation AddComment($input: AddCommentInput!) {
  addComment(input: $input) {
    id
    body
    post {
      id
      commentCount # Updated count
    }
    author {
      id
      name
    }
  }
}
```

### Return for Cache Updates

Select fields needed to update your cache:

```graphql
mutation DeletePost($id: ID!) {
  deletePost(id: $id) {
    id # Needed to remove from cache
    author {
      id
      postCount # May need to decrement
    }
  }
}
```

### Return Connections for List Updates

```graphql
mutation CreatePost($input: CreatePostInput!) {
  createPost(input: $input) {
    id
    title
    createdAt
    author {
      id
      posts(first: 1) {
        edges {
          node {
            id
          }
        }
        totalCount
      }
    }
  }
}
```

## Error Handling

### Query Result Unions

When schema uses union types for errors:

```graphql
mutation CreateUser($input: CreateUserInput!) {
  createUser(input: $input) {
    ... on CreateUserSuccess {
      user {
        id
        email
      }
    }
    ... on ValidationError {
      message
      field
    }
    ... on EmailAlreadyExists {
      message
      existingUserId
    }
  }
}
```

### Handle All Cases

```typescript
const result = await client.mutate({
  mutation: CREATE_USER,
  variables: { input },
});

const { createUser } = result.data;

switch (createUser.__typename) {
  case "CreateUserSuccess":
    // Handle success
    return createUser.user;
  case "ValidationError":
    // Handle validation error
    throw new ValidationError(createUser.field, createUser.message);
  case "EmailAlreadyExists":
    // Handle specific business error
    throw new EmailExistsError(createUser.existingUserId);
}
```

### GraphQL Errors

Handle network and GraphQL errors:

```typescript
try {
  const result = await client.mutate({
    mutation: CREATE_POST,
    variables: { input },
  });
  return result.data.createPost;
} catch (error) {
  if (error.graphQLErrors?.length) {
    // Handle GraphQL errors
    const gqlError = error.graphQLErrors[0];
    if (gqlError.extensions?.code === "UNAUTHENTICATED") {
      // Redirect to login
    }
  }
  if (error.networkError) {
    // Handle network error
  }
  throw error;
}
```

## Optimistic Updates

### Select Fields for Optimistic Response

Include all fields that will display immediately:

```graphql
mutation LikePost($postId: ID!) {
  likePost(postId: $postId) {
    id
    likeCount
    isLikedByViewer
  }
}
```

```typescript
client.mutate({
  mutation: LIKE_POST,
  variables: { postId: "post_123" },
  optimisticResponse: {
    likePost: {
      __typename: "Post",
      id: "post_123",
      likeCount: currentCount + 1,
      isLikedByViewer: true,
    },
  },
});
```

### Include Created IDs

For create mutations, use temporary IDs:

```graphql
mutation AddComment($input: AddCommentInput!) {
  addComment(input: $input) {
    id
    body
    createdAt
    author {
      id
      name
      avatarUrl
    }
  }
}
```

```typescript
client.mutate({
  mutation: ADD_COMMENT,
  variables: { input: { postId, body } },
  optimisticResponse: {
    addComment: {
      __typename: "Comment",
      id: `temp-${Date.now()}`, // Temporary ID
      body,
      createdAt: new Date().toISOString(),
      author: {
        __typename: "User",
        id: currentUser.id,
        name: currentUser.name,
        avatarUrl: currentUser.avatarUrl,
      },
    },
  },
});
```

## Mutation Naming

### Naming Conventions

| Operation    | Pattern              | Examples                        |
| ------------ | -------------------- | ------------------------------- |
| Create       | `Create{Type}`       | `CreateUser`, `CreatePost`      |
| Update       | `Update{Type}`       | `UpdateUser`, `UpdatePost`      |
| Delete       | `Delete{Type}`       | `DeleteUser`, `DeletePost`      |
| Action       | `{Verb}{Type}`       | `PublishPost`, `ArchiveProject` |
| Relationship | `{Add/Remove}{Type}` | `AddTeamMember`, `RemoveTag`    |

### Good Names

```graphql
mutation CreateUser($input: CreateUserInput!) { ... }
mutation UpdateUserProfile($userId: ID!, $input: ProfileInput!) { ... }
mutation DeletePost($id: ID!) { ... }
mutation PublishArticle($id: ID!) { ... }
mutation ArchiveProject($id: ID!) { ... }
mutation AddItemToCart($input: AddItemInput!) { ... }
mutation RemoveTeamMember($teamId: ID!, $userId: ID!) { ... }
mutation FollowUser($userId: ID!) { ... }
mutation MarkNotificationAsRead($id: ID!) { ... }
```

### Operation Name Matches Server

Match client operation name to server mutation:

```graphql
# Server schema
type Mutation {
  createPost(input: CreatePostInput!): Post!
}

# Client operation - name reflects the action
mutation CreatePost($input: CreatePostInput!) {
  createPost(input: $input) {
    id
    title
  }
}
```

### Context-Specific Names

Add context when same mutation is used differently:

```graphql
# For creating a draft
mutation CreateDraftPost($input: CreatePostInput!) {
  createPost(input: $input) {
    id
    title
    status
  }
}

# For creating and publishing immediately
mutation CreateAndPublishPost($input: CreatePostInput!) {
  createPost(input: $input) {
    id
    title
    status
    publishedAt
  }
}
```

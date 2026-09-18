# Query Patterns

This reference covers patterns for writing effective GraphQL queries.

## Table of Contents

- [Query Structure](#query-structure)
- [Field Selection](#field-selection)
- [Aliases](#aliases)
- [Directives](#directives)
- [Query Naming](#query-naming)
- [Query Organization](#query-organization)
- [Performance Optimization](#performance-optimization)

## Query Structure

### Basic Query

```graphql
query GetUser($id: ID!) {
  user(id: $id) {
    id
    name
    email
  }
}
```

Components:

- `query` - Operation type
- `GetUser` - Operation name
- `($id: ID!)` - Variable definitions
- `user(id: $id)` - Field with argument
- `{ id name email }` - Selection set

### Query with Multiple Root Fields

```graphql
query GetDashboardData($userId: ID!) {
  user(id: $userId) {
    id
    name
  }
  notifications(first: 5) {
    id
    message
  }
  stats {
    totalPosts
    totalComments
  }
}
```

### Nested Queries

```graphql
query GetUserWithPosts($userId: ID!) {
  user(id: $userId) {
    id
    name
    posts(first: 10) {
      edges {
        node {
          id
          title
          comments(first: 3) {
            edges {
              node {
                id
                body
              }
            }
          }
        }
      }
    }
  }
}
```

## Field Selection

### Request Only Needed Fields

```graphql
# For a user card component
query GetUserCard($id: ID!) {
  user(id: $id) {
    id
    name
    avatarUrl
    # Don't request email, bio, etc. if not displayed
  }
}
```

### Always Include ID Fields

Include `id` for any type you might cache or refetch:

```graphql
query GetPost($id: ID!) {
  post(id: $id) {
    id # Always include for caching
    title
    author {
      id # Include for author cache entry
      name
    }
  }
}
```

### Selecting Connections

For paginated data, request what you need:

```graphql
query GetUserPosts($userId: ID!, $first: Int!, $after: String) {
  user(id: $userId) {
    id
    posts(first: $first, after: $after) {
      edges {
        node {
          id
          title
          excerpt
        }
        cursor # Only if implementing infinite scroll
      }
      pageInfo {
        hasNextPage
        endCursor
      }
      totalCount # Only if displaying total
    }
  }
}
```

## Aliases

### Basic Alias

Rename fields in the response:

```graphql
query GetUserNames($id: ID!) {
  user(id: $id) {
    userId: id
    displayName: name
  }
}

# Response: { user: { userId: "123", displayName: "John" } }
```

### Query Same Field Multiple Times

```graphql
query GetMultipleUsers {
  admin: user(id: "1") {
    id
    name
  }
  moderator: user(id: "2") {
    id
    name
  }
  currentUser: user(id: "3") {
    id
    name
  }
}
```

### Alias with Different Arguments

```graphql
query GetPostsByStatus($userId: ID!) {
  user(id: $userId) {
    id
    publishedPosts: posts(status: PUBLISHED, first: 5) {
      edges {
        node {
          id
          title
        }
      }
    }
    draftPosts: posts(status: DRAFT, first: 5) {
      edges {
        node {
          id
          title
        }
      }
    }
  }
}
```

## Directives

### @include Directive

Include field only if condition is true:

```graphql
query GetUser($id: ID!, $includeEmail: Boolean!) {
  user(id: $id) {
    id
    name
    email @include(if: $includeEmail)
  }
}

# Variables: { id: "123", includeEmail: true }
# Returns email field

# Variables: { id: "123", includeEmail: false }
# Does not return email field
```

### @skip Directive

Skip field if condition is true:

```graphql
query GetPost($id: ID!, $isPreview: Boolean!) {
  post(id: $id) {
    id
    title
    content @skip(if: $isPreview)
    excerpt
  }
}
```

### Directives on Fragments

```graphql
query GetUser($id: ID!, $expanded: Boolean!) {
  user(id: $id) {
    id
    name
    ...UserDetails @include(if: $expanded)
  }
}

fragment UserDetails on User {
  bio
  website
  socialLinks {
    platform
    url
  }
}
```

### Combining Directives

```graphql
query GetPost($id: ID!, $showComments: Boolean!, $hideAuthor: Boolean!) {
  post(id: $id) {
    id
    title
    author @skip(if: $hideAuthor) {
      id
      name
    }
    comments(first: 10) @include(if: $showComments) {
      edges {
        node {
          id
          body
        }
      }
    }
  }
}
```

## Query Naming

### Naming Conventions

| Purpose               | Pattern            | Examples                             |
| --------------------- | ------------------ | ------------------------------------ |
| Fetch single item     | `Get{Type}`        | `GetUser`, `GetPost`                 |
| Fetch list            | `List{Types}`      | `ListUsers`, `ListPosts`             |
| Search                | `Search{Types}`    | `SearchUsers`, `SearchProducts`      |
| Fetch for specific UI | `Get{Feature}Data` | `GetDashboardData`, `GetProfilePage` |

### Good Names

```graphql
query GetUserProfile($id: ID!) { ... }
query ListRecentPosts($first: Int!) { ... }
query SearchProducts($query: String!) { ... }
query GetOrderDetails($orderId: ID!) { ... }
query GetHomeFeed($userId: ID!) { ... }
```

### Avoid Generic Names

```graphql
# Avoid
query Data { ... }
query Query1 { ... }
query FetchStuff { ... }

# Prefer
query GetCurrentUser { ... }
query ListActiveProjects { ... }
query SearchCustomers($query: String!) { ... }
```

## Query Organization

### One Query Per File

```
src/
  graphql/
    queries/
      GetUser.graphql
      ListPosts.graphql
      SearchProducts.graphql
```

```graphql
# GetUser.graphql
query GetUser($id: ID!) {
  user(id: $id) {
    id
    name
    email
  }
}
```

### Colocate with Components

```
src/
  components/
    UserProfile/
      UserProfile.tsx
      UserProfile.graphql
      UserProfile.test.tsx
```

### Import and Use

```typescript
// With graphql-tag
import { gql } from "@apollo/client";

export const GET_USER = gql`
  query GetUser($id: ID!) {
    user(id: $id) {
      id
      name
    }
  }
`;

// With .graphql files (requires loader)
import { GetUserDocument } from "./UserProfile.generated";
```

## Performance Optimization

### Avoid Over-fetching

Only request fields used by your component:

```graphql
# For a list view - minimal fields
query ListPostsForIndex {
  posts(first: 20) {
    edges {
      node {
        id
        title
        excerpt
        author { name }
      }
    }
  }
}

# For detail view - more fields
query GetPostDetail($id: ID!) {
  post(id: $id) {
    id
    title
    content
    publishedAt
    author {
      id
      name
      bio
      avatarUrl
    }
    comments(first: 10) { ... }
  }
}
```

### Use Pagination

Never fetch unbounded lists:

```graphql
# Avoid
query GetAllPosts {
  posts {
    # Could return thousands
    id
    title
  }
}

# Prefer
query GetPosts($first: Int = 20, $after: String) {
  posts(first: $first, after: $after) {
    edges {
      node {
        id
        title
      }
    }
    pageInfo {
      hasNextPage
      endCursor
    }
  }
}
```

### Batch Related Queries

Fetch related data in one request:

```graphql
# Instead of multiple queries
query GetDashboard($userId: ID!) {
  user(id: $userId) {
    id
    name
  }
  recentPosts: posts(first: 5, orderBy: { field: CREATED_AT, direction: DESC }) {
    edges {
      node {
        id
        title
      }
    }
  }
  notifications(first: 10, unreadOnly: true) {
    edges {
      node {
        id
        message
      }
    }
  }
}
```

### Use Fragments for Repeated Selections

```graphql
query GetPostsWithAuthors {
  posts(first: 10) {
    edges {
      node {
        id
        title
        author {
          ...AuthorInfo
        }
      }
    }
  }
  featuredPost {
    id
    title
    author {
      ...AuthorInfo
    }
  }
}

fragment AuthorInfo on User {
  id
  name
  avatarUrl
}
```

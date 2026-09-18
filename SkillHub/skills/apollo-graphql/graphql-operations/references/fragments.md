# Fragment Patterns

This reference covers patterns for organizing and using GraphQL fragments effectively.

## Table of Contents

- [Fragment Basics](#fragment-basics)
- [Fragment Colocation](#fragment-colocation)
- [Fragment Reuse](#fragment-reuse)
- [Inline Fragments](#inline-fragments)
- [Type Conditions](#type-conditions)
- [Fragment Composition](#fragment-composition)
- [Anti-Patterns](#anti-patterns)

## Fragment Basics

### Defining Fragments

```graphql
fragment UserBasicInfo on User {
  id
  name
  avatarUrl
}
```

### Using Fragments

```graphql
query GetUser($id: ID!) {
  user(id: $id) {
    ...UserBasicInfo
    email
  }
}

fragment UserBasicInfo on User {
  id
  name
  avatarUrl
}
```

### Fragment Spread

The `...` operator spreads fragment fields:

```graphql
query GetPost($id: ID!) {
  post(id: $id) {
    id
    title
    author {
      ...UserBasicInfo # Spreads id, name, avatarUrl
    }
  }
}
```

## Fragment Colocation

### Colocate with Components

Keep fragments next to the components that use them:

```
src/
  components/
    UserAvatar/
      UserAvatar.tsx
      UserAvatar.fragment.graphql
    UserCard/
      UserCard.tsx
      UserCard.fragment.graphql
    PostList/
      PostList.tsx
      PostList.query.graphql
```

### Component Owns Its Data

```tsx
// UserAvatar.tsx
import { gql } from "@apollo/client";

export const USER_AVATAR_FRAGMENT = gql`
  fragment UserAvatar on User {
    id
    name
    avatarUrl
  }
`;

interface UserAvatarProps {
  user: UserAvatarFragment;
}

export function UserAvatar({ user }: UserAvatarProps) {
  return <img src={user.avatarUrl} alt={user.name} className="avatar" />;
}
```

### Parent Composes Fragments

```tsx
// UserCard.tsx
import { gql } from "@apollo/client";
import { USER_AVATAR_FRAGMENT, UserAvatar } from "./UserAvatar";

export const USER_CARD_FRAGMENT = gql`
  fragment UserCard on User {
    id
    name
    bio
    ...UserAvatar
  }
  ${USER_AVATAR_FRAGMENT}
`;

export function UserCard({ user }: { user: UserCardFragment }) {
  return (
    <div className="user-card">
      <UserAvatar user={user} />
      <h3>{user.name}</h3>
      <p>{user.bio}</p>
    </div>
  );
}
```

### Query Uses Component Fragments

```tsx
// UserProfile.tsx
import { gql, useQuery } from "@apollo/client";
import { USER_CARD_FRAGMENT, UserCard } from "./UserCard";

const GET_USER = gql`
  query GetUserProfile($id: ID!) {
    user(id: $id) {
      ...UserCard
      email
      createdAt
    }
  }
  ${USER_CARD_FRAGMENT}
`;

export function UserProfile({ userId }: { userId: string }) {
  const { data } = useQuery(GET_USER, { variables: { id: userId } });

  if (!data) return null;

  return (
    <div>
      <UserCard user={data.user} />
      <p>Email: {data.user.email}</p>
    </div>
  );
}
```

## Fragment Reuse

### Shared Fragments

For common patterns used across many components:

```graphql
# fragments/common.graphql

fragment Timestamps on Node {
  createdAt
  updatedAt
}

fragment PageInfoFields on PageInfo {
  hasNextPage
  hasPreviousPage
  startCursor
  endCursor
}
```

### Domain-Specific Fragments

```graphql
# fragments/user.graphql

fragment UserSummary on User {
  id
  name
  avatarUrl
}

fragment UserProfile on User {
  ...UserSummary
  bio
  location
  website
  socialLinks {
    platform
    url
  }
}

fragment UserWithStats on User {
  ...UserSummary
  followerCount
  followingCount
  postCount
}
```

### Using Shared Fragments

```graphql
query GetPost($id: ID!) {
  post(id: $id) {
    id
    title
    ...Timestamps
    author {
      ...UserSummary
    }
  }
}
```

## Inline Fragments

### Anonymous Inline Fragments

For grouping fields with directives:

```graphql
query GetUser($id: ID!, $includeDetails: Boolean!) {
  user(id: $id) {
    id
    name
    ... @include(if: $includeDetails) {
      email
      bio
      website
    }
  }
}
```

### Inline Fragments on Interfaces

```graphql
query GetNodes($ids: [ID!]!) {
  nodes(ids: $ids) {
    id
    ... on User {
      name
      email
    }
    ... on Post {
      title
      content
    }
  }
}
```

## Type Conditions

### Fragments on Union Types

```graphql
query Search($query: String!) {
  search(query: $query) {
    ... on User {
      id
      name
      avatarUrl
    }
    ... on Post {
      id
      title
      excerpt
    }
    ... on Comment {
      id
      body
      post {
        id
        title
      }
    }
  }
}
```

### Named Fragments for Unions

```graphql
query Search($query: String!) {
  search(query: $query) {
    ...SearchResultUser
    ...SearchResultPost
    ...SearchResultComment
  }
}

fragment SearchResultUser on User {
  id
  name
  avatarUrl
}

fragment SearchResultPost on Post {
  id
  title
  excerpt
  author {
    name
  }
}

fragment SearchResultComment on Comment {
  id
  body
  post {
    id
    title
  }
}
```

### Handling \_\_typename

```typescript
function SearchResult({ result }) {
  switch (result.__typename) {
    case 'User':
      return <UserResult user={result} />;
    case 'Post':
      return <PostResult post={result} />;
    case 'Comment':
      return <CommentResult comment={result} />;
  }
}
```

## Fragment Composition

### Building Up Fragments

```graphql
# Base fragment
fragment PostCore on Post {
  id
  title
  slug
}

# Extended fragment
fragment PostPreview on Post {
  ...PostCore
  excerpt
  featuredImage {
    url
  }
}

# Full fragment
fragment PostFull on Post {
  ...PostPreview
  content
  publishedAt
  author {
    ...UserSummary
  }
  tags {
    id
    name
  }
}
```

### Fragments in Fragments

```graphql
fragment CommentWithAuthor on Comment {
  id
  body
  createdAt
  author {
    ...UserSummary
  }
}

fragment PostWithComments on Post {
  id
  title
  comments(first: 10) {
    edges {
      node {
        ...CommentWithAuthor
      }
    }
  }
}
```

### Fragment Spread Order

Order doesn't matter - fields are merged:

```graphql
query GetUser($id: ID!) {
  user(id: $id) {
    ...UserProfile
    ...UserStats
    # Both fragments' fields are included
  }
}
```

## Anti-Patterns

### Avoid Giant Fragments

```graphql
# Bad: Too many fields, not all needed everywhere
fragment UserEverything on User {
  id
  name
  email
  bio
  avatarUrl
  coverImage
  website
  location
  socialLinks { ... }
  posts { ... }
  followers { ... }
  following { ... }
  # ... 50 more fields
}

# Good: Focused fragments for specific uses
fragment UserAvatar on User {
  id
  name
  avatarUrl
}

fragment UserProfile on User {
  id
  name
  bio
  avatarUrl
  website
  location
}
```

### Avoid Unused Fragment Fields

```graphql
# Bad: Component only uses name and avatarUrl
fragment UserInfo on User {
  id
  name
  email # unused
  avatarUrl
  bio # unused
  website # unused
}

# Good: Only request what's needed
fragment UserInfo on User {
  id
  name
  avatarUrl
}
```

### Avoid Deeply Nested Fragments

```graphql
# Bad: Hard to understand what's being fetched
fragment Level1 on User {
  ...Level2
}
fragment Level2 on User {
  ...Level3
}
fragment Level3 on User {
  ...Level4
}
# ... continues

# Good: Keep nesting shallow
fragment UserWithPosts on User {
  id
  name
  posts {
    ...PostPreview
  }
}
```

### Avoid Circular Fragment Dependencies

```graphql
# Bad: Circular reference (won't work)
fragment UserWithPosts on User {
  posts {
    ...PostWithAuthor
  }
}

fragment PostWithAuthor on Post {
  author {
    ...UserWithPosts # Circular!
  }
}

# Good: Break the cycle
fragment UserWithPosts on User {
  posts {
    ...PostPreview
  }
}

fragment PostWithAuthor on Post {
  author {
    ...UserSummary # Different fragment, no cycle
  }
}
```

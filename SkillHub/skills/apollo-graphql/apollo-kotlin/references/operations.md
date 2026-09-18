# Operations

This reference covers queries, mutations, subscriptions, and response handling.

## GraphQL files

- Place your operations in `.graphql` files under `src/main/graphql/` (or `src/commonMain/graphql/` for multiplatform).
- Name the operations with a prefix indicating their type, e.g., `GetUserQuery`, `UpdateUserMutation`, `OnMessageReceivedSubscription`.
- Keep one operation per `.graphql` file, and name it with the operation name, e.g. `GetUserQuery.graphql` for `GetUserQuery`.
- Fragments can stay in the same file as the operation, or be in separate files if used across multiple operations.

## Queries and Mutations

Use generated query classes and call them with `.execute()`.

```kotlin
suspend fun loadUser(id: String): User {
  val response = apolloClient.query(GetUserQuery(id)).execute()
  val data = response.dataOrThrow()
  return data.user.toDomain()
}
```

## Subscriptions

- For subscriptions, never use `.execute()` which can only accept one emission, instead use `toFlow()`.

```kotlin
fun observeMessages() {
  apolloClient.subscription(GetMessagesSubscription()).toFlow().collect { response ->
    val messages = response.dataOrThrow().messages
    // Update UI
  }
}
```

## Error handling

- Local (e.g. network, http, parsing, ...) errors are in `response.exception`.
- Errors from the server that are returned in the GraphQL response are in `response.errors`.
- Some `data` may be present even if there are `errors`, but `data` will be null if `exception` is present.

## Ground rules

- Only select fields that are needed for the UI or app's logic.

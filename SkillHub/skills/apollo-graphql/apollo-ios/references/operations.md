# Operations

This reference covers queries, mutations, watchers, cache policies, error handling, and SwiftUI `@Observable` view-model patterns.

Apollo iOS v2 uses async/await and typed cache policies. Every operation returns a `GraphQLResponse<Operation>` that carries `data`, `errors`, and `source` (cache vs server).

## Write operations in `.graphql` files

Operations live in `.graphql` files inside a path listed in `input.operationSearchPaths` of `apollo-codegen-config.json`. Name each file after the operation it contains and include the operation name explicitly so the generated type is predictable.

```graphql
# GetUserQuery.graphql
query GetUser($id: ID!) {
  user(id: $id) {
    id
    name
    email
  }
}
```

Keep one operation per file. Co-locate fragments that are specific to an operation; put shared fragments in their own `.graphql` file.

After editing a `.graphql` file, regenerate Swift types:

```bash
./apollo-ios-cli generate
```

## Queries

`ApolloClient.fetch(query:cachePolicy:)` returns a single `GraphQLResponse<Query>` when the cache policy produces one response, and an `AsyncThrowingStream` when it produces more than one.

### Single response — `cacheFirst` (default), `networkFirst`, or `networkOnly`

```swift
import Apollo

func loadUser(id: String) async throws -> GetUserQuery.Data.User? {
  let response = try await apolloClient.fetch(
    query: GetUserQuery(id: id),
    cachePolicy: .cacheFirst
  )
  if let firstError = response.errors?.first {
    // `GraphQLError` conforms to `Error`, so it can be thrown directly.
    // Inspect `response.errors` for all of them if you need the full list.
    throw firstError
  }
  return response.data?.user
}
```

### Two responses — `cacheAndNetwork`

Returns cached data first (if any), then the network result. Use this when a view should render quickly from cache and then refresh.

```swift
func streamUser(id: String) throws -> AsyncThrowingStream<GraphQLResponse<GetUserQuery>, any Error> {
  try apolloClient.fetch(query: GetUserQuery(id: id), cachePolicy: .cacheAndNetwork)
}
```

### Cache-only — `cacheOnly`

Returns `GraphQLResponse<Query>?` — `nil` if the cache has no data.

```swift
let cached = try await apolloClient.fetch(query: GetUserQuery(id: id), cachePolicy: .cacheOnly)
```

## Cache policies

| Policy | Enum case | Return type | When to use |
|---|---|---|---|
| Cache first | `CachePolicy.Query.SingleResponse.cacheFirst` | `GraphQLResponse<Query>` | Default. Serve cache hits instantly; fall back to network on miss. |
| Network first | `CachePolicy.Query.SingleResponse.networkFirst` | `GraphQLResponse<Query>` | Correctness-critical reads (e.g. a checkout page). |
| Network only | `CachePolicy.Query.SingleResponse.networkOnly` | `GraphQLResponse<Query>` | Pull-to-refresh, or when cache is known stale. |
| Cache only | `CachePolicy.Query.CacheOnly.cacheOnly` | `GraphQLResponse<Query>?` | Offline reads, or checking what's already in cache. |
| Cache + network | `CachePolicy.Query.CacheAndNetwork.cacheAndNetwork` | `AsyncThrowingStream<GraphQLResponse<Query>, Error>` | Show cached UI instantly, then update once network returns. |

**Note:** The legacy `CachePolicy_v1` enum (`returnCacheDataElseFetch`, `fetchIgnoringCacheData`, etc.) is deprecated. Use the typed `CachePolicy.Query.*` variants shown above.

## Mutations

`perform(mutation:)` always hits the network (mutations have no cache policy). The return value is a `GraphQLResponse<Mutation>`.

```swift
func updateUserName(id: String, name: String) async throws {
  let response = try await apolloClient.perform(
    mutation: UpdateUserNameMutation(id: id, name: name)
  )
  if let firstError = response.errors?.first {
    throw firstError
  }
}
```

When the mutation's selection set matches the shape of cached records, the cache updates automatically. For optimistic UI or cross-entity updates, see [caching.md](caching.md#manual-cache-readswrites).

## Watchers

`watch(query:cachePolicy:resultHandler:)` returns a `GraphQLQueryWatcher<Query>` that fires the handler every time the matched records in the cache change. **Watchers are the reactive primitive for SwiftUI** — use them instead of polling.

The handler is a closure, not an `AsyncSequence`:

```swift
public typealias ResultHandler = @Sendable (Result<GraphQLResponse<Query>, any Swift.Error>) -> Void
```

### Bridging a watcher to an `@State` variable for SwiftUI

Store the watcher for the lifetime of the view and tear it down on cancellation:

```swift
import Apollo

@Observable
@MainActor
final class UserViewModel {
  var user: GetUserQuery.Data.User?
  var errorMessage: String?

  private let apolloClient: ApolloClient
  private var watcher: GraphQLQueryWatcher<GetUserQuery>?

  init(apolloClient: ApolloClient) { self.apolloClient = apolloClient }

  func start(userID: String) async {
    cancel()
    watcher = await apolloClient.watch(
      query: GetUserQuery(id: userID),
      cachePolicy: .cacheFirst
    ) { [weak self] result in
      Task { @MainActor in
        guard let self else { return }
        switch result {
        case .success(let response):
          self.user = response.data?.user
          self.errorMessage = response.errors?.first?.message
        case .failure(let error):
          self.errorMessage = error.localizedDescription
        }
      }
    }
  }

  func cancel() {
    watcher?.cancel()
    watcher = nil
  }

  deinit { watcher?.cancel() }
}
```

### Consuming from a SwiftUI view

```swift
struct UserDetailView: View {
  let userID: String
  @State private var viewModel: UserViewModel

  init(userID: String, apolloClient: ApolloClient) {
    self.userID = userID
    _viewModel = State(initialValue: UserViewModel(apolloClient: apolloClient))
  }

  var body: some View {
    Group {
      if let user = viewModel.user {
        Text(user.name)
      } else if let message = viewModel.errorMessage {
        Text(message).foregroundStyle(.red)
      } else {
        ProgressView()
      }
    }
    .task(id: userID) {
      await viewModel.start(userID: userID)
    }
    .onDisappear {
      viewModel.cancel()
    }
  }
}
```

Use `.task(id:)` so the watcher restarts whenever `userID` changes. `.task` cancels automatically when the view disappears, but watchers require an explicit `cancel()` because they are not bound to a Swift `Task`.

## Error handling

A network response can succeed (no thrown error) while still containing GraphQL errors in `response.errors`. Always check both.

```swift
let response = try await apolloClient.fetch(query: GetUserQuery(id: id))

// `response.errors` is `[GraphQLError]?`. Each `GraphQLError` conforms to
// `Error` and carries `.message`, `.locations`, `.path`, and `.extensions`.
// `response.data` may still contain partial data when there are errors.
if let firstError = response.errors?.first {
  throw firstError
}

guard let user = response.data?.user else {
  // No user was returned but no errors either — treat as not found.
  throw UserNotFound()
}
```

If you need to propagate *all* GraphQL errors (not just the first) and don't want to lose the rest, wrap them in an app-owned error type — for example:

```swift
enum APIError: Error {
  case graphQL([GraphQLError])
}

if let errors = response.errors, !errors.isEmpty {
  throw APIError.graphQL(errors)
}
```

`APIError` here is an app-level type you define and name to match your codebase — it is **not** provided by Apollo iOS. Apollo iOS ships only the singular `GraphQLError`; any aggregation wrapper is yours to design.

Errors that *prevent* a response entirely (network failures, cancellations, parsing errors) are thrown from `fetch` / `perform` / `subscribe` and surface as `Swift.Error`. Check specifically for `CancellationError` when an async `Task` is cancelled.

`response.source` tells you where data came from — `.cache` or `.server`. Useful for analytics or deciding whether to trigger a refresh.

## Ground rules

- Use `.task { }` / `.task(id:)` to scope fetch `Task`s to view lifetime so they cancel automatically.
- Cancel watchers explicitly; they are not bound to a `Task`.
- Create view models as `@MainActor @Observable` classes and hand them the `ApolloClient` at init. Do not fetch from inside `body`.
- Only select fields the UI actually uses. Every extra field is a larger cache record and a larger payload.
- Treat `response.errors` as data, not an exception. Partial responses are common in federated schemas.
- Never share a `GraphQLQueryWatcher` across views; each view owns its own watcher.

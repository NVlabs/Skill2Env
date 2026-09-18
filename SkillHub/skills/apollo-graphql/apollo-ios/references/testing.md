# Testing

Apollo iOS emits two distinct sets of testing affordances:

1. **`ApolloTestSupport`** — a public target shipped with the SDK. Use it to construct strongly-typed `Mock<Type>` fixtures for any object in your schema, and to wire those mocks into a `ApolloClient` via a fake network transport.
2. **Generated test mocks** — emitted alongside your schema types when `output.testMocks` is set to `swiftPackage` or `absolute` in `apollo-codegen-config.json`. These are the schema-specific counterparts to `Mock<Type>`.

This reference covers both, plus the recommended architecture for making view models testable without a real GraphQL server.

## Enable test mocks

Test-mock generation is **off by default** in the canonical setup ([setup.md](setup.md#generate-apollo-codegen-configjson) ships `testMocks: { "none": {} }`). The first time you write a test that uses `Mock<Type>`, flip the config to emit them, regenerate, and link the produced target.

### 1. Flip `output.testMocks` in `apollo-codegen-config.json`

For a project using `moduleType: swiftPackage` (the canonical default):

```json
"output": {
  "testMocks": {
    "swiftPackage": { "targetName": "MyAPITestMocks" }
  }
}
```

For a project using `moduleType: embeddedInTarget` or `other`, pick a location for the mocks yourself:

```json
"testMocks": {
  "absolute": { "path": "./MyAppTests/Mocks" }
}
```

### 2. Regenerate

```bash
./apollo-ios-cli generate
```

Commit the newly generated `MyAPITestMocks` files (or the files at the `absolute` path) alongside the config change.

### 3. Link the mocks target — see the next section.

## Link `ApolloTestSupport` to your test target

Add the dependency to your test target only:

```swift
// Package.swift
.testTarget(
  name: "MyAppTests",
  dependencies: [
    "MyApp",
    .product(name: "ApolloTestSupport", package: "apollo-ios"),
    // If you used `testMocks.swiftPackage`, add the generated mocks package too:
    .product(name: "MyAPITestMocks", package: "MyAPI"),
  ]
),
```

## Build test fixtures with `Mock<Type>`

A generated operation's `Data` is always rooted at the schema's root type (typically `Query` for queries, `Mutation` for mutations). To build a fixture:

1. Mock each nested entity in the response tree.
2. Mock the root type (`Query`/`Mutation`) and wire the nested mocks in as field values.
3. Call `<Operation>.Data.from(rootMock)` to coerce the root mock into the operation's `Data` type. This helper is `async`.

```swift
import ApolloTestSupport
import MyAPITestMocks
import Testing

@Test
func viewModelDisplaysUser() async throws {
  // 1. Leaf entity mock.
  let mockUser = Mock<User>(
    id: "user-1",
    name: "Ada Lovelace",
    email: "ada@example.com"
  )

  // 2. Root `Query` mock with the leaf mock attached to the `user` field.
  let mockQuery = Mock<Query>(user: mockUser)

  // 3. Coerce into a real `GetUserQuery.Data`. `.from(_:)` is async.
  let data = await GetUserQuery.Data.from(mockQuery)

  #expect(data.user?.name == "Ada Lovelace")
}
```

Codegen emits a `convenience init` on each `Mock<SchemaType>` with keyword arguments for every field on that type, so you can build deep fixtures concisely. For partial overrides, you can also use the `@dynamicMemberLookup` setters (`mockUser.name = "…"`) after calling `Mock<User>()`.

For mutations, mock the root `Mutation` type and feed it into `<Mutation>.Data.from(_:)`. The same rule applies — root first, leaves attached.

## Testability architecture — wrap `ApolloClient`

There is no public `MockNetworkTransport` or `MockApolloClient` in the SDK. The cleanest way to make view models testable is to **wrap `ApolloClient` in a protocol your app owns**, then mock the protocol in tests.

```swift
// In the app target:
protocol GraphQLService: Sendable {
  func getUser(id: String) async throws -> GetUserQuery.Data.User?
}

final class ApolloGraphQLService: GraphQLService {
  private let client: ApolloClient
  init(client: ApolloClient) { self.client = client }

  func getUser(id: String) async throws -> GetUserQuery.Data.User? {
    let response = try await client.fetch(query: GetUserQuery(id: id))
    if let firstError = response.errors?.first { throw firstError }
    return response.data?.user
  }
}
```

In tests, conform a fake type to `GraphQLService` and return mocks:

```swift
import ApolloTestSupport
import MyAPITestMocks

// `GraphQLService: Sendable`, so `FakeGraphQLService` must also be Sendable.
// Under Swift 6 strict concurrency that means stored properties must be `let` —
// inject the canned response at init time rather than mutating it after
// construction.
final class FakeGraphQLService: GraphQLService {
  let userToReturn: GetUserQuery.Data.User?
  init(userToReturn: GetUserQuery.Data.User?) { self.userToReturn = userToReturn }
  func getUser(id: String) async throws -> GetUserQuery.Data.User? { userToReturn }
}

@Test
func viewModelLoadsUser() async throws {
  // Build the fixture root-first (Mock<Query> with the User attached),
  // convert to the operation's Data, then hand the nested user field
  // back to the fake service.
  let mockUser = Mock<User>(id: "1", name: "Grace Hopper")
  let data = await GetUserQuery.Data.from(Mock<Query>(user: mockUser))

  let service = FakeGraphQLService(userToReturn: data.user)

  let viewModel = UserViewModel(service: service)
  await viewModel.load(userID: "1")

  #expect(viewModel.userName == "Grace Hopper")
}
```

This keeps Apollo-specific types contained to one boundary; the rest of the app tests against plain Swift.

## Integration-testing against a fake server

If you want to test the `ApolloClient` itself (interceptor wiring, cache behavior, response parsing), use a custom `NetworkTransport` that returns canned GraphQL responses.

A minimal pattern:

```swift
import Apollo
import ApolloAPI

final class CannedNetworkTransport: NetworkTransport, Sendable {
  let queryResponses: [String: String]  // operationName → JSON response body

  init(queryResponses: [String: String]) { self.queryResponses = queryResponses }

  func send<Query: GraphQLQuery>(
    query: Query,
    fetchBehavior: FetchBehavior,
    requestConfiguration: RequestConfiguration
  ) throws -> AsyncThrowingStream<GraphQLResponse<Query>, any Error> {
    return AsyncThrowingStream { continuation in
      guard let json = queryResponses[Query.operationName],
            let data = json.data(using: .utf8) else {
        continuation.finish(throwing: TestError.notConfigured)
        return
      }
      // Parse `data` into a GraphQLResponse<Query> using ApolloAPI decoders,
      // then yield and finish. The exact conversion helpers live in ApolloAPI.
      // For most tests, prefer the protocol-based FakeGraphQLService above —
      // this level of detail is only needed when testing Apollo itself.
      _ = data
      continuation.finish(throwing: TestError.notImplemented)
    }
  }

  func send<Mutation: GraphQLMutation>(
    mutation: Mutation,
    requestConfiguration: RequestConfiguration
  ) throws -> AsyncThrowingStream<GraphQLResponse<Mutation>, any Error> {
    throw TestError.notImplemented
  }

  enum TestError: Error { case notConfigured, notImplemented }
}
```

In practice, the overhead of building a fake `NetworkTransport` usually outweighs the benefit. **Prefer the protocol-wrapper pattern above** for view-model tests, and reserve custom transports for the rare cases where you need to test Apollo-specific behavior (cache writes, interceptors, subscription multipart parsing).

## Testing watchers

Watchers fire the result handler whenever the relevant cache records change. To test watcher behavior deterministically:

1. Build a test `ApolloStore` with `InMemoryNormalizedCache`.
2. Write fixture data to the cache with `withinReadWriteTransaction`.
3. Call `client.watch(…)` and assert the handler fires with the expected values.
4. Trigger an update with another `withinReadWriteTransaction` and assert the handler fires again.

```swift
@Test
@MainActor
func watcherReactsToCacheUpdate() async throws {
  let store = ApolloStore()
  // ... build an ApolloClient with a transport that never actually hits the network ...

  var received: [String] = []
  let watcher = await client.watch(query: GetUserQuery(id: "1")) { result in
    if case let .success(response) = result, let name = response.data?.user?.name {
      Task { @MainActor in received.append(name) }
    }
  }

  let beforeData = await GetUserQuery.Data.from(
    Mock<Query>(user: Mock<User>(id: "1", name: "Before"))
  )
  try await store.withinReadWriteTransaction { tx in
    try tx.write(data: beforeData, for: GetUserQuery(id: "1"))
  }
  try await Task.sleep(for: .milliseconds(50))

  let afterData = await GetUserQuery.Data.from(
    Mock<Query>(user: Mock<User>(id: "1", name: "After"))
  )
  try await store.withinReadWriteTransaction { tx in
    try tx.write(data: afterData, for: GetUserQuery(id: "1"))
  }
  try await Task.sleep(for: .milliseconds(50))

  #expect(received == ["Before", "After"])
  watcher.cancel()
}
```

## Ground rules

- **Wrap `ApolloClient` in an app-owned protocol**; test view models against the protocol. Keep Apollo-specific types behind that boundary.
- Never hit the real network in unit tests. If you must exercise `ApolloClient` itself, use a fake `NetworkTransport`.
- Keep `output.testMocks: { "none": {} }` until the first test that needs `Mock<Type>` is being written, then flip it on and regenerate. Generating mocks early wastes time and bloats the module for no benefit.
- Do not share `Mock<Type>` instances across tests. Build a fresh mock per test to avoid state bleed.
- Test watcher behavior by directly manipulating the `ApolloStore` in `withinReadWriteTransaction`, not by sending real network responses.
- Prefer Swift Testing (`@Test`, `#expect`) for new tests; XCTest also works with the same patterns.

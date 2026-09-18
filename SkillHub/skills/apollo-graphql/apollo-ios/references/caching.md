# Caching

Apollo iOS ships a normalized cache: records are keyed by object identity so multiple queries that reference the same entity share storage. When a mutation or new fetch updates a record, every watcher that depends on it is notified automatically.

This reference covers store selection, cache keys (declarative `@typePolicy` directives and programmatic fallback), watching, manual reads/writes, and clearing.

## Choose a store

The `ApolloStore` is backed by a `NormalizedCache`. Two implementations ship with the SDK:

### In-memory cache (default)

```swift
import Apollo

let store = ApolloStore()
// Equivalent to:
// let store = ApolloStore(cache: InMemoryNormalizedCache())
```

Lost on app termination. Good for data that doesn't need to persist (search results, transient UI).

### SQLite cache (persistent)

```swift
import Apollo
import ApolloSQLite

let cacheURL = try FileManager.default
  .url(for: .cachesDirectory, in: .userDomainMask, appropriateFor: nil, create: true)
  .appendingPathComponent("apollo_cache.sqlite")

let cache = try SQLiteNormalizedCache(fileURL: cacheURL)
let store = ApolloStore(cache: cache)
```

Persists across launches. Prefer `.cachesDirectory` (not `.documentDirectory`) so the OS can evict the file under storage pressure.

Pass the store to `ApolloClient` and to `RequestChainNetworkTransport` / `WebSocketTransport` when you build a custom transport (see [setup.md](setup.md)).

## Cache keys — prefer `@typePolicy`

For the cache to deduplicate records across queries, the SDK has to know which field identifies each object. Declare this **declaratively** with the `@typePolicy` schema directive.

### Declare cache keys in a schema extension file

Create a new `.graphqls` file (for example `cacheKeys.graphqls`) and include it in `input.schemaSearchPaths` in `apollo-codegen-config.json`.

```graphql
# cacheKeys.graphqls
extend type User @typePolicy(keyFields: "id")
extend type Book @typePolicy(keyFields: "isbn")
extend type Author @typePolicy(keyFields: "firstName lastName")
```

- Single field: `keyFields: "id"`
- Composite key: space-separate the fields (`keyFields: "firstName lastName"`)
- One `@typePolicy` per type you want deduplicated.

Regenerate after editing:

```bash
./apollo-ios-cli generate
```

See the official [Cache Key Resolution](https://www.apollographql.com/docs/ios/caching/cache-key-resolution) page for the full directive reference.

## `@fieldPolicy` — cache resolution for fields with arguments

`@typePolicy` tells the cache how to identify an _object_. `@fieldPolicy` tells the cache how to resolve a _field call with arguments_ to a cache record. Use them together.

The motivating problem: with only `@typePolicy(keyFields: "id")` on `User`, calling `client.fetch(query: GetUserQuery(id: "42"))` always hits the network even when a previous query already populated `User:42` in the cache. The cache stores the user record, but it has no way to know that the operation `user(id: "42")` should resolve to it. `@fieldPolicy` closes that gap.

Declare it on the type that owns the field (typically `Query`) in the same schema extension file used for `@typePolicy`:

```graphql
# cacheKeys.graphqls
extend type User @typePolicy(keyFields: "id")

extend type Query
  @fieldPolicy(forField: "user", keyArgs: "id")
  @fieldPolicy(forField: "book", keyArgs: "isbn")
```

Now `client.fetch(query: GetUserQuery(id: "42"), cachePolicy: .cacheFirst)` returns the cached `User:42` record without a network round-trip. The same applies to `cacheOnly` reads — they succeed against fields the app has never directly fetched, as long as the underlying object exists in the cache.

`keyArgs` is space-delimited and order-significant — argument order in the string determines the structure of the generated cache key:

```graphql
# Multi-argument field — resolves to one cache record per (species, habitat) pair.
extend type Query @fieldPolicy(forField: "allAnimals", keyArgs: "species habitat")
```

A field can have multiple `@fieldPolicy` directives stacked when the same query type owns multiple resolvable fields. Add them as you ship features that benefit from cache deduplication — there is no cost to declaring more.

**When to use which:**

| Goal | Directive |
|---|---|
| Identify a cached object by its own fields | `@typePolicy(keyFields: ...)` on the object type |
| Resolve a query field's arguments to that cached object | `@fieldPolicy(forField: ..., keyArgs: ...)` on the parent type |
| Cache-key a parameterized collection (e.g., `allAnimals(species:, habitat:)`) | `@fieldPolicy(forField: ..., keyArgs: ...)` on `Query` |

## Programmatic cache keys (advanced fallback)

Use programmatic keys only when `@typePolicy` cannot express what you need — for example, keys derived from nested fields, or interface types that key differently per concrete type.

Apollo iOS generates a `SchemaConfiguration.swift` stub inside your schema module. Edit the `cacheKeyInfo(for:object:)` method:

```swift
import ApolloAPI

public enum SchemaConfiguration: SchemaConfiguration_Compat {
  public static func cacheKeyInfo(
    for type: Object,
    object: ObjectData
  ) -> CacheKeyInfo? {
    switch type {
    case Objects.User:
      guard let id = object["id"] as? String else { return nil }
      return CacheKeyInfo(id: id)

    case Objects.Comment:
      // Composite key derived from author + timestamp.
      guard let authorID = (object["author"] as? ObjectData)?["id"] as? String,
            let createdAt = object["createdAt"] as? String else {
        return nil
      }
      return CacheKeyInfo(id: "\(authorID)_\(createdAt)")

    default:
      return nil
    }
  }
}
```

See the [Programmatic Cache Keys](https://www.apollographql.com/docs/ios/caching/programmatic-cache-keys) documentation for the full API.

## Watching the cache

`client.watch(query:resultHandler:)` fires every time records relevant to the query change — whether from a fetch, a mutation response, or a manual cache write. Use watchers as the reactive primitive for SwiftUI views. See [operations.md](operations.md#watchers) for the canonical `@Observable` view-model pattern.

When a mutation returns a response whose selection set matches existing cached records (same types, same cache keys, same requested fields), the cache is updated automatically. For anything else — inserting into a list, removing an item, optimistic UI — update the cache manually.

## Manual cache reads/writes

The `ApolloStore` exposes transactional read/write access. Always run writes inside `withinReadWriteTransaction` to avoid partial updates.

### Read

```swift
let data = try await apolloClient.store.withinReadTransaction { tx in
  try await tx.read(query: GetUserQuery(id: id))
}
```

### Write after a successful mutation (optimistic UI + confirmation)

```swift
func addTodo(_ title: String) async throws {
  // 1. Optimistic local write — UI updates immediately via watchers.
  try await apolloClient.store.withinReadWriteTransaction { tx in
    try await tx.update(query: GetTodosQuery()) { data in
      data.todos.append(
        GetTodosQuery.Data.Todo(
          _dataDict: .init(
            data: ["__typename": "Todo", "id": "temp", "title": title, "completed": false],
            fulfilledFragments: []
          )
        )
      )
    }
  }

  // 2. Perform the mutation; its response will update the cache with the real record.
  _ = try await apolloClient.perform(mutation: AddTodoMutation(title: title))
}
```

Exact method names on the transaction:

- `read(query:)` — read a full query's data from the cache.
- `update(query:)` / `updateObject(ofType:withKey:)` — mutate a cache entry and publish.
- `write(data:for:)` / `write(selectionSet:withKey:)` — overwrite a cache entry.

See `ApolloStore.ReadTransaction` and `ApolloStore.ReadWriteTransaction` in the SDK source for the full signatures.

## Clear the cache

On logout, or any time you need a clean slate:

```swift
try await apolloClient.clearCache()
```

This clears the entire normalized cache. For finer-grained clears (single record, single type), use `withinReadWriteTransaction` and remove or overwrite the relevant records.

## Ground rules

- Declare `@typePolicy` for every type you want deduplicated in the cache. This is the recommended default.
- Pair `@typePolicy` with `@fieldPolicy` on argument-bearing query fields (`Query.user(id:)`, `Query.book(isbn:)`, etc.) so cache reads can resolve to the deduplicated record without going through the network.
- Only drop to programmatic `cacheKeyInfo` when neither `@typePolicy` nor `@fieldPolicy` can express the key.
- Always wrap cache writes in `withinReadWriteTransaction` — concurrent writes without a transaction corrupt state.
- Never access the raw cache (`InMemoryNormalizedCache` / `SQLiteNormalizedCache`) directly. Always go through `ApolloStore`.
- Clear the cache on logout so the next user doesn't see cached data from the previous session.
- When adding a new type to your schema, add a `@typePolicy` entry in the same PR. Adding it later is trivial; noticing the deduplication bug in production is painful.

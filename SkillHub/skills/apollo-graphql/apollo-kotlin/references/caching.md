# Caching

This reference covers normalized cache setup and cache policies.

## When to use normalized cache

Use a normalized cache when:

- You need offline support or fast startup.
- Multiple screens depend on the same objects.
- You want consistent updates after mutations.

## Setup

- Always use the new Normalized Cache (`com.apollographql.cache:*`) rather than the classic one (`com.apollographql.apollo:*`)
- Always use the latest version
- To determine the latest version, execute `scripts/list-apollo-kotlin-normalized-cache-versions.sh` and pick the latest release

1. Add normalized cache dependencies:

```kotlin
implementation("com.apollographql.cache:normalized-cache:LATEST_CACHE_VERSION") // Memory cache
implementation("com.apollographql.cache:normalized-cache-sqlite:LATEST_CACHE_VERSION") // Disk cache
```

2. Configure the cache Apollo Compiler plugin:

```kotlin
apollo {
  service("service") {
    // Other configurations...

    plugin("com.apollographql.cache:normalized-cache-apollo-compiler-plugin:LATEST_CACHE_VERSION") {
      argument("com.apollographql.cache.packageName", packageName.get())
    }
  }
}
```

3. Configure the cache in `ApolloClient`:

```kotlin
val apolloClient = ApolloClient.Builder()
  .serverUrl("https://your.domain/graphql")
  .cache(MemoryCacheFactory()) // or SqlNormalizedCacheFactory() for disk cache
  .build()
```

Don't forget to add the necessary imports:

```kotlin
// For the generated `cache` extension function, use <the package configured in the apollo configuration in build.gradle.kts>.cache.Cache.cache
// E.g.
import com.example.graphql.cache.Cache.cache

// For MemoryCacheFactory
import com.apollographql.cache.normalized.memory.MemoryCacheFactory

// For SqlNormalizedCacheFactory
import com.apollographql.cache.normalized.sql.SqlNormalizedCacheFactory
```

## Cache keys

For the normalized cache to work efficiently, always specify the cache keys of your types with the `@typePolicy` directive. 

Use it in an `extra.graphqls` file next to the `schema.graphqls` file:

```graphql
# The directives must be imported
extend schema
@link(
  url: "https://specs.apollo.dev/kotlin_labs/v0.5",
  import: ["@typePolicy", "@fieldPolicy"]
)

extend type User @typePolicy(keyFields: "id")
```

When objects can be returned by fields that takes their cache keys as argument, declare it like so:

```graphql
extend type Query @fieldPolicy(forField: "user", keyArgs: "id")
```

## Watching the cache

- Use the cache as the single source of truth for the UI.

```kotlin
apolloClient.query(GetUserQuery(id))
  .watch()
  .collect { response ->
    // This will be triggered whenever any fields used by GetUserQuery are updated in the cache
    val data = response.dataOrThrow()
    // Update UI with data
  }
```

## Cache policies

The default cache policy is `CacheFirst`. It can be configured per query:

```kotlin
val response = apolloClient.query(GetUserQuery(id))
  .fetchPolicy(FetchPolicy.NetworkOnly)
  .execute()
```

The available policies are:
- `CacheFirst`: Try cache first, then network.
- `CacheOnly`: Always fetch from cache.
- `NetworkOnly`: Always fetch from network.
- `NetworkFirst`: Try network first, then cache.
- `CacheAndNetwork`: Fetch from cache first, then always fetch from network and update cache.

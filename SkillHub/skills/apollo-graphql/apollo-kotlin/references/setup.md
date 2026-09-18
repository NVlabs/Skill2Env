# Setup

Use this guide to setup Apollo Kotlin and configure code generation and schema downloads.

## Gradle

- Prefer Apollo Kotlin 5, do not use v3 or older versions
- Always use the latest version
- To determine the latest version, execute `scripts/list-apollo-kotlin-versions.sh` and pick the latest release

Add the Apollo Kotlin Gradle plugin:

```kotlin
plugins {
  // Other Gradle plugins, including Android and Kotlin
  // ...

  // Apollo Kotlin Gradle plugin
  id("com.apollographql.apollo").version("LATEST_APOLLO_VERSION")
}
```

Add the runtime dependency:

```kotlin
dependencies {
  // Other dependencies
  // ...

  // Apollo runtime
  implementation("com.apollographql.apollo:apollo-runtime") // Note: no need to specify version here because the plugin will manage it
}
```

## Service configuration

Define a service (one per GraphQL endpoint if multiple are needed).

```kotlin
apollo {
  service("service") {
    packageName.set("com.example.graphql")
  }
}
```

## Custom scalars

Map custom scalars to Kotlin types and adapters.

```kotlin
apollo {
  service("service") {
    // ...
    mapScalar("GeoPoint", "com.example.graphql.GeoPoint", "com.example.graphql.GeoPointAdapter")
  }
}
```

Some commonly used scalars adapters are available in this library: https://github.com/apollographql/apollo-kotlin-adapters. Use it to avoid writing your own adapters for common types like `BigDecimal`, `Instant`. etc.

## Schema management

Prefer a checked-in schema file so builds are reproducible.

Configure introspection schema download:

```kotlin
apollo {
  service("service") {
    // ...
    introspection {
      endpointUrl.set("https://your.domain/graphql")
      schemaFile.set(file("src/main/graphql/schema.graphqls"))
    }
  }
}
```
This creates a task `downloadServiceApolloSchemaFromIntrospection` that downloads the schema and saves it to the specified location.

Run it before writing operations:

```bash
./gradlew downloadServiceApolloSchemaFromIntrospection
```

## Multi-module

If multiple modules are desirable, a few rules apply:
- One and only one module can contain the schema (the "schema module"). This is the schema that all other modules ("feature modules") can reuse.
- The schema module and modules that want to share fragment definitions must enable the generation of metadata with `generateApolloMetadata.set(true)`.
- Feature modules that depend on the schema module and/or other modules must declare those dependencies with `dependsOn(project(":schema"))`
- Also add the reverse dependencies in the schema module with `isADependencyOf(project(":feature"))`, so only the used types are generated in the schema module.

## Project layout

A typical layout for an Android or JVM module:
```
src/main/graphql/
  GetUserQuery.graphql
  schema.graphqls
  extra.graphqls
src/main/kotlin/
  com/example/myapp/
    SomeClass.kt
```

For KMP:
```
src/commonMain/graphql/
  GetUserQuery.graphql
  schema.graphqls
  extra.graphqls
src/commonMain/kotlin/
  com/example/myapp/
    SomeClass.kt
```

## Client setup

- Keep a single `ApolloClient` (or one per service in a multiple services case) and inject it via DI.
- Add auth headers in one place through interceptors.
- Configure logging for dev builds only.

```kotlin
val apolloClient = ApolloClient.Builder()
  .serverUrl("https://your.domain/graphql")
  .addHttpInterceptor(AuthorizationInterceptor(token))
  .apply {
    if (isDebugBuild) {
      addHttpInterceptor(LoggingInterceptor(level = Level.BODY))
    }
  }
  .build()
```


# Setup

Use this guide to take an empty Xcode project to a running `ApolloClient` with generated types. Covers SDK install, codegen CLI install, writing `apollo-codegen-config.json`, running initial codegen, and wiring `ApolloClient` into SwiftUI.

## Add the SDK

- Always use Apollo iOS **v2+**. v1.x and v0.x are legacy and must not be used for new work.
- Always use the latest **v2.x** release. To find the latest version, run `scripts/list-apollo-ios-versions.sh` and pick the highest `2.N.M` tag (tags do not have a `v` prefix in the 2.x line).

### Swift Package Manager (recommended)

Add Apollo iOS to `Package.swift`:

```swift
dependencies: [
  .package(
    url: "https://github.com/apollographql/apollo-ios.git",
    .upToNextMajor(from: "LATEST_APOLLO_VERSION")
  ),
],
```

In Xcode, the equivalent workflow is **File → Add Package Dependencies → https://github.com/apollographql/apollo-ios.git**.

### Link the right product to each target

Apollo iOS ships five products. Pick per target based on what that target actually does:

| Product | Link when the target… |
|---|---|
| `Apollo` | …creates or uses `ApolloClient` — executes operations, configures the interceptor chain, reads/writes the normalized cache directly. Depends on `ApolloAPI`, so linking `Apollo` gives you the generated types as well. |
| `ApolloAPI` | …only consumes generated response models (queries, mutations, fragments) without ever touching `ApolloClient`. Typical for UI / presentation modules in multi-module apps. |
| `ApolloSQLite` | …wires up `SQLiteNormalizedCache` (persistent on-disk cache). Usually the same target that constructs `ApolloClient`. |
| `ApolloWebSocket` | …uses `WebSocketTransport` — for subscription-only WebSocket setups, or when every operation flows over the WebSocket. See [subscriptions.md](subscriptions.md). |
| `ApolloTestSupport` | …is a test target using generated `Mock<Type>` fixtures. See [testing.md](testing.md). |

Single-target apps almost always link just `Apollo` (plus optionally `ApolloSQLite` / `ApolloWebSocket`). Multi-module apps mix `Apollo` for infrastructure / data-layer modules and `ApolloAPI` for UI modules that only read generated models — this keeps the networking layer out of view code and reduces binary size. Target linking is a lazy decision — add products as new targets need them; there is no upfront decision to make before writing `apollo-codegen-config.json`. See the official [Project Modularization](https://www.apollographql.com/docs/ios/project-configuration/modularization) docs for the detailed rationale.

Example — a single-target SwiftUI app with persistent caching:

```swift
.target(
  name: "MyApp",
  dependencies: [
    .product(name: "Apollo", package: "apollo-ios"),
    .product(name: "ApolloSQLite", package: "apollo-ios"),
  ]
),
```

Example — a multi-module app where `DataLayer` owns the `ApolloClient` and `Feature` only reads models:

```swift
.target(
  name: "DataLayer",
  dependencies: [
    .product(name: "Apollo", package: "apollo-ios"),
    .product(name: "ApolloSQLite", package: "apollo-ios"),
    "MyAPI", // the generated schema package — see codegen.md
  ]
),
.target(
  name: "Feature",
  dependencies: [
    .product(name: "ApolloAPI", package: "apollo-ios"),
    "MyAPI",
  ]
),
```

## Install the codegen CLI

Apollo iOS ships an SPM command plugin that downloads the `apollo-ios-cli` binary into the project directory. From a directory containing the Apollo SPM package:

```bash
swift package plugin --allow-writing-to-package-directory apollo-cli-install
```

This produces an executable at `./apollo-ios-cli`. Prefix CLI invocations below with `./` (e.g. `./apollo-ios-cli generate`).

For CI and non-SPM setups, download the universal macOS binary from the [Apollo iOS Releases](https://github.com/apollographql/apollo-ios/releases) page.

## Generate `apollo-codegen-config.json`

The canonical default is a dedicated schema SPM package with operation files generated next to each `.graphql` that defines them. This shape works for single-target and multi-module apps alike, and is the shape the rest of this reference assumes.

### Choose a schema module name first

Before running `init`, pick a name for the generated schema module. The convention is `<ProjectName>API` — for a project called `RocketReserver` you would use `RocketReserverAPI`; for `PetFinder` you would use `PetFinderAPI`. This name becomes:

- the value of `schemaNamespace` in `apollo-codegen-config.json`
- the name of the generated SPM package directory and target
- the module that other targets import (`import PetFinderAPI`)

**Derive the name from the actual project** — check `Package.swift`, the `.xcodeproj` filename, or the app's product name. If the project name is unclear, ask the user with `AskUserQuestion` rather than guessing. The examples below use `MyAPI` as a placeholder; substitute your real name wherever you see it (including `MyAPITestMocks`). Likewise, `MyApp` in the `embeddedInTarget` example stands in for whatever target name you are embedding into.

### Run `init` with your chosen name

Generate a minimal config with `./apollo-ios-cli init`:

```bash
./apollo-ios-cli init \
  --schema-namespace MyAPI \
  --module-type swiftPackage
```

Then edit it to the canonical shape:

```json
{
  "schemaNamespace": "MyAPI",
  "input": {
    "schemaSearchPaths": ["**/*.graphqls"],
    "operationSearchPaths": ["**/*.graphql"]
  },
  "output": {
    "schemaTypes": {
      "path": "./MyAPI",
      "moduleType": { "swiftPackage": {} }
    },
    "operations": { "relative": {} },
    "testMocks": { "none": {} }
  }
}
```

What this config does:

- **`moduleType: swiftPackage`** generates `./MyAPI/` as its own Swift package containing the schema types. Other targets in your workspace depend on it like any other SPM package. This is the recommended default for any SPM-based project (either a `Package.swift` or an Xcode project that uses SPM for dependencies).
- **`operations: relative`** (with no subpath) writes each generated operation file next to the `.graphql` file that defines it. This co-locates operations with the feature code that uses them — easy to find, easy to own, easy to move. Targets containing generated operation files must link both `MyAPI` (the schema module) and `ApolloAPI` (the runtime types the operations conform to).
- **`testMocks: none`** skips generating test mocks until they are actually needed. Mocks take up space and increase codegen time; turn them on only once you start writing tests that use them — see [testing.md](testing.md#enable-test-mocks).

**Deviating from the default.** If the project cannot use SPM (no `Package.swift`, Xcode project configured without SPM), use `moduleType: embeddedInTarget` or `moduleType: other` instead. If you prefer a single shared location for generated operations (or want to share fragments across modules differently), pick `operations: inSchemaModule` or `operations: absolute`. See [codegen.md](codegen.md) for the full reference of each option, their tradeoffs, and fragment-sharing patterns.

## Download the schema

Add a `schemaDownload` section to your config, then run `./apollo-ios-cli fetch-schema`:

```json
{
  "schemaDownload": {
    "downloadMethod": {
      "introspection": {
        "endpointURL": "https://api.example.com/graphql"
      }
    },
    "outputPath": "./MyAPI/schema.graphqls"
  }
}
```

Alternatively, check in a `schema.graphqls` fetched from your GraphQL server or Apollo Studio. Committing the schema file makes builds reproducible.

## Run initial codegen

Once the config file and schema are in place, generate types:

```bash
./apollo-ios-cli generate
```

**Run codegen manually** — after editing `schema.graphqls` or any `.graphql` operation file, re-run the command. Commit the generated Swift files alongside the `.graphql` source so CI and other contributors don't need to re-run codegen.

Do **not** wire `apollo-ios-cli generate` into an Xcode **Run Script** build phase. Running codegen on every build measurably slows compile times (generation scans the entire schema, even for small schemas); the slowdown compounds as the schema grows. Regenerate deliberately, not on every Cmd+B. If you want a shortcut, wrap it in a shell alias or project script (`make codegen`, `./scripts/codegen.sh`) rather than a build phase.

## Initialize `ApolloClient`

The simplest case — in-memory cache, default interceptors, HTTP transport:

```swift
import Apollo

let apolloClient = ApolloClient(url: URL(string: "https://api.example.com/graphql")!)
```

For real apps, use the full initializer so you can inject a custom interceptor provider (for auth) and a persistent cache:

```swift
import Apollo
import ApolloSQLite

func makeApolloClient() throws -> ApolloClient {
  let cacheURL = try FileManager.default
    .url(for: .cachesDirectory, in: .userDomainMask, appropriateFor: nil, create: true)
    .appendingPathComponent("apollo_cache.sqlite")

  let cache = try SQLiteNormalizedCache(fileURL: cacheURL)
  let store = ApolloStore(cache: cache)

  let endpointURL = URL(string: "https://api.example.com/graphql")!
  let transport = RequestChainNetworkTransport(
    urlSession: URLSession(configuration: .default),
    interceptorProvider: DefaultInterceptorProvider(store: store),
    store: store,
    endpointURL: endpointURL
  )

  return ApolloClient(networkTransport: transport, store: store)
}
```

For custom interceptors (auth tokens, logging, retry), see [interceptors.md](interceptors.md). For subscriptions, see [subscriptions.md](subscriptions.md).

## Wire `ApolloClient` into SwiftUI

Apollo iOS does not ship a built-in SwiftUI environment key, but the canonical pattern is a custom `EnvironmentValues` entry plus a single shared instance at the app root:

```swift
import SwiftUI
import Apollo

extension EnvironmentValues {
  @Entry var apolloClient: ApolloClient = {
    // Replace with your real client. Using a throwing factory from app startup
    // and guarding against failure is preferable to force-unwrap in production.
    try! makeApolloClient()
  }()
}

@main
struct MyApp: App {
  private let apolloClient: ApolloClient

  init() {
    self.apolloClient = try! makeApolloClient()
  }

  var body: some Scene {
    WindowGroup {
      RootView()
        .environment(\.apolloClient, apolloClient)
    }
  }
}
```

Access it from any view:

```swift
struct RootView: View {
  @Environment(\.apolloClient) private var apolloClient
  var body: some View { /* ... */ }
}
```

See [operations.md](operations.md) for the `@Observable` view-model pattern that actually executes operations against this client.

## Ground rules

- Default to the canonical `swiftPackage` + `relative` codegen config unless the project has a specific constraint (no SPM, legacy structure, fragment-sharing needs that require `inSchemaModule`, etc.). See [codegen.md](codegen.md) for when to deviate.
- Link `Apollo` to targets that use `ApolloClient`. Link `ApolloAPI` to targets that only read generated models. Do this per target — there is no upfront decision to make before writing the codegen config.
- Commit `apollo-codegen-config.json`, `schema.graphqls`, and all `.graphql` files to source control so builds are reproducible.
- Commit generated Swift files to source control. Do not rely on a build-phase script to regenerate them on every build — that slows compile times unnecessarily.
- Regenerate deliberately (manually, or via a dedicated script alias) after every `.graphql` or schema change. Never hand-edit generated files.
- Create one `ApolloClient` per endpoint, hold it for the lifetime of the app, and inject it via `Environment`. Never construct a new client per request or per view.
- Put authentication and retry logic in interceptors (see [interceptors.md](interceptors.md)). Never embed them in view code or view models.

# Code Generation

This reference covers the `apollo-codegen-config.json` file, CLI commands, renaming generated types, test mocks, Swift 6 compatibility flags, and build-time automation. For customizing how a custom GraphQL scalar maps to a Swift type (default is `String`), see [custom-scalars.md](custom-scalars.md).

If you don't yet have a codegen config, start with [setup.md](setup.md), which walks through the three project-configuration questions and generates a working config from your answers.

## Mental model

`.graphql` operation files + `schema.graphqls` → `apollo-ios-cli generate` → Swift types conforming to `SelectionSet` / `GraphQLOperation` (plus cache types, test mocks, etc.).

The CLI reads `apollo-codegen-config.json` to determine where inputs live, where outputs go, and what options to apply. The [official Codegen Configuration page](https://www.apollographql.com/docs/ios/code-generation/codegen-configuration) is the source of truth for every field.

## `apollo-codegen-config.json` top-level keys

```json
{
  "schemaNamespace": "MyAPI",
  "input": { /* where .graphqls and .graphql files live */ },
  "output": { /* where generated Swift goes */ },
  "options": { /* codegen behavior tweaks */ },
  "schemaDownload": { /* optional: config for `fetch-schema` command */ },
  "operationManifest": { /* optional: APQ operation manifest output */ },
  "experimentalFeatures": { /* optional: opt-in experiments */ }
}
```

`schemaNamespace` is the name of the generated schema module and the Swift module that other targets will `import`. **Base it on the project name** (convention: `<ProjectName>API`, e.g. `RocketReserverAPI` for a project called `RocketReserver`). Every example in this reference uses `MyAPI` as a placeholder — substitute your chosen name (and `MyAPITestMocks` for the test-mocks target) everywhere it appears. If the project name is unclear, ask the user rather than guessing.

### `input`

- `schemaSearchPaths: [String]` — glob patterns resolved relative to the config file for schema files (`.graphqls`). Include extension files (such as `@typePolicy` declarations) here.
- `operationSearchPaths: [String]` — glob patterns for `.graphql` operation and fragment files.

```json
"input": {
  "schemaSearchPaths": ["**/*.graphqls"],
  "operationSearchPaths": ["**/*.graphql"]
}
```

### `output.schemaTypes`

Controls where the schema module (shared types, cache keys, etc.) is generated.

| Field | Required | Meaning |
|---|---|---|
| `path` | yes | Output directory. |
| `moduleType` | yes | One of `swiftPackage` (recommended default), `embeddedInTarget`, or `other`. |

#### `swiftPackage` (recommended default)

Generates the schema types as their own Swift Package at the given `path`. Other targets in the workspace depend on it like any other SPM package. This is the right choice for any project that uses SPM — either a standalone `Package.swift` or an Xcode project configured to use SPM for dependencies.

```json
"schemaTypes": {
  "path": "./MyAPI",
  "moduleType": { "swiftPackage": {} }
}
```

Optional `apolloSDKDependency` controls how the generated package pins Apollo — useful if you're developing Apollo iOS locally:

```json
"moduleType": {
  "swiftPackage": {
    "apolloSDKDependency": {
      "sdkVersion": { "local": { "path": "../apollo-ios" } }
    }
  }
}
```

#### `embeddedInTarget`

Emits schema types inline in an existing target. Use this only when the project cannot adopt SPM — for example, a legacy Xcode project with CocoaPods or Carthage, or a target that for other reasons cannot depend on a Swift package.

```json
"schemaTypes": {
  "path": "./MyApp/MyAPI",
  "moduleType": {
    "embeddedInTarget": {
      "name": "MyApp",
      "accessModifier": "internal"
    }
  }
}
```

#### `other`

You are using a non-SPM build system (Tuist, Bazel, XCFramework, etc.) and will wire the generated files into a module yourself.

```json
"schemaTypes": {
  "path": "./MyAPI",
  "moduleType": { "other": {} }
}
```

### `output.operations`

Controls where generated operation types are written. Three options, each with different tradeoffs around module linking and fragment sharing. Full reference: the official [Operation Models](https://www.apollographql.com/docs/ios/project-configuration/operation-models) page.

#### `relative` (recommended default)

Generates each operation Swift file next to the `.graphql` file that defines it. No `subpath` means the file lands in the same directory as its source.

```json
"operations": { "relative": {} }
```

Optional `subpath` nests the generated files under a subfolder of each `.graphql` file's location:

```json
"operations": { "relative": { "subpath": "Generated" } }
```

**Target linking requirement.** Any target that contains generated operation files must link both the schema module (for example `MyAPI`, from `moduleType: swiftPackage`) and `ApolloAPI` (the runtime types that operations conform to). See [setup.md](setup.md#link-the-right-product-to-each-target) for the product-linking table.

**When to use.** Co-locating operations with the feature code that uses them — easy to find, easy to own, easy to move when refactoring feature boundaries. Works for single-target apps (all operations land inside the app target) and multi-module apps (operations land inside whichever feature module owns each `.graphql` file).

#### `inSchemaModule`

Generates all operation types inside the schema module itself.

```json
"operations": { "inSchemaModule": {} }
```

Feature targets import the schema module and consume operations from it. There is nothing extra to link (no per-target `ApolloAPI` dependency) because everything lives in the schema package.

**When to use.** When every feature module already imports the schema module anyway and you prefer a single place for all generated types, or when you need the simplest possible linking story for a small app.

#### `absolute`

Generates all operation files into a single directory you specify.

```json
"operations": { "absolute": { "path": "./Shared/Operations" } }
```

You are responsible for wiring the generated files into a module (or directly into a target) yourself.

**When to use.** Custom project structures that do not fit the other two options — for example, when you want a single dedicated "Operations" module distinct from the schema module.

#### Fragment sharing across modules

When operation models live in multiple feature modules (via `relative`), you may want to reuse a fragment defined in one module from an operation in another. Use the `@import(module: String!)` client directive in the consuming operation to pull the fragment type in:

```graphql
# Shared fragment defined in FeatureA
fragment UserSummary on User {
  id
  name
}
```

```graphql
# Consuming operation in FeatureB — imports the fragment type from FeatureA
query GetUser($id: ID!) @import(module: "FeatureA") {
  user(id: $id) {
    ...UserSummary
  }
}
```

The consuming module must declare the fragment-owning module as a SPM dependency so the generated types resolve. See the [operation-models docs](https://www.apollographql.com/docs/ios/project-configuration/operation-models) for the full fragment-sharing reference.

### `output.testMocks`

Controls generation of `Mock<Type>` helpers that you use in unit tests.

**Default to `none`.** Generated mocks add files, increase codegen time, and pull `ApolloTestSupport` into the dependency graph. Keep them off until you actually start writing tests that use them, then switch to `swiftPackage` (or `absolute`) and regenerate. This is a lazy decision — flip it when the need appears.

```json
"testMocks": { "none": {} }
```

Default. Emits no mocks.

```json
"testMocks": { "swiftPackage": { "targetName": "MyAPITestMocks" } }
```

Emits a sibling test-mocks target in the schema SPM package. Use this with `moduleType: swiftPackage` — the mocks target ends up inside the generated schema package and test targets depend on `MyAPITestMocks` alongside `MyAPI`.

```json
"testMocks": { "absolute": { "path": "./MyAppTests/Mocks" } }
```

Emits mocks at a specific location. Use this with `moduleType: embeddedInTarget` or `other`, or when you want mocks outside the schema module for any reason.

See [testing.md](testing.md) for how to use the generated mocks and the full setup flow when you enable them for the first time.

## `options`

All fields optional — defaults are sensible for most projects.

- `schemaDocumentation: "include" | "exclude"` — keep or strip GraphQL doc comments in generated types.
- `deprecatedEnumCases: "include" | "exclude"` — emit deprecated schema enum cases.
- `warningsOnDeprecatedUsage: "include" | "exclude"` — `@available(*, deprecated, …)` on deprecated fields.
- `selectionSetInitializers` — control which selection sets get public memberwise initializers (e.g. for building test fixtures).
- `operationDocumentFormat` — one of `"definition"` (include the query source in generated code) or `"operationId"` (include only the hash, useful with APQ).
- `schemaCustomization.customTypeNames` — rename generated types, enums, and input-object fields (see below).
- `conversionStrategies.enumCases` — `"camelCase"` (default) or `"none"`.
- `pruneGeneratedFiles: Bool` — delete stale files from `schemaTypes.path` before generating.
- `markTypesNonisolated: Bool` — **critical for Swift 6** (see below).

### `options.markTypesNonisolated`

When `true`, generated types are emitted with `nonisolated` modifiers. This prevents compilation errors in modules that enable `SWIFT_DEFAULT_ACTOR_ISOLATION = MainActor` (Swift 6.2+).

- Defaults to `true` when the codegen tool is built with Swift 6.2+.
- Defaults to `false` when built with an older toolchain.

If your app runs under Swift 6.2+ with default `@MainActor` isolation and you see "actor-isolated" errors referencing generated Apollo types, ensure `markTypesNonisolated` is `true`.

```json
"options": {
  "markTypesNonisolated": true
}
```

## Renaming generated types

`options.schemaCustomization.customTypeNames` changes the Swift name of a generated type — scalar, enum case, enum type, input object, or input-object field. This is **only about naming**; it does not affect the underlying type mapping. (For changing the Swift type of a custom scalar — e.g. making a `DateTime` scalar a `Foundation.Date` instead of the default `String` — see [custom-scalars.md](custom-scalars.md).)

Simple rename (scalar or object type):

```json
"options": {
  "schemaCustomization": {
    "customTypeNames": {
      "DateTime": "APIDateTime"
    }
  }
}
```

Rename an enum and remap specific case names:

```json
"customTypeNames": {
  "SkinCovering": {
    "enum": {
      "name": "CustomSkinCovering",
      "cases": { "HAIR": "CUSTOMHAIR" }
    }
  }
}
```

Rename an input object and remap field names:

```json
"customTypeNames": {
  "PetSearchFilters": {
    "inputObject": {
      "name": "CustomPetSearchFilters",
      "fields": { "size": "customSize" }
    }
  }
}
```

Use this when the generated Swift name collides with something in your app, or when the schema's naming conventions don't match Swift conventions. It is not needed for routine setup.

## `schemaDownload`

Optional. Configures what `apollo-ios-cli fetch-schema` does.

### Introspection

```json
"schemaDownload": {
  "downloadMethod": {
    "introspection": {
      "endpointURL": "https://api.example.com/graphql"
    }
  },
  "outputPath": "./MyAPI/schema.graphqls"
}
```

### Apollo Registry (Studio)

```json
"schemaDownload": {
  "downloadMethod": {
    "apolloRegistry": {
      "graphID": "my-graph",
      "variant": "current",
      "apiKey": "$APOLLO_API_KEY"
    }
  },
  "outputPath": "./MyAPI/schema.graphqls"
}
```

## CLI commands

```bash
./apollo-ios-cli init \
  --schema-namespace MyAPI \
  --module-type embeddedInTarget \
  --target-name MyApp
```

Creates a minimal `apollo-codegen-config.json` in the current directory.

```bash
./apollo-ios-cli fetch-schema
```

Downloads the schema according to the `schemaDownload` section.

```bash
./apollo-ios-cli generate
```

Generates Swift types. Pass `--path` if your config file lives elsewhere.

```bash
./apollo-ios-cli generate-operation-manifest
```

Writes an operation manifest for Automatic Persisted Queries. See [interceptors.md](interceptors.md#apq) for how the manifest is consumed at runtime.

## Running generation

Run `./apollo-ios-cli generate` manually after editing `schema.graphqls` or any `.graphql` operation file, and commit the generated Swift alongside the source. A shell alias or project script (`make codegen`, `./scripts/codegen.sh`) makes the common case a single keystroke.

**Do not wire codegen into an Xcode Run Script build phase.** Running `apollo-ios-cli generate` on every build measurably slows compile times — the generator scans the full schema regardless of what changed, and the cost compounds as the schema grows. Deliberate regeneration + committed output is the recommended pattern. The rare exceptions are CI jobs that need to verify the generated files are up to date (run `generate`, check for a dirty tree, fail if anything changed), or developer machines where a pre-commit hook catches forgotten regeneration.

## Multi-module projects

If you picked `moduleType: swiftPackage` (see [setup.md](setup.md#generate-apollo-codegen-configjson)), the schema becomes its own SPM package:

```
MyAPI/
  Package.swift
  Sources/MyAPI/          # generated schema types
  Sources/MyAPITestMocks/ # if testMocks.swiftPackage is used
```

Feature modules depend on the schema package:

```swift
.target(
  name: "FeatureModule",
  dependencies: [
    .product(name: "Apollo", package: "apollo-ios"),
    .product(name: "MyAPI", package: "MyAPI"),
  ]
)
```

When feature modules own their own operations, switch `operations` to `relative` so each operation file is generated next to the `.graphql` file that defines it.

## Ground rules

- Regenerate after every `.graphql` or `.graphqls` change.
- Never hand-edit generated Swift files. Editable stubs (e.g. custom scalar implementations, `SchemaConfiguration.swift`) are emitted exactly once; if you need to regenerate them, delete the stub file first.
- Commit `apollo-codegen-config.json` and `schema.graphqls`. Commit the generated Swift sources unless you guarantee codegen runs on every build machine.
- Keep `markTypesNonisolated: true` for Swift 6 projects.
- Use `pruneGeneratedFiles: true` so deleted operations don't linger as dead Swift files.

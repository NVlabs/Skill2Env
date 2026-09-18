# Custom Scalars

A GraphQL schema can declare custom scalar types (`DateTime`, `UUID`, `URL`, `Decimal`, etc.). Apollo iOS generates a Swift type for each one, but the default mapping is always **`typealias <ScalarName> = String`**. If `String` is acceptable — for example, an ID-like opaque identifier you never interpret — you do nothing. If you need a real Swift type (`Date`, `URL`, `Decimal`, a custom struct), replace the default typealias with a type that conforms to `CustomScalarType`.

This reference covers when to customize, the protocol you implement, and the canonical patterns for the common cases.

## Default behavior — don't customize yet

After codegen runs, each custom scalar appears as a stub file in the schema types directory:

```swift
// @generated
// This file was automatically generated and can be edited to
// implement advanced custom scalar functionality.
//
// Any changes to this file will not be overwritten by future
// code generation execution.

import ApolloAPI

public typealias DateTime = String
```

The comment at the top is load-bearing: **codegen emits this stub exactly once and never overwrites your edits**. That means the stub is a safe place to replace the typealias with a real implementation.

**Leave custom scalars as `String` until you have a concrete reason to do otherwise.** If view code never parses the string, if business logic never computes with it, and if the server-provided format is acceptable to display directly — the default is correct and lower-maintenance.

## When to replace the default

Replace the default when:

- You need to compute with the value (date math, currency arithmetic, URL opening, comparisons).
- You want type safety beyond "any string" — for example, guaranteeing a field is always a valid `URL`.
- Multiple call sites would otherwise reimplement the same string → typed-value parsing.

Conversely, prefer keeping `String` when:

- The value is only displayed (a formatted timestamp, a human-readable name).
- The scalar is an opaque ID you never inspect.
- You have one call site that parses the value — parse locally and keep the scalar as `String`.

## Replace the stub — the protocol

`CustomScalarType` (in `ApolloAPI`) requires three things: `Hashable`, `Sendable`, and a JSON round-trip via `init(_jsonValue:)` / `var _jsonValue`.

```swift
public protocol CustomScalarType:
  AnyScalarType,            // Sendable, Hashable, JSONEncodable
  JSONDecodable,            // init(_jsonValue:) throws
  OutputTypeConvertible,
  GraphQLOperationVariableValue,
  GraphQLOperationVariableListElement
{}
```

Implementations provide:

```swift
init(_jsonValue value: JSONValue) throws
var _jsonValue: JSONValue { get }
```

The `JSONValue` flowing in and out is whatever the GraphQL server produced — usually a `String`, occasionally a `Double` or a dictionary. Cast to the expected shape, convert, and throw `JSONDecodingError.couldNotConvert(value:to:)` if conversion fails.

## Pattern 1 — ISO-8601 date

Schema has `scalar DateTime`. Server sends ISO-8601 strings (`"2026-04-23T09:00:00Z"`).

```swift
// Sources/MyAPI/Schema/CustomScalars/DateTime.swift
import ApolloAPI
import Foundation

public struct DateTime: CustomScalarType {
  public let value: Date

  public init(_ value: Date) { self.value = value }

  public init(_jsonValue value: JSONValue) throws {
    guard let string = value as? String,
          let date = DateTime.formatter.date(from: string) else {
      throw JSONDecodingError.couldNotConvert(value: value, to: Date.self)
    }
    self.value = date
  }

  public var _jsonValue: JSONValue {
    DateTime.formatter.string(from: value)
  }

  private static let formatter: ISO8601DateFormatter = {
    let f = ISO8601DateFormatter()
    f.formatOptions = [.withInternetDateTime, .withFractionalSeconds]
    return f
  }()
}
```

Use it in view code as `dateTime.value` (a `Date`). Construct for sending with `DateTime(someDate)`.

## Pattern 2 — URL

Schema has `scalar URL`. Server sends URL strings.

```swift
// Sources/MyAPI/Schema/CustomScalars/URL.swift
import ApolloAPI
import Foundation

// The custom scalar name collides with Foundation.URL; keep the generated
// name but wrap it to disambiguate.
public struct URL: CustomScalarType {
  public let value: Foundation.URL

  public init(_ value: Foundation.URL) { self.value = value }

  public init(_jsonValue value: JSONValue) throws {
    guard let string = value as? String,
          let url = Foundation.URL(string: string) else {
      throw JSONDecodingError.couldNotConvert(value: value, to: Foundation.URL.self)
    }
    self.value = url
  }

  public var _jsonValue: JSONValue { value.absoluteString }
}
```

If the name collision with `Foundation.URL` is awkward in call sites, rename the generated type via `customTypeNames` (see [codegen.md](codegen.md#renaming-generated-types)):

```json
"options": {
  "schemaCustomization": {
    "customTypeNames": {
      "URL": "APIURL"
    }
  }
}
```

Then the stub file the codegen produces — and the type you edit — is `APIURL`.

## Pattern 3 — `Decimal`

Schema has `scalar Money` or `scalar Decimal`. Server typically sends a stringified decimal (`"19.99"`) to avoid IEEE-754 rounding.

```swift
// Sources/MyAPI/Schema/CustomScalars/Decimal.swift
import ApolloAPI
import Foundation

public struct Decimal: CustomScalarType {
  public let value: Foundation.Decimal

  public init(_ value: Foundation.Decimal) { self.value = value }

  public init(_jsonValue value: JSONValue) throws {
    if let string = value as? String, let decimal = Foundation.Decimal(string: string) {
      self.value = decimal
    } else if let double = value as? Double {
      self.value = Foundation.Decimal(double)
    } else {
      throw JSONDecodingError.couldNotConvert(value: value, to: Foundation.Decimal.self)
    }
  }

  public var _jsonValue: JSONValue { "\(value)" }
}
```

## Regenerating after you edit a stub

Custom scalar stubs are **not overwritten** by subsequent `apollo-ios-cli generate` runs. If you need to regenerate a stub from scratch (for example, after renaming the scalar via `customTypeNames`), delete the stub file first; codegen will emit a fresh default typealias that you can re-customize.

## Ground rules

- Keep the default `typealias <Scalar> = String` until you need a real type. The generated stubs exist specifically so that customization is lazy and opt-in.
- Edit stubs only. Never hand-edit any other generated file.
- When you replace a stub with a full conformance, conform to `CustomScalarType` (not just `JSONDecodable`); that protocol provides the full set of conformances the generated code expects.
- If a scalar's Swift name collides with a stdlib/Foundation type (e.g. `URL`), use `customTypeNames` in the codegen config to rename it (see [codegen.md](codegen.md#renaming-generated-types)) rather than manually wrapping at every call site.
- If you rename a scalar via `customTypeNames` after editing its stub, delete the old stub file before regenerating so the new stub is emitted under the new name.
- Custom scalar implementations must be `Sendable` (required by `AnyScalarType`). Use value types and avoid mutable reference state.

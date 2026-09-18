# Interceptors

Apollo iOS uses a chain-of-responsibility interceptor model for networking. Four distinct protocols split the work by what part of the request they can see: GraphQL request/response, HTTP request/response, cache lookup, and response parsing. A custom `InterceptorProvider` supplies instances for each operation.

This reference explains the four protocols, how to build a custom provider, and the patterns for the three most common use cases: **auth**, **logging**, and **retry**.

## The four interceptor protocols

| Protocol | Sees | Use for |
|---|---|---|
| `GraphQLInterceptor` | `GraphQLRequest` (mutable, including `additionalHeaders`) and the parsed `ParsedResult` stream | Auth (attach + refresh + retry), general retry, operation-level logging, APQ. **Default choice for most cross-cutting concerns.** |
| `HTTPInterceptor` | `URLRequest` and `HTTPResponse` | Genuinely HTTP-scoped concerns — static headers unrelated to the operation (`User-Agent`, `Accept-Encoding`), raw-bytes logging, mTLS wiring, response-code instrumentation. |
| `CacheInterceptor` | Pre-flight cache lookup, post-flight cache write | Custom caching strategies (rare) |
| `ResponseParsingInterceptor` | Raw response → `ParsedResult` | Custom wire formats (very rare) |

**Decision rubric:**

- Anything that touches the operation lifecycle (auth, retry, logging per-operation, APQ, conditional retargeting) → `GraphQLInterceptor`. It can mutate `request.additionalHeaders` to set HTTP headers, and it's the only layer that can trigger a full-operation retry via `RequestChain.Retry`.
- Static, operation-independent HTTP configuration (`User-Agent`, `Accept-Encoding`, URL-level logging, response-code instrumentation) → `HTTPInterceptor`.
- Custom caching or wire-format handling → `CacheInterceptor` / `ResponseParsingInterceptor` (almost never needed).

**Why not split "attach token" into an `HTTPInterceptor`?** You can, and it works — but for any app that also handles token refresh + retry, you end up needing a `GraphQLInterceptor` anyway (see [Auth](#auth-attach--refresh--retry-in-one-interceptor) below). Consolidating attach and refresh in one place avoids a shared token-store coordinated across two layers and keeps auth logic in one file.

## Custom `InterceptorProvider`

The `InterceptorProvider` protocol returns a fresh set of interceptors for each operation. **Always construct new instances per operation** — the `MaxRetryInterceptor` and some auth-refresh patterns rely on per-operation state.

```swift
import Apollo
import Foundation

final class AppInterceptorProvider: InterceptorProvider, Sendable {
  private let tokenManager: AuthTokenManager

  init(tokenManager: AuthTokenManager) {
    self.tokenManager = tokenManager
  }

  func graphQLInterceptors<Operation: GraphQLOperation>(
    for operation: Operation
  ) -> [any GraphQLInterceptor] {
    [
      MaxRetryInterceptor(maxRetriesAllowed: 3),               // safety-net retry cap (must be first)
      AuthInterceptor(tokenManager: tokenManager),             // attach + refresh + retry-on-401
      AutomaticPersistedQueryInterceptor(),
    ]
  }

  // Most apps don't need custom HTTPInterceptors beyond the default ResponseCodeInterceptor
  // (provided automatically via the protocol extension). Override only when adding
  // static HTTP-scoped headers like User-Agent.

  // `cacheInterceptor` and `responseParser` fall back to the DefaultInterceptorProvider
  // implementations from an extension on InterceptorProvider.
}
```

Wire the provider into the transport:

```swift
let provider = AppInterceptorProvider(tokenManager: tokenManager)
let transport = RequestChainNetworkTransport(
  urlSession: URLSession(configuration: .default),
  interceptorProvider: provider,
  store: store,
  endpointURL: URL(string: "https://api.example.com/graphql")!
)
```

`AuthTokenManager` is an app-owned actor that holds the current access token and knows how to refresh it against your auth service. See the next section for its shape.

## Auth: attach + refresh + retry in one interceptor

Attach a bearer token on every request, detect 401 responses, refresh the token, and retry the operation — all in a single `GraphQLInterceptor`. This is the canonical pattern for any app that needs token refresh.

The mechanics:

- **Attach** by mutating `request.additionalHeaders["Authorization"]` in the pre-flight phase. Apollo iOS copies `additionalHeaders` into the outgoing `URLRequest` via `createDefaultRequest()` — functionally equivalent to setting the header at the HTTP layer.
- **Detect** failures post-flight via `.mapErrors`. When a 401 from the server surfaces, it arrives as a `ResponseCodeInterceptor.ResponseCodeError` with `response.statusCode == 401`.
- **Retry** by throwing `RequestChain.Retry(request:)`. The `RequestChain` specifically catches this error type and restarts the interceptor chain from step 1 with the request you provide. Every other thrown error bubbles up to the caller.
- **Cap infinite loops** with `MaxRetryInterceptor`. It tracks how many times the chain has been re-entered and throws `MaxRetryInterceptor.MaxRetriesError` once the limit is hit. It does **not** catch errors or trigger retries itself — it is a safety net on top of `RequestChain.Retry`.

```swift
import Apollo
import ApolloAPI
import Foundation

/// App-owned actor that holds the current access token and can refresh it.
/// Replace the body of `refreshToken()` with your real auth flow — exchanging a
/// stored refresh token at `/oauth/refresh`, prompting Sign in with Apple, etc.
actor AuthTokenManager {
  private(set) var token: String?

  init(initialToken: String? = nil) { self.token = initialToken }

  func currentToken() -> String? { token }

  func refreshToken() async throws -> String {
    let newToken = try await performServerRefresh()
    self.token = newToken
    return newToken
  }

  private func performServerRefresh() async throws -> String {
    // TODO: replace with your app's refresh call.
    fatalError("Implement performServerRefresh() against your auth service")
  }
}

struct AuthInterceptor: GraphQLInterceptor {
  let tokenManager: AuthTokenManager

  func intercept<Request: GraphQLRequest>(
    request: Request,
    next: NextInterceptorFunction<Request>
  ) async throws -> InterceptorResultStream<Request> {
    // Pre-flight: attach the current token.
    var request = request
    if let token = await tokenManager.currentToken() {
      request.additionalHeaders["Authorization"] = "Bearer \(token)"
    }

    // Post-flight: observe 401, refresh, and trigger a retry.
    let originalRequest = request
    return await next(request).mapErrors { [tokenManager] error in
      guard let codeError = error as? ResponseCodeInterceptor.ResponseCodeError,
            codeError.response.statusCode == 401 else {
        throw error
      }
      _ = try await tokenManager.refreshToken()

      // Hand RequestChain the request to retry with. On the next pass through
      // the chain, this same interceptor will re-attach the freshly-rotated
      // token from the manager.
      throw RequestChain.Retry(request: originalRequest)
    }
  }
}
```

Order in `graphQLInterceptors(for:)` matters: `MaxRetryInterceptor` must come **first** so it is re-entered on every retry and can count toward its cap. The `AppInterceptorProvider` shown above already orders them correctly.

**Simpler case — static token, no refresh:** if your app only needs to attach a token and never refreshes it, the attach-only half of the interceptor is the whole thing:

```swift
struct StaticAuthInterceptor: GraphQLInterceptor {
  let token: String

  func intercept<Request: GraphQLRequest>(
    request: Request,
    next: NextInterceptorFunction<Request>
  ) async throws -> InterceptorResultStream<Request> {
    var request = request
    request.additionalHeaders["Authorization"] = "Bearer \(token)"
    return await next(request)
  }
}
```

**When `HTTPInterceptor` makes sense instead:** if the header is purely HTTP-scoped (unrelated to the operation, never participates in retry), put it in an `HTTPInterceptor`. Static instrumentation headers (`User-Agent`, `Accept-Encoding`, a CSRF token keyed to an HTTP session) fit naturally. A team that prefers strict layer separation may also choose to attach the auth token at the HTTP layer using `request.setValue(_, forHTTPHeaderField:)` — functionally identical, but costs a second interceptor and cross-layer coordination through the shared `AuthTokenManager`.

## Logging interceptor (debug builds only)

A `GraphQLInterceptor` can log the operation name pre-flight and the parsed result post-flight. The WWDC-style recipe from the SDK's own docs:

```swift
import Apollo
import os

struct LoggingInterceptor: GraphQLInterceptor {
  let logger: Logger

  func intercept<Request: GraphQLRequest>(
    request: Request,
    next: NextInterceptorFunction<Request>
  ) async throws -> InterceptorResultStream<Request> {
    logger.debug("→ \(Request.Operation.operationName)")
    return await next(request)
      .map { result in
        logger.debug("← \(Request.Operation.operationName) ok")
        return result
      }
      .mapErrors { error in
        logger.error("✕ \(Request.Operation.operationName): \(error)")
        throw error
      }
  }
}
```

Add it to `graphQLInterceptors(for:)` only in `DEBUG` builds:

```swift
func graphQLInterceptors<Operation: GraphQLOperation>(
  for operation: Operation
) -> [any GraphQLInterceptor] {
  var interceptors: [any GraphQLInterceptor] = [MaxRetryInterceptor()]
  #if DEBUG
  interceptors.append(LoggingInterceptor(logger: Logger(subsystem: "MyApp", category: "Apollo")))
  #endif
  interceptors.append(AutomaticPersistedQueryInterceptor())
  return interceptors
}
```

## Retry

Retries in Apollo iOS are triggered by throwing `RequestChain.Retry(request:)` from an interceptor. When the `RequestChain` sees this specific error type, it restarts the chain from step 1 with the request you provided — same interceptor instances, same store, same session. Any other thrown error propagates to the caller normally.

`MaxRetryInterceptor` is a safety net that **prevents infinite retry loops**. On each pass through the chain, it increments an internal counter; once the counter exceeds its configured max, it throws `MaxRetryInterceptor.MaxRetriesError` before calling `next`. It does not catch errors itself and does not trigger retries.

Configure it with optional exponential backoff and jitter:

```swift
MaxRetryInterceptor(
  configuration: .init(
    maxRetries: 3,
    baseDelay: 0.3,
    multiplier: 2.0,
    maxDelay: 20.0,
    enableExponentialBackoff: true,
    enableJitter: true
  )
)
```

Put it **first** in `graphQLInterceptors(for:)` so it is re-entered on every retry and can count accurately. `MaxRetryInterceptor` is stateful per-operation — never share an instance across operations. The `InterceptorProvider` contract is to create fresh instances each call, which is why the example above returns a freshly constructed `MaxRetryInterceptor()` from the function.

### Writing a custom retry

Any interceptor can trigger a retry by throwing `RequestChain.Retry(request:)` from either pre-flight or post-flight (`.map` / `.mapErrors`) code. Mutate the request first if you want the retry to carry different state — a new header, a different `fetchBehavior`, a fallback endpoint. Example: if an HTTP response code error comes back, fall back to cache-only for the retry:

```swift
struct FallbackToCacheOnFailure: GraphQLInterceptor {
  func intercept<Request: GraphQLRequest>(
    request: Request,
    next: NextInterceptorFunction<Request>
  ) async throws -> InterceptorResultStream<Request> {
    return await next(request).mapErrors { error in
      guard error is ResponseCodeInterceptor.ResponseCodeError else { throw error }
      var request = request
      request.fetchBehavior = FetchBehavior.CacheOnly
      throw RequestChain.Retry(request: request)
    }
  }
}
```

If you write a custom retry interceptor, always keep `MaxRetryInterceptor` in the chain so a pathological retry loop can't run forever.

## Automatic Persisted Queries (APQ)

`AutomaticPersistedQueryInterceptor` is included in the default provider. It sends a hash of each operation; if the server has the operation cached, it responds with the result. If not, it asks for the full operation, and the client retries with the query body included.

To enable APQ end to end:

1. Add `AutomaticPersistedQueryInterceptor()` to `graphQLInterceptors(for:)` (it is included in the default provider).
2. Configure `operationDocumentFormat: "operationId"` in `apollo-codegen-config.json` if you want to strip operation bodies from generated code.
3. Generate and upload an operation manifest with `./apollo-ios-cli generate-operation-manifest` so the server can recognize the hashes.

See [codegen.md](codegen.md#cli-commands) for the manifest command and the [APQ docs](https://www.apollographql.com/docs/ios/fetching/persisted-queries) for server setup.

## Ground rules

- **Create fresh interceptor instances per operation.** Sharing an instance across operations causes state bleed — for example, `MaxRetryInterceptor` counts retries per instance.
- **Put auth (attach + refresh + retry) in a single `GraphQLInterceptor`.** Attach the token by mutating `request.additionalHeaders["Authorization"]`; catch 401s via `.mapErrors`; trigger retry by throwing `RequestChain.Retry(request:)`. Reserve `HTTPInterceptor` for genuinely HTTP-scoped headers like `User-Agent` or `Accept-Encoding`.
- **Trigger retries with `RequestChain.Retry(request:)`, not by rethrowing arbitrary errors.** Only that specific error type restarts the chain. `MaxRetryInterceptor` is a safety-net cap on retry count — it does not catch or replay.
- Always include a `MaxRetryInterceptor` (at the start of `graphQLInterceptors(for:)`) whenever any interceptor may throw `RequestChain.Retry`, so a retry storm cannot loop forever.
- Keep logging interceptors `#if DEBUG` — logging request bodies in release builds leaks data and slows the network path.
- Do not subclass or monkey-patch `DefaultInterceptorProvider` — implement `InterceptorProvider` directly. Most methods have default implementations via protocol extension.

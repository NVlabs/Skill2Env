# Subscriptions

Apollo iOS supports GraphQL subscriptions over two transports:

- **HTTP multipart** — subscriptions run over the same `RequestChainNetworkTransport` that handles queries and mutations, using the [Apollo Router multipart subscription protocol](https://www.apollographql.com/docs/graphos/routing/operations/subscriptions/multipart-protocol). Nothing extra to configure — if your server supports multipart subscriptions, you're done.
- **WebSocket** (`graphql-transport-ws`) — a persistent socket connection via `ApolloWebSocket`'s `WebSocketTransport`. Can carry any operation type, not just subscriptions.

This reference covers both options, plus auth via connection params, backgrounding via `pause()` / `resume()`, and consuming a subscription from SwiftUI.

## Pick a transport

| Transport | Use when |
|---|---|
| HTTP multipart (via `RequestChainNetworkTransport`) | Your server supports the multipart subscription protocol (Apollo Router does). Simplest setup — no second transport to configure. |
| `WebSocketTransport` alone | Every operation (query, mutation, subscription) runs over the WebSocket connection. |
| `SplitNetworkTransport` (HTTP + WebSocket) | Queries and mutations go over HTTP, subscriptions go over the WebSocket. Common when the server exposes subscriptions only over `graphql-transport-ws`. |

The rest of this reference focuses on the WebSocket setups because they have the most moving parts (connection lifecycle, backgrounding, auth via `connection_init`). **For HTTP multipart subscriptions, there is no additional setup** — call `client.subscribe(subscription:)` against an `ApolloClient` built with a standard `RequestChainNetworkTransport` ([setup.md](setup.md)), and consume the returned `SubscriptionStream` exactly as shown in [Consume a subscription from SwiftUI](#consume-a-subscription-from-swiftui) below.

## Setup — `SplitNetworkTransport` (recommended)

```swift
import Apollo
import ApolloWebSocket
import Foundation

func makeApolloClient() throws -> ApolloClient {
  let store = ApolloStore()
  let endpointURL = URL(string: "https://api.example.com/graphql")!
  let webSocketURL = URL(string: "wss://api.example.com/graphql")!

  // HTTP transport for queries and mutations.
  let httpTransport = RequestChainNetworkTransport(
    urlSession: URLSession(configuration: .default),
    interceptorProvider: DefaultInterceptorProvider(),
    store: store,
    endpointURL: endpointURL
  )

  // WebSocket transport for subscriptions.
  let webSocketTransport = try WebSocketTransport(
    urlSession: URLSession(configuration: .default),
    store: store,
    endpointURL: webSocketURL,
    configuration: WebSocketTransport.Configuration(
      reconnectionInterval: 1.0,
      connectingPayload: [
        // Sent in the `connection_init` message. See "Auth" below.
        "Authorization": "Bearer \(currentAuthToken())"
      ],
      pingInterval: 20.0
    )
  )

  let splitTransport = SplitNetworkTransport(
    queryTransport: httpTransport,
    mutationTransport: httpTransport,
    subscriptionTransport: webSocketTransport,
    uploadTransport: httpTransport
  )

  return ApolloClient(networkTransport: splitTransport, store: store)
}
```

## Auth via connection params

`graphql-transport-ws` requires that auth be sent in the `connection_init` message rather than as an HTTP header on the upgrade request. Pass a `connectingPayload` in the transport configuration:

```swift
WebSocketTransport.Configuration(
  connectingPayload: [
    "Authorization": "Bearer \(token)"
  ]
)
```

When the token rotates, call `updateConnectingPayload(_:)` on the transport. You'll usually do this from whatever owns the auth session:

```swift
await webSocketTransport.updateConnectingPayload([
  "Authorization": "Bearer \(newToken)"
])
```

Existing subscriptions stay open. The new payload is used on the next (re)connection.

## Backgrounding — pause and resume

When the app moves to the background, pause the transport so the OS can release the WebSocket without dropping subscribers. When the app returns to the foreground, resume. Subscription streams remain alive across a pause/resume cycle.

```swift
import SwiftUI

struct RootView: View {
  @Environment(\.apolloClient) private var apolloClient
  @Environment(\.scenePhase) private var scenePhase
  let webSocketTransport: WebSocketTransport

  var body: some View {
    ContentView()
      .onChange(of: scenePhase) { _, newPhase in
        Task {
          switch newPhase {
          case .background, .inactive:
            await webSocketTransport.pause()
          case .active:
            await webSocketTransport.resume()
          @unknown default:
            break
          }
        }
      }
  }
}
```

Hold a reference to the `WebSocketTransport` (for example, in the `App` struct or a dependency container) so you can call `pause()` / `resume()` from scene-phase callbacks.

## Consume a subscription from SwiftUI

`client.subscribe(subscription:)` returns a `SubscriptionStream<GraphQLResponse<Subscription>>`, which is an `AsyncSequence`. Use `.task` so the subscription cancels automatically when the view disappears.

```swift
import SwiftUI
import Apollo

@Observable
@MainActor
final class MessageViewModel {
  var messages: [MessageReceivedSubscription.Data.MessageReceived] = []

  private let apolloClient: ApolloClient

  init(apolloClient: ApolloClient) { self.apolloClient = apolloClient }

  func listen() async {
    do {
      let stream = try apolloClient.subscribe(
        subscription: MessageReceivedSubscription(),
        cachePolicy: .cacheThenNetwork
      )
      for try await response in stream {
        if let newMessage = response.data?.messageReceived {
          messages.append(newMessage)
        }
      }
    } catch is CancellationError {
      // Expected when the view goes away.
    } catch {
      print("Subscription failed: \(error)")
    }
  }
}

struct ChatView: View {
  @Environment(\.apolloClient) private var apolloClient
  @State private var viewModel: MessageViewModel?

  var body: some View {
    Group {
      if let viewModel {
        List(viewModel.messages, id: \.id) { message in
          Text(message.body)
        }
        .task { await viewModel.listen() }
      }
    }
    .onAppear {
      if viewModel == nil {
        viewModel = MessageViewModel(apolloClient: apolloClient)
      }
    }
  }
}
```

## Subscription cache policies

`CachePolicy.Subscription` has two cases:

- `.cacheThenNetwork` — emit cached matches first, then deliver live events.
- `.networkOnly` — ignore the cache; deliver live events only.

Default is `.cacheThenNetwork`. Use `.networkOnly` when cached data is never meaningful for the subscription (for example, presence or typing indicators).

## Ground rules

- Hold a single `WebSocketTransport` for the lifetime of the app. Never create one per view.
- Always call `pause()` on `.background` / `.inactive` and `resume()` on `.active`. Failing to pause drains the battery and can get the app throttled.
- Use `.task { for try await response in stream { … } }` to consume the `SubscriptionStream`. Task cancellation ends the subscription cleanly.
- Auth tokens go in `connectingPayload`, not as an HTTP `Authorization` header on the upgrade request — `graphql-transport-ws` uses the `connection_init` message.
- When the token rotates, call `updateConnectingPayload(_:)` on the transport rather than tearing it down.
- Never block on `await webSocketTransport.pause()` from inside `body`. Put the `await` inside a `Task`.

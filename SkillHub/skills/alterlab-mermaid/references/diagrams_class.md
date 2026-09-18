<!-- Source: https://github.com/SuperiorByteWorks-LLC/agent-project | License: Apache-2.0 | Author: Clayton Young / Superior Byte Works, LLC (Boreal Bytes) -->

# Class Diagram

> **Back to [Style Guide](../mermaid_style_guide.md)** — Read the style guide first for emoji, color, and accessibility rules.

**Syntax keyword:** `classDiagram`
**Best for:** Object-oriented design, type hierarchies, interface contracts, domain models
**When NOT to use:** Database schemas (use [ER](er.md)), runtime behavior (use [Sequence](sequence.md))

---

## Exemplar Diagram

```mermaid
classDiagram
    accTitle: Payment Processing Class Hierarchy
    accDescr: Interface and abstract base class with two concrete implementations for credit card and digital wallet payment processing

    class PaymentProcessor {
        <<interface>>
        +processPayment(amount) bool
        +refund(transactionId) bool
        +getStatus(transactionId) string
    }

    class BaseProcessor {
        <<abstract>>
        #apiKey: string
        #timeout: int
        +validateAmount(amount) bool
        #logTransaction(tx) void
    }

    class CreditCardProcessor {
        -gateway: string
        +processPayment(amount) bool
        +refund(transactionId) bool
        -tokenizeCard(card) string
    }

    class DigitalWalletProcessor {
        -provider: string
        +processPayment(amount) bool
        +refund(transactionId) bool
        -initiateHandshake() void
    }

    PaymentProcessor <|.. BaseProcessor : implements
    BaseProcessor <|-- CreditCardProcessor : extends
    BaseProcessor <|-- DigitalWalletProcessor : extends

    classDef iface fill:#ede9fe,stroke:#7c3aed,stroke-width:2px,color:#3b0764
    classDef base fill:#dbeafe,stroke:#2563eb,stroke-width:2px,color:#1e3a5f
    classDef impl fill:#dcfce7,stroke:#16a34a,stroke-width:2px,color:#14532d

    cssClass "PaymentProcessor" iface
    cssClass "BaseProcessor" base
    cssClass "CreditCardProcessor,DigitalWalletProcessor" impl
```

---

## Tips

- Use `<<interface>>` and `<<abstract>>` stereotypes for clarity
- Show visibility: `+` public, `-` private, `#` protected
- Keep to **4–6 classes** per diagram — split larger hierarchies
- Style with `classDef` + `cssClass` (or the `:::` shorthand: `class Foo:::impl`) — never inline `style`, per the style guide. Use the approved palette for light semantic coloring:
  - 🟣 Purple for interfaces/abstractions
  - 🔵 Blue for base/abstract classes
  - 🟢 Green for concrete implementations
- Relationship arrows:
  - `<|--` inheritance (extends)
  - `<|..` implementation (implements)
  - `*--` composition · `o--` aggregation · `-->` dependency

---

## Template

```mermaid
classDiagram
    accTitle: Your Title Here
    accDescr: Describe the class hierarchy and the key relationships between types

    class InterfaceName {
        <<interface>>
        +methodOne() ReturnType
        +methodTwo(param) ReturnType
    }

    class ConcreteClass {
        -privateField: Type
        +methodOne() ReturnType
        +methodTwo(param) ReturnType
    }

    InterfaceName <|.. ConcreteClass : implements
```

---

## Complex Example

An event-driven notification platform with 11 classes organized into 3 `namespace` groups — core orchestration, delivery channels, and data models. Shows interface implementation, composition, and dependency relationships across layers.

```mermaid
classDiagram
    accTitle: Event-Driven Notification Platform
    accDescr: Multi-namespace class hierarchy for a notification system showing core orchestration, four delivery channel implementations, and supporting data models with composition and dependency relationships

    namespace Core {
        class NotificationService {
            -queue: NotificationQueue
            -registry: ChannelRegistry
            +dispatch(notification) bool
            +scheduleDelivery(notification, time) void
            +getDeliveryStatus(id) DeliveryStatus
        }

        class NotificationQueue {
            -pending: List~Notification~
            -maxRetries: int
            +enqueue(notification) void
            +dequeue() Notification
            +retry(attempt) bool
        }

        class ChannelRegistry {
            -channels: Map~string, Channel~
            +register(name, channel) void
            +resolve(type) Channel
            +healthCheck() Map~string, bool~
        }
    }

    namespace Channels {
        class Channel {
            <<interface>>
            +send(notification, recipient) DeliveryAttempt
            +getStatus(attemptId) DeliveryStatus
            +validateRecipient(recipient) bool
        }

        class EmailChannel {
            -smtpHost: string
            -templateEngine: TemplateEngine
            +send(notification, recipient) DeliveryAttempt
            +getStatus(attemptId) DeliveryStatus
            +validateRecipient(recipient) bool
        }

        class SMSChannel {
            -provider: string
            -rateLimit: int
            +send(notification, recipient) DeliveryAttempt
            +getStatus(attemptId) DeliveryStatus
            +validateRecipient(recipient) bool
        }

        class PushChannel {
            -firebaseKey: string
            -apnsKey: string
            +send(notification, recipient) DeliveryAttempt
            +getStatus(attemptId) DeliveryStatus
            +validateRecipient(recipient) bool
        }

        class WebhookChannel {
            -signingSecret: string
            -timeout: int
            +send(notification, recipient) DeliveryAttempt
            +getStatus(attemptId) DeliveryStatus
            +validateRecipient(recipient) bool
        }
    }

    namespace Models {
        class Notification {
            +id: uuid
            +channel: string
            +subject: string
            +body: string
            +priority: string
            +createdAt: timestamp
        }

        class Recipient {
            +id: uuid
            +email: string
            +phone: string
            +deviceTokens: List~string~
            +preferences: Map~string, bool~
        }

        class DeliveryAttempt {
            +id: uuid
            +notificationId: uuid
            +recipientId: uuid
            +status: DeliveryStatus
            +attemptNumber: int
            +sentAt: timestamp
        }

        class DeliveryStatus {
            <<enumeration>>
            QUEUED
            SENDING
            DELIVERED
            FAILED
            BOUNCED
        }
    }

    NotificationService *-- NotificationQueue : contains
    NotificationService *-- ChannelRegistry : contains
    ChannelRegistry --> Channel : resolves

    Channel <|.. EmailChannel : implements
    Channel <|.. SMSChannel : implements
    Channel <|.. PushChannel : implements
    Channel <|.. WebhookChannel : implements

    Channel ..> Notification : receives
    Channel ..> Recipient : delivers to
    Channel ..> DeliveryAttempt : produces

    DeliveryAttempt --> DeliveryStatus : has

    classDef iface fill:#ede9fe,stroke:#7c3aed,stroke-width:2px,color:#3b0764
    classDef core fill:#dbeafe,stroke:#2563eb,stroke-width:2px,color:#1e3a5f
    classDef impl fill:#dcfce7,stroke:#16a34a,stroke-width:2px,color:#14532d
    classDef model fill:#f3f4f6,stroke:#6b7280,stroke-width:2px,color:#1f2937

    cssClass "Channel,DeliveryStatus" iface
    cssClass "NotificationService,NotificationQueue,ChannelRegistry" core
    cssClass "EmailChannel,SMSChannel,PushChannel,WebhookChannel" impl
    cssClass "Notification,Recipient,DeliveryAttempt" model
```

### Why this works

- **3 namespaces mirror architectural layers** — Core (orchestration), Channels (delivery implementations), Models (data). A developer can scan one namespace without reading the others.
- **Color encodes the role** — purple for interfaces/enums, blue for core services, green for concrete implementations, gray for data models. The pattern is instantly recognizable.
- **Relationship types are deliberate** — composition (`*--`) for "owns and manages", implementation (`<|..`) for "fulfills contract", dependency (`..>`) for "uses at runtime". Each arrow type carries meaning.

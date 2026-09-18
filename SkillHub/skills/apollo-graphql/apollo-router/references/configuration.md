# Router Configuration Reference

The Router is configured via a YAML file (`router.yaml`). This reference covers the most common configuration options.

## Basic Structure (v2 default)

```yaml
supergraph:
  listen: 127.0.0.1:4000
  introspection: true
  path: /graphql

sandbox:
  enabled: true

homepage:
  enabled: false

cors:
  allow_any_origin: true  # development only

headers:
  all:
    request:
      - propagate:
          matching: ".*"

telemetry:
  # ... telemetry config
```

## Basic Structure (v1 legacy)

```yaml
cors:
  origins:
    - "*"
```

## Supergraph Configuration

```yaml
supergraph:
  # Address to listen on
  listen: 127.0.0.1:4000

  # GraphQL endpoint path
  path: /graphql

  # Enable introspection queries
  introspection: true

  # Query planning options
  query_planning:
    # Enable query plan caching
    cache:
      in_memory:
        limit: 512
```

## Sandbox and Introspection

```yaml
# Apollo Sandbox (GraphQL IDE)
sandbox:
  enabled: true  # Disabled by default in production

# Introspection (required for Sandbox)
supergraph:
  introspection: true  # Disabled by default in production
```

For development mode, both are enabled automatically with `--dev`.

## CORS Configuration

> **v1 vs v2**: CORS schemas are incompatible. See [divergence-map.md](../divergence-map.md) for details.

### v1 (flat schema)

```yaml
cors:
  origins:
    - http://localhost:3000
    - https://studio.apollographql.com
  allow_headers:
    - Content-Type
    - Authorization
  methods:
    - GET
    - POST
    - OPTIONS
  allow_credentials: true
  max_age: 24h  # duration string
```

### v2 (policies schema)

```yaml
cors:
  allow_credentials: true
  methods:
    - GET
    - POST
    - OPTIONS
  max_age: 24h  # duration string, not integer
  policies:
    - origins:
        - http://localhost:3000
        - https://studio.apollographql.com
      allow_headers:
        - Content-Type
        - Authorization
```

## Subgraph Configuration

```yaml
# Override subgraph URLs (useful for local development)
override_subgraph_url:
  products: http://localhost:4001/graphql
  reviews: http://localhost:4002/graphql

# Subgraph-specific settings
traffic_shaping:
  all:
    timeout: 30s
  subgraphs:
    products:
      timeout: 60s  # Override for slow subgraph
```

## Traffic Shaping

```yaml
traffic_shaping:
  # Apply to all subgraphs
  all:
    # Request timeout
    timeout: 30s

    # Rate limiting
    global_rate_limit:
      capacity: 1000
      interval: 1s

  # Router-level settings
  router:
    timeout: 60s

  # Per-subgraph settings
  subgraphs:
    slow-service:
      timeout: 120s
```

## Authentication (JWT)

> **v1 vs v2**: The `issuer` field was renamed to `issuers` (plural array) in v2. `issuer` is v1-only.

### v1

```yaml
authentication:
  router:
    jwt:
      jwks:
        - url: https://auth.example.com/.well-known/jwks.json
          issuer: https://auth.example.com/  # singular string

authorization:
  require_authentication: true
```

### v2

```yaml
authentication:
  router:
    jwt:
      jwks:
        - url: https://auth.example.com/.well-known/jwks.json
          issuers:                              # plural array
            - https://auth.example.com/

authorization:
  require_authentication: true
```

## Response Caching (v2.6.0+)

> Response caching uses the `response_cache` top-level key (not `supergraph.cache`).
> See [response-caching.md](response-caching.md) for full setup, schema directives, invalidation, and observability.

```yaml
# Minimal response caching setup
response_cache:
  enabled: true
  subgraph:
    all:
      enabled: true
      ttl: 5m
      redis:
        urls: ["redis://localhost:6379"]
```

## Persisted Queries (APQ)

```yaml
apq:
  enabled: true
  router:
    cache:
      in_memory:
        limit: 512
      # Or Redis
      # redis:
      #   urls:
      #     - redis://localhost:6379
```

## Limits and Security

```yaml
limits:
  # Maximum request body size
  http_max_request_bytes: 2000000  # 2MB

  # Query complexity limits
  max_depth: 15
  max_height: 200
  max_aliases: 30
  max_root_fields: 20
```

## Include Subgraph Errors

```yaml
# Control which subgraph errors are exposed to clients
include_subgraph_errors:
  all: true  # Include all subgraph errors (development)

  # Or selectively
  # all: false
  # subgraphs:
  #   products: true  # Only expose products errors
```

## Subscriptions

```yaml
subscription:
  enabled: true
  mode:
    # WebSocket-based subscriptions
    passthrough:
      all:
        path: /ws

    # Or callback-based
    # callback:
    #   public_url: https://router.example.com/callback
```

## Development vs Production

### Development Configuration

```yaml
# router.dev.yaml
supergraph:
  introspection: true

sandbox:
  enabled: true

include_subgraph_errors:
  all: true

telemetry:
  exporters:
    logging:
      stdout:
        enabled: true
        format: text
```

### Production Configuration

```yaml
# router.prod.yaml
supergraph:
  listen: 0.0.0.0:4000
  introspection: false

sandbox:
  enabled: false

homepage:
  enabled: false

health_check:
  enabled: true
  listen: 0.0.0.0:8088
  path: /health

include_subgraph_errors:
  all: false

# CORS — use v1 or v2 format as appropriate (see CORS section above)
cors:
  origins:
    - https://app.example.com

telemetry:
  exporters:
    tracing:
      otlp:
        enabled: true
        endpoint: http://collector:4317
```

For complete production templates with all features, see:
- [templates/v1/production.yaml](../templates/v1/production.yaml)
- [templates/v2/production.yaml](../templates/v2/production.yaml)

## Environment Variable Expansion

Use environment variables in configuration:

```yaml
supergraph:
  listen: ${env.ROUTER_LISTEN_ADDRESS:-127.0.0.1:4000}

override_subgraph_url:
  products: ${env.PRODUCTS_URL}

authentication:
  router:
    jwt:
      jwks:
        - url: ${env.JWKS_URL}
```

## Configuration Validation

Validate configuration without starting the Router:

```bash
router config validate router.yaml
```

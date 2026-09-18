---
name: netlify-blobs
description: Guide for using Netlify Blobs for file and asset storage — images, documents, uploads, exports, cached binary artifacts. Covers getStore(), CRUD operations, metadata, listing, deploy-scoped vs site-scoped stores, and local development. Do NOT use Blobs as a dynamic data store — use Netlify Database for that.
---

# Netlify Blobs

Netlify Blobs is zero-config object storage for **files and assets**: images, documents, uploads, exports, cached binary artifacts. Available from any Netlify compute (functions, edge functions, framework server routes). No provisioning required.

**Not for dynamic data.** If the project needs to store records, user data, application state, or anything queryable, use Netlify Database instead — see `netlify-database/SKILL.md`. Reach for Blobs when the thing you're storing is a file or an asset blob, not a record.

```bash
npm install @netlify/blobs
```

## Before you build

If the prompt didn't already specify, ask the user a few short questions before scaffolding any blob storage — answers shape access patterns, scoping, and how the assets are served back to clients:

- **What kind of asset?** (User uploads, exported documents, cached binaries, generated images — drives the storage and serving pattern.)
- **Who should be able to read it?** Public (anyone with a URL, or an unauthenticated endpoint that streams the blob) or private (only authenticated users, gated by your server code)? Blobs have **no built-in access control** — the serving layer is the gate. When in doubt, default to private; making something public later is easy, while pulling back data that was inadvertently exposed is not.
- **Site-scoped or deploy-scoped?** Site-scoped (`getStore()`) persists across deploys — the right default for user data. Deploy-scoped (`getDeployStore()`) is tied to a single deploy and disappears when that deploy is replaced — use only when the lifecycle should match a deploy (e.g., per-deploy build artifacts).
- **Roughly how big and how many?** Helps choose between a single large blob vs many small keyed blobs, and informs whether you'll need `list({ prefix: ... })` patterns.

**If you don't have preferences here, tell me what the assets are and I'll pick sensible defaults** — typically site-scoped with private access, served through an authenticated function.

## Getting a Store

```typescript
import { getStore } from "@netlify/blobs";

const store = getStore({ name: "my-store" });

// Use "strong" consistency when you need immediate reads after writes
const store = getStore({ name: "my-store", consistency: "strong" });
```

## CRUD Operations

These are the **only** store methods. Do not invent others.

### Create / Update

```typescript
// String or binary data
await store.set("key", "value");
await store.set("key", fileBuffer);

// With metadata
await store.set("key", data, {
  metadata: { contentType: "image/png", uploadedAt: new Date().toISOString() },
});

// JSON data
await store.setJSON("key", { name: "Example", count: 42 });
```

### Read

```typescript
// Text (default)
const text = await store.get("key");                    // string | null

// Typed retrieval
const json = await store.get("key", { type: "json" });  // object | null
const stream = await store.get("key", { type: "stream" });
const blob = await store.get("key", { type: "blob" });
const buffer = await store.get("key", { type: "arrayBuffer" });

// With metadata
const result = await store.getWithMetadata("key");
// { data: any, etag: string, metadata: object } | null

// Metadata only (no data download)
const meta = await store.getMetadata("key");
// { etag: string, metadata: object } | null
```

### Delete

```typescript
await store.delete("key");
```

### List

```typescript
const { blobs } = await store.list();
// blobs: [{ etag: string, key: string }, ...]

// Filter by prefix
const { blobs } = await store.list({ prefix: "uploads/" });
```

## Store Types

- **Site-scoped** (`getStore()`): Persist across all deploys. Use for most cases.
- **Deploy-scoped** (`getDeployStore()`): Tied to a specific deploy lifecycle.

## Limits

| Limit | Value |
|---|---|
| Max object size | 5 GB |
| Store name max length | 64 bytes |
| Key max length | 600 bytes |

## Local Development

Local dev uses a sandboxed store (separate from production). For Vite-based projects, install `@netlify/vite-plugin` to enable local Blobs access. Otherwise, use `netlify dev`.

**Common error**: "The environment has not been configured to use Netlify Blobs" — install `@netlify/vite-plugin` or run via `netlify dev`.

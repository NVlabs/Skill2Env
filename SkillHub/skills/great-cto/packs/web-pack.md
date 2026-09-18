---
name: web-pack
description: Framework decision tree (Next/Nuxt/Hono/Fastify), ORM choice (Prisma/Drizzle/Kysely), edge runtime constraints (Cloudflare Workers, Vercel Edge, Deno Deploy), auth providers
when_to_use: Building web services, REST/GraphQL APIs, full-stack apps, edge functions
applies_to:
  - web-service
---

# Web Service Pack

> Extends `web-service` archetype with framework-specific guidance for full-stack web apps, REST/GraphQL APIs, edge runtime services, and microservices.
> Auto-loaded when `archetype: web-service` is detected in PROJECT.md (covers ~60% of projects).
> Also loaded explicitly via `packs: [web-pack]`.

## Decision tree — frontend framework

| If you need... | Pick | Why |
|---------------|------|-----|
| SEO + dynamic content + React | **Next.js 15** (App Router) | Server Components, RSC streaming, partial prerendering, edge runtime, native auth |
| SEO + dynamic content + Vue | **Nuxt 3.x** | Same SSR story for Vue. Edge-deployable on Cloudflare/Vercel. |
| SEO + dynamic content + Svelte | **SvelteKit** | Smallest bundles, fastest hydration. Best DX in the SSR space. |
| MPA-feel + islands architecture | **Astro 5** | Default zero-JS. Use for content-heavy sites where most pages are static. |
| Enterprise SPA, no SSR | **Angular 18+** | Standalone components, Signals, RxJS. Pick when team already knows Angular. |
| Quick admin / internal tool UI | **Next.js + shadcn/ui** OR **Retool** | shadcn for control + customisation; Retool for "I need this by Friday" |
| Real-time / collaboration | **Next.js + tRPC subscriptions** OR **Liveblocks** | tRPC gives type-safe client. Liveblocks abstracts presence/cursors/comments |

**Anti-pattern**: SSR for an internal admin tool that 5 users see. Pure SPA + Vite is faster to build and maintain.

## Decision tree — backend framework

| Stack | When | Notes |
|-------|------|-------|
| **Node + Hono** | Edge-first, Cloudflare Workers, Deno Deploy | Smallest cold start, Web Standard APIs, fits edge runtime |
| **Node + Fastify** | Standard Node REST API | Faster than Express, type-safe via TypeBox, mature plugin ecosystem |
| **Node + NestJS** | Large team, OOP preference, Angular background | Opinionated structure, dependency injection, scales with team size |
| **Node + Express** | Legacy / minimal new code | Only for migrations. New services: Fastify or Hono. |
| **Python + FastAPI** | Async-heavy, ML serving, Pydantic schemas | Best Python REST framework right now. Auto OpenAPI. |
| **Python + Django** | CRUD-heavy admin, batteries included | When you need admin panel + ORM + auth out of the box |
| **Go + Gin / Chi / Echo** | High throughput, low memory, single binary | Pick Chi for stdlib feel; Gin for ergonomics; Echo for middleware ecosystem |
| **Rust + Axum** | Maximum performance, type-safety obsession | Steep learning curve. Justify with concrete perf budget. |

**Default for new project without strong preference**: Node + Fastify + TypeScript + Drizzle ORM + Postgres.

## ORM / database access

| Tool | When |
|------|------|
| **Drizzle ORM** | TypeScript-first, edge-compatible, SQL-like API, smallest bundle | Default for new TypeScript projects |
| **Prisma 6** | Need migrations CLI + Studio + complex relations | More mature; heavier client; not edge-compatible without driver adapters |
| **Kysely** | You want SQL but type-safe, no ORM abstraction | When you prefer query-builder over ORM |
| **TypeORM** | Migrating from Java/.NET background | Not recommended for new projects in 2026 — Drizzle/Prisma are better |
| **SQLAlchemy 2.x (Python)** | Python projects | Async support is mature, migrations via Alembic |
| **sqlx (Rust)** | Compile-time checked SQL | Best for Rust projects; macros verify queries against actual schema |

**Rule**: never write raw SQL with string concatenation from user input. Always parameterised queries. The ORM is not optional for SQL injection prevention — even if you don't like ORMs, use a query builder.

## Auth — pick one and commit

| Provider | Best for | Cost |
|----------|----------|------|
| **Clerk** | SaaS where you need fast time to market, MFA, organisations, billing | $25+/mo, scales with MAU |
| **Auth.js (NextAuth v5)** | Self-hosted, OAuth providers, no per-MAU cost | Free (your hosting) |
| **Lucia** | You want the auth primitives, not a framework | Free, very low magic |
| **Supabase Auth** | Already using Supabase for DB | Bundled with Supabase plan |
| **WorkOS** | Enterprise SSO (SAML, SCIM) for B2B SaaS | Pricing on volume; built for B2B |
| **Auth0** | Existing enterprise integration | Most expensive. Don't pick new in 2026. |

**Anti-pattern**: rolling your own session + password reset + email verification + MFA + OAuth. Three months of work, security risks at every step. Use Clerk/Auth.js.

## Edge runtime considerations

If you're targeting `edge-app` (Cloudflare Workers, Vercel Edge, Deno Deploy):

- **Cold start budget**: < 50ms
- **Bundle size budget**: < 1 MB compressed
- **Memory budget**: 128 MB (Workers) / 256 MB (Vercel Edge)
- **No Node APIs**: no `fs`, no `child_process`, no native modules
- **Database access**: use HTTP-based drivers (Neon, PlanetScale, Turso) or D1; classical TCP-based pg/mysql clients won't work
- **Multi-region replication**: data lives in multiple regions; design for eventual consistency
- **Durable Objects** (Cloudflare) when you need consistent state at edge

These are hard constraints, not preferences. If your service can't meet them, pick a regional Node.js host instead (Vercel Functions, Render, Fly.io).

## Realtime patterns

| Need | Pick |
|------|------|
| Live cursors, presence, comments | **Liveblocks** or **Yjs + y-websocket** |
| Server → client push, low frequency | **SSE (EventSource)** — simpler than WebSocket |
| Bi-directional, high frequency | **WebSocket** (raw or via Pusher/Ably/Soketi) |
| Type-safe RPC + subscriptions | **tRPC subscriptions** over WebSocket |
| Game-style realtime sync | **Colyseus** (Node) or custom WebRTC DataChannel |

**Pitfall**: WebSocket connections don't survive Cloudflare Workers. Use Durable Objects or Pusher/Ably for edge.

## Performance budget (default for `web-service`)

```
First Byte (p95):           < 200ms (regional) | < 300ms (multi-region)
Largest Contentful Paint:   < 2.5s
First Input Delay (INP):    < 200ms
Cumulative Layout Shift:    < 0.1
JS bundle (initial):        < 200 KB compressed
Total page weight:          < 1 MB
```

Measure with [PageSpeed Insights](https://pagespeed.web.dev/), [WebPageTest](https://www.webpagetest.org/), or built-in `next/script` web vitals reporting. CI gate via [Lighthouse CI](https://github.com/GoogleChrome/lighthouse-ci).

## E2E testing — Playwright always

`qa-engineer` runs Playwright by default for `web-service` archetype. Patterns:

```typescript
// Critical user flow — runs in CI on every PR
test('checkout flow completes', async ({ page }) => {
  await page.goto('/products/widget');
  await page.click('text=Add to cart');
  await page.click('text=Checkout');
  await page.fill('[name=email]', 'test@example.com');
  await page.fill('[name=card]', '4242424242424242');
  await page.click('text=Pay');
  await expect(page).toHaveURL(/\/order\/confirmed/);
});
```

**Don't write Cypress for new projects** — Playwright is faster, more parallel, and supports more browsers (incl. mobile). Migrate Cypress codebases gradually if cost-effective.

## Observability essentials

For any production web-service:

- **Tracing**: OpenTelemetry SDK + Tempo (or Datadog/Honeycomb if budget)
- **Logs**: structured JSON, ship to Loki / CloudWatch / Datadog
- **Metrics**: Prometheus (RED method: Rate, Errors, Duration)
- **Frontend errors**: Sentry, Bugsnag, or Highlight.io
- **Real User Monitoring (RUM)**: Sentry Performance, Datadog RUM, Grafana Faro

If you're MCP-integrated with Grafana (see `mcp-servers/grafana.md`), `l3-support` reads from Loki/Tempo automatically.

## Common compliance for `web-service`

Default: **OWASP Top 10** + GDPR if EU users. Override via `compliance: []` in PROJECT.md:

| Trigger | Add |
|---------|-----|
| EU users + cookies | `gdpr-cookie` (consent banner, no third-party trackers without consent) |
| Auth flows | `owasp-auth` (rate limiting, MFA, password rotation) |
| File upload | `owasp-upload` (size limit, MIME check, virus scan, store outside webroot) |
| Public API | `owasp-api` (rate limit per token, schema validation, CORS lockdown) |
| Storing PII | `gdpr` (DPIA, deletion, export, consent records) |

`security-officer` runs the matching checklist when these are set.

## Anti-patterns specific to `web-service`

| Pattern | Why it fails | Fix |
|---------|-------------|-----|
| One monolith deployed via FTP | No staging, no rollback, no diff | Container + canary deploy via `devops` agent |
| Storing JWT in localStorage | XSS = full account takeover | HTTP-only cookies + CSRF token |
| `db.query("SELECT * FROM users WHERE id=" + id)` | SQL injection | Parameterised query / ORM |
| Generated GraphQL schemas with no depth limit | DoS via deep query | Add depth + complexity limits at gateway |
| 50-table monolith Prisma schema | Migration hell | Split by bounded context, deploy independently |
| No rate limit on public API | Abuse, cost runaway | Rate limit at gateway (Cloudflare, Kong) and at app (express-rate-limit) |
| Long-running synchronous jobs in HTTP handler | Timeout, retry storms | Queue (BullMQ, SQS, Trigger.dev) + status endpoint |

## Default deploy pattern

For `web-service`:

1. **Build**: containerised (Docker), tagged with git SHA
2. **Push**: registry (GHCR, ECR, GAR)
3. **Deploy**: canary 1% → 5% → 25% → 100%, 5-minute soak at each step
4. **Smoke test**: `devops` runs `/healthz` + critical-path probe at each step
5. **Rollback trigger**: error rate > 2× baseline OR p95 latency > 1.5× baseline
6. **Rollback action**: traffic shift back to previous tag, < 30s

For edge-app (Cloudflare Workers / Vercel Edge):

1. **Build**: native build (no container)
2. **Deploy**: `wrangler deploy` (CF) or `vercel deploy --prod` — atomic
3. **Rollback**: `wrangler rollback` or Vercel "Promote previous deployment"
4. **Multi-region testing**: hit edge endpoint from multiple regions before promote

## QA extras provided by this pack

When `archetype: web-service`, `qa-engineer` automatically runs:

- **Playwright** smoke test on critical paths (login, checkout, primary CRUD)
- **Lighthouse CI** for Core Web Vitals (LCP, INP, CLS)
- **OWASP ZAP baseline scan** if `compliance: [owasp]` is set
- **k6 load test** if `qa-extras: [load-test]` is set
- **Pact contract test** if `qa-extras: [contract-test]` is set
- **Bundle size diff** vs main branch (fail if > 10% increase without justification)

## Recommended `PROJECT.md` for new web-service

```yaml
primary: web-fullstack
archetype: web-service
project_size: medium
stack: [typescript, nextjs, postgres, prisma]
team-size: 3
compliance: [owasp, gdpr]
performance-sla: p95 < 200ms
qa-extras: [contract-test]
packs: [web-pack]
```

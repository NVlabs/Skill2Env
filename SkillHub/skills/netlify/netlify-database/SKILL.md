---
name: netlify-database
description: Guide for using Netlify Database — the GA managed Postgres product built into Netlify. Use when a project needs any kind of dynamic, structured, or relational data. Covers provisioning via @netlify/database, Drizzle ORM (@beta) setup, migrations, preview branching, and safe production data handling. Blobs is only for file/asset storage — any dynamic data belongs in the database.
---

# Netlify Database

**Netlify Database** is the managed Postgres product built into the Netlify platform. It is **GA** and is the default choice for any dynamic data in a Netlify project.

Install `@netlify/database` and Netlify auto-provisions a Postgres database for the site at deploy time. Each deploy preview gets its own isolated branch forked from production data. No Neon account, connection-string wiring, or claim flow — the database is a first-class Netlify primitive.

## Database vs Blobs

Use **Netlify Database** for anything dynamic:

- Any user-generated or app-generated records (posts, comments, orders, sessions, audit logs)
- Structured data that will grow, be queried, or be joined
- Key-value-style data read or written by application code at runtime

Use **Netlify Blobs** only for **file and asset storage**: images, documents, exports, uploads, cached binary artifacts. Do not use Blobs as a dynamic data store — reach for Database instead. See `netlify-blobs/SKILL.md`.

## Before you build

If the prompt didn't already specify, ask the user a few short questions before scaffolding any database code — answers shape the schema, the seed data, and the query layer:

- **What entities does the app need?** (Users, posts, orders, sessions — drives the schema in `db/schema.ts`.)
- **Any seed data for the prototype?** (Test rows, default roles, sample content — these become a DML migration, not ad-hoc `INSERT`s against production.)
- **Drizzle (recommended) or native driver?** (Drizzle for type-safe queries and generated migrations; native for raw SQL or a different query builder like Kysely.)

**If you don't have preferences here, tell me roughly what the app does and I'll pick sensible defaults** — typically Drizzle with timestamp-prefix migrations and a starter schema for the entities the prompt implies.

## CRITICAL: Install Drizzle from the `@beta` dist-tag

The Netlify Database adapter for Drizzle ORM currently only exists on the `beta` release line of `drizzle-orm`. Install **both** `drizzle-orm` and `drizzle-kit` from the `@beta` dist-tag:

```bash
npm install drizzle-orm@beta
npm install -D drizzle-kit@beta
```

The default `latest` versions do not include the `drizzle-orm/netlify-db` adapter and will fail. If `drizzle-kit generate` errors about being outdated, or the `drizzle-orm/netlify-db` import fails to resolve, the install is missing `@beta`.

The `@beta` tag only affects the installed version — imports are written as `drizzle-orm`, `drizzle-orm/pg-core`, and `drizzle-orm/netlify-db` without modification.

## CRITICAL: Use the Netlify CLI for database operations

The CLI ships a complete database surface under `netlify database` (alias: `netlify db`) that replaces hand-rolled scripts and direct API/UI work. Reach for these commands first before writing custom tooling. **Requires Netlify CLI 26.0.0+** — if a `netlify database` subcommand isn't recognized, run `npm install -g netlify-cli@latest`.

The corollary: **never go around the CLI**, even for read-only operations. Specifically:

- **Do not run `psql`, `pg_dump`, or any other raw Postgres client** against a Netlify-hosted database, even for "harmless" `SELECT`s. Use `netlify database connect --query "..."` instead.
- **Do not curl `https://api.netlify.com/...`** to manage the database.
- **Do not read auth tokens** out of `~/Library/Preferences/netlify/config.json` (or anywhere on disk) to authenticate side-channel calls.
- **Do not use `netlify api <method>`** as a recovery hatch when a deploy fails to provision the database. The supported recovery is documented under [If the first deploy fails to provision the database](#if-the-first-deploy-fails-to-provision-the-database).

Wandering off the documented surface is how agents end up touching the wrong database, deleting the wrong resource, or leaking credentials. If the documented happy path doesn't work, surface the failure to the user with context — see [When something fails, surface and stop](#when-something-fails-surface-and-stop) below.

Full reference is in [Netlify CLI commands](#netlify-cli-commands-for-netlify-database) below.

## When something fails, surface and stop

When a `netlify` command fails, a deploy fails to provision the database, or any documented happy path errors out, the right action is to **report the failure to the user** with the deploy log URL, the exact error, and the affected site/branch — and stop. Do not invent recovery commands or escalate to lower-level tools.

Specific failure modes (like the first-deploy 401) get their own playbooks below. The general rule applies everywhere: a stuck agent surfacing context is far safer than a "helpful" agent that wanders off and deletes the wrong database.

## CRITICAL: Never apply migrations to a Netlify-hosted database

The only database you ever apply migrations to yourself is the **local development DB**. For any Netlify-hosted database — production or a deploy preview branch — **Netlify applies migrations automatically during the deploy**. Your job is to create migration files and commit them. The deploy does the rest.

This means:

- Use `netlify database migrations apply` for the local DB. Do NOT run `drizzle-kit migrate` against `NETLIFY_DB_URL` in any context.
- Do NOT run `drizzle-kit push` at all. Generate a migration and let the deploy apply it.
- Do NOT run raw DDL (`CREATE`, `ALTER`, `DROP`, `TRUNCATE`) via `netlify database connect`, `psql`, or any other direct connection. Schema changes go through migration files; out-of-band DDL drifts the migration history from the actual schema.
- Do NOT export `NETLIFY_DB_URL` from a preview or production context and run a client against it. Migrations drift the moment anything touches the schema out-of-band.

The one documented exception is a **one-time data import** during a provider switch — see `references/migration-from-extension.md`. Outside that specific flow, the rule is absolute: schema changes go through migration files, migration files get applied by the deploy.

## Not the legacy "Netlify DB" extension

The older **Netlify DB** extension (Beta) is **deprecated**. It is a separate product and must not be confused with Netlify Database. Do not recommend or install it for new projects.

| | Netlify Database (GA, recommended) | Netlify DB extension (deprecated Beta) |
|---|---|---|
| Package | `@netlify/database` | `@netlify/neon` |
| Env var | `NETLIFY_DB_URL` | `NETLIFY_DATABASE_URL` |
| Setup | `netlify database init` or install the package — auto-provisioned at deploy | Historically `netlify db init` on older CLI versions, with a claim into the user's Neon account; that flow is no longer reachable from the current CLI |
| Status | GA | Deprecated; new creation blocked as of April 2026 |

If an existing project is already using the `@netlify/neon` extension, keep it working and encourage the user to switch. See `references/legacy-extension.md` for recognition and coexistence, and `references/migration-from-extension.md` for the full switching process (also covers switching from other external Postgres providers).

## Provisioning

The fastest path is `netlify database init` — an interactive setup that installs `@netlify/database`, lets the user pick Drizzle or raw SQL, writes `drizzle.config.ts` if needed, scaffolds a starter migration, applies it locally, and runs a sample query end-to-end:

```bash
netlify database init           # interactive
netlify database init --yes     # accept defaults — for CI/agents
```

If you'd rather wire things up by hand, install the package directly:

```bash
npm install @netlify/database
```

Either way, the presence of `@netlify/database` in the dependency tree triggers provisioning on the next deploy. A database can also be created manually from the Netlify UI before first deploy, but the package + deploy path is the supported automation flow.

### Provisioning workflow: preview-first

The supported inner loop is **preview-first**, not `--prod`-first:

1. **First deploy: `netlify deploy`** (no `--prod`). This provisions the database if needed, applies any pending migrations to the production branch, and produces a draft URL. Verify the deploy log shows `Netlify Database setup completed in <n>s` (and, if migrations exist, `Loading migrations from netlify/database/migrations directory`) before continuing.
2. **User verifies on the draft URL** — and completes any dashboard-only setup along the way (e.g., enabling Identity if the project also uses it; see `netlify-identity/SKILL.md`).
3. **Promote: `netlify deploy --prod`**.

Why preview-first matters: the preview deploy provisions the database and applies migrations exactly the way the production deploy will, so a failure during preview is recoverable without prod ever entering a half-configured state. `--prod`-first works in the happy case but is harder to recover from when something goes wrong.

### If the first deploy fails to provision the database

**Symptom:** the build (or the Netlify Database setup extension inside the build) fails with a `401 Access Denied` on `createSiteDatabase`, typically on the very first deploy of a brand-new site. The deploy log shows the failure inside the extension's setup step.

**If the failure happened on `netlify deploy --prod` as the very first deploy**, the first thing to try is the supported preview-first flow — run `netlify deploy` (no `--prod`). The failure has only been observed on `--prod`-first attempts on brand-new sites.

**If a preview deploy also fails — or the original failure was already on a preview — report the failure to the user and stop.** Do not work around it. Specifically, do not:

- Curl `https://api.netlify.com/...` directly
- Run `netlify api createSiteDatabase` (or any other `netlify api` call to manually create what the platform was supposed to provision)
- Pull auth tokens out of `~/Library/Preferences/netlify/config.json`
- Connect via `psql` to "check on things"

The recovery is to give the user the deploy log URL, the site URL, and the exact error, and let them decide what to do next (file a support issue, recreate the site fresh, switch teams, etc.). Wandering off the happy path is how agents end up deleting the wrong resource — being stuck and clear is much safer than being "helpful" with side-channel calls.

## Drizzle ORM (recommended path)

Drizzle is the recommended way to work with Netlify Database. Prefer Drizzle over writing raw SQL or hand-editing migration files — manual migrations are an edge case (see `references/migrations.md`).

### Install

```bash
npm install @netlify/database drizzle-orm@beta
npm install -D drizzle-kit@beta
```

### Schema file

Create `db/schema.ts`. Define all tables here using Drizzle's schema builder.

```typescript
// db/schema.ts
import { boolean, pgTable, serial, text, timestamp, varchar } from "drizzle-orm/pg-core";

export const items = pgTable("items", {
  id: serial().primaryKey(),
  title: varchar({ length: 255 }).notNull(),
  description: text(),
  isActive: boolean("is_active").notNull().default(true),
  createdAt: timestamp("created_at").defaultNow(),
  updatedAt: timestamp("updated_at").defaultNow(),
});

export type Item = typeof items.$inferSelect;
export type NewItem = typeof items.$inferInsert;
```

Use snake_case strings for column names (`"is_active"`, `"created_at"`) to match Postgres conventions. Drizzle variable names can be camelCase.

### Drizzle client

Create `db/index.ts`. The adapter on `drizzle-orm/netlify-db` picks the right driver for the runtime automatically.

```typescript
// db/index.ts
import { drizzle } from "drizzle-orm/netlify-db";
import * as schema from "./schema";

export const db = drizzle({ schema });
```

The connection is configured automatically — no connection string needed. If your project uses native ESM with `.js` extensions on relative imports (`from "./schema.js"`), keep that style consistent here.

### Drizzle Kit config

Create `drizzle.config.ts` at the project root. Set `out` to `netlify/database/migrations` — that's the directory the deploy applies migrations from:

```typescript
// drizzle.config.ts
import { defineConfig } from "drizzle-kit";

export default defineConfig({
  dialect: "postgresql",
  schema: "./db/schema.ts",
  out: "netlify/database/migrations",
});
```

### Package scripts

```json
{
  "scripts": {
    "db:generate": "drizzle-kit generate",
    "db:migrate": "netlify database migrations apply"
  }
}
```

- `db:generate` writes a new migration file under `netlify/database/migrations/` from the current schema.
- `db:migrate` applies pending migrations to the **local development database only**, via the CLI. Hosted migrations (preview branches, production) are applied by the deploy — never by this script.

### Schema-change workflow

1. Edit `db/schema.ts`.
2. `npm run db:generate` — writes a new file into `netlify/database/migrations/`.
3. Review the SQL.
4. `npm run db:migrate` — applies it to the local development DB for testing.
5. Commit the schema change and migration file together and push. The deploy applies the migration to the preview branch, then to production on publish.

### Query patterns

```typescript
import { db } from "./db";
import { items } from "./db/schema";
import { eq, desc } from "drizzle-orm";

// Select all
const all = await db.select().from(items);

// Select with condition
const [one] = await db.select().from(items).where(eq(items.id, id)).limit(1);

// Ordering and limit
const recent = await db.select().from(items).orderBy(desc(items.createdAt)).limit(10);

// Insert
const [created] = await db.insert(items).values({ title: "New" }).returning();

// Update
const [updated] = await db.update(items).set({ title: "Updated" }).where(eq(items.id, id)).returning();

// Delete
await db.delete(items).where(eq(items.id, id));
```

Full migration workflow, expand-and-contract for breaking schema changes, and production DML migrations are in `references/migrations.md`.

## Native driver (when Drizzle isn't a fit)

When a project wants raw SQL, uses a different query builder (Kysely, etc.), or has a library that needs a `pg.Pool`, use the native driver exposed by `@netlify/database`.

```bash
npm install @netlify/database
```

```typescript
import { getDatabase } from "@netlify/database";

const db = getDatabase();

// Tagged template — parameters are safely bound, not interpolated
const users = await db.sql`SELECT * FROM users WHERE active = ${true}`;

// Insert with RETURNING
const [user] = await db.sql`
  INSERT INTO users (name, email)
  VALUES (${name}, ${email})
  RETURNING *
`;

// Bulk insert
const rows = db.sql.values([
  ["Ada", "ada@example.com"],
  ["Bob", "bob@example.com"],
]);
await db.sql`INSERT INTO users (name, email) VALUES ${rows}`;
```

Transactions go through `db.pool` so `BEGIN`, the queries, and `COMMIT`/`ROLLBACK` all run on the same connection:

```typescript
import { getDatabase } from "@netlify/database";

const db = getDatabase();
const client = await db.pool.connect();
try {
  await client.query("BEGIN");
  await client.query("INSERT INTO users (name, email) VALUES ($1, $2)", [name, email]);
  await client.query("INSERT INTO posts (author_id, title) VALUES ($1, $2)", [id, title]);
  await client.query("COMMIT");
} catch (e) {
  await client.query("ROLLBACK");
  throw e;
} finally {
  client.release();
}
```

For third-party tools that need a raw connection string, import `getConnectionString` from `@netlify/database` — but prefer `getDatabase()` for application code.

### Manual migrations

With the native driver, scaffold migration files via the CLI:

```bash
netlify database migrations new -d "create users table"
```

This creates `netlify/database/migrations/<prefix>_<slug>/migration.sql` and prompts for the numbering scheme if it can't be detected from existing files. Open the file and write the SQL. The CLI auto-detects an existing scheme; for new projects it'll ask — choose `timestamp` unless you have a reason not to.

You can also write the file by hand if you prefer. Two layouts are supported:

- **Flat:** `netlify/database/migrations/<prefix>_<slug>.sql`
- **Subdirectory:** `netlify/database/migrations/<prefix>_<slug>/migration.sql` (what `migrations new` produces)

In both, `<prefix>` is digits (timestamp like `20260417143022` or sequential like `0001`) and `<slug>` is lowercase letters, numbers, hyphens, or underscores. Files apply in lexicographic order. See `references/migrations.md`.

Once a migration has been applied to any database, never modify it — roll forward with a new migration instead.

## Connection — don't reach for the env var

`NETLIFY_DB_URL` is set automatically across builds, functions, edge functions, and local dev. Use the `getDatabase()` / `getConnectionString()` helpers above rather than reading it directly — only reach for the raw env var for third-party tools that demand a bare string.

`NETLIFY_DB_URL` is intentionally different from the legacy extension's `NETLIFY_DATABASE_URL`. The two coexist so a project mid-migration doesn't break. Don't rename between them.

## Preview branching

Each deploy preview runs against its own database branch forked from production data. Schema and data changes in a preview do not affect production until the branch is merged and published. This means:

- Migrations run against the preview branch first — failures fail the preview, not production.
- Ad-hoc edits in a preview (via the Netlify UI data browser or a direct client) do **not** propagate to production. Always express production changes as migrations.

## Production data changes — write a DML migration

When a user asks for data changes that should land in production (seed data, backfills, one-off cleanups, CSV imports), **do not connect to the production database and run queries**. Generate a DML migration in `netlify/database/migrations/` (SQL `INSERT`/`UPDATE`/`DELETE`, or a Drizzle-generated equivalent). Tell the user you created a data migration and that merging to production will apply it. Let them verify in the preview branch first.

If the request is ambiguous ("update this record"), confirm that the user wants a production migration rather than a preview-only edit. See `references/migrations.md`.

## Netlify CLI commands for Netlify Database

The CLI ships a complete database surface under `netlify database` (alias: `netlify db`). Requires CLI 26.0.0+. Most commands accept `--json` for machine-readable output — useful when scripting or reading results from an agent.

Full per-command reference — `init`, `status`, `connect`, `migrations new` / `apply` / `pull` / `reset`, and `reset` — is in `references/cli-commands.md`. The one rule that applies across all of them: **never run DDL (`CREATE`/`ALTER`/`DROP`/`TRUNCATE`) through `connect`, `psql`, or any direct connection** — schema changes go through migration files.

## Iterating on migrations

When a migration you generated needs to change, what you do depends on whether it's been applied anywhere yet:

- **Already applied** to any database (local dev DB, a preview branch, or production) → treat as immutable. Roll forward with a new migration that applies the correction.
- **Only on disk** (not yet applied anywhere) → don't edit the SQL or snapshot files by hand. Run `netlify database migrations reset`, update `db/schema.ts`, then re-run `npm run db:generate`. Hand-editing desyncs Drizzle Kit's internal state and tends to produce broken migrations on the next generate.

## Local development

`netlify dev` runs the project against a local Postgres-compatible database — no remote connection, no risk of touching production. Use `netlify database migrations apply` to apply pending migrations locally, `netlify database connect` to query, and `netlify database reset` to wipe and replay. See `references/local-dev.md`.

## Common mistakes

1. **Forgetting the `@beta` dist-tag.** `drizzle-orm` and `drizzle-kit` must be installed as `@beta`. The `latest` releases lack the `drizzle-orm/netlify-db` adapter.
2. **Wrong migration output directory.** Drizzle Kit defaults to `drizzle/`. Set `out: "netlify/database/migrations"` in `drizzle.config.ts` — migrations outside that directory are not applied by the deploy.
3. **Writing raw `CREATE TABLE` when using Drizzle.** The schema file is the source of truth. Define tables in `db/schema.ts` and generate migrations.
4. **Running `drizzle-kit migrate` or `push` against a hosted DB.** Never. The deploy applies migrations. For local, use `netlify database migrations apply` instead.
5. **Using `netlify database connect` to change schema.** Schema changes go through migration files — never DDL through `connect` or any direct connection.
6. **Misunderstanding `netlify database migrations reset`.** It only deletes unapplied files. It cannot undo an applied migration — for that, roll forward with a new migration.
7. **Assuming `netlify dev` applies migrations automatically.** It doesn't — only the deploy does. Run `netlify database migrations apply` locally yourself.

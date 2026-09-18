# Rover Schema Commands

Commands for **exploring** a GraphQL schema: get a structured overview, zoom into a single type or field, or search for types and fields by keyword. These are designed for agent-driven schema discovery — an agent can search → describe → write a query in a closed loop, without loading a huge SDL into its context.

> **Local and offline — these take SDL, not a graph ref.** `rover schema describe` and `rover schema search` read SDL from a **file or from stdin only**; they do not call GraphOS and need no authentication. Unlike other rover commands, passing a graph ref fails:
>
> ```bash
> ❌ rover schema describe my-graph@current
> ✅ rover graph fetch my-graph@current | rover schema describe -
> ```
>
> **Pipe — don't read the raw SDL.** Running `rover graph fetch`/`introspect` on its own dumps the whole schema into context; always pipe it into `describe`/`search` so only the compact result reaches you. To explore a graph that lives in GraphOS, fetch its schema first and pipe it in — see [GraphOS Schema Exploration](#graphos-schema-exploration).

## schema describe

Describe a schema by type, field, or directive. With no coordinate it prints a schema overview; with `--coord` it zooms into a single element.

```bash
# Schema overview (type counts, root operations)
rover schema describe schema.graphql

# Describe one type
rover schema describe schema.graphql --coord User

# Describe one field
rover schema describe schema.graphql --coord User.posts

# Expand referenced types one level deep
rover schema describe schema.graphql --coord User --depth 1

# Describe a directive
rover schema describe schema.graphql --coord @deprecated

# Raw SDL excerpt for the coordinate instead of a description
rover schema describe schema.graphql --coord User --view sdl

# Read from stdin (omit the file or pass -)
cat schema.graphql | rover schema describe
cat schema.graphql | rover schema describe - --coord User

# Machine-readable output
rover schema describe schema.graphql --coord User --format json
```

**Coordinate forms** (apollo-compiler `SchemaCoordinate` syntax):

| Form | Matches |
|------|---------|
| `Type` | object, interface, enum, input, scalar, or union |
| `Type.field` | field on an object/interface, or value on an enum/input |
| `Type.field(arg:)` | argument on a field |
| `@directive` | directive definition |
| `@directive(arg:)` | argument on a directive |

**Options:**
| Option | Description |
|--------|-------------|
| `[FILE]` | SDL file to read. Omit or pass `-` to read from stdin. |
| `--coord, -c <COORDINATE>` | Schema coordinate to inspect. Omit for a full overview. |
| `--depth, -d <N>` | Inline referenced type definitions up to N levels deep (types/fields only; default `0`). |
| `--include-deprecated` | Show deprecated fields and enum values. |
| `--view, -v <VIEW>` | Output view: `description` (default) or `sdl`. |
| `--format json` | Machine-readable JSON output. Works on the subcommand or top-level (`rover --format json schema describe ...`). |

> Field coordinates automatically include the field's argument and return types, so a single `--coord Type.field` call gives an agent enough context to use it.

## schema search

Find types and fields by keyword. Each result is a schema coordinate plus the path(s) from a root operation that reach it — enough to write a query from a single search.

```bash
# Single keyword
rover schema search schema.graphql email

# Multiple terms — all must match (AND)
rover schema search schema.graphql "create post"

# Comma-separated clauses — any clause matches (OR)
rover schema search schema.graphql "email, displayName"

# Limit results (default 10)
rover schema search schema.graphql author --limit 20

# Include deprecated members
rover schema search schema.graphql id --include-deprecated

# Read from stdin (FILE must be -)
cat schema.graphql | rover schema search - user

# Machine-readable output
rover --format json schema search schema.graphql email
```

Example output:

```
1 result for "email"

User.email — The user's email address
  field  ·  via Query.user, Mutation.createPost -> Post.author
```

The `via` line lists complete paths from a `Query`/`Mutation` root to the match, with intermediate types included — so an agent can turn a result straight into an operation.

**Ranking** — results are ordered by match tier (strongest first), then alphabetically by coordinate. Names are split on camelCase / snake_case and matching is case-insensitive:

| Tier | Matches when the term… |
|------|------------------------|
| Exact | is a substring of the name or a name token |
| Stem | shares an English stem with a name token |
| Fuzzy | is within one edit of a name token (terms ≥ 4 chars; shorter terms must match a token exactly) |
| Description | appears in the SDL description, with no name match |

**Options:**
| Option | Description |
|--------|-------------|
| `<FILE>` | SDL file to read (required). Pass `-` to read from stdin. |
| `<TERMS>...` | Search terms (required). Space-separated = all match (AND); comma-separated = OR clauses. |
| `--limit, -n <N>` | Maximum number of results (default `10`). |
| `--include-deprecated` | Include deprecated fields and enum values. |
| `--format json` | Machine-readable JSON output. Works on the subcommand or top-level. |

## GraphOS Schema Exploration

`schema describe` and `schema search` work on local SDL, so to explore a graph registered in GraphOS you fetch its schema first and pipe it in. Any `rover ... fetch` command prints SDL to stdout in its default (`plain`) format, so it pipes directly.

> **Authentication:** the fetch step calls GraphOS and needs auth (`rover config auth` or `APOLLO_KEY`) and a graph reference (`graph@variant`). The `schema describe` / `schema search` step is local and needs neither.

**Fetch sources:**

| Command | Returns |
|---------|---------|
| `rover graph fetch <GRAPH_REF>` | API schema (client-facing) — **best default** for discovering what clients can query; omits federation internals |
| `rover subgraph fetch <GRAPH_REF> --name <NAME>` | one subgraph's schema (with federation directives) |
| `rover supergraph fetch <GRAPH_REF>` | full supergraph SDL — includes federation internals (`join__`/`link__` types); use only for composition/federation inspection |

**Pipe directly (no temp file):**

```bash
# Overview of a GraphOS graph
rover graph fetch my-graph@current | rover schema describe

# Find fields by keyword
rover graph fetch my-graph@current | rover schema search - "playback"

# Zoom into a coordinate from the search results
rover graph fetch my-graph@current | rover schema describe - --coord <Type.field> --depth 1
```

**Save once, explore repeatedly** (more efficient for large schemas):

```bash
rover supergraph fetch my-graph@current > schema.graphql
rover schema search   schema.graphql "playback"
rover schema describe schema.graphql --coord <Type.field> --depth 1
```

A local running server works too, via introspection:

```bash
rover subgraph introspect http://localhost:4001/graphql | rover schema search - "user"
```

## Closed-Loop Agent Workflow

With these two commands an agent can go from a vague request to an executable query with no human guidance:

```bash
# 1. What's in this graph?
rover graph fetch mcp-showcase-spotify@current | rover schema describe

# 2. Find the relevant fields — returns Player.currentlyPlaying
#    via Query.me -> CurrentUser.player
rover graph fetch mcp-showcase-spotify@current | rover schema search - "currently playing"

# 3. Expand the type on the returned path
rover graph fetch mcp-showcase-spotify@current | rover schema describe - --coord Player.currentlyPlaying --depth 1

# 4. Write and run the query using the `via` path from step 2.
```

When piping, prefer the save-once pattern in step 2–3 if you run several searches against the same graph — it avoids re-fetching.

**Running it (step 4):** Rover does not execute operations. Get the endpoint — `rover subgraph list <graph@variant>` shows the **Routing Url** for a single-subgraph graph, or use the router URL from GraphOS Studio (for a cloud router, `rover cloud config fetch <graph@variant>`) for a federated one — then send the query with `curl`. Don't hunt for it via the Platform API; the API key lives in Rover's profile/keychain, not `$APOLLO_KEY`.

## Tips

- **`search` vs `describe`:** use `search` to find a field by concept/keyword — it surfaces **nested** fields with their path from a root operation. Use `describe` for the overview or a known coordinate. The overview lists only root fields, so `search` is how you locate nested ones (e.g. `search "service provider"` → `Launch.launchServiceProvider`, which no overview shows).
- These commands are offline; only the `fetch`/`introspect` step needs network and auth.
- Use `--coord Type.field --depth 1` to pull a field plus its argument and return types in one call.
- Use `rover --format json schema search ...` (or `describe`) when a script or tool consumes the output.
- For natural-language / semantic search (vector-based), see the `apollo-mcp-server` skill — `rover schema search` is keyword/fuzzy (lexical) matching.

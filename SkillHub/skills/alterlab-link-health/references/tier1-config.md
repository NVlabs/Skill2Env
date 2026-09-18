# Tier 1 — Config

Goal: eliminate CI-level false positives with a single reviewable commit that introduces three artefacts at the repo root.

## Files to create

1. `.lychee.toml` — lychee's config file (auto-discovered).
2. `.lycheeignore` — regex-per-line exclusion list.
3. `.github/workflows/check-links.yml` — hardened workflow.

## `.lychee.toml` template

```toml
# lychee.toml — auto-discovered at repo root by lychee-action.

# HTTP status codes treated as success. The CLI `--accept` flag REPLACES
# lychee's default accept set rather than extending it — a common footgun.
# Configuring the list here makes it explicit and additive.
accept = ["200..=299", "301", "302", "304", "308", "400", "403", "429"]

# Cache results between scheduled runs. lychee writes `.lycheecache`.
cache = true

# Per-request timeout. 30s gives slow academic mirrors a fair chance.
timeout = 30

# Back-off before retrying a failed request.
retry_wait_time = 5

# Retry transient failures (5xx, network errors, 429) up to this many times.
# 5 absorbs most DOI / publisher flakes without bloating CI time.
max_retries = 5

# Follow redirect chains common to DOIs and archive.org links (3-5 hops).
max_redirects = 10

# Paths to skip entirely.
exclude_path = ["node_modules", ".git", ".github/ISSUE_TEMPLATE"]

# Placeholder / example DOIs deliberately included in templates.
exclude = [
  "^https?://doi\\.org/x+$",
  "^https?://doi\\.org/10\\.x+",
  "^https?://doi\\.org/xx\\.",
  "^https?://doi\\.org/10\\.xxx/yyy",
  "^https?://doi\\.org/10\\.xxxx/yyyy",
  "^https?://doi\\.org/xx\\.xxx/yyyy",
  "^https?://your-tenant\\.benchling\\.com/.*",
]
```

### Why each `accept` code

- `200..=299` — normal success.
- `301, 302, 304, 308` — redirects; combined with `max_redirects = 10` covers DOI → publisher chains.
- `400` — GraphQL endpoints (e.g. `api.gnomad.broadinstitute.org`, `data.rcsb.org/graphql`) return 400 on GET; they're alive but require POST.
- `403` — academic / publisher sites (BMJ, Oxford Academic, Sage, OECD, Ensembl) bot-block HEAD requests even when content is public.
- `429` — rate-limited responses on retry are transient, not broken links.

**Do not** blanket-accept `500..=504`. Those indicate upstream infrastructure problems. Handle per-host in `.lycheeignore` with a comment.

## `.lycheeignore` starter

```
# Badge / shield services — always 200 but noisy.
^https?://img\.shields\.io/.*
^https?://shields\.io/.*
^https?://awesome\.re/.*
^https?://capsule-render\.vercel\.app/.*

# Anti-bot / auth-walled hosts.
^https?://([a-z0-9-]+\.)?linkedin\.com/.*
^https?://(twitter\.com|x\.com|t\.co)/.*

# gitter.im 301s to matrix.to and trips max-redirects.
^https?://gitter\.im/.*
```

Add host-specific entries during Tier 4 (see `tier4-exclusions.md`) with a `#` comment above each group explaining why the host is excluded.

## Workflow (`.github/workflows/check-links.yml`)

```yaml
name: Check Links

on:
  schedule:
    - cron: "0 9 * * 1"
  workflow_dispatch:

permissions:
  contents: read

jobs:
  check-links:
    name: Check for Dead Links
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v5

      - name: Restore lychee cache
        uses: actions/cache@v4
        with:
          path: .lycheecache
          key: cache-lychee-${{ github.sha }}
          restore-keys: cache-lychee-

      - name: Check links in Markdown files
        uses: lycheeverse/lychee-action@v2
        with:
          args: --config .lychee.toml --no-progress "**/*.md"
          output: .lycheecache
          fail: true
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### Hardening checklist

- `actions/checkout@v5` — Node 24 native, avoids the Node 20 deprecation shim.
- `actions/cache@v4` keyed on SHA — consecutive scheduled runs skip already-verified URLs.
- Args reference `.lychee.toml` via `--config` — keep inline args to the glob only.
- `fail: true` — CI fails on residual errors so regressions are visible.
- `permissions: contents: read` — least privilege; the workflow doesn't need write.
- `GITHUB_TOKEN` exposed — lychee authenticates github.com URLs (higher rate limit).

## The gotcha that motivated this tier

The original workflow passed `args: --verbose --no-progress --accept 403 "**/*.md"`. The `--accept` flag **replaces** the default accept set instead of extending it — so every `200 OK` was reclassified as a failure. That single line accounted for the bulk of the 1208 baseline errors. Moving the config to `.lychee.toml` makes the accepted-status set explicit and reviewable, and survives future CLI-flag drift.

**Write the root cause into the PR body**, not just the commit message: "the `--accept 403` flag on the lychee CLI replaces the default accept set rather than extending it — every 200 OK was rejected as a result." That one sentence saves the next person from rediscovering the footgun in six months.

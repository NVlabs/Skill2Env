# Tier 4 — Exclusions

Goal: get the link checker to zero errors (or to a stable documented residual set) by excluding URLs that genuinely cannot be fixed by content changes. Each entry in `.lycheeignore` is a policy decision — not a "make CI green" shortcut.

## Decision: exclude or substitute?

Walk the decision tree before adding an entry:

1. **Is the URL dead?** (`curl -sSI` times out / resolves to 404 / 5xx with no redirect)
   - **Is there a verified-alive replacement?** → Tier 3 substitute.
   - **No verified replacement?** → Exclude here with a `# Reason: <why>` comment. Document in `KNOWN_LINK_DEBT.md`.

2. **Is the URL alive in a browser but failing from CI?**
   - SSL / OCSP revocation failures → Exclude. Cannot be fixed repo-side.
   - Bot-block (anti-scraping 403/451/999) → Exclude. Likewise.
   - HTTP/2 handshake errors from GitHub Actions runners → Exclude. lychee limitation.
   - Transient 5xx or timeout on the flakiest few percent of runs → **First**, bump `max_retries` in `.lychee.toml`. Only exclude if retries don't help.

3. **Is the URL a deliberate placeholder in a template or example?**
   - `doi.org/xxxxx`-style pedagogical filler → Exclude via regex in `.lychee.toml`'s `exclude` array (not `.lycheeignore`) — these belong with config, not policy.
   - `your-tenant.<domain>` tenant placeholders → Same.
   - `localhost:port/*` dev-server references → `.lycheeignore`.

4. **Is the URL in a skill whose upstream is mid-migration?**
   - Example: `docs.pylabrobot.org/*` during the MyST rewrite.
   - **Blanket-exclude with a tracking issue**. Document in `KNOWN_LINK_DEBT.md` § "Upstream migrations" with the issue number. When upstream stabilizes, the issue's closure is the signal to re-audit that skill and remove the exclusion.

## Category rubric

Every `.lycheeignore` block should fit one of these five categories:

| Category | Permanence | Example patterns |
|----------|-----------|------------------|
| **Infrastructure hostility** | Permanent unless host policy changes | `linkedin.com`, `twitter.com`, `*.stlouisfed.org`, `dicom.nema.org`, FDA deep links that bot-block |
| **Pedagogical placeholders** | Permanent (deliberate) | `doi.org/x+`, `your-tenant.benchling.com`, `localhost:*` |
| **Upstream migrations** | Temporary; track in issue | `docs.pylabrobot.org/*` during MyST rewrite |
| **Dead infrastructure, no substitute** | Permanent until someone finds replacement content | `iqtree.org/workshop/molevol2022*` (SSL expired), `fged.org/projects/miame/?` (org defunct) |
| **Fabricated / example DOIs** | Permanent (deliberate) | Illustrative citations in writing-tool templates |

Each block of lines in `.lycheeignore` should have a `# <category>: <specific reason>` comment above it. Maintainers reading the file six months from now need to know the **why** for each pattern.

## `.lycheeignore` syntax

One regex per line. Lychee treats lines as case-sensitive POSIX-ish regex anchored with `^`. Standard escapes apply.

```
# Category + specific reason on the line above each block.

# Infrastructure hostility — bot-blocks on CI runners.
^https?://([a-z0-9-]+\.)?linkedin\.com/.*
^https?://(twitter\.com|x\.com|t\.co)/.*

# Pedagogical placeholders — template-example DOIs.
^https?://doi\.org/10\.1038/nrd\.2023\.001$
```

**Prefer host-level exclusions over full-URL exclusions** when the category is permanent (e.g. `linkedin.com/*`), because individual page changes on those hosts would otherwise require ignoring-list maintenance each time a skill touches the host.

**Use specific-URL exclusions** for dead-infrastructure cases, because excluding the whole host would hide legitimate future-working pages on the same domain.

## Retries before exclusions

If a URL is live-in-browser but flaky from CI, exhaust the config knobs first:

- `max_retries = 5` in `.lychee.toml` (up from the default 3).
- `retry_wait_time = 5` or higher — gives transient services time to recover.
- `timeout = 30` or higher for slow academic mirrors.

Only exclude a flaky URL after retries fail across multiple dispatches. A single CI flake is not evidence of a dead link.

## Documenting debt

Every exclusion gets a row in `.github/KNOWN_LINK_DEBT.md` (see `references/known-debt-template.md`). The file is the durable record of **why** each exclusion exists — `.lycheeignore` comments get lost in diffs over time, but a well-structured debt doc stays reviewable.

Minimum row content: URL pattern, category, reason, date excluded, revisit trigger (or tracking issue).

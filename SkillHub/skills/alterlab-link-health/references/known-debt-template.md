# `KNOWN_LINK_DEBT.md` — Template

Every repo that runs this skill should ship a `.github/KNOWN_LINK_DEBT.md` documenting every `.lycheeignore` entry with rationale. The file is the durable memory of **why** each exclusion exists.

## Structure

Five category sections, in this order. Empty sections keep their header with "No current entries." — the presence of the category keeps maintainers from re-categorizing when future entries land.

```markdown
# Known Link Debt

URLs excluded from link checking that warrant future review. Each entry explains *why* the exclusion exists so maintainers do not need to reconstruct context. Keep this file in sync with `.lycheeignore` — if you add or remove an exclusion pattern, update the corresponding row here (or add a new one with rationale).

## Categories

### Infrastructure hostility (permanent)

URLs where the host systematically blocks or fails for CI runners, regardless of any fix on our side. Rows are permanent unless the host changes policy.

| URL pattern | Reason | Date excluded | Revisit trigger |
| --- | --- | --- | --- |
| `<host>/*` | <why CI always fails> | YYYY-MM-DD | <what would change to revisit> |

### Upstream migrations (temporary)

Exclusions expected to be removed once upstream projects finish doc restructures. Each row tracks an issue to reassess.

| URL pattern | Reason | Date excluded | Tracking issue |
| --- | --- | --- | --- |
| `<host>/*` | <upstream state> | YYYY-MM-DD | #<issue> |

### Pedagogical placeholders (deliberate)

URLs that are intentional filler in template or example files. They demonstrate a citation FORMAT, not real resources. These should stay excluded indefinitely.

| URL pattern | Reason |
| --- | --- |
| `<regex>` | <pedagogical use case> |

### <Language/domain> journal / resource DOIs (needs native reader review)

<Optional: only if the repo has DOIs that a native-language or domain-expert reader should verify against source citations. Omit section if N/A.>

- `<DOI>` ← <note on suspected issue>

### Dead substitutions (review for replacement)

URLs where the original target is dead and no verified replacement has been committed. Empty state is the goal — populating this section means somebody guessed and left a breadcrumb for future verification.

No current entries.

## Maintenance

- When adding to `.lycheeignore`, add a row here with reason + date.
- When removing an entry from `.lycheeignore` (because upstream fixed the issue), delete the corresponding row here.
- Entries in "Upstream migrations" should link a tracking issue; close the entry when the issue resolves.
```

## Sync discipline

A `.lycheeignore` entry without a corresponding `KNOWN_LINK_DEBT.md` row is a bug. Add a CI check (or a CODEOWNERS comment on `.lycheeignore` changes) that requires both files to change together in any PR that modifies either. The two files must stay in sync or the debt doc becomes lying-by-omission.

## Writing good reasons

Good reason text answers three questions in one or two sentences:

1. What's wrong with the URL from CI's perspective?
2. Why can't we fix it with a substitute or accept-list change?
3. What would have to change upstream (or in tooling) for us to re-include this URL?

Example:

> **`*.stlouisfed.org/*`** — Consistently fails HTTP/2 handshakes from GitHub Actions runners (live from desktop). `max_retries = 5` doesn't help; handshake fails deterministically per-host. **Revisit when** lychee's HTTP/2 handling improves or GitHub Actions runners update their libcurl.

Bad reason text:

> **`*.stlouisfed.org/*`** — Fails in CI.

The bad version loses the "HTTP/2 handshake" detail and the revisit trigger — six months later someone reading this has to rediscover both.

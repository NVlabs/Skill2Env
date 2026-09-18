# Tier 3 — External URL substitution

Goal: replace MOVED or DEAD external URLs with verified replacements. This tier is where most self-inflicted regressions happen. Two rules are non-negotiable.

---

## THE GUARDRAIL

> **After any URL substitution pass, re-run the link checker and diff against the baseline success set. Any URL that returned 200 OK in baseline and is non-200 after substitution is a regression and MUST be reverted before commit.**
>
> **Self-check:**
>
> ```bash
> diff <(grep "^\[200\]" baseline.log | sort -u) \
>      <(grep "^\[200\]" post.log | sort -u)
> ```
>
> **Deletions are regressions.** The diff should show only additions (URLs that were failing in baseline and now pass). Any `< ` line is a URL you broke.

### Why this rule exists

During the source audit of this skill, a broad `sed` substitution pipeline applied prefix rewrites across the skill tree. Three of those rewrites had unintended collateral:

- `/v3/` → `/v3/docs` also matched URLs already ending in `/v3/docs`, producing `/v3/docsdocs`.
- `docs.pylabrobot.org/api/` → `docs.pylabrobot.org/user_guide/index.html` concatenated onto more specific paths, producing `user_guide/index.htmlpylabrobot.*.html`.
- `clinvar/docs/` → `clinvar/docs/help/` rewrote specific sub-paths like `clinvar/docs/xsd_public/` into non-existent `clinvar/docs/help/xsd_public/`.

None of these was caught by the commit's own review — they surfaced only when the link checker re-ran on the branch. **Assume your Tier 3 pass will have at least one such bug. Plan for the diff check.**

---

## THE VERIFICATION RULE

> **DEFAULT to probe-verification before any URL substitution. Unverified substitutions are how phantom URLs land in public skills.**

For every proposed `[old] → [new]`:

| Target type | Probe |
|-------------|-------|
| GitHub repo or user | `gh api repos/owner/name` — status must be 200 and `"archived": false` |
| HTTP URL | `curl -sSI -L --max-time 15 '<new>'` — final status 200 after redirects |
| PyPI / npm / crates package | Hit the registry landing page or API directly |
| Google Cloud / marketplace | Often fails HTTP/2 handshakes from CI even when alive — probe with `--http1.1` flag before trusting |

**If verification fails**, the correct action is to **exclude the dead target** via `.lycheeignore` with a commented rationale — **not** to guess a plausible-looking replacement.

Real example from the source audit:

```
Proposed: github.com/benchling/benchling-sdk → github.com/benchling/benchling-api-client
Probe:    gh api repos/benchling/benchling-api-client  →  404 Not Found
Action:   Exclude github.com/benchling/benchling-sdk.* in .lycheeignore.
          (Later, verified pypi.org/project/benchling-sdk/ returns 200 — substituted to PyPI in the post-merge cleanup.)
```

A wrong substitution that looks plausible is worse than an acknowledged exclusion: it misleads readers and is harder to spot in review.

---

## Sed-safety patterns

Bulk URL rewriting via `sed -f <scriptfile>` is faster than a hand-written `Edit` per file, but has sharp edges.

### Use a delimiter URLs don't contain

URLs contain `/` constantly and sometimes `&`, `|`, `%`. Pick `|` only if no URL has a pipe; otherwise `~` is a safe default:

```bash
sed -E 's~OLD~NEW~g'
```

### Anchor prefix substitutions

A rule like `s~cbioportal.org/api/~cbioportal.org/api/swagger-ui/index.html~g` will catch more specific paths you didn't intend. Anchor by the end of the URL when possible:

```bash
# Wrong — catches cbioportal.org/api/foo → cbioportal.org/api/swagger-ui/index.htmlfoo
s~cbioportal\.org/api/~cbioportal.org/api/swagger-ui/index.html~g

# Right — only matches the bare endpoint
s~cbioportal\.org/api/"~cbioportal.org/api/swagger-ui/index.html"~g
```

Or: make the old string more specific (include surrounding context) so accidentally overlapping targets aren't matched.

### Order matters

When one rule's `NEW` is a prefix of another rule's `OLD`, chain-substitutions can cascade. Either:

- Apply specific rules first, general rules last (so general rules don't see the specific rule's output), **or**
- Run each rule against the **original** file content (use `-e` with `sed` and read-modify-write explicitly, or apply rules one at a time with `git diff` inspection between).

### Scripted batches

For many substitutions, put them in a `.sedfile` and apply once per file:

```bash
find skills -type f -name '*.md' -print0 \
  | xargs -0 sed -i -f tier3.sedfile
```

This is ~100× faster than `xargs sed -i -e '<expr>' -e '<expr>' ...` for every rule.

---

## Probe-before-commit workflow

1. Compile the `[old] → [new]` proposal list (from agent reports or your own triage).
2. Batch-probe: loop over each `[new]` with `curl -sSI -L --max-time 15` or `gh api`. Emit a TSV of `old \t new \t status`.
3. Drop every proposal where `[new]` is not 200/2xx from the TSV. Those move to Tier 4 exclusions.
4. Apply the filtered sed script.
5. **Rerun the link checker.**
6. Run the guardrail diff. If any previously-200 URL is now non-200, that substitution is a regression — revert the specific sed rule or manually restore the URL.
7. Only then commit.

---

## Dealing with unavoidable regressions

Sometimes a correct substitution still surfaces a new error downstream: e.g. your new GCP marketplace URL for AlphaFold is correct but returns HTTP/2 errors from the CI runner. That's not a regression of a previously-working URL — the baseline didn't include this URL at all — so it's a **new residual**, not a violation of the guardrail.

New residuals get cleaned up in Tier 4 (`tier4-exclusions.md`), not reverted.

The guardrail is strict about one thing only: **don't make a previously-passing URL fail**.

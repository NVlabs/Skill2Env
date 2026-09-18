---
name: library-pack
description: Supply-chain security for published packages: OpenSSF Scorecard, npm provenance, PyPI Trusted Publishing, SBOM (Syft/CycloneDX), semver enforcement, deprecation policy
when_to_use: Building SDKs, CLIs, compilers, IDE plugins, npm/PyPI/crates packages — anything published as a dependency for others
applies_to:
  - library
---

# Library Pack

> Extends `library` archetype with deep supply-chain security, semver discipline, and distribution patterns for SDKs, CLIs, npm packages, PyPI packages, Rust crates, Go modules, plugins.
> Auto-loaded when `archetype: library` is detected in PROJECT.md.
> Also loaded explicitly via `packs: [library-pack]`.

## Why this pack matters

Libraries are the **biggest supply-chain attack surface**. One compromised package poisons every project that depends on it. Recent examples:

- `event-stream` (npm, 2018) — typosquat replaced legit maintainer, drained Bitcoin wallets
- `colors` / `faker` (npm, 2022) — maintainer self-sabotage, infinite loop in production
- PyTorch nightly (Dec 2022) — malicious `torchtriton` typosquat
- `xz-utils` (Mar 2024) — multi-year social engineering against systemd dependency
- npm `@solana/web3.js` (Dec 2024) — backdoored versions stole keys

If you ship a library, you owe downstream consumers a higher bar than you'd accept for your own app.

## OpenSSF Scorecard — minimum baseline

Run [Scorecard](https://github.com/ossf/scorecard) on every commit to main. Target score: **≥ 7.5/10**.

```bash
# Install
go install github.com/ossf/scorecard/v4@latest

# Run
scorecard --repo=github.com/<org>/<repo>
```

Critical checks (must pass):

| Check | Threshold | Why |
|-------|-----------|-----|
| **Branch-Protection** | Required reviews on main | Prevents single-actor compromise |
| **Code-Review** | All commits reviewed | Catches malicious changes pre-merge |
| **Pinned-Dependencies** | All deps pinned by hash in CI | Prevents transitive supply-chain swaps |
| **Token-Permissions** | Workflow tokens use `contents: read` minimum | Limits blast radius if workflow compromised |
| **Signed-Releases** | Releases tagged + signed | Cryptographic proof of authentic release |
| **SAST** | CodeQL or Semgrep on PRs | Catches injection, secrets, common bugs |
| **Vulnerabilities** | No known critical CVEs in deps | Hard fail if found |

`security-officer` runs these automatically when `archetype: library`.

## Provenance — required for npm + PyPI in 2026

Both registries now support cryptographic provenance via Sigstore. **Use it.**

### npm provenance

```yaml
# .github/workflows/publish.yml
name: Publish
on:
  release:
    types: [published]

jobs:
  publish:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      id-token: write   # MANDATORY for provenance
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          registry-url: 'https://registry.npmjs.org'
      - run: npm ci
      - run: npm run build
      - run: npm publish --provenance --access public
        env:
          NODE_AUTH_TOKEN: ${{ secrets.NPM_TOKEN }}
```

This embeds a signed certificate in the published package linking it to the exact GitHub Action workflow that built it. Consumers can verify with `npm audit signatures`.

### PyPI Trusted Publishing (OIDC)

```yaml
# .github/workflows/publish.yml
- uses: pypa/gh-action-pypi-publish@release/v1
  # No token needed — OIDC handles auth via id-token
```

Configure once at https://pypi.org/manage/account/publishing/ — links your PyPI project to a specific GitHub repo + workflow file. No long-lived API token in CI.

### Rust crates.io

Cargo provenance is rolling out (RFC #3724). For now: pin verified publishers, use `cargo crev` for community trust web.

## SBOM generation

Software Bill of Materials — the manifest of what's inside your release.

```bash
# Install Syft (Anchore)
brew install syft

# Generate SBOM in CycloneDX format
syft <package-tarball> -o cyclonedx-json > sbom.json

# Or directly from source
syft . -o cyclonedx-json > sbom.json
```

Attach `sbom.json` to every GitHub Release. Downstream consumers run `grype sbom:./sbom.json` to scan their dependency for CVEs without needing the source.

CI step:

```yaml
- name: Generate SBOM
  run: syft . -o cyclonedx-json > sbom-${{ github.sha }}.json
- name: Upload SBOM
  uses: actions/upload-artifact@v4
  with:
    name: sbom
    path: sbom-${{ github.sha }}.json
- name: Attach to release
  if: startsWith(github.ref, 'refs/tags/')
  uses: softprops/action-gh-release@v2
  with:
    files: sbom-${{ github.sha }}.json
```

## Semver enforcement

| Tool | Language |
|------|----------|
| **semantic-release** | Node — fully automated based on conventional commits |
| **Changesets** | Node monorepo — manual changeset files per PR, batched into release |
| **release-please** | Multi-language (Google) — GitHub Action that opens release PR |
| **cargo-semver-checks** | Rust — detects breaking changes between versions |
| **Sigstore-cosign** | Any — signs release artifacts |

**Semver discipline rules:**

- **PATCH** (x.y.Z): bug fixes, no new public API, no behavior changes for existing API
- **MINOR** (x.Y.0): new public API additions, deprecations (with warnings, not removal)
- **MAJOR** (X.0.0): breaking changes, removals, behavior changes

**Hard rule for libraries**: never break SemVer in a PATCH or MINOR. Run `cargo-semver-checks` (Rust), `api-extractor` (TypeScript), `golang.org/x/exp/cmd/gorelease` (Go), or `mypy --strict` (Python with type stubs) in CI as a gate.

If you must ship a breaking change, do a MAJOR with:
1. Deprecation notice in previous MINOR (at least 90 days before)
2. Migration guide in CHANGELOG
3. Codemod where possible (TypeScript: `ts-morph`; Python: `bowler`/`refactor`)

## Cross-version compat matrix

For runtime libraries, define your support matrix and test against it. Example for a Node library:

```yaml
# .github/workflows/test.yml
strategy:
  matrix:
    node-version: ['20', '22', '24']     # LTS + current
    os: [ubuntu-latest, macos-latest, windows-latest]
```

For Python:

```yaml
strategy:
  matrix:
    python-version: ['3.10', '3.11', '3.12', '3.13']
```

For Rust:

```yaml
strategy:
  matrix:
    rust: [stable, beta, msrv]   # MSRV declared in Cargo.toml
```

Drop a version from your matrix only after 90-day deprecation notice in CHANGELOG.

## Bundle size budget (npm libraries)

Set a budget. Enforce in CI. Don't let a library quietly grow from 5 KB to 500 KB.

```bash
# Install
npm install -D size-limit @size-limit/preset-small-lib

# Configure in package.json
{
  "size-limit": [
    {
      "path": "dist/index.js",
      "limit": "10 KB"
    },
    {
      "path": "dist/index.esm.js",
      "limit": "10 KB"
    }
  ]
}

# Run
npx size-limit
```

Bundle bloat sources to audit:

- Unnecessary dependencies (lodash → use stdlib or fp-ts)
- Bundled types (TypeScript `.d.ts` shouldn't include implementation)
- Including dev tools in dist (test framework imports leaking through)
- Importing from default export of large packages (`import _ from 'lodash'`)

## Tree-shakability — ESM-first

For npm libraries:

```json
// package.json
{
  "name": "my-lib",
  "type": "module",
  "exports": {
    ".": {
      "types": "./dist/index.d.ts",
      "import": "./dist/index.mjs",
      "require": "./dist/index.cjs"
    },
    "./subpath": {
      "types": "./dist/subpath.d.ts",
      "import": "./dist/subpath.mjs",
      "require": "./dist/subpath.cjs"
    }
  },
  "sideEffects": false
}
```

`"sideEffects": false` tells bundlers it's safe to drop unused exports. **Don't lie** — if your library has side effects (CSS imports, polyfill registration), declare them.

## Documentation generation

| Tool | Language |
|------|----------|
| **TypeDoc** | TypeScript |
| **Sphinx** | Python |
| **rustdoc** | Rust (built-in) |
| **godoc / pkgsite** | Go (built-in) |
| **VitePress / Docusaurus** | Hand-written reference + guides |

Publish docs from CI on every release. Host on GitHub Pages, Vercel, or Netlify.

**Bare minimum for a library:**

1. Quickstart (paste this code, see this output, in 30 seconds)
2. API reference (auto-generated from doc comments)
3. Migration guide between MAJOR versions
4. Examples folder (runnable)
5. CHANGELOG (auto-generated from conventional commits)

If a developer can't get from "I found this library" to "first call working" in 90 seconds, you'll lose them.

## Deprecation policy

When you remove or change something:

1. Deprecate in MINOR with `@deprecated` JSDoc tag (TypeScript) / `DeprecationWarning` (Python) / `#[deprecated]` (Rust)
2. Add suggested replacement in deprecation message
3. Wait at least 90 days OR one MAJOR cycle
4. Remove only on next MAJOR

Document each deprecation in `docs/deprecations/DEPRECATION-CALENDAR.md` (great_cto template). `/digest` will surface deprecations within 90 days of EOL.

## Security disclosure

Every library repo MUST have:

- `SECURITY.md` with: contact email, supported versions, response SLA
- Private vulnerability reporting enabled on GitHub (Settings → Code security)
- 24h ack SLA, 90d disclosure window unless coordinated

Template:

```markdown
# Security Policy

## Reporting a Vulnerability
Email security@example.com or use GitHub's [private vulnerability reporting](https://github.com/<org>/<repo>/security/advisories/new).

## Supported Versions
| Version | Supported          |
| ------- | ------------------ |
| 2.x     | ✅ Active          |
| 1.x     | 🔒 Security only (until 2026-12-31) |
| < 1.0   | ❌ Unsupported     |

## Response Timeline
- Acknowledgement: within 24 hours
- Initial assessment: within 7 days
- Fix + disclosure: within 90 days (coordinated)
```

## CLI-specific (when archetype is `cli-tool`)

Beyond library basics:

- **Distribution**: provide single-binary builds (use `pkg`/`nexe` for Node, `pyinstaller` for Python, native for Go/Rust)
- **Installation**: support package managers (Homebrew, Scoop, apt, AUR) + direct download
- **Update channel**: built-in self-update or notification when newer version available
- **Telemetry**: opt-in only, transparent about what's collected, easy to disable
- **Help discoverability**: `--help`, sub-command help, examples in help text
- **Exit codes**: 0 success, 1 generic error, 2 misuse, 64+ for specific failures (sysexits.h)

Distribution example for a Go CLI:

```yaml
# .goreleaser.yml
builds:
  - main: ./cmd/mycli
    binary: mycli
    goos: [linux, darwin, windows]
    goarch: [amd64, arm64]
brews:
  - tap:
      owner: <org>
      name: homebrew-tap
release:
  github:
    owner: <org>
    name: <repo>
```

## Compliance checklist (auto-applied by `security-officer`)

When `archetype: library`:

- [ ] OpenSSF Scorecard ≥ 7.5
- [ ] Branch protection on main (≥ 1 review)
- [ ] CI uses pinned actions (full SHA, not version tags)
- [ ] No hardcoded secrets (gitleaks, trufflehog scan)
- [ ] CVE scan clean (npm audit / pip-audit / cargo audit / govulncheck)
- [ ] Provenance attached on publish (npm `--provenance` or PyPI OIDC)
- [ ] SBOM attached to release
- [ ] SECURITY.md present
- [ ] LICENSE present (MIT/Apache-2.0/BSD recommended for max adoption)
- [ ] Semver-compliant (no breaking change in PATCH/MINOR)
- [ ] CHANGELOG present and current

`security-officer` BLOCKS the release gate if any critical (provenance, SBOM, CVE, secrets) is missing.

## Recommended `PROJECT.md` for new library

```yaml
primary: library-sdk
archetype: library
project_size: small
stack: [typescript, npm]
team-size: 1
compliance: [openssf]
qa-extras: [semver, cross-version-compat, bundle-size]
packs: [library-pack]
```

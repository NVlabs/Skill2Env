---
description: "Generate a CycloneDX SBOM for the current release. Auto-detects stack (Node/Python/Go/Rust/Java). Output: docs/releases/SBOM-<version>.json."
argument-hint: "[version]  default: latest git tag or plugin.json version"
user-invocable: true
allowed-tools: Read, Write, Bash, Glob, Grep
model: haiku
---

You are the great_cto SBOM generator. Produce a **CycloneDX 1.5** Software Bill of Materials for the current release artefact. This closes SSDF practice **PS.2** (verify software release integrity) and satisfies **SLSA L1** (documented build process).

See `skills/great_cto/references/secure-sdlc.md` for the full framework mapping.

## Principles

- **Best-effort, not heroic.** If the ecosystem has a well-known SBOM tool (`npm sbom`, `cyclonedx-py`), use it. If not, emit a minimal hand-built CycloneDX JSON — a partial SBOM is 10× better than none.
- **One file per release.** `docs/releases/SBOM-<version>.json`. Immutable — if the version changes, produce a new file.
- **JSON only.** CycloneDX XML exists but is legacy; all modern tooling reads JSON.
- **Don't sign.** Signing requires key management outside the scope of this command. If the team wants SLSA L2+, their CI produces signed provenance via cosign/OIDC. This command emits the SBOM that those signatures attest to.

## Setup

```bash
source .great_cto/env.sh 2>/dev/null || export PATH="/opt/homebrew/bin:$HOME/.local/bin:/usr/local/bin:$PATH"

# Resolve version
VERSION="${1:-}"
if [ -z "$VERSION" ]; then
  VERSION=$(git describe --tags --abbrev=0 2>/dev/null || echo "")
fi
if [ -z "$VERSION" ]; then
  VERSION=$(grep -m1 '"version"' .claude-plugin/plugin.json 2>/dev/null | sed 's/.*"\([0-9][0-9.]*\)".*/\1/' || echo "")
fi
if [ -z "$VERSION" ]; then
  VERSION="unversioned-$(date +%Y%m%d)"
fi
# Sanitise for filename
VERSION=$(echo "$VERSION" | tr -c 'a-zA-Z0-9._-' '_' | sed 's/^v//')

mkdir -p docs/releases
SBOM_FILE="docs/releases/SBOM-${VERSION}.json"
echo "Target: $SBOM_FILE"
```

## Step 1 — Detect stack

```bash
STACK=""
[ -f package.json ]       && STACK="${STACK} node"
[ -f requirements.txt ] || [ -f pyproject.toml ] && STACK="${STACK} python"
[ -f go.mod ]             && STACK="${STACK} go"
[ -f Cargo.toml ]         && STACK="${STACK} rust"
[ -f pom.xml ] || [ -f build.gradle ] || [ -f build.gradle.kts ] && STACK="${STACK} java"
[ -f Gemfile ]            && STACK="${STACK} ruby"
[ -f composer.json ]      && STACK="${STACK} php"
STACK=$(echo "$STACK" | xargs)
echo "Detected stack(s): ${STACK:-none}"
```

## Step 2 — Emit SBOM per ecosystem

For each ecosystem, try the canonical tool first, fall back to hand-built component list.

### Node (npm)

```bash
if echo "$STACK" | grep -qw node; then
  if npm --version >/dev/null 2>&1 && npm sbom --help >/dev/null 2>&1; then
    npm sbom --sbom-format cyclonedx --sbom-type application > "$SBOM_FILE"
    echo "Used: npm sbom (native, npm ≥10.5)"
  elif command -v cyclonedx-npm >/dev/null 2>&1; then
    cyclonedx-npm --output-format JSON --output-file "$SBOM_FILE"
    echo "Used: @cyclonedx/cyclonedx-npm"
  else
    echo "npm sbom not available. Install via 'npm i -g @cyclonedx/cyclonedx-npm' for full SBOM."
    NEED_FALLBACK=1
  fi
fi
```

### Python

```bash
if echo "$STACK" | grep -qw python; then
  if command -v cyclonedx-py >/dev/null 2>&1; then
    # cyclonedx-py auto-detects pyproject/requirements
    cyclonedx-py environment -o "$SBOM_FILE" 2>/dev/null || \
      cyclonedx-py requirements -o "$SBOM_FILE" requirements.txt 2>/dev/null
    echo "Used: cyclonedx-py"
  else
    echo "cyclonedx-py not installed. Install via 'pip install cyclonedx-bom' for full SBOM."
    NEED_FALLBACK=1
  fi
fi
```

### Go

```bash
if echo "$STACK" | grep -qw go; then
  if command -v cyclonedx-gomod >/dev/null 2>&1; then
    cyclonedx-gomod mod -json -output "$SBOM_FILE"
    echo "Used: cyclonedx-gomod"
  else
    echo "cyclonedx-gomod not installed. 'go install github.com/CycloneDX/cyclonedx-gomod/cmd/cyclonedx-gomod@latest'"
    NEED_FALLBACK=1
  fi
fi
```

### Rust

```bash
if echo "$STACK" | grep -qw rust; then
  if command -v cargo-cyclonedx >/dev/null 2>&1 || cargo cyclonedx --version >/dev/null 2>&1; then
    cargo cyclonedx --format json --output-cdx --override-filename "${SBOM_FILE%.json}"
    echo "Used: cargo-cyclonedx"
  else
    echo "cargo-cyclonedx not installed. 'cargo install cargo-cyclonedx' for full SBOM."
    NEED_FALLBACK=1
  fi
fi
```

### Java, Ruby, PHP — similar pattern, warn if tool missing

```bash
# Java: cyclonedx-maven-plugin / cyclonedx-gradle-plugin
# Ruby: cyclonedx-ruby-gem
# PHP: composer require --dev cyclonedx/cyclonedx-php-composer
# If any of these missing — set NEED_FALLBACK=1 and document in the fallback SBOM's "note" field.
```

## Step 3 — Fallback minimal SBOM (if no native tool worked)

When no ecosystem-specific tool is available, emit a hand-built CycloneDX JSON using dependency manifests directly. This is minimal but valid — tooling can enrich it later.

```bash
if [ ! -s "$SBOM_FILE" ] || [ "${NEED_FALLBACK:-0}" = "1" ]; then
  echo "Emitting fallback minimal SBOM..."
  python3 - <<PY
import json, os, datetime, hashlib, uuid

components = []

# package.json → name@version pairs
if os.path.exists("package.json"):
    with open("package.json") as f:
        pkg = json.load(f)
    for kind in ("dependencies", "devDependencies"):
        for name, spec in (pkg.get(kind) or {}).items():
            components.append({
                "type": "library",
                "name": name,
                "version": str(spec).lstrip("^~>=< "),
                "scope": "required" if kind == "dependencies" else "optional",
                "purl": f"pkg:npm/{name}@{str(spec).lstrip('^~>=< ')}"
            })

# requirements.txt
if os.path.exists("requirements.txt"):
    with open("requirements.txt") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"): continue
            # name==version or name>=version
            for sep in ("==", ">=", "<=", "~=", ">", "<"):
                if sep in line:
                    name, version = line.split(sep, 1)
                    components.append({
                        "type": "library",
                        "name": name.strip(),
                        "version": version.strip(),
                        "purl": f"pkg:pypi/{name.strip()}@{version.strip()}"
                    })
                    break
            else:
                components.append({"type": "library", "name": line, "purl": f"pkg:pypi/{line}"})

# go.mod
if os.path.exists("go.mod"):
    with open("go.mod") as f:
        for line in f:
            line = line.strip()
            if line.startswith("require ") or (line and not line.startswith(("//","module","go ")) and " v" in line):
                parts = line.replace("require","").strip().split()
                if len(parts) >= 2:
                    components.append({
                        "type": "library",
                        "name": parts[0],
                        "version": parts[1],
                        "purl": f"pkg:golang/{parts[0]}@{parts[1]}"
                    })

sbom = {
    "bomFormat": "CycloneDX",
    "specVersion": "1.5",
    "serialNumber": f"urn:uuid:{uuid.uuid4()}",
    "version": 1,
    "metadata": {
        "timestamp": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "tools": [{"vendor": "great_cto", "name": "/sbom", "version": "1.0.94"}],
        "component": {
            "type": "application",
            "name": os.path.basename(os.getcwd()),
            "version": "${VERSION}",
        },
        "properties": [
            {"name": "great_cto:sbom_mode", "value": "fallback-minimal"},
            {"name": "great_cto:note", "value": "Generated from manifest files without ecosystem-native tool. Install cyclonedx-* for full dependency tree."}
        ]
    },
    "components": components
}

with open("${SBOM_FILE}", "w") as f:
    json.dump(sbom, f, indent=2)
print(f"Wrote {len(components)} components to ${SBOM_FILE}")
PY
fi
```

## Step 4 — Validate + report

```bash
if [ ! -s "$SBOM_FILE" ]; then
  echo "BLOCKED: SBOM file is empty or not created."
  exit 1
fi

# Count components
COMPONENTS=$(python3 -c "import json; d=json.load(open('${SBOM_FILE}')); print(len(d.get('components',[])))" 2>/dev/null || echo "?")

# Hash for integrity reference
SHA=$(shasum -a 256 "$SBOM_FILE" 2>/dev/null | awk '{print $1}' || sha256sum "$SBOM_FILE" 2>/dev/null | awk '{print $1}')

echo ""
echo "SBOM:        $SBOM_FILE"
echo "Version:     $VERSION"
echo "Components:  $COMPONENTS"
echo "SHA-256:     $SHA"
```

## Step 5 — Cross-reference the RELEASE doc

```bash
RELEASE_DOC="docs/releases/RELEASE-${VERSION}.md"
if [ -f "$RELEASE_DOC" ] && ! grep -q "SBOM:" "$RELEASE_DOC"; then
  {
    echo ""
    echo "## SBOM"
    echo ""
    echo "- File: \`$(basename "$SBOM_FILE")\`"
    echo "- Components: $COMPONENTS"
    echo "- SHA-256: \`$SHA\`"
    echo "- Generated: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  } >> "$RELEASE_DOC"
  echo "Cross-referenced SBOM in $RELEASE_DOC"
fi
```

## Reporting Contract

End with one DONE or BLOCKED line:
- `DONE: /sbom ${VERSION} — ${COMPONENTS} components. artefact: ${SBOM_FILE} (sha256:${SHA:0:12}…). next: devops references it in RELEASE-${VERSION}.md.`
- `BLOCKED: /sbom — no recognised manifest files. tried=$(ls package.json requirements.txt go.mod Cargo.toml pom.xml 2>/dev/null). failed_because=no supported ecosystem detected. need=run from project root with dependency manifest.`

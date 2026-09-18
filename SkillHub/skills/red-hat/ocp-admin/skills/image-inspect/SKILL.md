---
name: image-inspect
description: Fetch container image labels, validate registry ownership, resolve tag/digest via SBOM, and report the SBOM artifact reference for a Red Hat container image.
license: Apache-2.0
user_invocable: true
model: inherit
color: cyan
---

# Red Hat Container Image Inspector

## When to Use This Skill

Use this skill when the user asks you to inspect, describe, check metadata for, or get information about a Red Hat container image. The user may provide a tag-based or digest-based image reference. Input is taken from conversation context.

## Optional Output Flags

The user may specify an optional output format flag:

- `--format markdown` — (default) Markdown report
- `--format json` — machine-readable JSON object
- `--format csv` — single-row CSV with a header row

Record the resolved value as `OUTPUT_FORMAT` (default: `markdown`). Strip this flag before identifying the image reference.

## Input Validation

Confirm you have a fully qualified container image reference including registry, image name, and tag or digest. It must:
- Contain at least one `/`
- Contain only letters, digits, `.`, `-`, `_`, `/`, `:`, `@` — no spaces or shell metacharacters

If the image reference is missing or invalid, ask the user to provide it. Do not proceed.

## Prerequisites

**Resolve scripts directory:**
```bash
SCRIPTS_DIR="$(git rev-parse --show-toplevel)/ocp-admin/scripts/security-validation"
test -f "$SCRIPTS_DIR/inspect_image.py" || { echo "Error: Scripts directory not found at $SCRIPTS_DIR"; exit 1; }
```
The scripts handle tool checks internally (regctl, cosign) and return clear errors if tools are missing.

## Workflow

### Step 1 — Inspect image metadata

Run the `inspect_image.py` script:
```bash
python $SCRIPTS_DIR/inspect_image.py [IMAGE_REFERENCE]
```

Returns JSON with `labels` (cpe, name, com.redhat.component, vendor, maintainer, org.opencontainers.image.created), `digest`, `architecture`, and `errors`.

If authentication fails, run `regctl registry login registry.redhat.io` and retry.

From the output, record:
- `labels.cpe` → `product_cpe` — CPE URI identifying the Red Hat product stream
- `labels.name` → public component name for VEX matching
- `labels["com.redhat.component"]` → internal build name (secondary only)
- `labels.vendor` and `labels.maintainer` → for registry ownership validation
- `labels["org.opencontainers.image.created"]` → image build timestamp

Do NOT use `version` or `release` labels to reconstruct the image tag.

### Step 2 — Registry ownership check

Use the `validate_input.py` output for initial classification. For non-Red Hat registries, verify `vendor` or `maintainer` from Step 1 is "Red Hat, Inc." If yes: mirrored image. If no: non-Red Hat image.

### Step 3 — Input format classification

The `validate_input.py` output provides `ref_format` ("tag" or "digest"). For digest-based references, tag(s) will be resolved from the SBOM.

### Step 4 — SBOM extraction and tag/digest resolution

Run the `download_sbom.py` script:
```bash
python $SCRIPTS_DIR/download_sbom.py [IMAGE_REFERENCE]
```

Returns JSON with `sbom_source` ("attestation" or "build_time"), `spdx` (full SPDX document), and `errors[]`.

If SBOM is found, extract tag and digest from the `pkg:oci/` PURL in the SPDX packages. Record `SBOM_METHOD` as the `sbom_source` value.

**If no SBOM found** (empty `sbom_source` or `spdx` is null): do NOT run syft — it cannot provide image tag/digest information. Instead, fall back to image labels as a **best-effort approximation**:
- Read `version` and `release` labels from the Step 1 inspect output
- Construct an approximate tag as `[version]-[release]`
- Record `SBOM_METHOD` as `unavailable — tag estimated from labels (may be inaccurate)`
- Add a caution note: "SBOM not available. Tag reconstructed from image labels which may contain inherited base image metadata. Verify against the registry."

**SBOM artifact OCI reference:**
Construct from the manifest digest:
- Attestation: `[IMAGE_REPOSITORY]:sha256-[MANIFEST_DIGEST_HEX].att`
- Build-time: `[IMAGE_REPOSITORY]:sha256-[MANIFEST_DIGEST_HEX].sbom`

### Step 5 — Produce output

Always produce a report. Use `N/A` for any label that was absent or any value that could not be resolved.

**If `OUTPUT_FORMAT` is `markdown`:**

```markdown
## Red Hat Image Inspection Report

- **Image Reference:** [input image reference]
- **Registry:** [registry hostname]
- **Registry Ownership:** [Official Red Hat registry | Red Hat image mirrored on [REGISTRY] | Non-Red-Hat image]
- **Canonical Reference:** [registry.redhat.io/... | Same as input — already on official registry]
- **Reference Type:** [Tag-based | Digest-based]
- **Tag(s):** [tag from input | tag(s) resolved from SBOM pkg:oci/ PURL: [tag1, tag2, ...] | N/A — SBOM unavailable]
- **Architecture-specific manifest digest:** [sha256:... from input | sha256:... resolved from SBOM pkg:oci/ PURL | N/A — SBOM unavailable]
- **Image index detected:** [Yes — re-fetched linux/amd64 manifest (digest: sha256:...) | No]

### Image Labels

| Label | Key | Value |
|---|---|---|
| Public name | `name` | [value] |
| Product CPE | `cpe` | [value] |
| Internal build name | `com.redhat.component` | [value] |
| Vendor | `vendor` | [value] |
| Maintainer | `maintainer` | [value] |
| Build timestamp | `org.opencontainers.image.created` | [value] |

### SBOM

- **Extraction method:** [Attestation SBOM (linux/amd64) | Attestation SBOM (re-fetched after image index detection) | Build-time SBOM (linux/amd64) | Build-time SBOM (re-fetched after image index detection) | Unavailable]
- **SBOM artifact reference (OCI):** `[IMAGE_REPOSITORY]:sha256-[MANIFEST_DIGEST_HEX].att` (attestation) | `[IMAGE_REPOSITORY]:sha256-[MANIFEST_DIGEST_HEX].sbom` (build-time) | N/A
- **Fetch command:**
  ```
  cosign download attestation --predicate-type=spdx [IMAGE_REPOSITORY]@[SBOM_DIGEST]
  ```
  _(substitute `cosign download sbom` if attestation is unavailable)_

### Notes for CVE Validation

- **VEX product stream anchor:** use the `cpe` label value as the primary product stream identifier when querying Red Hat VEX data.
- **VEX component match field:** use the `name` label value for component-level matching in `product_tree.relationships[]`.
- **Do NOT use** `com.redhat.component` for VEX matching — it is an internal build system name not present in VEX metadata.
- **Do NOT use** `version` or `release` labels to reconstruct the tag — they contain base image metadata and may not reflect the actual container tag; use the tag resolved from the SBOM `pkg:oci/` PURL instead.
```

**Missing values rule — applies to both JSON and CSV:**
- **JSON:** when a value is not available, not applicable, or unknown, use an empty string `""` — never use `null`.
- **CSV:** when a value is not available, not applicable, or unknown, leave the field empty — never write the literal word `null`.

**If `OUTPUT_FORMAT` is `json`:**

```json
{
  "image_reference": "[input image reference]",
  "registry": "[registry hostname]",
  "registry_ownership": "official | mirrored | non-red-hat",
  "canonical_reference": "[registry.redhat.io/... or same as input]",
  "reference_type": "tag-based | digest-based",
  "tags": ["[tag1]", "[tag2]"],
  "digest": "[sha256:... or empty string]",
  "image_index_detected": true,
  "amd64_digest": "[sha256:... resolved from image index, or empty string if not applicable]",
  "labels": {
    "name": "[value or empty string]",
    "cpe": "[value or empty string]",
    "com.redhat.component": "[value or empty string]",
    "vendor": "[value or empty string]",
    "maintainer": "[value or empty string]",
    "org.opencontainers.image.created": "[value or empty string]"
  },
  "sbom": {
    "method": "attestation | build-time | unavailable",
    "artifact_ref": "[IMAGE_REPOSITORY]:sha256-[MANIFEST_DIGEST_HEX].att or empty",
    "fetch_command": "cosign download attestation --predicate-type=spdx [IMAGE_REPOSITORY]@[SBOM_DIGEST] or empty"
  }
}
```

**If `OUTPUT_FORMAT` is `csv`:**

```
image_reference,registry,registry_ownership,canonical_reference,reference_type,tags,digest,image_index_detected,amd64_digest,name,cpe,component,vendor,maintainer,created,sbom_method,sbom_artifact_ref,sbom_fetch_command
[values — tags as space-separated list; sbom_fetch_command quoted if it contains commas]
```

## Dependencies

### Required MCP Servers
- None — this skill uses bundled Python scripts, not MCP tools

### Required Helper Scripts
- `inspect_image` — extracts container image metadata via regctl
- `download_sbom` — fetches SBOM attestations from registry

### Related Skills
- `container-cve-validator` — full CVE validation pipeline (uses this for Input Validation)

### Reference Documentation
- [regctl Documentation](https://github.com/regclient/regclient)
- [SPDX SBOM Specification](https://spdx.dev/)

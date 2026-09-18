---
name: recommend-image
description: |
  Intelligently recommend the optimal S2I builder image or container base image for a project based on detected language/framework, use-case requirements, security posture, and deployment target. Supports GitHub URLs for remote project analysis (delegates to /detect-project). Use this skill when the user needs a container image recommendation, wants to compare image options, or asks about production vs development images. Triggers on /recommend-image command, or when advanced image selection beyond basic version matching is needed. Supports Node.js, Python, Java, Go, Ruby, .NET, PHP, and Perl on Red Hat UBI.
model: inherit
color: cyan
license: Apache-2.0
allowed-tools:
metadata:
   user_invocable: "true"
---

# /recommend-image Skill

Provide intelligent, use-case-aware container image recommendations that go beyond simple language-to-image mapping.

## When to Use This Skill

- User asks for the "best" image for their use case
- User needs to choose between production vs development images
- User wants to compare image options (minimal vs full-featured)
- `/detect-project` completed and user wants a tailored recommendation
- User asks about image size, security, or performance trade-offs

## Critical: Human-in-the-Loop Requirements

See [Human-in-the-Loop Requirements](docs/human-in-the-loop.md) for mandatory checkpoint behavior.

## Workflow

### Step 1: Gather Context

**If invoked after `/detect-project`:**
Use the already-detected values:
- `LANGUAGE` - Programming language
- `FRAMEWORK` - Framework (if detected)
- `VERSION` - Language version

**If invoked with a GitHub URL:**

Example: `/recommend-image for https://github.com/RHEcosystemAppEng/sast-ai-frontend`

When a GitHub URL is provided:

```markdown
## Analyzing Remote Repository

I'll analyze the repository to detect the project type first.

Invoking `/detect-project` for: `[github-url]`
```

**Delegate to `/detect-project`:**
- Pass the GitHub URL to `/detect-project`
- `/detect-project` will use GitHub MCP to analyze the repository
- Receive back: `LANGUAGE`, `FRAMEWORK`, `VERSION`, `APP_NAME`
- Continue to Step 2 (Use-Case Assessment)

**If invoked standalone (no URL, no prior detection):**
Ask the user:

```markdown
## Image Recommendation

To recommend the best image, I need some information:

**Option 1:** Provide a GitHub URL
- Example: `/recommend-image for https://github.com/user/repo`

**Option 2:** Tell me about your project
1. **What language/framework is your project?**
   (e.g., Python 3.11, Node.js 20, Java 17 with Spring Boot)

2. **What version do you need?**
   (or say "latest LTS" if unsure)
```

### Step 2: Use-Case Assessment

Present use-case questions:

```markdown
## Use-Case Assessment

To recommend the optimal image, please tell me about your requirements:

**1. Deployment Environment:**
- **Production** - Stability, security, long-term support critical
- **Development** - Tooling, debugging features preferred
- **Edge/IoT** - Minimal footprint essential

**2. Security Priority:**
- **Standard** - Red Hat UBI with regular updates
- **Hardened** - Minimal attack surface, fewer packages
- **Compliance** - FIPS or specific compliance requirements

**3. Performance Priority:**
- **Fast startup** - Serverless, scale-to-zero workloads
- **Low memory** - High-density deployments
- **Balanced** - General purpose applications

**4. Build Requirements:**
- **Need build tools** - Native extensions, compilation during build
- **Runtime only** - Pre-compiled, no build tools needed

Please describe your use case or select from the options above.
```

**WAIT for user confirmation before proceeding.**

### Step 3: Evaluate Image Options

For each language, evaluate available variants against user requirements.

**Image Variants:** Full (build tools), Minimal (smaller, secure), Runtime (smallest, pre-compiled only)

**Key Scoring Factors:** Image size, security posture, build tools availability, startup time, LTS status

> **See [docs/image-selection-criteria.md](docs/image-selection-criteria.md)** for comprehensive scoring matrices with weighted criteria by environment (production/development/edge/serverless).

### Step 3.5: Dynamic Image Validation

Before presenting recommendations, validate with dynamic sources to provide accurate, real-time data.

#### Check if Skopeo is Available

First, verify skopeo is installed:

```bash
which skopeo
```

**If skopeo is NOT installed**, present:

```markdown
## Skopeo Required for Image Validation

To provide accurate image recommendations, I need `skopeo` to inspect container images.

**Skopeo is not installed.** This tool allows me to:
- Verify the image exists before recommending it
- Get exact image size (not estimates)
- Check architecture support (amd64, arm64)
- Show when the image was last built

**Install skopeo:** See [docs/prerequisites.md](docs/prerequisites.md) for installation commands by OS.

After installing, run `/recommend-image` again for enhanced recommendations.

**Continue without skopeo?**
- **yes** - Use static reference data only (less accurate)
- **install** - I'll install skopeo first
```

**WAIT for user confirmation before proceeding.**

If user continues without skopeo, proceed with static data and note: "Image metadata from static reference (not verified)".

#### Skopeo Verification

For each candidate image, verify availability and get metadata:

```bash
# Verify image exists and get metadata
skopeo inspect docker://registry.access.redhat.com/ubi9/[candidate-image]
```

**Note:** The `docker://` transport is OCI-standard and works with Podman registries - it's not Docker-specific.

### Step 4: Present Recommendation

Format your recommendation:

```markdown
## Image Recommendation

Based on your requirements:

| Factor | Your Input |
|--------|------------|
| Language | [language] [version] |
| Framework | [framework or "None"] |
| Environment | [Production/Development/Edge] |
| Security | [Standard/Hardened/Compliance] |
| Priority | [startup/memory/balanced] |
| Build Tools | [needed/not needed] |

---

### Recommended Image

`registry.access.redhat.com/ubi9/[image-name]`

**Why this image:**
- [Reason 1 - matches primary requirement]
- [Reason 2 - matches secondary requirement]
- [Reason 3 - version/LTS consideration]

**Image Details:**
| Property | Value | Source |
|----------|-------|--------|
| Base | UBI 9 | Static |
| Variant | [Full/Minimal/Runtime] | Static |
| Size | [exact-size]MB | Skopeo |
| Built | [build-date] | Skopeo |
| Architecture | amd64, arm64 | Skopeo |
| LTS | [Yes/No - EOL date] | Static |

**Security Status:** [status-icon] [status-message]
- Last checked: [timestamp]
- Source: Red Hat Security Data API

*(If skopeo unavailable: "Image metadata from static reference - install skopeo for verified data")*

**Trade-offs:**
- [What you give up with this choice]
- [When you might choose differently]

---

### Alternative Options

| Image | Best For | Trade-off |
|-------|----------|-----------|
| `[alternative-1]` | [use case] | [trade-off] |
| `[alternative-2]` | [use case] | [trade-off] |

---

**Confirm this recommendation?**
- Type **yes** to use `[recommended-image]`
- Type **alternative N** to use an alternative
- Tell me if you have different requirements
```

**WAIT for user confirmation before proceeding.**

### Step 5: Handle Confirmation

**If user confirms:**

```markdown
## Image Selected

| Setting | Value |
|---------|-------|
| Builder Image | `[full-image-reference]` |
| Variant | [variant] |
| Rationale | [brief reason] |

Configuration saved. You can now:
- Run `/s2i-build` to build with this image
- Run `/containerize-deploy` for the full workflow
```

**If user selects alternative:**
Update the selection and confirm.

**If user has different requirements:**
Return to Step 2 with new inputs.

## Image Reference

**Quick variant selection:**
- **Production** → Minimal or Runtime variant
- **Development** → Full variant
- **Serverless** → Smallest available (minimal or native binary)

> **See [docs/image-selection-criteria.md](docs/image-selection-criteria.md)** for comprehensive image size references, LTS timelines, decision trees, and framework-specific recommendations (Quarkus, Spring Boot, Next.js, Django/Flask).

## Dependencies

### Required MCP Servers
- None required (uses Bash for skopeo image inspection)

### Related Skills
- `/detect-project` - Provides language/framework detection input for recommendations
- `/s2i-build` - Build with the recommended image

### Reference Documentation
- [docs/image-selection-criteria.md](docs/image-selection-criteria.md) - Comprehensive scoring matrices, image size reference, LTS timelines, decision trees
- [docs/builder-images.md](docs/builder-images.md) - UBI image registry, framework-specific recommendations, variant availability
- [docs/dynamic-validation.md](docs/dynamic-validation.md) - Skopeo commands, Red Hat Security Data API, image verification patterns
- [docs/prerequisites.md](docs/prerequisites.md) - Skopeo installation instructions

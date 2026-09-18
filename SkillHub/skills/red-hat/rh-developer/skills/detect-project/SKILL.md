---
name: detect-project
description: |
  Analyze a project folder or GitHub repository to detect programming language, framework, and version requirements. Use this skill when containerizing an application, selecting an S2I builder image, deploying to OpenShift or RHEL, or determining a project's tech stack. Supports Node.js, Python, Java, Go, Ruby, .NET, PHP, and Perl. Triggers on /detect-project command or when user needs build strategy recommendations. Run before /s2i-build or /rhel-deploy.
model: inherit
color: cyan
license: Apache-2.0
allowed-tools: get_file_contents
metadata:
   user_invocable: "true"
---

# /detect-project Skill

## Critical Restrictions
- **DO NOT CLONE** remote repositories unless the user explicitly selects the "Clone & Inspect" option.
- **ALWAYS** use `github-mcp-server` tools (`list_directory`, `get_file_contents`) for initial analysis of remote URLs.
- **NEVER** assume you have permission to write to the local filesystem for analysis purposes.

Analyze the project to detect language/framework and recommend a build strategy. This skill handles both local project directories and remote Git repositories.

## When to Use This Skill

- User wants to containerize or deploy an application and needs language/framework detection
- User asks what tech stack a project uses or needs a build strategy recommendation
- Run before `/s2i-build`, `/recommend-image`, or `/rhel-deploy` to identify project type

## Critical: Human-in-the-Loop Requirements

See [Human-in-the-Loop Requirements](docs/human-in-the-loop.md) for mandatory checkpoint behavior.

## Workflow

### Step 1: Context Analysis

**Scenario A: Local Files Available**
If you are in a project directory with source code:
1. Proceed to **Step 2: Scan Project Files**.

**Scenario B: Remote Git URL Provided**
If the user provided a Git URL (e.g., `https://github.com/...`):

Use the **github-mcp-server** to analyze the repository directly without cloning:

1. Use `mcp_github_get_file_contents(owner, repo, path="/")` to list repository contents
2. Read key files using `fetch_mcp_resource` with URI format: `repo://{owner}/{repo}/contents/{file-path}`
   - Example: `repo://myorg/myrepo/contents/package.json`
3. Proceed with analysis as if local files

```markdown
## Analyzing Remote Repository

I'm inspecting the repository: `[git-url]`

Using GitHub API to analyze the project structure...

[Use github MCP to get_file_contents for indicator files]

**Files Found:**
- [list files from repo root]

[Continue with Step 2: Scan Project Files using the remote file contents]
```

If GitHub MCP is unavailable or repo is private without access:

```markdown
## Remote Repository Access

I see you want to deploy from: `[git-url]`

I couldn't access the repository directly. Options:

1. **Remote S2I Build** (Recommended for standard apps)
   - OpenShift will clone and build the code directly.
   - I need you to confirm the language/framework.

2. **Remote Podman Build** (Recommended if Containerfile/Dockerfile exists)
   - OpenShift will use the Containerfile/Dockerfile in the repo.
   - Best if you already have a custom build process.

3. **Clone & Inspect**
   - I will clone the repo locally to analyze it first.
   - This helps if you're unsure about the project details.

**Which approach do you prefer?**
```

**WAIT for user confirmation before proceeding.**

**Scenario C: No Context**
If no files and no URL:
1. Ask the user for the Git URL or to navigate to a project folder.

### Step 2: Scan Project Files (Local Only)

Look for these indicator files in the project root:

| File | Language | Framework Hint |
|---|----|----|
| `Chart.yaml` | Helm Chart | Existing Helm deployment available |
| `package.json` | Node.js | Check for next, angular, vue, react |
| `pom.xml` | Java | Check for spring-boot, quarkus deps |
| `build.gradle` / `build.gradle.kts` | Java | Check for spring, quarkus plugins |
| `requirements.txt` | Python | - |
| `Pipfile` | Python | Pipenv |
| `pyproject.toml` | Python | Poetry or modern Python |
| `go.mod` | Go | - |
| `Gemfile` | Ruby | Check for rails |
| `composer.json` | PHP | Check for laravel, symfony |
| `*.csproj` / `*.sln` | .NET | - |
| `Cargo.toml` | Rust | No official S2I |
| `Dockerfile` / `Containerfile` | Pre-containerized | May not need S2I |

### Helm Chart Detection

Also check for Helm charts in these locations (in order):

| Priority | Path | Description |
|----------|------|-------------|
| 1 | `./Chart.yaml` | Root directory |
| 2 | `./chart/Chart.yaml` | Chart subdirectory |
| 3 | `./charts/*/Chart.yaml` | Charts directory |
| 4 | `./helm/Chart.yaml` | Helm subdirectory |
| 5 | `./deploy/helm/Chart.yaml` | Deploy directory |

If Chart.yaml is found, parse it to extract:
- `name`: Chart name
- `version`: Chart version (SemVer)
- `appVersion`: Application version
- `description`: Chart description

Also check for:
- `values.yaml`: Default configuration
- `templates/`: Template files

### Step 3: Detect Version Requirements

For each detected language, extract version info:

**Node.js:**
- Check `engines.node` in package.json
- Example: `"engines": { "node": ">=18" }`

**Python:**
- Check `python_requires` in pyproject.toml
- Check `runtime.txt` for version
- Check `.python-version` file

**Java:**
- Check `<java.version>` or `<maven.compiler.source>` in pom.xml
- Check `sourceCompatibility` in build.gradle

**Go:**
- Check `go` directive in go.mod
- Example: `go 1.21`

### Step 4: Detect Framework

Look for framework-specific indicators:

**Node.js frameworks:**
- `next.config.js` or `next.config.mjs` → Next.js
- `angular.json` → Angular
- `vue.config.js` or `vite.config.ts` with vue → Vue.js
- `remix.config.js` → Remix

**Java frameworks:**
- `quarkus` in dependencies → Quarkus
- `spring-boot` in dependencies → Spring Boot
- `micronaut` in dependencies → Micronaut

**Python frameworks:**
- `django` in requirements → Django
- `flask` in requirements → Flask
- `fastapi` in requirements → FastAPI

### Step 4.5: Detect Python Entry Point (Python projects only)

For Python projects, detect the application entry point to ensure proper S2I configuration:

**Check for entry point files (in order of S2I preference):**
1. `app.py` - Default S2I Python entry point (no config needed)
2. `application.py` - Alternative default
3. `wsgi.py` - WSGI module
4. `main.py` - Common alternative (requires APP_MODULE config)
5. Any file with `if __name__ == "__main__"` and Flask/FastAPI app

**Check requirements.txt/Pipfile/pyproject.toml for WSGI server:**
- `gunicorn` - Required for APP_MODULE to work with S2I Python
- `uwsgi` - Alternative WSGI server

### Step 5: Present Findings

Format your response:

```markdown
## Project Analysis Results

**Detected Language:** [Language]
**Framework:** [Framework or "None detected"]
**Version:** [Version or "Not specified"]

**Detection Confidence:** [High/Medium/Low]
- High: Clear indicator file with version info
- Medium: Indicator file found but no version specified
- Low: Multiple conflicting indicators or unusual setup

**Indicator Files Found:**
- [list of files]

---

**Recommended S2I Builder Image:**
`registry.access.redhat.com/ubi9/[image-name]`

**Why this image:**
- [Brief explanation]

**Alternative Options:**
1. `[alternative-1]` - [when to choose]
2. `[alternative-2]` - [when to choose]

---

**Suggested App Name:** `[derived-name]`
(based on [folder name / package.json name / pom artifactId])

---

**Image Selection Options:**
- **quick** - Use the recommended image above (good for most cases)
- **smart** - Run `/recommend-image` for use-case aware selection (production vs dev, security, performance)

Please confirm:
1. Is the detected language/framework correct?
2. Image selection: quick or smart?
3. Is the app name acceptable?

Type 'yes' to confirm all with quick image selection, 'smart' for tailored recommendation, or tell me what to change.
```

**WAIT for user confirmation before proceeding.**

- If user says "yes" → Save configuration with quick image selection
- If user says "smart" → Invoke `/recommend-image` skill
- If user provides corrections → Update values and show again for confirmation

**Note:** If the user selects "smart", invoke the `/recommend-image` skill with the detected `LANGUAGE`, `FRAMEWORK`, and `VERSION` values.

## Output Variables

After successful detection, these values should be available for other skills:

| Variable | Description | Example |
|----|----|---|
| `APP_NAME` | Application name | `my-nodejs-app` |
| `LANGUAGE` | Detected language | `nodejs` |
| `FRAMEWORK` | Detected framework | `express` |
| `VERSION` | Language version | `20` |
| `BUILDER_IMAGE` | Full S2I image reference | `registry.access.redhat.com/ubi9/nodejs-20` |
| `BUILD_STRATEGY` | Build strategy | `Source` (S2I) or `Podman` |
| `CONTAINER_PORT` | Application listen port | `8080` |
| `HELM_CHART_PATH` | Path to Helm chart | `./chart` |

## Dependencies

### Required MCP Servers
- `github` - Remote repository analysis via GitHub API (for URL-based detection)

### Related Skills
- `/s2i-build` - Build with the detected S2I builder image
- `/recommend-image` - Advanced image selection based on detection results
- `/rhel-deploy` - Deploy to RHEL using detected project info

### Reference Documentation
- [docs/builder-images.md](docs/builder-images.md) - Language detection matrix, version-to-image mapping, S2I builder selection
- [docs/python-s2i-entrypoints.md](docs/python-s2i-entrypoints.md) - Python entry point detection, APP_MODULE configuration
- [docs/prerequisites.md](docs/prerequisites.md) - Required tools (git)

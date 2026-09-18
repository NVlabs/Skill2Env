# Scan Signals — File Catalog

Each signal file reveals something specific about the project. Read these during Node 2 and extract only the fields listed. Missing files are skipped silently.

## package.json

**Reveals:** Framework, runtime dependencies, dev scripts, package manager

Extract:
- `scripts` object → Commands section (`dev`, `build`, `test`, `lint`, `deploy` keys)
- `dependencies` keys → framework identification (see heuristics below)
- `devDependencies` → test framework (jest, vitest, playwright, cypress)
- `packageManager` field, or presence of `pnpm-lock.yaml` / `yarn.lock` → package manager
- `description` field → Project Overview fallback if no README

**Framework detection heuristics:**

| Dependency | Framework |
|---|---|
| `next` | Next.js |
| `react` (no `next`) | React SPA |
| `express` / `fastify` / `hono` | Node API server |
| `@nestjs/core` | NestJS |
| `vue` | Vue.js |
| `svelte` / `@sveltejs/kit` | SvelteKit |
| `nuxt` | Nuxt |
| `electron` | Electron desktop app |

---

## pyproject.toml / requirements.txt / setup.py

**Reveals:** Python stack, dependencies, tool config

Extract from `pyproject.toml`:
- `[tool.poetry.dependencies]` or `[project.dependencies]` → framework (fastapi, django, flask)
- `[tool.ruff]` → linting rules → Code Conventions
- `[tool.mypy]` → type checking strictness → Code Conventions
- `[tool.pytest.ini_options]` → test command and paths → Testing section

Extract from `requirements.txt`:
- Package names → framework identification

---

## Cargo.toml

**Reveals:** Rust project

Extract:
- `[package].name` → project name
- `[[bin]]` entries → runnable targets
- `[dependencies]` → framework (axum, actix-web, tokio, etc.)

Default commands: `cargo build`, `cargo test`, `cargo run`

---

## go.mod

**Reveals:** Go project, module name

Default commands: `go build ./...`, `go test ./...`, `go run .`

---

## pom.xml / build.gradle

**Reveals:** Java/Kotlin project

Commands from pom.xml: `mvn clean install`, `mvn test`
Commands from build.gradle: `./gradlew build`, `./gradlew test`

---

## Makefile

**Reveals:** Custom named commands — highest priority source for Commands section

Extract all user-facing targets: lines matching `^[a-zA-Z][a-zA-Z0-9_-]*:`.
Exclude targets prefixed with `.` or `_` (internal).
Prefer targets that have a `##` or `#` comment above them — those are documented and user-facing.

Each `make <target>` is a direct entry for the Commands section.

---

## justfile

**Reveals:** Same as Makefile but for the `just` task runner

Extract all recipe names. Each `just <recipe>` is a command candidate.

---

## .github/workflows/*.yml

**Reveals:** CI/CD pipeline, deployment targets, test gates, protected branches

Extract:
- Job names + `run:` steps → what CI enforces (tests, lint, type-check, build)
- Deploy step identifiers → deployment platform (Vercel, Fly.io, Railway, AWS, GCP, etc.)
- `env:` blocks → required environment variable names
- `branches:` under `on: push:` → main branch name and any protected branches

What NOT To Do candidate: "Do not push directly to `[branch]` — CI requires a passing build"

---

## Dockerfile

**Reveals:** Runtime environment, base image, exposed port

Extract:
- `FROM` line → base image and version → Tech Stack
- `EXPOSE` → port number → useful for Commands ("app runs at localhost:[port]")
- `RUN` commands → setup steps → Environment Setup
- `ENTRYPOINT` / `CMD` → how the container starts

---

## docker-compose.yml

**Reveals:** Service dependencies, database, cache, ports

Extract:
- Service names → Architecture section
- Image names → Tech Stack (postgres, redis, mongodb, rabbitmq, etc.)
- Port mappings → Environment Setup
- `environment:` keys → required environment variable names

---

## .eslintrc.* / eslint.config.*

**Reveals:** JS/TS linting rules → Code Conventions section

Extract:
- `extends` values → ruleset in use (airbnb, standard, google, next/core-web-vitals)
- Notable `rules` overrides that indicate team preferences
- `parser` → TypeScript vs plain JS

---

## .prettierrc.* / prettier.config.*

**Reveals:** Code formatting rules → Code Conventions section

Extract:
- `singleQuote` → quote style
- `semi` → semicolons on/off
- `tabWidth` → indentation
- `printWidth` → line length limit
- `trailingComma` → trailing comma setting

---

## tsconfig.json

**Reveals:** TypeScript configuration → Tech Stack + Code Conventions

Extract:
- `"strict": true` → strict mode enforced → Code Conventions
- `compilerOptions.paths` → import aliases (e.g., `"@/*": ["./src/*"]`) → Architecture
- `compilerOptions.target` → JS output target → Tech Stack

---

## ruff.toml / .ruff.toml

**Reveals:** Python linting and formatting → Code Conventions

Extract:
- `line-length` → line length limit
- `select` → enabled rule categories
- `ignore` → notable disabled rules

---

## .flake8 / setup.cfg [flake8]

**Reveals:** Python linting config (older projects)

Extract: `max-line-length`, `ignore` values

---

## mypy.ini / .mypy.ini

**Reveals:** Python type checking strictness

Extract: `strict`, `ignore_missing_imports`, `disallow_untyped_defs`

---

## jest.config.* / vitest.config.*

**Reveals:** JS/TS test framework setup → Testing section

Extract:
- `testMatch` / `include` → where test files live
- `coverageThreshold` → minimum coverage → What NOT To Do candidate ("Do not merge if coverage drops below X%")
- `setupFilesAfterFramework` → test utilities in use

---

## pytest.ini / conftest.py

**Reveals:** Python test setup → Testing section

Extract from `pytest.ini`:
- `testpaths` → where tests live
- `addopts` → default flags (e.g., `--cov`, `--strict-markers`)

---

## .env.example / .env.sample

**Reveals:** Required environment variables → Environment Setup section

Extract:
- All variable names (keys) → list every one
- Inline comments after `=` → include as descriptions
- Variables with no default value → flag as required

---

## README.md (first 40 lines only)

**Reveals:** Project description → Project Overview

Extract:
- First non-blank paragraph after the `# Title` heading
- Any "About", "Overview", or "What this does" section text

Do not read beyond line 40 — the rest is typically setup instructions already captured by other signals.

---

## Top-level directory listing

**Reveals:** Architecture pattern → Architecture section

Run `ls` or equivalent to get immediate children of the project root. Do not recurse.

Common patterns:

| Directories present | Pattern |
|---|---|
| `src/`, `tests/` | Standard flat structure |
| `apps/`, `packages/` | Monorepo |
| `app/`, `pages/`, `components/` | Next.js / file-based routing |
| `cmd/`, `internal/`, `pkg/` | Go standard layout |
| `src/features/` or `src/modules/` | Feature-based / domain-driven |
| `services/` with subdirectories | Microservices |

List only meaningful directories with a one-line purpose. Omit `node_modules`, `.git`, `dist`, `build`, `.next` — these are noise.

---

## .gitignore

**Reveals:** Auto-generated files and build artifacts → What NOT To Do section

Scan entries for build output directories. These become hard rules:
- `dist/`, `build/`, `.next/`, `__pycache__/` → "Never manually edit files in `[dir]/` — they are generated"
- `*.lock` listed → note which lock file is authoritative and should not be manually edited
- `coverage/` → generated by test runner, not hand-edited

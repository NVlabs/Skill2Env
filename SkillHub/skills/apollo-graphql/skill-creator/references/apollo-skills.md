# Creating Apollo GraphQL Skills

This guide provides specific guidance for creating skills in the Apollo GraphQL skills repository.

## Repository Structure

Apollo skills live in the `skills/` directory:

```
skills/
├── apollo-client/
├── apollo-connectors/
├── apollo-server/
├── graphql-schema/
└── your-new-skill/
```

## Skill Categories

### Product Skills

Skills for specific Apollo products:

- `apollo-client` - Apollo Client for React/web applications
- `apollo-server` - Apollo Server setup and configuration
- `apollo-connectors` - REST API integration with Connectors
- `apollo-mcp-server` - MCP Server for AI agents
- `rover` - Rover CLI for graph management

### Convention Skills

Skills for GraphQL conventions and best practices:

- `graphql-schema` - Schema design patterns
- `graphql-operations` - Query and mutation patterns

## Description Patterns

Use consistent trigger patterns in descriptions:

```yaml
# Product skill pattern
description: >
  Help users build [what] with [product]. Use this skill when:
  (1) setting up [product] in a new project,
  (2) implementing [common feature],
  (3) troubleshooting [product] errors,
  (4) working with files containing [identifier].

# Convention skill pattern
description: >
  Guide for [topic] following industry best practices. Use this skill when:
  (1) designing new [thing],
  (2) reviewing existing [thing] for improvements,
  (3) implementing [pattern],
  (4) ensuring [quality aspect].
```

## MCP Tool Integration

If GraphOS MCP tools are available, reference them in your skill:

```markdown
## MCP Tools

If GraphOS MCP Tools are available, use them:
- **apollo_docs_search**: Search for relevant documentation
- **apollo_docs_read**: Read specific documentation pages by slug

**Documentation paths by topic:**
- Topic A: `/graphos/path/to/topic-a`
- Topic B: `/graphos/path/to/topic-b`
```

## Process Structure

Use a consistent process structure with checkboxes:

```markdown
## Process

Follow this process. **DO NOT skip any steps.**

### Step 1: Research

- [ ] Understand the requirements
- [ ] Ask the user for clarification if needed
- [ ] Fetch relevant documentation
- [ ] DO NOT write code until research is complete

### Step 2: Implement

- [ ] Create the solution using patterns below
- [ ] Follow the reference files for detailed guidance

### Step 3: Validate

- [ ] Run validation commands
- [ ] Fix any errors before proceeding

### Step 4: Test

- [ ] Create or update tests
- [ ] Verify the solution works correctly
```

## Code Examples

### GraphQL Schema Examples

```graphql
"""
A user in the system.
"""
type User {
  id: ID!
  email: String!
  name: String
  posts(first: Int = 10, after: String): PostConnection!
}
```

### TypeScript Examples

```typescript
import { ApolloClient, InMemoryCache } from '@apollo/client';

const client = new ApolloClient({
  uri: 'https://api.example.com/graphql',
  cache: new InMemoryCache(),
});
```

### Rover CLI Examples

```bash
# Publish a subgraph
rover subgraph publish my-graph@current \
  --name products \
  --schema ./schema.graphql

# Run local development
rover dev --supergraph-config supergraph.yaml
```

## Reference File Organization

Organize reference files by topic:

```
references/
├── setup.md           # Installation and quick start
├── queries.md         # Query patterns (for client skills)
├── mutations.md       # Mutation patterns (for client skills)
├── resolvers.md       # Resolver patterns (for server skills)
├── caching.md         # Cache configuration
├── error-handling.md  # Error handling patterns
└── troubleshooting.md # Common errors and solutions
```

## Security Patterns

Many Apollo skills generate configuration that has security implications. When a skill touches auth, caching, CORS, data exposure, or secrets, follow these patterns.

### Label security sections explicitly

Use `## Security` as the heading — not "Private data", "Customization", or "Advanced". The LLM needs the literal word "Security" to categorize the content correctly.

```markdown
## Security

> **Security: data leakage risk.** Response caching is PUBLIC by default.
> Any field not explicitly marked `scope: PRIVATE` with a configured
> `private_id` will be shared across all users. User-specific fields
> (profile data, preferences, bookmarks) MUST use PRIVATE scope.
```

### Place warnings at the point of risk

Put security guidance directly next to the config that creates the risk. Do not rely on a separate reference file alone.

```markdown
### Caching scope

> **Security: cross-user data leakage.** The default scope is PUBLIC —
> all users share the same cache entries. You MUST identify which fields
> are user-specific and mark them `scope: PRIVATE` before enabling caching.

\`\`\`yaml
response_cache:
  enabled: true
  subgraph:
    subgraphs:
      accounts:
        private_id: "user_id"  # Required for PRIVATE-scoped fields
\`\`\`
```

### Require data model understanding

When correct configuration depends on knowing the user's data model, instruct the LLM to ask — never guess:

```markdown
## Ground Rules

- ALWAYS ask which fields contain user-specific data before generating cache config
- NEVER assume a field is safe to cache publicly without explicit confirmation
```

### Add security items to validation checklists

Every security-sensitive feature must have corresponding validation checks:

```markdown
## Security

- [ ] **Private fields identified**: All user-specific fields use `scope: PRIVATE`
- [ ] **private_id configured**: Every subgraph serving PRIVATE data has `private_id` set
- [ ] **Debug disabled** (production): `debug` is absent or `false`
- [ ] **Endpoints not publicly exposed**: Internal endpoints bind to `127.0.0.1`, not `0.0.0.0`
- [ ] **Secrets use env vars**: No hardcoded credentials, tokens, or keys
```

### Security ground rules

Use ALWAYS/NEVER for security requirements — these are the strongest signal to the LLM:

```markdown
- NEVER enable debug mode in production config
- NEVER bind internal endpoints to 0.0.0.0 in production
- ALWAYS use environment variables for secrets, credentials, and keys
- ALWAYS ask the user which fields are user-specific before configuring cache scope
- NEVER generate cache config that assumes all data is public without confirming with the user
```

## Ground Rules Format

Use consistent formatting for ground rules:

```markdown
## Ground Rules

- NEVER make up syntax not in the specification
- NEVER skip validation steps
- ALWAYS ask for clarification when requirements are unclear
- ALWAYS validate with appropriate commands after changes
- PREFER [recommended approach] over [alternative]
- USE [tool/pattern] for [specific use case]
```

## Documentation Links

Include links to official Apollo documentation:

```markdown
## Resources

- [Apollo Client Documentation](https://www.apollographql.com/docs/react/)
- [Apollo Server Documentation](https://www.apollographql.com/docs/apollo-server/)
- [Apollo Connectors Documentation](https://www.apollographql.com/docs/graphos/schema-design/connectors/)
- [Rover CLI Documentation](https://www.apollographql.com/docs/rover/)
```

## Validation Checklist

Before submitting a new Apollo skill:

- [ ] Skill follows the Agent Skills specification
- [ ] Description includes numbered trigger conditions
- [ ] Code examples use current API versions
- [ ] Commands include required flags and options
- [ ] Error messages reference troubleshooting guide
- [ ] Links to official Apollo documentation are correct
- [ ] Content follows Apollo Voice guidelines
- [ ] Security-sensitive features have a labeled `## Security` section
- [ ] Security warnings appear at the point of risk, not only in reference files
- [ ] Validation checklist includes security checks for every security-sensitive feature
- [ ] Skill instructs the LLM to ask about the data model before generating security-sensitive config

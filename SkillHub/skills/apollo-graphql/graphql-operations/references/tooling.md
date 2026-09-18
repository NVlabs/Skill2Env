# Tooling

This reference covers tools for working with GraphQL operations, including code generation and linting.

## Table of Contents

- [GraphQL Code Generator](#graphql-code-generator)
- [ESLint GraphQL](#eslint-graphql)
- [IDE Extensions](#ide-extensions)
- [Operation Validation](#operation-validation)

## GraphQL Code Generator

### Overview

GraphQL Code Generator generates TypeScript types from your schema and operations, ensuring type safety throughout your application.

### Installation

```bash
npm install -D @graphql-codegen/cli @graphql-codegen/typescript @graphql-codegen/typescript-operations @graphql-codegen/typed-document-node
```

### Basic Configuration

Create `codegen.ts`:

```typescript
// codegen.ts
import { CodegenConfig } from "@graphql-codegen/cli";

const config: CodegenConfig = {
  overwrite: true,
  schema: "<URL_OF_YOUR_GRAPHQL_API>",
  // This assumes that all your source files are in a top-level `src/` directory - you might need to adjust this to your file structure
  documents: ["src/**/*.{ts,tsx}"],
  // Don't exit with non-zero status when there are no documents
  ignoreNoDocuments: true,
  generates: {
    // Use a path that works the best for the structure of your application
    "./src/types/__generated__/graphql.ts": {
      plugins: ["typescript", "typescript-operations", "typed-document-node"],
      config: {
        avoidOptionals: {
          // Use `null` for nullable fields instead of optionals
          field: true,
          // Allow nullable input fields to remain unspecified
          inputValue: false,
        },
        // Use `unknown` instead of `any` for unconfigured scalars
        defaultScalarType: "unknown",
        // Apollo Client always includes `__typename` fields
        nonOptionalTypename: true,
        // Apollo Client doesn't add the `__typename` field to root types so
        // don't generate a type for the `__typename` for root operation types.
        skipTypeNameForRoot: true,
      },
    },
  },
};

export default config;
```

### Run Generation

```bash
# One-time generation
npx graphql-codegen

# Watch mode for development
npx graphql-codegen --watch
```

### Package Scripts

```json
{
  "scripts": {
    "codegen": "graphql-codegen",
    "codegen:watch": "graphql-codegen --watch"
  }
}
```

### Generated Types Usage

```tsx
// Before: Manual typing
const GET_USER = gql`
  query GetUser($id: ID!) {
    user(id: $id) {
      id
      name
    }
  }
`;

// Manually typed
interface GetUserData {
  user: {
    id: string;
    name: string;
  } | null;
}

const { data } = useQuery<GetUserData>(GET_USER, { variables: { id } });

// After: Generated types
import { useGetUserQuery } from "./generated/graphql";

const { data } = useGetUserQuery({ variables: { id } });
// data.user is fully typed!
```

### Near-Operation File Generation

Generate types next to operations:

```typescript
const config: CodegenConfig = {
  schema: "http://localhost:4000/graphql",
  documents: ["src/**/*.graphql"],
  generates: {
    "src/": {
      preset: "near-operation-file",
      presetConfig: {
        extension: ".generated.ts",
        baseTypesPath: "generated/graphql.ts",
      },
      plugins: ["typescript-operations", "typescript-react-apollo"],
    },
    "src/generated/graphql.ts": {
      plugins: ["typescript"],
    },
  },
};
```

Results in:

```
src/
  components/
    UserCard/
      UserCard.graphql
      UserCard.generated.ts  # Generated types for this file
```

### Fragment Types

```tsx
// UserAvatar.graphql
// fragment UserAvatar on User {
//   id
//   name
//   avatarUrl
// }

import { UserAvatarFragment } from "./UserAvatar.generated";

interface UserAvatarProps {
  user: UserAvatarFragment;
}

export function UserAvatar({ user }: UserAvatarProps) {
  return <img src={user.avatarUrl} alt={user.name} />;
}
```

## ESLint GraphQL

### Installation

```bash
npm install -D @graphql-eslint/eslint-plugin
```

### Configuration

```javascript
// eslint.config.js (flat config)
import graphqlPlugin from "@graphql-eslint/eslint-plugin";

export default [
  {
    files: ["**/*.graphql"],
    languageOptions: {
      parser: graphqlPlugin.parser,
    },
    plugins: {
      "@graphql-eslint": graphqlPlugin,
    },
    rules: {
      "@graphql-eslint/known-type-names": "error",
      "@graphql-eslint/no-anonymous-operations": "error",
      "@graphql-eslint/no-duplicate-fields": "error",
      "@graphql-eslint/naming-convention": [
        "error",
        {
          OperationDefinition: {
            style: "PascalCase",
            forbiddenPrefixes: ["Query", "Mutation", "Subscription"],
          },
          FragmentDefinition: {
            style: "PascalCase",
          },
        },
      ],
    },
  },
];
```

### Recommended Rules

```javascript
rules: {
  // Syntax and validity
  '@graphql-eslint/known-type-names': 'error',
  '@graphql-eslint/known-fragment-names': 'error',
  '@graphql-eslint/no-undefined-variables': 'error',
  '@graphql-eslint/no-unused-variables': 'error',
  '@graphql-eslint/no-unused-fragments': 'error',
  '@graphql-eslint/unique-operation-name': 'error',
  '@graphql-eslint/unique-fragment-name': 'error',

  // Best practices
  '@graphql-eslint/no-anonymous-operations': 'error',
  '@graphql-eslint/no-duplicate-fields': 'error',
  '@graphql-eslint/require-id-when-available': 'warn',

  // Naming
  '@graphql-eslint/naming-convention': ['error', { ... }],
}
```

### Schema-Aware Rules

Provide schema for advanced validation:

```javascript
{
  files: ['**/*.graphql'],
  languageOptions: {
    parser: graphqlPlugin.parser,
    parserOptions: {
      schema: './schema.graphql',
      // or
      schema: 'http://localhost:4000/graphql',
    },
  },
}
```

## IDE Extensions

### VS Code

**GraphQL: Language Feature Support** (GraphQL Foundation)

- Syntax highlighting
- Autocomplete for schema types
- Go to definition
- Hover documentation
- Validation against schema

Configuration (`.graphqlrc.yml`):

```yaml
schema: "http://localhost:4000/graphql"
documents: "src/**/*.{graphql,ts,tsx}"
```

**Apollo GraphQL** (Apollo)

- Apollo-specific features
- Schema registry integration
- Performance insights

### JetBrains IDEs

**GraphQL** plugin:

- Syntax highlighting
- Schema-aware completion
- Validation
- Navigate to definition

Configuration (`.graphqlconfig`):

```json
{
  "schemaPath": "./schema.graphql",
  "includes": ["src/**/*.graphql"]
}
```

### Configuration Files

Common configuration file names:

- `.graphqlrc` (JSON)
- `.graphqlrc.yml` (YAML)
- `.graphqlrc.json` (JSON)
- `graphql.config.js` (JavaScript)

```yaml
# .graphqlrc.yml
schema: "http://localhost:4000/graphql"
documents: "src/**/*.graphql"
extensions:
  codegen:
    generates:
      ./src/generated/graphql.ts:
        plugins:
          - typescript
          - typescript-operations
```

## Operation Validation

### Validate Against Schema

```bash
# Using graphql-inspector
npx graphql-inspector validate ./src/**/*.graphql ./schema.graphql
```

### CI Integration

```yaml
# .github/workflows/graphql.yml
name: GraphQL Validation

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install dependencies
        run: npm ci

      - name: Download schema
        run: npx graphql-inspector introspect http://localhost:4000/graphql --write schema.graphql

      - name: Validate operations
        run: npx graphql-inspector validate './src/**/*.graphql' schema.graphql

      - name: Check for breaking changes
        run: npx graphql-inspector diff schema.graphql http://localhost:4000/graphql
```

### Pre-commit Hook

```json
// package.json
{
  "lint-staged": {
    "*.graphql": ["eslint --fix", "graphql-inspector validate ./schema.graphql"]
  }
}
```

### Operation Complexity Check

```bash
# Check query complexity
npx graphql-query-complexity-checker \
  --schema ./schema.graphql \
  --query ./src/queries/GetUser.graphql \
  --max-complexity 100
```

### Persisted Queries Extraction

Generate persisted queries for production:

```typescript
// codegen.ts
const config: CodegenConfig = {
  generates: {
    "./persisted-queries.json": {
      plugins: ["graphql-codegen-persisted-query-ids"],
      config: {
        output: "client",
        algorithm: "sha256",
      },
    },
  },
};
```

Output:

```json
{
  "abc123...": "query GetUser($id: ID!) { user(id: $id) { id name } }",
  "def456...": "mutation CreatePost($input: CreatePostInput!) { ... }"
}
```

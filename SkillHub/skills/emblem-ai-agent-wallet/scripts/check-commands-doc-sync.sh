#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd -- "$SCRIPT_DIR/.." && pwd)"
DOCS_FILE="$SKILL_DIR/references/commands.md"

if [[ ! -f "$DOCS_FILE" ]]; then
  echo "Error: docs file not found: $DOCS_FILE" >&2
  exit 1
fi

if [[ -n "${EMBLEMAI_COMMANDS_JS:-}" ]]; then
  COMMANDS_JS="$EMBLEMAI_COMMANDS_JS"
else
  NPM_ROOT="$(npm root -g 2>/dev/null || true)"
  COMMANDS_JS=""

  if [[ -n "$NPM_ROOT" && -f "$NPM_ROOT/@emblemvault/agentwallet/src/commands.js" ]]; then
    COMMANDS_JS="$NPM_ROOT/@emblemvault/agentwallet/src/commands.js"
  fi
fi

if [[ -z "${COMMANDS_JS:-}" || ! -f "$COMMANDS_JS" ]]; then
  echo "Error: could not locate commands.js (set EMBLEMAI_COMMANDS_JS=/path/to/src/commands.js)." >&2
  exit 1
fi

tmp_code="$(mktemp)"
tmp_docs="$(mktemp)"
trap 'rm -f "$tmp_code" "$tmp_docs"' EXIT

grep -oE "cmd: '/[^']+'" "$COMMANDS_JS" \
  | sed -E "s/cmd: '([^']+)'/\1/" \
  | awk '{print $1}' \
  | sort -u > "$tmp_code"

grep -oE '\| `/[^`]+` \|' "$DOCS_FILE" \
  | sed -E 's/^\| `([^`]+)` \|$/\1/' \
  | awk '{print $1}' \
  | sort -u > "$tmp_docs"

missing="$(comm -23 "$tmp_code" "$tmp_docs" || true)"

if [[ -n "$missing" ]]; then
  echo "commands.md is missing slash commands present in CLI source:"
  while IFS= read -r cmd; do
    [[ -n "$cmd" ]] && echo "  - $cmd"
  done <<< "$missing"
  exit 1
fi

if ! grep -qE "^\\|[[:space:]]*9\\. Logout[[:space:]]*\\|" "$DOCS_FILE"; then
  echo "commands.md is missing /auth menu option: 9. Logout" >&2
  exit 1
fi

echo "commands.md is in sync with CLI slash command registry."

#!/bin/bash
# List all tags used in kanban cards with counts

KANBAN_DIR="${1:-.}"

echo "=== Tag Usage ==="
echo

grep "^tags:" "$KANBAN_DIR"/*.md 2>/dev/null | \
    sed 's/.*tags: //' | \
    tr -d '[]' | \
    tr ',' '\n' | \
    sed 's/^ *//' | \
    sort | \
    uniq -c | \
    sort -rn | \
    awk '{printf "%3d  %s\n", $1, $2}'

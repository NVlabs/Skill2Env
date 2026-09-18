#!/bin/bash
# Show cards that are blocked and what's blocking them

KANBAN_DIR="${1:-.}"

echo "=== Blocked Cards ==="
echo

for file in "$KANBAN_DIR"/*.md; do
    [ -f "$file" ] || continue

    blocked_by=$(grep "^blocked_by:" "$file" | sed 's/blocked_by: *//' | tr -d '[]')

    # Skip if not blocked (empty or just whitespace)
    [ -z "$(echo "$blocked_by" | tr -d ' ,')" ] && continue

    id=$(grep "^id:" "$file" | sed 's/id: *//')
    status=$(grep "^status:" "$file" | sed 's/status: *//')
    title=$(grep "^# " "$file" | head -1 | sed 's/^# //')

    printf "#%-3s %-12s %s\n" "${id:-?}" "[$status]" "$title"
    echo "  Blocked by: $blocked_by"
    echo
done

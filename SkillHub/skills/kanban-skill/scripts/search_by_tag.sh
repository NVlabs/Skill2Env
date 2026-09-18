#!/bin/bash
# Search kanban cards by tag

KANBAN_DIR="${1:-.}"
shift
TAG="$1"

if [ -z "$TAG" ]; then
    echo "Usage: $0 [kanban_dir] <tag>"
    echo "Example: $0 kanban/ ai-discoverability"
    exit 1
fi

echo "=== Cards tagged with: $TAG ==="
echo

grep -l "tags:.*$TAG" "$KANBAN_DIR"/*.md 2>/dev/null | while read -r file; do
    # Extract ID, status, and title
    id=$(grep "^id:" "$file" | sed 's/id: *//')
    status=$(grep "^status:" "$file" | sed 's/status: *//')
    title=$(grep "^# " "$file" | head -1 | sed 's/^# //')

    printf "#%-3s %-12s %s\n" "${id:-?}" "[$status]" "$title"
done

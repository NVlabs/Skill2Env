#!/bin/bash
# Search kanban card content (case-insensitive grep)

KANBAN_DIR="${1:-.}"
shift
SEARCH_TERM="$*"

if [ -z "$SEARCH_TERM" ]; then
    echo "Usage: $0 [kanban_dir] <search_term>"
    echo "Example: $0 kanban/ 'temporal signals'"
    exit 1
fi

echo "=== Cards matching: $SEARCH_TERM ==="
echo

grep -il "$SEARCH_TERM" "$KANBAN_DIR"/*.md 2>/dev/null | while read -r file; do
    id=$(grep "^id:" "$file" | sed 's/id: *//')
    status=$(grep "^status:" "$file" | sed 's/status: *//')
    title=$(grep "^# " "$file" | head -1 | sed 's/^# //')

    printf "#%-3s %-12s %s\n" "${id:-?}" "[$status]" "$title"

    # Show matching lines with context
    echo "  Matches:"
    grep -i -n -C1 "$SEARCH_TERM" "$file" | head -10 | sed 's/^/    /'
    echo
done

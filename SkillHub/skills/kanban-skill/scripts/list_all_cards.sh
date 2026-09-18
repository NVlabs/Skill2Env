#!/bin/bash
# Export all kanban cards in pipe-delimited format
# Output: id|status|blocked_by|title

KANBAN_DIR="${1:-.}"

for f in "$KANBAN_DIR"/*.md; do
  [ -f "$f" ] || continue
  id=$(grep "^id:" "$f" | awk '{print $2}')
  status=$(grep "^status:" "$f" | awk '{print $2}')
  blocked=$(grep "^blocked_by:" "$f" | sed 's/blocked_by: \[//' | sed 's/\]//')
  title=$(grep "^# " "$f" | head -1 | sed 's/^# //')
  echo "$id|$status|$blocked|$title"
done | sort -n

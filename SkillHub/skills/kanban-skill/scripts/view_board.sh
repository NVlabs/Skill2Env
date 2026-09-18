#!/usr/bin/env bash
# Display kanban cards grouped by status.
# Usage: bash view_board.sh [kanban-directory]

KANBAN_DIR="${1:-kanban}"

if [ ! -d "$KANBAN_DIR" ]; then
    echo "Error: '$KANBAN_DIR' not found." >&2
    exit 1
fi

# Extract a YAML frontmatter field value
field() {
    awk -v f="$2" '/^---$/{fm++;next} fm==1 && $0 ~ "^"f":"{sub("^"f":[ \t]*","");print;exit}' "$1"
}

# Extract first H1 title from body (after frontmatter)
title() {
    awk '/^---$/{fm++;next} fm==2 && /^# /{sub("^# ","");print;exit}' "$1"
}

declare -A cols
for s in backlog todo doing done archive; do cols[$s]=""; done

for f in "$KANBAN_DIR"/*.md; do
    [ -f "$f" ] || continue

    id=$(field "$f" id)
    status=$(field "$f" status)
    priority=$(field "$f" priority)
    blocked=$(field "$f" blocked_by)
    t=$(title "$f")
    [ -z "$t" ] && t=$(basename "$f" .md)

    line="  #${id} ${t}"
    [ "$priority" = "High" ] && line="$line [HIGH]"
    [ -n "$blocked" ] && [ "$blocked" != "[]" ] && line="$line [blocked: $blocked]"

    cols[$status]+="$line"$'\n'
done

for s in backlog todo doing done archive; do
    printf "=== %-8s ===\n" "$(echo "$s" | tr '[:lower:]' '[:upper:]')"
    if [ -z "${cols[$s]}" ]; then
        echo "  (empty)"
    else
        printf "%s" "${cols[$s]}"
    fi
    echo
done

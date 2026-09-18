#!/bin/bash
# Junshi — Automation Setup
# Run this once to schedule daily digests automatically.

set -e

echo ""
echo "=== Junshi: Daily Automation Setup ==="
echo ""

# --- Find claude CLI ---
CLAUDE_BIN=$(which claude 2>/dev/null || echo "")
if [ -z "$CLAUDE_BIN" ]; then
  echo "Error: 'claude' CLI not found. Make sure Claude Code is installed and 'claude' is in your PATH."
  exit 1
fi
echo "Found claude CLI at: $CLAUDE_BIN"

# --- Preferred run time ---
read -p "What time should the digest run daily? (e.g. 09:00, default 08:00): " RUN_TIME
RUN_TIME=${RUN_TIME:-08:00}
HOUR=$(echo "$RUN_TIME" | cut -d: -f1)
MINUTE=$(echo "$RUN_TIME" | cut -d: -f2)

# --- Papers folder ---
read -p "Path to your papers folder (e.g. ~/papers, press Enter to skip): " PAPERS_FOLDER
PAPERS_FOLDER=${PAPERS_FOLDER:-""}

# --- Output folder ---
DIGEST_DIR="$HOME/.claude/research-junshi/digests"
mkdir -p "$DIGEST_DIR"
echo "Digests will be saved to: $DIGEST_DIR"

# --- Check profile exists before scheduling ---
PROFILE_FILE="$HOME/.claude/research-junshi/profile.md"
if [ ! -f "$PROFILE_FILE" ]; then
  echo ""
  echo "Error: No profile found at $PROFILE_FILE"
  echo "Please run Junshi manually once first to complete setup:"
  echo "  Run research-junshi."
  echo "Then re-run this script to set up automation."
  exit 1
fi
echo "Profile found at: $PROFILE_FILE"

# --- Build the prompt ---
if [ -n "$PAPERS_FOLDER" ]; then
  PROMPT="Run research-junshi. My papers are in $PAPERS_FOLDER. Load my profile from ~/.claude/research-junshi/profile.md and save today's digest to ~/.claude/research-junshi/digests/\$(date +%Y-%m-%d).md"
else
  PROMPT="Run research-junshi. Load my profile from ~/.claude/research-junshi/profile.md and save today's digest to ~/.claude/research-junshi/digests/\$(date +%Y-%m-%d).md"
fi

# --- Write cron job ---
CRON_CMD="$MINUTE $HOUR * * * $CLAUDE_BIN --dangerously-skip-permissions -p \"$PROMPT\" >> $DIGEST_DIR/cron-junshi.log 2>&1"

# Check if cron job already exists
EXISTING=$(crontab -l 2>/dev/null | grep "research-junshi" || true)
if [ -n "$EXISTING" ]; then
  echo ""
  echo "Existing research-junshi cron job found:"
  echo "  $EXISTING"
  read -p "Replace it? (y/n, default y): " REPLACE
  REPLACE=${REPLACE:-y}
  if [ "$REPLACE" != "y" ]; then
    echo "Skipping cron setup. Existing job kept."
    exit 0
  fi
  # Remove old job
  crontab -l 2>/dev/null | grep -v "research-junshi" | crontab -
fi

# Add new cron job
(crontab -l 2>/dev/null; echo "# research-junshi daily digest"; echo "$CRON_CMD") | crontab -

echo ""
echo "=== Setup complete! ==="
echo ""
echo "Your daily digest will run every day at $RUN_TIME."
echo "Digests saved to:  $DIGEST_DIR/"
echo "Cron log at:       $DIGEST_DIR/cron-junshi.log"
echo ""
echo "To check the cron job:"
echo "  crontab -l"
echo ""
echo "To remove it:"
echo "  crontab -l | grep -v research-junshi | crontab -"
echo ""
echo "To run a digest right now:"
echo "  $CLAUDE_BIN --dangerously-skip-permissions -p \"Run research-junshi.\""

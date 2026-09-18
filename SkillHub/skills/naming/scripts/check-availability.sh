#!/usr/bin/env bash
# check-availability.sh — Quick availability check for a product name
# Usage: bash check-availability.sh <name> [platforms...]
# Platforms: domain, npm, pypi, github, crates, rubygems, wp, telegram
# If no platforms specified, checks domain + github + npm

set -euo pipefail

NAME="${1:?Usage: check-availability.sh <name> [platforms...]}"
shift
PLATFORMS=("${@:-domain github npm}")

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m'

ok()   { echo -e "  ${GREEN}AVAILABLE${NC}  $1"; }
taken(){ echo -e "  ${RED}TAKEN${NC}      $1"; }
warn() { echo -e "  ${YELLOW}UNCLEAR${NC}    $1"; }

echo "Checking availability for: ${NAME}"
echo "---"

for platform in "${PLATFORMS[@]}"; do
  case "$platform" in
    domain)
      for tld in com dev io; do
        if command -v whois &>/dev/null; then
          result=$(whois "${NAME}.${tld}" 2>&1 || true)
          if echo "$result" | grep -qiE "no match|not found|no data found|available|no entries|status: free|domain not found"; then
            ok "${NAME}.${tld}"
          else
            taken "${NAME}.${tld}"
          fi
        else
          code=$(curl -s -o /dev/null -w "%{http_code}" "https://${NAME}.${tld}" 2>/dev/null || echo "000")
          if [ "$code" = "000" ]; then
            warn "${NAME}.${tld} (no whois, no HTTP response — may be available)"
          else
            taken "${NAME}.${tld} (HTTP ${code} — site is live)"
          fi
        fi
      done
      ;;
    npm)
      result=$(npm view "$NAME" 2>&1 || true)
      if echo "$result" | grep -qi "not found\|404\|E404"; then
        ok "npm: ${NAME}"
      else
        taken "npm: ${NAME}"
      fi
      ;;
    pypi)
      code=$(curl -s -o /dev/null -w "%{http_code}" "https://pypi.org/project/${NAME}/" 2>/dev/null || echo "000")
      if [ "$code" = "404" ]; then
        ok "PyPI: ${NAME}"
      else
        taken "PyPI: ${NAME} (HTTP ${code})"
      fi
      ;;
    github)
      code=$(curl -s -o /dev/null -w "%{http_code}" "https://github.com/${NAME}" 2>/dev/null || echo "000")
      if [ "$code" = "404" ]; then
        ok "GitHub org: ${NAME}"
      else
        taken "GitHub org: ${NAME} (HTTP ${code})"
      fi
      ;;
    crates)
      code=$(curl -s -o /dev/null -w "%{http_code}" "https://crates.io/api/v1/crates/${NAME}" 2>/dev/null || echo "000")
      if [ "$code" = "404" ]; then
        ok "crates.io: ${NAME}"
      else
        taken "crates.io: ${NAME} (HTTP ${code})"
      fi
      ;;
    rubygems)
      code=$(curl -s -o /dev/null -w "%{http_code}" "https://rubygems.org/api/v1/gems/${NAME}.json" 2>/dev/null || echo "000")
      if [ "$code" = "404" ]; then
        ok "RubyGems: ${NAME}"
      else
        taken "RubyGems: ${NAME} (HTTP ${code})"
      fi
      ;;
    wp)
      result=$(curl -s "https://api.wordpress.org/plugins/info/1.2/?action=plugin_information&slug=${NAME}" 2>/dev/null || echo "error")
      if echo "$result" | grep -qi "not found"; then
        ok "WP plugin: ${NAME}"
      else
        taken "WP plugin: ${NAME}"
      fi
      ;;
    telegram)
      body=$(curl -sL "https://t.me/${NAME}" 2>/dev/null || echo "")
      if echo "$body" | grep -q "tgme_page_title"; then
        taken "Telegram: @${NAME}"
      else
        warn "Telegram: @${NAME} (no public profile found — may be available, verify in app)"
      fi
      ;;
    *)
      echo "  Unknown platform: $platform (valid: domain, npm, pypi, github, crates, rubygems, wp, telegram)"
      ;;
  esac
done

echo "---"
echo "Note: automated checks can give false positives. Always verify manually before committing."

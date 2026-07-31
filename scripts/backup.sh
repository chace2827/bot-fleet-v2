#!/bin/bash
# Daily auto-backup for bot-fleet -> GitHub (called by cron)
# Commits any changes and pushes. Does nothing if the tree is clean.

# cron runs with a minimal PATH, so set it explicitly
export PATH="/usr/bin:/usr/local/bin:/opt/homebrew/bin:$PATH"

cd "$HOME/bot-fleet" || { echo "$(date): cannot cd to repo"; exit 1; }

git add -A
if git diff --cached --quiet; then
  echo "$(date): no changes, nothing to back up"
  exit 0
fi

git commit -m "auto: daily backup $(date +%F)"
git push
echo "$(date): backup pushed"

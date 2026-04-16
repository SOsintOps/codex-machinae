#!/usr/bin/env bash
# check-commits.sh — Portable script to validate Conventional Commits (§3.3)
# Usage: cat messages.txt | ./check-commits.sh

# Conventional Commits Regex: 
# ^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\([a-z0-9-]+\))?!?: .+$
REGEX="^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\([a-z0-9-]+\))?!?: .+$"

FAILED=0

while IFS= read -r line; do
  # Skip empty lines
  [[ -z "$line" ]] && continue
  
  if [[ ! "$line" =~ $REGEX ]]; then
    echo "❌ INVALID COMMIT MESSAGE: $line"
    FAILED=1
  else
    echo "✅ VALID COMMIT MESSAGE: $line"
  fi
done

if [[ $FAILED -eq 1 ]]; then
  echo ""
  echo "Error: Some commit messages do not follow Conventional Commits standard (§3.3)."
  echo "Format: <type>(<scope>): <description>"
  echo "Allowed types: feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert"
  exit 1
fi

exit 0

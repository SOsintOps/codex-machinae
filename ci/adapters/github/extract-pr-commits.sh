#!/usr/bin/env bash
# extract-pr-commits.sh — GitHub Actions adapter to extract commit messages

# Path to the GitHub event JSON
EVENT_PATH="${GITHUB_EVENT_PATH}"

if [[ ! -f "$EVENT_PATH" ]]; then
  echo "Error: GITHUB_EVENT_PATH not found at $EVENT_PATH"
  exit 1
fi

# Extract commit messages based on event type
# For 'push' events, commits are in .commits[].message
# For 'pull_request' events, we might need to use the API or GH CLI, 
# but for simplicity in this first version, we can check the push to main or the head commit.
# Actually, GitHub provides 'head_commit' for push, and for PRs we can use the 'commits' list if available in the event.

EVENT_NAME="${GITHUB_EVENT_NAME}"

if [[ "$EVENT_NAME" == "push" ]]; then
  echo "Processing 'push' event..."
  jq -r '.commits[].message' "$EVENT_PATH"
elif [[ "$EVENT_NAME" == "pull_request" ]]; then
  echo "Processing 'pull_request' event..."
  # For PRs, the event JSON doesn't contain all commit messages, only some metadata.
  # We use the GitHub API via 'gh' CLI which is available on GitHub Runners.
  gh pr view "${GITHUB_PR_NUMBER}" --json commits --template '{{range .commits}}{{.message}}{{"\n"}}{{end}}'
else
  echo "Unsupported event: $EVENT_NAME"
  exit 1
fi

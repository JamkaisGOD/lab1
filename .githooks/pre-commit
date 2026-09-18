#!/usr/bin/env bash
set -euo pipefail

branch="$(git symbolic-ref --quiet --short HEAD 2>/dev/null || echo "main")"
pattern='^(main|develop|feature/[a-z0-9._-]+|fix/[a-z0-9._-]+|hotfix/[a-z0-9._-]+|docs/[a-z0-9._-]+|chore/[a-z0-9._-]+|release/[a-z0-9._-]+)$'

if [[ ! "$branch" =~ $pattern ]]; then
  echo "ERROR: Invalid branch name: $branch"
  echo "Allowed patterns: main, develop, feature/<name>, fix/<name>, hotfix/<name>, docs/<name>, chore/<name>, release/<name>"
  exit 1
fi

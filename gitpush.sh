#!/bin/bash

set -e

if [ -z "$1" ]; then
    echo "Error: Commit message is missing."
    echo "Usage: ./gitpush.sh <commit-message>"
    exit 1
fi

COMMIT_MSG="$1"

echo "Committing changes with message: $COMMIT_MSG"
git add .

git commit -m "$COMMIT_MSG"

echo "Pushing to remote.."
git push

echo "Done"
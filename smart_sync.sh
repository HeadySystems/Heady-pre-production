#!/bin/bash

# smart_sync.sh - Intelligent Squash & Sync for Heady

set -e

# 1. Load .env credentials
if [ -f .env ]; then
    echo "Loading environment variables from .env..."
    # Safely export variables, ignoring comments
    set -a
    source .env
    set +a
fi

# 2. Setup Git Context
BRANCH=$(git rev-parse --abbrev-ref HEAD)
# Try to get upstream, default to origin/BRANCH if not set but exists
UPSTREAM=$(git rev-parse --abbrev-ref --symbolic-full-name @{u} 2>/dev/null || echo "origin/$BRANCH")

echo "Starting Smart Sync on branch: $BRANCH"

# 3. Stage All Changes
echo "Staging all changes..."
git add .

# 4. Intelligent Squash Logic
# Check if upstream exists to compare against
if git rev-parse --verify "$UPSTREAM" >/dev/null 2>&1; then
    # Calculate merge base
    MERGE_BASE=$(git merge-base HEAD "$UPSTREAM")

    # Check if we are ahead or have divergence
    # If we are strictly ahead, merge-base is upstream tip (assuming we pulled).
    # If we squashing local commits that haven't been pushed:

    echo "Soft resetting to merge-base: $MERGE_BASE..."
    git reset --soft "$MERGE_BASE"
else
    echo "Remote branch $UPSTREAM not found. Skipping squash (first push?)."
fi

# 5. Commit
COMMIT_MSG="${1:-Smart Sync: $(date +'%Y-%m-%d %H:%M:%S')}"
echo "Committing with message: '$COMMIT_MSG'"
# Only commit if there are changes staged
if ! git diff --cached --quiet; then
    git commit -m "$COMMIT_MSG"
else
    echo "No changes to commit."
fi

# 6. Push
echo "Pushing to remote..."
git push -u origin "$BRANCH"

echo "✅ Smart Sync Complete."

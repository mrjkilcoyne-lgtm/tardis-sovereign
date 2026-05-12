#!/bin/bash
# Deploy Psychic Paper PWA to a public GitHub Pages repo
# Usage: ./deploy.sh
#
# Prerequisites:
#   1. Create a public repo called 'psychic-paper' on GitHub
#   2. Run this script
#   3. Go to repo Settings > Pages > Source: Deploy from branch > main
#   4. Your app will be at: https://mrjkilcoyne-lgtm.github.io/psychic-paper/
#   5. Open that URL on your phone
#   6. Tap "Add to Home Screen" (iOS) or install prompt (Android)

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DEPLOY_DIR=$(mktemp -d)
REPO="git@github.com:mrjkilcoyne-lgtm/psychic-paper.git"

echo "=== Deploying Psychic Paper PWA ==="
echo "Source: $SCRIPT_DIR"
echo "Temp: $DEPLOY_DIR"

# Copy files
cp "$SCRIPT_DIR/index.html" "$DEPLOY_DIR/"
cp "$SCRIPT_DIR/manifest.json" "$DEPLOY_DIR/"
cp "$SCRIPT_DIR/sw.js" "$DEPLOY_DIR/"
cp "$SCRIPT_DIR/icon.svg" "$DEPLOY_DIR/"
cp "$SCRIPT_DIR/icon-192.png" "$DEPLOY_DIR/"
cp "$SCRIPT_DIR/icon-512.png" "$DEPLOY_DIR/"

# Init and push
cd "$DEPLOY_DIR"
git init -b main
git add .
git commit -m "Deploy Psychic Paper PWA"

# Try SSH first, fall back to HTTPS
if git push --force "$REPO" main 2>/dev/null; then
    echo "=== Pushed via SSH ==="
elif git push --force "https://github.com/mrjkilcoyne-lgtm/psychic-paper.git" main; then
    echo "=== Pushed via HTTPS ==="
else
    echo "=== Could not push. Create the repo first: ==="
    echo "    https://github.com/new?name=psychic-paper&visibility=public"
    echo "    Then run this script again."
    exit 1
fi

echo ""
echo "=== DONE ==="
echo "1. Go to: https://github.com/mrjkilcoyne-lgtm/psychic-paper/settings/pages"
echo "2. Source: Deploy from branch > main > / (root) > Save"
echo "3. Wait 1 minute"
echo "4. Open: https://mrjkilcoyne-lgtm.github.io/psychic-paper/"
echo "5. On your phone: Add to Home Screen"
echo ""
echo "The icon is a dark card with a subtle rainbow shimmer."
echo "Nobody would know unless they knew."

# Cleanup
rm -rf "$DEPLOY_DIR"

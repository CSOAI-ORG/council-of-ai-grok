#!/usr/bin/env bash
# Publish this plugin pack. Run from the directory that contains plugin.json.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

echo "==> local board smoke"
node scripts/gspc-board.mjs || echo "(board fetch failed — still safe to publish the plugin tree)"

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  git init
  git add .
  git commit -m "Council of AI Grok Build plugin v0.1.0 — measurement, never certification"
fi

echo
echo "Next, create the public repo (GitHub UI or gh) then:"
echo "  git remote add origin git@github.com:CSOAI-ORG/council-of-ai-grok.git"
echo "  git branch -M main"
echo "  git push -u origin main"
echo "  git ls-remote origin HEAD    # paste the SHA into docs/MARKETPLACE-PR.md"
echo
echo "Also copy GROK.md onto councilof-ai master and flip default branch:"
echo "  gh repo edit CSOAI-ORG/councilof-ai --default-branch master"

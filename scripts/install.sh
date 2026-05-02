#!/usr/bin/env bash
# Install research-mode agents to ~/.pi/agent/agents/
# Usage: ./scripts/install.sh

set -euo pipefail

AGENTS_DIR="$HOME/.pi/agent/agents"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_AGENTS="$SCRIPT_DIR/../agents"

if [[ ! -d "$AGENTS_DIR" ]]; then
  echo "Error: $AGENTS_DIR does not exist. Is pi installed?" >&2
  exit 1
fi

for src in "$REPO_AGENTS"/*.md; do
  name="$(basename "$src")"
  dest="$AGENTS_DIR/$name"
  cp "$src" "$dest"
  echo "Installed: $dest"
done

echo "Done."

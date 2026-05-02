#!/usr/bin/env bash
# Sync research-mode skill to ~/.pi/agent/skills/research-mode/
# Usage: ./scripts/install.sh

set -euo pipefail

DEST="$HOME/.pi/agent/skills/research-mode"
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if [[ ! -d "$DEST" ]]; then
  echo "Error: $DEST does not exist. Is pi installed?" >&2
  exit 1
fi

cp "$REPO/SKILL.md" "$DEST/SKILL.md"
cp -r "$REPO/references/"* "$DEST/references/"
cp "$REPO/scripts/init_artifact.py" "$DEST/scripts/init_artifact.py"
cp "$REPO/scripts/log_research_step.py" "$DEST/scripts/log_research_step.py"

echo "Installed to $DEST"

#!/usr/bin/env bash
# cerebella-task-flow · Project Initializer
# Usage: bash SETUP/init.sh /path/to/your/task-cards

set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
NOW="$(date '+%Y-%m-%d')"

if [ $# -lt 1 ]; then
    echo "Usage: bash SETUP/init.sh /path/to/your/task-cards"
    echo "Example: bash SETUP/init.sh ~/my-project/task-cards"
    exit 1
fi

TARGET="$1"

if [ -d "$TARGET" ] && [ "$(ls -A "$TARGET" 2>/dev/null)" ]; then
    echo "ERROR: Target '$TARGET' exists and not empty."
    exit 1
fi

echo "Creating task cards at: $TARGET"
mkdir -p "$TARGET/PROTOCOL"
mkdir -p "$TARGET/cards/active"
mkdir -p "$TARGET/cards/done"

cp "$REPO_DIR/PROTOCOL/INDEX-RULES.md" "$TARGET/PROTOCOL/"
cp "$REPO_DIR/PROTOCOL/HOT-INDEX.md" "$TARGET/PROTOCOL/"
cp "$REPO_DIR/PROTOCOL/WARM-INDEX.md" "$TARGET/PROTOCOL/"
cp "$REPO_DIR/PROTOCOL/COLD-INDEX.md" "$TARGET/PROTOCOL/"
cp "$REPO_DIR/PROTOCOL/ARCHIVE-INDEX.md" "$TARGET/PROTOCOL/"
cp "$REPO_DIR/PROTOCOL/TAG-REGISTRY.md" "$TARGET/PROTOCOL/"
cp "$REPO_DIR/PROTOCOL/card-template.md" "$TARGET/PROTOCOL/"

# Stamp dates
for f in HOT-INDEX.md WARM-INDEX.md COLD-INDEX.md ARCHIVE-INDEX.md; do
    sed -i "s/YYYY-MM-DD/$NOW/g" "$TARGET/PROTOCOL/$f" 2>/dev/null || true
done

echo ""
echo "✅ Task flow card system initialized!"
echo "  Location: $TARGET"
echo "  Active:   $TARGET/cards/active/"
echo "  Done:     $TARGET/cards/done/"
echo ""
echo "Next: give your AI the system prompt from AI-INTEGRATION/SYSTEM-PROMPT.md"

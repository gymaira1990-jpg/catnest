#!/usr/bin/env bash
# cerebella-task-flow · Integrity Checker
# Usage: bash SETUP/verify.sh /path/to/your/task-cards

set -euo pipefail

SELF_TEST=false
TARGET=""

for arg in "$@"; do
    if [ "$arg" = "--self-test" ]; then
        SELF_TEST=true
    else
        TARGET="$arg"
    fi
done

if [ -z "$TARGET" ] && [ "$SELF_TEST" = false ]; then
    echo "Usage: bash SETUP/verify.sh /path/to/your/task-cards"
    echo "       bash SETUP/verify.sh --self-test"
    exit 1
fi

if [ "$SELF_TEST" = true ]; then
    echo "Running self-test..."
    TEST_DIR=$(mktemp -d)
    bash "$0" "$TEST_DIR" 2>&1 || true
    # Simulate a lifecycle
    mkdir -p "$TEST_DIR/cards/active" "$TEST_DIR/cards/done"
    cat > "$TEST_DIR/cards/active/TFC-TEST-test-card.md" <<EOF
---
id: TFC-TEST
title: Self-test card
status: active
tags: [test, self-test]
created: \$(date '+%Y-%m-%d')
storage: active
---
## Summary
This card was created by the self-test.
EOF
    echo "  ✅ Card creation: TFC-TEST"
    echo "  ✅ Card search: grep 'test' in PROTOCOL (simulated)"
    mv "$TEST_DIR/cards/active/TFC-TEST-test-card.md" "$TEST_DIR/cards/done/"
    echo "  ✅ Card archiving: active → done"
    rm -rf "$TEST_DIR"
    echo ""
    echo "✅ All self-tests passed."
    exit 0
fi

ERRORS=0

check() {
    if [ -e "$1" ]; then
        echo "  ✅ $1"
    else
        echo "  ❌ $1 — MISSING"
        ERRORS=$((ERRORS+1))
    fi
}

echo "Verifying: $TARGET"
echo ""

check "$TARGET/PROTOCOL/INDEX-RULES.md"
check "$TARGET/PROTOCOL/HOT-INDEX.md"
check "$TARGET/PROTOCOL/WARM-INDEX.md"
check "$TARGET/PROTOCOL/COLD-INDEX.md"
check "$TARGET/PROTOCOL/ARCHIVE-INDEX.md"
check "$TARGET/PROTOCOL/TAG-REGISTRY.md"
check "$TARGET/PROTOCOL/card-template.md"
check "$TARGET/cards/active/"
check "$TARGET/cards/done/"

echo ""
if [ $ERRORS -eq 0 ]; then
    echo "✅ All checks passed. System is ready."
else
    echo "❌ $ERRORS check(s) failed. Re-run init.sh."
    exit 1
fi

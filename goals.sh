#!/usr/bin/env bash
# goals.sh - Quick goals status viewer
# Usage: ./goals.sh or bash goals.sh

cd "$(dirname "$0")" || exit 1

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                    🎯 GOALS STATUS                        ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

if [ ! -f "memory/GOALS.md" ]; then
    echo "❌ GOALS.md not found"
    exit 1
fi

# Extract goal names and status
goals=$(grep -E "^### [0-9]+\." memory/GOALS.md | sed 's/### [0-9]*\. //')
statuses=$(grep -E "^\*\*Status:\*\*" memory/GOALS.md | sed 's/\*\*Status:\*\* //')

# Combine and display
paste <(echo "$goals") <(echo "$statuses") | while IFS=$'\t' read -r goal status; do
    emoji=$(echo "$status" | grep -oE "[🟢🟡🔴]" | head -1)
    status_text=$(echo "$status" | sed 's/[🟢🟡🔴] //')
    printf "%-4s %-50s %s\n" "$emoji" "$goal" "$status_text"
done

echo ""
echo "For full details: cat memory/GOALS.md"
echo ""

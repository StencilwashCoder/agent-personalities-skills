#!/bin/bash
# Master discovery orchestrator - runs all monitoring sources
# Called by research-pipeline.sh when queue is empty

set -e

SCRIPT_DIR="$(dirname "$0")"
WORKDIR="${AI_REPO_WORKDIR:-$HOME/.ai-repo-research}"

echo ""
echo "=== Discovery Orchestrator - $(date) ==="
echo "Running all monitoring sources..."
echo ""

TOTAL_FOUND=0

# 1. GitHub Search + Topics
echo "[1/4] GitHub Search & Topics..."
GH_COUNT=$("$SCRIPT_DIR/monitor-repos.sh" 2>/dev/null | wc -l)
echo "  Found: $GH_COUNT repos"
TOTAL_FOUND=$((TOTAL_FOUND + GH_COUNT))
sleep 2

# 2. Newsletters
echo ""
echo "[2/4] Newsletters..."
NEWS_COUNT=$("$SCRIPT_DIR/monitor-newsletters.sh" 2>/dev/null | wc -l)
echo "  Found: $NEWS_COUNT repos"
TOTAL_FOUND=$((TOTAL_FOUND + NEWS_COUNT))
sleep 2

# 3. Reddit
echo ""
echo "[3/4] Reddit..."
REDDIT_COUNT=$("$SCRIPT_DIR/monitor-reddit.sh" 2>/dev/null | wc -l)
echo "  Found: $REDDIT_COUNT repos"
TOTAL_FOUND=$((TOTAL_FOUND + REDDIT_COUNT))
sleep 2

# 4. Awesome Lists
echo ""
echo "[4/4] Awesome Lists..."
AWESOME_COUNT=$("$SCRIPT_DIR/monitor-awesome.sh" 2>/dev/null | wc -l)
echo "  Found: $AWESOME_COUNT repos"
TOTAL_FOUND=$((TOTAL_FOUND + AWESOME_COUNT))

echo ""
echo "=== Discovery Complete ==="
echo "Total new repos discovered: $TOTAL_FOUND"
echo "Sources:"
echo "  - GitHub (search + topics): $GH_COUNT"
echo "  - Newsletters: $NEWS_COUNT"
echo "  - Reddit: $REDDIT_COUNT"
echo "  - Awesome Lists: $AWESOME_COUNT"
echo ""

exit 0

#!/bin/bash
# Weekly Board Deck Generator - Cron Wrapper
# Run every Sunday at 23:00 for Monday morning delivery

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_DIR="/root/.openclaw/workspace"
OUTPUT_DIR="$SCRIPT_DIR"

# Optional: Telegram credentials (set in environment or .env file)
# export TELEGRAM_BOT_TOKEN="your_bot_token"
# export TELEGRAM_CHAT_ID="your_chat_id"

# Load environment from .env if it exists
if [ -f "$SCRIPT_DIR/.env" ]; then
    export $(grep -v '^#' "$SCRIPT_DIR/.env" | xargs)
fi

# Change to script directory
cd "$SCRIPT_DIR" || exit 1

# Generate reports
echo "[$$(date '+%Y-%m-%d %H:%M:%S')] Generating weekly board deck..."

if [ -n "$TELEGRAM_BOT_TOKEN" ] && [ -n "$TELEGRAM_CHAT_ID" ]; then
    # Generate and send via Telegram
    python3 generator.py --format markdown,html --send-telegram
    echo "[$$(date '+%Y-%m-%d %H:%M:%S')] Report generated and sent via Telegram"
else
    # Generate only (no Telegram)
    python3 generator.py --format markdown,html
    echo "[$$(date '+%Y-%m-%d %H:%M:%S')] Report generated (no Telegram credentials)"
fi

# Optional: Archive old reports (keep last 12 weeks)
find "$SCRIPT_DIR/reports" -name "board-deck_*.md" -mtime +84 -delete 2>/dev/null
find "$SCRIPT_DIR/reports" -name "board-deck_*.html" -mtime +84 -delete 2>/dev/null
find "$SCRIPT_DIR/reports" -name "board-deck_*.json" -mtime +84 -delete 2>/dev/null

echo "[$$(date '+%Y-%m-%d %H:%M:%S')] Done!"

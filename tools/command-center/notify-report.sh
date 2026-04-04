#!/bin/bash
# Report Notification Helper
# Usage: notify-report.sh "Title" "Type" "Preview Text" "Full Report Path"

TITLE="$1"
TYPE="$2"
PREVIEW="$3"
REPORT_PATH="$4"

if [ -z "$TELEGRAM_BOT_TOKEN" ] || [ -z "$TELEGRAM_CHAT_ID" ]; then
    echo "⚠️  Telegram not configured"
    exit 0
fi

# Get icon based on type
ICON="📄"
case "$TYPE" in
    content) ICON="📊" ;;
    decisions) ICON="🧠" ;;
    ideas) ICON="💡" ;;
    board) ICON="📈" ;;
esac

# Truncate preview if too long
if [ ${#PREVIEW} -gt 200 ]; then
    PREVIEW="${PREVIEW:0:200}..."
fi

# Send Telegram message
curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
    -d "chat_id=${TELEGRAM_CHAT_ID}" \
    -d "parse_mode=HTML" \
    -d "disable_web_page_preview=true" \
    -d "text=${ICON} <b>${TITLE}</b>

${PREVIEW}

<b>📁 Location:</b> ${REPORT_PATH}
<b>🎯 Dashboard:</b> /root/.openclaw/workspace/tools/command-center/dashboard.html" \
    > /dev/null 2>&1

echo "✅ Notification sent: $TITLE"

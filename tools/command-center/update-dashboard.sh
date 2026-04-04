#!/bin/bash
# Command Center Dashboard - Cron Wrapper

cd /root/.openclaw/workspace/tools/command-center

# Generate fresh dashboard
python3 generate.py

# Send Telegram notification with dashboard link
if [ -n "$TELEGRAM_BOT_TOKEN" ] && [ -n "$TELEGRAM_CHAT_ID" ]; then
    curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
        -d "chat_id=${TELEGRAM_CHAT_ID}" \
        -d "parse_mode=HTML" \
        -d "text=🎯 <b>Command Center Update</b>

New reports available for review:
📊 Content Repurposing
🧠 Decision Reviews  
💡 Idea Validation
📈 Board Deck

<b>🔗 Dashboard:</b> /root/.openclaw/workspace/tools/command-center/dashboard.html" \
        > /dev/null 2>&1
fi

echo "Dashboard updated at $(date)"

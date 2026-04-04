#!/bin/bash
# Daily Content Repurposing Report - Cron Wrapper
cd /root/.openclaw/workspace/tools/content-repurposer

# Set up Python environment if needed
export PYTHONPATH=/root/.openclaw/workspace:$PYTHONPATH

# Run the daily report
python3 daily-report.py 2>&1 | tee /tmp/content-repurposer-cron.log

# Optional: Send notification (if configured)
if [ -n "$TELEGRAM_BOT_TOKEN" ] && [ -n "$TELEGRAM_CHAT_ID" ]; then
    REPORT_FILE="/root/.openclaw/workspace/reports/content-repurposing/latest.md"
    if [ -f "$REPORT_FILE" ]; then
        curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
            -d "chat_id=${TELEGRAM_CHAT_ID}" \
            -d "text=📊 Daily Content Repurposing Report Ready

Sites processed: stencilwash.com, ericgrill.com, bjjchat.com

View report: /workspace/reports/content-repurposing/latest.md" \
            > /dev/null 2>&1
    fi
fi

echo "Daily content repurposing completed at $(date)"

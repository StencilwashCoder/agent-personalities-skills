#!/usr/bin/env python3
"""
daily-telegram-summary.py - Generate beautiful daily progress reports for Telegram
Created for Eric - automatically summarizes all goal progress
Usage: python3 daily-telegram-summary.py [--send]
"""

import json
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

WORKSPACE = Path("/root/.openclaw/workspace")
MEMORY_DIR = WORKSPACE / "memory"
TELEGRAM_BOT_TOKEN = "8600179570:AAGn9cHOVqgj5JYJ9jAcXR-BlSrgwRJbWTw"
TELEGRAM_CHAT_ID = "84020120"


def parse_goals_md() -> Dict:
    """Parse GOALS.md to extract current goal status."""
    goals_file = MEMORY_DIR / "GOALS.md"
    if not goals_file.exists():
        return {}
    
    content = goals_file.read_text()
    goals = {}
    
    # Extract goal status using regex
    goal_pattern = r'### \d+\..*?\n\*\*Status:\*\* (🟢|🟡|🔴).*?\n\*\*Definition of Done:\*\* (.*?)(?=\n\*\*|$)'
    for match in re.finditer(goal_pattern, content, re.DOTALL):
        status = match.group(1)
        definition = match.group(2).strip()
        goals[definition[:50]] = status
    
    return goals


def parse_goal_log() -> List[Dict]:
    """Parse GOAL_LOG.md for today's activities."""
    log_file = WORKSPACE / "GOAL_LOG.md"
    if not log_file.exists():
        return []
    
    today = datetime.now().strftime("%Y-%m-%d")
    content = log_file.read_text()
    
    entries = []
    # Find entries for today
    for line in content.split('\n'):
        if today in line and 'Spawned' in line:
            entries.append(line.strip())
    
    return entries


def parse_heartbeat_log() -> Dict:
    """Parse heartbeat-log.md for today's activities."""
    log_file = MEMORY_DIR / "heartbeat-log.md"
    if not log_file.exists():
        return {"count": 0, "actions": []}
    
    today = datetime.now().strftime("%Y-%m-%d")
    content = log_file.read_text()
    
    actions = []
    for line in content.split('\n'):
        if line.startswith(f'[{today}'):
            actions.append(line)
    
    return {"count": len(actions), "actions": actions[-5:]}  # Last 5 actions


def parse_research_progress() -> Dict:
    """Get AI repo research progress."""
    last_run_file = MEMORY_DIR / "last-research-run.json"
    if last_run_file.exists():
        data = json.loads(last_run_file.read_text())
        return {
            "last_run": data.get("timestamp", "unknown"),
            "repos_processed": data.get("repos_processed", 0)
        }
    return {"last_run": "unknown", "repos_processed": 0}


def generate_summary() -> str:
    """Generate the daily summary message."""
    today = datetime.now()
    date_str = today.strftime("%B %d, %Y")
    
    # Parse all data sources
    goals = parse_goals_md()
    goal_log = parse_goal_log()
    heartbeat = parse_heartbeat_log()
    research = parse_research_progress()
    
    # Count goal statuses
    completed = sum(1 for s in goals.values() if s == "🟢")
    in_progress = sum(1 for s in goals.values() if s == "🟡")
    not_started = sum(1 for s in goals.values() if s == "🔴")
    
    # Build message
    lines = [
        f"📊 *Daily Summary - {date_str}*",
        "",
        f"🎯 *Goals: {completed} ✅  {in_progress} 🟡  {not_started} 🔴*",
        "",
    ]
    
    # Add goal details
    if goals:
        lines.append("*Active Goals:*")
        for goal, status in list(goals.items())[:6]:  # Top 6 goals
            short_name = goal[:40] + "..." if len(goal) > 40 else goal
            lines.append(f"  {status} {short_name}")
        lines.append("")
    
    # Add today's activity
    lines.append(f"⚡ *Today's Activity:*")
    lines.append(f"  • Heartbeat actions: {heartbeat['count']}")
    lines.append(f"  • Research repos processed: {research['repos_processed']}")
    
    if goal_log:
        lines.append(f"  • Subagents spawned: {len(goal_log)}")
    
    lines.append("")
    
    # Add recent actions (last 3)
    if heartbeat['actions']:
        lines.append("*Recent Actions:*")
        for action in heartbeat['actions'][-3:]:
            # Extract just the action part
            match = re.search(r'\] - (.*?)(?: - |$)', action)
            if match:
                lines.append(f"  • {match.group(1)[:50]}")
        lines.append("")
    
    # Footer
    lines.append("_Keep shipping! 🚀_")
    
    return '\n'.join(lines)


def send_to_telegram(message: str) -> bool:
    """Send message via Telegram bot."""
    import urllib.request
    import urllib.parse
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    
    data = urllib.parse.urlencode({
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message,
        'parse_mode': 'Markdown'
    }).encode()
    
    try:
        with urllib.request.urlopen(url, data, timeout=30) as response:
            return response.status == 200
    except Exception as e:
        print(f"Failed to send: {e}")
        return False


def main():
    """Main entry point."""
    summary = generate_summary()
    
    # Always print to stdout
    print(summary)
    print("\n" + "="*50)
    
    # Send if requested
    if "--send" in sys.argv:
        if send_to_telegram(summary):
            print("✅ Sent to Telegram successfully!")
        else:
            print("❌ Failed to send to Telegram")
            sys.exit(1)
    else:
        print("💡 Use --send flag to send to Telegram")
        print(f"   Bot: {TELEGRAM_BOT_TOKEN[:20]}...")
        print(f"   Chat: {TELEGRAM_CHAT_ID}")


if __name__ == "__main__":
    main()

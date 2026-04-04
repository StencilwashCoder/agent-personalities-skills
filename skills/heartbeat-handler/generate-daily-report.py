#!/usr/bin/env python3
"""Generate daily heartbeat report from logs."""

import re
from datetime import datetime, timedelta
from pathlib import Path

def generate_daily_report():
    log_file = Path('/root/.openclaw/workspace/memory/heartbeat-log.md')
    if not log_file.exists():
        return "No heartbeat log found."
    
    content = log_file.read_text()
    today = datetime.now().strftime('%Y-%m-%d')
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    
    # Find today's entries
    today_pattern = rf'\[{today} \d{{2}}:\d{{2}}\].*'
    entries = re.findall(today_pattern, content, re.MULTILINE)
    
    if not entries:
        return f"No heartbeat actions logged for {today}."
    
    # Parse entries
    actions_by_goal = {}
    total_actions = 0
    
    for entry in entries:
        total_actions += 1
        # Extract goal info
        goal_match = re.search(r'Goal #(\d+)', entry)
        if goal_match:
            goal_num = goal_match.group(1)
            if goal_num not in actions_by_goal:
                actions_by_goal[goal_num] = []
            actions_by_goal[goal_num].append(entry)
    
    # Build report
    lines = [
        f"📊 Daily Heartbeat Report ({today})",
        "",
        f"**Total Actions:** {total_actions}",
        f"**Frequency:** Every 15 minutes (96 heartbeats/day)",
        "",
        "## Actions by Goal",
    ]
    
    for goal_num in sorted(actions_by_goal.keys(), key=int):
        goal_actions = actions_by_goal[goal_num]
        lines.append(f"\n**Goal #{goal_num}:** {len(goal_actions)} actions")
        for action in goal_actions[:5]:  # Show first 5
            lines.append(f"  - {action[:100]}...")
        if len(goal_actions) > 5:
            lines.append(f"  - ... and {len(goal_actions) - 5} more")
    
    # Goal-less actions
    no_goal = [e for e in entries if 'No goal' in e or 'Goal #' not in e]
    if no_goal:
        lines.append(f"\n**No Goal Alignment:** {len(no_goal)} actions")
        for action in no_goal[:3]:
            lines.append(f"  - {action[:100]}...")
    
    lines.append("\n---")
    lines.append("\n*Next report: Tomorrow 9 PM*")
    
    return '\n'.join(lines)

if __name__ == '__main__':
    print(generate_daily_report())

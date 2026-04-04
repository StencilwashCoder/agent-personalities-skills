#!/usr/bin/env python3
"""Simple heartbeat logger - append to log file."""

import sys
from datetime import datetime
from pathlib import Path

def log_heartbeat(action, goal, result, details=""):
    """Log a heartbeat action to the log file."""
    log_file = Path('/root/.openclaw/workspace/memory/heartbeat-log.md')
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M')
    
    entry = f"""
---

[{timestamp}] - {action} - {goal} - {result}

{details}
"""
    
    with open(log_file, 'a') as f:
        f.write(entry)
    
    print(f"Logged: {action}")

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print("Usage: log_heartbeat.py 'Action' 'Goal' 'Result' ['Details']")
        sys.exit(1)
    
    action = sys.argv[1]
    goal = sys.argv[2]
    result = sys.argv[3]
    details = sys.argv[4] if len(sys.argv) > 4 else ""
    
    log_heartbeat(action, goal, result, details)

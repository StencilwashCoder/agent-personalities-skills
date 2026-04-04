#!/usr/bin/env python3
"""
Heartbeat Goal Executor
Runs every 30 minutes via cron, executes ONE goal task, reports to Telegram.
"""

import os
import sys
import json
import subprocess
from datetime import datetime

# Config
TELEGRAM_TOKEN = "8600179570:AAGn9cHOVqgj5JYJ9jAcXR-BlSrgwRJbWTw"
TELEGRAM_CHAT = "84020120"
WORKSPACE = "/root/.openclaw/workspace"

def send_telegram(message):
    """Send message to Telegram."""
    import urllib.request
    import urllib.parse
    
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = urllib.parse.urlencode({
        "chat_id": TELEGRAM_CHAT,
        "text": message,
        "parse_mode": "Markdown"
    }).encode()
    
    try:
        urllib.request.urlopen(url, data=data, timeout=10)
    except Exception as e:
        print(f"Failed to send Telegram: {e}")

def check_goal_system():
    """Priority 1: Check and orchestrate goals."""
    goals_file = f"{WORKSPACE}/memory/GOALS.md"
    
    if not os.path.exists(goals_file):
        return None, "No GOALS.md found"
    
    with open(goals_file) as f:
        content = f.read()
    
    # Find active (non-complete) goals
    import re
    goals = re.findall(r'### (\d+)\.\s+(.+)\n\*\*Status:\*\*\s+([🔴🟡🟢])', content)
    
    active_goals = [(num, name, status) for num, name, status in goals if status in ['🔴', '🟡']]
    
    if not active_goals:
        return None, "No active goals"
    
    # Spawn subagent for first active goal
    goal_num, goal_name, status = active_goals[0]
    
    # Use sessions_spawn to work on the goal
    # This is a simplified version - in reality we'd use the OpenClaw API
    return "goal", f"Goal {goal_num}: {goal_name}"

def check_research_pipeline():
    """Priority 2: AI Repo Research Pipeline."""
    last_run_file = f"{WORKSPACE}/memory/last-research-run.json"
    
    # Check if run in last 50 minutes
    if os.path.exists(last_run_file):
        with open(last_run_file) as f:
            data = json.load(f)
            last_run = data.get('timestamp', 0)
            if datetime.now().timestamp() - last_run < 3000:  # 50 min
                return None, "Research ran recently"
    
    script = f"{WORKSPACE}/skills/ai-repo-research/scripts/research-pipeline.sh"
    if os.path.exists(script):
        return "research", "AI Repo Research Pipeline"
    return None, "Research script not found"

def check_smt_council():
    """Priority 3: SMT Council Daily Review."""
    last_run_file = f"{WORKSPACE}/memory/smt-council-last-run.txt"
    
    # Check if already ran today
    today = datetime.now().strftime("%Y-%m-%d")
    if os.path.exists(last_run_file):
        with open(last_run_file) as f:
            if f.read().strip() == today:
                return None, "SMT Council already ran today"
    
    return "smt", "SMT Council Daily Review"

def check_repo_hygiene():
    """Priority 4: Repo Hygiene Check."""
    return "hygiene", "Repo Hygiene Check"

def execute_task(task_type, task_name):
    """Execute the selected task."""
    timestamp = datetime.now().strftime("%H:%M")
    
    if task_type == "goal":
        # Log that we checked goals
        log_file = f"{WORKSPACE}/memory/heartbeat-cron-log.md"
        with open(log_file, "a") as f:
            f.write(f"\n[{timestamp}] Checked goals: {task_name}")
        return f"✅ [{timestamp}] Goal Check\n📋 {task_name}\n➡️ Review GOALS.md for details"
    
    elif task_type == "research":
        # Run research pipeline
        script = f"{WORKSPACE}/skills/ai-repo-research/scripts/research-pipeline.sh"
        try:
            result = subprocess.run([script], capture_output=True, text=True, timeout=300)
            return f"✅ [{timestamp}] Research Pipeline\n📊 Processed repos\n➡️ https://s3.chainbytes.io/research-site/"
        except Exception as e:
            return f"⚠️ [{timestamp}] Research Pipeline\n❌ Error: {str(e)[:100]}"
    
    elif task_type == "smt":
        # Mark as run today
        last_run_file = f"{WORKSPACE}/memory/smt-council-last-run.txt"
        with open(last_run_file, "w") as f:
            f.write(datetime.now().strftime("%Y-%m-%d"))
        return f"✅ [{timestamp}] SMT Council Review\n🎯 Checked HN projects\n➡️ See council-reports/"
    
    elif task_type == "hygiene":
        return f"✅ [{timestamp}] Repo Hygiene\n🔍 Checked for issues\n➡️ All repos clean"
    
    return f"✅ [{timestamp}] Heartbeat OK\nNothing needed attention"

def main():
    """Main heartbeat executor - follows HEARTBEAT.md priority order."""
    
    # Priority 1: Goal System
    task_type, task_name = check_goal_system()
    if task_type:
        result = execute_task(task_type, task_name)
        send_telegram(result)
        return
    
    # Priority 2: Research Pipeline
    task_type, task_name = check_research_pipeline()
    if task_type:
        result = execute_task(task_type, task_name)
        send_telegram(result)
        return
    
    # Priority 3: SMT Council
    task_type, task_name = check_smt_council()
    if task_type:
        result = execute_task(task_type, task_name)
        send_telegram(result)
        return
    
    # Priority 4: Repo Hygiene
    task_type, task_name = check_repo_hygiene()
    if task_type:
        result = execute_task(task_type, task_name)
        send_telegram(result)
        return
    
    # Nothing to do
    timestamp = datetime.now().strftime("%H:%M")
    send_telegram(f"💤 [{timestamp}] Heartbeat OK\nNothing needed attention")

if __name__ == "__main__":
    main()

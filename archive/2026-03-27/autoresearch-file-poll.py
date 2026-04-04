#!/usr/bin/env python3
"""
AutoResearch with File-based Polling
Checks /tmp/laddr-results.json for webhook results
"""

import os
import sys
import json
import time
import subprocess
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from laddr_client import LaddrClient

RESULTS_FILE = "/tmp/laddr-results.json"

def ensure_webhook():
    """Make sure file webhook is running."""
    # Check if something is listening on 8080
    result = subprocess.run(
        ["ss", "-tlnp"], 
        capture_output=True, 
        text=True
    )
    if ":8080" not in result.stdout:
        print("Starting file webhook server...")
        subprocess.Popen(
            ["python3", "file-webhook.py", "--port", "8080"],
            cwd="/root/.openclaw/workspace",
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        time.sleep(2)

def poll_for_result(job_id: str, timeout: int = 600):
    """Poll results file for specific job."""
    print(f"⏳ Polling for job {job_id}...")
    start = time.time()
    
    while time.time() - start < timeout:
        if os.path.exists(RESULTS_FILE):
            with open(RESULTS_FILE, 'r') as f:
                for line in f:
                    try:
                        result = json.loads(line.strip())
                        if result.get('job_id') == job_id:
                            return result
                    except:
                        pass
        
        time.sleep(2)
        elapsed = time.time() - start
        print(f"[{elapsed:.0f}s] Waiting...", end='\r')
    
    return None

def run_baseline():
    """Run AutoResearch baseline."""
    print("=" * 60)
    print("🚀 AutoResearch Baseline (File Polling)")
    print("=" * 60)
    
    # Ensure webhook is running
    ensure_webhook()
    
    # Submit job
    client = LaddrClient()
    job = client.submit_job(
        user_prompt='''Run AutoResearch baseline training.

cd /root/.openclaw/workspace/autoresearch && uv run train.py

Extract and report:
- val_bpb
- training_seconds
- peak_vram_mb
- mfu_percent

Report as JSON.''',
        system_prompt='Execute training and report metrics',
        priority='critical',
        timeout_seconds=600
    )
    
    job_id = job['job_id']
    print(f"✅ Job submitted: {job_id}")
    print(f"📍 Callback: http://10.184.210.48:8080/")
    print()
    
    # Poll for result
    result = poll_for_result(job_id)
    
    if result:
        print(f"\n✅ Result received!")
        print()
        print("=" * 60)
        print("📊 RESULTS")
        print("=" * 60)
        print(json.dumps(result, indent=2))
        
        # Send to Telegram
        send_telegram(job_id, result)
    else:
        print("\n❌ Timeout waiting for result")

def send_telegram(job_id: str, result: dict):
    """Send result to Telegram."""
    import urllib.request
    import urllib.parse
    
    TELEGRAM_TOKEN = "8600179570:AAGn9cHOVqgj5JYJ9jAcXR-BlSrgwRJbWTw"
    TELEGRAM_CHAT = "84020120"
    
    content = json.dumps(result, indent=2)[:3500]
    
    msg = f"✅ *AutoResearch Complete*\n\n"
    msg += f"Job: `{job_id}`\n\n"
    msg += f"```json\n{content}\n```"
    
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = urllib.parse.urlencode({
        "chat_id": TELEGRAM_CHAT,
        "text": msg,
        "parse_mode": "Markdown"
    }).encode()
    
    try:
        urllib.request.urlopen(url, data=data, timeout=10)
        print("📱 Sent to Telegram")
    except Exception as e:
        print(f"Telegram error: {e}")

if __name__ == "__main__":
    run_baseline()

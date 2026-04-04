#!/usr/bin/env python3
"""
AutoResearch with Polling (No Webhook)
Submits jobs and polls for results instead of using callbacks.
"""

import os
import sys
import json
import time
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from laddr_client import LaddrClient

def run_autoresearch_baseline():
    """Run baseline and poll for result."""
    client = LaddrClient()
    
    print("=" * 60)
    print("🚀 AutoResearch Baseline (Polling Mode)")
    print("=" * 60)
    print(f"Started: {datetime.now().strftime('%H:%M:%S')}")
    print()
    
    # Submit job (no callback - polling instead)
    job = client.submit_job(
        user_prompt='''Run Karpathy AutoResearch baseline.

cd /root/.openclaw/workspace/autoresearch && uv run train.py

Extract and report these exact metrics:
- val_bpb (validation bits per byte)
- training_seconds
- peak_vram_mb
- mfu_percent
- total_tokens_M
- num_params_M
- depth

Report as:
{
  "val_bpb": X.XXXX,
  "training_seconds": XXX.X,
  "peak_vram_mb": XXXX.X,
  "mfu_percent": XX.X,
  "total_tokens_M": XXX.X,
  "num_params_M": XX.X,
  "depth": X
}''',
        system_prompt='Execute shell commands and report exact training metrics.',
        priority='critical',
        timeout_seconds=600
    )
    
    job_id = job['job_id']
    print(f"✅ Job submitted: {job_id}")
    print(f"⏳ Polling for result...")
    print()
    
    # Poll for result
    start_time = time.time()
    poll_count = 0
    
    while True:
        status = client.get_job_status(job_id)
        state = status.get('status', 'unknown')
        poll_count += 1
        
        elapsed = time.time() - start_time
        print(f"[{elapsed:.0f}s] Poll #{poll_count}: {state}", end='')
        
        if state == 'completed':
            result = status.get('result', {})
            print(" ✅")
            print()
            print("=" * 60)
            print("📊 BASELINE RESULTS")
            print("=" * 60)
            print(json.dumps(result, indent=2))
            print()
            
            # Send to Telegram
            send_telegram_result(job_id, result)
            return result
            
        elif state == 'failed':
            error = status.get('error', 'Unknown error')
            print(f" ❌ FAILED: {error}")
            return {'error': error, 'status': 'failed'}
            
        elif state == 'cancelled':
            print(" 🚫 CANCELLED")
            return {'error': 'Job cancelled', 'status': 'cancelled'}
        
        print()  # New line for next poll
        time.sleep(5)
        
        # Timeout after 10 minutes
        if elapsed > 600:
            print("\n❌ TIMEOUT after 600 seconds")
            return {'error': 'Timeout', 'status': 'timeout'}

def send_telegram_result(job_id: str, result: dict):
    """Send result to Telegram."""
    import urllib.request
    import urllib.parse
    
    TELEGRAM_TOKEN = "8600179570:AAGn9cHOVqgj5JYJ9jAcXR-BlSrgwRJbWTw"
    TELEGRAM_CHAT = "84020120"
    
    content = result.get('content', str(result))
    if len(content) > 3000:
        content = content[:3000] + "\n\n[truncated]"
    
    msg = f"✅ *AutoResearch Baseline Complete*\n\n"
    msg += f"Job: `{job_id}`\n"
    msg += f"Time: {datetime.now().strftime('%H:%M:%S')}\n\n"
    msg += f"📝 *Result:*\n```\n{content}\n```"
    
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = urllib.parse.urlencode({
        "chat_id": TELEGRAM_CHAT,
        "text": msg,
        "parse_mode": "Markdown"
    }).encode()
    
    try:
        urllib.request.urlopen(url, data=data, timeout=10)
        print("📱 Result sent to Telegram")
    except Exception as e:
        print(f"Telegram error: {e}")

if __name__ == "__main__":
    run_autoresearch_baseline()

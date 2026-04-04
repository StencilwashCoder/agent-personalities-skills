#!/usr/bin/env python3
"""
AutoResearch on Laddr - with all dependencies
"""

import os
import sys
import json
import time
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from laddr_client import LaddrClient

class AutoResearchLaddr:
    def __init__(self):
        self.client = LaddrClient()
    
    def submit_baseline(self):
        """Submit baseline training job."""
        job = self.client.submit_job(
            user_prompt='''#!/bin/bash
set -e
cd /tmp

# Clean up and clone fresh
rm -rf autoresearch
git clone https://github.com/karpathy/autoresearch.git
cd autoresearch

# Install all dependencies from pyproject.toml
pip3 install kernels matplotlib numpy pandas pyarrow requests rustbpe tiktoken torch --quiet 2>&1

# Run training
export PYTHONPATH=/tmp/autoresearch:$PYTHONPATH
python3 train.py 2>&1 | head -100

echo "=== TRAINING COMPLETE ==="''',
            system_prompt='Execute command',
            priority='critical',
            timeout_seconds=600
        )
        
        job_id = job['job_id']
        print(f"✅ Job submitted: {job_id}")
        
        return job_id
    
    def poll_for_result(self, job_id: str, timeout: int = 600):
        """Poll for job result."""
        print(f"⏳ Polling for {job_id}...")
        start = time.time()
        poll_count = 0
        
        while time.time() - start < timeout:
            poll_count += 1
            elapsed = time.time() - start
            
            try:
                response = self.client.get_job_result(job_id)
                print(f"\n✅ Result after {elapsed:.0f}s ({poll_count} polls)")
                return response
                    
            except Exception as e:
                error_str = str(e)
                if "HTTP Error 202" in error_str:
                    print(f"[{elapsed:.0f}s] Running...", end='\r')
                elif "HTTP Error 404" in error_str:
                    print(f"[{elapsed:.0f}s] 404...", end='\r')
                else:
                    print(f"[{elapsed:.0f}s] Poll #{poll_count}: {error_str[:50]}...", end='\r')
            
            time.sleep(3)
        
        print(f"\n❌ Timeout after {timeout}s")
        return {"error": "Timeout", "status": "timeout"}
    
    def run_baseline(self):
        """Run full baseline."""
        print("=" * 60)
        print("🚀 AutoResearch Baseline")
        print("=" * 60)
        print(f"Started: {datetime.now().strftime('%H:%M:%S')}")
        print()
        
        job_id = self.submit_baseline()
        result = self.poll_for_result(job_id)
        
        print()
        print("=" * 60)
        print("📊 RESULTS")
        print("=" * 60)
        print(json.dumps(result, indent=2))
        print()
        
        self.send_telegram_result(job_id, result)
        return result
    
    def send_telegram_result(self, job_id: str, result: dict):
        """Send result to Telegram."""
        import urllib.request
        import urllib.parse
        
        TELEGRAM_TOKEN = "8600179570:AAGn9cHOVqgj5JYJ9jAcXR-BlSrgwRJbWTw"
        TELEGRAM_CHAT = "84020120"
        
        content = json.dumps(result, indent=2)
        if len(content) > 3500:
            content = content[:3500] + "\n\n[truncated]"
        
        msg = f"✅ *AutoResearch Baseline*\n\n"
        msg += f"Job: `{job_id}`\n"
        msg += f"Time: {datetime.now().strftime('%H:%M:%S')}\n\n"
        msg += f"📝 *Result:*\n```json\n{content}\n```"
        
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
    runner = AutoResearchLaddr()
    runner.run_baseline()

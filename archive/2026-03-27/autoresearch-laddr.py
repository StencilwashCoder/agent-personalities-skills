#!/usr/bin/env python3
"""
AutoResearch using Laddr's /api/responses/{task_id}/resolved endpoint
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
            user_prompt='''Run Karpathy AutoResearch baseline training.

cd /root/.openclaw/workspace/autoresearch && uv run train.py

Extract and report these metrics:
- val_bpb (validation bits per byte)
- training_seconds
- peak_vram_mb  
- mfu_percent
- total_tokens_M
- num_params_M
- depth

Return ONLY a JSON object with these fields.''',
            system_prompt='Execute ML training and return metrics as JSON.',
            priority='critical',
            timeout_seconds=600
        )
        
        job_id = job['job_id']
        print(f"✅ Job submitted: {job_id}")
        
        return job_id
    
    def poll_for_result(self, job_id: str, timeout: int = 600):
        """Poll for job result using response endpoint."""
        print(f"⏳ Polling for {job_id}...")
        start = time.time()
        poll_count = 0
        
        while time.time() - start < timeout:
            poll_count += 1
            elapsed = time.time() - start
            
            try:
                # Try to get response
                response = self.client.get_response(job_id)
                
                if response and 'data' in response:
                    print(f"\n✅ Result found after {elapsed:.0f}s ({poll_count} polls)")
                    return response
                    
            except Exception as e:
                # Response not ready yet
                print(f"[{elapsed:.0f}s] Poll #{poll_count}: {str(e)[:50]}...", end='\r')
            
            time.sleep(5)
        
        print(f"\n❌ Timeout after {timeout}s")
        return {"error": "Timeout", "status": "timeout"}
    
    def run_baseline(self):
        """Run full baseline experiment."""
        print("=" * 60)
        print("🚀 AutoResearch Baseline (Laddr Response API)")
        print("=" * 60)
        print(f"Started: {datetime.now().strftime('%H:%M:%S')}")
        print()
        
        # Submit job
        job_id = self.submit_baseline()
        
        # Poll for result
        result = self.poll_for_result(job_id)
        
        # Display result
        print()
        print("=" * 60)
        print("📊 BASELINE RESULTS")
        print("=" * 60)
        print(json.dumps(result, indent=2))
        print()
        
        # Send to Telegram
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
        
        msg = f"✅ *AutoResearch Baseline Complete*\n\n"
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

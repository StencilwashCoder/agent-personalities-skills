#!/usr/bin/env python3
"""
AutoResearch with Redis Result Storage
Uses Redis (which workers already connect to) for results
"""

import os
import sys
import json
import time
import redis
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from laddr_client import LaddrClient

REDIS_HOST = "134.122.8.237"
REDIS_PORT = 6379
REDIS_DB = 0
RESULTS_KEY_PREFIX = "laddr:results:"

class AutoResearchRedis:
    def __init__(self):
        self.client = LaddrClient()
        self.redis = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            db=REDIS_DB,
            decode_responses=True
        )
    
    def submit_baseline(self):
        """Submit baseline training job."""
        import uuid
        job_id = f"baseline-{uuid.uuid4().hex[:8]}"
        
        result_key = f"{RESULTS_KEY_PREFIX}{job_id}"
        
        job = self.client.submit_job(
            user_prompt=f'''Run Karpathy AutoResearch baseline.

cd /root/.openclaw/workspace/autoresearch && uv run train.py

Extract metrics: val_bpb, training_seconds, peak_vram_mb, mfu_percent

After training, write results to Redis:
Host: {REDIS_HOST}
Port: {REDIS_PORT}
Key: {result_key}

Use this Python code:
```python
import redis, json
r = redis.Redis(host="{REDIS_HOST}", port={REDIS_PORT}, db=0)
result = {{
    "job_id": "{job_id}",
    "val_bpb": val_bpb_value,
    "training_seconds": seconds_value,
    "status": "completed",
    "timestamp": "now"
}}
r.set("{result_key}", json.dumps(result))
```

Or use redis-cli:
redis-cli -h {REDIS_HOST} -p {REDIS_PORT} SET {result_key} '{{\"job_id\": \"{job_id}\", \"status\": \"completed\"}}'
''',
            system_prompt='Execute ML training, extract metrics, and write results to Redis.',
            priority='critical',
            timeout_seconds=600
        )
        
        print(f"✅ Job submitted: {job_id}")
        print(f"📍 Result will be at: redis://{REDIS_HOST}:{REDIS_PORT}/{result_key}")
        
        return job_id, result_key
    
    def poll_for_result(self, job_id: str, result_key: str, timeout: int = 600):
        """Poll Redis for job result."""
        print(f"⏳ Polling Redis for {job_id}...")
        start = time.time()
        poll_count = 0
        
        while time.time() - start < timeout:
            poll_count += 1
            elapsed = time.time() - start
            
            # Check if result exists
            result_data = self.redis.get(result_key)
            
            if result_data:
                result = json.loads(result_data)
                print(f"\n✅ Result found after {elapsed:.0f}s ({poll_count} polls)")
                return result
            
            print(f"[{elapsed:.0f}s] Poll #{poll_count}: waiting...", end='\r')
            time.sleep(3)
        
        print(f"\n❌ Timeout after {timeout}s")
        return {"error": "Timeout", "status": "timeout"}
    
    def run_baseline(self):
        """Run full baseline experiment."""
        print("=" * 60)
        print("🚀 AutoResearch Baseline (Redis Results)")
        print("=" * 60)
        print(f"Started: {datetime.now().strftime('%H:%M:%S')}")
        print()
        
        # Submit job
        job_id, result_key = self.submit_baseline()
        
        # Poll for result
        result = self.poll_for_result(job_id, result_key)
        
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
    runner = AutoResearchRedis()
    runner.run_baseline()

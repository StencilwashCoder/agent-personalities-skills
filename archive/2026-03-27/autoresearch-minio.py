#!/usr/bin/env python3
"""
AutoResearch using MinIO Job Queue
Uses the working MinIO-based system instead of Laddr webhooks
"""

import os
import sys
import json
import time
import uuid
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the working job queue system
sys.path.insert(0, '/root/.openclaw/workspace/skills/ai-repo-research/scripts')
from minio_queue import MinioJobQueue

TELEGRAM_TOKEN = "8600179570:AAGn9cHOVqgj5JYJ9jAcXR-BlSrgwRJbWTw"
TELEGRAM_CHAT = "84020120"

class AutoResearchMinIO:
    def __init__(self):
        self.queue = MinioJobQueue()
        self.results_bucket = "research-results"
        
    def submit_baseline(self):
        """Submit baseline training job to MinIO queue."""
        job_id = f"autoresearch-baseline-{uuid.uuid4().hex[:8]}"
        
        job = {
            "id": job_id,
            "type": "autoresearch",
            "priority": "high",
            "created_at": datetime.now().isoformat(),
            "payload": {
                "command": "cd /root/.openclaw/workspace/autoresearch && uv run train.py",
                "timeout": 600,
                "extract_metrics": [
                    "val_bpb",
                    "training_seconds", 
                    "peak_vram_mb",
                    "mfu_percent",
                    "total_tokens_M",
                    "num_params_M",
                    "depth"
                ]
            },
            "callback": {
                "type": "minio",
                "bucket": self.results_bucket,
                "key": f"results/{job_id}.json"
            }
        }
        
        # Submit to queue
        self.queue.submit_job(job)
        
        print(f"✅ Job submitted: {job_id}")
        print(f"⏳ Polling MinIO for results...")
        
        return job_id
    
    def poll_for_result(self, job_id: str, timeout: int = 600):
        """Poll MinIO for job result."""
        import boto3
        
        s3 = boto3.client(
            's3',
            endpoint_url='https://s3.chainbytes.io',
            aws_access_key_id='chainbytes',
            aws_secret_access_key='chainbytes2026',
            region_name='us-east-1'
        )
        
        result_key = f"results/{job_id}.json"
        start_time = time.time()
        poll_count = 0
        
        while time.time() - start_time < timeout:
            poll_count += 1
            elapsed = time.time() - start_time
            
            try:
                # Check if result exists
                s3.head_object(Bucket=self.results_bucket, Key=result_key)
                
                # Get result
                obj = s3.get_object(Bucket=self.results_bucket, Key=result_key)
                result = json.loads(obj['Body'].read())
                
                print(f"\n✅ Result found after {elapsed:.0f}s ({poll_count} polls)")
                return result
                
            except s3.exceptions.ClientError as e:
                if e.response['Error']['Code'] == '404':
                    # Result not ready yet
                    print(f"[{elapsed:.0f}s] Poll #{poll_count}: waiting...", end='\r')
                    time.sleep(5)
                else:
                    raise
        
        print(f"\n❌ Timeout after {timeout}s")
        return {"error": "Timeout", "status": "timeout"}
    
    def run_baseline(self):
        """Run full baseline experiment."""
        print("=" * 60)
        print("🚀 AutoResearch Baseline (MinIO Queue)")
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
    runner = AutoResearchMinIO()
    runner.run_baseline()

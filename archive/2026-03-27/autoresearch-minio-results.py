#!/usr/bin/env python3
"""
AutoResearch with MinIO Result Storage
Workers write results to MinIO, we poll for them
"""

import os
import sys
import json
import time
import boto3
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from laddr_client import LaddrClient

# MinIO config
MINIO_ENDPOINT = "https://s3.chainbytes.io"
MINIO_ACCESS_KEY = "chainbytes"
MINIO_SECRET_KEY = "chainbytes2026"
RESULTS_BUCKET = "laddr-results"

class AutoResearchMinIO:
    def __init__(self):
        self.client = LaddrClient()
        self.s3 = boto3.client(
            's3',
            endpoint_url=MINIO_ENDPOINT,
            aws_access_key_id=MINIO_ACCESS_KEY,
            aws_secret_access_key=MINIO_SECRET_KEY,
            region_name='us-east-1'
        )
        self._ensure_bucket()
    
    def _ensure_bucket(self):
        """Create results bucket if it doesn't exist."""
        try:
            self.s3.head_bucket(Bucket=RESULTS_BUCKET)
        except:
            try:
                self.s3.create_bucket(Bucket=RESULTS_BUCKET)
                print(f"✅ Created bucket: {RESULTS_BUCKET}")
            except Exception as e:
                print(f"⚠️ Bucket issue: {e}")
    
    def submit_baseline(self):
        """Submit baseline training job."""
        import uuid
        job_id = f"baseline-{uuid.uuid4().hex[:8]}"
        
        # The worker will write to this key when done
        result_key = f"results/{job_id}.json"
        
        job = self.client.submit_job(
            user_prompt=f'''Run Karpathy AutoResearch baseline.

cd /root/.openclaw/workspace/autoresearch && uv run train.py

Extract and report these metrics:
- val_bpb
- training_seconds
- peak_vram_mb
- mfu_percent
- total_tokens_M
- num_params_M
- depth

After training, write results to MinIO:
Bucket: {RESULTS_BUCKET}
Key: {result_key}

Format:
{{
  "job_id": "{job_id}",
  "val_bpb": X.XXXX,
  "training_seconds": XXX.X,
  "peak_vram_mb": XXXX.X,
  "mfu_percent": XX.X,
  "total_tokens_M": XXX.X,
  "num_params_M": XX.X,
  "depth": X,
  "status": "completed"
}}''',
            system_prompt='Execute ML training, extract metrics, and write results to MinIO S3.',
            priority='critical',
            timeout_seconds=600
        )
        
        print(f"✅ Job submitted: {job_id}")
        print(f"📍 Result will be at: s3://{RESULTS_BUCKET}/{result_key}")
        
        return job_id, result_key
    
    def poll_for_result(self, job_id: str, result_key: str, timeout: int = 600):
        """Poll MinIO for job result."""
        print(f"⏳ Polling MinIO for {job_id}...")
        start = time.time()
        poll_count = 0
        
        while time.time() - start < timeout:
            poll_count += 1
            elapsed = time.time() - start
            
            try:
                # Check if result exists
                self.s3.head_object(Bucket=RESULTS_BUCKET, Key=result_key)
                
                # Get result
                obj = self.s3.get_object(Bucket=RESULTS_BUCKET, Key=result_key)
                result = json.loads(obj['Body'].read())
                
                print(f"\n✅ Result found after {elapsed:.0f}s ({poll_count} polls)")
                return result
                
            except self.s3.exceptions.ClientError as e:
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
        print("🚀 AutoResearch Baseline (MinIO Results)")
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
    runner = AutoResearchMinIO()
    runner.run_baseline()

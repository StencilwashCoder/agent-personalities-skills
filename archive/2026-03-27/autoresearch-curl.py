#!/usr/bin/env python3
"""
AutoResearch using curl for results
Worker uses curl to POST results to a simple HTTP endpoint
"""

import os
import sys
import json
import time
import subprocess
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime
from threading import Thread

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from laddr_client import LaddrClient

RESULTS = {}

class ResultHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass
    
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        try:
            result = json.loads(post_data.decode('utf-8'))
            job_id = result.get('job_id', 'unknown')
            RESULTS[job_id] = result
            
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'{"status": "received"}')
            
            print(f"[RESULT] Received for job {job_id}")
        except Exception as e:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())
    
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(json.dumps({
            "status": "ok",
            "results": RESULTS
        }).encode())

def start_server(port=9999):
    """Start result server."""
    server = HTTPServer(('0.0.0.0', port), ResultHandler)
    print(f"Result server on port {port}")
    server.serve_forever()

class AutoResearchCurl:
    def __init__(self):
        self.client = LaddrClient()
        self.server_port = 9999
        self.server_ip = "47.84.109.85"  # Public IP
    
    def start_result_server(self):
        """Start result server in background."""
        thread = Thread(target=start_server, args=(self.server_port,), daemon=True)
        thread.start()
        time.sleep(1)
        print(f"✅ Result server started on port {self.server_port}")
    
    def submit_baseline(self):
        """Submit baseline training job."""
        import uuid
        job_id = f"baseline-{uuid.uuid4().hex[:8]}"
        
        result_url = f"http://{self.server_ip}:{self.server_port}/"
        
        job = self.client.submit_job(
            user_prompt=f'''Run Karpathy AutoResearch baseline training.

cd /root/.openclaw/workspace/autoresearch && uv run train.py

Extract these metrics from output:
- val_bpb
- training_seconds  
- peak_vram_mb
- mfu_percent

Then POST results as JSON to:
{result_url}

Use curl like this:
curl -X POST "{result_url}" \\
  -H "Content-Type: application/json" \\
  -d '{{"job_id": "{job_id}", "val_bpb": VALUE, "training_seconds": VALUE, "status": "completed"}}'

Or if curl fails, just print the JSON result to stdout.''',
            system_prompt='Execute ML training, extract metrics, and POST results using curl.',
            priority='critical',
            timeout_seconds=600
        )
        
        print(f"✅ Job submitted: {job_id}")
        print(f"📍 POST results to: {result_url}")
        
        return job_id
    
    def poll_for_result(self, job_id: str, timeout: int = 600):
        """Poll local results dict for job result."""
        print(f"⏳ Polling for {job_id}...")
        start = time.time()
        poll_count = 0
        
        while time.time() - start < timeout:
            poll_count += 1
            elapsed = time.time() - start
            
            if job_id in RESULTS:
                result = RESULTS[job_id]
                print(f"\n✅ Result found after {elapsed:.0f}s ({poll_count} polls)")
                return result
            
            print(f"[{elapsed:.0f}s] Poll #{poll_count}: waiting...", end='\r')
            time.sleep(3)
        
        print(f"\n❌ Timeout after {timeout}s")
        return {"error": "Timeout", "status": "timeout"}
    
    def run_baseline(self):
        """Run full baseline experiment."""
        print("=" * 60)
        print("🚀 AutoResearch Baseline (Curl Results)")
        print("=" * 60)
        print(f"Started: {datetime.now().strftime('%H:%M:%S')}")
        print()
        
        # Start result server
        self.start_result_server()
        
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
    runner = AutoResearchCurl()
    runner.run_baseline()

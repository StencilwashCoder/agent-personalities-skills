#!/usr/bin/env python3
"""
AutoResearch on Laddr - CPU mode with proper patches
"""

import os
import sys
import json
import time
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from laddr_client import LaddrClient

PATCH_SCRIPT = '''
import sys

# Read train.py
with open('train.py', 'r') as f:
    content = f.read()

# Replace CUDA code with CPU equivalents
content = content.replace('cap = torch.cuda.get_device_capability()', 'cap = None  # CPU mode')
content = content.replace('repo = "varunneal/flash-attention-3" if cap == (9, 0) else "kernels-community/flash-attn3"', 'repo = None  # CPU mode')
content = content.replace('fa3 = get_kernel(repo).flash_attn_interface', 'fa3 = None  # CPU mode')
content = content.replace('device = "cuda"', 'device = "cpu"')
content = content.replace('torch.cuda.synchronize()', 'pass  # CPU mode')
content = content.replace('torch.cuda.empty_cache()', 'pass  # CPU mode')
content = content.replace('torch.cuda.max_memory_allocated()', '0')
content = content.replace('torch.cuda.current_device()', '0')

# Comment out kernels import (not needed for CPU)
content = content.replace('from kernels import get_kernel', '# from kernels import get_kernel  # CPU mode')

# Write back
with open('train.py', 'w') as f:
    f.write(content)

print("Patched train.py for CPU mode")
'''

class AutoResearchLaddr:
    def __init__(self):
        self.client = LaddrClient()
    
    def submit_baseline(self):
        """Submit baseline training job - CPU mode."""
        job = self.client.submit_job(
            user_prompt=f'''#!/bin/bash
set -e
cd /tmp

# Clean up and clone fresh
rm -rf autoresearch
git clone https://github.com/karpathy/autoresearch.git
cd autoresearch

# Create patch script
cat > patch.py << 'EOF'
{PATCH_SCRIPT}
EOF

# Patch train.py for CPU
python3 patch.py

# Create venv and install deps (CPU-only torch)
python3 -m venv .venv
source .venv/bin/activate
pip install matplotlib numpy pandas pyarrow requests tiktoken kernels rustbpe --quiet 2>&1
pip install torch --index-url https://download.pytorch.org/whl/cpu --quiet 2>&1

# Run training
export PYTHONPATH=/tmp/autoresearch:$PYTHONPATH
python train.py 2>&1 | head -100

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
        print("🚀 AutoResearch Baseline (CPU Mode)")
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

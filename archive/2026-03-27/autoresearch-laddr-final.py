#!/usr/bin/env python3
"""
AutoResearch on Laddr - FINAL version, simplified
"""

import os
import sys
import json
import time
import base64
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from laddr_client import LaddrClient

PATCH_CODE = """
import sys

# Read train.py
with open('train.py', 'r') as f:
    content = f.read()

# CPU patches
content = content.replace('cap = torch.cuda.get_device_capability()', 'cap = None')
content = content.replace('fa3 = get_kernel(repo).flash_attn_interface', 'fa3 = None')
content = content.replace('device = "cuda"', 'device = "cpu"')
content = content.replace('torch.cuda.synchronize()', 'pass')
content = content.replace('torch.cuda.empty_cache()', 'pass')
content = content.replace('torch.cuda.max_memory_allocated()', '0')
content = content.replace('torch.cuda.current_device()', '0')
content = content.replace('model.to_empty(device=device)', 'model.to_empty(device="cpu")')
content = content.replace('from kernels import get_kernel', '# from kernels import get_kernel')
content = content.replace('y = fa3.flash_attn_func(q, k, v, causal=True, window_size=window_size)', 'y = F.scaled_dot_product_attention(q, k, v, is_causal=True)')

# DISABLE torch.compile completely - handle all variants
import re
content = re.sub(r'@torch\.compile\([^)]*\)', '# torch.compile disabled', content)
content = content.replace('model = torch.compile(model)', '# model = torch.compile(model)')

with open('train.py', 'w') as f:
    f.write(content)
print('Patched train.py')

# Read prepare.py  
with open('prepare.py', 'r') as f:
    content = f.read()
content = content.replace('device="cuda"', 'device="cpu"')
content = content.replace('torch.cuda.current_device()', '0')
with open('prepare.py', 'w') as f:
    f.write(content)
print('Patched prepare.py')
"""

class AutoResearchLaddr:
    def __init__(self):
        self.client = LaddrClient()
    
    def submit_baseline(self):
        patch_b64 = base64.b64encode(PATCH_CODE.encode()).decode()
        
        job_script = f'''#!/bin/bash
set -e
cd /tmp
rm -rf autoresearch
git clone https://github.com/karpathy/autoresearch.git
cd autoresearch

echo "{patch_b64}" | base64 -d > patch.py
python3 patch.py

python3 -m venv .venv
source .venv/bin/activate
pip install matplotlib numpy pandas pyarrow requests tiktoken kernels rustbpe -q 2>&1
pip install torch --index-url https://download.pytorch.org/whl/cpu -q 2>&1

echo "=== PREPARE ==="
python prepare.py --num-shards 2 2>&1 | tail -15

echo "=== TRAIN ==="
export PYTHONPATH=/tmp/autoresearch:$PYTHONPATH
export TORCH_COMPILE_DISABLE=1
python train.py 2>&1 | head -100

echo "=== DONE ==="'''

        job = self.client.submit_job(
            user_prompt=job_script,
            system_prompt='Execute command',
            priority='critical',
            timeout_seconds=600
        )
        
        job_id = job['job_id']
        print(f"✅ Job submitted: {job_id}")
        return job_id
    
    def poll_for_result(self, job_id: str, timeout: int = 600):
        print(f"⏳ Polling for {job_id}...")
        start = time.time()
        
        while time.time() - start < timeout:
            try:
                response = self.client.get_job_result(job_id)
                if response.get('status') != 'pending':
                    elapsed = time.time() - start
                    print(f"\n✅ Result after {elapsed:.0f}s")
                    return response
            except Exception as e:
                pass
            time.sleep(3)
        
        return {"error": "Timeout", "status": "timeout"}
    
    def run_baseline(self):
        print("=" * 60)
        print("🚀 AutoResearch Baseline")
        print("=" * 60)
        
        job_id = self.submit_baseline()
        result = self.poll_for_result(job_id)
        
        print()
        print("=" * 60)
        print("📊 RESULTS")
        print("=" * 60)
        print(json.dumps(result, indent=2))
        
        return result

if __name__ == "__main__":
    runner = AutoResearchLaddr()
    runner.run_baseline()

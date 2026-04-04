#!/usr/bin/env python3
"""
Submit AutoResearch training job to Laddr cluster
"""

import sys
import os
sys.path.insert(0, '/root/.openclaw/workspace')

from laddr_client import LaddrClient

# Training job prompt for Mac/MPS
TRAINING_PROMPT = '''
Run Karpathy AutoResearch baseline training on Mac/MPS.

Setup:
1. cd /tmp && git clone https://github.com/miolini/autoresearch-macos.git autoresearch-run
2. cd autoresearch-run

Data Preparation (if not cached):
3. uv sync
4. uv run prepare.py --num-shards 2

Training:
5. uv run train.py

Extract and report in this exact format:
```json
{
  "val_bpb": <number>,
  "training_seconds": <number>,
  "peak_vram_mb": <number>,
  "mfu_percent": <number>,
  "num_params_M": <number>,
  "depth": <number>,
  "device": "mps",
  "success": true
}
```

If training fails, report:
```json
{
  "success": false,
  "error": "description of what failed"
}
```
'''

def main():
    client = LaddrClient()
    
    # Submit job with script-exec requirement
    job = client.submit_job(
        user_prompt=TRAINING_PROMPT,
        system_prompt="You are an ML engineer running training experiments. Execute commands carefully and report exact metrics from the training output.",
        requirements={"mode": "script-exec"},
        priority="high",
        timeout_seconds=900  # 15 minutes for data prep + training
    )
    
    print("🚀 AutoResearch Training Job Submitted")
    print(f"   Job ID: {job['job_id']}")
    print(f"   Status: {job['status']}")
    print(f"   Target: Laddr Mac workers with MPS")
    print()
    print("⏳ Training takes ~5-10 minutes (including data prep)")
    print("📊 Results will be sent via webhook")
    
    return job

if __name__ == "__main__":
    job = main()
    print(f"\nJob ID for tracking: {job['job_id']}")

#!/usr/bin/env python3
"""
AutoResearch Experiment Loop
Submits iterative training experiments to Laddr cluster
"""

import os
import sys
import json
import time
import random
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from laddr_client import LaddrClient

class AutoResearchLoop:
    def __init__(self):
        self.client = LaddrClient()
        self.experiment_count = 0
        self.best_val_bpb = float('inf')
        self.best_job_id = None
        self.results_log = []
    
    def generate_experiment_idea(self, baseline_result: dict = None) -> str:
        """Generate next experiment idea based on previous results."""
        
        ideas = [
            "Increase learning rate from 0.001 to 0.003",
            "Add dropout layer with rate 0.1",
            "Increase batch size by 2x",
            "Use AdamW instead of Muon optimizer",
            "Add gradient clipping at 1.0",
            "Increase model depth by 2 layers",
            "Use GeLU activation instead of SwiGLU",
            "Add LayerNorm before attention",
            "Use rotary embeddings instead of learned positional",
            "Increase warmup steps from 100 to 200",
            "Add weight decay 0.01",
            "Use cosine schedule instead of linear",
            "Double the embedding dimension",
            "Add residual connection modification",
            "Use different initialization (xavier vs kaiming)",
        ]
        
        if baseline_result:
            # Could do smarter selection based on what worked
            return random.choice(ideas)
        
        return "Run baseline - no changes"
    
    def submit_experiment(self, experiment_idea: str, is_baseline: bool = False) -> dict:
        """Submit an experiment to Laddr."""
        
        if is_baseline:
            prompt = '''Run Karpathy AutoResearch baseline.

cd /root/.openclaw/workspace/autoresearch && uv run train.py

Extract and report:
- val_bpb (lower is better)
- training_seconds
- peak_vram_mb
- mfu_percent
- num_params_M
- depth

Format: JSON'''
        else:
            prompt = f'''Modify train.py for this experiment: {experiment_idea}

1. Read current train.py
2. Apply the modification: {experiment_idea}
3. Save changes
4. Run: uv run train.py
5. Report results in JSON:
{{
  "val_bpb": X.XXXX,
  "training_seconds": XXX.X,
  "peak_vram_mb": XXXX.X,
  "mfu_percent": XX.X,
  "modification": "description of what was changed",
  "success": true/false
}}

If the run fails (OOM, error), report success: false with error message.'''
        
        job = self.client.submit_job(
            user_prompt=prompt,
            system_prompt="You are an ML researcher running experiments. Modify code carefully, run training, report exact metrics.",
            priority="high" if is_baseline else "normal",
            timeout_seconds=600
        )
        
        self.experiment_count += 1
        
        print(f"🧪 Experiment #{self.experiment_count} submitted")
        print(f"   Job ID: {job['job_id']}")
        print(f"   Idea: {experiment_idea if not is_baseline else 'BASELINE'}")
        
        return job
    
    def run_baseline(self):
        """Run baseline experiment."""
        print("=" * 60)
        print("🚀 Starting AutoResearch Baseline")
        print("=" * 60)
        
        job = self.submit_experiment("baseline", is_baseline=True)
        
        print(f"\n✅ Baseline submitted: {job['job_id']}")
        print("⏳ Result will come via webhook to Telegram")
        print("\nNext: Start iteration loop after baseline completes")
        
        return job
    
    def run_iteration(self, count: int = 10):
        """Run N experiments iteratively."""
        print(f"\n🔄 Starting {count} iteration experiments")
        print("=" * 60)
        
        for i in range(count):
            idea = self.generate_experiment_idea()
            job = self.submit_experiment(idea)
            
            # Wait a bit between submissions to not overwhelm
            if i < count - 1:
                time.sleep(5)
        
        print(f"\n✅ {count} experiments submitted")
        print("📊 Results will arrive via webhook")
    
    def run_overnight(self, count: int = 100):
        """Run overnight batch."""
        print(f"\n🌙 Starting overnight batch: {count} experiments")
        print("=" * 60)
        
        # Submit all with normal priority (will queue up)
        for i in range(count):
            idea = self.generate_experiment_idea()
            job = self.client.submit_job(
                user_prompt=f'''Experiment {i+1}/{count}: {idea}

cd /root/.openclaw/workspace/autoresearch
# Modify train.py: {idea}
uv run train.py
# Report val_bpb and whether it improved''',
                system_prompt="ML researcher running experiments",
                priority="low",  # Lower priority for batch
                timeout_seconds=600
            )
            
            if (i + 1) % 10 == 0:
                print(f"  Submitted {i+1}/{count}...")
            
            time.sleep(1)  # Rate limit
        
        print(f"\n✅ {count} experiments queued for overnight run")
        print("🌅 Check Telegram in the morning for results!")

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="AutoResearch Experiment Loop")
    parser.add_argument("mode", choices=["baseline", "iter", "overnight"], 
                       help="Run mode: baseline, iter (10 exp), or overnight (100 exp)")
    
    args = parser.parse_args()
    
    loop = AutoResearchLoop()
    
    if args.mode == "baseline":
        loop.run_baseline()
    elif args.mode == "iter":
        loop.run_iteration(10)
    elif args.mode == "overnight":
        loop.run_overnight(100)

if __name__ == "__main__":
    main()

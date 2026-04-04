#!/usr/bin/env python3
"""
Submit job to Laddr cluster (Eric's distributed Mac GPU fleet)
Replaces local LM Studio for cloud-based inference
"""

import os
import sys
import json
import argparse
from datetime import datetime

# Add parent dir to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from laddr_client import LaddrClient

def submit_job(
    user_prompt: str,
    system_prompt: str = "You are a helpful assistant.",
    priority: str = "normal",
    mode: str = "generic",
    timeout: int = 120,
    wait: bool = False
):
    """Submit a job to Laddr cluster."""
    
    client = LaddrClient()
    
    print(f"Submitting to Laddr cluster...")
    print(f"  Priority: {priority}")
    print(f"  Mode: {mode}")
    print(f"  Timeout: {timeout}s")
    
    job = client.submit_job(
        user_prompt=user_prompt,
        system_prompt=system_prompt,
        priority=priority,
        requirements={"mode": mode},
        timeout_seconds=timeout
    )
    
    print(f"\n✅ Job submitted!")
    print(f"  Job ID: {job['job_id']}")
    print(f"  Status: {job['status']}")
    
    if wait:
        print(f"\n⏳ Waiting for result (not implemented - use callback or poll Redis)...")
    
    return job

def check_fleet():
    """Check fleet status."""
    client = LaddrClient()
    
    print("Laddr Fleet Status\n")
    
    workers = client.get_fleet_status()
    for worker in workers.get("workers", []):
        print(f"🖥️  {worker['name']}")
        print(f"   Models: {len(worker.get('models', []))}")
        print(f"   Capacity: {worker.get('capacity', 'unknown')}")
        print()
    
    queue = client.get_queue_depth()
    print("Queue Depth:")
    for priority, count in queue.items():
        print(f"  {priority}: {count}")
    
    stats = client.get_dispatcher_stats()
    print(f"\nDispatcher: {json.dumps(stats, indent=2)}")

def main():
    parser = argparse.ArgumentParser(description="Submit jobs to Laddr cluster")
    parser.add_argument("--prompt", "-p", required=True, help="User prompt")
    parser.add_argument("--system", "-s", default="You are a helpful assistant.", help="System prompt")
    parser.add_argument("--priority", default="normal", choices=["critical", "high", "normal", "low"])
    parser.add_argument("--mode", "-m", default="generic", help="Requirement mode (generic, template:xyz, explicit)")
    parser.add_argument("--timeout", "-t", type=int, default=120, help="Timeout in seconds")
    parser.add_argument("--wait", "-w", action="store_true", help="Wait for result")
    parser.add_argument("--fleet", action="store_true", help="Check fleet status instead of submitting")
    
    args = parser.parse_args()
    
    if args.fleet:
        check_fleet()
    else:
        submit_job(
            user_prompt=args.prompt,
            system_prompt=args.system,
            priority=args.priority,
            mode=args.mode,
            timeout=args.timeout,
            wait=args.wait
        )

if __name__ == "__main__":
    main()

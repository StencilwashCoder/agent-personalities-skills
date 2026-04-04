#!/usr/bin/env python3
"""
Submit AI Job to Queue
Usage: python submit_job.py --prompt "Your prompt here" --priority 1 --model "llama-3.1-70b"
"""

import os
import json
import uuid
import argparse
from datetime import datetime

import boto3

def submit_job(
    user_prompt: str,
    system_prompt: str = "You are a helpful assistant.",
    priority: int = 5,
    model: str = "local-model",
    temperature: float = 0.7,
    max_tokens: int = 4096,
    skills: list = None,
    context_files: list = None,
    metadata: dict = None,
    callback_url: str = None
):
    """Submit a job to the AI queue."""
    
    # S3 config
    s3 = boto3.client(
        's3',
        endpoint_url=os.getenv('S3_ENDPOINT', 'https://s3.chainbytes.io'),
        aws_access_key_id=os.getenv('S3_ACCESS_KEY', 'chainbytes'),
        aws_secret_access_key=os.getenv('S3_SECRET_KEY', 'chainbytes2026'),
        region_name=os.getenv('S3_REGION', 'us-east-1')
    )
    
    bucket = os.getenv('JOBS_BUCKET', 'ai-jobs')
    
    # Build job
    job = {
        "id": str(uuid.uuid4()),
        "priority": priority,
        "model": model,
        "system_prompt": system_prompt,
        "user_prompt": user_prompt,
        "parameters": {
            "temperature": temperature,
            "max_tokens": max_tokens,
            "top_p": 1.0,
            "frequency_penalty": 0,
            "presence_penalty": 0
        },
        "skills": skills or [],
        "context_files": context_files or [],
        "streaming": False,
        "callback_url": callback_url,
        "metadata": metadata or {
            "submitted_by": os.getenv('USER', 'unknown'),
            "source": "cli"
        },
        "created_at": datetime.utcnow().isoformat(),
        "requested_by": os.getenv('USER', 'patchrat')
    }
    
    # Upload to incoming
    key = f"incoming/{job['id']}.json"
    s3.put_object(
        Bucket=bucket,
        Key=key,
        Body=json.dumps(job, indent=2).encode(),
        ContentType='application/json'
    )
    
    print(f"✅ Job submitted: {job['id']}")
    print(f"   Priority: {priority} (1=high, 10=low)")
    print(f"   Model: {model}")
    print(f"   Waiting for worker...")
    
    return job['id']

def wait_for_result(job_id: str, timeout: int = 300):
    """Poll for job result."""
    import time
    
    s3 = boto3.client(
        's3',
        endpoint_url=os.getenv('S3_ENDPOINT', 'https://s3.chainbytes.io'),
        aws_access_key_id=os.getenv('S3_ACCESS_KEY', 'chainbytes'),
        aws_secret_access_key=os.getenv('S3_SECRET_KEY', 'chainbytes2026'),
        region_name=os.getenv('S3_REGION', 'us-east-1')
    )
    
    bucket = os.getenv('JOBS_BUCKET', 'ai-jobs')
    result_key = f"completed/{job_id}-result.json"
    
    print(f"⏳ Waiting for result (timeout: {timeout}s)...")
    
    start = time.time()
    while time.time() - start < timeout:
        try:
            response = s3.get_object(Bucket=bucket, Key=result_key)
            result = json.loads(response['Body'].read())
            
            if result['success']:
                print(f"\n✅ Job completed in {result['result']['duration_seconds']:.2f}s")
                print(f"\n📝 Result:\n{result['result']['content']}")
            else:
                print(f"\n❌ Job failed: {result.get('error', 'Unknown error')}")
            
            return result
            
        except s3.exceptions.NoSuchKey:
            time.sleep(1)
            continue
    
    print("⏰ Timeout waiting for result")
    return None

def main():
    parser = argparse.ArgumentParser(description='Submit AI job to queue')
    parser.add_argument('--prompt', '-p', required=True, help='User prompt')
    parser.add_argument('--system', '-s', default='You are a helpful assistant.', help='System prompt')
    parser.add_argument('--priority', type=int, default=5, help='Priority 1-10 (1=high)')
    parser.add_argument('--model', '-m', default='local-model', help='Model name in LM Studio')
    parser.add_argument('--temp', type=float, default=0.7, help='Temperature')
    parser.add_argument('--tokens', type=int, default=4096, help='Max tokens')
    parser.add_argument('--wait', '-w', action='store_true', help='Wait for result')
    parser.add_argument('--skill', action='append', help='Skill file (bucket:key)')
    
    args = parser.parse_args()
    
    # Parse skills
    skills = []
    if args.skill:
        for s in args.skill:
            parts = s.split(':')
            if len(parts) == 2:
                skills.append({'bucket': parts[0], 'key': parts[1]})
    
    job_id = submit_job(
        user_prompt=args.prompt,
        system_prompt=args.system,
        priority=args.priority,
        model=args.model,
        temperature=args.temp,
        max_tokens=args.tokens,
        skills=skills
    )
    
    if args.wait:
        wait_for_result(job_id)

if __name__ == '__main__':
    main()

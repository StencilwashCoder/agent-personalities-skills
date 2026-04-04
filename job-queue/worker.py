#!/usr/bin/env python3
"""
AI Job Queue Worker
Runs on local machine with LM Studio, polls MinIO for jobs.
"""

import os
import json
import time
import uuid
import logging
from datetime import datetime
from typing import Optional, Dict, Any

import boto3
import requests
from botocore.exceptions import ClientError
from tenacity import retry, stop_after_attempt, wait_exponential

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class JobWorker:
    def __init__(self):
        # MinIO config
        self.s3_endpoint = os.getenv('S3_ENDPOINT', 'https://s3.chainbytes.io')
        self.s3_access_key = os.getenv('S3_ACCESS_KEY', 'chainbytes')
        self.s3_secret_key = os.getenv('S3_SECRET_KEY', 'chainbytes2026')
        self.s3_region = os.getenv('S3_REGION', 'us-east-1')
        self.bucket = os.getenv('JOBS_BUCKET', 'ai-jobs')
        
        # LM Studio config
        self.lmstudio_url = os.getenv('LMSTUDIO_URL', 'http://localhost:1234')
        self.lmstudio_api_key = os.getenv('LMSTUDIO_API_KEY', '')
        
        # Worker config
        self.worker_id = os.getenv('WORKER_ID', str(uuid.uuid4())[:8])
        self.poll_interval = float(os.getenv('POLL_INTERVAL', '1.0'))  # seconds
        self.max_jobs = int(os.getenv('MAX_JOBS', '10'))  # jobs before restart
        
        # Initialize S3 client
        self.s3 = boto3.client(
            's3',
            endpoint_url=self.s3_endpoint,
            aws_access_key_id=self.s3_access_key,
            aws_secret_access_key=self.s3_secret_key,
            region_name=self.s3_region
        )
        
        self.jobs_processed = 0
        
        logger.info(f"Worker {self.worker_id} started")
        logger.info(f"S3 Endpoint: {self.s3_endpoint}")
        logger.info(f"LM Studio: {self.lmstudio_url}")
        logger.info(f"Poll interval: {self.poll_interval}s")
    
    def ensure_buckets_exist(self):
        """Create buckets if they don't exist."""
        folders = ['incoming', 'processing', 'completed', 'failed']
        for folder in folders:
            try:
                self.s3.put_object(Bucket=self.bucket, Key=f"{folder}/", Body=b'')
                logger.info(f"Ensured bucket folder: {folder}/")
            except Exception as e:
                logger.warning(f"Could not create folder {folder}: {e}")
    
    def list_pending_jobs(self) -> list:
        """List jobs in incoming folder, sorted by priority."""
        try:
            response = self.s3.list_objects_v2(
                Bucket=self.bucket,
                Prefix='incoming/',
                MaxKeys=100
            )
            
            jobs = []
            for obj in response.get('Contents', []):
                key = obj['Key']
                if key.endswith('.json'):
                    try:
                        # Get job to check priority
                        job_data = self.s3.get_object(Bucket=self.bucket, Key=key)
                        job = json.loads(job_data['Body'].read())
                        jobs.append({
                            'key': key,
                            'priority': job.get('priority', 10),
                            'created_at': job.get('created_at', ''),
                            'id': job.get('id', '')
                        })
                    except Exception as e:
                        logger.warning(f"Could not read job {key}: {e}")
            
            # Sort by priority (lower = higher priority), then by created_at
            jobs.sort(key=lambda x: (x['priority'], x['created_at']))
            return jobs
            
        except Exception as e:
            logger.error(f"Error listing jobs: {e}")
            return []
    
    def move_job(self, source_key: str, dest_folder: str) -> str:
        """Move job file to different folder."""
        filename = source_key.split('/')[-1]
        dest_key = f"{dest_folder}/{filename}"
        
        # Copy to destination
        self.s3.copy_object(
            Bucket=self.bucket,
            CopySource={'Bucket': self.bucket, 'Key': source_key},
            Key=dest_key
        )
        
        # Delete from source
        self.s3.delete_object(Bucket=self.bucket, Key=source_key)
        
        return dest_key
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
    def call_lmstudio(self, job: Dict[str, Any]) -> Dict[str, Any]:
        """Call LM Studio API with job parameters."""
        
        # Build messages
        messages = []
        
        # Add system prompt if provided
        if job.get('system_prompt'):
            messages.append({
                "role": "system",
                "content": job['system_prompt']
            })
        
        # Load skills as additional context
        skills_context = ""
        for skill in job.get('skills', []):
            try:
                skill_data = self.s3.get_object(
                    Bucket=skill['bucket'],
                    Key=skill['key']
                )
                skills_context += f"\n\n### Skill: {skill['key']}\n{skill_data['Body'].read().decode()}"
            except Exception as e:
                logger.warning(f"Could not load skill {skill}: {e}")
        
        # Load context files
        context = ""
        for ctx_file in job.get('context_files', []):
            try:
                file_data = self.s3.get_object(
                    Bucket=ctx_file['bucket'],
                    Key=ctx_file['key']
                )
                context += f"\n\n### Context: {ctx_file['key']}\n{file_data['Body'].read().decode()}"
            except Exception as e:
                logger.warning(f"Could not load context {ctx_file}: {e}")
        
        # Build final user message
        user_content = job['user_prompt']
        if skills_context:
            user_content = f"[SKILLS]{skills_context}\n\n[REQUEST]\n{user_content}"
        if context:
            user_content = f"{context}\n\n{user_content}"
        
        messages.append({
            "role": "user",
            "content": user_content
        })
        
        # Prepare request
        params = job.get('parameters', {})
        payload = {
            "model": job.get('model', 'local-model'),
            "messages": messages,
            "temperature": params.get('temperature', 0.7),
            "max_tokens": params.get('max_tokens', 4096),
            "top_p": params.get('top_p', 1.0),
            "frequency_penalty": params.get('frequency_penalty', 0),
            "presence_penalty": params.get('presence_penalty', 0),
            "stream": job.get('streaming', False)
        }
        
        headers = {"Content-Type": "application/json"}
        if self.lmstudio_api_key:
            headers["Authorization"] = f"Bearer {self.lmstudio_api_key}"
        
        # Call LM Studio
        logger.info(f"Calling LM Studio with model: {job.get('model')}")
        start_time = time.time()
        
        response = requests.post(
            f"{self.lmstudio_url}/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=300  # 5 minute timeout
        )
        response.raise_for_status()
        
        duration = time.time() - start_time
        result = response.json()
        
        logger.info(f"LM Studio response received in {duration:.2f}s")
        
        return {
            "success": True,
            "duration_seconds": duration,
            "model_used": result.get('model', job.get('model')),
            "content": result['choices'][0]['message']['content'],
            "usage": result.get('usage', {}),
            "finish_reason": result['choices'][0].get('finish_reason', 'unknown')
        }
    
    def process_job(self, job_key: str) -> bool:
        """Process a single job."""
        logger.info(f"Processing job: {job_key}")
        
        try:
            # Read job
            job_data = self.s3.get_object(Bucket=self.bucket, Key=job_key)
            job = json.loads(job_data['Body'].read())
            
            job_id = job.get('id', 'unknown')
            logger.info(f"Job {job_id} - Priority: {job.get('priority')} - Model: {job.get('model')}")
            
            # Move to processing
            processing_key = self.move_job(job_key, 'processing')
            
            # Update job with worker info
            job['worker_id'] = self.worker_id
            job['started_at'] = datetime.utcnow().isoformat()
            
            # Save updated job
            self.s3.put_object(
                Bucket=self.bucket,
                Key=processing_key,
                Body=json.dumps(job, indent=2).encode()
            )
            
            # Call LM Studio
            try:
                result = self.call_lmstudio(job)
                
                # Build result object
                result_obj = {
                    "job_id": job_id,
                    "worker_id": self.worker_id,
                    "success": True,
                    "started_at": job['started_at'],
                    "completed_at": datetime.utcnow().isoformat(),
                    "result": result
                }
                
            except Exception as e:
                logger.error(f"Job {job_id} failed: {e}")
                result_obj = {
                    "job_id": job_id,
                    "worker_id": self.worker_id,
                    "success": False,
                    "started_at": job['started_at'],
                    "completed_at": datetime.utcnow().isoformat(),
                    "error": str(e)
                }
            
            # Save result
            result_key = f"completed/{job_id}-result.json"
            self.s3.put_object(
                Bucket=self.bucket,
                Key=result_key,
                Body=json.dumps(result_obj, indent=2).encode()
            )
            
            # Move job to completed (or failed)
            if result_obj['success']:
                self.move_job(processing_key, 'completed')
                logger.info(f"Job {job_id} completed successfully")
            else:
                self.move_job(processing_key, 'failed')
                logger.warning(f"Job {job_id} failed, moved to failed/")
            
            # Call webhook if provided
            if job.get('callback_url'):
                try:
                    requests.post(job['callback_url'], json=result_obj, timeout=10)
                except Exception as e:
                    logger.warning(f"Webhook failed: {e}")
            
            self.jobs_processed += 1
            return result_obj['success']
            
        except Exception as e:
            logger.error(f"Error processing job {job_key}: {e}")
            return False
    
    def run(self):
        """Main worker loop."""
        logger.info("Starting worker loop...")
        self.ensure_buckets_exist()
        
        while True:
            try:
                # Check if we've hit max jobs
                if self.jobs_processed >= self.max_jobs:
                    logger.info(f"Processed {self.max_jobs} jobs, restarting...")
                    break
                
                # List pending jobs
                jobs = self.list_pending_jobs()
                
                if not jobs:
                    logger.debug("No pending jobs, sleeping...")
                    time.sleep(self.poll_interval)
                    continue
                
                # Process highest priority job
                job = jobs[0]
                logger.info(f"Found {len(jobs)} pending jobs, processing highest priority")
                
                self.process_job(job['key'])
                
                # Small delay between jobs
                time.sleep(0.1)
                
            except KeyboardInterrupt:
                logger.info("Worker stopped by user")
                break
            except Exception as e:
                logger.error(f"Error in worker loop: {e}")
                time.sleep(self.poll_interval)

if __name__ == '__main__':
    worker = JobWorker()
    worker.run()

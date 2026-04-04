#!/usr/bin/env python3
"""
Laddr API Client
Distributed LLM inference across Eric's Mac cluster.
Uses requests library (no httpx dependency).
"""

import os
import json
import time
import urllib.request
import urllib.parse
from typing import Optional, Dict, Any
from datetime import datetime

LADDR_BASE_URL = os.getenv("LADDR_URL", "http://134.122.8.237:8000")
LADDR_API_KEY = os.getenv("LADDR_API_KEY", "628d73c47741dabd9d077d7df5ae4c05ffaada3a5fb5263f")
LADDR_CALLBACK_URL = os.getenv("LADDR_CALLBACK_URL", "http://10.184.210.48:8080/")  # Using internal IP

class LaddrClient:
    def __init__(self, base_url: str = None, api_key: str = None, callback_url: str = None):
        self.base_url = base_url or LADDR_BASE_URL
        self.api_key = api_key or LADDR_API_KEY
        self.callback_url = callback_url or LADDR_CALLBACK_URL
    
    def _request(self, method: str, path: str, data: dict = None) -> dict:
        """Make HTTP request."""
        url = f"{self.base_url}{path}"
        headers = {
            "X-API-Key": self.api_key,
            "Content-Type": "application/json"
        }
        
        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode() if data else None,
            headers=headers,
            method=method
        )
        
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode())
    
    def submit_job(
        self,
        user_prompt: str,
        system_prompt: str = "You are a helpful assistant.",
        requirements: Dict[str, Any] = None,
        priority: str = "normal",
        timeout_seconds: int = 120,
        callback_url: str = None
    ) -> Dict[str, Any]:
        """Submit a job to the Laddr cluster."""
        
        payload = {
            "system_prompt": system_prompt,
            "user_prompt": user_prompt,
            "requirements": requirements or {"mode": "generic"},
            "priority": priority,
            "timeout_seconds": int(timeout_seconds)  # Ensure integer
        }
        
        if callback_url:
            payload["callback_url"] = callback_url
        elif self.callback_url:
            payload["callback_url"] = self.callback_url
        
        return self._request("POST", "/api/jobs/capability", payload)
    
    def get_fleet_status(self) -> Dict[str, Any]:
        """Get status of all workers."""
        return self._request("GET", "/api/workers")
    
    def get_queue_depth(self) -> Dict[str, Any]:
        """Get queue depths by priority."""
        return self._request("GET", "/api/queue")
    
    def get_templates(self) -> list:
        """List available job templates."""
        return self._request("GET", "/api/templates")
    
    def get_dispatcher_stats(self) -> Dict[str, Any]:
        """Get dispatcher metrics."""
        return self._request("GET", "/api/dispatcher/stats")
    
    def get_job_result(self, job_id: str) -> Dict[str, Any]:
        """Get job result (poll until complete).
        
        Returns:
            202 - still running, poll again
            200 - done, result in response body
            404 - expired or never existed
        """
        return self._request("GET", f"/api/jobs/{job_id}/result")
    
    def get_response(self, task_id: str) -> Dict[str, Any]:
        """Get resolved response for a task."""
        return self._request("GET", f"/api/responses/{task_id}/resolved")
    
    def wait_for_job(
        self,
        job_id: str,
        poll_interval: int = 5,
        timeout: int = 600
    ) -> Dict[str, Any]:
        """Poll for job completion and return result."""
        import time
        start = time.time()
        
        while time.time() - start < timeout:
            status = self.get_job_status(job_id)
            state = status.get('status', 'unknown')
            
            if state == 'completed':
                return status.get('result', {})
            elif state == 'failed':
                return {'error': status.get('error', 'Unknown error'), 'status': 'failed'}
            elif state == 'cancelled':
                return {'error': 'Job cancelled', 'status': 'cancelled'}
            
            time.sleep(poll_interval)
        
        return {'error': f'Timeout after {timeout}s', 'status': 'timeout'}
    
    def submit_and_wait(
        self,
        user_prompt: str,
        system_prompt: str = "You are a helpful assistant.",
        requirements: Dict[str, Any] = None,
        priority: str = "normal",
        timeout_seconds: int = 120,
        poll_interval: int = 5
    ) -> Dict[str, Any]:
        """Submit job and poll for result (no webhook needed)."""
        job = self.submit_job(
            user_prompt=user_prompt,
            system_prompt=system_prompt,
            requirements=requirements,
            priority=priority,
            timeout_seconds=timeout_seconds
        )
        
        job_id = job['job_id']
        print(f"Job {job_id} queued, polling for result...")
        
        return self.wait_for_job(job_id, poll_interval, timeout_seconds + 60)
    
    def quick_chat(
        self,
        prompt: str,
        system: str = None,
        priority: str = "normal"
    ) -> str:
        """Quick one-off chat completion."""
        job = self.submit_job(
            user_prompt=prompt,
            system_prompt=system or "You are a helpful assistant.",
            priority=priority
        )
        return f"Job queued: {job['job_id']} (status: {job['status']})"

# CLI interface
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Laddr API Client")
    parser.add_argument("command", choices=["submit", "fleet", "queue", "templates", "stats"])
    parser.add_argument("--prompt", "-p", help="User prompt")
    parser.add_argument("--system", "-s", default="You are a helpful assistant.", help="System prompt")
    parser.add_argument("--priority", default="normal", choices=["critical", "high", "normal", "low"])
    parser.add_argument("--mode", default="generic", help="Requirement mode")
    
    args = parser.parse_args()
    
    client = LaddrClient()
    
    if args.command == "submit":
        if not args.prompt:
            print("Error: --prompt required for submit")
            exit(1)
        
        result = client.submit_job(
            user_prompt=args.prompt,
            system_prompt=args.system,
            priority=args.priority,
            requirements={"mode": args.mode}
        )
        print(json.dumps(result, indent=2))
    
    elif args.command == "fleet":
        result = client.get_fleet_status()
        print(json.dumps(result, indent=2))
    
    elif args.command == "queue":
        result = client.get_queue_depth()
        print(json.dumps(result, indent=2))
    
    elif args.command == "templates":
        result = client.get_templates()
        print(json.dumps(result, indent=2))
    
    elif args.command == "stats":
        result = client.get_dispatcher_stats()
        print(json.dumps(result, indent=2))

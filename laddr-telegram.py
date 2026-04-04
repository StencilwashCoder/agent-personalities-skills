#!/usr/bin/env python3
"""
Submit AI job via Laddr and send result to Telegram
"""

import os
import sys
import json
import time
import urllib.request
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from laddr_client import LaddrClient

TELEGRAM_TOKEN = "8600179570:AAGn9cHOVqgj5JYJ9jAcXR-BlSrgwRJbWTw"
TELEGRAM_CHAT = "84020120"

def send_telegram(message: str):
    """Send message to Telegram."""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = urllib.parse.urlencode({
        "chat_id": TELEGRAM_CHAT,
        "text": message,
        "parse_mode": "Markdown"
    }).encode()
    
    try:
        urllib.request.urlopen(url, data=data, timeout=10)
    except Exception as e:
        print(f"Telegram error: {e}")

def submit_and_notify(
    prompt: str,
    system: str = None,
    priority: str = "normal"
):
    """Submit to Laddr and notify Telegram."""
    
    client = LaddrClient()
    
    # Submit job
    job = client.submit_job(
        user_prompt=prompt,
        system_prompt=system or "You are a helpful assistant.",
        priority=priority,
        requirements={"mode": "generic"}
    )
    
    # Notify
    msg = f"🚀 *Job Submitted to Laddr*\n\n"
    msg += f"Job ID: `{job['job_id']}`\n"
    msg += f"Priority: {priority}\n"
    msg += f"Status: {job['status']}\n\n"
    msg += f"Prompt: {prompt[:100]}..."
    
    send_telegram(msg)
    
    print(f"Job submitted: {job['job_id']}")
    print(f"Telegram notification sent")
    
    return job

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", "-p", required=True)
    parser.add_argument("--system", "-s")
    parser.add_argument("--priority", default="normal")
    
    args = parser.parse_args()
    
    submit_and_notify(
        prompt=args.prompt,
        system=args.system,
        priority=args.priority
    )

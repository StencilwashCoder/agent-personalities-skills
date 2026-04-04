#!/usr/bin/env python3
"""
Laddr Webhook Receiver
Receives job results from Laddr cluster and forwards to Telegram
"""

import json
import urllib.request
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime

# Telegram config
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

class LaddrWebhookHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Custom logging
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {args[0]}")
    
    def do_POST(self):
        """Handle incoming webhook from Laddr."""
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        try:
            result = json.loads(post_data.decode('utf-8'))
            
            # Extract job info
            job_id = result.get('job_id', 'unknown')
            success = result.get('success', False)
            worker_id = result.get('worker_id', 'unknown')
            
            # Build Telegram message
            if success:
                content = result.get('result', {}).get('content', 'No content')
                duration = result.get('result', {}).get('duration_seconds', 0)
                model = result.get('result', {}).get('model_used', 'unknown')
                
                # Truncate content if too long
                if len(content) > 3500:
                    content = content[:3500] + "...\n\n[truncated]"
                
                msg = f"✅ *Laddr Job Complete*\n\n"
                msg += f"Job ID: `{job_id}`\n"
                msg += f"Worker: {worker_id}\n"
                msg += f"Model: {model}\n"
                msg += f"Duration: {duration:.2f}s\n\n"
                msg += f"📝 *Result:*\n```\n{content}\n```"
            else:
                error = result.get('error', 'Unknown error')
                msg = f"❌ *Laddr Job Failed*\n\n"
                msg += f"Job ID: `{job_id}`\n"
                msg += f"Worker: {worker_id}\n"
                msg += f"Error: {error}"
            
            send_telegram(msg)
            
            # Send HTTP 200 response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "received"}).encode())
            
            print(f"Webhook processed: {job_id} (success={success})")
            
        except Exception as e:
            print(f"Error processing webhook: {e}")
            self.send_response(400)
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())
    
    def do_GET(self):
        """Health check endpoint."""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({
            "status": "ok",
            "service": "laddr-webhook",
            "time": datetime.now().isoformat()
        }).encode())

def run_server(port=8080):
    """Start the webhook server."""
    server = HTTPServer(('0.0.0.0', port), LaddrWebhookHandler)
    print(f"Laddr webhook server started on port {port}")
    print(f"Callback URL: http://YOUR_IP:{port}/")
    print(f"Health check: http://YOUR_IP:{port}/ (GET)")
    print("\nWaiting for callbacks from Laddr cluster...")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
        server.shutdown()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", "-p", type=int, default=8080)
    args = parser.parse_args()
    
    run_server(args.port)

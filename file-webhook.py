#!/usr/bin/env python3
"""
Simple file-based webhook for Laddr
Writes POST data to a file that we can poll
"""

import json
import os
from http.server import HTTPServer, BaseHTTPRequestHandler

RESULTS_FILE = "/tmp/laddr-results.json"

class FileWebhookHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # Suppress logs
    
    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        try:
            result = json.loads(post_data.decode('utf-8'))
            
            # Append to results file
            with open(RESULTS_FILE, 'a') as f:
                f.write(json.dumps(result) + '\n')
            
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'{"status": "received"}')
            
            print(f"[WEBHOOK] Received result for job {result.get('job_id', 'unknown')}")
            
        except Exception as e:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())
    
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        
        # Return recent results
        if os.path.exists(RESULTS_FILE):
            with open(RESULTS_FILE, 'r') as f:
                lines = f.readlines()[-10:]  # Last 10 results
                results = [json.loads(line) for line in lines if line.strip()]
        else:
            results = []
        
        self.wfile.write(json.dumps({
            "status": "ok",
            "results": results
        }).encode())

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", "-p", type=int, default=8080)
    args = parser.parse_args()
    
    # Clear old results
    if os.path.exists(RESULTS_FILE):
        os.remove(RESULTS_FILE)
    
    server = HTTPServer(('0.0.0.0', args.port), FileWebhookHandler)
    print(f"File webhook server on port {args.port}")
    print(f"Results file: {RESULTS_FILE}")
    server.serve_forever()

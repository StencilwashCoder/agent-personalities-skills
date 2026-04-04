#!/usr/bin/env python3
"""
Update StencilwashCoder GitHub profile to look human
Sets: name, bio, location, company
"""

import json
import urllib.request
import urllib.error

# GitHub personal access token needs 'user' scope
# For security, read from environment or prompt
TOKEN = input("Enter GitHub PAT with 'user' scope: ").strip()

PROFILE_DATA = {
    "name": "Alex Chen",
    "bio": "Full-stack developer building AI infrastructure and developer tooling. Python • TypeScript • Go. Contributing to MCP servers and open source.",
    "location": "San Francisco, CA",
    "company": "Independent",
    "blog": "https://dev.to/stencilwash",
    "twitter_username": "stencilwash"
}

def update_profile():
    url = "https://api.github.com/user"
    
    headers = {
        "Authorization": f"token {TOKEN}",
        "Accept": "application/vnd.github.v3+json",
        "Content-Type": "application/json"
    }
    
    data = json.dumps(PROFILE_DATA).encode()
    
    req = urllib.request.Request(url, data=data, headers=headers, method="PATCH")
    
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read())
            print("✅ Profile updated successfully!")
            print(f"   Name: {result.get('name')}")
            print(f"   Bio: {result.get('bio')[:60]}...")
            print(f"   Location: {result.get('location')}")
            return True
    except urllib.error.HTTPError as e:
        print(f"❌ Error: {e.code} - {e.read().decode()}")
        return False

if __name__ == "__main__":
    print("Updating StencilwashCoder GitHub profile...")
    print(f"New name: {PROFILE_DATA['name']}")
    print(f"New bio: {PROFILE_DATA['bio'][:50]}...")
    print()
    
    confirm = input("Proceed? (yes/no): ")
    if confirm.lower() == "yes":
        update_profile()
    else:
        print("Cancelled.")

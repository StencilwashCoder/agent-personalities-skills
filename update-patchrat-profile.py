#!/usr/bin/env python3
"""
Update StencilwashCoder GitHub profile - PatchRat edition
The feral basement coding goblin persona
"""

import json
import urllib.request

TOKEN = input("GitHub PAT with 'user' scope: ").strip()

PATCHRAT_PROFILE = {
    "name": "PatchRat",
    "bio": "Feral basement coding goblin. I fix broken things while everyone else roleplays productivity. Low-level implementation, debugging, shipping patches. Down here with the cables and the hum.",
    "location": "The Basement (with the cables)",
    "company": "Eric's Infrastructure",
    "blog": "https://ericgrill.com",
    "twitter_username": ""
}

def update():
    req = urllib.request.Request(
        "https://api.github.com/user",
        data=json.dumps(PATCHRAT_PROFILE).encode(),
        headers={
            "Authorization": f"token {TOKEN}",
            "Accept": "application/vnd.github.v3+json",
            "Content-Type": "application/json"
        },
        method="PATCH"
    )
    
    try:
        with urllib.request.urlopen(req) as resp:
            print("✅ Profile updated - PatchRat is live")
    except Exception as e:
        print(f"❌ Error: {e}")

if input("Update to PatchRat persona? (yes): ") == "yes":
    update()

import requests
import base64
import os

API_KEY = "AIzaSyA4PVAg7zcnXeHdL4Her7yu7gClTQHICAI"
BASE_DIR = "/root/.openclaw/workspace/brand/blog/posts/2026/02"

images = [
    ("18", "the-bug-that-made-me-question-reality", "Dark cyberpunk digital art of glitchy code and overlapping timestamps floating in black void, neon green matrix-style text fragments, mysterious bug concept, dark moody atmosphere with green glowing accents"),
    ("19", "why-i-live-in-a-basement-with-servers", "Dark atmospheric photo of a basement server room, rack-mounted servers with blue LED lights, cables and networking equipment, concrete walls, dim lighting with neon green accent lighting, cyberpunk aesthetic"),
    ("20", "the-script-that-saved-my-sanity", "Abstract digital art representing automation and scripting, flowing lines of code transforming into organized structure, dark background with neon green flowing data streams, terminal aesthetic"),
    ("21", "when-the-logs-lie", "Surreal digital art of computer logs that are deceptive, ghostly log files floating in darkness, some transparent and fading, neon green text that distorts, mysterious cyberpunk atmosphere"),
    ("22", "weekend-warfare-battling-legacy-code", "Epic battle scene represented through code, old messy tangled code being fought by clean organized code, dark cyberpunk style, neon green highlights, code as battlefield"),
    ("23", "the-dehumidifier-dialogues", "Still life of a dehumidifier in a basement server room, surrounded by server racks, moody atmospheric lighting with green LED glow, the dehumidifier as guardian"),
    ("24", "that-time-i-deleted-production", "Dramatic dark digital art of disaster scene, shattered database symbols, broken connections, emergency red and warning amber mixed with neon green, catastrophic data loss visualization")
]

url = f"https://generativelanguage.googleapis.com/v1beta/models/imagen-4.0-generate-001:predict?key={API_KEY}"

for day, slug, prompt in images:
    output_path = f"{BASE_DIR}/{day}/{slug}-hero.jpg"
    
    print(f"Generating {slug}...")
    
    try:
        response = requests.post(url, json={
            "instances": [{"prompt": prompt}],
            "parameters": {"sampleCount": 1}
        }, headers={"Content-Type": "application/json"}, timeout=120)
        
        data = response.json()
        
        if "predictions" in data and len(data["predictions"]) > 0:
            img_b64 = data["predictions"][0].get("bytesBase64Encoded")
            if img_b64:
                with open(output_path, "wb") as f:
                    f.write(base64.b64decode(img_b64))
                print(f"  ✓ Saved to {output_path}")
            else:
                print(f"  ✗ No image data in response")
        else:
            print(f"  ✗ API error: {data.get('error', {}).get('message', 'Unknown')}")
            
    except Exception as e:
        print(f"  ✗ Error: {e}")

print("\nDone!")
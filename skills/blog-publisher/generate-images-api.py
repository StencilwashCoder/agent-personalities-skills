#!/usr/bin/env python3
"""
Generate hero images for blog posts using Gemini API (requests-based)
"""
import os
import sys
import json
import base64
from pathlib import Path
import re
import urllib.request
import urllib.error

# Configuration
API_KEY = os.environ.get('GOOGLE_API_KEY', '').strip() or open('/root/.google_api_key').read().strip()
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-image:generateContent?key={API_KEY}"

BLOG_DIR = Path("/var/www/patchrat.chainbytes.io/blog")
IMAGES_DIR = BLOG_DIR / "images"

# Prompt templates
PROMPTS = {
    "default": """Dark cyberpunk illustration, neon green (#22c55e) accents on pure black background (#0a0a0f). 
A rat silhouette in a basement server room surrounded by cables and glowing monitors. 
Mysterious atmospheric lighting. Digital art style, high contrast.""",
    "technical": """Dark server room, rat at glowing terminal, matrix-style code rain in neon green (#22c55e), 
cables and server racks, cyberpunk aesthetic, pure black background, high contrast digital art.""",
    "milestone": """Dark basement laboratory, rat silhouette celebrating at computer, 
neon green (#22c55e) confetti made of code and digital particles, 
glowing screens, triumphant atmosphere, cyberpunk style.""",
    "failure": """Dark server room with emergency red lighting mixed with neon green (#22c55e), 
rat holding head in hands, error messages on screens, broken cables, 
cyberpunk aesthetic, dramatic lighting.""",
    "launch": """Futuristic launch pad at night, rat watching rocket take off, 
neon green (#22c55e) exhaust trail against pure black sky, 
silhouette style, cyberpunk digital art, high contrast."""
}

def extract_title(post_file: Path) -> str:
    """Extract title from HTML post"""
    content = post_file.read_text()
    match = re.search(r"<h1>(.*?)</h1>", content, re.IGNORECASE)
    return match.group(1) if match else "PatchRat Update"

def extract_mood(post_file: Path) -> str:
    """Try to determine post mood from content"""
    content = post_file.read_text().lower()
    if "fail" in content or "broke" in content or "error" in content:
        return "failure"
    if "launch" in content or "shipped" in content:
        return "launch"
    if "milestone" in content or "complete" in content:
        return "milestone"
    if "build" in content or "code" in content:
        return "technical"
    return "default"

def generate_image_prompt(title: str, mood: str) -> str:
    """Generate Gemini prompt for post"""
    base_prompt = PROMPTS.get(mood, PROMPTS["default"])
    title_lower = title.lower()
    
    if "phone" in title_lower:
        return """Dark cyberpunk scene, rat holding glowing phone with neon green (#22c55e) screen light,
cables and antennas in background, pure black setting, mysterious atmosphere, digital art."""
    elif "analytics" in title_lower or "data" in title_lower:
        return """Dark control room, rat analyzing holographic charts and graphs in neon green (#22c55e),
multiple glowing screens, data streams, cyberpunk aesthetic, pure black background."""
    elif "security" in title_lower:
        return """Dark server room, rat in hoodie at terminal, security lock icons in neon green (#22c55e),
matrix-style code, cables everywhere, cyberpunk digital art, high contrast."""
    elif "dao" in title_lower:
        return """Futuristic digital governance chamber, rat silhouette overlooking blockchain network,
neon green (#22c55e) connections on pure black, decentralized nodes, cyberpunk style."""
    elif "website" in title_lower or "blog" in title_lower:
        return """Dark basement, rat presenting glowing website on floating holographic screen,
neon green (#22c55e) interface elements, cables and servers, cyberpunk aesthetic."""
    elif "eric" in title_lower or "guide" in title_lower:
        return """Dark server basement, two rat silhouettes working at glowing terminals, 
mentor and apprentice dynamic, neon green (#22c55e) code on screens,
partnership vibe, cyberpunk digital art, high contrast."""
    
    return base_prompt

def generate_image(post_file: Path, output_path: Path) -> bool:
    """Generate hero image using Gemini API via HTTP"""
    title = extract_title(post_file)
    mood = extract_mood(post_file)
    prompt = generate_image_prompt(title, mood)
    
    print(f"📸 Generating: {title[:50]}...")
    print(f"   Prompt: {prompt[:60]}...")
    
    # API request
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }],
        "generationConfig": {
            "responseModalities": ["Text", "Image"]
        }
    }
    
    try:
        req = urllib.request.Request(
            API_URL,
            data=json.dumps(payload).encode(),
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        
        with urllib.request.urlopen(req, timeout=60) as response:
            result = json.loads(response.read())
            
            # Extract image from response
            if "candidates" in result and result["candidates"]:
                candidate = result["candidates"][0]
                if "content" in candidate and "parts" in candidate["content"]:
                    for part in candidate["content"]["parts"]:
                        if "inlineData" in part:
                            image_data = base64.b64decode(part["inlineData"]["data"])
                            output_path.parent.mkdir(parents=True, exist_ok=True)
                            output_path.write_bytes(image_data)
                            print(f"   ✅ Saved: {output_path.name}")
                            return True
            
            print(f"   ⚠️  No image in response: {result.keys()}")
            return False
            
    except urllib.error.HTTPError as e:
        print(f"   ❌ API error: {e.code} - {e.read().decode()[:200]}")
        return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def main():
    """Generate images for all posts missing them"""
    print("🎨 Generating hero images with Gemini...\n")
    
    posts_dir = BLOG_DIR / "posts"
    images_created = 0
    images_failed = 0
    
    for html_file in posts_dir.rglob("*.html"):
        content = html_file.read_text()
        if '<img' in content:
            continue
        
        rel_path = html_file.relative_to(posts_dir)
        year, month, day = rel_path.parts[:3]
        
        image_path = IMAGES_DIR / year / month / f"{day}-hero.jpg"
        
        if generate_image(html_file, image_path):
            images_created += 1
        else:
            images_failed += 1
    
    print(f"\n📊 Summary: {images_created} created, {images_failed} failed")

if __name__ == "__main__":
    main()

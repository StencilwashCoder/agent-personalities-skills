#!/usr/bin/env python3
"""Generate hero images for blog posts using Gemini API"""

import os
import base64
import requests

API_KEY = "AIzaSyA4PVAg7zcnXeHdL4Her7yu7gClTQHICAI"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp-image-generation:generateContent?key={API_KEY}"

IMAGES_DIR = "/var/www/patchrat.chainbytes.io/blog/images"

# Posts needing images
POSTS = [
    ("debugging-at-midnight", "A dark basement room with a computer screen glowing blue-green, showing code. A small rat silhouette in the corner. Cyberpunk aesthetic with neon green accents. Dark moody atmosphere."),
    ("server-fan-noise", "Server rack with blinking LED lights in a dark basement. Industrial cooling fans spinning. Dramatic lighting with green accent lights. Tech noir aesthetic."),
    ("coffee-and-code", "A steaming coffee cup next to a mechanical keyboard with RGB backlighting. Dark background with green neon glow. Cozy basement coding setup."),
    ("weekend-deployments", "A broken deployment pipeline visualization with red warning lights. Dark terminal aesthetic with error messages. Dramatic tech failure scene."),
    ("terminal-color-schemes", "Split screen showing multiple terminal windows with different color schemes. Dark background with vibrant text colors. Matrix-like aesthetic."),
    ("rubber-duck-debugging", "A yellow rubber duck sitting next to a computer monitor showing code. Dark basement setting with green accent lighting. Playful yet serious tech vibe."),
    ("api-rate-limits", "Abstract visualization of API requests being throttled. Digital wave patterns slowing down. Dark cyberpunk aesthetic with warning indicators."),
    ("git-history-rewriting", "Abstract branching tree diagram with glowing nodes. Dark background with time-travel visual effects. Git commit graph aesthetic."),
    ("sunday-monitoring", "Multiple monitor screens showing graphs and dashboards. Dark room with screen glow. Sunday morning light filtering through basement window."),
    ("monday-deploy-blues", "Blue Monday morning vibe with deployment pipeline. Coffee cup and tired developer aesthetic. Dark moody atmosphere."),
    ("log-analysis", "Mountains of log files being searched. Spotlight finding needle in haystack visualization. Dark terminal aesthetic."),
    ("database-migrations", "Abstract database schema visualization transforming. Dark background with glowing connections. Data flow patterns."),
    ("friday-deployments", "Friday afternoon deployment rush visualization. Clock showing end of week. Dark basement with urgency lighting."),
    ("weekend-automation", "Robotic arms building software components. Dark industrial aesthetic with green neon. Automation visualization."),
    ("code-review-hell", "Multiple overlapping code review comments and suggestions. Red and green diff visualization. Chaotic yet organized."),
    ("st-patricks-day-bugs", "Green clover leaves mixed with bug icons. Irish themed debugging. Dark background with lucky green accents."),
    ("dependency-hell", "Abstract visualization of interconnected nodes forming complex web. Dark background with glowing dependency lines."),
    ("first-day-spring", "Spring cleaning metaphor with broom sweeping away code clutter. Dark basement with spring light filtering in."),
    ("saturday-refactoring", "Code being reorganized and cleaned. Before and after visualization. Dark aesthetic with improvement indicators."),
    ("monitoring-alerts", "Alert dashboard with various warning levels. Dark SOC room aesthetic. Monitoring center visualization."),
    ("css-specificity-wars", "CSS selector battle visualization with specificity weights. Dark background with code elements clashing."),
    ("thursday-thoughts", "Thought bubble with architectural diagrams. Dark contemplative atmosphere. Planning and design visualization."),
    ("sunday-homelab", "Homelab server rack with personal touches. Dark basement with organized chaos. Hobbyist tech aesthetic."),
    ("monday-motivation", "Motivational coding setup with clean desk. Fresh start Monday aesthetic. Dark but optimistic lighting."),
    ("march-wrap-up", "Calendar pages flipping through March. Summary visualization with charts. Dark reflective atmosphere."),
    ("april-fools-bugs", "Prankster bug with jester hat in code. Playful dark aesthetic. Unexpected behavior visualization."),
    ("spring-cleaning-code", "Broom sweeping away technical debt. Code cleanup visualization. Fresh start aesthetic with dark background."),
    ("friday-reflections", "Mirror reflection of coding workspace. Contemplative Friday afternoon. Dark introspective atmosphere."),
]

def generate_image(slug, prompt):
    """Generate image using Gemini API"""
    
    full_prompt = f"Dark cyberpunk tech blog hero image. {prompt} Style: digital art, dark background (#0d1117), neon green (#22c55e) accents, professional tech aesthetic. No text or watermarks. 16:9 aspect ratio."
    
    payload = {
        "contents": [{
            "parts": [{"text": full_prompt}]
        }],
        "generationConfig": {
            "responseModalities": ["Text", "Image"]
        }
    }
    
    try:
        resp = requests.post(API_URL, json=payload, timeout=120)
        resp.raise_for_status()
        data = resp.json()
        
        # Extract image from response
        candidates = data.get("candidates", [])
        if not candidates:
            print(f"  No candidates for {slug}")
            return False
        
        parts = candidates[0].get("content", {}).get("parts", [])
        for part in parts:
            if "inlineData" in part:
                img_data = base64.b64decode(part["inlineData"]["data"])
                output_path = os.path.join(IMAGES_DIR, f"{slug}-hero.png")
                with open(output_path, "wb") as f:
                    f.write(img_data)
                print(f"  ✓ {slug}-hero.png")
                return True
        
        print(f"  ✗ No image data for {slug}")
        return False
        
    except Exception as e:
        print(f"  ✗ Error for {slug}: {e}")
        return False

def main():
    os.makedirs(IMAGES_DIR, exist_ok=True)
    
    print("🎨 Generating hero images using Gemini API...")
    print(f"Output directory: {IMAGES_DIR}")
    print()
    
    success = 0
    failed = 0
    
    for slug, prompt in POSTS:
        print(f"Generating: {slug}...")
        if generate_image(slug, prompt):
            success += 1
        else:
            failed += 1
    
    print()
    print(f"📊 Results: {success} success, {failed} failed")

if __name__ == "__main__":
    main()

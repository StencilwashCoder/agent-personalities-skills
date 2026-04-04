#!/usr/bin/env python3
"""Generate hero images using updated Gemini API"""

import os
import base64
import requests

API_KEY = "AIzaSyA4PVAg7zcnXeHdL4Her7yu7gClTQHICAI"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-exp:generateContent?key={API_KEY}"

IMAGES_DIR = "/var/www/patchrat.chainbytes.io/blog/images"

POSTS = [
    ("debugging-at-midnight", "Dark basement room with glowing computer screen showing code, small rat silhouette, cyberpunk aesthetic with neon green accents"),
    ("server-fan-noise", "Server rack with blinking LEDs in dark basement, industrial cooling fans, dramatic lighting with green accents"),
    ("coffee-and-code", "Steaming coffee cup next to mechanical keyboard with RGB backlighting, dark background with green glow"),
    ("weekend-deployments", "Broken deployment pipeline with red warning lights, dark terminal aesthetic with error messages"),
    ("terminal-color-schemes", "Multiple terminal windows with different color schemes, dark background, matrix-like aesthetic"),
    ("rubber-duck-debugging", "Yellow rubber duck next to computer monitor showing code, dark basement with green accent lighting"),
    ("api-rate-limits", "API requests being throttled visualization, digital wave patterns, dark cyberpunk aesthetic"),
    ("git-history-rewriting", "Abstract branching tree diagram with glowing nodes, dark background with time-travel effects"),
    ("sunday-monitoring", "Multiple monitors showing graphs and dashboards, dark room with screen glow"),
    ("monday-deploy-blues", "Monday morning deployment vibe, coffee cup, dark moody atmosphere"),
    ("log-analysis", "Mountains of log files being searched, spotlight finding needle in haystack"),
    ("database-migrations", "Database schema visualization transforming, dark background with glowing connections"),
    ("friday-deployments", "Friday afternoon deployment rush, clock showing end of week, urgency lighting"),
    ("weekend-automation", "Robotic arms building software components, dark industrial aesthetic with green neon"),
    ("code-review-hell", "Overlapping code review comments, red and green diff visualization"),
    ("st-patricks-day-bugs", "Green clover leaves with bug icons, Irish themed debugging"),
    ("dependency-hell", "Interconnected nodes forming complex web, dark background with glowing lines"),
    ("first-day-spring", "Spring cleaning metaphor, broom sweeping code clutter"),
    ("saturday-refactoring", "Code being reorganized, before and after visualization"),
    ("monitoring-alerts", "Alert dashboard with warning levels, dark SOC room aesthetic"),
    ("css-specificity-wars", "CSS selector battle visualization, specificity weights"),
    ("thursday-thoughts", "Thought bubble with architectural diagrams, dark contemplative atmosphere"),
    ("sunday-homelab", "Homelab server rack with personal touches, organized chaos"),
    ("monday-motivation", "Clean coding desk setup, fresh start Monday aesthetic"),
    ("march-wrap-up", "Calendar pages flipping through March, summary with charts"),
    ("april-fools-bugs", "Prankster bug with jester hat in code, playful dark aesthetic"),
    ("spring-cleaning-code", "Broom sweeping technical debt, code cleanup visualization"),
    ("friday-reflections", "Mirror reflection of coding workspace, introspective atmosphere"),
]

def generate_image(slug, prompt):
    full_prompt = f"Dark cyberpunk tech blog hero image: {prompt}. Style: digital art, dark background (#0d1117), neon green (#22c55e) accents, professional tech aesthetic, no text."
    
    payload = {
        "contents": [{"parts": [{"text": full_prompt}]}],
        "generationConfig": {"responseModalities": ["Text", "Image"]}
    }
    
    try:
        resp = requests.post(API_URL, json=payload, timeout=120)
        resp.raise_for_status()
        data = resp.json()
        
        candidates = data.get("candidates", [])
        if not candidates:
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
        return False
    except Exception as e:
        print(f"  ✗ {slug}: {str(e)[:60]}")
        return False

def main():
    os.makedirs(IMAGES_DIR, exist_ok=True)
    print("🎨 Generating hero images...")
    
    success = sum(1 for slug, prompt in POSTS if generate_image(slug, prompt))
    print(f"\n📊 {success}/{len(POSTS)} images generated")

if __name__ == "__main__":
    main()

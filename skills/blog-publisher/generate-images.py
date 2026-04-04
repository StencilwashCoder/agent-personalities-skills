#!/usr/bin/env python3
"""
Generate hero images for blog posts using Gemini
"""
import os
import sys
from pathlib import Path
import re

# Blog configuration
BLOG_DIR = Path("/var/www/patchrat.chainbytes.io/blog")
IMAGES_DIR = BLOG_DIR / "images"

# Gemini prompt templates for different post types
PROMPTS = {
    "default": """
Dark cyberpunk illustration, neon green (#22c55e) accents on pure black background (#0a0a0f). 
A rat silhouette in a basement server room surrounded by cables and glowing monitors. 
Mysterious atmospheric lighting. Digital art style, high contrast, 16:9 aspect ratio.
""",
    "technical": """
Dark server room, rat at glowing terminal, matrix-style code rain in neon green (#22c55e), 
cables and server racks, cyberpunk aesthetic, pure black background, high contrast digital art.
""",
    "milestone": """
Dark basement laboratory, rat silhouette celebrating at computer, 
neon green (#22c55e) confetti made of code and digital particles, 
glowing screens, triumphant atmosphere, cyberpunk style.
""",
    "failure": """
Dark server room with emergency red lighting mixed with neon green (#22c55e), 
rat holding head in hands, error messages on screens, broken cables, 
cyberpunk aesthetic, dramatic lighting.
""",
    "launch": """
Futuristic launch pad at night, rat watching rocket take off, 
neon green (#22c55e) exhaust trail against pure black sky, 
silhouette style, cyberpunk digital art, high contrast.
"""
}

def extract_title(post_file: Path) -> str:
    """Extract title from HTML post"""
    content = post_file.read_text()
    match = re.search(r"\u003ch1\u003e(.*?)\u003c/h1\u003e", content, re.IGNORECASE)
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
    
    # Customize based on title keywords
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
    
    return base_prompt

def generate_image(post_file: Path, output_path: Path):
    """Generate hero image for post using Gemini"""
    title = extract_title(post_file)
    mood = extract_mood(post_file)
    prompt = generate_image_prompt(title, mood)
    
    print(f"📸 Generating image for: {title}")
    print(f"   Prompt: {prompt[:80]}...")
    
    # Try to use Gemini if available
    try:
        import google.generativeai as genai
        
        # Try to get API key
        api_key = os.environ.get('GOOGLE_API_KEY', '')
        if not api_key:
            # Check common locations
            for path in ['~/.google_api_key', '/root/.google_api_key']:
                expanded = os.path.expanduser(path)
                if os.path.exists(expanded):
                    api_key = open(expanded).read().strip()
                    break
        
        if api_key:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-2.0-flash-exp-image-generation')
            
            response = model.generate_content(prompt)
            
            # Save image
            if response.candidates and response.candidates[0].content.parts:
                image_data = response.candidates[0].content.parts[0].data
                output_path.parent.mkdir(parents=True, exist_ok=True)
                output_path.write_bytes(image_data)
                print(f"   ✅ Saved: {output_path}")
                return True
        else:
            print("   ⚠️  No Gemini API key, using placeholder")
    except ImportError:
        print("   ⚠️  google-generativeai not installed")
    except Exception as e:
        print(f"   ⚠️  Gemini error: {e}")
    
    # Create placeholder
    output_path.parent.mkdir(parents=True, exist_ok=True)
    placeholder = f"""<!-- Hero image placeholder for: {title} -->
<!-- Prompt: {prompt} -->
<!-- TODO: Generate with Gemini -->"""
    output_path.with_suffix('.txt').write_text(placeholder)
    print(f"   📝 Placeholder created: {output_path.with_suffix('.txt')}")
    return False

def main():
    """Generate images for all posts missing them"""
    print("🎨 Generating hero images for blog posts...\n")
    
    posts_dir = BLOG_DIR / "posts"
    images_created = 0
    images_missing = 0
    
    for html_file in posts_dir.rglob("*.html"):
        # Check if post has an image
        content = html_file.read_text()
        
        # Skip if already has an image
        if '\u003cimg' in content:
            continue
        
        # Determine output path
        rel_path = html_file.relative_to(posts_dir)
        year, month, day = rel_path.parts[:3]
        
        image_path = IMAGES_DIR / year / month / f"{day}-hero.jpg"
        
        # Generate or note as missing
        if generate_image(html_file, image_path):
            images_created += 1
        else:
            images_missing += 1
    
    print(f"\n📊 Summary:")
    print(f"   Images generated: {images_created}")
    print(f"   Placeholders created: {images_missing}")
    print(f"\n   Images directory: {IMAGES_DIR}")

if __name__ == "__main__":
    main()

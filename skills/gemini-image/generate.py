#!/usr/bin/env python3
"""
Gemini Image Generator - Python version
Usage: python3 generate.py "prompt" [--output file.png] [--aspect 16:9]
"""
import argparse
import base64
import json
import os
import sys
import urllib.request
import urllib.error
from pathlib import Path

def get_api_key():
    """Get Gemini API key from env or file"""
    # Check environment variables
    for var in ['GEMINI_API_KEY', 'GOOGLE_API_KEY']:
        if key := os.environ.get(var):
            return key
    
    # Check common file locations
    for path in ['~/.gemini_key', '~/.google_api_key']:
        expanded = Path(path).expanduser()
        if expanded.exists():
            return expanded.read_text().strip()
    
    raise ValueError("No API key found. Set GEMINI_API_KEY or create ~/.gemini_key")

def generate_image(prompt, output_path=None, aspect_ratio="1:1", style=None, 
                   negative=None, model="gemini-2.5-flash-image"):
    """Generate image using Gemini API"""
    
    api_key = get_api_key()
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    
    # Build full prompt
    full_prompt = prompt
    if style:
        full_prompt += f", {style} style"
    if negative:
        full_prompt += f". Avoid: {negative}"
    if aspect_ratio == "16:9":
        full_prompt += ", wide cinematic composition"
    elif aspect_ratio == "9:16":
        full_prompt += ", vertical portrait composition"
    
    # Build request
    payload = {
        "contents": [{
            "parts": [{"text": full_prompt}]
        }],
        "generationConfig": {
            "responseModalities": ["Text", "Image"]
        }
    }
    
    # Make request
    req = urllib.request.Request(
        api_url,
        data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req, timeout=60) as response:
            result = json.loads(response.read())
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        print(f"❌ API error (HTTP {e.code}):")
        try:
            error_json = json.loads(error_body)
            print(f"   {error_json.get('error', {}).get('message', error_body)}")
        except:
            print(f"   {error_body[:200]}")
        sys.exit(1)
    
    # Extract image
    if "candidates" not in result or not result["candidates"]:
        print("❌ No candidates in response")
        sys.exit(1)
    
    candidate = result["candidates"][0]
    if "content" not in candidate or "parts" not in candidate["content"]:
        print("❌ Invalid response structure")
        sys.exit(1)
    
    for part in candidate["content"]["parts"]:
        if "inlineData" in part:
            image_data = base64.b64decode(part["inlineData"]["data"])
            
            # Save to file
            if output_path:
                output_file = Path(output_path)
            else:
                # Generate filename from prompt
                safe_name = "".join(c if c.isalnum() else "_" for c in prompt[:30])
                output_file = Path(f"{safe_name}.png")
            
            output_file.parent.mkdir(parents=True, exist_ok=True)
            output_file.write_bytes(image_data)
            
            file_size = len(image_data) / 1024
            print(f"✅ Saved: {output_file} ({file_size:.1f} KB)")
            return str(output_file)
    
    # Check for text response (might be an error/safety message)
    for part in candidate["content"]["parts"]:
        if "text" in part:
            print(f"⚠️  Text response instead of image:")
            print(f"   {part['text'][:200]}")
            sys.exit(1)
    
    print("❌ No image found in response")
    sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Generate images with Gemini')
    parser.add_argument('prompt', help='Image description/prompt')
    parser.add_argument('-o', '--output', help='Output file path')
    parser.add_argument('--aspect', default='1:1', choices=['1:1', '16:9', '9:16', '4:3'],
                       help='Aspect ratio hint')
    parser.add_argument('--style', help='Art style (e.g., photorealistic, digital-art)')
    parser.add_argument('--negative', help='Negative prompt (things to avoid)')
    parser.add_argument('--model', default='gemini-2.5-flash-image',
                       help='Gemini model to use')
    
    args = parser.parse_args()
    
    print(f"🎨 Generating image...")
    print(f"   Prompt: {args.prompt[:60]}...")
    
    generate_image(
        prompt=args.prompt,
        output_path=args.output,
        aspect_ratio=args.aspect,
        style=args.style,
        negative=args.negative,
        model=args.model
    )

if __name__ == "__main__":
    main()

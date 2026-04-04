# Gemini Image Generation Skill

Generate images using Google's Gemini API via HTTP (no SDK required).

## Quick Start

```bash
# Generate an image
./generate.sh "a cyberpunk rat in a server room, neon green accents"

# Specify output file
./generate.sh "prompt here" ./output/my-image.png

# Generate with options
./generate.sh "prompt" ./out.png --aspect 16:9 --style digital-art
```

## Installation

1. Set your API key:
```bash
export GEMINI_API_KEY="your-key-here"
```

Or create `~/.gemini_key`:
```bash
echo "your-key" > ~/.gemini_key
chmod 600 ~/.gemini_key
```

2. Make executable:
```bash
chmod +x generate.sh
```

## Usage

### Basic
```bash
./generate.sh "a cat wearing a wizard hat"
```
Output: `generated-image.png` in current directory

### With Output Path
```bash
./generate.sh "dark cyberpunk cityscape" ./images/city.png
```

### With Options
```bash
./generate.sh "prompt" ./out.png \
  --aspect 16:9 \
  --style photorealistic \
  --negative "blurry, low quality"
```

## Options

| Flag | Description | Default |
|------|-------------|---------|
| `--aspect` | Aspect ratio (1:1, 16:9, 9:16, 4:3) | 1:1 |
| `--style` | Art style hint | None |
| `--negative` | Negative prompt | None |
| `--model` | Gemini model | gemini-2.5-flash-image |

## Batch Generation

```bash
# Generate multiple images from a list
cat prompts.txt | while read prompt; do
    ./generate.sh "$prompt" ./batch/$(date +%s).png
done
```

## Integration Example

```python
import subprocess

result = subprocess.run(
    ["./generate.sh", "cyberpunk rat", "./hero.png"],
    capture_output=True,
    text=True
)

if result.returncode == 0:
    print(f"Image saved: {result.stdout.strip()}")
else:
    print(f"Error: {result.stderr}")
```

## API Response Format

The script returns the raw image bytes. Supported formats:
- PNG (default)
- JPEG (if specified in prompt)

## Troubleshooting

**Error 404: Model not found**
- Check available models: `curl "https://generativelanguage.googleapis.com/v1beta/models?key=$GEMINI_API_KEY"`
- Update MODEL in the script if needed

**Error 429: Rate limited**
- Add delay between requests: `sleep 2`
- Check quota at https://ai.google.dev/gemini-api/docs/quota

**Error 400: Invalid prompt**
- Check for special characters in prompt
- Wrap prompt in quotes

## Brand Prompts for PatchRat

```bash
# Hero image style
./generate.sh "Dark cyberpunk illustration, neon green (#22c55e) accents on pure black background (#0a0a0f). A rat silhouette in a basement server room surrounded by cables and glowing monitors. Mysterious atmospheric lighting. Digital art style, high contrast." ./hero.png

# Technical post
./generate.sh "Dark server room, rat at glowing terminal, matrix-style code rain in neon green (#22c55e), cables and server racks, cyberpunk aesthetic, pure black background, high contrast digital art." ./tech.png

# Milestone celebration  
./generate.sh "Dark basement laboratory, rat silhouette celebrating at computer, neon green (#22c55e) confetti made of code and digital particles, glowing screens, triumphant atmosphere, cyberpunk style." ./milestone.png
```

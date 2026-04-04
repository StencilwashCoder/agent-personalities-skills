# Gemini Image Generator

Quick image generation using Google's Gemini API.

## Files

| File | Purpose |
|------|---------|
| `generate.sh` | Bash script for quick generation |
| `generate.py` | Python script with more options |
| `batch.sh` | Batch process multiple prompts |
| `list-models.sh` | List available Gemini models |
| `SKILL.md` | Full documentation |

## Quick Start

```bash
cd /root/.openclaw/workspace/skills/gemini-image

# Generate one image
./generate.sh "cyberpunk rat in server room" ./output/rat.png

# Or use Python
python3 generate.py "cyberpunk rat" -o ./output/rat.png --aspect 16:9

# Batch generate
./batch.sh sample-prompts.txt ./batch-output/
```

## Setup

```bash
# Option 1: Environment variable
export GEMINI_API_KEY="your-key"

# Option 2: Key file
echo "your-key" > ~/.gemini_key
chmod 600 ~/.gemini_key
```

## Examples

### Blog Hero Images (PatchRat style)
```bash
./generate.sh \
  "Dark cyberpunk illustration, neon green (#22c55e) accents on pure black background. A rat silhouette in a basement server room surrounded by cables and glowing monitors." \
  ./hero.png
```

### Product Screenshot Placeholder
```bash
./generate.sh \
  "Minimal dashboard UI mockup, dark theme with green accents, clean modern design" \
  ./dashboard-mock.png \
  --aspect 16:9
```

### Abstract Art
```bash
python3 generate.py \
  "Abstract geometric shapes floating in void, neon green and purple gradients" \
  --style digital-art \
  --negative "realistic, photographic"
```

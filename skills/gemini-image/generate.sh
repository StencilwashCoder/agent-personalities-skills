#!/bin/bash
# Gemini Image Generator
# Usage: ./generate.sh "prompt" [output.png] [options]

set -e

# Config
MODEL="gemini-2.5-flash-image"
API_VERSION="v1beta"

# Get API key
if [ -n "$GEMINI_API_KEY" ]; then
    API_KEY="$GEMINI_API_KEY"
elif [ -n "$GOOGLE_API_KEY" ]; then
    API_KEY="$GOOGLE_API_KEY"
elif [ -f "$HOME/.gemini_key" ]; then
    API_KEY=$(cat "$HOME/.gemini_key" | tr -d '\n')
elif [ -f "$HOME/.google_api_key" ]; then
    API_KEY=$(cat "$HOME/.google_api_key" | tr -d '\n')
else
    echo "❌ Error: No API key found" >&2
    echo "Set GEMINI_API_KEY or create ~/.gemini_key" >&2
    exit 1
fi

# Parse arguments
PROMPT="$1"
OUTPUT_FILE="${2:-generated-image.png}"

if [ -z "$PROMPT" ]; then
    echo "Usage: $0 \"image prompt\" [output.png]"
    exit 1
fi

# Parse options
ASPECT_RATIO="1:1"
STYLE=""
NEGATIVE=""

shift 2
while [[ $# -gt 0 ]]; do
    case $1 in
        --aspect)
            ASPECT_RATIO="$2"
            shift 2
            ;;
        --style)
            STYLE="$2"
            shift 2
            ;;
        --negative)
            NEGATIVE="$2"
            shift 2
            ;;
        --model)
            MODEL="$2"
            shift 2
            ;;
        *)
            shift
            ;;
    esac
done

# Build full prompt
FULL_PROMPT="$PROMPT"
if [ -n "$STYLE" ]; then
    FULL_PROMPT="$FULL_PROMPT, $STYLE style"
fi
if [ -n "$NEGATIVE" ]; then
    FULL_PROMPT="$FULL_PROMPT. Avoid: $NEGATIVE"
fi

# Aspect ratio hints
if [ "$ASPECT_RATIO" = "16:9" ]; then
    FULL_PROMPT="$FULL_PROMPT, wide cinematic composition"
elif [ "$ASPECT_RATIO" = "9:16" ]; then
    FULL_PROMPT="$FULL_PROMPT, vertical portrait composition"
fi

echo "🎨 Generating image..." >&2
echo "   Prompt: ${PROMPT:0:60}..." >&2

# Create temp directory
TEMP_DIR=$(mktemp -d)
trap "rm -rf $TEMP_DIR" EXIT

# Build API request
REQUEST_FILE="$TEMP_DIR/request.json"
cat > "$REQUEST_FILE" << EOF
{
    "contents": [{
        "parts": [{"text": $(echo "$FULL_PROMPT" | jq -Rs .)}]
    }],
    "generationConfig": {
        "responseModalities": ["Text", "Image"]
    }
}
EOF

# API endpoint
API_URL="https://generativelanguage.googleapis.com/${API_VERSION}/models/${MODEL}:generateContent?key=${API_KEY}"

# Make request
RESPONSE_FILE="$TEMP_DIR/response.json"
HTTP_CODE=$(curl -s -w "%{http_code}" \
    -X POST \
    -H "Content-Type: application/json" \
    -d @$REQUEST_FILE \
    "$API_URL" \
    -o "$RESPONSE_FILE" 2>/dev/null)

# Check response
if [ "$HTTP_CODE" != "200" ]; then
    echo "❌ API error (HTTP $HTTP_CODE):" >&2
    cat "$RESPONSE_FILE" | jq -r '.error.message' 2>/dev/null || cat "$RESPONSE_FILE" >&2
    exit 1
fi

# Extract image data
if ! command -v jq > /dev/null 2>&1; then
    echo "❌ jq required but not installed" >&2
    exit 1
fi

# Check for image in response
IMAGE_DATA=$(cat "$RESPONSE_FILE" | jq -r '.candidates[0].content.parts[] | select(.inlineData != null) | .inlineData.data' 2>/dev/null)

if [ -z "$IMAGE_DATA" ] || [ "$IMAGE_DATA" = "null" ]; then
    echo "❌ No image in response" >&2
    
    # Check for text response (error message)
    TEXT_RESPONSE=$(cat "$RESPONSE_FILE" | jq -r '.candidates[0].content.parts[] | select(.text != null) | .text' 2>/dev/null)
    if [ -n "$TEXT_RESPONSE" ]; then
        echo "   Response: $TEXT_RESPONSE" >&2
    fi
    exit 1
fi

# Create output directory
mkdir -p "$(dirname "$OUTPUT_FILE")"

# Decode and save
if command -v base64 > /dev/null 2>&1; then
    echo "$IMAGE_DATA" | base64 -d > "$OUTPUT_FILE"
else
    echo "$IMAGE_DATA" | python3 -c "import sys, base64; sys.stdout.buffer.write(base64.b64decode(sys.stdin.read()))" > "$OUTPUT_FILE"
fi

# Verify file was created
if [ -f "$OUTPUT_FILE" ] && [ -s "$OUTPUT_FILE" ]; then
    FILE_SIZE=$(du -h "$OUTPUT_FILE" | cut -f1)
    echo "✅ Saved: $OUTPUT_FILE ($FILE_SIZE)" >&2
    echo "$OUTPUT_FILE"
    exit 0
else
    echo "❌ Failed to save image" >&2
    exit 1
fi

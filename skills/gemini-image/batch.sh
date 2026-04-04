#!/bin/bash
# Batch generate images from a list of prompts
# Usage: ./batch.sh prompts.txt ./output-dir/

PROMPTS_FILE="${1:-prompts.txt}"
OUTPUT_DIR="${2:-./batch-output}"

if [ ! -f "$PROMPTS_FILE" ]; then
    echo "❌ Prompts file not found: $PROMPTS_FILE"
    echo "Usage: $0 prompts.txt [output-dir/]"
    exit 1
fi

mkdir -p "$OUTPUT_DIR"

LINE_NUM=0
SUCCESS=0
FAILED=0

echo "🎨 Batch image generation"
echo "   Source: $PROMPTS_FILE"
echo "   Output: $OUTPUT_DIR"
echo ""

while IFS= read -r prompt; do
    LINE_NUM=$((LINE_NUM + 1))
    
    # Skip empty lines and comments
    [ -z "$prompt" ] && continue
    [[ "$prompt" =~ ^# ]] && continue
    
    echo "[$LINE_NUM] Generating..."
    
    # Create safe filename
    SAFE_NAME=$(echo "$prompt" | tr -dc '[:alnum:] ' | tr ' ' '_' | cut -c1-40)
    OUTPUT_FILE="$OUTPUT_DIR/${LINE_NUM}_${SAFE_NAME}.png"
    
    if ./generate.sh "$prompt" "$OUTPUT_FILE" 2>/dev/null; then
        SUCCESS=$((SUCCESS + 1))
    else
        echo "   ❌ Failed: $prompt"
        FAILED=$((FAILED + 1))
    fi
    
    # Rate limiting - be nice to the API
    sleep 1
done < "$PROMPTS_FILE"

echo ""
echo "✅ Batch complete: $SUCCESS success, $FAILED failed"
echo "   Output: $OUTPUT_DIR"

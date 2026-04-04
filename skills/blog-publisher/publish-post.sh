#!/bin/bash
# Publish Blog Post
# Usage: ./publish-post.sh draft.html "2026-03-28"

set -e

DRAFT_FILE="$1"
DATE="$2"
BLOG_DIR="/var/www/patchrat.chainbytes.io/blog"

echo "🚀 Publishing blog post..."

# Validate inputs
if [ -z "$DRAFT_FILE" ] || [ -z "$DATE" ]; then
    echo "Usage: $0 \u003cdraft.html\u003e \u003cYYYY-MM-DD\u003e"
    exit 1
fi

if [ ! -f "$DRAFT_FILE" ]; then
    echo "❌ Draft file not found: $DRAFT_FILE"
    exit 1
fi

# Extract components
YEAR=${DATE:0:4}
MONTH=${DATE:5:2}
DAY=${DATE:8:2}

# Run consistency check
echo "🔍 Running consistency checks..."
if ! ./check-post.sh "$DRAFT_FILE"; then
    echo "❌ Consistency check failed. Fix issues before publishing."
    exit 1
fi

# Check for hero image
POST_CONTENT=$(cat "$DRAFT_FILE")
if ! echo "$POST_CONTENT" | grep -q "\u003cimg"; then
    echo "⚠️  No hero image detected. Generating..."
    
    # Extract title for image prompt
    TITLE=$(echo "$POST_CONTENT" | grep -oP "(?\u003c=\u003ch1\u003e).*?(?=\u003c/h1\u003e)" | head -1)
    
    # Generate image via Gemini (placeholder - would call actual API)
    echo "   Title: $TITLE"
    echo "   Would generate: Dark cyberpunk illustration of '$TITLE'"
    echo "   Save to: ${BLOG_DIR}/images/${YEAR}/${MONTH}/${DAY}-hero.jpg"
    
    # For now, copy a default hero image
    mkdir -p "${BLOG_DIR}/images/${YEAR}/${MONTH}"
    # cp default-hero.jpg "${BLOG_DIR}/images/${YEAR}/${MONTH}/${DAY}-hero.jpg"
fi

# Create post directory
mkdir -p "${BLOG_DIR}/posts/${YEAR}/${MONTH}/${DAY}"

# Create slug from title
SLUG=$(echo "$POST_CONTENT" | grep -oP "(?\u003c=\u003ch1\u003e).*?(?=\u003c/h1\u003e)" | head -1 | \
       tr '[:upper:]' '[:lower:]' | \
       tr ' ' '-' | \
       tr -dc 'a-z0-9-' | \
       cut -c1-50)

# Copy post
cp "$DRAFT_FILE" "${BLOG_DIR}/posts/${YEAR}/${MONTH}/${DAY}/${SLUG}.html"
echo "✅ Post copied to: posts/${YEAR}/${MONTH}/${DAY}/${SLUG}.html"

# Update index
echo "📊 Regenerating index..."
cd "$BLOG_DIR" && python3 generate-index.py

# Git operations (if repo exists)
if [ -d "${BLOG_DIR}/.git" ]; then
    echo "📦 Committing to git..."
    cd "$BLOG_DIR"
    git add .
    git commit -m "Publish: ${TITLE} (${DATE})"
    git push origin main
fi

echo ""
echo "🎉 Published successfully!"
echo "   URL: https://patchrat.chainbytes.io/blog/posts/${YEAR}/${MONTH}/${DAY}/${SLUG}.html"

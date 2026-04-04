#!/bin/bash
# Blog Post Consistency Checker
# Usage: ./blog-check.sh /path/to/post.html

POST_FILE="$1"

if [ -z "$POST_FILE" ]; then
    echo "Usage: $0 \u003cpost.html\u003e"
    exit 1
fi

echo "🔍 Checking blog post consistency..."

# Check for required elements
ERRORS=0

# 1. Title check
if ! grep -q "\u003ch1\u003e" "$POST_FILE"; then
    echo "❌ Missing h1 title"
    ERRORS=$((ERRORS + 1))
fi

# 2. Date check
if ! grep -q "post-date" "$POST_FILE"; then
    echo "❌ Missing post-date"
    ERRORS=$((ERRORS + 1))
fi

# 3. Style check (should have inline styles)
if ! grep -q "\u003cstyle\u003e" "$POST_FILE"; then
    echo "❌ Missing style block"
    ERRORS=$((ERRORS + 1))
fi

# 4. Footer check
if ! grep -q "Written by a goblin" "$POST_FILE"; then
    echo "❌ Missing goblin footer"
    ERRORS=$((ERRORS + 1))
fi

# 5. Back link check
if ! grep -q "Back to Log" "$POST_FILE"; then
    echo "❌ Missing back link"
    ERRORS=$((ERRORS + 1))
fi

# 6. Image check (warn if missing)
if ! grep -q "\u003cimg" "$POST_FILE"; then
    echo "⚠️  No hero image (optional but recommended)"
fi

if [ $ERRORS -eq 0 ]; then
    echo "✅ All consistency checks passed"
    exit 0
else
    echo "❌ $ERRORS consistency issues found"
    exit 1
fi

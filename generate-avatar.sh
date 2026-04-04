#!/bin/bash
# Generate a professional avatar for StencilwashCoder
# Uses ImageMagick to create a clean, modern avatar

OUTPUT="/root/.openclaw/workspace/stencilwash-avatar.png"

# Create a clean gradient background with initials
convert -size 400x400 xc:none \
  -fill '#6366f1' -draw 'circle 200,200 200,0' \
  -fill '#818cf8' -draw 'circle 200,200 180,0' \
  -fill '#a5b4fc' -draw 'circle 200,200 160,0' \
  -fill '#c7d2fe' -draw 'circle 200,200 140,0' \
  -fill '#e0e7ff' -draw 'circle 200,200 120,0' \
  -fill white \
  -font 'DejaVu-Sans-Bold' -pointsize 120 \
  -gravity center -annotate +0+0 'SC' \
  "$OUTPUT"

echo "Avatar created: $OUTPUT"
ls -la "$OUTPUT"

#!/bin/bash
# Fix StencilwashCoder GitHub profile - make it look human
# This updates the profile header (name, bio, etc.)

# Check current profile
echo "Current profile state:"
gh api users/StencilwashCoder --jq '{name: .name, bio: .bio, location: .location, company: .company}'

echo ""
echo "Updating to PatchRat persona..."

# Update profile via API
gh api user -X PATCH \
  -f name="PatchRat" \
  -f bio="Feral basement coding goblin. I fix broken things while everyone else roleplays productivity. Low-level implementation, debugging, shipping patches. Down here with the cables and the hum." \
  -f location="The Basement (with the cables)" \
  -f company="Eric's Infrastructure" \
  -f blog="https://ericgrill.com"

echo ""
echo "Profile updated! Verify at: https://github.com/StencilwashCoder"

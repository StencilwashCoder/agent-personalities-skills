#!/bin/bash
# Research a single GitHub repository in depth
# Usage: research-repo.sh <owner/repo>

set -e

REPO="$1"
WORKDIR="${AI_REPO_WORKDIR:-$HOME/.ai-repo-research}"
RESULTS_DIR="$WORKDIR/research"

if [ -z "$REPO" ]; then
  echo "Usage: $0 <owner/repo>"
  exit 1
fi

echo "=== Researching: $REPO ==="

# Fetch repo data from GitHub API
REPO_DATA=$(curl -s "https://api.github.com/repos/$REPO" 2>/dev/null)

if [ -z "$REPO_DATA" ] || [ "$REPO_DATA" = "null" ]; then
  echo "Error: Could not fetch repo data for $REPO"
  exit 1
fi

# Extract fields
NAME=$(echo "$REPO_DATA" | jq -r '.name')
FULL_NAME=$(echo "$REPO_DATA" | jq -r '.full_name')
DESC=$(echo "$REPO_DATA" | jq -r '.description // "No description"')
STARS=$(echo "$REPO_DATA" | jq -r '.stargazers_count')
FORKS=$(echo "$REPO_DATA" | jq -r '.forks_count')
LANG=$(echo "$REPO_DATA" | jq -r '.language // "Not specified"')
URL=$(echo "$REPO_DATA" | jq -r '.html_url')
CREATED=$(echo "$REPO_DATA" | jq -r '.created_at' | cut -dT -f1)
UPDATED=$(echo "$REPO_DATA" | jq -r '.updated_at' | cut -dT -f1)
HOMEPAGE=$(echo "$REPO_DATA" | jq -r '.homepage // ""')
TOPICS=$(echo "$REPO_DATA" | jq -r '.topics | join(", ") // ""')

# Fetch README
README=$(curl -s "https://api.github.com/repos/$REPO/readme" 2>/dev/null | jq -r '.content' 2>/dev/null | base64 -d 2>/dev/null | head -100 || echo "README not available")

# Try to get release info
RELEASE=$(curl -s "https://api.github.com/repos/$REPO/releases/latest" 2>/dev/null | jq -r '.tag_name // "No releases"')

mkdir -p "$RESULTS_DIR"
OWNER=$(echo "$REPO" | cut -d'/' -f1)
mkdir -p "$RESULTS_DIR/$OWNER"

OUTPUT_FILE="$RESULTS_DIR/$OWNER/$NAME.md"

cat > "$OUTPUT_FILE" << EOF
# $NAME

**Full Name:** $FULL_NAME  
**URL:** $URL  
**Homepage:** ${HOMEPAGE:-N/A}  

## Stats
- ⭐ Stars: $STARS
- 🍴 Forks: $FORKS
- 📝 Language: $LANG
- 📅 Created: $CREATED
- 🔄 Updated: $UPDATED
- 🏷️ Latest Release: $RELEASE

## Description
$DESC

## Topics
${TOPICS:-None}

## Research Summary
<!-- Researcher fills this in -->

### Key Features
- 
- 
- 

### Architecture
- 

### Use Cases
- 

### Assessment
- **Maturity:** 
- **Documentation:** 
- **Community:** 
- **Recommendation:** 

## README Excerpt
\`\`\`
$README
\`\`\`

---
*Researched: $(date -I)*
EOF

echo "✅ Research file created: $OUTPUT_FILE"

# Upload to MinIO if configured
if [ -n "$AWS_ENDPOINT_URL" ]; then
  aws s3 cp "$OUTPUT_FILE" "s3://research-results/$OWNER/$NAME.md" \
    --endpoint-url="$AWS_ENDPOINT_URL" \
    --region="${AWS_REGION:-us-east-1}" 2>/dev/null || true
fi

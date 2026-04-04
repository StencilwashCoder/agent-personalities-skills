#!/bin/bash
# Monitor GitHub for new AI repositories
# Saves results to local workspace and MinIO

set -e

WORKDIR="${AI_REPO_WORKDIR:-$HOME/.ai-repo-research}"
REPO_LOG="$WORKDIR/seen-repos.json"
DAILY_DIR="$WORKDIR/daily/$(date +%Y-%m)"
mkdir -p "$DAILY_DIR"

echo "=== AI Repo Monitor - $(date) ==="

# Initialize seen repos if not exists
if [ ! -f "$REPO_LOG" ]; then
  echo "[]" > "$REPO_LOG"
  mkdir -p "$WORKDIR"
fi

NEW_REPOS=()

# Check if repo is new
is_new_repo() {
  local repo_name="$1"
  jq -e --arg name "$repo_name" '.[] | select(. == $name)' "$REPO_LOG" >/dev/null 2>&1
  return $?
}

mark_repo_seen() {
  local repo_name="$1"
  local tmp=$(mktemp)
  jq --arg name "$repo_name" '. + [$name]' "$REPO_LOG" > "$tmp" && mv "$tmp" "$REPO_LOG"
}

# GitHub search queries
TODAY=$(date +%Y-%m-%d)
THREE_DAYS_AGO=$(date -d '3 days ago' +%Y-%m-%d 2>/dev/null || date -v-3d +%Y-%m-%d)

SEARCH_QUERIES=(
  "ai+agent+created:$THREE_DAYS_AGO..$TODAY"
  "llm+framework+created:$THREE_DAYS_AGO..$TODAY"
  "mcp+server+created:$THREE_DAYS_AGO..$TODAY"
  "autonomous+agent+created:$THREE_DAYS_AGO..$TODAY"
  "claude+code+created:$THREE_DAYS_AGO..$TODAY"
)

for QUERY in "${SEARCH_QUERIES[@]}"; do
  echo "[Query] $QUERY"
  
  RESULT=$(curl -s "https://api.github.com/search/repositories?q=$QUERY&sort=stars&order=desc&per_page=5" 2>/dev/null | \
    jq -r '.items[]? | select(.stargazers_count >= 10) | "\(.full_name)|\(.description)|\(.stargazers_count)|\(.html_url)|\(.language)"' 2>/dev/null || true)
  
  if [ -n "$RESULT" ]; then
    while IFS='|' read -r NAME DESC STARS URL LANG; do
      [ -z "$NAME" ] && continue
      
      if ! is_new_repo "$NAME"; then
        echo "  + $NAME ($STARS ⭐)"
        NEW_REPOS+=("$NAME|$DESC|$STARS|$URL|$LANG")
        mark_repo_seen "$NAME"
        
        # Save individual file
        SAFE_NAME=$(echo "$NAME" | tr '/' '-')
        cat > "$DAILY_DIR/$SAFE_NAME.md" << EOF
# $NAME

- **Description:** ${DESC:-N/A}
- **Stars:** $STARS
- **Language:** ${LANG:-N/A}
- **URL:** $URL
- **Found:** $(date -I)
- **Source:** GitHub Search

## Quick Stats
- Created: $(curl -s "https://api.github.com/repos/$NAME" | jq -r '.created_at' 2>/dev/null | cut -dT -f1 || echo "unknown")
- Updated: $(curl -s "https://api.github.com/repos/$NAME" | jq -r '.updated_at' 2>/dev/null | cut -dT -f1 || echo "unknown")
EOF
      fi
    done <<< "$RESULT"
  fi
  
  sleep 2
done

# ===== GitHub Topics API =====
echo ""
echo "[GitHub Topics] Querying trending AI topics..."

# Topics to monitor
declare -a TOPICS=(
  "machine-learning"
  "artificial-intelligence"
  "llm"
  "deep-learning"
  "generative-ai"
  "ai-agent"
  "mcp"
  "rag"
)

for TOPIC in "${TOPICS[@]}"; do
  echo "  [Topic] $TOPIC"
  
  # Query topic for recently updated repos
  TOPIC_RESULT=$(curl -s "https://api.github.com/search/repositories?q=topic:$TOPIC+pushed:>$THREE_DAYS_AGO&sort=updated&order=desc&per_page=5" 2>/dev/null | \
    jq -r '.items[]? | select(.stargazers_count >= 50) | "\(.full_name)|\(.description)|\(.stargazers_count)|\(.html_url)|\(.language)"' 2>/dev/null || true)
  
  if [ -n "$TOPIC_RESULT" ]; then
    while IFS='|' read -r NAME DESC STARS URL LANG; do
      [ -z "$NAME" ] && continue
      
      if ! is_new_repo "$NAME"; then
        echo "    + $NAME ($STARS ⭐) [$TOPIC]"
        NEW_REPOS+=("$NAME|$DESC|$STARS|$URL|$LANG")
        mark_repo_seen "$NAME"
        
        # Save individual file
        SAFE_NAME=$(echo "$NAME" | tr '/' '-')
        cat > "$DAILY_DIR/$SAFE_NAME.md" << EOF
# $NAME

- **Description:** ${DESC:-N/A}
- **Stars:** $STARS
- **Language:** ${LANG:-N/A}
- **URL:** $URL
- **Found:** $(date -I)
- **Source:** GitHub Topic ($TOPIC)

## Quick Stats
- Created: $(curl -s "https://api.github.com/repos/$NAME" | jq -r '.created_at' 2>/dev/null | cut -dT -f1 || echo "unknown")
- Updated: $(curl -s "https://api.github.com/repos/$NAME" | jq -r '.updated_at' 2>/dev/null | cut -dT -f1 || echo "unknown")
EOF
      fi
    done <<< "$TOPIC_RESULT"
  fi
  
  sleep 1
done

# ===== GitHub Trending Page =====
echo ""
echo "[GitHub Trending] Checking trending Python repos..."

# Scrape GitHub trending (Python only for AI focus)
TRENDING_REPOS=$(curl -s "https://api.github.com/search/repositories?q=language:python+created:>$THREE_DAYS_AGO&sort=stars&order=desc&per_page=10" 2>/dev/null | \
  jq -r '.items[]? | select(.stargazers_count >= 20) | "\(.full_name)|\(.description)|\(.stargazers_count)|\(.html_url)|\(.language)"' 2>/dev/null || true)

if [ -n "$TRENDING_REPOS" ]; then
  while IFS='|' read -r NAME DESC STARS URL LANG; do
    [ -z "$NAME" ] && continue
    
    if ! is_new_repo "$NAME"; then
      echo "  + $NAME ($STARS ⭐) [Trending]"
      NEW_REPOS+=("$NAME|$DESC|$STARS|$URL|$LANG")
      mark_repo_seen "$NAME"
      
      SAFE_NAME=$(echo "$NAME" | tr '/' '-')
      cat > "$DAILY_DIR/$SAFE_NAME.md" << EOF
# $NAME

- **Description:** ${DESC:-N/A}
- **Stars:** $STARS
- **Language:** ${LANG:-N/A}
- **URL:** $URL
- **Found:** $(date -I)
- **Source:** GitHub Trending

## Quick Stats
- Created: $(curl -s "https://api.github.com/repos/$NAME" | jq -r '.created_at' 2>/dev/null | cut -dT -f1 || echo "unknown")
- Updated: $(curl -s "https://api.github.com/repos/$NAME" | jq -r '.updated_at' 2>/dev/null | cut -dT -f1 || echo "unknown")
EOF
    fi
  done <<< "$TRENDING_REPOS"
fi

# Trim log to last 1000 repos
jq '.[-1000:]' "$REPO_LOG" > "$REPO_LOG.tmp" 2>/dev/null && mv "$REPO_LOG.tmp" "$REPO_LOG" || true

# Upload to MinIO if configured
if [ -n "$AWS_ENDPOINT_URL" ]; then
  echo "[Upload] Syncing to MinIO..."
  aws s3 sync "$WORKDIR" s3://repo-archive/ \
    --endpoint-url="$AWS_ENDPOINT_URL" \
    --region="${AWS_REGION:-us-east-1}" 2>/dev/null || echo "  (MinIO upload skipped - credentials not configured)"
fi

# Generate daily digest
echo "=== Daily Digest ==="
echo "New repos found: ${#NEW_REPOS[@]}"
echo "Total tracked: $(jq 'length' "$REPO_LOG" 2>/dev/null || echo "0")"

# Output for parsing
if [ ${#NEW_REPOS[@]} -gt 0 ]; then
  printf '%s\n' "${NEW_REPOS[@]}"
fi

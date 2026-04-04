#!/bin/bash
# GitHub AI Repos Monitor - Direct Source Edition
# Combines GitHub Trending + curated sources for daily AI repo digest

set -e

TELEGRAM_BOT="8600179570:AAGn9cHOVqgj5JYJ9jAcXR-BlSrgwRJbWTw"
TELEGRAM_CHAT="84020120"
WORKDIR="/root/.openclaw/workspace/ai-repos-daily"
REPO_LOG="$WORKDIR/seen_repos.json"
mkdir -p "$WORKDIR"

# Initialize seen repos log if not exists
if [ ! -f "$REPO_LOG" ]; then
  echo "[]" > "$REPO_LOG"
fi

echo "=== AI Repo Monitor - $(date) ==="

# Array to store new repos
NEW_REPOS=()

# Function to check if repo is already seen
is_new_repo() {
  local repo_name="$1"
  jq -e --arg name "$repo_name" '.[] | select(. == $name)' "$REPO_LOG" > /dev/null 2>&1
  return $?
}

# Function to add repo to seen log
mark_repo_seen() {
  local repo_name="$1"
  local tmp_file=$(mktemp)
  jq --arg name "$repo_name" '. + [$name]' "$REPO_LOG" > "$tmp_file" && mv "$tmp_file" "$REPO_LOG"
}

# Source 1: GitHub Search - AI repos created in last 3 days, sorted by stars
echo "[Source 1] Checking GitHub for new AI repos..."
TODAY=$(date +%Y-%m-%d)
THREE_DAYS_AGO=$(date -d '3 days ago' +%Y-%m-%d)

# Multiple search queries for different AI categories
SEARCH_QUERIES=(
  "ai+agent+created:$THREE_DAYS_AGO..$TODAY"
  "llm+framework+created:$THREE_DAYS_AGO..$TODAY"
  "claude+openai+created:$THREE_DAYS_AGO..$TODAY"
  "mcp+server+created:$THREE_DAYS_AGO..$TODAY"
  "autonomous+agent+created:$THREE_DAYS_AGO..$TODAY"
)

for QUERY in "${SEARCH_QUERIES[@]}"; do
  echo "  Query: $QUERY"
  
  RESULT=$(curl -s "https://api.github.com/search/repositories?q=$QUERY&sort=stars&order=desc&per_page=5" | \
    jq -r '.items[] | select(.stargazers_count >= 10) | "\(.full_name)|\(.description)|\(.stargazers_count)|\(.html_url)|\(.language)"' 2>/dev/null || true)
  
  if [ -n "$RESULT" ]; then
    while IFS='|' read -r NAME DESC STARS URL LANG; do
      if ! is_new_repo "$NAME"; then
        echo "    NEW: $NAME ($STARS ⭐)"
        NEW_REPOS+=("$NAME|$DESC|$STARS|$URL|$LANG")
        mark_repo_seen "$NAME"
        
        # Save individual repo file
        SAFE_NAME=$(echo "$NAME" | tr '/' '-')
        cat > "$WORKDIR/$SAFE_NAME.md" << EOF
# $NAME

- **Description:** $DESC
- **Stars:** $STARS
- **Language:** $LANG
- **URL:** $URL
- **Found:** $(date -I)
- **Source:** GitHub Search
EOF
      fi
    done <<< "$RESULT"
  fi
  
  sleep 2  # Rate limit protection
done

# Source 2: GitHub Trending (scraping trending page)
echo "[Source 2] Checking GitHub Trending..."

# Trending repos are harder to get via API - use search for recently starred
TRENDING_RESULT=$(curl -s "https://api.github.com/search/repositories?q=ai+OR+llm+OR+agent+pushed:$THREE_DAYS_AGO..$TODAY&sort=stars&order=desc&per_page=10" | \
  jq -r '.items[] | select(.stargazers_count >= 50) | "\(.full_name)|\(.description)|\(.stargazers_count)|\(.html_url)|\(.language)"' 2>/dev/null || true)

if [ -n "$TRENDING_RESULT" ]; then
  while IFS='|' read -r NAME DESC STARS URL LANG; do
    if ! is_new_repo "$NAME"; then
      echo "    NEW: $NAME ($STARS ⭐) [Trending]"
      NEW_REPOS+=("$NAME|$DESC|$STARS|$URL|$LANG")
      mark_repo_seen "$NAME"
    fi
  done <<< "$TRENDING_RESULT"
fi

# Source 3: Try to fetch from agents.blog RSS if available
echo "[Source 3] Checking agents.blog feed..."
# Note: agents.blog may not have RSS - this is a placeholder for future RSS integration

# Clean up old entries (keep last 500 repos)
echo "[Cleanup] Trimming repo history..."
jq '.[-500:]' "$REPO_LOG" > "$REPO_LOG.tmp" && mv "$REPO_LOG.tmp" "$REPO_LOG"

# Send digest if new repos found
echo "[Notification] Checking for new repos to report..."

if [ ${#NEW_REPOS[@]} -gt 0 ]; then
  MESSAGE="🤖 AI Repo Digest ($(date +%Y-%m-%d))

Found ${#NEW_REPOS[@]} new AI repositories:"
  
  # Limit to top 10 for Telegram message length
  COUNT=0
  for REPO in "${NEW_REPOS[@]}"; do
    if [ $COUNT -ge 10 ]; then
      MESSAGE="$MESSAGE

...and $((${#NEW_REPOS[@]} - 10)) more saved to workspace"
      break
    fi
    
    NAME=$(echo "$REPO" | cut -d'|' -f1)
    DESC=$(echo "$REPO" | cut -d'|' -f2 | cut -c1-80)
    STARS=$(echo "$REPO" | cut -d'|' -f3)
    URL=$(echo "$REPO" | cut -d'|' -f4)
    LANG=$(echo "$REPO" | cut -d'|' -f5)
    
    MESSAGE="$MESSAGE

🔹 $NAME
⭐ $STARS | ${LANG:-N/A}
${DESC:-No description}
$URL"
    
    ((COUNT++))
  done
  
  # Send to Telegram
  curl -s -X POST "https://api.telegram.org/bot$TELEGRAM_BOT/sendMessage" \
    -d "chat_id=$TELEGRAM_CHAT" \
    -d "text=$MESSAGE" \
    -d "disable_web_page_preview=true" > /dev/null
  
  echo "✅ Sent Telegram notification: ${#NEW_REPOS[@]} repos"
else
  echo "ℹ️ No new repos found today"
fi

echo "=== Done - $(date) ==="
echo "Total repos tracked: $(jq 'length' "$REPO_LOG")"

#!/bin/bash
# AlexAI GitHub Repo Monitor
# Runs twice daily to find repos mentioned in AlexAI Facebook posts

set -e

APIFY_TOKEN="${APIFY_TOKEN:-your_apify_token_here}"
TELEGRAM_BOT="${TELEGRAM_BOT_TOKEN:-your_telegram_bot_token_here}"
TELEGRAM_CHAT="${TELEGRAM_CHAT_ID:-your_chat_id_here}"
WORKDIR="/root/.openclaw/workspace/alexai-repos"
mkdir -p "$WORKDIR"

echo "=== AlexAI Repo Monitor ==="
echo "Time: $(date)"

# Step 1: Scrape Facebook posts
echo "[1/4] Scraping AlexAI Facebook posts..."
RUN_RESULT=$(curl -s -X POST "https://api.apify.com/v2/acts/apify~facebook-posts-scraper/runs?token=$APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "startUrls": [{"url": "https://www.facebook.com/Alexaiupdate"}],
    "resultsLimit": 20,
    "includeComments": false
  }')

RUN_ID=$(echo "$RUN_RESULT" | jq -r '.data.id')
if [ "$RUN_ID" = "null" ] || [ -z "$RUN_ID" ]; then
  echo "ERROR: Failed to start Apify run"
  echo "$RUN_RESULT"
  exit 1
fi

echo "Run ID: $RUN_ID"

# Wait for completion
for i in {1..30}; do
  sleep 10
  STATUS=$(curl -s "https://api.apify.com/v2/actor-runs/$RUN_ID?token=$APIFY_TOKEN" | jq -r '.data.status')
  echo "  Status: $STATUS (attempt $i)"
  if [ "$STATUS" = "SUCCEEDED" ]; then
    break
  elif [ "$STATUS" = "FAILED" ] || [ "$STATUS" = "ABORTED" ]; then
    echo "ERROR: Run failed with status $STATUS"
    exit 1
  fi
done

# Get dataset ID
DATASET_ID=$(curl -s "https://api.apify.com/v2/actor-runs/$RUN_ID?token=$APIFY_TOKEN" | jq -r '.data.defaultDatasetId')
echo "Dataset ID: $DATASET_ID"

# Step 2: Extract post text and find repo mentions
echo "[2/4] Extracting repo names from posts..."
curl -s "https://api.apify.com/v2/datasets/$DATASET_ID/items?token=$APIFY_TOKEN" > /tmp/alexai_posts.json

# Extract potential repo names using patterns
# Pattern 1: quoted names
# Pattern 2: "called/named X" 
# Pattern 3: CamelCase words that look like repo names
# Pattern 4: hyphenated names

REPO_NAMES=$(cat /tmp/alexai_posts.json | jq -r '.[].text' | grep -v null | \
  grep -oEi '(called|named) "?[^"]{3,50}"?' | \
  sed -E 's/(called|named) "?//gi; s/"$//' | \
  sort -u | head -20)

# Also extract CamelCase/hyphenated that look like projects
PROJECT_NAMES=$(cat /tmp/alexai_posts.json | jq -r '.[].text' | grep -v null | \
  grep -oE '(^|[[:space:]])[A-Z][a-z]+[A-Z][a-zA-Z0-9]*|(^|[[:space:]])[a-z]+-[a-z]+' | \
  tr -d '[:space:]' | sort -u | head -20)

echo "Found repo name hints:"
echo "$REPO_NAMES"
echo "$PROJECT_NAMES"

# Step 3: Search GitHub for each potential repo
echo "[3/4] Searching GitHub for repos..."
FOUND_REPOS=()

for NAME in $REPO_NAMES $PROJECT_NAMES; do
  # Clean up the name
  CLEAN_NAME=$(echo "$NAME" | tr -cd '[:alnum:]-_' | head -c 50)
  if [ -z "$CLEAN_NAME" ] || [ ${#CLEAN_NAME} -lt 3 ]; then
    continue
  fi
  
  echo "  Searching: $CLEAN_NAME"
  
  # Search GitHub
  SEARCH_RESULT=$(curl -s "https://api.github.com/search/repositories?q=$CLEAN_NAME+in:name&sort=stars&order=desc&per_page=1" | \
    jq -r '.items[0] | if . then "\(.full_name)|\(.description)|\(.stargazers_count)|\(.html_url)" else empty end')
  
  if [ -n "$SEARCH_RESULT" ]; then
    # Check if we already have this repo
    REPO_FILE="$WORKDIR/$(echo "$SEARCH_RESULT" | cut -d'|' -f1 | tr '/' '-').md"
    if [ ! -f "$REPO_FILE" ]; then
      echo "    NEW: $SEARCH_RESULT"
      FOUND_REPOS+=("$SEARCH_RESULT")
      
      # Save to file
      echo "# $(echo "$SEARCH_RESULT" | cut -d'|' -f1)" > "$REPO_FILE"
      echo "" >> "$REPO_FILE"
      echo "- **Description:** $(echo "$SEARCH_RESULT" | cut -d'|' -f2)" >> "$REPO_FILE"
      echo "- **Stars:** $(echo "$SEARCH_RESULT" | cut -d'|' -f3)" >> "$REPO_FILE"
      echo "- **URL:** $(echo "$SEARCH_RESULT" | cut -d'|' -f4)" >> "$REPO_FILE"
      echo "- **Found:** $(date -I)" >> "$REPO_FILE"
      echo "" >> "$REPO_FILE"
      echo "## Source" >> "$REPO_FILE"
      echo "From AlexAI Facebook page" >> "$REPO_FILE"
    fi
  fi
done

# Step 4: Send Telegram digest if new repos found
echo "[4/4] Sending notifications..."

if [ ${#FOUND_REPOS[@]} -gt 0 ]; then
  MESSAGE="📊 AlexAI Repo Digest ($(date +%Y-%m-%d))

Found ${#FOUND_REPOS[@]} new GitHub repositories:"
  
  for REPO in "${FOUND_REPOS[@]}"; do
    NAME=$(echo "$REPO" | cut -d'|' -f1)
    DESC=$(echo "$REPO" | cut -d'|' -f2 | cut -c1-100)
    STARS=$(echo "$REPO" | cut -d'|' -f3)
    URL=$(echo "$REPO" | cut -d'|' -f4)
    
    MESSAGE="$MESSAGE

🔹 $NAME
⭐ $STARS stars
$DESC
$URL"
  done
  
  # Send to Telegram
  curl -s -X POST "https://api.telegram.org/bot$TELEGRAM_BOT/sendMessage" \
    -d "chat_id=$TELEGRAM_CHAT" \
    -d "text=$MESSAGE" \
    -d "disable_web_page_preview=true"
  
  echo "Sent Telegram notification with ${#FOUND_REPOS[@]} repos"
else
  echo "No new repos found"
fi

echo "=== Done ==="

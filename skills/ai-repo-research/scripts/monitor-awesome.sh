#!/bin/bash
# Monitor Awesome Lists for new AI/ML repository additions
# Tracks: awesome-machine-learning, Awesome-LLM, awesome-computer-vision, etc.

set -e

WORKDIR="${AI_REPO_WORKDIR:-$HOME/.ai-repo-research}"
REPO_LOG="$WORKDIR/seen-repos.json"
AWESOME_LOG="$WORKDIR/awesome-lists.json"
QUEUE_DIR="$WORKDIR/queue/pending"
DAILY_DIR="$WORKDIR/daily/$(date +%Y-%m)"
mkdir -p "$QUEUE_DIR" "$DAILY_DIR"

echo "=== Awesome Lists Scraper - $(date) ==="

# Initialize
if [ ! -f "$REPO_LOG" ]; then
  echo "[]" > "$REPO_LOG"
fi
if [ ! -f "$AWESOME_LOG" ]; then
  echo "{}" > "$AWESOME_LOG"
fi

is_new_repo() {
  local repo_name="$1"
  jq -e --arg name "$repo_name" '.[] | select(. == $name)' "$REPO_LOG" >/dev/null 2>&1
  return $?
}

mark_repo_seen() {
  local repo_name="$1"
  local tmp=$(mktemp)
  jq --arg name "$repo_name" '. + [$name]' "$REPO_LOG" > "$tmp" 2>/dev/null && mv "$tmp" "$REPO_LOG" || rm "$tmp"
}

submit_to_queue() {
  local repo="$1"
  local source="$2"
  local timestamp=$(date +%s)
  local request_file="$QUEUE_DIR/${timestamp}-$(echo "$repo" | tr '/' '-').json"
  
  cat > "$request_file" << EOF
{
  "repo": "$repo",
  "priority": "medium",
  "requested_by": "awesome-scraper",
  "notes": "Discovered via $source",
  "submitted_at": "$(date -Iseconds)"
}
EOF
  echo "  → Queued for research"
}

extract_repos() {
  # Extract repos from markdown links [name](github.com/owner/repo)
  grep -oE '\(https?://github\.com/[a-zA-Z0-9_-]+/[a-zA-Z0-9._-]+\)' | \
    sed 's|https://github.com/||;s|http://github.com/||;s/)//g;s/(//g' | sort -u
}

NEW_REPOS=()

# Define awesome lists to monitor
declare -a AWESOME_LISTS=(
  "josephmisiti/awesome-machine-learning|72.1k|General ML"
  "academic/awesome-datascience|28.7k|Data Science"
  "Hannibal046/Awesome-LLM|26.5k|Large Language Models"
  "jbhuang0604/awesome-computer-vision|23.1k|Computer Vision"
  "EthicalML/awesome-production-machine-learning|20.3k|MLOps"
  "keon/awesome-nlp|18.3k|NLP"
  "BradyFU/Awesome-Multimodal-Large-Language-Models|17.5k|Multimodal AI"
  "WooooDyy/LLM-Agent-Paper-List|7.6k|LLM Agents"
  "christoschristofidis/awesome-deep-learning|10k|Deep Learning"
  "awesomelistsio/awesome-generative-ai|2.5k|Generative AI"
  "ai-boost/awesome-ai-for-science|1.4k|Scientific AI"
  "Jim-Schwoebel/awesome_ai_agents|5k|AI Agents"
  "Shubhamsaboo/awesome-llm-apps|8k|LLM Apps"
)

for LIST_INFO in "${AWESOME_LISTS[@]}"; do
  IFS='|' read -r REPO STARS FOCUS <<< "$LIST_INFO"
  
  echo ""
  echo "[List] $REPO ($FOCUS)"
  
  # Get raw README
  README_URL="https://raw.githubusercontent.com/$REPO/main/README.md"
  README=$(curl -sL "$README_URL" 2>/dev/null || curl -sL "${README_URL/main/master}" 2>/dev/null || true)
  
  if [ -z "$README" ]; then
    echo "  (Could not fetch README)"
    continue
  fi
  
  # Get last commit date for change tracking
  LAST_COMMIT=$(curl -s "https://api.github.com/repos/$REPO/commits?per_page=1" 2>/dev/null | \
    jq -r '.[0].commit.committer.date' 2>/dev/null | cut -dT -f1 || echo "unknown")
  
  # Check if we've seen this list version
  LAST_SEEN=$(jq -r --arg repo "$REPO" '.[$repo] // "never"' "$AWESOME_LOG" 2>/dev/null)
  
  if [ "$LAST_COMMIT" = "$LAST_SEEN" ]; then
    echo "  (No changes since $LAST_SEEN)"
    continue
  fi
  
  # Extract repos from README
  LIST_REPOS=$(echo "$README" | extract_repos || true)
  REPO_COUNT=0
  
  for FOUND_REPO in $LIST_REPOS; do
    # Skip self-references
    [[ "$FOUND_REPO" == "$REPO"* ]] && continue
    
    if ! is_new_repo "$FOUND_REPO"; then
      echo "  + $FOUND_REPO"
      NEW_REPOS+=("$FOUND_REPO|$REPO")
      mark_repo_seen "$FOUND_REPO"
      submit_to_queue "$FOUND_REPO" "$REPO (awesome list)"
      REPO_COUNT=$((REPO_COUNT + 1))
      
      # Limit per list to avoid overwhelming
      [ "$REPO_COUNT" -ge 10 ] && break
    fi
  done
  
  # Update last seen
  TMP=$(mktemp)
  jq --arg repo "$REPO" --arg date "$LAST_COMMIT" '.[$repo] = $date' "$AWESOME_LOG" > "$TMP" 2>/dev/null && mv "$TMP" "$AWESOME_LOG" || rm "$TMP"
  
  sleep 1
done

# ===== Summary =====
echo ""
echo "=== Awesome Lists Summary ==="
echo "New repos found: ${#NEW_REPOS[@]}"
echo "Total tracked: $(jq 'length' "$REPO_LOG" 2>/dev/null || echo "0")"

# Upload queue to MinIO if configured
if [ -n "$AWS_ENDPOINT_URL" ] && [ ${#NEW_REPOS[@]} -gt 0 ]; then
  echo "[Upload] Syncing queue to MinIO..."
  aws s3 sync "$QUEUE_DIR" "s3://research-queue/pending/" \
    --endpoint-url="$AWS_ENDPOINT_URL" \
    --region="${AWS_REGION:-us-east-1}" 2>/dev/null || echo "  (MinIO sync may have issues)"
fi

# Output for parsing
if [ ${#NEW_REPOS[@]} -gt 0 ]; then
  printf '%s\n' "${NEW_REPOS[@]}"
fi

echo "Done: $(date)"

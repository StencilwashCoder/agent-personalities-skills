#!/bin/bash
# Monitor Reddit communities for GitHub repository links
# Tracks: r/MachineLearning, r/LocalLLaMA, r/ArtificialIntelligence

set -e

WORKDIR="${AI_REPO_WORKDIR:-$HOME/.ai-repo-research}"
REPO_LOG="$WORKDIR/seen-repos.json"
QUEUE_DIR="$WORKDIR/queue/pending"
DAILY_DIR="$WORKDIR/daily/$(date +%Y-%m)"
mkdir -p "$QUEUE_DIR" "$DAILY_DIR"

echo "=== Reddit Repo Scraper - $(date) ==="

# Initialize
if [ ! -f "$REPO_LOG" ]; then
  echo "[]" > "$REPO_LOG"
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
  "priority": "high",
  "requested_by": "reddit-scraper",
  "notes": "Discovered via $source",
  "submitted_at": "$(date -Iseconds)"
}
EOF
  echo "  → Queued for research"
}

extract_repos() {
  grep -oE 'github\.com/[a-zA-Z0-9_-]+/[a-zA-Z0-9._-]+' | sed 's|github.com/||' | sort -u
}

NEW_REPOS=()

# ===== r/MachineLearning =====
echo ""
echo "[Subreddit] r/MachineLearning"
# Reddit JSON API - no auth needed for public read
ML_JSON=$(curl -s -A "Mozilla/5.0 (compatible; AIBot/1.0)" \
  "https://www.reddit.com/r/MachineLearning/hot.json?limit=25" 2>/dev/null || true)

if [ -n "$ML_JSON" ]; then
  ML_REPOS=$(echo "$ML_JSON" | jq -r '.data.children[].data | "\(.title) \(.selftext) \(.url)"' 2>/dev/null | extract_repos || true)
  
  for REPO in $ML_REPOS; do
    if ! is_new_repo "$REPO"; then
      echo "  + $REPO (r/MachineLearning)"
      NEW_REPOS+=("$REPO|r/MachineLearning")
      mark_repo_seen "$REPO"
      submit_to_queue "$REPO" "r/MachineLearning"
    fi
  done
fi

# ===== r/LocalLLaMA =====
echo ""
echo "[Subreddit] r/LocalLLaMA"
LOCAL_JSON=$(curl -s -A "Mozilla/5.0 (compatible; AIBot/1.0)" \
  "https://www.reddit.com/r/LocalLLaMA/hot.json?limit=25" 2>/dev/null || true)

if [ -n "$LOCAL_JSON" ]; then
  LOCAL_REPOS=$(echo "$LOCAL_JSON" | jq -r '.data.children[].data | "\(.title) \(.selftext) \(.url)"' 2>/dev/null | extract_repos || true)
  
  for REPO in $LOCAL_REPOS; do
    if ! is_new_repo "$REPO"; then
      echo "  + $REPO (r/LocalLLaMA)"
      NEW_REPOS+=("$REPO|r/LocalLLaMA")
      mark_repo_seen "$REPO"
      submit_to_queue "$REPO" "r/LocalLLaMA"
    fi
  done
fi

# ===== r/ArtificialIntelligence =====
echo ""
echo "[Subreddit] r/ArtificialIntelligence"
AI_JSON=$(curl -s -A "Mozilla/5.0 (compatible; AIBot/1.0)" \
  "https://www.reddit.com/r/ArtificialIntelligence/hot.json?limit=25" 2>/dev/null || true)

if [ -n "$AI_JSON" ]; then
  AI_REPOS=$(echo "$AI_JSON" | jq -r '.data.children[].data | "\(.title) \(.selftext) \(.url)"' 2>/dev/null | extract_repos || true)
  
  for REPO in $AI_REPOS; do
    if ! is_new_repo "$REPO"; then
      echo "  + $REPO (r/ArtificialIntelligence)"
      NEW_REPOS+=("$REPO|r/ArtificialIntelligence")
      mark_repo_seen "$REPO"
      submit_to_queue "$REPO" "r/ArtificialIntelligence"
    fi
  done
fi

# ===== r/OpenAI =====
echo ""
echo "[Subreddit] r/OpenAI"
OPENAI_JSON=$(curl -s -A "Mozilla/5.0 (compatible; AIBot/1.0)" \
  "https://www.reddit.com/r/OpenAI/hot.json?limit=15" 2>/dev/null || true)

if [ -n "$OPENAI_JSON" ]; then
  OPENAI_REPOS=$(echo "$OPENAI_JSON" | jq -r '.data.children[].data | "\(.title) \(.selftext) \(.url)"' 2>/dev/null | extract_repos || true)
  
  for REPO in $OPENAI_REPOS; do
    if ! is_new_repo "$REPO"; then
      echo "  + $REPO (r/OpenAI)"
      NEW_REPOS+=("$REPO|r/OpenAI")
      mark_repo_seen "$REPO"
      submit_to_queue "$REPO" "r/OpenAI"
    fi
  done
fi

# ===== r/LLM =====
echo ""
echo "[Subreddit] r/LLM"
LLM_JSON=$(curl -s -A "Mozilla/5.0 (compatible; AIBot/1.0)" \
  "https://www.reddit.com/r/LLM/hot.json?limit=15" 2>/dev/null || true)

if [ -n "$LLM_JSON" ]; then
  LLM_REPOS=$(echo "$LLM_JSON" | jq -r '.data.children[].data | "\(.title) \(.selftext) \(.url)"' 2>/dev/null | extract_repos || true)
  
  for REPO in $LLM_REPOS; do
    if ! is_new_repo "$REPO"; then
      echo "  + $REPO (r/LLM)"
      NEW_REPOS+=("$REPO|r/LLM")
      mark_repo_seen "$REPO"
      submit_to_queue "$REPO" "r/LLM"
    fi
  done
fi

# ===== Summary =====
echo ""
echo "=== Reddit Scraper Summary ==="
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

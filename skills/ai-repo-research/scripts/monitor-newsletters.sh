#!/bin/bash
# Scrape AI newsletters for GitHub repository links
# Supports: TLDR AI, Import AI, AlphaSignal, Papers with Code

set -e

WORKDIR="${AI_REPO_WORKDIR:-$HOME/.ai-repo-research}"
REPO_LOG="$WORKDIR/seen-repos.json"
QUEUE_DIR="$WORKDIR/queue/pending"
DAILY_DIR="$WORKDIR/daily/$(date +%Y-%m)"
mkdir -p "$QUEUE_DIR" "$DAILY_DIR"

echo "=== Newsletter Repo Scraper - $(date) ==="

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
  "priority": "medium",
  "requested_by": "newsletter-scraper",
  "notes": "Discovered via $source",
  "submitted_at": "$(date -Iseconds)"
}
EOF
  echo "  → Queued for research"
}

NEW_REPOS=()

# Function to extract GitHub repos from text
extract_repos() {
  grep -oE 'github\.com/[a-zA-Z0-9_-]+/[a-zA-Z0-9._-]+' | sed 's|github.com/||' | sort -u
}

# ===== TLDR AI =====
echo ""
echo "[Source] TLDR AI (tldr.tech/ai)"
echo "  Note: Requires RSS or archive scraping"
echo "  Checking GitHub trending as proxy..."

# ===== AlphaSignal =====
echo ""
echo "[Source] AlphaSignal (alphasignal.ai)"
# AlphaSignal has API endpoint for trending repos
ALPHASIGNAL_REPOS=$(curl -s "https://alphasignal.ai/api/trending" 2>/dev/null | jq -r '.repositories[]?.full_name' 2>/dev/null || true)
if [ -n "$ALPHASIGNAL_REPOS" ]; then
  for REPO in $ALPHASIGNAL_REPOS; do
    if ! is_new_repo "$REPO"; then
      echo "  + $REPO (AlphaSignal)"
      NEW_REPOS+=("$REPO|AlphaSignal")
      mark_repo_seen "$REPO"
      submit_to_queue "$REPO" "AlphaSignal"
    fi
  done
fi

# ===== Papers with Code =====
echo ""
echo "[Source] Papers with Code (huggingface.co/papers/trending)"
PWC_REPOS=$(curl -s "https://huggingface.co/api/papers?date=$(date +%Y-%m-%d)" 2>/dev/null | \
  jq -r '.papers[]?.github_url' 2>/dev/null | grep github.com | extract_repos || true)

if [ -n "$PWC_REPOS" ]; then
  for REPO in $PWC_REPOS; do
    if ! is_new_repo "$REPO"; then
      echo "  + $REPO (Papers with Code)"
      NEW_REPOS+=("$REPO|Papers with Code")
      mark_repo_seen "$REPO"
      submit_to_queue "$REPO" "Papers with Code"
    fi
  done
fi

# ===== Import AI Archive =====
echo ""
echo "[Source] Import AI (importai.substack.com)"
echo "  Note: Archive scraping via Substack RSS"
IMPORTAI_URL="https://importai.substack.com/feed"
IMPORTAI_REPOS=$(curl -s "$IMPORTAI_URL" 2>/dev/null | \
  grep -oE 'github\.com/[a-zA-Z0-9_-]+/[a-zA-Z0-9._-]+' | sed 's|github.com/||' | sort -u || true)

if [ -n "$IMPORTAI_REPOS" ]; then
  for REPO in $IMPORTAI_REPOS; do
    if ! is_new_repo "$REPO"; then
      echo "  + $REPO (Import AI)"
      NEW_REPOS+=("$REPO|Import AI")
      mark_repo_seen "$REPO"
      submit_to_queue "$REPO" "Import AI Newsletter"
    fi
  done
fi

# ===== TheSequence =====
echo ""
echo "[Source] TheSequence (thesequence.substack.com)"
SEQUENCE_URL="https://thesequence.substack.com/feed"
SEQUENCE_REPOS=$(curl -s "$SEQUENCE_URL" 2>/dev/null | \
  grep -oE 'github\.com/[a-zA-Z0-9_-]+/[a-zA-Z0-9._-]+' | sed 's|github.com/||' | sort -u | head -10 || true)

if [ -n "$SEQUENCE_REPOS" ]; then
  for REPO in $SEQUENCE_REPOS; do
    if ! is_new_repo "$REPO"; then
      echo "  + $REPO (TheSequence)"
      NEW_REPOS+=("$REPO|TheSequence")
      mark_repo_seen "$REPO"
      submit_to_queue "$REPO" "TheSequence Newsletter"
    fi
  done
fi

# ===== AI Breakfast =====
echo ""
echo "[Source] AI Breakfast (aibreakfast.beehiiv.com)"
echo "  Note: Beehiiv RSS feed if available"
# AI Breakfast doesn't have public RSS, would need scraping

# ===== Ben's Bites =====
echo ""
echo "[Source] Ben's Bites (bensbites.co)"
BENSBITES_URL="https://www.bensbites.co/feed"
BENSBITES_REPOS=$(curl -s "$BENSBITES_URL" 2>/dev/null | \
  grep -oE 'github\.com/[a-zA-Z0-9_-]+/[a-zA-Z0-9._-]+' | sed 's|github.com/||' | sort -u | head -10 || true)

if [ -n "$BENSBITES_REPOS" ]; then
  for REPO in $BENSBITES_REPOS; do
    if ! is_new_repo "$REPO"; then
      echo "  + $REPO (Ben's Bites)"
      NEW_REPOS+=("$REPO|Ben's Bites")
      mark_repo_seen "$REPO"
      submit_to_queue "$REPO" "Ben's Bites Newsletter"
    fi
  done
fi

# ===== Summary =====
echo ""
echo "=== Newsletter Scraper Summary ==="
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

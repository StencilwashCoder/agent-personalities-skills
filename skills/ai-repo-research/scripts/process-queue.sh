#!/bin/bash
# Process research requests from MinIO queue
# Pulls from research-queue/pending/, researches each, moves to results

set -e

WORKDIR="${AI_REPO_WORKDIR:-$HOME/.ai-repo-research}"
QUEUE_DIR="$WORKDIR/queue"

echo "=== Processing Research Queue ==="

# Check if MinIO is configured
if [ -z "$AWS_ENDPOINT_URL" ]; then
  echo "Error: MinIO not configured. Set AWS_ENDPOINT_URL, AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY"
  exit 1
fi

# Sync queue from MinIO
mkdir -p "$QUEUE_DIR/pending" "$QUEUE_DIR/processed"
echo "[Sync] Downloading queue from MinIO..."
aws s3 sync "s3://research-queue/pending/" "$QUEUE_DIR/pending/" \
  --endpoint-url="$AWS_ENDPOINT_URL" \
  --region="${AWS_REGION:-us-east-1}" 2>/dev/null || true

# Process each request
PROCESSED=0
for REQUEST_FILE in "$QUEUE_DIR/pending"/*.json; do
  [ -f "$REQUEST_FILE" ] || continue
  
  REPO=$(jq -r '.repo' "$REQUEST_FILE" 2>/dev/null)
  PRIORITY=$(jq -r '.priority // "medium"' "$REQUEST_FILE")
  REQUESTED_BY=$(jq -r '.requested_by // "unknown"' "$REQUEST_FILE")
  NOTES=$(jq -r '.notes // ""' "$REQUEST_FILE")
  
  if [ -z "$REPO" ] || [ "$REPO" = "null" ]; then
    echo "  ✗ Invalid request in $(basename "$REQUEST_FILE")"
    mv "$REQUEST_FILE" "$QUEUE_DIR/processed/"
    continue
  fi
  
  echo "[Processing] $REPO (priority: $PRIORITY, requested by: $REQUESTED_BY)"
  [ -n "$NOTES" ] && echo "  Notes: $NOTES"
  
  # Run research
  if "$(dirname "$0")/research-repo.sh" "$REPO"; then
    echo "  ✓ Research complete"
    PROCESSED=$((PROCESSED + 1))
    
    # Move to processed
    mv "$REQUEST_FILE" "$QUEUE_DIR/processed/$(basename "$REQUEST_FILE")"
    
    # Upload processed marker to MinIO
    echo '{"status": "completed", "processed_at": "'$(date -I)'"}' | \
      aws s3 cp - "s3://research-queue/processed/$(basename "$REQUEST_FILE")" \
      --endpoint-url="$AWS_ENDPOINT_URL" \
      --region="${AWS_REGION:-us-east-1}" 2>/dev/null || true
  else
    echo "  ✗ Research failed"
  fi
done

echo "=== Done ==="
echo "Processed: $PROCESSED requests"

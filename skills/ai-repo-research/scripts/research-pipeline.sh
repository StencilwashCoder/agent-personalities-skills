#!/bin/bash
# Continuous AI Repo Research Pipeline
# Processes up to 5 repos per hour from queue, or discovers new ones if empty
# Then regenerates the static site

set -e

WORKDIR="${AI_REPO_WORKDIR:-$HOME/.ai-repo-research}"
QUEUE_DIR="$WORKDIR/queue"
RESEARCH_DIR="$WORKDIR/research"
SCRIPT_DIR="$(dirname "$0")"

mkdir -p "$QUEUE_DIR/pending" "$QUEUE_DIR/processed" "$RESEARCH_DIR"

echo "=== AI Repo Research Pipeline ==="
echo "Time: $(date)"
echo ""

# Set MinIO env if not set
export AWS_ENDPOINT_URL="${AWS_ENDPOINT_URL:-https://s3.chainbytes.io}"
export AWS_ACCESS_KEY_ID="${AWS_ACCESS_KEY_ID:-chainbytes}"
export AWS_SECRET_ACCESS_KEY="${AWS_SECRET_ACCESS_KEY:-chainbytes2026}"
export AWS_REGION="${AWS_REGION:-us-east-1}"

PROCESSED=0
MAX_BATCH=5

# Step 1: Sync queue from MinIO
echo "[Step 1] Syncing queue from MinIO..."
python3 << 'PY' 2>/dev/null || echo "  (MinIO sync may have issues)"
import boto3, os, sys
s3 = boto3.client('s3', endpoint_url=os.environ['AWS_ENDPOINT_URL'],
    aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
    aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
    region_name=os.environ['AWS_REGION'])
try:
    os.makedirs(os.path.expanduser('~/.ai-repo-research/queue/pending'), exist_ok=True)
    resp = s3.list_objects_v2(Bucket='research-queue', Prefix='pending/')
    for obj in resp.get('Contents', []):
        if obj['Key'].endswith('.json'):
            local_path = os.path.expanduser(f'~/.ai-repo-research/queue/pending/{os.path.basename(obj["Key"])}')
            s3.download_file('research-queue', obj['Key'], local_path)
            print(f"  Downloaded: {obj['Key']}")
except Exception as e:
    print(f"  Queue sync error: {e}")
PY

# Step 2: Count pending requests
echo ""
echo "[Step 2] Checking queue..."
PENDING_COUNT=$(find "$QUEUE_DIR/pending" -name "*.json" 2>/dev/null | wc -l)
echo "  Pending requests: $PENDING_COUNT"

# Step 3: Process queue items first
if [ "$PENDING_COUNT" -gt 0 ]; then
  echo ""
  echo "[Step 3] Processing queue items..."
  
  for REQUEST_FILE in "$QUEUE_DIR/pending"/*.json; do
    [ -f "$REQUEST_FILE" ] || continue
    [ "$PROCESSED" -ge "$MAX_BATCH" ] && break
    
    REPO=$(jq -r '.repo' "$REQUEST_FILE" 2>/dev/null)
    PRIORITY=$(jq -r '.priority // "medium"' "$REQUEST_FILE")
    
    if [ -z "$REPO" ] || [ "$REPO" = "null" ]; then
      mv "$REQUEST_FILE" "$QUEUE_DIR/processed/"
      continue
    fi
    
    echo "  Researching [$PRIORITY]: $REPO"
    
    if "$SCRIPT_DIR/research-repo.sh" "$REPO" >/dev/null 2>&1; then
      PROCESSED=$((PROCESSED + 1))
      mv "$REQUEST_FILE" "$QUEUE_DIR/processed/"
      
      # Mark complete in MinIO
      REQUEST_BASENAME=$(basename "$REQUEST_FILE")
      python3 << PY
import boto3, os
s3 = boto3.client('s3', endpoint_url=os.environ['AWS_ENDPOINT_URL'],
    aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
    aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
    region_name=os.environ['AWS_REGION'])
key = "processed/${REQUEST_BASENAME}"
s3.put_object(Bucket='research-queue', Key=key, Body=b'{"status":"completed"}')
PY
    else
      echo "    Failed, will retry later"
    fi
  done
fi

# Step 4: If queue empty or batch not full, run discovery orchestrator
REMAINING=$((MAX_BATCH - PROCESSED))
if [ "$REMAINING" -gt 0 ]; then
  echo ""
  echo "[Step 4] Queue has $PROCESSED items, need to fill remaining $REMAINING slots..."
  
  # Run discovery orchestrator to fill queue with new repos
  "$SCRIPT_DIR/discover-all.sh"
  
  # Re-check queue after discovery
  PENDING_COUNT=$(find "$QUEUE_DIR/pending" -name "*.json" 2>/dev/null | wc -l)
  echo ""
  echo "[Step 4b] Queue now has $PENDING_COUNT pending items"
  
  # Process newly discovered items
  if [ "$PENDING_COUNT" -gt 0 ] && [ "$PROCESSED" -lt "$MAX_BATCH" ]; then
    for REQUEST_FILE in "$QUEUE_DIR/pending"/*.json; do
      [ -f "$REQUEST_FILE" ] || continue
      [ "$PROCESSED" -ge "$MAX_BATCH" ] && break
      
      REPO=$(jq -r '.repo' "$REQUEST_FILE" 2>/dev/null)
      [ -z "$REPO" ] && continue
      
      # Check if already researched
      OWNER=$(echo "$REPO" | cut -d'/' -f1)
      NAME=$(echo "$REPO" | cut -d'/' -f2)
      if [ -f "$RESEARCH_DIR/$OWNER/$NAME.md" ]; then
        mv "$REQUEST_FILE" "$QUEUE_DIR/processed/"
        continue
      fi
      
      echo "  Researching: $REPO"
      if "$SCRIPT_DIR/research-repo.sh" "$REPO" >/dev/null 2>&1; then
        PROCESSED=$((PROCESSED + 1))
        mv "$REQUEST_FILE" "$QUEUE_DIR/processed/"
        
        # Mark complete in MinIO
        REQUEST_BASENAME=$(basename "$REQUEST_FILE")
        python3 << PY 2>/dev/null
import boto3, os
s3 = boto3.client('s3', endpoint_url=os.environ['AWS_ENDPOINT_URL'],
    aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
    aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
    region_name=os.environ['AWS_REGION'])
key = "processed/${REQUEST_BASENAME}"
s3.put_object(Bucket='research-queue', Key=key, Body=b'{"status":"completed"}')
PY
      fi
    done
  fi
fi

# Step 5: Regenerate site
echo ""
echo "[Step 5] Regenerating site..."
if [ "$PROCESSED" -gt 0 ]; then
  "$SCRIPT_DIR/generate-site.sh" >/dev/null 2>&1
  echo "  ✅ Site updated with $PROCESSED new repos"
else
  echo "  No new repos to publish"
fi

# Step 6: Summary
echo ""
echo "=== Summary ==="
echo "Processed: $PROCESSED repos"
echo "Total researched: $(find "$RESEARCH_DIR" -name '*.md' 2>/dev/null | wc -l)"
echo "Next run: $(date -d '+1 hour' +'%H:%M' 2>/dev/null || echo 'in 1 hour')"
echo "Site: https://s3.chainbytes.io/research-site/index.html"
echo ""
echo "Done: $(date)"

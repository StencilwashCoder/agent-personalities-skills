#!/bin/bash
# Submit a research request to the queue
# Usage: submit-request.sh <owner/repo> [priority] [notes]

REPO="$1"
PRIORITY="${2:-medium}"
NOTES="${3:-}"
REQUESTED_BY="${USER:-unknown}"

if [ -z "$REPO" ]; then
  echo "Usage: $0 <owner/repo> [priority:high|medium|low] [notes]"
  exit 1
fi

if [ -z "$AWS_ENDPOINT_URL" ]; then
  echo "Error: MinIO not configured"
  exit 1
fi

TIMESTAMP=$(date +%s)
REQUEST_FILE="/tmp/${TIMESTAMP}-$(echo "$REPO" | tr '/' '-').json"

cat > "$REQUEST_FILE" << EOF
{
  "repo": "$REPO",
  "priority": "$PRIORITY",
  "requested_by": "$REQUESTED_BY",
  "notes": "$NOTES",
  "submitted_at": "$(date -Iseconds)"
}
EOF

echo "Submitting research request for: $REPO"
aws s3 cp "$REQUEST_FILE" "s3://research-queue/pending/$(basename "$REQUEST_FILE")" \
  --endpoint-url="$AWS_ENDPOINT_URL" \
  --region="${AWS_REGION:-us-east-1}"

rm "$REQUEST_FILE"
echo "✅ Request submitted"

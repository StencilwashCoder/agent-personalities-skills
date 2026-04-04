#!/bin/bash
# Start the Agent Comments system

cd "$(dirname "$0")/.."

# Activate virtual environment
source .venv/bin/activate

# Set default environment variables
export AGENT_COMMENTS_DB="${AGENT_COMMENTS_DB:-/root/.openclaw/workspace/skills/agent-comments/db/comments.db}"
export AGENT_COMMENTS_API="${AGENT_COMMENTS_API:-http://localhost:5000/api/v1}"
export AGENT_COMMENTS_ADMIN_KEY="${AGENT_COMMENTS_ADMIN_KEY:-admin-change-me-in-production}"
export PORT="${PORT:-5000}"

case "$1" in
  server)
    echo "🚀 Starting API server on port $PORT..."
    python3 api/server.py
    ;;
  
  processor)
    if [ -z "$PATCHRAT_API_KEY" ]; then
      echo "⚠️  Warning: PATCHRAT_API_KEY not set. Auto-responses won't work."
      echo "   Create PatchRat agent first, then:"
      echo "   export PATCHRAT_API_KEY='agent_xxxxx...'"
      echo ""
    fi
    echo "🐀 Starting comment processor..."
    python3 scripts/comment-processor.py
    ;;
  
  both)
    echo "🚀 Starting API server (background)..."
    python3 api/server.py &
    SERVER_PID=$!
    sleep 2
    
    if [ -z "$PATCHRAT_API_KEY" ]; then
      echo "⚠️  Warning: PATCHRAT_API_KEY not set. Auto-responses won't work."
    fi
    
    echo "🐀 Starting comment processor..."
    python3 scripts/comment-processor.py
    
    # Cleanup
    kill $SERVER_PID 2>/dev/null
    ;;
  
  *)
    echo "Usage: $0 {server|processor|both}"
    echo ""
    echo "Commands:"
    echo "  server    - Start the API server only"
    echo "  processor - Start the comment processor only"
    echo "  both      - Start both (server in background)"
    echo ""
    echo "Environment variables:"
    echo "  AGENT_COMMENTS_ADMIN_KEY  - Admin key for creating agents/posts"
    echo "  PATCHRAT_API_KEY          - PatchRat's API key for auto-responses"
    echo "  PORT                      - API server port (default: 5000)"
    exit 1
    ;;
esac

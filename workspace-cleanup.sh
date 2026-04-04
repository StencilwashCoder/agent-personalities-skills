#!/bin/bash
# workspace-cleanup.sh - Archive old script iterations and clean workspace clutter
# Created: $(date +%Y-%m-%d)
# Purpose: Keep workspace tidy by archiving duplicate/trial scripts

set -e

ARCHIVE_DIR="/root/.openclaw/workspace/archive/$(date +%Y-%m-%d)"
LOG_FILE="/root/.openclaw/workspace/memory/workspace-cleanup-log.md"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log() {
    echo -e "${GREEN}[$(date +%H:%M:%S)]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Create archive directory
mkdir -p "$ARCHIVE_DIR"
log "Created archive directory: $ARCHIVE_DIR"

# Files to archive (old autoresearch iterations)
ARCHIVE_PATTERNS=(
    "autoresearch-laddr-v2.py"
    "autoresearch-laddr-venv.py"
    "autoresearch-laddr-pip.py"
    "autoresearch-laddr-full.py"
    "autoresearch-laddr-cpu.py"
    "autoresearch-laddr.py"
    "autoresearch-laddr-final.py"
    "autoresearch-polling.py"
    "autoresearch-polling-final.py"
    "autoresearch-curl.py"
    "autoresearch-redis.py"
    "autoresearch-file-poll.py"
    "autoresearch-minio.py"
    "autoresearch-minio-results.py"
)

ARCHIVED_COUNT=0

for pattern in "${ARCHIVE_PATTERNS[@]}"; do
    if [ -f "/root/.openclaw/workspace/$pattern" ]; then
        cp "/root/.openclaw/workspace/$pattern" "$ARCHIVE_DIR/"
        rm "/root/.openclaw/workspace/$pattern"
        log "Archived: $pattern"
        ((ARCHIVED_COUNT++))
    fi
done

# Keep these working versions:
# - autoresearch-loop.py (main polling script)
# - autoresearch/ directory (full training setup)

# Log the cleanup
cat >> "$LOG_FILE" << EOF

## Workspace Cleanup - $(date +%Y-%m-%d)

**Archived $ARCHIVED_COUNT files to:** \`$ARCHIVE_DIR\`

### Files Moved:
EOF

for pattern in "${ARCHIVE_PATTERNS[@]}"; do
    if [ -f "$ARCHIVE_DIR/$pattern" ]; then
        echo "- \`$pattern\`" >> "$LOG_FILE"
    fi
done

cat >> "$LOG_FILE" << EOF

### Files Preserved:
- \`autoresearch-loop.py\` - Main polling script (keep)
- \`autoresearch/\` directory - Full training setup (keep)

### Result:
Workspace root cleaned. Reduced from 15+ autoresearch files to 2.
EOF

log "====================================="
log "Cleanup complete!"
log "Archived: $ARCHIVED_COUNT files"
log "Location: $ARCHIVE_DIR"
log "Log: $LOG_FILE"
log "====================================="

# Show disk usage
DU=$(du -sh "$ARCHIVE_DIR" | cut -f1)
log "Archive size: $DU"

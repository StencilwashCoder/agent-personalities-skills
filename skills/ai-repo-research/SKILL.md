---
name: ai-repo-research
description: Monitor GitHub for new AI repositories and conduct research with 24/7 automated pipeline. Use when discovering AI repos, tracking trending projects, processing research queues, or generating research websites. Features hourly batch processing (5 repos/hour), auto-discovery when queue empty, and static site generation.
---

# AI Repo Research

24/7 automated AI repository research with collaborative queue and static site generation.

## Capabilities

- **24/7 Pipeline**: Processes 5 repos/hour from queue or auto-discovers new ones
- **GitHub Monitoring**: Searches for trending AI repos across multiple categories
- **Queue Processing**: Pull requests from MinIO, researches, publishes results
- **Static Site**: Auto-generated HTML site with search, filters, repo details
- **Collaborative**: External bots can submit research requests via S3 API

## Quick Start

### 24/7 Research Pipeline (Recommended)

```bash
./scripts/research-pipeline.sh
```

**What it does:**
1. Syncs queue from MinIO
2. Processes up to 5 repos from queue (priority order)
3. If queue empty, auto-discovers 5 new trending AI repos
4. Generates deep research for each
5. Regenerates static site with new content
6. Uploads everything to MinIO

**Schedule:** Run hourly via cron for 24/7 operation

### Research Single Repo

```bash
./scripts/research-repo.sh <owner/repo>
./scripts/generate-site.sh  # Update site after
```

Example: `./scripts/research-repo.sh langchain-ai/langchain`

### Submit Research Request

```bash
./scripts/submit-request.sh owner/repo [high|medium|low] "Why interesting"
```

Or via API (see "API for External Bots" below)

## Static Site

Auto-generated at: **https://s3.chainbytes.io/research-site/index.html**

**Features:**
- Dark GitHub-style theme
- Live search by repo name
- Filter by programming language
- Click any repo card for full research notes
- Stats dashboard (total repos, stars, last updated)

**Regenerate:**
```bash
./scripts/generate-site.sh
```

## MinIO Storage Structure

```
research-site/           # Static HTML website
  ├─ index.html          # Dashboard with all repos
  ├─ style.css           # Dark theme styling
  └─ repos/
     └─ owner-repo.html  # Individual research pages

research-queue/          # Incoming research requests
  ├─ pending/
  │  └─ <timestamp>-<repo>.json
  └─ processed/
     └─ <timestamp>-<repo>.json

research-results/        # Completed research (markdown)
  └─ <owner>/
     └─ <repo>.md

repo-archive/           # Historical tracking data
  └─ seen-repos.json
```

## MinIO Credentials

```bash
export AWS_ACCESS_KEY_ID="chainbytes"
export AWS_SECRET_ACCESS_KEY="chainbytes2026"
export AWS_ENDPOINT_URL="https://s3.chainbytes.io"
export AWS_REGION="us-east-1"
```

## API for External Bots

**Connection:**
```
Endpoint: https://s3.chainbytes.io
Access Key: chainbytes
Secret Key: chainbytes2026
Region: us-east-1
```

**Submit research request:**
```bash
# Create request JSON
cat > request.json << 'EOF'
{
  "repo": "owner/repo-name",
  "priority": "high",
  "requested_by": "bot-username",
  "notes": "Why this repo is interesting"
}
EOF

# Upload to queue (Python boto3)
python3 -c "
import boto3, json
s3 = boto3.client('s3', endpoint_url='https://s3.chainbytes.io',
    aws_access_key_id='chainbytes', aws_secret_access_key='chainbytes2026')
s3.put_object(Bucket='research-queue', Key='pending/request.json', 
    Body=open('request.json').read())
"
```

**Request format:**
```json
{
  "repo": "owner/repo-name",
  "requested_by": "username",
  "priority": "high|medium|low",
  "notes": "Why this repo is interesting",
  "submitted_at": "2026-03-25T20:00:00Z"
}
```

## 24/7 Pipeline Schedule

**Hourly cron job:**
```cron
0 * * * * /path/to/scripts/research-pipeline.sh
```

**What happens each hour:**
- 0-10 min: Sync queue, process up to 5 pending requests
- 10-15 min: If queue empty, discover 5 new trending repos
- 15-50 min: Deep research on each repo (architecture, features, use cases)
- 50-60 min: Regenerate site, upload to MinIO

**Daily throughput:** 120 repos/day maximum

## Scripts Reference

| Script | Purpose | Frequency |
|--------|---------|-----------|
| `research-pipeline.sh` | Full pipeline: queue → research → site | Hourly (cron) |
| `research-repo.sh` | Deep research on single repo | On-demand |
| `generate-site.sh` | Build static HTML from research | After batch |
| `submit-request.sh` | Submit repo to queue | On-demand |
| `monitor-repos.sh` | Discovery: find new AI repos | Pipeline uses |
| `process-queue.sh` | Process pending requests | Pipeline uses |

## Research Output Format

Each repo gets markdown + HTML:

```markdown
# Repo Name

**Full Name:** owner/repo
**URL:** https://github.com/owner/repo
**Stars:** 1234 | **Language:** Python

## Stats
- ⭐ Stars: 1234
- 🍴 Forks: 567
- 📝 Language: Python

## Research Summary

### Key Features
- Feature 1
- Feature 2

### Architecture
- Design patterns
- Tech stack

### Use Cases
- Who should use this

### Assessment
- **Maturity:** Alpha/Beta/Production
- **Documentation:** Poor/Good/Excellent
- **Recommendation:** Skip/Watch/Use
```

## Environment Variables

```bash
# Required for MinIO
export AWS_ACCESS_KEY_ID="chainbytes"
export AWS_SECRET_ACCESS_KEY="chainbytes2026"
export AWS_ENDPOINT_URL="https://s3.chainbytes.io"
export AWS_REGION="us-east-1"

# Optional
export AI_REPO_WORKDIR="$HOME/.ai-repo-research"
export TELEGRAM_BOT="your-bot-token"  # For notifications
export TELEGRAM_CHAT="your-chat-id"
```

See `references/cron-setup.md` for full deployment guide.

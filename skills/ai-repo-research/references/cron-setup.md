# Cron Setup for AI Repo Research

## Recommended Schedule

### Daily Repo Monitoring
```
# 8:00 AM ET - Morning digest
0 8 * * * /path/to/skills/ai-repo-research/scripts/monitor-repos.sh

# 6:00 PM ET - Evening digest  
0 18 * * * /path/to/skills/ai-repo-research/scripts/monitor-repos.sh
```

### Queue Processing
```
# Every hour during business hours
0 9-18 * * 1-5 /path/to/skills/ai-repo-research/scripts/process-queue.sh

# Or continuously every 15 minutes
*/15 * * * * /path/to/skills/ai-repo-research/scripts/process-queue.sh
```

### Research Backups
```
# Daily backup to MinIO
0 2 * * * aws s3 sync ~/.ai-repo-research/ s3://repo-archive/ --endpoint-url=https://s3.chainbytes.io
```

## Environment Setup

Add to crontab or ~/.bashrc:
```bash
export AI_REPO_WORKDIR="$HOME/.ai-repo-research"
export AWS_ACCESS_KEY_ID="chainbytes"
export AWS_SECRET_ACCESS_KEY="chainbytes2026"
export AWS_ENDPOINT_URL="https://s3.chainbytes.io"
export AWS_REGION="us-east-1"
```

## OpenClaw Integration

For OpenClaw scheduled jobs:
```json
{
  "name": "AI Repo Monitor - Morning",
  "schedule": "0 8 * * *",
  "timezone": "America/New_York",
  "command": "skills/ai-repo-research/scripts/monitor-repos.sh"
}
```

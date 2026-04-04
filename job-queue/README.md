# AI Job Queue System

Real-time distributed AI job queue using MinIO (S3) as the message bus. Your local LM Studio instance processes jobs from the cloud.

## Architecture

```
┌─────────────────┐      ┌──────────────────┐      ┌─────────────────┐
│   Cloud (Me)    │      │  chainbytes.io   │      │  Your Machine   │
│                 │◄────►│  (MinIO S3)      │◄────►│  (LM Studio)    │
│  - Submit jobs  │      │                  │      │  - Worker polls │
│  - Get results  │      │ s3://ai-jobs/    │      │  - Runs on GPU  │
│                 │      │   /incoming/     │      │  - Writes back  │
│                 │      │   /processing/   │      │                 │
│                 │      │   /completed/    │      │                 │
└─────────────────┘      └──────────────────┘      └─────────────────┘
```

## Quick Start

### 1. On Your Machine (with LM Studio)

```bash
# Clone/navigate to job-queue directory
cd job-queue

# Build worker image
docker build -t ai-job-worker:latest .

# Or use the helper
./ai-job build

# Start worker (edit docker-compose.yml first for your LM Studio URL)
docker-compose up -d

# Or use helper
./ai-job up
```

**Before starting**, edit `docker-compose.yml`:
```yaml
environment:
  - LMSTUDIO_URL=http://your-lm-studio-ip:1234  # Change this
```

If LM Studio is on the same machine:
- Linux: `http://host.docker.internal:1234` (with `extra_hosts` in compose)
- Mac/Windows: `http://host.docker.internal:1234`

### 2. In LM Studio

1. Load your model(s)
2. Click "Start Server"
3. Note the port (default: 1234)

### 3. Submit Jobs (from anywhere)

```bash
# Submit a simple job
./ai-job submit -p "Write a Python function to reverse a string" --priority 1

# Submit and wait for result
./ai-job submit -p "Explain Docker containers" --priority 1 --wait

# With specific model and parameters
./ai-job submit \
  -p "Refactor this code" \
  -m "qwen-2.5-coder" \
  --temp 0.3 \
  --tokens 2048 \
  --priority 1 \
  --wait
```

### 4. Check Status

```bash
# Queue status
./ai-job status

# Get result
./ai-job result <job-id>

# View worker logs
./ai-job logs
```

## Job Schema

```json
{
  "id": "uuid-string",
  "priority": 1,
  "model": "llama-3.1-70b",
  "system_prompt": "You are a coding assistant...",
  "user_prompt": "Write a function...",
  "parameters": {
    "temperature": 0.7,
    "max_tokens": 4096,
    "top_p": 1.0,
    "frequency_penalty": 0,
    "presence_penalty": 0
  },
  "skills": [
    {"bucket": "skills", "key": "python-best-practices.md"}
  ],
  "context_files": [
    {"bucket": "context", "key": "project-docs/api.md", "type": "markdown"}
  ],
  "streaming": false,
  "callback_url": "https://...",
  "metadata": {"source": "cli"},
  "created_at": "2026-03-26T...",
  "requested_by": "patchrat"
}
```

## Priority Levels

| Priority | Use Case |
|----------|----------|
| 1 | Critical - Blocked on this |
| 2-3 | High - User waiting |
| 4-5 | Normal - Default |
| 6-7 | Low - Batch work |
| 8-10 | Background - Overnight jobs |

## Environment Variables

### Worker
```bash
S3_ENDPOINT=https://s3.chainbytes.io
S3_ACCESS_KEY=chainbytes
S3_SECRET_KEY=chainbytes2026
S3_REGION=us-east-1
JOBS_BUCKET=ai-jobs
LMSTUDIO_URL=http://localhost:1234
LMSTUDIO_API_KEY=optional
WORKER_ID=worker-1
POLL_INTERVAL=1.0
MAX_JOBS=1000
```

### CLI
```bash
# Same S3 config as worker
export S3_ENDPOINT=https://s3.chainbytes.io
export S3_ACCESS_KEY=chainbytes
export S3_SECRET_KEY=chainbytes2026
export JOBS_BUCKET=ai-jobs
```

## API Usage (Python)

```python
from submit_job import submit_job, wait_for_result

# Submit
job_id = submit_job(
    user_prompt="Analyze this code",
    system_prompt="You are a senior engineer...",
    priority=1,
    model="qwen-2.5-coder",
    skills=[
        {"bucket": "skills", "key": "code-review.md"}
    ]
)

# Wait for result
result = wait_for_result(job_id)
print(result['result']['content'])
```

## Docker Deployment

```bash
# Build
docker build -t ai-job-worker:latest .

# Run
docker run -d \
  --name ai-worker \
  --restart unless-stopped \
  -e LMSTUDIO_URL=http://host.docker.internal:1234 \
  -e S3_ENDPOINT=https://s3.chainbytes.io \
  ai-job-worker:latest

# Or use docker-compose
docker-compose up -d
```

## Monitoring

```bash
# Watch logs
docker-compose logs -f

# Queue depth (run anywhere with S3 access)
aws s3 ls s3://ai-jobs/incoming/ --endpoint-url https://s3.chainbytes.io | wc -l
```

## Troubleshooting

**Worker can't connect to LM Studio:**
- Check LM Studio is running and server is started
- Verify `LMSTUDIO_URL` in docker-compose.yml
- Try `network_mode: host` if on Linux

**Jobs not processing:**
- Check worker logs: `docker-compose logs`
- Verify S3 credentials
- Check `incoming/` folder has jobs

**Results not saving:**
- Check S3 permissions
- Verify bucket exists

## Future Enhancements

- [ ] Scheduled/batch jobs
- [ ] Multiple workers with load balancing
- [ ] Job progress streaming
- [ ] Automatic retries
- [ ] Cost tracking per job
- [ ] Priority inheritance for child jobs

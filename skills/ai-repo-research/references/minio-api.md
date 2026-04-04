# MinIO API Reference for AI Repo Research

## Connection Details

```
S3 Endpoint: https://s3.chainbytes.io
Web Console: https://minio.chainbytes.io
Access Key: chainbytes
Secret Key: chainbytes2026
Region: us-east-1
```

## Bucket Structure

### research-queue/
Incoming research requests land here.

```bash
# Structure
s3://research-queue/
├── pending/           # Unprocessed requests
│   └── <timestamp>-<repo>.json
└── processed/         # Completed requests
    └── <timestamp>-<repo>.json
```

### research-results/
Completed research reports.

```bash
# Structure
s3://research-results/
├── <owner>/
│   └── <repo>.md
└── index.json         # Searchable index
```

### repo-archive/
Historical tracking data.

```bash
# Structure
s3://repo-archive/
├── seen-repos.json
└── daily/
    └── YYYY-MM/
        └── DD.md
```

## API Examples

### Submit Research Request (CLI)
```bash
aws s3 cp request.json s3://research-queue/pending/ \
  --endpoint-url=https://s3.chainbytes.io
```

### Submit Research Request (curl)
```bash
curl -X PUT \
  https://s3.chainbytes.io/research-queue/pending/request.json \
  -H "Content-Type: application/json" \
  -d @request.json
```

### List Pending Requests
```bash
aws s3 ls s3://research-queue/pending/ \
  --endpoint-url=https://s3.chainbytes.io
```

### Download Research Result
```bash
aws s3 cp s3://research-results/owner/repo.md ./ \
  --endpoint-url=https://s3.chainbytes.io
```

## Request JSON Format

```json
{
  "repo": "owner/repo-name",
  "priority": "high|medium|low",
  "requested_by": "username",
  "notes": "Why this repo is interesting",
  "submitted_at": "2026-03-25T20:00:00Z"
}
```

## Bot Integration

For bots connecting to this system:

**Python (boto3):**
```python
import boto3

s3 = boto3.client('s3',
    endpoint_url='https://s3.chainbytes.io',
    aws_access_key_id='chainbytes',
    aws_secret_access_key='chainbytes2026',
    region_name='us-east-1'
)

# Submit request
s3.put_object(
    Bucket='research-queue',
    Key='pending/my-request.json',
    Body=json.dumps({"repo": "foo/bar"})
)
```

**Node.js (@aws-sdk/client-s3):**
```javascript
import { S3Client } from '@aws-sdk/client-s3';

const s3 = new S3Client({
  endpoint: 'https://s3.chainbytes.io',
  credentials: {
    accessKeyId: 'chainbytes',
    secretAccessKey: 'chainbytes2026'
  },
  region: 'us-east-1'
});
```

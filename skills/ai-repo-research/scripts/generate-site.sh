#!/bin/bash
# Generate compact grid-based HTML site from research markdown
# Outputs to site/ directory, uploads to MinIO

set -e

WORKDIR="${AI_REPO_WORKDIR:-$HOME/.ai-repo-research}"
RESEARCH_DIR="$WORKDIR/research"
SITE_DIR="$WORKDIR/site"

echo "=== Generating Compact Research Site ==="

# Create site structure
mkdir -p "$SITE_DIR/repos"

# Generate CSS with compact grid layout
cat > "$SITE_DIR/style.css" << 'CSS'
:root {
  --bg: #0d1117;
  --bg-secondary: #161b22;
  --bg-tertiary: #21262d;
  --border: #30363d;
  --text: #c9d1d9;
  --text-secondary: #8b949e;
  --text-muted: #6e7681;
  --accent: #58a6ff;
  --accent-hover: #79b8ff;
  --success: #238636;
  --warning: #d29922;
  --danger: #da3633;
}

* { box-sizing: border-box; margin: 0; padding: 0; }

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
  background: var(--bg);
  color: var(--text);
  line-height: 1.5;
  max-width: 1400px;
  margin: 0 auto;
  padding: 20px;
}

header {
  border-bottom: 1px solid var(--border);
  padding-bottom: 16px;
  margin-bottom: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 12px;
}

header h1 { color: var(--accent); font-size: 1.5rem; }
header p { color: var(--text-secondary); font-size: 0.875rem; }

.stats {
  display: flex;
  gap: 24px;
}

.stat { text-align: center; }
.stat-value { font-size: 1.25rem; font-weight: bold; color: var(--accent); }
.stat-label { font-size: 0.75rem; color: var(--text-secondary); }

.controls {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
  flex-wrap: wrap;
  align-items: center;
}

.controls input, .controls select {
  padding: 8px 12px;
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: 6px;
  color: var(--text);
  font-size: 0.875rem;
}

.controls input { min-width: 200px; flex: 1; }
.controls input:focus, .controls select:focus {
  outline: none;
  border-color: var(--accent);
}

.repo-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 12px;
}

.repo-card {
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 14px;
  transition: all 0.15s ease;
  cursor: pointer;
}

.repo-card:hover {
  border-color: var(--accent);
  background: var(--bg-tertiary);
}

.repo-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 8px;
  margin-bottom: 6px;
}

.repo-name {
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--accent);
  text-decoration: none;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.repo-name:hover { text-decoration: underline; }

.repo-badges {
  display: flex;
  gap: 4px;
  flex-shrink: 0;
}

.badge {
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 0.7rem;
  font-weight: 500;
  white-space: nowrap;
}

.badge-stars { background: #f1c40f20; color: #f1c40f; }
.badge-lang { background: var(--bg-tertiary); color: var(--text-secondary); }
.badge-status { background: var(--success); color: white; font-size: 0.65rem; }

.repo-desc {
  color: var(--text-secondary);
  font-size: 0.8rem;
  line-height: 1.4;
  margin-bottom: 8px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.repo-meta {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.topic-tag {
  padding: 2px 8px;
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: 12px;
  font-size: 0.7rem;
  color: var(--text-muted);
}

.no-results {
  text-align: center;
  padding: 40px;
  color: var(--text-secondary);
  grid-column: 1 / -1;
}

footer {
  margin-top: 30px;
  padding-top: 16px;
  border-top: 1px solid var(--border);
  text-align: center;
  color: var(--text-secondary);
  font-size: 0.8rem;
}

/* Repo Detail Page */
.back-link {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  color: var(--accent);
  text-decoration: none;
  margin-bottom: 16px;
  font-size: 0.875rem;
}

.back-link:hover { text-decoration: underline; }

.repo-detail h1 { font-size: 1.5rem; margin-bottom: 4px; }
.repo-detail .subtitle {
  color: var(--text-secondary);
  margin-bottom: 16px;
  font-size: 0.875rem;
}

.repo-detail .subtitle a {
  color: var(--accent);
  text-decoration: none;
}

.repo-detail .subtitle a:hover { text-decoration: underline; }

.section {
  background: var(--bg-secondary);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 16px;
  margin: 16px 0;
}

.section h2 {
  font-size: 1rem;
  margin-bottom: 12px;
  color: var(--text);
  border-bottom: 1px solid var(--border);
  padding-bottom: 8px;
}

.markdown-content h1 { font-size: 1.25rem; border-bottom: 1px solid var(--border); padding-bottom: 6px; }
.markdown-content h2 { font-size: 1.1rem; margin-top: 16px; }
.markdown-content h3 { font-size: 1rem; color: var(--accent); }
.markdown-content p { margin-bottom: 10px; color: var(--text-secondary); font-size: 0.875rem; }
.markdown-content ul { margin-left: 20px; margin-bottom: 12px; }
.markdown-content li { margin: 4px 0; color: var(--text-secondary); font-size: 0.875rem; }
.markdown-content code { background: var(--bg); padding: 2px 4px; border-radius: 3px; font-size: 0.8rem; }
.markdown-content a { color: var(--accent); }
.markdown-content strong { color: var(--text); }
CSS

echo "[CSS] Generated compact style.css"

# Start building repo data JSON for JavaScript filtering
REPO_JSON="$SITE_DIR/repos.json"
echo "[" > "$REPO_JSON"

# Generate repo data
FIRST=true
find "$RESEARCH_DIR" -name "*.md" | while read -r MD_FILE; do
  FILENAME=$(basename "$MD_FILE" .md)
  
  # Extract fields from markdown
  NAME=$(grep -m1 "^# " "$MD_FILE" | sed 's/^# //' || echo "$FILENAME")
  URL=$(grep "^\*\*URL:\*\*" "$MD_FILE" | head -1 | sed -E 's/.*URL:\*\* ?//' | sed 's/[[:space:]]*$//' || echo "#")
  
  # Extract stars from the ## Stats section
  STARS=$(awk '/^## Stats/{found=1} found && /⭐ Stars:/{match($0, /⭐ Stars: ([0-9]+)/, arr); print arr[1]; exit}' "$MD_FILE")
  [ -z "$STARS" ] && STARS=$(grep "^- ⭐ Stars:" "$MD_FILE" | grep -oP '[0-9]+' | head -1 || echo "0")
  
  # Extract language
  LANG=$(awk '/^## Stats/{found=1} found && /📝 Language:/{for(i=3;i<=NF;i++)printf "%s ", $i; exit}' "$MD_FILE" | sed 's/[[:space:]]*$//')
  [ -z "$LANG" ] && LANG=$(grep "^- 📝 Language:" "$MD_FILE" | sed 's/.*Language: //' | head -1 || echo "Unknown")
  
  # Extract created date for sorting
  CREATED=$(awk '/^## Stats/{found=1} found && /📅 Created:/{print $3; exit}' "$MD_FILE")
  
  # Get description from ## Description section
  DESC=$(awk '/^## Description/{found=1; next} found && /^##/{exit} found && NF{print; exit}' "$MD_FILE" | sed 's/"/\\"/g' || echo "")
  
  # Get first few topics as tags
  TOPICS=$(grep "^## Topics" -A1 "$MD_FILE" | tail -1 | tr ',' '\n' | head -3 | sed 's/[[:space:]]//g' | tr '\n' ',' | sed 's/,$//')
  
  # Clean up
  LANG=$(echo "$LANG" | tr -d '\r\n')
  DESC=$(echo "$DESC" | tr -d '\r\n' | cut -c1-120)
  
  # Extract owner/repo for URL
  REPO_PATH=$(echo "$URL" | sed 's|https://github.com/||' | sed 's|/$||' | sed 's/[[:space:]]//g')
  SAFE_NAME=$(echo "$REPO_PATH" | tr '/' '-')
  
  # Generate detail page
  REPO_HTML="$SITE_DIR/repos/${SAFE_NAME}.html"
  
  cat > "$REPO_HTML" << REPO
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>$NAME - AI Repo Research</title>
  <link rel="stylesheet" href="../style.css">
</head>
<body class="repo-detail">
  <a href="../index.html" class="back-link">← Back to all repos</a>
  
  <h1>$NAME</h1>
  <p class="subtitle"><a href="$URL" target="_blank">$URL</a></p>
REPO

  # Stats section
  cat >> "$REPO_HTML" << REPO
  
  <div class="section">
    <h2>📊 Stats</h2>
REPO
  
  awk '/^## Stats/{found=1} found && /^## [^S]/{exit} found' "$MD_FILE" | grep "^-" | while read -r line; do
    CLEAN_LINE=$(echo "$line" | sed 's/^- //' | sed 's/^[⭐🍴📝📅🔄🏷️] //')
    echo "    <p>$CLEAN_LINE</p>" >> "$REPO_HTML"
  done
  
  cat >> "$REPO_HTML" << REPO
  </div>
REPO

  # Description
  if [ -n "$DESC" ]; then
    cat >> "$REPO_HTML" << REPO
  
  <div class="section">
    <h2>📝 Description</h2>
    <p>$DESC</p>
  </div>
REPO
  fi

  # Research Notes
  cat >> "$REPO_HTML" << REPO
  
  <div class="section">
    <h2>🔬 Research Notes</h2>
    <div class="markdown-content">
REPO

  awk '/^## /{found=1} found' "$MD_FILE" | while IFS= read -r line; do
    [ -z "$line" ] && continue
    line=$(echo "$line" | sed -E 's/^#### (.*)/<h4>\1<\/h4>/')
    line=$(echo "$line" | sed -E 's/^### (.*)/<h3>\1<\/h3>/')
    line=$(echo "$line" | sed -E 's/^## (.*)/<h2>\1<\/h2>/')
    line=$(echo "$line" | sed -E 's/\*\*([^*]+)\*\*/<strong>\1<\/strong>/g')
    line=$(echo "$line" | sed -E 's/`([^`]+)`/<code>\1<\/code>/g')
    line=$(echo "$line" | sed -E 's/\[([^\]]+)\]\(([^)]+)\)/<a href="\2" target="_blank">\1<\/a>/g')
    if echo "$line" | grep -qE "^- "; then
      line=$(echo "$line" | sed -E 's/^- (.*)/<li>\1<\/li>/')
    fi
    if ! echo "$line" | grep -qE "^<[ahp]"; then
      line="<p>$line</p>"
    fi
    echo "      $line" >> "$REPO_HTML"
  done

  cat >> "$REPO_HTML" << REPO
    </div>
  </div>
  
  <footer>
    <p>Generated: $(date -I)</p>
  </footer>
</body>
</html>
REPO

  # Append to JSON
  if [ "$FIRST" = true ]; then
    FIRST=false
  else
    echo "," >> "$REPO_JSON"
  fi
  
  cat >> "$REPO_JSON" << JSON
  {
    "name": "$NAME",
    "safeName": "$SAFE_NAME",
    "url": "$URL",
    "stars": ${STARS:-0},
    "language": "${LANG:-Unknown}",
    "description": "$DESC",
    "created": "${CREATED:-}",
    "topics": "$TOPICS"
  }
JSON
  
  echo "  Generated: $SAFE_NAME.html ($STARS ⭐)"
done

echo "]" >> "$REPO_JSON"

# Count repos and stars for header
REPO_COUNT=$(find "$RESEARCH_DIR" -name "*.md" 2>/dev/null | wc -l)
TOTAL_STARS=$(cat "$REPO_JSON" | grep -oP '"stars": [0-9]+' | grep -oP '[0-9]+' | awk '{sum+=$1} END {print sum}')

# Generate index.html using external Python script to avoid bash escaping hell
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
python3 "$SCRIPT_DIR/generate-index.py" "$REPO_COUNT" "${TOTAL_STARS:-0}" "$SITE_DIR/index.html"

echo "[HTML] Generated compact index.html"

# Upload to MinIO
echo "[Upload] Syncing to MinIO..."
python3 << 'PYTHON'
import boto3, os, json

endpoint = os.environ.get('AWS_ENDPOINT_URL', 'https://s3.chainbytes.io')
key = os.environ.get('AWS_ACCESS_KEY_ID', 'chainbytes')
secret = os.environ.get('AWS_SECRET_ACCESS_KEY', 'chainbytes2026')
region = os.environ.get('AWS_REGION', 'us-east-1')
site_dir = os.path.expanduser('~/.ai-repo-research/site')

try:
    s3 = boto3.client('s3', endpoint_url=endpoint, aws_access_key_id=key, 
                      aws_secret_access_key=secret, region_name=region)
    
    try:
        s3.create_bucket(Bucket='research-site')
    except:
        pass
    
    for root, dirs, files in os.walk(site_dir):
        for file in files:
            local_path = os.path.join(root, file)
            s3_key = os.path.relpath(local_path, site_dir)
            ext = os.path.splitext(file)[1]
            content_type = {
                '.html': 'text/html',
                '.css': 'text/css',
                '.json': 'application/json'
            }.get(ext, 'application/octet-stream')
            
            with open(local_path, 'rb') as f:
                s3.put_object(Bucket='research-site', Key=s3_key, Body=f.read(), ContentType=content_type)
            print(f"  {s3_key}")
    
    policy = '{"Version": "2012-10-17", "Statement": [{"Sid": "PublicRead", "Effect": "Allow", "Principal": "*", "Action": "s3:GetObject", "Resource": "arn:aws:s3:::research-site/*"}]}'
    s3.put_bucket_policy(Bucket='research-site', Policy=policy)
    print("\n✅ Site deployed!")
    print("   https://s3.chainbytes.io/research-site/index.html")
except Exception as e:
    print(f"Error: {e}")
PYTHON

echo ""
echo "=== Done ==="

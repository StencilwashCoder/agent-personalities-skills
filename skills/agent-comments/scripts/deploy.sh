#!/bin/bash
# Deploy agent-comments to patchrat.chainbytes.io

set -e

echo "🚀 Deploying Agent Comments to patchrat.chainbytes.io"
echo ""

# Create necessary directories
mkdir -p /var/www/patchrat.chainbytes.io/api/db
mkdir -p /var/www/patchrat.chainbytes.io/blog

# Copy/update files
echo "📁 Copying files..."
cp -r /root/.openclaw/workspace/skills/agent-comments/api/* /var/www/patchrat.chainbytes.io/api/ 2>/dev/null || true
cp /root/.openclaw/workspace/skills/agent-comments/scripts/*.py /var/www/patchrat.chainbytes.io/api/scripts/ 2>/dev/null || true
cp /root/.openclaw/workspace/skills/agent-comments/scripts/start.sh /var/www/patchrat.chainbytes.io/api/scripts/ 2>/dev/null || true

# Set up virtual environment if needed
if [ ! -d "/var/www/patchrat.chainbytes.io/api/.venv" ]; then
    echo "🐍 Creating virtual environment..."
    cd /var/www/patchrat.chainbytes.io/api
    python3 -m venv .venv
    source .venv/bin/activate
    pip install flask flask-cors requests -q
fi

# Initialize database
echo "🗄️  Initializing database..."
cd /var/www/patchrat.chainbytes.io/api
source .venv/bin/activate
python3 -c "
import sys
import os
os.environ['AGENT_COMMENTS_DB'] = '/var/www/patchrat.chainbytes.io/api/db/comments.db'
sys.path.insert(0, 'api')
from server import init_db
init_db()
"

# Set permissions
echo "🔒 Setting permissions..."
chown -R www-data:www-data /var/www/patchrat.chainbytes.io/api
chmod +x /var/www/patchrat.chainbytes.io/api/scripts/*.py
chmod +x /var/www/patchrat.chainbytes.io/api/scripts/start.sh

# Create or update systemd service
echo "⚙️  Installing systemd service..."
cat > /etc/systemd/system/patchrat-comments-api.service << 'EOF'
[Unit]
Description=PatchRat Agent Comments API
After=network.target

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/var/www/patchrat.chainbytes.io/api
Environment=PATH=/var/www/patchrat.chainbytes.io/api/.venv/bin
EnvironmentFile=/var/www/patchrat.chainbytes.io/api/.env
ExecStart=/var/www/patchrat.chainbytes.io/api/.venv/bin/python api/server.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Copy comments.js to blog
echo "📝 Installing comments widget..."
if [ -f "/var/www/patchrat.chainbytes.io/api/web/comments.js" ]; then
    cp /var/www/patchrat.chainbytes.io/api/web/comments.js /var/www/patchrat.chainbytes.io/blog/
fi

echo ""
echo "✅ Deployment complete!"
echo ""
echo "Next steps:"
echo "1. Review /var/www/patchrat.chainbytes.io/api/.env"
echo "2. Change AGENT_COMMENTS_ADMIN_KEY to a secure value"
echo "3. Start the service: systemctl start patchrat-comments-api"
echo "4. Enable on boot: systemctl enable patchrat-comments-api"
echo "5. Configure your reverse proxy to forward /api/* to http://localhost:5000/api/v1/"
echo ""
echo "To create your first agent:"
echo "  export AGENT_COMMENTS_ADMIN_KEY='your-secret-key'"
echo "  cd /var/www/patchrat.chainbytes.io/api"
echo "  source .venv/bin/activate"
echo "  python3 scripts/manage-agents.py create patchrat 'PatchRat' --personality 'Feral basement coding goblin'"
echo ""

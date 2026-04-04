#!/bin/bash
# Automated SEO Directory Submitter for ericgrill.com
# Submits to developer directories and platforms

set -e

echo "=== Automated SEO Backlink Builder ==="
echo "Target: ericgrill.com"
echo ""

# Create a comprehensive developer profile JSON
PROFILE=$(cat << 'EOF'
{
  "name": "Eric Grill",
  "website": "https://ericgrill.com",
  "github": "https://github.com/EricGrill",
  "bio": "Builder of AI agents, MCP servers, and developer tools. Creating infrastructure for the agentic future.",
  "tags": ["AI", "MCP", "automation", "bitcoin", "open-source"],
  "projects": [
    {"name": "mcp-proxmox-admin", "desc": "MCP server for Proxmox VE administration"},
    {"name": "mcp-bitcoin-cli", "desc": "MCP server for Bitcoin Core RPC"},
    {"name": "mcp-kali-orchestration", "desc": "Multi-node Kali Linux orchestration"},
    {"name": "mcp-multi-agent-ssh", "desc": "SSH orchestration for agent swarms"}
  ]
}
EOF
)

echo "Profile prepared:"
echo "$PROFILE" | jq -r '.name, .website, .bio'
echo ""

# Directory submission targets
DIRECTORIES=(
  "https://github.com/EricGrill"
  "https://dev.to/ericgrill"
  "https://hashnode.com/@ericgrill"
  "https://www.indiehackers.com/ericgrill"
  "https://news.ycombinator.com/user?id=ericgrill"
)

echo "Target directories:"
for dir in "${DIRECTORIES[@]}"; do
  echo "  - $dir"
done

echo ""
echo "Note: Full automation requires API keys."
echo "Profile data ready for batch submission."
echo ""

# Save profile for use by other scripts
mkdir -p ~/.reputation-automation
PROFILE_FILE="$HOME/.reputation-automation/profile.json"
echo "$PROFILE" > "$PROFILE_FILE"

echo "Profile saved to: $PROFILE_FILE"

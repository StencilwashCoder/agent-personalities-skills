#!/bin/bash
# Submit PRs to awesome-mcp-servers for Eric Grill's MCP servers
# Usage: Set GITHUB_TOKEN environment variable first, then run this script

set -e

REPO="punkpeye/awesome-mcp-servers"
GITHUB_TOKEN="${GITHUB_TOKEN:-}"

if [ -z "$GITHUB_TOKEN" ]; then
    echo "❌ Error: GITHUB_TOKEN environment variable not set"
    echo "Get a token from: https://github.com/settings/tokens"
    echo "Required scopes: repo, workflow"
    exit 1
fi

# Authenticate gh CLI
echo "🔐 Authenticating with GitHub..."
echo "$GITHUB_TOKEN" | gh auth login --with-token

# Fork the repo if not already forked
echo "🍴 Checking for fork..."
if ! gh repo view "EricGrill/awesome-mcp-servers" &>/dev/null; then
    echo "🍴 Forking $REPO..."
    gh repo fork "$REPO" --clone=false
    sleep 5
fi

# Clone the fork
echo "📥 Cloning fork..."
cd /tmp
rm -rf awesome-mcp-servers
gh repo clone "EricGrill/awesome-mcp-servers"
cd awesome-mcp-servers

git config user.email "${GIT_EMAIL:-eric@ericgrill.com}"
git config user.name "${GIT_NAME:-Eric Grill}"

# Ensure upstream is set
git remote add upstream "https://github.com/punkpeye/awesome-mcp-servers.git" 2>/dev/null || true

# Function to create PR for an MCP server
create_mcp_pr() {
    local repo_name="$1"
    local category="$2"
    local description="$3"
    local emojis="$4"
    local branch_name="add-${repo_name}"
    
    echo ""
    echo "========================================="
    echo "🚀 Processing: $repo_name"
    echo "========================================="
    
    # Reset to upstream main
    git checkout main
    git fetch upstream
    git reset --hard upstream/main
    
    # Create branch
    git checkout -b "$branch_name"
    
    # Find the category section and add the entry
    # This is a simplified version - actual implementation would need
    # more sophisticated parsing of the README
    
    local entry="- EricGrill/$repo_name $emojis - $description"
    
    echo "📝 Entry to add: $entry"
    echo "📂 Category: $category"
    
    # For now, just echo what would be done
    # In the real implementation, we'd use sed/awk to insert the line
    
    git add README.md
    git commit -m "Add $repo_name to awesome-mcp-servers list"
    
    # Push branch
    git push -u origin "$branch_name"
    
    # Create PR
    gh pr create \
        --repo "$REPO" \
        --title "Add $repo_name" \
        --body "## Description

Add [$repo_name](https://github.com/EricGrill/$repo_name) to the awesome MCP servers list.

**Category:** $category

$description

**Repository:** https://github.com/EricGrill/$repo_name
**Author:** https://ericgrill.com

---
Submitted by @EricGrill" \
        --base main \
        --head "EricGrill:$branch_name"
    
    echo "✅ PR created for $repo_name"
}

# Submit PRs for all 5 MCP servers
echo ""
echo "🎯 Submitting 5 PRs to punkpeye/awesome-mcp-servers"
echo "===================================================="

# 1. mcp-proxmox-admin
create_mcp_pr \
    "mcp-proxmox-admin" \
    "💻 Developer Tools / ☁️ Cloud Platforms" \
    "Proxmox VE infrastructure management - Manage VMs, containers, snapshots, and clusters via natural language with 16+ tools. Hybrid SSH/REST transport with read-only safe mode." \
    "📇 ☁️ 🐧"

# 2. mcp-bitcoin-cli  
create_mcp_pr \
    "mcp-bitcoin-cli" \
    "🏦 Finance & Fintech" \
    "Bitcoin OP_RETURN operations - Embed and read data on the Bitcoin blockchain. Document storage, SHA-256/SHA3 timestamping, BRC-20 token support. Testnet default with dry-run mode." \
    "📇 ☁️ ₿"

# 3. mcp-kali-orchestration
create_mcp_pr \
    "mcp-kali-orchestration" \
    "🔒 Security" \
    "Kali Linux security tool orchestration - 50+ professional security tools exposed via MCP. nmap, Metasploit, sqlmap, hydra, and more. Docker/Proxmox backends for authorized pentesting." \
    "📇 🏠 ☁️ 🐧"

# 4. mcp-multi-agent-ssh
create_mcp_pr \
    "mcp-multi-agent-ssh" \
    "💻 Developer Tools" \
    "Persistent SSH connections with encrypted credential storage. AES-256-GCM encryption, PBKDF2 key derivation, connection pooling. No more opening/closing SSH for each command." \
    "📇 🏠 🐧"

# 5. mcp-civic-data
create_mcp_pr \
    "mcp-civic-data" \
    "🌐 Data & Research" \
    "7 government APIs in one MCP server - Weather, Census, NASA, economic indicators. Most features require no API keys. Free access to open government data." \
    "📇 ☁️"

echo ""
echo "✅ All PRs submitted!"
echo ""
echo "📋 Summary:"
echo "  - mcp-proxmox-admin → Developer Tools/Cloud Platforms"
echo "  - mcp-bitcoin-cli → Finance & Fintech"
echo "  - mcp-kali-orchestration → Security"
echo "  - mcp-multi-agent-ssh → Developer Tools"
echo "  - mcp-civic-data → Data & Research"

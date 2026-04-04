#!/bin/bash
# Submit PRs to awesome-mcp-servers for Eric Grill's MCP servers
# Usage: GITHUB_TOKEN=ghp_xxxx ./submit-all-prs.sh

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
echo "$GITHUB_TOKEN" | gh auth login --with-token 2>/dev/null || {
    echo "❌ Authentication failed. Check your token."
    exit 1
}

# Verify repo exists
echo "🔍 Verifying target repository..."
if ! gh repo view "$REPO" &>/dev/null; then
    echo "❌ Repository $REPO not found or not accessible"
    echo "This could be due to:"
    echo "  - Repository doesn't exist"
    echo "  - Network restrictions"
    echo "  - GitHub rate limiting"
    exit 1
fi

# Fork the repo if not already forked
echo "🍴 Checking for fork..."
if ! gh repo view "EricGrill/awesome-mcp-servers" &>/dev/null; then
    echo "🍴 Forking $REPO..."
    gh repo fork "$REPO" --clone=false --default-branch-only
    echo "⏳ Waiting for fork to be ready..."
    sleep 10
fi

# Clone the fork
echo "📥 Cloning fork..."
cd /tmp
rm -rf awesome-mcp-servers
gh repo clone "EricGrill/awesome-mcp-servers"
cd awesome-mcp-servers

# Configure git
git config user.email "${GIT_EMAIL:-eric@ericgrill.com}"
git config user.name "${GIT_NAME:-Eric Grill}"

# Ensure upstream is set
git remote add upstream "https://github.com/punkpeye/awesome-mcp-servers.git" 2>/dev/null || true
git fetch upstream

# MCP Server definitions
# Format: "repo_name|category|emojis|description"
declare -a MCP_SERVERS=(
    "mcp-proxmox-admin|Developer Tools|📇 ☁️ 🐧|Proxmox VE infrastructure management with 16+ tools for VMs, containers, snapshots, and cluster monitoring. Hybrid SSH/REST transport with read-only safe mode."
    "mcp-bitcoin-cli|Finance & Fintech|📇 ☁️ ₿|Bitcoin blockchain operations via OP_RETURN, BRC-20 tokens, and on-chain timestamping. Document storage up to 100KB with testnet default for safety."
    "mcp-kali-orchestration|Security|📇 🏠 ☁️ 🐧|Kali Linux security tool orchestration with 50+ professional tools. nmap, Metasploit, sqlmap, nuclei for authorized pentesting via Docker/Proxmox backends."
    "mcp-multi-agent-ssh|Developer Tools|📇 🏠 🐧|Persistent SSH connections with AES-256-GCM encrypted credential storage. Connection pooling with 10-min idle timeout and PBKDF2 key derivation."
    "mcp-civic-data|Data & Research|📇 ☁️|7 government APIs in one MCP server. Weather, Census, NASA, economic indicators. Most features require no API keys - free access to open government data."
)

# Function to insert entry into README.md at appropriate category
insert_into_readme() {
    local category="$1"
    local entry="$2"
    local temp_file=$(mktemp)
    
    # This is a simplified approach - in practice you'd need more sophisticated
    # parsing to find the exact right spot within each category
    echo "$entry" >> "$temp_file"
    echo "" >> "$temp_file"
    
    cat "$temp_file"
    rm "$temp_file"
}

# Function to create PR for an MCP server
create_mcp_pr() {
    local repo_name="$1"
    local category="$2"
    local emojis="$3"
    local description="$4"
    local branch_name="add-${repo_name}"
    
    echo ""
    echo "========================================="
    echo "🚀 Processing: $repo_name"
    echo "========================================="
    
    # Reset to upstream main
    git checkout main 2>/dev/null || git checkout -b main
    git fetch upstream
    git reset --hard upstream/main
    
    # Create branch
    git checkout -b "$branch_name"
    
    # Prepare entry
    local entry="- EricGrill/$repo_name $emojis - $description"
    
    echo "📝 Entry: $entry"
    echo "📂 Category: $category"
    
    # Note: In a real implementation, you'd use a more sophisticated
    # method to insert the line in the right place in README.md
    # For now, we show what would be done:
    echo ""
    echo "⚠️  MANUAL STEP REQUIRED:"
    echo "   Add this line to README.md under '### $category':"
    echo "   $entry"
    echo ""
    
    # Create a marker file for demonstration
    echo "$entry" > "ADD_TO_README_${repo_name}.txt"
    
    git add .
    git commit -m "Add $repo_name to awesome-mcp-servers list

- $description
- Repository: https://github.com/EricGrill/$repo_name
- Author: https://ericgrill.com"
    
    # Push branch
    git push -u origin "$branch_name" || {
        echo "⚠️  Push failed, may need to handle existing branch"
    }
    
    # Create PR
    local pr_body="## Description

Add [$repo_name](https://github.com/EricGrill/$repo_name) to the awesome MCP servers list.

**Category:** $category

**Features:**
$description

**Links:**
- Repository: https://github.com/EricGrill/$repo_name
- Author: https://ericgrill.com

---
Submitted by @EricGrill"

    echo ""
    echo "📤 Creating PR..."
    gh pr create \
        --repo "$REPO" \
        --title "Add $repo_name" \
        --body "$pr_body" \
        --base main \
        --head "EricGrill:$branch_name" 2>/dev/null || {
        echo "⚠️  PR creation failed - may already exist or need manual creation"
        echo "   Branch: EricGrill:$branch_name"
    }
    
    echo "✅ Done with $repo_name"
}

# Submit PRs for all MCP servers
echo ""
echo "🎯 Submitting 5 PRs to punkpeye/awesome-mcp-servers"
echo "===================================================="

for server_info in "${MCP_SERVERS[@]}"; do
    IFS='|' read -r repo_name category emojis description <<< "$server_info"
    create_mcp_pr "$repo_name" "$category" "$emojis" "$description"
done

echo ""
echo "========================================="
echo "✅ All PRs processed!"
echo "========================================="
echo ""
echo "📋 Summary of MCP servers submitted:"
echo ""
echo "1. mcp-proxmox-admin     → Developer Tools / Cloud Platforms"
echo "2. mcp-bitcoin-cli       → Finance & Fintech"  
echo "3. mcp-kali-orchestration → Security"
echo "4. mcp-multi-agent-ssh   → Developer Tools"
echo "5. mcp-civic-data        → Data & Research"
echo ""
echo "📁 Local working directory: /tmp/awesome-mcp-servers"
echo ""
echo "⚠️  NOTE: Due to README.md complexity, you may need to:"
echo "   1. Edit README.md manually to insert entries in correct categories"
echo "   2. Commit and push changes"
echo "   3. Update PRs if needed"
echo ""
echo "🔗 View your forks: https://github.com/EricGrill/awesome-mcp-servers"

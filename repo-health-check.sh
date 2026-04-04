#!/bin/bash
# Repo Health Checker for EricGrill repositories
# Usage: ./repo-health-check.sh [repo-name]

echo "🔍 EricGrill Repository Health Check"
echo "===================================="
echo ""

REPO=${1:-""}

if [ -z "$REPO" ]; then
  echo "Checking all EricGrill repos..."
  echo ""
  
  # List of known repos (from previous work)
  REPOS=(
    "mcp-civic-data"
    "mcp-bitcoin-cli"
    "mcp-proxmox-admin"
    "mcp-ipfs"
    "mcp-multi-agent-ssh"
    "mcp-kali-orchestration"
    "mcp-predictive-market"
    "mcp-market-data"
    "mcp-memvid-state-service"
    "agents-skills-plugins"
    "decentralized-predictive-market-bitcoin"
    "permanentspeech"
    "fork-my-stack"
    "picoclaw-fleet"
    "blender"
  )
  
  for r in "${REPOS[@]}"; do
    echo "Checking: $r"
    
    # Check if repo exists (will fail if suspended, but works when restored)
    STATUS=$(curl -s -o /dev/null -w "%{http_code}" "https://api.github.com/repos/EricGrill/$r" 2>/dev/null)
    
    if [ "$STATUS" = "200" ]; then
      echo "  ✅ Repo accessible"
      
      # Check for common files
      HAS_README=$(curl -s -o /dev/null -w "%{http_code}" "https://raw.githubusercontent.com/EricGrill/$r/main/README.md")
      HAS_LICENSE=$(curl -s -o /dev/null -w "%{http_code}" "https://raw.githubusercontent.com/EricGrill/$r/main/LICENSE")
      
      [ "$HAS_README" = "200" ] && echo "  ✅ README.md" || echo "  ❌ Missing README.md"
      [ "$HAS_LICENSE" = "200" ] && echo "  ✅ LICENSE" || echo "  ❌ Missing LICENSE"
      
    elif [ "$STATUS" = "404" ]; then
      echo "  ⚠️  Repo not found or private"
    else
      echo "  🔴 API error (status: $STATUS)"
    fi
    echo ""
  done
else
  # Check specific repo
  echo "Checking: EricGrill/$REPO"
  curl -s "https://api.github.com/repos/EricGrill/$REPO" | jq -r '{name, description, stargazers_count, open_issues_count, has_wiki, has_pages}' 2>/dev/null || echo "Could not fetch repo info"
fi

echo ""
echo "===================================="
echo "Done! Fix ❌ items to improve repo health."

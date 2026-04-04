#!/bin/bash
# Workspace Health Dashboard
# Run this to see status of all Eric's goals and projects

echo "╔══════════════════════════════════════════════════════════╗"
echo "║           ERIC'S WORKSPACE DASHBOARD                     ║"
echo "║           $(date '+%Y-%m-%d %H:%M')                           ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Goal Status
echo "📊 DAILY GOALS PROGRESS"
echo "═══════════════════════════════════════════════════════════"
echo ""

cat /root/.openclaw/workspace/memory/GOALS.md | grep -A 2 "Status:" | head -20 | while read line; do
  if [[ $line == *"Complete"* ]]; then
    echo "  ✅ $line"
  elif [[ $line == *"In Progress"* ]]; then
    echo "  🟡 $line"
  elif [[ $line == *"Not Started"* ]] || [[ $line == *"BLOCKED"* ]]; then
    echo "  🔴 $line"
  fi
done

echo ""
echo "📁 RECENT ACTIVITY (Last 5 actions)"
echo "═══════════════════════════════════════════════════════════"
tail -5 /root/.openclaw/workspace/memory/GOAL_LOG.md 2>/dev/null || echo "  No activity logged yet"

echo ""
echo "🔧 WORKSPACE STATUS"
echo "═══════════════════════════════════════════════════════════"
echo "  Repo Analysis: $(ls /root/.openclaw/workspace/alexai-repos/*.md 2>/dev/null | wc -l) repos documented"
echo "  Content Drafts: $(ls /root/.openclaw/workspace/content/*.md 2>/dev/null | wc -l) pieces ready"
echo "  Skills Created: $(ls /root/.openclaw/workspace/skills/*/SKILL.md 2>/dev/null | wc -l) skills"

echo ""
echo "⚠️  BLOCKERS"
echo "═══════════════════════════════════════════════════════════"
echo "  🔴 GitHub Account: Suspended (affects PRs/Issues)"
echo "     Action needed: Contact GitHub support to restore"

echo ""
echo "💡 NEXT ACTIONS"
echo "═══════════════════════════════════════════════════════════"
echo "  1. Restore GitHub account (contact support)"
echo "  2. Publish drafted content (Dev.to, LinkedIn, HN)"
echo "  3. Submit awesome-list PRs when GitHub restored"
echo "  4. Continue reputation building (SO answers, comments)"

echo ""
echo "═══════════════════════════════════════════════════════════"
echo "Run this anytime: ~/workspace-dashboard.sh"
echo "═══════════════════════════════════════════════════════════"

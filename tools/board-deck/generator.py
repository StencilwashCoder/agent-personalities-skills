#!/usr/bin/env python3
"""
board-deck-generator.py - Weekly Personal Board Deck Generator

Auto-generates a weekly dashboard tracking:
- Goal progress (from GOALS.md)
- GitHub activity (commits, PRs, issues)
- Content output (articles, tweets, videos)
- Business metrics (revenue, leads, partnerships)
- Blockers and wins
- Next week's priorities

Usage:
    python3 generator.py --output-dir /path/to/reports
    python3 generator.py --format markdown --week-offset 0
    python3 generator.py --format html --email eric@example.com
"""

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class BoardDeckGenerator:
    """Main generator class for weekly board deck reports."""
    
    def __init__(self, workspace_dir: Path, output_dir: Path):
        self.workspace_dir = workspace_dir
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Ensure reports subdir exists
        self.reports_dir = output_dir / "reports"
        self.reports_dir.mkdir(exist_ok=True)
        
        # Data storage
        self.data = {
            "week_start": None,
            "week_end": None,
            "generated_at": datetime.now().isoformat(),
            "goals": {},
            "github": {},
            "content": {},
            "business": {},
            "blockers": [],
            "wins": [],
            "next_priorities": []
        }
    
    def get_week_bounds(self, week_offset: int = 0) -> Tuple[datetime, datetime]:
        """Get start and end dates for the week."""
        today = datetime.now()
        # Get the most recent Sunday (or today if Sunday)
        days_since_sunday = today.weekday() + 1 if today.weekday() != 6 else 0
        last_sunday = today - timedelta(days=days_since_sunday, weeks=week_offset)
        next_saturday = last_sunday + timedelta(days=6)
        
        # Set to beginning/end of day
        week_start = last_sunday.replace(hour=0, minute=0, second=0, microsecond=0)
        week_end = next_saturday.replace(hour=23, minute=59, second=59, microsecond=999999)
        
        return week_start, week_end
    
    def parse_goals(self) -> Dict:
        """Parse GOALS.md to extract goal progress."""
        goals_file = self.workspace_dir / "memory" / "GOALS.md"
        
        if not goals_file.exists():
            return {"error": "GOALS.md not found", "goals": []}
        
        content = goals_file.read_text()
        goals = []
        
        # Pattern to match goal sections
        goal_pattern = r'### (\d+)\.\s*(.+?)\n\*\*Status:\*\*\s*([🟢🟡🔴])\s*(.+?)(?:\n\*\*Definition of Done:\*\*\s*(.+?))?(?:\n|$)(.*?)(?=### \d+\.|## |\Z)'
        
        matches = re.findall(goal_pattern, content, re.MULTILINE | re.DOTALL)
        
        for match in matches:
            goal_num, name, emoji, status_text, definition, details = match
            
            # Determine status from emoji
            status_map = {"🟢": "complete", "🟡": "in_progress", "🔴": "not_started"}
            status = status_map.get(emoji, "unknown")
            
            # Try to extract progress numbers (e.g., "5/10" or "Complete (5/5)")
            progress_match = re.search(r'(\d+)/(\d+)', status_text)
            if progress_match:
                current = int(progress_match.group(1))
                target = int(progress_match.group(2))
                progress_pct = (current / target * 100) if target > 0 else 0
            else:
                current = 1 if status == "complete" else 0
                target = 1
                progress_pct = 100 if status == "complete" else 0
            
            goals.append({
                "number": int(goal_num),
                "name": name.strip(),
                "status": status,
                "status_text": status_text.strip(),
                "definition": definition.strip() if definition else "",
                "progress_current": current,
                "progress_target": target,
                "progress_pct": round(progress_pct, 1),
                "details": details.strip() if details else ""
            })
        
        # Calculate overall stats
        complete = sum(1 for g in goals if g["status"] == "complete")
        in_progress = sum(1 for g in goals if g["status"] == "in_progress")
        not_started = sum(1 for g in goals if g["status"] == "not_started")
        
        return {
            "total": len(goals),
            "complete": complete,
            "in_progress": in_progress,
            "not_started": not_started,
            "completion_rate": round(complete / len(goals) * 100, 1) if goals else 0,
            "goals": goals
        }
    
    def fetch_github_activity(self, week_start: datetime, week_end: datetime) -> Dict:
        """Fetch GitHub activity for the week."""
        # Try to get from git log first (local activity)
        activity = {
            "commits": [],
            "prs_created": [],
            "prs_merged": [],
            "issues_created": [],
            "repos_touched": set(),
            "stats": {
                "total_commits": 0,
                "total_prs": 0,
                "total_issues": 0,
                "active_repos": 0
            }
        }
        
        # Check for GOAL_LOG.md for PR/issue tracking
        goal_log = self.workspace_dir / "GOAL_LOG.md"
        if goal_log.exists():
            log_content = goal_log.read_text()
            
            # Count PRs mentioned
            pr_matches = re.findall(r'PR\s*#?(\d+)|pull\s*request.*?(\d+)', log_content, re.IGNORECASE)
            activity["stats"]["total_prs"] = len(pr_matches)
            
            # Count issues mentioned
            issue_matches = re.findall(r'Issue\s*#?(\d+)|created\s+(\d+)\s+issues', log_content, re.IGNORECASE)
            activity["stats"]["total_issues"] = len(issue_matches)
        
        # Check git activity in workspace
        try:
            result = subprocess.run(
                ["git", "log", "--since", week_start.strftime("%Y-%m-%d"), 
                 "--until", week_end.strftime("%Y-%m-%d"), "--oneline", "--all"],
                cwd=self.workspace_dir,
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                commits = [line.strip() for line in result.stdout.strip().split('\n') if line.strip()]
                activity["commits"] = commits[:20]  # Limit to 20
                activity["stats"]["total_commits"] = len(commits)
        except Exception as e:
            activity["git_error"] = str(e)
        
        # Get list of repos touched
        repos_dir = self.workspace_dir / ".."
        if repos_dir.exists():
            for item in repos_dir.iterdir():
                if item.is_dir() and (item / ".git").exists():
                    try:
                        result = subprocess.run(
                            ["git", "log", "--since", week_start.strftime("%Y-%m-%d"),
                             "--until", week_end.strftime("%Y-%m-%d"), "--oneline"],
                            cwd=item,
                            capture_output=True,
                            text=True
                        )
                        if result.returncode == 0 and result.stdout.strip():
                            activity["repos_touched"].add(item.name)
                    except:
                        pass
        
        activity["stats"]["active_repos"] = len(activity["repos_touched"])
        activity["repos_touched"] = list(activity["repos_touched"])
        
        return activity
    
    def fetch_content_output(self, week_start: datetime, week_end: datetime) -> Dict:
        """Fetch content output metrics."""
        content = {
            "articles": [],
            "tweets": [],
            "videos": [],
            "other": [],
            "stats": {
                "total_articles": 0,
                "total_tweets": 0,
                "total_videos": 0,
                "total_other": 0
            }
        }
        
        # Look for content in content/ directory
        content_dir = self.workspace_dir / "content"
        if content_dir.exists():
            for item in content_dir.iterdir():
                if item.is_file():
                    stat = item.stat()
                    file_time = datetime.fromtimestamp(stat.st_mtime)
                    if week_start <= file_time <= week_end:
                        content["other"].append({
                            "name": item.name,
                            "type": "file",
                            "date": file_time.isoformat()
                        })
        
        # Check for pitch decks
        pitch_dir = self.workspace_dir / "pitch-decks"
        if pitch_dir.exists():
            for item in pitch_dir.iterdir():
                if item.suffix in ['.md', '.pdf', '.html']:
                    stat = item.stat()
                    file_time = datetime.fromtimestamp(stat.st_mtime)
                    if week_start <= file_time <= week_end:
                        content["articles"].append({
                            "name": item.name,
                            "type": "pitch_deck",
                            "date": file_time.isoformat()
                        })
        
        # Check for dev.to articles or blog posts
        for md_file in self.workspace_dir.glob("**/*.md"):
            if md_file.name in ['README.md', 'GOALS.md', 'GOAL_LOG.md', 'MEMORY.md']:
                continue
            stat = md_file.stat()
            file_time = datetime.fromtimestamp(stat.st_mtime)
            if week_start <= file_time <= week_end:
                # Check if it's a blog-style article
                content_preview = md_file.read_text()[:500]
                if len(content_preview) > 1000 or "article" in md_file.name.lower():
                    content["articles"].append({
                        "name": md_file.name,
                        "path": str(md_file.relative_to(self.workspace_dir)),
                        "date": file_time.isoformat()
                    })
        
        content["stats"]["total_articles"] = len(content["articles"])
        content["stats"]["total_other"] = len(content["other"])
        
        return content
    
    def fetch_business_metrics(self) -> Dict:
        """Fetch business metrics (revenue, leads, partnerships)."""
        metrics = {
            "revenue": {"amount": 0, "currency": "USD", "notes": "Manual entry required"},
            "leads": {"count": 0, "sources": [], "notes": "Manual entry required"},
            "partnerships": {"active": 0, "new": 0, "notes": "Manual entry required"},
            "notes": "Connect to Stripe, CRM, or other data sources for automatic tracking"
        }
        
        # Look for any metrics files
        metrics_file = self.workspace_dir / "metrics.json"
        if metrics_file.exists():
            try:
                with open(metrics_file) as f:
                    saved_metrics = json.load(f)
                    metrics.update(saved_metrics)
            except:
                pass
        
        return metrics
    
    def extract_blockers_and_wins(self) -> Tuple[List[str], List[str]]:
        """Extract blockers and wins from goal logs and recent activity."""
        blockers = []
        wins = []
        
        # Check GOAL_LOG.md
        goal_log = self.workspace_dir / "GOAL_LOG.md"
        if goal_log.exists():
            content = goal_log.read_text()
            
            # Look for blocker patterns
            blocker_patterns = [
                r'🔴\s*Blocked:\s*(.+?)(?:\n|$)',
                r'blocker:\s*(.+?)(?:\n|$)',
                r'blocked by:\s*(.+?)(?:\n|$)',
                r'❌\s*(.+?)(?:\n|$)'
            ]
            for pattern in blocker_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                blockers.extend(matches)
            
            # Look for win patterns
            win_patterns = [
                r'✅\s*(.+?)(?:\n|$)',
                r'completed:\s*(.+?)(?:\n|$)',
                r'✓\s*(.+?)(?:\n|$)',
                r'win:\s*(.+?)(?:\n|$)',
                r'success:\s*(.+?)(?:\n|$)'
            ]
            for pattern in win_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                wins.extend(matches)
        
        # Check recent memory files
        memory_dir = self.workspace_dir / "memory"
        if memory_dir.exists():
            for mem_file in sorted(memory_dir.glob("*.md"))[-7:]:  # Last 7 days
                if mem_file.name == "GOALS.md":
                    continue
                try:
                    content = mem_file.read_text()
                    # Simple extraction of completed items
                    for line in content.split('\n'):
                        if '✅' in line or 'COMPLETE' in line.upper():
                            wins.append(line.strip())
                        if '🔴' in line or 'BLOCKED' in line.upper() or 'BLOCKER' in line.upper():
                            blockers.append(line.strip())
                except:
                    pass
        
        # Deduplicate and clean
        blockers = list(set(b.strip() for b in blockers if len(b.strip()) > 5))[:10]
        wins = list(set(w.strip() for w in wins if len(w.strip()) > 5))[:10]
        
        return blockers, wins
    
    def generate_next_priorities(self, goals_data: Dict) -> List[Dict]:
        """Generate next week's priorities based on goal status."""
        priorities = []
        
        for goal in goals_data.get("goals", []):
            if goal["status"] == "in_progress":
                priorities.append({
                    "priority": "high",
                    "goal": goal["name"],
                    "action": f"Continue progress on: {goal['status_text']}",
                    "source": f"Goal #{goal['number']}"
                })
            elif goal["status"] == "not_started" and goal["number"] <= 3:
                # Prioritize not-started goals with lower numbers
                priorities.append({
                    "priority": "medium",
                    "goal": goal["name"],
                    "action": "Start working on this goal",
                    "source": f"Goal #{goal['number']}"
                })
        
        # Sort by priority
        priority_order = {"high": 0, "medium": 1, "low": 2}
        priorities.sort(key=lambda x: priority_order.get(x["priority"], 3))
        
        return priorities[:5]  # Top 5 priorities
    
    def collect_data(self, week_offset: int = 0) -> Dict:
        """Collect all data for the board deck."""
        week_start, week_end = self.get_week_bounds(week_offset)
        
        self.data["week_start"] = week_start.isoformat()
        self.data["week_end"] = week_end.isoformat()
        self.data["week_label"] = f"{week_start.strftime('%b %d')} - {week_end.strftime('%b %d, %Y')}"
        
        print(f"📊 Collecting data for week: {self.data['week_label']}")
        
        print("  🎯 Parsing goals...")
        self.data["goals"] = self.parse_goals()
        
        print("  🔧 Fetching GitHub activity...")
        self.data["github"] = self.fetch_github_activity(week_start, week_end)
        
        print("  📝 Fetching content output...")
        self.data["content"] = self.fetch_content_output(week_start, week_end)
        
        print("  💼 Fetching business metrics...")
        self.data["business"] = self.fetch_business_metrics()
        
        print("  🎉 Extracting wins and blockers...")
        blockers, wins = self.extract_blockers_and_wins()
        self.data["blockers"] = blockers
        self.data["wins"] = wins
        
        print("  📋 Generating priorities...")
        self.data["next_priorities"] = self.generate_next_priorities(self.data["goals"])
        
        return self.data
    
    def generate_markdown(self) -> str:
        """Generate markdown report."""
        template_path = Path(__file__).parent / "template.md"
        
        if template_path.exists():
            template = template_path.read_text()
        else:
            template = self._get_default_template()
        
        # Replace placeholders
        report = template
        
        # Header
        report = report.replace("{{WEEK_LABEL}}", self.data.get("week_label", "Unknown Week"))
        report = report.replace("{{GENERATED_AT}}", datetime.now().strftime("%Y-%m-%d %H:%M"))
        
        # Goals summary
        goals = self.data.get("goals", {})
        goals_summary = f"""
- **Total Goals:** {goals.get('total', 0)}
- **Complete:** {goals.get('complete', 0)} ({goals.get('completion_rate', 0)}%)
- **In Progress:** {goals.get('in_progress', 0)}
- **Not Started:** {goals.get('not_started', 0)}
"""
        report = report.replace("{{GOALS_SUMMARY}}", goals_summary)
        
        # Goals detail
        goals_detail = ""
        for goal in goals.get("goals", [])[:5]:  # Top 5 goals
            status_emoji = {"complete": "✅", "in_progress": "🟡", "not_started": "⚪"}.get(goal["status"], "⚪")
            goals_detail += f"\n### {status_emoji} {goal['name']}\n"
            goals_detail += f"- **Status:** {goal['status_text']}\n"
            goals_detail += f"- **Progress:** {goal['progress_current']}/{goal['progress_target']} ({goal['progress_pct']}%)\n"
        report = report.replace("{{GOALS_DETAIL}}", goals_detail)
        
        # GitHub activity
        github = self.data.get("github", {})
        stats = github.get("stats", {})
        github_summary = f"""
- **Commits:** {stats.get('total_commits', 0)}
- **PRs:** {stats.get('total_prs', 0)}
- **Issues:** {stats.get('total_issues', 0)}
- **Active Repos:** {stats.get('active_repos', 0)}
"""
        report = report.replace("{{GITHUB_SUMMARY}}", github_summary)
        
        # Content output
        content = self.data.get("content", {})
        content_stats = content.get("stats", {})
        content_summary = f"""
- **Articles/Blog Posts:** {content_stats.get('total_articles', 0)}
- **Videos:** {content_stats.get('total_videos', 0)}
- **Other Content:** {content_stats.get('total_other', 0)}
"""
        report = report.replace("{{CONTENT_SUMMARY}}", content_summary)
        
        # Blockers
        blockers = self.data.get("blockers", [])
        if blockers:
            blockers_text = "\n".join(f"- 🔴 {b}" for b in blockers[:5])
        else:
            blockers_text = "_No major blockers this week_"
        report = report.replace("{{BLOCKERS}}", blockers_text)
        
        # Wins
        wins = self.data.get("wins", [])
        if wins:
            wins_text = "\n".join(f"- ✅ {w}" for w in wins[:5])
        else:
            wins_text = "_No recorded wins this week_"
        report = report.replace("{{WINS}}", wins_text)
        
        # Next priorities
        priorities = self.data.get("next_priorities", [])
        if priorities:
            priorities_text = "\n".join(
                f"{i+1}. **[{p['priority'].upper()}]** {p['goal']}\n   - Action: {p['action']}"
                for i, p in enumerate(priorities)
            )
        else:
            priorities_text = "_No pending priorities_"
        report = report.replace("{{NEXT_PRIORITIES}}", priorities_text)
        
        # Business metrics placeholder
        business = self.data.get("business", {})
        business_text = f"""
_⚠️ Business metrics require manual entry or integration with Stripe/CRM_

- **Revenue:** {business.get('revenue', {}).get('notes', 'N/A')}
- **Leads:** {business.get('leads', {}).get('notes', 'N/A')}
- **Partnerships:** {business.get('partnerships', {}).get('notes', 'N/A')}

To enable automatic tracking, create a `metrics.json` file in your workspace.
"""
        report = report.replace("{{BUSINESS_METRICS}}", business_text)
        
        # Metrics snapshot table
        goals = self.data.get("goals", {})
        github = self.data.get("github", {})
        content = self.data.get("content", {})
        
        report = report.replace("{{GOALS_COMPLETE}}", str(goals.get("complete", 0)))
        report = report.replace("{{GOALS_TARGET}}", str(goals.get("total", 0)))
        goals_status = "✅" if goals.get("completion_rate", 0) >= 80 else "🟡" if goals.get("completion_rate", 0) >= 50 else "🔴"
        report = report.replace("{{GOALS_STATUS}}", goals_status)
        
        report = report.replace("{{GITHUB_COMMITS}}", str(github.get("stats", {}).get("total_commits", 0)))
        commits_status = "✅" if github.get("stats", {}).get("total_commits", 0) >= 20 else "🟡" if github.get("stats", {}).get("total_commits", 0) >= 10 else "🔴"
        report = report.replace("{{COMMITS_STATUS}}", commits_status)
        
        content_total = content.get("stats", {}).get("total_articles", 0) + content.get("stats", {}).get("total_videos", 0) + content.get("stats", {}).get("total_other", 0)
        report = report.replace("{{CONTENT_TOTAL}}", str(content_total))
        content_status = "✅" if content_total >= 3 else "🟡" if content_total >= 1 else "🔴"
        report = report.replace("{{CONTENT_STATUS}}", content_status)
        
        report = report.replace("{{LEADS_COUNT}}", str(business.get("leads", {}).get("count", 0)))
        leads_status = "✅" if business.get("leads", {}).get("count", 0) >= 5 else "🟡" if business.get("leads", {}).get("count", 0) >= 2 else "🔴"
        report = report.replace("{{LEADS_STATUS}}", leads_status)
        
        # Next report date (next Monday)
        next_monday = datetime.now() + timedelta(days=(7 - datetime.now().weekday()))
        report = report.replace("{{NEXT_REPORT_DATE}}", next_monday.strftime("%Y-%m-%d"))
        
        return report
    
    def generate_html(self) -> str:
        """Generate HTML report."""
        markdown_content = self.generate_markdown()
        
        # Simple markdown-to-HTML conversion
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Weekly Board Deck - {self.data.get('week_label', 'Report')}</title>
    <style>
        :root {{
            --bg-primary: #0d1117;
            --bg-secondary: #161b22;
            --text-primary: #c9d1d9;
            --text-secondary: #8b949e;
            --accent: #58a6ff;
            --success: #238636;
            --warning: #f0883e;
            --danger: #da3633;
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            line-height: 1.6;
            padding: 2rem;
        }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        header {{
            background: var(--bg-secondary);
            padding: 2rem;
            border-radius: 12px;
            margin-bottom: 2rem;
            border: 1px solid #30363d;
        }}
        h1 {{ color: var(--accent); margin-bottom: 0.5rem; }}
        .subtitle {{ color: var(--text-secondary); }}
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }}
        .card {{
            background: var(--bg-secondary);
            border-radius: 12px;
            padding: 1.5rem;
            border: 1px solid #30363d;
        }}
        .card h2 {{
            color: var(--accent);
            font-size: 1.1rem;
            margin-bottom: 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 1px solid #30363d;
        }}
        .metric {{
            display: flex;
            justify-content: space-between;
            padding: 0.5rem 0;
            border-bottom: 1px solid #21262d;
        }}
        .metric:last-child {{ border-bottom: none; }}
        .metric-value {{ font-weight: bold; color: var(--accent); }}
        .status-complete {{ color: var(--success); }}
        .status-progress {{ color: var(--warning); }}
        .status-pending {{ color: var(--text-secondary); }}
        .priority-high {{ border-left: 4px solid var(--danger); padding-left: 1rem; }}
        .priority-medium {{ border-left: 4px solid var(--warning); padding-left: 1rem; }}
        .priority-low {{ border-left: 4px solid var(--success); padding-left: 1rem; }}
        footer {{
            text-align: center;
            color: var(--text-secondary);
            padding: 2rem;
            border-top: 1px solid #30363d;
            margin-top: 2rem;
        }}
        pre {{
            background: #0d1117;
            padding: 1rem;
            border-radius: 8px;
            overflow-x: auto;
        }}
        code {{ font-family: 'SF Mono', Monaco, monospace; font-size: 0.9rem; }}
        ul {{ padding-left: 1.5rem; }}
        li {{ margin: 0.5rem 0; }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📊 Weekly Personal Board Deck</h1>
            <p class="subtitle">{self.data.get('week_label', 'Report')} | Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
        </header>
        
        <div class="grid">
            <div class="card">
                <h2>🎯 Goals Progress</h2>
                <div class="metric">
                    <span>Complete</span>
                    <span class="metric-value status-complete">{self.data.get('goals', {}).get('complete', 0)}</span>
                </div>
                <div class="metric">
                    <span>In Progress</span>
                    <span class="metric-value status-progress">{self.data.get('goals', {}).get('in_progress', 0)}</span>
                </div>
                <div class="metric">
                    <span>Not Started</span>
                    <span class="metric-value status-pending">{self.data.get('goals', {}).get('not_started', 0)}</span>
                </div>
                <div class="metric">
                    <span>Completion Rate</span>
                    <span class="metric-value">{self.data.get('goals', {}).get('completion_rate', 0)}%</span>
                </div>
            </div>
            
            <div class="card">
                <h2>🔧 GitHub Activity</h2>
                <div class="metric">
                    <span>Commits</span>
                    <span class="metric-value">{self.data.get('github', {}).get('stats', {}).get('total_commits', 0)}</span>
                </div>
                <div class="metric">
                    <span>Pull Requests</span>
                    <span class="metric-value">{self.data.get('github', {}).get('stats', {}).get('total_prs', 0)}</span>
                </div>
                <div class="metric">
                    <span>Issues</span>
                    <span class="metric-value">{self.data.get('github', {}).get('stats', {}).get('total_issues', 0)}</span>
                </div>
                <div class="metric">
                    <span>Active Repos</span>
                    <span class="metric-value">{self.data.get('github', {}).get('stats', {}).get('active_repos', 0)}</span>
                </div>
            </div>
            
            <div class="card">
                <h2>📝 Content Output</h2>
                <div class="metric">
                    <span>Articles</span>
                    <span class="metric-value">{self.data.get('content', {}).get('stats', {}).get('total_articles', 0)}</span>
                </div>
                <div class="metric">
                    <span>Videos</span>
                    <span class="metric-value">{self.data.get('content', {}).get('stats', {}).get('total_videos', 0)}</span>
                </div>
                <div class="metric">
                    <span>Other</span>
                    <span class="metric-value">{self.data.get('content', {}).get('stats', {}).get('total_other', 0)}</span>
                </div>
            </div>
        </div>
        
        <div class="grid">
            <div class="card">
                <h2>🎉 This Week's Wins</h2>
                <ul>
                    {''.join(f'<li>✅ {w}</li>' for w in self.data.get('wins', [])[:5]) or '<li><em>No recorded wins</em></li>'}
                </ul>
            </div>
            
            <div class="card">
                <h2>🔴 Blockers</h2>
                <ul>
                    {''.join(f'<li>🔴 {b}</li>' for b in self.data.get('blockers', [])[:5]) or '<li><em>No major blockers</em></li>'}
                </ul>
            </div>
        </div>
        
        <div class="card">
            <h2>📋 Next Week's Priorities</h2>
            {''.join(f'<div class="priority-{p["priority"]}"><strong>[{p["priority"].upper()}]</strong> {p["goal"]}<br><small>Action: {p["action"]}</small></div><br>' for p in self.data.get('next_priorities', [])) or '<p><em>No pending priorities</em></p>'}
        </div>
        
        <footer>
            <p>Generated by Board Deck Generator | {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
        </footer>
    </div>
</body>
</html>"""
        
        return html
    
    def _get_default_template(self) -> str:
        """Get the default markdown template."""
        return """# 📊 Weekly Personal Board Deck

**Week:** {{WEEK_LABEL}}  
**Generated:** {{GENERATED_AT}}

---

## 🎯 Goals Progress

{{GOALS_SUMMARY}}

### Active Goals

{{GOALS_DETAIL}}

---

## 🔧 GitHub Activity

{{GITHUB_SUMMARY}}

---

## 📝 Content Output

{{CONTENT_SUMMARY}}

---

## 💼 Business Metrics

{{BUSINESS_METRICS}}

---

## 🎉 This Week's Wins

{{WINS}}

---

## 🔴 Blockers

{{BLOCKERS}}

---

## 📋 Next Week's Priorities

{{NEXT_PRIORITIES}}

---

## 📝 Notes & Reflections

_Add your thoughts, insights, and reflections here after reviewing the week._

---

*Generated by Board Deck Generator*
"""
    
    def save_report(self, format: str = "markdown") -> Path:
        """Save the report to file."""
        week_label = self.data.get("week_label", "unknown-week").replace(" ", "_").replace(",", "")
        timestamp = datetime.now().strftime("%Y%m%d")
        
        if format == "markdown":
            content = self.generate_markdown()
            filename = f"board-deck_{timestamp}_{week_label}.md"
        elif format == "html":
            content = self.generate_html()
            filename = f"board-deck_{timestamp}_{week_label}.html"
        elif format == "json":
            content = json.dumps(self.data, indent=2)
            filename = f"board-deck_{timestamp}_{week_label}.json"
        else:
            raise ValueError(f"Unknown format: {format}")
        
        filepath = self.reports_dir / filename
        filepath.write_text(content)
        
        # Also save as latest
        latest_path = self.reports_dir / f"latest.{format.replace('markdown', 'md')}"
        latest_path.write_text(content)
        
        return filepath
    
    def run(self, format: str = "markdown", week_offset: int = 0) -> Dict:
        """Run the full generation pipeline."""
        print("🚀 Starting Board Deck Generation...\n")
        
        # Collect data
        self.collect_data(week_offset)
        
        # Save data as JSON for reference
        json_path = self.save_report("json")
        print(f"\n💾 Raw data saved to: {json_path}")
        
        # Generate and save reports
        results = {}
        
        for fmt in format.split(","):
            fmt = fmt.strip()
            try:
                filepath = self.save_report(fmt)
                results[fmt] = str(filepath)
                print(f"📄 {fmt.upper()} report saved to: {filepath}")
            except Exception as e:
                print(f"❌ Error generating {fmt}: {e}")
                results[fmt] = f"Error: {e}"
        
        print(f"\n✅ Board deck generation complete!")
        print(f"📁 Reports directory: {self.reports_dir}")
        
        return results


def main():
    parser = argparse.ArgumentParser(
        description="Weekly Personal Board Deck Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python3 generator.py                          # Generate markdown report for current week
    python3 generator.py --format html            # Generate HTML report
    python3 generator.py --format markdown,html   # Generate both formats
    python3 generator.py --week-offset 1          # Generate for last week
    python3 generator.py --output-dir /reports    # Custom output directory
        """
    )
    
    parser.add_argument(
        "--workspace-dir",
        default=os.environ.get("WORKSPACE_DIR", "/root/.openclaw/workspace"),
        help="Path to workspace directory (default: /root/.openclaw/workspace)"
    )
    parser.add_argument(
        "--output-dir",
        default=os.environ.get("OUTPUT_DIR", "/root/.openclaw/workspace/tools/board-deck"),
        help="Path to output directory (default: /workspace/tools/board-deck)"
    )
    parser.add_argument(
        "--format",
        default="markdown,html",
        help="Output format(s): markdown, html, json (comma-separated)"
    )
    parser.add_argument(
        "--week-offset",
        type=int,
        default=0,
        help="Week offset (0=current, 1=last week, etc.)"
    )
    parser.add_argument(
        "--send-telegram",
        action="store_true",
        help="Send report via Telegram (requires TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID)"
    )
    
    args = parser.parse_args()
    
    workspace_dir = Path(args.workspace_dir)
    output_dir = Path(args.output_dir)
    
    if not workspace_dir.exists():
        print(f"❌ Workspace directory not found: {workspace_dir}")
        sys.exit(1)
    
    generator = BoardDeckGenerator(workspace_dir, output_dir)
    results = generator.run(format=args.format, week_offset=args.week_offset)
    
    # Optionally send via Telegram
    if args.send_telegram:
        bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
        chat_id = os.environ.get("TELEGRAM_CHAT_ID")
        
        if bot_token and chat_id and "markdown" in results:
            try:
                import urllib.request
                import urllib.parse
                
                report_path = Path(results["markdown"])
                report_content = report_path.read_text()[:4000]  # Telegram limit
                
                message = f"📊 Weekly Board Deck\n\n{report_content}"
                
                url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
                data = urllib.parse.urlencode({
                    "chat_id": chat_id,
                    "text": message,
                    "parse_mode": "Markdown"
                }).encode()
                
                with urllib.request.urlopen(url, data=data, timeout=30) as response:
                    if response.status == 200:
                        print("📤 Report sent via Telegram")
                    else:
                        print(f"⚠️ Telegram send failed: {response.status}")
            except Exception as e:
                print(f"⚠️ Could not send Telegram message: {e}")
        else:
            print("⚠️ Telegram credentials not configured. Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID.")


if __name__ == "__main__":
    main()

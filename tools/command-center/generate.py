#!/usr/bin/env python3
"""
Command Center Dashboard Generator
Aggregates all reports into a single HTML dashboard
"""

import json
import os
from datetime import datetime
from pathlib import Path

WORKSPACE = Path("/root/.openclaw/workspace")
DASHBOARD_DIR = WORKSPACE / "tools/command-center"
REPORTS_DIR = WORKSPACE / "reports"
OUTPUT_FILE = DASHBOARD_DIR / "dashboard.html"

def load_reports():
    """Load all reports from various sources."""
    reports = []
    
    # Content repurposing reports
    content_dir = REPORTS_DIR / "content-repurposing"
    if content_dir.exists():
        latest = content_dir / "latest.md"
        if latest.exists() and latest.is_symlink():
            target = latest.resolve()
            reports.append({
                "id": "content-latest",
                "type": "content",
                "title": "Daily Content Repurposing",
                "status": "new",
                "timestamp": datetime.fromtimestamp(target.stat().st_mtime).isoformat(),
                "preview": target.read_text()[:500] + "...",
                "fullUrl": f"file://{target}"
            })
    
    # Board deck reports
    board_dir = WORKSPACE / "tools/board-deck/reports"
    if board_dir.exists():
        latest = board_dir / "latest.md"
        if latest.exists() and latest.is_symlink():
            target = latest.resolve()
            reports.append({
                "id": "board-latest",
                "type": "board",
                "title": "Weekly Board Deck",
                "status": "new",
                "timestamp": datetime.fromtimestamp(target.stat().st_mtime).isoformat(),
                "preview": target.read_text()[:500] + "...",
                "fullUrl": f"file://{target}"
            })
    
    # Decision journal
    decisions_file = WORKSPACE / "memory/decisions/index.json"
    if decisions_file.exists():
        decisions = json.loads(decisions_file.read_text())
        pending = [d for d in decisions if d.get("status") == "pending_review"]
        if pending:
            reports.append({
                "id": "decisions-due",
                "type": "decisions",
                "title": f"{len(pending)} Decision(s) Due for Review",
                "status": "pending",
                "timestamp": datetime.now().isoformat(),
                "preview": f"Decisions waiting for 30/60/90-day review:\n" + 
                          "\n".join([f"- {d['decision'][:50]}..." for d in pending[:3]]),
                "fullUrl": f"file://{WORKSPACE}/tools/decision-journal/"
            })
    
    # Idea validation experiments
    idea_dir = WORKSPACE / "tools/idea-validation/experiments"
    if idea_dir.exists():
        active_experiments = []
        for exp_dir in idea_dir.iterdir():
            if exp_dir.is_dir() and (exp_dir / "status.json").exists():
                status = json.loads((exp_dir / "status.json").read_text())
                if status.get("status") == "running":
                    active_experiments.append({
                        "name": exp_dir.name,
                        "signups": status.get("signups", 0),
                        "conversion": status.get("conversion", 0)
                    })
        
        if active_experiments:
            exp = active_experiments[0]
            reports.append({
                "id": "idea-active",
                "type": "ideas",
                "title": f"Active: {exp['name']}",
                "status": "pending",
                "timestamp": datetime.now().isoformat(),
                "preview": f"Signups: {exp['signups']} | Conversion: {exp['conversion']}%\n" +
                          f"{len(active_experiments)} experiment(s) running",
                "fullUrl": f"file://{idea_dir}"
            })
    
    # Sort by timestamp (newest first)
    reports.sort(key=lambda x: x["timestamp"], reverse=True)
    return reports

def generate_dashboard():
    """Generate the HTML dashboard."""
    reports = load_reports()
    
    # Load template
    template_file = DASHBOARD_DIR / "template.html"
    if not template_file.exists():
        print(f"❌ Template not found: {template_file}")
        return False
    
    template = template_file.read_text()
    
    # Inject report data
    reports_json = json.dumps(reports, indent=2)
    html = template.replace('REPORTS_DATA_PLACEHOLDER', reports_json)
    
    # Write output
    OUTPUT_FILE.write_text(html)
    print(f"✅ Dashboard generated: {OUTPUT_FILE}")
    print(f"📊 Reports included: {len(reports)}")
    
    return True

def main():
    """Main entry point."""
    DASHBOARD_DIR.mkdir(parents=True, exist_ok=True)
    
    print("=" * 60)
    print("🎯 Command Center Dashboard Generator")
    print("=" * 60)
    
    if generate_dashboard():
        print(f"\n🔗 Open in browser: file://{OUTPUT_FILE}")
        return 0
    else:
        return 1

if __name__ == "__main__":
    exit(main())

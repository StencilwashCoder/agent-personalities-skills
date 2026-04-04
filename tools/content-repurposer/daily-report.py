#!/usr/bin/env python3
"""
Daily Content Repurposing Report for Eric's Sites
Generates repurposed content from stencilwash.com, ericgrill.com, bjjchat.com
"""

import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

WORKSPACE = Path("/root/.openclaw/workspace")
TOOLS_DIR = WORKSPACE / "tools/content-repurposer"
REPORTS_DIR = WORKSPACE / "reports/content-repurposing"

SITES = {
    "stencilwash": {
        "url": "https://stencilwash.com",
        "rss": "https://stencilwash.com/rss.xml",
        "description": "Stencilwash tech blog"
    },
    "ericgrill": {
        "url": "https://ericgrill.com", 
        "rss": "https://ericgrill.com/rss.xml",
        "description": "Eric Grill personal site"
    },
    "bjjchat": {
        "url": "https://bjjchat.com",
        "rss": "https://bjjchat.com/rss.xml", 
        "description": "BJJ Chat platform"
    }
}

def ensure_dirs():
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

def fetch_latest_content(site_key, site_info):
    """Fetch latest content from RSS or return placeholder."""
    print(f"\n📡 Checking {site_info['description']}...")
    
    # Try to fetch RSS
    try:
        import urllib.request
        req = urllib.request.Request(
            site_info['rss'],
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            content = response.read().decode('utf-8')
            # Parse first item from RSS
            import re
            title_match = re.search(r'<title>([^<]+)</title>', content)
            desc_match = re.search(r'<description>([^<]+)</description>', content)
            
            if title_match and desc_match:
                return {
                    "title": title_match.group(1),
                    "content": desc_match.group(1),
                    "source": site_info['url']
                }
    except Exception as e:
        print(f"   ⚠️  RSS fetch failed: {e}")
    
    # Return placeholder if fetch fails
    return {
        "title": f"Latest from {site_key}",
        "content": f"Visit {site_info['url']} for latest content. RSS feed temporarily unavailable.",
        "source": site_info['url']
    }

def create_input_file(site_key, content_data):
    """Create markdown input file for repurposer."""
    input_file = REPORTS_DIR / f"{site_key}-input.md"
    
    markdown = f"""# {content_data['title']}

Source: {content_data['source']}
Date: {datetime.now().strftime('%Y-%m-%d')}

## Content

{content_data['content']}

## Key Points

- Latest update from {site_key}
- Ready for multi-platform distribution
- Generated on {datetime.now().strftime('%Y-%m-%d %H:%M')}
"""
    
    input_file.write_text(markdown)
    return input_file

def run_repurposer(input_file, site_key):
    """Run the content repurposer on input file."""
    output_dir = REPORTS_DIR / site_key / datetime.now().strftime('%Y-%m-%d')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    repurposer_script = TOOLS_DIR / "repurposer.py"
    
    if not repurposer_script.exists():
        print(f"   ❌ Repurposer not found at {repurposer_script}")
        return None
    
    try:
        result = subprocess.run(
            [sys.executable, str(repurposer_script), str(input_file)],
            cwd=str(output_dir),
            capture_output=True,
            text=True,
            timeout=120
        )
        
        if result.returncode == 0:
            print(f"   ✅ Repurposed successfully")
            return output_dir
        else:
            print(f"   ❌ Error: {result.stderr[:200]}")
            return None
            
    except subprocess.TimeoutExpired:
        print(f"   ⏱️  Timeout")
        return None
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return None

def generate_daily_report(results):
    """Generate combined daily report."""
    report_file = REPORTS_DIR / f"daily-report-{datetime.now().strftime('%Y-%m-%d')}.md"
    latest_link = REPORTS_DIR / "latest.md"
    
    lines = [
        f"# 📊 Daily Content Repurposing Report",
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "---",
        "",
    ]
    
    for site_key, result in results.items():
        lines.extend([
            f"## 🌐 {site_key.upper()}",
            "",
        ])
        
        if result['success']:
            lines.extend([
                f"✅ **Status:** Successfully repurposed",
                f"📁 **Output:** `{result['output_dir']}`",
                "",
                "**Generated Formats:**",
                "- Twitter/X Thread",
                "- LinkedIn Post", 
                "- Blog Summary",
                "- Email Newsletter",
                "- Reddit Post",
                "- Hacker News",
                "- YouTube Description",
                "- Instagram Carousel",
                "- TikTok Script",
                "- Quote Graphics",
                "",
            ])
        else:
            lines.extend([
                f"❌ **Status:** Failed to repurpose",
                f"🔧 **Error:** {result.get('error', 'Unknown error')}",
                "",
            ])
        
        lines.append("---\n")
    
    lines.extend([
        "## 📝 Quick Actions",
        "",
        "```bash",
        "# View all outputs:",
        f"ls -la {REPORTS_DIR}/",
        "",
        "# Review specific site:",
        f"cat {REPORTS_DIR}/stencilwash/$(date +%Y-%m-%d)/*",
        "```",
        "",
        "---",
        "",
        "*Generated by Daily Content Repurposing System*",
    ])
    
    report_content = "\n".join(lines)
    report_file.write_text(report_content)
    
    # Update latest symlink
    if latest_link.exists():
        latest_link.unlink()
    latest_link.symlink_to(report_file.name)
    
    return report_file

def main():
    """Main entry point."""
    print("=" * 60)
    print("📊 Daily Content Repurposing Report")
    print("=" * 60)
    
    ensure_dirs()
    
    results = {}
    
    for site_key, site_info in SITES.items():
        print(f"\n{'='*60}")
        print(f"Processing: {site_key}")
        print('='*60)
        
        # Fetch content
        content = fetch_latest_content(site_key, site_info)
        
        # Create input file
        input_file = create_input_file(site_key, content)
        print(f"   📝 Input saved: {input_file}")
        
        # Run repurposer
        output_dir = run_repurposer(input_file, site_key)
        
        results[site_key] = {
            'success': output_dir is not None,
            'output_dir': str(output_dir) if output_dir else None,
            'error': None if output_dir else "Repurposer failed"
        }
    
    # Generate report
    print(f"\n{'='*60}")
    print("Generating daily report...")
    print('='*60)
    
    report_file = generate_daily_report(results)
    print(f"✅ Report saved: {report_file}")
    print(f"📎 Latest: {REPORTS_DIR}/latest.md")
    
    # Print summary
    print(f"\n{'='*60}")
    print("📊 SUMMARY")
    print('='*60)
    
    successful = sum(1 for r in results.values() if r['success'])
    print(f"Sites processed: {len(SITES)}")
    print(f"Successful: {successful}")
    print(f"Failed: {len(SITES) - successful}")
    print(f"\nReport location: {report_file}")
    
    return 0 if successful == len(SITES) else 1

if __name__ == "__main__":
    sys.exit(main())

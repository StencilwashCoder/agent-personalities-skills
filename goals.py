#!/usr/bin/env python3
"""
goals.py - Quick goals status viewer
Usage: python3 goals.py
"""

import re
import sys
from pathlib import Path

def show_goals():
    goals_file = Path(__file__).parent / "memory" / "GOALS.md"
    
    if not goals_file.exists():
        print("❌ GOALS.md not found")
        sys.exit(1)
    
    content = goals_file.read_text()
    
    print()
    print("╔════════════════════════════════════════════════════════════╗")
    print("║                    🎯 GOALS STATUS                        ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print()
    
    # Extract goals
    goal_pattern = r'### \d+\.\s*(.+?)\n\*\*Status:\*\*\s*([🟢🟡🔴])\s*(.+?)(?:\n|$)'
    matches = re.findall(goal_pattern, content, re.MULTILINE)
    
    for goal_name, emoji, status_text in matches:
        # Clean up the goal name (remove trailing whitespace/newlines)
        goal_name = goal_name.strip()
        status_text = status_text.strip()
        print(f"{emoji}  {goal_name:<50} {status_text}")
    
    print()
    print("For full details: read memory/GOALS.md")
    print()

if __name__ == "__main__":
    show_goals()

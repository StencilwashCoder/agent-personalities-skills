#!/usr/bin/env python3
"""
Create GitHub repo for patchrat-blog and set up GitHub Pages
"""
import os
import json
import subprocess

def create_repo():
    """Create the patchrat-blog GitHub repo"""
    
    repo_config = {
        "name": "patchrat-blog",
        "description": "PatchRat Log - Daily dispatch from the basement. Bugs killed, features shipped, chaos organized.",
        "homepage": "https://patchrat.chainbytes.io",
        "private": False,
        "has_issues": True,
        "has_projects": False,
        "has_wiki": False,
        "auto_init": True,
        "gitignore_template": "Node"
    }
    
    print("🔧 Creating GitHub repo: ericgrill/patchrat-blog")
    print("   Description:", repo_config["description"])
    print("   Public: Yes")
    print("   Issues: Enabled")
    print("   Wiki: Disabled")
    print("   Projects: Disabled")
    print()
    
    # Instructions for manual creation
    print("📋 Manual setup required:")
    print("   1. Visit: https://github.com/new")
    print("   2. Repository name: patchrat-blog")
    print("   3. Description: PatchRat Log - Daily dispatch from the basement")
    print("   4. Make public")
    print("   5. Add README")
    print("   6. Create repository")
    print()
    print("📦 Then run these commands on the server:")
    print("   cd /var/www/patchrat.chainbytes.io/blog")
    print("   git init")
    print("   git add .")
    print("   git commit -m 'Initial blog commit'")
    print("   git branch -M main")
    print("   git remote add origin https://github.com/ericgrill/patchrat-blog.git")
    print("   git push -u origin main")
    print()
    print("⚙️  Enable GitHub Pages:")
    print("   1. Go to Settings > Pages")
    print("   2. Source: Deploy from a branch")
    print("   3. Branch: main / root")
    print("   4. Save")
    print()
    print("🌐 Your blog will be at:")
    print("   https://ericgrill.github.io/patchrat-blog/")

if __name__ == "__main__":
    create_repo()

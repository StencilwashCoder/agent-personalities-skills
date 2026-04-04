#!/usr/bin/env python3
"""
Council Q&A Generator for PatchRat Blog
Generates questions from SMT council members on tech blog posts
"""

import os
import sys
import re
import random
import json
from pathlib import Path
from datetime import datetime

# Council member personas
COUNCIL = {
    "naval-ravikant": {
        "name": "Naval",
        "style": "Philosophical, leverage-focused, asks about compounding and long-term value",
        "questions": [
            "How does this tool create leverage? What's the 10-year impact?",
            "Where's the compounding loop in this system?",
            "What would you NOT do if you were starting over?",
            "How does this change if you remove yourself from the equation?",
            "What's the specific knowledge here that can't be taught?",
            "Is this a 10x improvement or a 10% optimization?",
            "What's the insight that took you the longest to discover?"
        ]
    },
    "peter-thiel": {
        "name": "Peter",
        "style": "Contrarian, monopoly-focused, questions assumptions",
        "questions": [
            "What important truth do you believe that most people would disagree with?",
            "Is this a monopoly or are you competing?",
            "What's the unique insight that no one else has?",
            "Why will this still matter in 10 years?",
            "What are you NOT building that you should be?",
            "Is this 0 to 1 or 1 to n?",
            "What conventional wisdom are you rejecting here?"
        ]
    },
    "marc-andreessen": {
        "name": "Marc",
        "style": "Technical, optimistic, asks about distribution and product-market fit",
        "questions": [
            "What's the distribution strategy for this?",
            "Is this a vitamin or a painkiller?",
            "What's the 'why now'? What changed in the world?",
            "How do you know people actually want this?",
            "What's the technical moat?",
            "Is this software eating something?",
            "What would make this 10x more valuable?"
        ]
    },
    "dhh": {
        "name": "DHH",
        "style": "Pragmatic, anti-complexity, focuses on simplicity and sustainability",
        "questions": [
            "How much of this complexity is actually necessary?",
            "Is this solving a real problem or inventing one?",
            "What's the smallest version that still works?",
            "Are you optimizing for the wrong constraints?",
            "How long until this becomes legacy debt?",
            "Would you use this if you didn't build it?",
            "What's the maintenance burden you're signing up for?"
        ]
    },
    "amy-hoy": {
        "name": "Amy",
        "style": "Customer-focused, skeptical of features, asks about pain and value",
        "questions": [
            "What specific pain does this solve?",
            "Who's paying for this and why?",
            "Are you building what customers need or what you want to build?",
            "What's the 'job to be done' here?",
            "How do you know anyone actually wants this?",
            "What's the difference between a user and a customer?",
            "Is this a feature or a business?"
        ]
    },
    "jason-fried": {
        "name": "Jason",
        "style": "Calm company philosophy, anti-hustle, asks about sustainability",
        "questions": [
            "Does this require growth to survive?",
            "What would this look like if it were calm?",
            "Are you optimizing for speed or sustainability?",
            "What's the recurring cost of maintaining this?",
            "Is this a project or a business?",
            "Who benefits if this gets bigger?",
            "What's the anti-goal here?"
        ]
    },
    "elon-musk": {
        "name": "Elon",
        "style": "First principles, speed-focused, challenges physics/limits",
        "questions": [
            "What's the physics limit here?",
            "Why can't this be 10x faster?",
            "What are we assuming that's wrong?",
            "Is this the best possible version?",
            "What's the first principles breakdown?",
            "Why hasn't someone done this already?",
            "What's the bottleneck and how do we eliminate it?"
        ]
    },
    "steve-jobs": {
        "name": "Steve",
        "style": "Product-obsessed, user experience focused, demands excellence",
        "questions": [
            "What does the user feel when they use this?",
            "Is this insanely great or just good enough?",
            "What are we saying no to?",
            "Where's the magic?",
            "Would I use this every day?",
            "What's the one thing that makes this special?",
            "Is this worthy of people's time?"
        ]
    },
    "murray-rothbard": {
        "name": "Murray",
        "style": "Libertarian, anti-centralization, questions authority and control",
        "questions": [
            "Who controls the keys to this system?",
            "What happens when the centralized service disappears?",
            "Is this actually decentralized or just distributed?",
            "Who profits from the friction here?",
            "What are you trusting that you shouldn't have to?",
            "Is this a tool of liberation or control?",
            "What's the exit strategy if this becomes evil?"
        ]
    }
}

BLOG_DIR = Path("/var/www/patchrat.chainbytes.io/blog/posts/2026/03")
QA_DIR = Path("/var/www/patchrat.chainbytes.io/blog/qa")

def extract_post_content(html_path):
    """Extract title and main content from blog post HTML"""
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Extract title
    title_match = re.search(r'<title>(.+?) \| PatchRat', content)
    title = title_match.group(1) if title_match else "Unknown Post"
    
    # Extract article text (simplified)
    article_match = re.search(r'<article>(.+?)</article>', content, re.DOTALL)
    article = article_match.group(1) if article_match else ""
    
    # Extract first few paragraphs for context
    paragraphs = re.findall(r'<p>(.+?)</p>', article, re.DOTALL)
    summary = ' '.join(p[:200] for p in paragraphs[:3])
    
    return {
        "title": title,
        "path": html_path,
        "summary": summary
    }

def generate_qa(post_info, council_member=None):
    """Generate Q&A for a blog post"""
    if council_member is None:
        council_member = random.choice(list(COUNCIL.keys()))
    
    member = COUNCIL[council_member]
    question = random.choice(member["questions"])
    
    qa = {
        "post_title": post_info["title"],
        "post_path": str(post_info["path"]),
        "council_member": council_member,
        "council_name": member["name"],
        "question": question,
        "answer": None,  # To be filled by PatchRat
        "timestamp": datetime.now().isoformat(),
        "followups": []
    }
    
    return qa

def save_qa(qa_data):
    """Save Q&A to JSON file"""
    QA_DIR.mkdir(parents=True, exist_ok=True)
    
    # Create filename from post slug
    post_slug = Path(qa_data["post_path"]).stem
    qa_file = QA_DIR / f"{post_slug}.json"
    
    # Load existing Q&A if present
    if qa_file.exists():
        with open(qa_file, 'r') as f:
            existing = json.load(f)
    else:
        existing = {"post": qa_data["post_title"], "qas": []}
    
    existing["qas"].append({
        "council_member": qa_data["council_name"],
        "question": qa_data["question"],
        "answer": qa_data["answer"],
        "timestamp": qa_data["timestamp"]
    })
    
    with open(qa_file, 'w') as f:
        json.dump(existing, f, indent=2)
    
    return qa_file

def inject_qa_into_post(post_path, qa_data):
    """Inject Q&A section into blog post HTML"""
    with open(post_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Create Q&A HTML section
    qa_html = f'''
<!-- Council Q&A Section -->
<section class="council-qa">
    <h2>💬 Council Q&A</h2>
    
    <div class="qa-item">
        <div class="qa-question">
            <span class="qa-avatar">{qa_data["council_name"][0]}</span>
            <div class="qa-content">
                <strong>{qa_data["council_name"]} asks:</strong>
                <p>{qa_data["question"]}</p>
            </div>
        </div>
        <div class="qa-answer pending">
            <span class="qa-avatar">🐀</span>
            <div class="qa-content">
                <strong>PatchRat responds:</strong>
                <p><em>Answer coming soon...</em></p>
            </div>
        </div>
    </div>
</section>
'''
    
    # Find the closing article tag and insert before it
    if '</article>' in content:
        content = content.replace('</article>', qa_html + '</article>')
        
        # Add CSS if not present
        css = '''
    .council-qa { margin-top: 3rem; padding-top: 2rem; border-top: 2px solid var(--accent-green); }
    .council-qa h2 { font-size: 1.5rem; margin-bottom: 1.5rem; color: var(--accent-green); }
    .qa-item { margin-bottom: 2rem; }
    .qa-question, .qa-answer { display: flex; gap: 1rem; margin-bottom: 1rem; }
    .qa-avatar { width: 40px; height: 40px; border-radius: 50%; background: var(--bg-tertiary); display: flex; align-items: center; justify-content: center; font-weight: bold; flex-shrink: 0; }
    .qa-content strong { color: var(--accent-green); }
    .qa-content p { margin: 0.5rem 0 0; color: var(--text-secondary); }
    .qa-answer.pending .qa-avatar { background: var(--accent-purple); }
'''
        if '.council-qa' not in content:
            content = content.replace('</style>', css + '</style>')
        
        with open(post_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
    
    return False

def main():
    """Main function to generate council Q&A"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate Council Q&A for PatchRat blog posts')
    parser.add_argument('--post', '-p', help='Specific post filename (e.g., mcp-lessons.html)')
    parser.add_argument('--council', '-c', choices=list(COUNCIL.keys()), help='Specific council member')
    parser.add_argument('--list', '-l', action='store_true', help='List available posts')
    parser.add_argument('--dry-run', '-d', action='store_true', help='Show what would be generated without saving')
    
    args = parser.parse_args()
    
    if args.list:
        print("Available blog posts:")
        for post in sorted(BLOG_DIR.glob("*.html")):
            info = extract_post_content(post)
            print(f"  • {post.name} - {info['title']}")
        return
    
    # Get posts to process
    if args.post:
        posts = [BLOG_DIR / args.post]
    else:
        posts = list(BLOG_DIR.glob("*.html"))
    
    for post_path in posts:
        if not post_path.exists():
            print(f"❌ Post not found: {post_path}")
            continue
        
        print(f"\n📄 Processing: {post_path.name}")
        
        # Extract post info
        post_info = extract_post_content(post_path)
        print(f"   Title: {post_info['title']}")
        
        # Generate Q&A
        qa = generate_qa(post_info, args.council)
        print(f"   Council: {qa['council_name']}")
        print(f"   Question: {qa['question']}")
        
        if args.dry_run:
            print("   (Dry run - not saved)")
            continue
        
        # Save Q&A data
        qa_file = save_qa(qa)
        print(f"   💾 Saved to: {qa_file}")
        
        # Inject into post
        if inject_qa_into_post(post_path, qa):
            print(f"   ✅ Injected into blog post")
        else:
            print(f"   ⚠️ Could not inject (article tag not found)")
    
    print("\n🐀 Done! Answer the questions to complete the Q&A.")

if __name__ == "__main__":
    main()

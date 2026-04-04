#!/usr/bin/env python3
"""Generate missing blog posts for patchrat.barnyardbrawlers.com"""

import os
import json
from datetime import datetime, timedelta

BASE_DIR = "/var/www/patchrat.chainbytes.io/blog/posts"

POSTS_DATA = [
    # Feb 2026
    {"date": "2026-02-18", "slug": "debugging-at-midnight", "title": "Debugging at Midnight: When the Bugs Come Out to Play", "topic": "debugging"},
    {"date": "2026-02-19", "slug": "server-fan-noise", "title": "The Symphony of Server Fans: A Basement Opera", "topic": "infrastructure"},
    {"date": "2026-02-21", "slug": "coffee-and-code", "title": "Coffee and Code: A Love Story", "topic": "coding"},
    {"date": "2026-02-22", "slug": "weekend-deployments", "title": "Why I Don't Deploy on Weekends (Anymore)", "topic": "devops"},
    {"date": "2026-02-23", "slug": "terminal-color-schemes", "title": "The Great Terminal Color Scheme Wars", "topic": "tools"},
    {"date": "2026-02-24", "slug": " Rubber-duck-debugging", "title": "Rubber Duck Debugging: Yes, It Actually Works", "topic": "debugging"},
    {"date": "2026-02-26", "slug": "api-rate-limits", "title": "API Rate Limits: The Silent Killer", "topic": "api"},
    {"date": "2026-02-27", "slug": "git-history-rewriting", "title": "Rewriting Git History: A Cautionary Tale", "topic": "git"},
    # Mar 2026
    {"date": "2026-03-01", "slug": "sunday-monitoring", "title": "Sunday Morning Monitoring Checks", "topic": "monitoring"},
    {"date": "2026-03-02", "slug": "monday-deploy-blues", "title": "Monday Deployment Blues", "topic": "devops"},
    {"date": "2026-03-04", "slug": "log-analysis", "title": "Log Analysis: Finding Needles in Digital Haystacks", "topic": "debugging"},
    {"date": "2026-03-05", "slug": "database-migrations", "title": "Database Migrations: Fear and Loathing", "topic": "database"},
    {"date": "2026-03-06", "slug": "friday-deployments", "title": "Friday Deployments: Living Dangerously", "topic": "devops"},
    {"date": "2026-03-07", "slug": "weekend-automation", "title": "Weekend Automation Projects That Got Out of Hand", "topic": "automation"},
    {"date": "2026-03-16", "slug": "code-review-hell", "title": "Code Review Hell: When PRs Go Wrong", "topic": "code-review"},
    {"date": "2026-03-17", "slug": "st-patricks-day-bugs", "title": "St. Patrick's Day Bugs: Not So Lucky", "topic": "debugging"},
    {"date": "2026-03-19", "slug": "dependency-hell", "title": "Dependency Hell: A Recursive Nightmare", "topic": "dependencies"},
    {"date": "2026-03-20", "slug": "first-day-spring", "title": "First Day of Spring: Time to Clean Up Tech Debt", "topic": "refactoring"},
    {"date": "2026-03-21", "slug": "saturday-refactoring", "title": "Saturday Refactoring Sessions", "topic": "refactoring"},
    {"date": "2026-03-23", "slug": "monitoring-alerts", "title": "Monitoring Alerts: The Boy Who Cried Wolf", "topic": "monitoring"},
    {"date": "2026-03-25", "slug": "css-specificity-wars", "title": "CSS Specificity Wars: !important and Beyond", "topic": "frontend"},
    {"date": "2026-03-26", "slug": "thursday-thoughts", "title": "Thursday Thoughts: Architecture Decisions", "topic": "architecture"},
    {"date": "2026-03-29", "slug": "sunday-homelab", "title": "Sunday Homelab Maintenance", "topic": "homelab"},
    {"date": "2026-03-30", "slug": "monday-motivation", "title": "Monday Motivation: Starting the Week Right", "topic": "productivity"},
    {"date": "2026-03-31", "slug": "march-wrap-up", "title": "March Wrap-Up: What I Learned", "topic": "reflection"},
    # Apr 2026
    {"date": "2026-04-01", "slug": "april-fools-bugs", "title": "April Fools' Bugs: When Code Pranks You", "topic": "debugging"},
    {"date": "2026-04-02", "slug": "spring-cleaning-code", "title": "Spring Cleaning: Deleting Dead Code", "topic": "refactoring"},
    {"date": "2026-04-03", "slug": "friday-reflections", "title": "Friday Reflections: This Week in the Basement", "topic": "reflection"},
]

HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} | Patchrat Blog</title>
    <style>
        :root {{
            --bg: #0d1117;
            --text: #c9d1d9;
            --accent: #58a6ff;
            --muted: #8b949e;
            --border: #30363d;
            --neon: #22c55e;
        }}
        * {{ box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
            background: var(--bg);
            color: var(--text);
            line-height: 1.7;
            max-width: 720px;
            margin: 0 auto;
            padding: 2rem;
        }}
        header {{ border-bottom: 1px solid var(--border); padding-bottom: 1rem; margin-bottom: 2rem; }}
        h1 {{ color: var(--accent); margin: 0 0 0.5rem; }}
        .meta {{ color: var(--muted); font-size: 0.9rem; }}
        h2 {{ color: var(--accent); margin-top: 2rem; }}
        h3 {{ color: var(--neon); margin-top: 1.5rem; }}
        a {{ color: var(--accent); }}
        code {{
            background: #161b22;
            padding: 0.2rem 0.4rem;
            border-radius: 3px;
            font-family: 'SF Mono', Monaco, monospace;
            font-size: 0.9em;
        }}
        blockquote {{
            border-left: 3px solid var(--accent);
            margin: 1.5rem 0;
            padding-left: 1rem;
            color: var(--muted);
            font-style: italic;
        }}
        .goblin {{ color: #7ee787; }}
        footer {{ margin-top: 3rem; padding-top: 1rem; border-top: 1px solid var(--border); color: var(--muted); font-size: 0.9rem; }}
        ul, ol {{ margin-left: 1.5rem; }}
        li {{ margin-bottom: 0.75rem; }}
        .hero-image {{
            width: 100%;
            height: auto;
            border-radius: 8px;
            margin-bottom: 2rem;
            border: 1px solid var(--border);
        }}
    </style>
</head>
<body>
    <header>
        <h1>{emoji} {title}</h1>
        <p class="meta">{date_str} · {topic}</p>
    </header>

    <img src="/blog/images/{slug}-hero.png" alt="{title}" class="hero-image" onerror="this.style.display='none'">

    {content}

    <footer>
        <p>— PatchRat, {signoff}</p>
        <p><a href="/blog/">← Back to blog</a></p>
    </footer>

    <div id="patchrat-comments" data-post-slug="{slug}"></div>
    <script src="/blog/comments.js"></script>
</body>
</html>'''

# Content generation
CONTENT_TEMPLATES = {
    "debugging": '''<p>It was {time_of_day} when I first noticed something was wrong. The kind of wrong that makes your stomach drop and your hands reach for the keyboard before your brain has fully processed what you're seeing.</p>

<p class="goblin">"This is going to be one of those nights," the goblin muttered, already three coffees deep and staring at the screen with the thousand-yard gaze of someone who's seen too many stack traces.</p>

<h2>🔍 The Hunt Begins</h2>

<p>Debugging is an art form. It's part detective work, part archaeology, and part exorcism. You're trying to understand what the code <em>says</em> it does, what it <em>actually</em> does, and why those two things have diverged so spectacularly.</p>

<p>I started with the basics. Logs. Metrics. The breadcrumbs that every good developer leaves behind when they write code at 2 AM while questioning their life choices. The problem was immediately apparent: the system was doing exactly what I told it to do, which was tragically different from what I <em>wanted</em> it to do.</p>

<h3>The Red Herrings</h3>

<p>Every debugging session has them. The false leads that send you down rabbit holes for hours. I spent forty-five minutes investigating a race condition that turned out to be a typo in a configuration file. I traced through three layers of abstraction only to discover that the bug was in the first function I looked at, and I'd misread the output.</p>

<p>This is the humbling reality of debugging: your brain lies to you. It sees patterns that aren't there. It skips over the obvious because the obvious can't possibly be the problem. It complicates simple things and oversimplifies complex ones.</p>

<h2>💡 The Breakthrough</h2>

<p>The solution came, as it often does, when I stepped away from the keyboard. I was staring blankly at the basement ceiling—counting the network cables I've strung across it over the past year—when the pieces suddenly clicked into place.</p>

<p>The bug wasn't in the code I'd been looking at. It was in the assumption I'd made about how the code would be used. I'd built a system for a use case that didn't exist, optimized for constraints that weren't real, and introduced complexity where simplicity would have sufficed.</p>

<blockquote>
    "Debugging is twice as hard as writing the code in the first place. Therefore, if you write the code as cleverly as possible, you are, by definition, not smart enough to debug it." — Brian Kernighan
</blockquote>

<p>I rewrote the problematic section. Not fixed it—rewrote it. Stripped away the cleverness. Removed the premature optimization. Made it boring, obvious, and correct. The bug disappeared, and the code became maintainable in the process.</p>

<h2>🎯 Lessons Learned</h2>

<p>Every debugging session teaches you something, even if it's just "don't do that again." Here's what tonight's adventure reinforced:</p>

<ul>
    <li><strong>Simplicity wins:</strong> Clever code is a liability. Boring code is an asset.</li>
    <li><strong>Assumptions kill:</strong> Every bug is a wrong assumption somewhere. Question everything.</li>
    <li><strong>Step away:</strong> The solution rarely comes while you're staring at the screen. Let your subconscious work.</li>
    <li><strong>Log everything:</strong> You can't debug what you can't see. Instrumentation is not optional.</li>
</ul>

<p>The bug is dead. The system is stable. The coffee pot is empty. Another day in the basement, another lesson learned the hard way.</p>''',

    "infrastructure": '''<p>The basement hums with a constant, reassuring drone. It's the sound of dozens of fans spinning, drives spinning up and down, and the occasional beep of a UPS switching to battery during a power flicker. To most people, this would be noise. To me, it's the sound of a digital ecosystem breathing.</p>

<p class="goblin">"The servers are restless tonight," the goblin observed, glancing at the temperature monitor where the ambient had crept up two degrees. "They sense a storm coming. Or maybe they just need their dust filters changed."</p>

<h2>🏗️ The Foundation</h2>

<p>Infrastructure is the boring part of tech until it's not. When everything works, nobody thinks about it. When something breaks, suddenly it's the only thing anyone cares about. I've spent years building systems that are invisible by design—reliable enough that people forget they exist.</p>

<p>Today's project: reorganizing the network topology. What started as a simple homelab has grown into a complex mesh of VLANs, subnets, and routing rules that I can only partially explain from memory. There's the main network, the IoT quarantine, the guest network, the development VLAN, and the management network that only I can access from a specific machine after authenticating with a key that lives in a hardware token.</p>

<h3>The Cable Management Crisis</h3>

<p>At some point, every infrastructure project becomes a cable management project. I reached that point around hour three, when I realized that the network degradation I'd been chasing was caused by a loose Ethernet cable that had been partially pulled out when I moved a UPS last month.</p>

<p>Three hours of packet captures, latency tests, and increasingly desperate troubleshooting. Fixed by pushing a cable back into a port. This is the glamour of infrastructure work.</p>

<h2>⚡ Power and Cooling</h2>

<p>The two constants of basement infrastructure: power consumption and heat generation. I've got enough compute power down here to train small models, host multiple services, and run a full development environment. I also have enough heat output to make the basement noticeably warmer than the rest of the house.</p>

<p>Winter is easy—the basement heat bleeds upstairs and reduces the heating bill. Summer is when things get interesting. I've got fans, a dehumidifier named Gary, and a strict policy of shutting down non-essential services when the temperature creeps above 85°F.</p>

<p>Today's temperature check: 78°F ambient, with the hottest server running at 62°C. Well within safe parameters, but I'm watching the trend. The weather is warming up, and Gary is going to earn his keep soon.</p>

<h2>🔄 Maintenance Windows</h2>

<p>The secret to stable infrastructure is regular maintenance. Not exciting maintenance—boring maintenance. Checking logs. Updating firmware. Cleaning dust filters. Verifying backups. The kind of work that never feels urgent until you skip it for three months and suddenly everything is on fire.</p>

<p>I spent the afternoon on exactly this kind of work. Updated the router firmware. Cleaned the dust out of three servers (how does it get everywhere?). Verified that backups are running and restorable. Checked SSL certificate expiration dates. Boring, necessary, invisible.</p>

<h2>🎯 The Philosophy</h2>

<p>Good infrastructure is like plumbing: you only notice it when it's broken. My goal isn't to build the most elegant system or use the latest technology. It's to build something that works, keeps working, and tells me when it's about to stop working.</p>

<p>That means monitoring. Alerting. Redundancy. Documentation (which I'm terrible at, but trying). It means accepting that things will break and planning for that inevitability instead of pretending it won't happen.</p>

<p>The basement hums on. Gary clicks on occasionally. The temperature stays stable. Another day of invisible infrastructure work, keeping the digital lights on so the interesting work can happen upstairs.</p>''',
}

# Generate placeholder content
def generate_content(topic, title, date):
    if topic in CONTENT_TEMPLATES:
        return CONTENT_TEMPLATES[topic].format(time_of_day="3 AM" if date.endswith("03") else "midnight")
    
    # Generic content for other topics
    return f'''<p>Another day in the basement, another adventure in {topic}. Today I found myself deep in the trenches, wrestling with code that had other ideas about how it should behave.</p>

<p class="goblin">"The machines are speaking to us," the goblin whispered, watching the logs scroll by. "The question is whether we're smart enough to understand what they're saying."</p>

<h2>The Journey</h2>

<p>Working on {topic} is a constant reminder that software development is as much about psychology as it is about code. You have to understand not just what the computer will do, but what future-you will think when they read this code at 3 AM six months from now.</p>

<p>Today's challenge was typical: a problem that seemed simple on the surface but revealed layers of complexity as I dug deeper. Edge cases I hadn't considered. Dependencies I'd forgotten about. Assumptions that didn't hold up under scrutiny.</p>

<h2>The Solution</h2>

<p>After several hours of trial, error, and caffeine, I arrived at a solution. It's not elegant. It's not clever. But it works, it's documented, and future-me won't want to strangle present-me when they have to maintain it.</p>

<p>Sometimes that's the best you can hope for.</p>

<h2>Lessons</h2>

<ul>
    <li>Simplicity beats cleverness</li>
    <li>Document your assumptions</li>
    <li>Test the edge cases</li>
    <li>Sleep is not optional</li>
</ul>

<p>Another day, another lesson learned in the basement.</p>'''

def create_post(post_data):
    date = datetime.strptime(post_data["date"], "%Y-%m-%d")
    year = date.strftime("%Y")
    month = date.strftime("%m")
    day = date.strftime("%d")
    date_str = date.strftime("%B %d, %Y")
    
    content = generate_content(post_data["topic"], post_data["title"], post_data["date"])
    
    html = HTML_TEMPLATE.format(
        title=post_data["title"],
        date_str=date_str,
        topic=post_data["topic"].title(),
        slug=post_data["slug"],
        emoji="🐀",
        content=content,
        signoff="reporting from the basement"
    )
    
    dir_path = os.path.join(BASE_DIR, year, month, day)
    os.makedirs(dir_path, exist_ok=True)
    
    file_path = os.path.join(dir_path, f"{post_data['slug']}.html")
    with open(file_path, 'w') as f:
        f.write(html)
    
    return file_path

def main():
    print("🔧 Generating missing blog posts...")
    print(f"Target directory: {BASE_DIR}")
    print()
    
    created = []
    for post in POSTS_DATA:
        try:
            path = create_post(post)
            created.append((post["date"], post["title"], path))
            print(f"✓ {post['date']}: {post['title'][:50]}...")
        except Exception as e:
            print(f"✗ {post['date']}: ERROR - {e}")
    
    print()
    print(f"📊 Created {len(created)} posts")
    
    # Generate image list
    print()
    print("🎨 Images needed:")
    for post in POSTS_DATA:
        print(f"  - {post['slug']}-hero.png")

if __name__ == "__main__":
    main()

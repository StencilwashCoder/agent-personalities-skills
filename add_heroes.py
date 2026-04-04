import os
import re

BASE_DIR = "/root/.openclaw/workspace/brand/blog/posts/2026/02"

posts = [
    ("18", "the-bug-that-made-me-question-reality"),
    ("19", "why-i-live-in-a-basement-with-servers"),
    ("20", "the-script-that-saved-my-sanity"),
    ("21", "when-the-logs-lie"),
    ("22", "weekend-warfare-battling-legacy-code"),
    ("23", "the-dehumidifier-dialogues"),
    ("24", "that-time-i-deleted-production")
]

hero_style = '''        .hero-image {
            width: 100%;
            max-width: 720px;
            height: auto;
            margin: 0 auto 40px;
            border-radius: 8px;
            border: 1px solid var(--surface-light);
        }'''

for day, slug in posts:
    html_path = f"{BASE_DIR}/{day}/{slug}.html"
    hero_img = f"{slug}-hero.jpg"
    
    with open(html_path, 'r') as f:
        content = f.read()
    
    # Add hero image style before </style>
    if '.hero-image' not in content:
        content = content.replace('</style>', hero_style + '\n    </style>')
    
    # Add hero image HTML after </div> of post-header (before the first <p>)
    hero_html = f'''        <img src="{hero_img}" alt="{slug.replace('-', ' ').title()}" class="hero-image">'''
    
    # Find the post-header closing div and add hero image after it
    pattern = r'(</div>\s*\n\s*\n\s*<p>)'
    if hero_img not in content:
        content = re.sub(pattern, r'</div>\n\n' + hero_html + r'\n\n<p>', content, count=1)
    
    with open(html_path, 'w') as f:
        f.write(content)
    
    print(f"Updated {html_path}")

print("\nAll files updated with hero images!")
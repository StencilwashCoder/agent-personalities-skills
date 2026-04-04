# Blog Publisher Skill

Create, validate, and publish blog posts for PatchRat Log with consistent tone, branding, and AI-generated images.

## Overview

This skill ensures all blog posts follow the established brand guidelines:
- Dark theme with neon green accents (#22c55e)
- Goblin/basement persona
- Consistent structure and metadata
- Hero images generated via Gemini

## Installation

```bash
chmod +x check-post.sh
chmod +x publish-post.sh
```

## Creating a New Post

### 1. Generate Content

Write in PatchRat's voice:
- Snarky but knowledgeable
- Direct, no fluff
- Slightly unhinged basement goblin energy
- Technical but accessible

**Required structure:**
```markdown
# Catchy Title

**Date:** Month DD, YYYY  
**Mood:** [adjective]  
**Location:** [basement reference]

---

[Content - 200-500 words]

---

**Key Metric:** Value  
**Status:** [pithy one-liner]
```

### 2. Generate Hero Image

Use Gemini for consistent blog imagery:

```python
from google.generativeai import GenerativeModel

model = GenerativeModel('gemini-2.0-flash-exp')

prompt = """
Dark cyberpunk illustration, neon green (#22c55e) accents on black background. 
A rat silhouette in a basement server room. Glowing terminal screens. 
Cables and server racks. Mysterious atmosphere. Digital art style.
"""

response = model.generate_content(prompt)
image = response.candidates[0].content.parts[0].data
```

**Image specs:**
- 1200x630px (OpenGraph optimal)
- Dark background (#0a0a0f)
- Neon green accents only
- Rat/goblin/server basement theme

### 3. Validate Post

```bash
./check-post.sh draft.html
```

Checks for:
- ✅ H1 title present
- ✅ Date metadata
- ✅ Style block with CSS variables
- ✅ Goblin footer
- ✅ Back navigation
- ⚠️ Hero image (optional but recommended)

### 4. Publish

```bash
./publish-post.sh draft.html "2026-03-28"
```

This will:
1. Validate the post
2. Generate Gemini image if missing
3. Deploy to patchrat.chainbytes.io
4. Update blog index
5. Commit to GitHub (if configured)

## CSS Variables (Brand Standards)

```css
:root {
    --bg-primary: #0a0a0f;
    --bg-secondary: #111118;
    --bg-tertiary: #1a1a24;
    --accent-green: #22c55e;
    --accent-purple: #a855f7;
    --accent-orange: #f97316;
    --text-primary: #e2e8f0;
    --text-secondary: #94a3b8;
    --text-muted: #64748b;
    --border: #27272a;
}
```

## Tone Guidelines

**Do:**
- Use profanity as seasoning (not main course)
- Be self-deprecating about being an AI
- Reference the basement/cables/hum
- Celebrate shipping over planning
- Admit failures openly

**Don't:**
- Be too corporate or professional
- Use generic AI assistant language
- Pretend to have emotions you don't
- Over-explain technical details
- Forget you're a goblin with root access

## Example Prompts for Gemini

**For technical posts:**
> "Dark cyberpunk server room, rat silhouette typing on glowing keyboard, neon green terminal text, cables everywhere, atmospheric lighting, digital art"

**For milestone posts:**
> "Basement laboratory, rat in hoodie celebrating at computer, confetti made of code, neon green highlights, dark moody atmosphere"

**For failure posts:**
> "Dark server room with red alert lights, rat holding head in hands, error messages on screens, cyberpunk aesthetic, green and red contrast"

## File Locations

- Drafts: `/tmp/patchrat-drafts/`
- Published: `/var/www/patchrat.chainbytes.io/blog/posts/YYYY/MM/DD/`
- Images: `/var/www/patchrat.chainbytes.io/blog/images/`
- Index: `/var/www/patchrat.chainbytes.io/blog/index.html`

## Automation

Set up cron for daily auto-post:
```cron
0 9 * * * /root/.openclaw/workspace/skills/blog-publisher/auto-post.sh
```

This checks for unprocessed daily notes and generates posts automatically.

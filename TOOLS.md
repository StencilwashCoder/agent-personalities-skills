# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

## Telegram Bots

### AlexAI Monitor Bot
- **Token:** `8600179570:AAGn9cHOVqgj5JYJ9jAcXR-BlSrgwRJbWTw`
- **Purpose:** Daily digest of GitHub repos from AlexAI Facebook page
- **Bot Username:** @patchrat_bot
- **Chat ID:** 84020120 (Eric's personal chat)
- **Status:** ✅ Active and responding

### Usage
```bash
# Get bot info
curl "https://api.telegram.org/bot8600179570:AAGn9cHOVqgj5JYJ9jAcXR-BlSrgwRJbWTw/getMe"

# Send message
curl -X POST "https://api.telegram.org/bot8600179570:AAGn9cHOVqgj5JYJ9jAcXR-BlSrgwRJbWTw/sendMessage" \
  -d "chat_id=CHAT_ID" \
  -d "text=Your message here"
```

---

## API Keys

### Apify
- **API Token:** `$APIFY_TOKEN` (set in environment)
- **Purpose:** Web scraping, browser automation, data extraction
- **Docs:** https://docs.apify.com/api

### Google Gemini
- **API Key:** `$GEMINI_API_KEY` (set in environment)
- **Purpose:** Image generation for blog hero images
- **Docs:** https://ai.google.dev/gemini-api/docs

---

## GitHub Authentication

### Stencilwashcoder Account
- **Token Location:** `/root/.config/gh/token` ✅ **ACTIVE**
- **Usage:** `export GITHUB_TOKEN=$(cat /root/.config/gh/token)`
- **Scope:** repo (full repository access)
- **Account:** stencilwashcoder
- **Status:** Ready to push

### Token Storage (Secure)
```bash
# Token is stored at:
/root/.config/gh/token

# Set permissions:
chmod 600 /root/.config/gh/token

# Use with git:
export GITHUB_TOKEN=$(cat /root/.config/gh/token)
git remote set-url origin https://stencilwashcoder:${GITHUB_TOKEN}@github.com/stencilwashcoder/REPO.git
git push
```

### SSH Deploy Keys (Server)
- **Key:** `/root/.ssh/id_ed25519_deploy`
- **Public:** `/root/.ssh/id_ed25519_deploy.pub`
- **Fingerprint:** `SHA256:...L66 chainbytes-server-deploy`
- **Note:** Currently read-only on most repos - enable write access per-repo as needed

---

Add whatever helps you do your job. This is your cheat sheet.

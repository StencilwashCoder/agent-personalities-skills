# Skill: AlexAI Repo Monitor

## Purpose
Monitor AlexAI's Facebook page (https://www.facebook.com/Alexaiupdate) for GitHub repository links shared in posts and comments.

## How It Works

**Your setup:** You run the Apify Facebook scraper separately
**My job:** Check your completed runs, extract GitHub repos, send daily digest

### Flow
1. Every 6 hours during heartbeat → Check recent Apify runs
2. Get dataset items from completed Facebook scraper runs
3. Extract all `github.com` links from posts and comments
4. Compare against stored list in `memory/alexai-repos.json`
5. If new repos found → Send Telegram digest via @patchrat_bot

## Files

| File | Purpose |
|------|---------|
| `skills/alexai-monitor/SKILL.md` | This documentation |
| `skills/alexai-monitor/check-alexai.sh` | Main monitoring script |
| `memory/alexai-repos.json` | Database of all found repos |
| `memory/alexai-last-check.json` | Last check timestamp |

## Data Format

### alexai-repos.json
```json
{
  "repos": [
    {
      "url": "https://github.com/user/repo",
      "name": "user/repo",
      "date": "2026-03-25",
      "isNew": true
    }
  ],
  "lastUpdated": "2026-03-25T10:00:00Z"
}
```

## Telegram Output

```
📊 AlexAI Daily Repo Digest (2026-03-25)
Found 3 new GitHub repositories:

1. awesome-user/cool-project
   🔗 https://github.com/awesome-user/cool-project

2. another-dev/useful-tool
   🔗 https://github.com/another-dev/useful-tool

3. some-org/great-library
   🔗 https://github.com/some-org/great-library
```

## Configuration

Apify token and Telegram bot are configured in `check-alexai.sh`:
- `APIFY_TOKEN` - Your Apify API token
- `BOT_TOKEN` - Telegram bot token (@patchrat_bot)
- `CHAT_ID` - Eric's chat ID (84020120)

## Notes

- Runs every 6 hours (checks `alexai-last-check.json`)
- Only reports NEW repos (deduplicated against stored list)
- Requires your Apify runs to use `scrapio/facebook-page-scraper` actor
- Looks for repos in both post text and comments

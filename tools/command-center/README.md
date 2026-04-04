# 🎯 Command Center

**Your single source of truth for all reports, decisions, and experiments.**

## Problem Solved

Reports used to get lost in Telegram notifications. Now everything lives in one persistent dashboard that you can check anytime.

## How It Works

1. **Reports are generated** by various tools (content repurposer, board deck, etc.)
2. **Dashboard auto-updates** every hour + after each new report
3. **Telegram notifications** include a link to the dashboard
4. **Everything in one place** - never lost, always accessible

## Dashboard Location

```
/root/.openclaw/workspace/tools/command-center/dashboard.html
```

Open in browser:
```bash
# From terminal
open /root/.openclaw/workspace/tools/command-center/dashboard.html

# Or via file browser
file:///root/.openclaw/workspace/tools/command-center/dashboard.html
```

## Features

| Feature | Description |
|---------|-------------|
| **Stats Bar** | Unread reports, decisions due, active experiments, today's count |
| **Filter by Type** | Content, Decisions, Ideas, Board Deck |
| **Status Tracking** | New (green), Pending (yellow), Read (gray) |
| **Quick Actions** | View full report, Mark as read |
| **Auto-refresh** | Dashboard regenerates hourly |

## Report Types

| Icon | Type | Source |
|------|------|--------|
| 📊 | Content Repurposing | Daily from stencilwash/ericgrill/bjjchat |
| 🧠 | Decision Reviews | When 30/60/90-day reviews are due |
| 💡 | Idea Validation | Active experiments + Go/No-Go status |
| 📈 | Board Deck | Weekly personal dashboard |

## Scheduled Jobs

| Job | Schedule | Action |
|-----|----------|--------|
| Content Repurposing | 12:00 PM daily | Generate content + update dashboard |
| Decision Check | 9:00 AM daily | Check reviews + update dashboard |
| Board Deck | 11:00 PM Sundays | Weekly report + update dashboard |
| Dashboard Refresh | Every hour | Keep dashboard current |

## Manual Commands

```bash
# Regenerate dashboard now
cd /root/.openclaw/workspace/tools/command-center && python3 generate.py

# Update dashboard + send notification
./update-dashboard.sh
```

## Notification Format

Telegram messages now look like:

```
📊 Content Repurposing Complete

Fresh content ready for stencilwash.com, ericgrill.com, bjjchat.com

🎯 View Dashboard:
/root/.openclaw/workspace/tools/command-center/dashboard.html

All your reports in one place. Never lost.
```

## Files

| File | Purpose |
|------|---------|
| `dashboard.html` | Generated dashboard (view this) |
| `template.html` | Dashboard template |
| `generate.py` | Dashboard generator script |
| `update-dashboard.sh` | Cron wrapper with notifications |
| `notify-report.sh` | Helper for individual report notifications |

---

*Dashboard auto-refreshes every hour. Manual refresh: `python3 generate.py`*

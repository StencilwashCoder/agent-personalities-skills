# Weekly Personal Board Deck Generator

Auto-generates a comprehensive weekly dashboard tracking personal goals, development activity, content output, and business metrics.

## 📁 Files

| File | Purpose |
|------|---------|
| `generator.py` | Main generator script - collects data and generates reports |
| `template.md` | Markdown template for report formatting |
| `README.md` | This file - usage and configuration guide |

## 🚀 Quick Start

### Generate Report for Current Week

```bash
cd /workspace/tools/board-deck
python3 generator.py
```

### Generate Report for Last Week

```bash
python3 generator.py --week-offset 1
```

### Generate Multiple Formats

```bash
python3 generator.py --format markdown,html,json
```

### Send via Telegram

```bash
export TELEGRAM_BOT_TOKEN="your_bot_token"
export TELEGRAM_CHAT_ID="your_chat_id"
python3 generator.py --send-telegram
```

## 📊 Metrics Tracked

### 1. Goal Progress (from GOALS.md)
- Reads `/workspace/memory/GOALS.md`
- Tracks completion status for each active goal
- Calculates completion percentage
- Identifies in-progress and not-started goals

### 2. GitHub Activity
- Commits from git log
- PRs created (from GOAL_LOG.md)
- Issues created (from GOAL_LOG.md)
- Active repositories touched

### 3. Content Output
- Articles/blog posts (markdown files)
- Pitch decks created
- Content in `content/` directory
- Any markdown files modified this week

### 4. Business Metrics
⚠️ **Requires manual configuration**

Create a `metrics.json` file in your workspace to enable automatic tracking:

```json
{
  "revenue": {
    "amount": 5000,
    "currency": "USD",
    "notes": "Stripe MRR: $5,000"
  },
  "leads": {
    "count": 12,
    "sources": ["Website", "LinkedIn", "Referral"],
    "notes": "5 qualified, 2 in negotiation"
  },
  "partnerships": {
    "active": 3,
    "new": 1,
    "notes": "New partner: Acme Corp"
  }
}
```

### 5. Blockers and Wins
- Automatically extracts from GOAL_LOG.md
- Scans recent memory files for ✅ (wins) and 🔴 (blockers)
- Uses pattern matching to identify completed items and obstacles

### 6. Next Week's Priorities
- Automatically generated from in-progress goals
- Prioritizes high-value incomplete goals
- Suggests specific actions based on goal status

## 📝 Output Format

Reports are saved to `reports/` directory with timestamps:

```
reports/
├── board-deck_20260327_Mar_21_-_Mar_27_2026.md
├── board-deck_20260327_Mar_21_-_Mar_27_2026.html
├── board-deck_20260327_Mar_21_-_Mar_27_2026.json
└── latest.md  # Symlink to most recent
```

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `WORKSPACE_DIR` | Path to workspace | `/root/.openclaw/workspace` |
| `OUTPUT_DIR` | Where to save reports | `/workspace/tools/board-deck` |
| `TELEGRAM_BOT_TOKEN` | Bot token for Telegram | - |
| `TELEGRAM_CHAT_ID` | Chat ID for Telegram | - |

### Customizing the Template

Edit `template.md` to customize the report format. Available placeholders:

| Placeholder | Description |
|-------------|-------------|
| `{{WEEK_LABEL}}` | Week date range |
| `{{GENERATED_AT}}` | Generation timestamp |
| `{{GOALS_SUMMARY}}` | Goals overview stats |
| `{{GOALS_DETAIL}}` | Detailed goal list |
| `{{GITHUB_SUMMARY}}` | GitHub activity stats |
| `{{CONTENT_SUMMARY}}` | Content output stats |
| `{{BUSINESS_METRICS}}` | Business metrics section |
| `{{WINS}}` | List of wins |
| `{{BLOCKERS}}` | List of blockers |
| `{{NEXT_PRIORITIES}}` | Next week's priorities |

## 🕐 Scheduled Execution

### Cron Setup (Sunday Evening)

Add to crontab for automatic weekly generation:

```bash
# Open crontab editor
crontab -e

# Add this line for Sunday at 11:00 PM
0 23 * * 0 cd /root/.openclaw/workspace/tools/board-deck && /usr/bin/python3 generator.py --format markdown,html

# Or with Telegram notification
0 23 * * 0 cd /root/.openclaw/workspace/tools/board-deck && /usr/bin/python3 generator.py --format markdown,html --send-telegram
```

### Alternative: Monday Morning Delivery

```bash
# Monday at 8:00 AM
0 8 * * 1 cd /root/.openclaw/workspace/tools/board-deck && /usr/bin/python3 generator.py --format markdown,html --send-telegram
```

## 🔧 Integration Ideas

### Connect to Stripe for Revenue

Extend `fetch_business_metrics()` in `generator.py`:

```python
def fetch_stripe_revenue(self):
    import stripe
    stripe.api_key = os.environ.get("STRIPE_API_KEY")
    # Fetch MRR, new customers, etc.
```

### Connect to GitHub API

For more detailed GitHub metrics:

```python
def fetch_github_api(self):
    import requests
    headers = {"Authorization": f"token {os.environ['GITHUB_TOKEN']}"}
    # Fetch detailed PR/issue data
```

### Connect to Notion/Airtable

Store metrics in a database:

```python
def save_to_notion(self, data):
    # Use Notion API to create weekly entry
    pass
```

## 📈 Report Structure

Each generated report includes:

1. **Executive Summary** - At-a-glance goal progress
2. **Goal Detail** - Each active goal with progress %
3. **Development Activity** - GitHub commits, PRs, issues
4. **Content Output** - Articles, videos, other content
5. **Business Metrics** - Revenue, leads, partnerships
6. **Wins** - Completed items and achievements
7. **Blockers** - Obstacles and challenges
8. **Next Priorities** - Top 5 focus areas for next week
9. **Reflection Section** - Space for manual notes

## 🎯 Best Practices

1. **Review Weekly** - Set aside 15 minutes Monday morning to review
2. **Add Context** - Manually fill in reflection sections
3. **Track Trends** - Compare week-over-week in the JSON data
4. **Share Selectively** - HTML reports are great for sharing with stakeholders
5. **Iterate Template** - Customize the template to match your workflow

## 🐛 Troubleshooting

### No goals showing
- Ensure `/workspace/memory/GOALS.md` exists
- Check goal format matches expected pattern

### No GitHub activity
- Verify git is configured in workspace
- Check that GOAL_LOG.md contains PR/issue references

### Business metrics empty
- Create `metrics.json` file manually
- Or extend the generator to pull from your CRM/payment system

### Telegram not sending
- Verify `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` are set
- Check bot has permission to send messages
- Message might be too long (Telegram limit: 4096 chars)

## 📝 Changelog

### v1.0.0 (2026-03-27)
- Initial release
- Markdown and HTML report generation
- Automatic goal parsing from GOALS.md
- GitHub activity tracking
- Telegram integration
- Weekly scheduling support

## 🔮 Future Enhancements

- [ ] PDF generation using WeasyPrint
- [ ] Interactive charts using Chart.js
- [ ] Trend analysis (week-over-week comparisons)
- [ ] Integration with more data sources (Notion, Airtable, etc.)
- [ ] Email delivery option
- [ ] Slack/Discord notifications
- [ ] Custom metric plugins

---

Built with ❤️ for personal productivity tracking.

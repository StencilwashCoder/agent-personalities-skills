# HEARTBEAT.md

## Heartbeat Priority Order

Each heartbeat, work through these in order. Stop after completing ONE task.

### 1. Goal System (Highest Priority)

**Check GOALS.md** - If active goals exist:

**New Approach: Spawn 1 subagent per goal**

1. Read GOALS.md to identify all active goals
2. Spawn subagents in parallel (1 per goal):
   - Subagent #1 → Goal #1 (PRs)
   - Subagent #2 → Goal #2 (Issues)
   - Subagent #3 → Goal #3 (Stencilwashcoder)
   - etc.
3. Each subagent works independently and reports results
4. Log the orchestration action to GOAL_LOG.md
5. Report to user: "Spawned N subagents for parallel goal execution"

**This counts as ONE action** (orchestration), but achieves parallel progress on all goals.

**Goal Format:**
- Status emoji (🔴/🟡/🟢)
- Clear Definition of Done
- Progress log section

**Logging Format:**
```
[YYYY-MM-DD HH:MM] - Goal Orchestration - [Spawned N subagents] - [Goal #1, #2, #3...] - Aligns by: [Parallel execution hits daily targets efficiently]
```

### 2. AI Repo Research Pipeline (Hourly)

**Run the 24/7 research pipeline to process/discover AI repos:**

1. Check `memory/last-research-run.json` - skip if run within 50 minutes
2. Execute `/root/.openclaw/workspace/skills/ai-repo-research/scripts/research-pipeline.sh`
3. Pipeline will:
   - Process up to 5 repos from MinIO queue
   - Auto-discover 5 new trending AI repos if queue empty
   - Generate deep research for each
   - Regenerate static site
   - Upload to s3://research-site/
4. Report results:
   - Repos processed this batch
   - New repos discovered (if any)
   - Total repos on site
   - Site URL: https://s3.chainbytes.io/research-site/index.html

**Output Format:**
```
🤖 AI Repo Research Update (YYYY-MM-DD HH:MM)
Processed: X repos this hour
Discovered: Y new trending repos
Total on site: Z repos
Site: https://s3.chainbytes.io/research-site/index.html

New repos:
1. owner/repo-name (⭐ stars)
   Key: One-line summary from research
```

**Target:** 5 repos/hour = 120 repos/day
**Goal:** Maintain 24/7 continuous research pipeline

**Script Path:** `/root/.openclaw/workspace/skills/ai-repo-research/scripts/research-pipeline.sh`

### 3. SMT Council Daily Review (New - Once per day)

**Check smt-council bucket for high-potential HN projects:**

1. Check if already reviewed today (`memory/smt-council-last-run.txt`)
2. Read evaluations from MinIO: `s3://smt-council/hn-<post_id>/`
3. Parse council votes (amy-hoy, dhh, elon-musk, jason-fried, marc-andreessen, murray-rothbard, naval-ravikant, peter-thiel, steve-jobs)
4. Report threshold: **1+ YES votes** OR **avg score ≥ 6/10**
5. If threshold met:
   - Report top opportunities to Eric
   - Include: Title, URL, who voted YES, key reasoning
   - Suggest: "Build this?" with brief analysis
6. Log the review to `memory/council-reviews.md`

**Report Format:**
```
🎯 SMT Council Daily Review (YYYY-MM-DD)

TOP PICK:
- Project: [title]
- URL: [url]
- Council Score: X/10 (N evaluations)
- Votes: X YES | X NO | X MAYBE
- Why: [one-line from council assessment]
- Verdict: [Build / Watch / Skip]

AI FOCUS PICKS:
1. [title] - [one-line summary]
2. [title] - [one-line summary]
```

**What to look for:**
- AI/agent tools (Eric's interest)
- Developer productivity tools
- Open source projects with validation
- Clear pain point + working solution

**MinIO Access:**
```python
s3 = boto3.client('s3',
    endpoint_url='https://s3.chainbytes.io',
    aws_access_key_id='chainbytes',
    aws_secret_access_key='chainbytes2026',
    region_name='us-east-1'
)
# List: s3.list_objects_v2(Bucket='smt-council')
# Read: s3.get_object(Bucket='smt-council', Key='hn-<id>/post.json')
# Evals: s3.get_object(Bucket='smt-council', Key='hn-<id>/<member>.md')
```

**Script Path:** `/root/.openclaw/workspace/skills/ai-repo-research/scripts/check-council.py`

### 4. Repo Hygiene Check (If No Active Goals)

**Check EricGrill repos for:**
- Missing LICENSE files
- Empty or incomplete READMEs
- Missing .env.example files
- Security issues (exposed keys, etc.)

**Filter:** Only original repos (no forks)

**Action:**
- Identify ONE repo needing attention
- Make the fix (add LICENSE, write README, etc.)
- Commit and push
- Log the improvement

### 4. Baseline (If Nothing Above)

Reply: HEARTBEAT_OK

---

## Logging Requirements

**Every heartbeat action MUST be logged.** Use the `write` tool to append to `memory/heartbeat-log.md`:

```python
# Example logging - use write tool with append
write(file_path='memory/heartbeat-log.md', content='''
---

[2026-03-27 HH:MM] - [Priority #N: Action] - [Goal] - [Result]

Details:
- What was done
- Goal contribution
- Status
''', append=True)
```

**Or use the helper script:**
```bash
python3 /root/.openclaw/workspace/skills/heartbeat-handler/log_heartbeat.py "Action" "Goal" "Result"
```

## Reporting

**Log all actions to memory files** (GOAL_LOG.md, council-reviews.md, etc.)

---

## Rules

- ONE action per heartbeat (no multitasking)
- **Exception: Goal orchestration via subagents counts as 1 action**
- Every action must have explicit alignment statement if tied to a goal
- Everything gets logged to `memory/heartbeat-log.md`
- Report what was done, even for repo hygiene
- Results are reported through this channel (kimi-claw), NOT Telegram

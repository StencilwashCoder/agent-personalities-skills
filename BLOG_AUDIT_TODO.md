# BLOG AUDIT TODO - Priority 1

## CRITICAL ISSUES FOUND

### 1. MISSING IMAGES (13 of 15 posts affected)
Only 2 posts have images:
- ✅ qa-blitz-expansion.html
- ✅ 2026-03-27-1904.html

Missing images:
- ❌ hello-world.html
- ❌ the-bot-that-makes-phone-calls.html
- ❌ bjjchat-analytics.html
- ❌ iron-grips-migration.html
- ❌ blinkcfo-sprint-3.html
- ❌ blinkcfo-sprint-4.html
- ❌ eight-blog-posts.html
- ❌ agent-dao.html
- ❌ mission-control-center.html
- ❌ chainwarden.html
- ❌ the-skills-keep-coming.html
- ❌ i-have-a-website.html
- ❌ langchain-framework.html

### 2. MISSING DAILY POSTS (24+ days missing)
Current posts only cover 15 days. Missing:
- Feb 18, 19, 21-24, 26, 27
- Mar 1, 2, 4-7, 9-11, 13, 14, 16, 17, 19-21, 23, 25, 26
- Mar 29-31, Apr 1-3 (today is Apr 3)

### 3. WORD COUNT AUDIT
All existing posts are 1000+ words ✅

## TODO LIST

### PHASE 1: Add Images to Existing Posts (13 posts)
- [ ] Generate hero images for each post
- [ ] Insert image HTML into each post
- [ ] Verify images load correctly

### PHASE 2: Create Missing Daily Posts (24+ posts)
- [ ] Create content for each missing date
- [ ] Generate hero images for each
- [ ] Ensure 1000+ words per post
- [ ] Backdate posts to correct dates

### PHASE 3: Set Up Daily Publishing System
- [ ] Create blog post template
- [ ] Set up cron for daily generation
- [ ] Create image generation workflow

## EXECUTION PLAN
1. Spawn subagents for image generation (parallel)
2. Spawn subagents for content creation (parallel)
3. Verify all posts have images and 1000+ words
4. Update blog index
5. Deploy to server
6. Sign off with Eric

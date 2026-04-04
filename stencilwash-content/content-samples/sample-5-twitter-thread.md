# The Hidden Complexity of Git Rebasing

*A technical deep-dive into what actually happens when you rebase*

🧵 Thread (1/15)

---

1/ You've used `git rebase` hundreds of times. 

But do you actually understand what it's doing?

Most developers don't. They treat it as magic.

Let's pull back the curtain on what might be Git's most misunderstood command.

---

2/ First, the common understanding:

"Rebase moves my commits on top of another branch"

This is wrong. Rebase doesn't "move" anything.

It *recreates* your commits. Every single one.

Here's why this matters 👇

---

3/ When you run:
```bash
git checkout feature
git rebase main
```

Git doesn't add your commits to main. It:

- Detaches HEAD to main's tip
- Cherry-picks each of your commits, one by one
- Creates NEW commits with the same changes

Your original commits? Abandoned. Garbage collected eventually.

---

4/ Let's see this in action.

Before rebase:
```
main:    A---B---C
              \
feature:       D---E---F
```

After `git rebase main`:
```
main:    A---B---C
                   \
feature:            D'---E'---F'
```

D', E', F' are NEW commits. Different hashes. Same diffs.

---

5/ "Same diffs" but not quite.

Each recreated commit has:
- Different parent → different hash
- Potentially different content (conflict resolution)
- Same author/date... initially

But `git commit --amend` or rebase's interactive mode changes timestamps.

---

6/ The reflog saves you.

Scared of losing work during rebase? Don't be.

```bash
git reflog
# Find pre-rebase state
git reset --hard HEAD@{5}
```

Rebase is non-destructive... until garbage collection runs (usually 30+ days).

---

7/ Why recreate commits instead of moving them?

Git's immutable design. Commits are identified by hash of their entire content, including parent.

Change the parent → change the hash → it's a different commit.

This isn't a limitation. It's the feature that makes Git distributed and reliable.

---

8/ Interactive rebase is where it gets interesting.

```bash
git rebase -i HEAD~5
```

You're not just replaying commits. You're rewriting history:

- Reorder commits (change pick order)
- Squash commits (fixup/squash)
- Edit commits (stop and amend)
- Delete commits (drop)
- Split commits (edit + reset)

---

9/ The pick order matters more than you think.

If commit B depends on changes from commit A, reordering them creates conflicts.

Git applies commits sequentially. Each must apply cleanly to the result of previous.

This is why "clean history" advocates group related changes in logical order.

---

10/ Merge commits during rebase? Complicated.

Default rebase (`git rebase main`) *linearizes* history. Merge commits become regular commits.

Preserve merges:
```bash
git rebase main --rebase-merges
```

This recreates the merge structure but still creates new commit objects.

---

11/ The three-way merge algorithm during rebase:

For each commit being rebased:
1. Find merge-base between original parent and new parent
2. Compute diff between merge-base and your commit
3. Apply that diff to new parent
4. If conflicts, pause for resolution

Understanding this explains why conflicts happen where they do.

---

12/ Conflict resolution is commit-by-commit.

Unlike `git merge` where you resolve all conflicts at once, rebase stops at each conflicting commit.

```bash
# Fix conflicts
git add .
git rebase --continue

# Or skip this commit
git rebase --skip

# Or abort entirely
git rebase --abort
```

---

13/ The "golden rule" of rebasing:

**Never rebase commits that exist outside your local repository.**

Why? Because you've rewritten history. Your D' conflicts with their D.

Force push after rebase = pain for teammates.

```bash
# DON'T do this after rebase
git push --force origin feature

# Do this instead (safer)
git push --force-with-lease origin feature
```

---

14/ `force-with-lease` vs `force`:

- `--force`: My commits replace remote. Period.
- `--force-with-lease`: Only if remote hasn't changed since I fetched

The lease check prevents overwriting teammates' work. Use it. Always.

---

15/ When to rebase vs merge:

**Rebase for:**
- Cleaning up feature branch before PR
- Linear history preference
- Incorporating upstream changes to avoid merge commits

**Merge for:**
- Long-running branches with shared history
- Preserving complete context
- Teams that prefer merge bubbles

No universal right answer. Know the tradeoffs.

---

🎯 TL;DR:

- Rebase recreates commits, doesn't move them
- New commits = new hashes
- Interactive rebase is history rewriting
- Never force push rebased shared branches
- Use `--force-with-lease` when you must

---

📚 Want to go deeper?

- Pro Git book (free): git-scm.com/book
- "Git Internals" by Scott Chacon
- `git help rebase` (actually comprehensive)

---

🔥 Hot take: Developers who understand Git's object model write better commit messages and design cleaner branching strategies.

Spend 2 hours learning Git internals. Save 200 hours over your career.

---

Like this thread?

- Retweet the first tweet to share
- Follow for more deep dives
- Reply with topics you'd like covered

Next week: How Git's packfile compression achieves 10:1 space savings

---

*Written by Stencilwash Content Agency. We create technical content that teaches, engages, and converts.*

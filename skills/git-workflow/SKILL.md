---
name: claude-code-git-workflow
description: Git workflow optimization for Claude Code. Use when working with git operations including commit message generation, branch management, PR preparation, and conflict resolution. Provides smart defaults and practical workflows specifically designed for AI-assisted coding sessions.
---

# Claude Code Git Workflow

Optimized git workflows for Claude Code users. Focuses on practical, AI-friendly patterns that reduce friction in the development cycle.

## Installation

1. Add this skill to your Claude Code skills directory:
   ```bash
   # Clone or copy the skill to your skills folder
   cp -r skills/claude-code/git-workflow ~/.claude/skills/
   ```

2. Or use directly by referencing the skill path in your Claude Code configuration.

## Usage

### Commit Message Generation

Generate conventional commit messages from your changes:

```bash
# Stage your changes first
git add -p  # Review changes interactively

# Generate commit message based on staged changes
/claude commit  # Claude analyzes diff and suggests message

# Or manually with Claude's help
/claude "Write a conventional commit message for these changes: $(git diff --staged)"
```

**Commit Message Format:**
```
type(scope): subject

body (optional)

footer (optional)
```

**Types:**
- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation only
- `style` - Code style (formatting, missing semi colons, etc)
- `refactor` - Code refactoring
- `perf` - Performance improvements
- `test` - Adding/updating tests
- `chore` - Build process or auxiliary tool changes

### Branch Management

**Feature Branch Workflow:**
```bash
# Start new feature
/claude "Create a feature branch for: [description]"
# Claude suggests: git checkout -b feat/description-here

# Or manually
git checkout -b feat/user-authentication

# Keep branch up to date
git fetch origin
git rebase origin/main
```

**Branch Naming Conventions:**
```
feat/short-description      # New features
fix/bug-description         # Bug fixes
hotfix/critical-issue       # Production fixes
docs/what-changed           # Documentation
refactor/what-changed       # Refactoring
test/what-being-tested      # Test additions
chore/what-changed          # Maintenance
```

**Clean Up Old Branches:**
```bash
# Delete merged branches
/claude "Clean up merged branches"
# Claude runs: git branch --merged | grep -v "\\*" | xargs -n 1 git branch -d

# Or manually
git branch --merged | grep -v "\\*" | grep -v main | xargs git branch -d
```

### PR Preparation

**Before Creating PR:**
```bash
# 1. Review all changes
/claude "Review my changes before PR"

# 2. Check for common issues
/claude "Check for console.logs, TODOs, or debugging code"

# 3. Run tests
npm test  # or your test command

# 4. Update documentation if needed
/claude "Update README for these changes"
```

**Generate PR Description:**
```bash
# Get PR description from Claude
/claude "Write a PR description for these changes: $(git diff main...HEAD)"
```

**PR Template:**
```markdown
## Summary
Brief description of changes

## Changes
- Change 1
- Change 2

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows project style
- [ ] Documentation updated
- [ ] No console.logs or debug code
```

### Conflict Resolution

**When Conflicts Occur:**
```bash
# 1. See which files have conflicts
git status

# 2. Ask Claude to help resolve
/claude "Help resolve conflicts in src/components/UserProfile.tsx"

# 3. Or resolve manually - look for:
<<<<<<< HEAD
your changes
=======
their changes
>>>>>>> branch-name
```

**Resolution Workflow:**
1. Identify the conflict markers
2. Decide which changes to keep (or merge both)
3. Remove conflict markers
4. Stage resolved file: `git add <file>`
5. Continue rebase/merge: `git rebase --continue` or `git merge --continue`

**Prevent Conflicts:**
```bash
# Pull before pushing
git pull --rebase origin main

# Work on small, focused branches
# Rebase frequently during long-running work
git fetch origin && git rebase origin/main
```

### AI-Friendly Patterns

**Commit Often:**
```bash
# Small, atomic commits are easier for AI to understand
/claude "Commit these changes with a good message"
# Claude suggests logical groupings
```

**Describe Intent, Not Just Changes:**
```bash
# Bad: "Update UserProfile.tsx"
# Good: "feat(profile): add avatar upload validation"

/claude "Write a commit message that explains WHY not just WHAT"
```

**Use `git add -p` for Review:**
```bash
# Review changes before committing
git add -p
# y - stage this hunk
# n - don't stage
# s - split into smaller hunks
# e - edit manually
```

## Tips

### Best Practices

1. **Commit Messages:**
   - Use imperative mood ("Add feature" not "Added feature")
   - Keep subject line under 50 characters
   - Use body for explaining WHY, not HOW

2. **Branch Hygiene:**
   - Delete feature branches after merge
   - Keep `main` always deployable
   - Use descriptive branch names

3. **Before Committing:**
   - Review your own diff first (`git diff`)
   - Run tests
   - Check for sensitive data (API keys, passwords)

4. **Working with Claude:**
   - Ask Claude to review changes before commit
   - Use Claude to generate meaningful commit messages
   - Let Claude help resolve complex merge conflicts

### Common Commands

```bash
# Quick status
git status

# See what changed
git diff

# See staged changes
git diff --staged

# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo changes in file
git checkout -- <file>

# Stash work temporarily
git stash
git stash pop

# View commit history
git log --oneline --graph
```

### Troubleshooting

**Forgot to commit?**
```bash
/claude "I made changes but forgot to commit, help me organize these"
```

**Messy commit history?**
```bash
# Interactive rebase to clean up
/claude "Help me clean up this commit history before PR"
```

**Accidentally committed to main?**
```bash
# Move commits to new branch
/claude "I committed to main by mistake, help me fix this"
```
---
name: git-workflow-optimization
description: Optimize Git workflows for cleaner history, efficient collaboration, and safer deployments. Use when creating branches, committing changes, handling merge conflicts, reviewing code, or managing releases. Provides battle-tested patterns for feature branching, commit hygiene, pull requests, and release management optimized for OpenAI Codex.
---

# Git Workflow Optimization (Codex)

Clean, efficient Git workflows for solo developers and teams using Codex. Focuses on practical patterns that make code history readable, collaboration smooth, and deployments safer.

## Quick Reference

### Daily Commands
```bash
# Start new feature
git checkout -b feature/user-authentication
git commit -m "feat: add user login form"

# Sync with main
git fetch origin
git rebase origin/main

# Share your work
git push -u origin feature/user-authentication

# Clean up after merge
git checkout main
git pull
git branch -d feature/user-authentication
```

### Emergency Fixes
```bash
# Undo last commit (keep changes)
git reset --soft HEAD~1

# Undo last commit (discard changes)
git reset --hard HEAD~1

# Fix commit message
git commit --amend -m "new message"

# Stash changes temporarily
git stash push -m "WIP: auth refactor"
git stash pop  # restore later
```

## Branching Strategies

### Feature Branch Workflow

```bash
# 1. Create feature branch from updated main
git checkout main
git pull origin main
git checkout -b feature/payment-gateway

# 2. Make commits with clear messages
git add .
git commit -m "feat: integrate Stripe payment processing"
git commit -m "feat: add payment confirmation email"

# 3. Keep branch updated
git fetch origin
git rebase origin/main  # or: git merge origin/main

# 4. Push and create PR
git push -u origin feature/payment-gateway
```

### Commit Message Convention (Conventional Commits)

```
type(scope): subject

body (optional)

footer (optional)
```

**Types:**
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Formatting, semicolons, etc.
- `refactor:` Code change that neither fixes a bug nor adds a feature
- `perf:` Performance improvement
- `test:` Adding or correcting tests
- `chore:` Build process, dependencies, etc.

**Examples:**
```bash
# Good commits
git commit -m "feat(auth): add OAuth2 login with Google"
git commit -m "fix(api): handle null response from payment gateway"
git commit -m "docs(readme): update installation instructions"
git commit -m "refactor(utils): extract validation logic to separate module"
git commit -m "test(auth): add tests for token refresh flow"

# Bad commits (avoid these)
git commit -m "fix stuff"
git commit -m "WIP"
git commit -m "update"
git commit -m "changes"
```

### Branch Naming Conventions

```bash
# Feature branches
feature/user-authentication
feature/payment-gateway
feat/oauth-integration

# Bug fix branches
fix/login-redirect-loop
bugfix/api-timeout-issue
fix/memory-leak-in-parser

# Release branches
release/v2.1.0
release/2024-03-15

# Hotfix branches (for production emergencies)
hotfix/critical-security-patch
hotfix/fix-payment-processing

# Personal/developer branches
user/john/feature-name
john/refactor-auth

# Experiment/spike branches
spike/graphql-migration
experiment/new-ui-framework
```

## Commit Hygiene

### Atomic Commits

Each commit should:
- Do one logical thing
- Leave the codebase in a working state
- Have a clear, descriptive message

```bash
# Bad: Multiple unrelated changes in one commit
git add .
git commit -m "updates"

# Good: Separate logical changes
git add src/auth/login.js
git commit -m "feat(auth): implement JWT token validation"

git add src/auth/tests/login.test.js
git commit -m "test(auth): add JWT validation tests"

git add docs/auth.md
git commit -m "docs(auth): document JWT implementation"
```

### Interactive Rebase for Clean History

```bash
# Rebase last 5 commits
git rebase -i HEAD~5

# Common operations in interactive rebase:
# pick    = use commit as-is
# reword  = use commit but edit message
# squash  = combine with previous commit
# fixup   = like squash but discard message
# drop    = remove commit

# Example: Clean up before PR
git rebase -i origin/main
# Change:
#   pick abc123 feat: add login
#   pick def456 fix: typo
#   pick ghi789 fix: another typo
# To:
#   pick abc123 feat: add login
#   fixup def456 fix: typo
#   fixup ghi789 fix: another typo
```

### Stash Workflow

```bash
# Save current work
git stash push -m "half-done with payment refactor"

# List stashes
git stash list
# stash@{0}: On feature/payment: half-done with payment refactor
# stash@{1}: On main: WIP: auth changes

# Apply stash without removing
git stash apply stash@{0}

# Apply and remove stash
git stash pop stash@{0}

# Drop specific stash
git stash drop stash@{1}

# Clear all stashes
git stash clear
```

## Merge Conflict Resolution

### Prevention

```bash
# Keep feature branch updated (prevents conflicts)
git fetch origin
git rebase origin/main

# Before starting work, ensure main is current
git checkout main
git pull origin main
git checkout -b feature/new-thing
```

### Resolution Workflow

```bash
# During rebase, conflict occurs
git rebase origin/main
# Auto-merging src/app.js
# CONFLICT (content): Merge conflict in src/app.js

# 1. See conflicting files
git status

# 2. Open file and resolve markers
# <<<<<<< HEAD
# console.log('main branch version');
# =======
# console.log('feature branch version');
# >>>>>>> feature/my-feature

# 3. Mark as resolved
git add src/app.js

# 4. Continue rebase
git rebase --continue

# Or abort if needed
git rebase --abort
```

### Conflict Resolution Tools

```bash
# Use VS Code as merge tool
git config --global merge.tool vscode
git config --global mergetool.vscode.cmd "code --wait $MERGED"

# Launch merge tool
git mergetool

# See conflict details
git diff  # Shows all conflicts
git diff --name-only --diff-filter=U  # Lists conflicted files only
```

## Code Review Workflow

### Preparing for Review

```bash
# 1. Ensure branch is current
git fetch origin
git rebase origin/main

# 2. Squash fixup commits
git rebase -i origin/main
# Change 'pick' to 'squash' or 'fixup' for cleanup commits

# 3. Run tests
npm test
pytest
make test

# 4. Push (force if rebased)
git push -f origin feature/branch-name
```

### Reviewing Code

```bash
# Fetch PR branch
git fetch origin pull/123/head:pr-123
git checkout pr-123

# Review changes
git diff origin/main...HEAD

# Test the changes
npm test
npm run build

# Leave feedback and return
git checkout main
git branch -D pr-123
```

### Addressing Review Comments

```bash
# Make requested changes
git checkout feature/branch-name
# ... edit files ...

git add .
git commit -m "refactor(auth): address PR feedback - simplify validation"

# Or amend if it's a small fix
git add .
git commit --amend --no-edit

# Push updates
git push origin feature/branch-name
```

## Release Management

### Semantic Versioning

```
Version format: MAJOR.MINOR.PATCH

MAJOR - Breaking changes
MINOR - New features (backwards compatible)
PATCH - Bug fixes (backwards compatible)

Examples:
2.1.0 -> 2.2.0  (new feature)
2.1.0 -> 2.1.1  (bug fix)
2.1.0 -> 3.0.0  (breaking change)
```

### Release Workflow

```bash
# 1. Create release branch
git checkout -b release/v2.1.0

# 2. Update version numbers
npm version minor  # or: patch, major
# Updates package.json and creates commit + tag

# 3. Final testing
npm test
npm run build

# 4. Merge to main
git checkout main
git merge --no-ff release/v2.1.0 -m "Release v2.1.0"
git tag -a v2.1.0 -m "Release version 2.1.0"

# 5. Push everything
git push origin main --tags

# 6. Merge back to develop (if using git-flow)
git checkout develop
git merge main
```

### Hotfix Workflow (Production Emergency)

```bash
# 1. Create hotfix from main
git checkout main
git pull origin main
git checkout -b hotfix/critical-fix

# 2. Fix the issue with minimal changes
git add .
git commit -m "fix: patch critical security vulnerability"

# 3. Test thoroughly
npm test

# 4. Merge to main and tag
git checkout main
git merge --no-ff hotfix/critical-fix
git tag -a v2.1.1 -m "Hotfix v2.1.1"
git push origin main --tags

# 5. Also merge to develop
git checkout develop
git merge main
```

## Advanced Workflows

### Git Hooks for Quality

```bash
# Install husky for JS projects
npx husky-init && npm install

# Pre-commit hook (scripts/pre-commit)
#!/bin/sh
. "$(dirname "$0")/_/husky.sh"

npm run lint
npm test -- --watchAll=false

# Commit-msg hook for conventional commits
#!/bin/sh
. "$(dirname "$0")/_/husky.sh"

npx --no -- commitlint --edit ${1}
```

### Signing Commits (GPG)

```bash
# Configure GPG signing
git config --global user.signingkey YOUR_GPG_KEY_ID
git config --global commit.gpgsign true

# Sign specific commit
git commit -S -m "feat: add secure feature"

# Verify signatures
git log --show-signature
```

### Bisect for Finding Bugs

```bash
# Start bisect session
git bisect start

# Mark current commit as bad
git bisect bad

# Mark known good commit
git bisect good v2.0.0

# Git checks out middle commit - test it
npm test

# Mark result
git bisect good  # or: git bisect bad

# Repeat until found...
# Bisecting: 3 revisions left to test after this

# End session
git bisect reset
```

### Worktrees for Parallel Work

```bash
# Create worktree for hotfix without stashing
git worktree add ../project-hotfix main
cd ../project-hotfix
# Work on hotfix independently

# When done
cd ../project
git worktree remove ../project-hotfix
```

## Troubleshooting

### Recovering Lost Work

```bash
# See recent operations (useful after bad rebase)
git reflog
# abc1234 HEAD@{0}: commit: feat: add login
# def5678 HEAD@{1}: checkout: moving from main to feature

# Recover deleted branch
git reflog | grep branch-name
git checkout -b recovered-branch abc1234

# Recover file from another branch
git checkout other-branch -- path/to/file.js
```

### Fixing Common Mistakes

```bash
# Committed to wrong branch
git reset HEAD~1 --soft  # Undo commit, keep changes
git checkout correct-branch
git add .
git commit -m "proper commit message"

# Forgot to add file to last commit
git add forgotten-file.js
git commit --amend --no-edit

# Wrong commit message
git commit --amend -m "correct message"

# Pushed sensitive data (immediately!)
git rm --cached secret.txt
echo "secret.txt" >> .gitignore
git add .gitignore
git commit --amend --no-edit
git push --force-with-lease  # Careful with force push!
```

### Large File Issues

```bash
# Find large files in history
git rev-list --objects --all | \
  git cat-file --batch-check='%(objecttype) %(objectname) %(objectsize) %(rest)' | \
  awk '/^blob/ {print $3, $4}' | sort -rn | head -20

# Use git-lfs for large files
git lfs track "*.psd"
git lfs track "*.zip"
git add .gitattributes
```

## Team Collaboration

### Fork Workflow (Open Source)

```bash
# 1. Fork on GitHub, then clone your fork
git clone https://github.com/YOUR_USERNAME/project.git
cd project
git remote add upstream https://github.com/ORIGINAL/project.git

# 2. Sync with upstream
git fetch upstream
git checkout main
git rebase upstream/main

# 3. Create feature branch and work
git checkout -b feature/my-contribution
# ... make changes ...
git push origin feature/my-contribution

# 4. Create PR from your fork to upstream
# Use GitHub UI or gh CLI
```

### Submodules

```bash
# Add submodule
git submodule add https://github.com/user/repo.git libs/repo

# Clone with submodules
git clone --recurse-submodules https://github.com/user/project.git

# Update submodules
git submodule update --init --recursive
git submodule update --remote

# Remove submodule
git submodule deinit libs/repo
git rm libs/repo
rm -rf .git/modules/libs/repo
```

## Tips for Clean Git History

1. **Commit early, commit often** - But squash fixups before PR
2. **Never force push to shared branches** - Only feature branches
3. **Keep commits atomic** - One logical change per commit
4. **Write meaningful messages** - Future you will thank present you
5. **Pull before you push** - Avoid unnecessary merge commits
6. **Use branches for everything** - Don't commit directly to main
7. **Delete merged branches** - Keep the repo clean
8. **Tag releases** - Makes rollback easy
9. **Review before merging** - Even if it's your own PR
10. **Keep main deployable** - Never break the main branch

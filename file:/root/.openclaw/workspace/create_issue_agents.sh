: "Create issue: agents-skills-plugins needs CONTRIBUTING.md" && cat << 'EOF' | gh issue create --repo EricGrill/agents-skills-plugins --title "Add CONTRIBUTING.md - Missing contributor guidelines" --body-file -
## Problem
This repository has 9 stars and 1 open issue but lacks contribution guidelines. This creates friction for potential contributors:

1. **Unclear submission process** - Contributors don't know how to submit new plugins
2. **No quality standards** - No criteria for what makes an acceptable plugin
3. **No development setup docs** - Contributors must reverse-engineer the sync workflows
4. **Missing code of conduct** - No guidelines for community interaction

## Recommended Solution

Create `CONTRIBUTING.md` with the following sections:

### Plugin Submission Process
1. Fork the repository
2. Add plugin to appropriate `*/plugins.json` file
3. Ensure plugin has: `name`, `description`, `repo`, `author`, `tags`
4. Submit PR with description of what the plugin does

### Quality Criteria
- Plugin must have a clear README
- Must be actively maintained (activity within last 6 months)
- Should have clear use case
- Must not duplicate existing functionality

### Sync Workflow Explanation
Explain that plugins are auto-synced from upstream sources via GitHub Actions and manual edits to generated files will be overwritten.

### Example Template
```markdown
## Submitting a New Plugin

1. Check [existing plugins](PLUGINS.md) first - no duplicates
2. Edit the appropriate category file in `*/plugins.json`
3. Add entry with required fields
4. Open PR with description

## Development

This repo uses GitHub Actions to sync plugins from upstream sources.
Do not edit auto-generated files directly - they will be overwritten.
```

## Impact
- **Risk**: Medium (community growth friction)
- **Effort**: 20 minutes
- **Benefit**: Lowers barrier to contribution, grows plugin ecosystem

## References
- [GitHub Docs - Setting guidelines for repository contributors](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/setting-guidelines-for-repository-contributors)
EOF
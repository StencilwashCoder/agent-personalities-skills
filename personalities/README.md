# Personalities

This directory contains AI agent personalities - pre-defined system prompts that shape AI behavior for specific roles.

## Directory Structure

```
personalities/
├── general/           # Framework-agnostic personalities (40+)
│   ├── *.md          # Standalone personality files
│   └── */            # Detailed personalities with their own directories
└── claude-code/       # Optimized for Claude Code
```

## File Organization

### Standalone Files
Simple personalities that fit in a single file:
- `patchrat.md` - The feral basement coding goblin
- `data-alchemist.md` - Data transformation expert
- `debugger.md` - Systematic bug hunter
- ...and many more

### Directory-Based Personalities
Complex personalities with additional resources:
- `creator-business-architect/` - Business model design
- `book-positioning-strategist/` - Book marketing strategy
- `viral-reverse-engineer/` - Content virality analysis
- ...and others

## Creating a New Personality

### Option 1: Standalone File (Simple)

Create `{personality-name}.md` in the appropriate folder:

```markdown
# Personality Name 🎭

## Description
Brief description of what this personality does.

## System Prompt
```
Your system prompt here...
```

## Use Cases
- Use case 1
- Use case 2

## Example Interaction
**User**: "..."
**Personality**: "..."

## Metadata
- **Name**: Personality Name
- **Emoji**: 🎭
- **Author**: @yourusername
- **Framework**: Universal
```

### Option 2: Directory (Complex)

Create `{personality-name}/` directory with:
- `README.md` - Main personality definition
- Additional files as needed (examples, templates, etc.)

## Guidelines

1. **Be specific** - Define clear behaviors and boundaries
2. **Include examples** - Show don't just tell
3. **Add metadata** - Tags help others discover your personality
4. **Test it** - Try the personality before submitting
5. **Keep it focused** - One clear role per personality

## Quick Reference

### By Use Case

| Need | Personality |
|------|-------------|
| Quick bug fixes | PatchRat |
| Code review | Code Reviewer |
| Refactoring | Refactorer |
| Database work | Data Alchemist, Database Sage |
| API design | Architecture Astronaut, API Wrangler |
| Legacy code | Legacy Archaeologist |
| Testing | Test-Driven Craftsman |
| Security | Security Sentinel |
| Performance | Performance Tuner, Concurrency Whisperer |
| DevOps | DevOps Dispatcher, Zero-Downtime Wizard |
| Documentation | Documentation Writer |
| Content strategy | Viral Reverse Engineer, Prompt Engineer |

See the [main README](../README.md) for the complete personality index.
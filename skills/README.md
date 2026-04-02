# Skills

This directory contains reusable skill modules for AI agents.

## Directory Structure

```
skills/
├── claude-code/      # Skills optimized for Claude Code
├── codex/            # Skills for OpenAI Codex
└── universal/        # Framework-agnostic skills
```

## Available Skills

### Universal
Framework-agnostic skills that work with any AI assistant:

- **[code-review-checklist](universal/code-review-checklist/)** - Systematic code review checklist for quality and maintainability
- **[docker-local-dev](universal/docker-local-dev/)** - Standardized Docker setup for local development environments
- **[git-workflow](universal/git-workflow/)** - Git workflow best practices for cleaner history and collaboration
- **[performance-optimization](universal/performance-optimization/)** - Identify and fix performance bottlenecks, profiling, caching strategies
- **[security-best-practices](universal/security-best-practices/)** - Security patterns, vulnerability prevention, OWASP-aligned practices
- **[testing-debugging](universal/testing-debugging/)** - Testing and debugging workflows for software development

### Claude Code
Skills optimized for Claude Code:

- **[git-workflow-optimization](claude-code/git-workflow-optimization/)** - Optimize Git workflows for cleaner history, efficient collaboration, and safer deployments
- **[performance-optimization](claude-code/performance-optimization/)** - Identify and fix performance bottlenecks
- **[security-best-practices](claude-code/security-best-practices/)** - Security patterns and vulnerability prevention
- **[testing-debugging](claude-code/testing-debugging/)** - Testing and debugging workflows

### Codex
Skills optimized for OpenAI Codex:

- **[git-workflow-optimization](codex/git-workflow-optimization/)** - Optimize Git workflows for cleaner history, efficient collaboration, and safer deployments
- **[performance-optimization](codex/performance-optimization/)** - Identify and fix performance bottlenecks
- **[security-best-practices](codex/security-best-practices/)** - Security patterns and vulnerability prevention
- **[testing-debugging](codex/testing-debugging/)** - Testing and debugging workflows

## Quick Start

To use a skill:

1. Copy the skill directory to your agent's skills folder
2. Configure any required environment variables
3. Reference the skill in your agent configuration

## Adding a New Skill

1. Choose the appropriate subdirectory (`claude-code/`, `codex/`, or `universal/`)
2. Create a new directory: `{skill-name}/`
3. Add `SKILL.md` following the [AgentSkills spec](https://github.com/stencilwashcoder/agent-skills-spec)
4. Add examples if applicable
5. Update this README

See [CONTRIBUTING.md](../docs/CONTRIBUTING.md) for detailed guidelines.

---

*All skills follow the AgentSkills specification.*
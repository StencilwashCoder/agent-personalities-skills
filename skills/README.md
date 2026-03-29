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

### Claude Code
- **git-workflow-optimization** - Optimize Git workflows for cleaner history, efficient collaboration, and safer deployments
- **testing-debugging** - Testing and debugging workflows for software development

### Codex  
- **git-workflow-optimization** - Optimize Git workflows for cleaner history, efficient collaboration, and safer deployments
- **testing-debugging** - Testing and debugging workflows for software development

### Universal
- **git-workflow-optimization** - Optimize Git workflows for cleaner history, efficient collaboration, and safer deployments
- **testing-debugging** - Testing and debugging workflows for software development

## Adding a New Skill

1. Choose the appropriate subdirectory (`claude-code/`, `codex/`, or `universal/`)
2. Create a new directory: `{skill-name}/`
3. Add `SKILL.md` following the [AgentSkills spec](https://github.com/stencilwashcoder/agent-skills-spec)
4. Add examples if applicable
5. Update this README

See [CONTRIBUTING.md](../docs/CONTRIBUTING.md) for detailed guidelines.

## Quick Start

To use a skill:

1. Copy the skill directory to your agent's skills folder
2. Configure any required environment variables
3. Reference the skill in your agent configuration

---

*All skills follow the AgentSkills specification.*

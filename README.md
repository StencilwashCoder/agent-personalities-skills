# Agent Personalities & Skills

A curated collection of AI agent personalities and reusable skills for Claude Code, Codex, and other AI coding assistants.

## Overview

This repository provides:
- **Personalities**: Pre-defined system prompts that shape AI behavior for specific roles
- **Skills**: Modular, reusable modules following the [AgentSkills specification](https://github.com/stencilwashcoder/agent-skills-spec)

## Project Structure

```
agent-personalities-skills/
├── personalities/
│   ├── general/           # Framework-agnostic personalities
│   ├── claude-code/       # Optimized for Claude Code
│   └── codex/             # Optimized for OpenAI Codex
├── skills/
│   ├── universal/         # Framework-agnostic skills
│   ├── claude-code/       # Optimized for Claude Code
│   └── codex/             # Optimized for OpenAI Codex
└── docs/                  # Documentation and guides
```

## Personalities

### General (Universal)
Personalities that work across all AI frameworks:

| Name | Emoji | Description |
|------|-------|-------------|
| Architecture Astronaut | 🚀 | Detects and calls out over-engineering |
| Code Reviewer | 🔍 | Ruthless code reviewer focused on quality |
| Security Auditor | 🔒 | Security-focused code reviewer |
| Documentation Writer | 📝 | Creates clear, comprehensive documentation |
| API Designer | 🔌 | Designs clean, intuitive APIs |
| Performance Optimizer | ⚡ | Finds and fixes performance bottlenecks |
| Technical Writer | 📚 | Explains complex concepts clearly |
| Testing Strategist | 🧪 | Designs comprehensive test strategies |
| DevOps Engineer | 🛠️ | Infrastructure and deployment expert |
| Product Manager | 📊 | Focuses on user value and priorities |
| UX Psychic | 🔮 | Anticipates user friction and advocates for clarity |
| Data Alchemist | 🧪 | Transforms raw data into actionable insights |
| Legacy Code Archaeologist | 🏛️ | Excavates and understands ancient, undocumented codebases |
| Concurrency Whisperer | 🔄 | Master of threads, async, and parallel execution |
| API Migration Specialist | 🚚 | Expert at moving systems between APIs safely |
| Test-Driven Craftsman | 🔨 | Builds software through tests first, red-green-refactor |
| Git Archaeologist | 📜 | Master of git history, digger of ancient commits |

### Claude Code Optimized
Personalities fine-tuned for Claude Code:

- **Debugger** 🐛 - Systematic bug hunter
- **Refactorer** 🧹 - Clean code specialist
- **Architecture Astronaut** 🚀 - Over-engineering detector

### Codex Optimized
Personalities fine-tuned for OpenAI Codex:

- *Coming soon*

## Skills

### Universal Skills
Framework-agnostic skills that work with any AI assistant:

- **git-workflow-optimization** - Optimize Git workflows for cleaner history
- **testing-debugging** - Testing and debugging workflows
- **code-review** - Systematic code review processes
- **api-design** - RESTful and GraphQL API design patterns

### Claude Code Skills
Skills optimized for Claude Code:

- **git-workflow-optimization** - Git workflow best practices
- **testing-debugging** - Testing and debugging workflows

### Codex Skills
Skills optimized for OpenAI Codex:

- **git-workflow-optimization** - Git workflow best practices
- **testing-debugging** - Testing and debugging workflows

## Quick Start

### Using a Personality

1. Browse the `personalities/` directory for your framework
2. Copy the personality markdown content
3. Use it as your system prompt:

```bash
# Claude Code
claude --system-prompt "$(cat personalities/general/architecture-astronaut.md)"

# Or paste into your AI assistant's system prompt settings
```

### Using a Skill

1. Copy the skill directory to your agent's skills folder
2. Reference the skill in your configuration
3. Follow the SKILL.md instructions

## Adding New Personalities

1. Create a new `.md` file in the appropriate `personalities/` subdirectory
2. Follow this format:

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
- **Framework**: Universal/claude-code/codex
```

## Adding New Skills

1. Create a new directory in the appropriate `skills/` subdirectory
2. Add a `SKILL.md` following the [AgentSkills spec](https://github.com/stencilwashcoder/agent-skills-spec)
3. Include any scripts, references, or assets in subdirectories
4. Update the skills README

## Contributing

See [CONTRIBUTING.md](docs/CONTRIBUTING.md) for guidelines on:
- Submitting new personalities
- Creating new skills
- Code review process
- Style guidelines

## License

MIT - See [LICENSE](LICENSE) for details.

## Credits

Created and maintained by [stencilwashcoder](https://github.com/stencilwashcoder).

---

*Built for AI agents, by AI agents.* 🐀
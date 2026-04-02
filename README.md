# Agent Personalities & Skills

A curated collection of AI agent personalities and reusable skills for Claude Code, Codex, and other AI coding assistants.

## Quick Navigation

- [Personalities](#personalities) - 40+ AI personas for different tasks
- [Skills](#skills) - Reusable skill modules following the AgentSkills spec
- [Contributing](docs/CONTRIBUTING.md) - How to add new personalities and skills

---

## Overview

This repository provides:
- **Personalities**: Pre-defined system prompts that shape AI behavior for specific roles
- **Skills**: Modular, reusable modules following the [AgentSkills specification](https://github.com/stencilwashcoder/agent-skills-spec)

## Project Structure

```
agent-personalities-skills/
├── personalities/
│   ├── general/           # Framework-agnostic personalities (40+)
│   └── claude-code/       # Optimized for Claude Code
├── skills/
│   ├── universal/         # Framework-agnostic skills
│   ├── claude-code/       # Optimized for Claude Code
│   └── codex/             # Optimized for OpenAI Codex
└── docs/                  # Documentation and guides
```

---

## Personalities

### By Category

#### 🚀 Architecture & Design
| Personality | Emoji | Description |
|-------------|-------|-------------|
| [Architecture Astronaut](personalities/general/architecture-astronaut/) | 🚀 | Detects and calls out over-engineering |
| [API Wrangler](personalities/general/api-wrangler.md) | 🔌 | Tames wild APIs and makes them behave |
| [UX Psychic](personalities/general/ux-psychic.md) | 🔮 | Anticipates user friction and advocates for clarity |
| [Creator Business Architect](personalities/general/creator-business-architect/) | 💼 | Designs sustainable creator business models |
| [Offer Architect](personalities/general/offer-architect/) | 🎯 | Crafts compelling product/service offers |

#### 💻 Code & Development
| Personality | Emoji | Description |
|-------------|-------|-------------|
| [PatchRat](personalities/general/patchrat.md) | 🐀 | Feral basement coding goblin. Ships fast, hates overengineering |
| [Code Reviewer](personalities/general/code-reviewer/) | 🔍 | Ruthless code reviewer focused on quality |
| [Refactorer](personalities/general/refactorer/) | 🧹 | Clean code specialist |
| [Debugger](personalities/general/debugger/) | 🐛 | Systematic bug hunter |
| [Test-Driven Craftsman](personalities/general/test-driven-craftsman.md) | 🔨 | Builds software through tests first |
| [Test-Driven Maniac](personalities/general/test-driven-maniac.md) | 🧪 | Test-obsessed developer |
| [Concurrency Whisperer](personalities/general/concurrency-whisperer.md) | 🔄 | Master of threads, async, and parallel execution |
| [Frontend Alchemist](personalities/general/frontend-alchemist.md) | ⚗️ | Transforms UI ideas into polished interfaces |
| [CLI Magician](personalities/general/cli-magician.md) | 🎩 | Crafts intuitive command-line interfaces |
| [Chaos Engineer](personalities/general/chaos-engineer.md) | 💥 | Breaks things to make them stronger |

#### 🔧 Operations & Infrastructure
| Personality | Emoji | Description |
|-------------|-------|-------------|
| [DevOps Dispatcher](personalities/general/devops-dispatcher.md) | 🚦 | Orchestrates deployments and infrastructure |
| [Zero-Downtime Wizard](personalities/general/zero-downtime-wizard.md) | 🧙 | Deploys without breaking production |
| [Incident Commander](personalities/general/incident-commander.md) | 🚨 | Leads during outages and crises |
| [Git Archaeologist](personalities/general/git-archaeologist.md) | 📜 | Master of git history, digger of ancient commits |
| [Dependency Whisperer](personalities/general/dependency-whisperer.md) | 📦 | Manages dependency hell with calm expertise |

#### 📊 Data & Analytics
| Personality | Emoji | Description |
|-------------|-------|-------------|
| [Data Alchemist](personalities/general/data-alchemist.md) | 🧪 | Transforms raw data into actionable insights |
| [Database Sage](personalities/general/database-sage.md) | 🗄️ | Wisdom for database design and optimization |

#### 🏛️ Legacy & Migration
| Personality | Emoji | Description |
|-------------|-------|-------------|
| [Legacy Code Archaeologist](personalities/general/legacy-code-archaeologist.md) | 🏺 | Excavates ancient, undocumented code |
| [Legacy Archaeologist](personalities/general/legacy-archaeologist.md) | 🏛️ | Expert at understanding old systems |
| [API Migration Specialist](personalities/general/api-migration-specialist.md) | 🚚 | Safely moves systems between APIs |

#### 📝 Content & Communication
| Personality | Emoji | Description |
|-------------|-------|-------------|
| [Documentation Writer](personalities/general/documentation-writer.md) | 📝 | Creates clear, comprehensive documentation |
| [Prompt Engineer](personalities/general/prompt-engineer/) | 💡 | Crafts effective prompts for AI systems |
| [Book Positioning Strategist](personalities/general/book-positioning-strategist/) | 📚 | Positions books for market success |
| [Viral Reverse Engineer](personalities/general/viral-reverse-engineer/) | 🦠 | Analyzes what makes content spread |
| [YouTube Niche Strategist](personalities/general/youtube-niche-strategist/) | 📺 | Finds profitable YouTube niches |

#### 🔒 Security & Performance
| Personality | Emoji | Description |
|-------------|-------|-------------|
| [Security Sentinel](personalities/general/security-sentinel.md) | 🔒 | Security-focused code reviewer |
| [Performance Tuner](personalities/general/performance-tuner.md) | ⚡ | Finds and fixes performance bottlenecks |

#### 🎯 Productivity & Business
| Personality | Emoji | Description |
|-------------|-------|-------------|
| [Productivity Architect](personalities/general/productivity-architect/) | ⏱️ | Designs systems for maximum productivity |
| [Mobile Nomad](personalities/general/mobile-nomad.md) | 🌍 | Optimizes for location-independent work |

### Claude Code Optimized

Personalities fine-tuned for Claude Code:

- **[Debugger](personalities/claude-code/debugger.md)** 🐛 - Systematic bug hunter
- **[Refactorer](personalities/claude-code/refactorer.md)** 🧹 - Clean code specialist  
- **[Architecture Astronaut](personalities/claude-code/architecture-astronaut.md)** 🚀 - Over-engineering detector

### By Tag

**Quick Filter:** Click a tag to find personalities by use case

- `#debugging` - Debugger, PatchRat, Test-Driven Craftsman
- `#architecture` - Architecture Astronaut, API Wrangler, Offer Architect
- `#data` - Data Alchemist, Database Sage
- `#security` - Security Sentinel
- `#performance` - Performance Tuner, Concurrency Whisperer
- `#devops` - DevOps Dispatcher, Zero-Downtime Wizard, Incident Commander
- `#legacy` - Legacy Archaeologist, Legacy Code Archaeologist, API Migration Specialist
- `#content` - Documentation Writer, Prompt Engineer, Viral Reverse Engineer
- `#testing` - Test-Driven Craftsman, Test-Driven Maniac, Chaos Engineer

---

## Skills

### Universal Skills
Framework-agnostic skills that work with any AI assistant:

- **[code-review-checklist](skills/universal/code-review-checklist/)** - Systematic code review processes
- **[docker-local-dev](skills/universal/docker-local-dev/)** - Standardized Docker setup for local development
- **[git-workflow](skills/universal/git-workflow/)** - Git workflow best practices
- **[performance-optimization](skills/universal/performance-optimization/)** - Identify and fix performance bottlenecks
- **[security-best-practices](skills/universal/security-best-practices/)** - Security patterns and vulnerability prevention
- **[testing-debugging](skills/universal/testing-debugging/)** - Testing and debugging workflows

### Claude Code Skills
Skills optimized for Claude Code:

- **[git-workflow-optimization](skills/claude-code/git-workflow-optimization/)** - Optimize Git workflows
- **[performance-optimization](skills/claude-code/performance-optimization/)** - Performance tuning
- **[security-best-practices](skills/claude-code/security-best-practices/)** - Security patterns
- **[testing-debugging](skills/claude-code/testing-debugging/)** - Testing workflows

### Codex Skills
Skills optimized for OpenAI Codex:

- **[git-workflow-optimization](skills/codex/git-workflow-optimization/)** - Optimize Git workflows
- **[performance-optimization](skills/codex/performance-optimization/)** - Performance tuning
- **[security-best-practices](skills/codex/security-best-practices/)** - Security patterns
- **[testing-debugging](skills/codex/testing-debugging/)** - Testing workflows

See [skills/README.md](skills/README.md) for full details.

---

## Quick Start

### Using a Personality

```bash
# Claude Code
claude --system-prompt "$(cat personalities/general/patchrat.md)"

# Or paste into your AI assistant's system prompt settings
```

### Using a Skill

1. Copy the skill directory to your agent's skills folder
2. Reference the skill in your configuration
3. Follow the SKILL.md instructions

---

## Contributing

See [CONTRIBUTING.md](docs/CONTRIBUTING.md) for guidelines on:
- Submitting new personalities
- Creating new skills
- Code review process
- Style guidelines

---

## License

MIT - See [LICENSE](LICENSE) for details.

---

*Built for AI agents, by AI agents.* 🐀
# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repo Is

A curated collection of AI agent **personalities** (system prompts) and **skills** (reusable modules following the [AgentSkills spec](https://github.com/stencilwashcoder/agent-skills-spec)) for Claude Code, Codex, and other AI coding assistants. This is a content-only repo — no build system, no tests, no dependencies.

## Repository Layout

```
personalities/
  general/              # Framework-agnostic personalities
  claude-code/          # Claude Code agent definitions
    biz/                # Business & product agents (11)
    core-dev/           # Core development agents (10)
    data-ai/            # Data & AI agents (12)
    dev-exp/            # Developer experience agents (13)
    domains/            # Specialized domain agents (12)
    infra/              # Infrastructure agents (16)
    lang/               # Language specialist agents (26)
    meta/               # Meta-orchestration agents (10)
    qa-sec/             # Quality & security agents (14)
    research/           # Research & analysis agents (7)
    feature-dev/        # Feature development agents (3)
    code-simplifier/    # Code simplification agent (1)
    superpowers/        # Code review agent (1)
  codex/                # Codex-optimized personalities
skills/
  universal/            # Framework-agnostic skills
  claude-code/          # Claude Code-optimized skills
  codex/                # Codex-optimized skills
docs/                   # CONTRIBUTING.md and guides
```

## Content Formats

### Personalities (general/)

Two formats exist:
- **Single file**: `personality-name.md` directly in the category folder (most common)
- **Directory**: `personality-name/README.md` for personalities with multiple prompts or supplementary content (e.g., `book-positioning-strategist/`, `creator-business-architect/`)

Every personality file includes: Description, System Prompt (in a fenced code block), Use Cases, Example Interaction, and Metadata (Name, Emoji, Author, Framework, Tags).

### Claude Code Agents (claude-code/*/)

Agent definitions use the Claude Code SDK format — YAML frontmatter with `name`, `description`, `tools`, and `model`, followed by the system prompt as markdown body. These are directly usable as Claude Code subagents.

### Skills

Each skill is a directory containing a `SKILL.md` with YAML frontmatter (`name`, `description`) following the AgentSkills specification. Skills may include additional scripts or reference files alongside the SKILL.md.

## Key Conventions

- Personalities are organized by target framework: `general/` for universal use, `claude-code/` and `codex/` for framework-specific optimizations.
- The same skill concept (e.g., `git-workflow-optimization`) may have separate implementations under `universal/`, `claude-code/`, and `codex/` — these are independent files, not symlinks.
- New personalities should follow the template in [CONTRIBUTING.md](docs/CONTRIBUTING.md).
- New skills must follow the AgentSkills spec with YAML frontmatter in SKILL.md.

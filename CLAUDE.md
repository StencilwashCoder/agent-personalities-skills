# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Repo Is

A Claude Code plugin providing 136 specialized agent definitions, 4 reusable skills, and a collection of framework-agnostic AI personalities. Installable via the Claude Code plugin system.

## Plugin Structure

```
.claude-plugin/
  plugin.json             # Plugin metadata (required for installation)
agents/                   # Claude Code agent definitions (136 agents)
  biz/                    # Business & product (11)
  core-dev/               # Core development (10)
  data-ai/                # Data & AI (12)
  dev-exp/                # Developer experience (13)
  domains/                # Specialized domains (12)
  infra/                  # Infrastructure (16)
  lang/                   # Language specialists (26)
  meta/                   # Meta-orchestration (10)
  qa-sec/                 # Quality & security (14)
  research/               # Research & analysis (7)
  feature-dev/            # Feature development (3)
  code-simplifier/        # Code simplification (1)
  superpowers/            # Code review (1)
skills/                   # Reusable skills
  git-workflow-optimization/
  testing-debugging/
  code-review-checklist/
  docker-local-dev/
personalities/            # Framework-agnostic personality prompts
  general/                # Universal personalities
  claude-code/            # Claude Code-specific (legacy format)
  codex/                  # Codex-specific
docs/                     # Contributing guidelines
```

## Content Formats

### Agents (`agents/`)

YAML frontmatter with `name`, `description`, `tools`, and `model`, followed by the system prompt as markdown body. Directly loadable as Claude Code subagents.

### Skills (`skills/`)

Each skill is a directory containing a `SKILL.md` with YAML frontmatter (`name`, `description`).

### Personalities (`personalities/general/`)

Human-readable format: Description, System Prompt (fenced code block), Use Cases, Example Interaction, and Metadata. Two sub-formats: single `.md` file or directory with `README.md`.

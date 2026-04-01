# Contributing to Agent Personalities & Skills

Thank you for your interest in contributing! This document provides guidelines for submitting new personalities and skills to this repository.

## Getting Started

1. Fork the repository
2. Create a new branch for your contribution
3. Follow the guidelines below
4. Submit a pull request

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
└── docs/                  # Documentation
```

## Adding a Personality

### 1. Choose the Right Location

- `personalities/general/` - Works with any AI framework
- `personalities/claude-code/` - Optimized for Claude Code
- `personalities/codex/` - Optimized for OpenAI Codex

### 2. Create Your Personality File

Create a new `{personality-name}.md` file following this template:

```markdown
# Personality Name 🎭

## Description
Brief description of what this personality does and when to use it.

## System Prompt
```
Your complete system prompt here...
Be specific about tone, rules, and behavior.
```

## Use Cases
- Use case 1
- Use case 2
- Use case 3

## Example Interaction

**User**: "Example user query"

**Personality**: "Example response showing the personality in action"

## Metadata
- **Name**: Personality Name
- **Emoji**: 🎭
- **Author**: @yourusername
- **Framework**: Universal/claude-code/codex
- **Version**: 1.0.0
- **Tags**: tag1, tag2, tag3
```

### 3. Personality Guidelines

- **Be specific**: Define clear behaviors and boundaries
- **Include examples**: Show don't just tell
- **Add metadata**: Tags help others discover your personality
- **Test it**: Try the personality before submitting
- **Keep it focused**: One clear role per personality

## Adding a Skill

### 1. Choose the Right Location

- `skills/universal/` - Works with any AI framework
- `skills/claude-code/` - Optimized for Claude Code
- `skills/codex/` - Optimized for OpenAI Codex

### 2. Create Your Skill Directory

Create a new directory: `{skill-name}/`

### 3. Add SKILL.md

Follow the [AgentSkills specification](https://github.com/stencilwashcoder/agent-skills-spec):

```markdown
---
name: skill-name
description: Brief description of what this skill does
---

# Skill Name

## Overview
What this skill does and when to use it.

## Quick Start
### Installation
```bash
# Installation commands
```

### Basic Usage
```bash
# Example commands
```

## Commands

### Command 1
Description of command 1

```bash
# Example
```

### Command 2
Description of command 2

```bash
# Example
```

## Configuration

### Environment Variables
| Variable | Description | Required |
|----------|-------------|----------|
| `API_KEY` | API key for service | Yes |
| `DEBUG` | Enable debug mode | No |

### Configuration File
```yaml
# config.yaml
key: value
```

## Examples

### Example 1: Basic Usage
```bash
# Example commands
```

### Example 2: Advanced Usage
```bash
# Example commands
```

## Troubleshooting

### Issue 1
Solution for issue 1

### Issue 2
Solution for issue 2

## References
- [Link 1](url)
- [Link 2](url)
```

### 4. Skill Guidelines

- **Follow the spec**: Use the AgentSkills format
- **Be practical**: Focus on real-world usage
- **Include examples**: Show common use cases
- **Document edge cases**: Help users avoid pitfalls
- **Add troubleshooting**: Common issues and solutions
- **Keep it focused**: One skill = one purpose

## Style Guidelines

### Writing Style

- **Clear and concise**: Get to the point
- **Action-oriented**: Use imperative verbs
- **Specific examples**: Show real commands, not placeholders
- **Consistent formatting**: Follow existing patterns

### Markdown Formatting

- Use ATX-style headers (`# Header`)
- Use fenced code blocks with language tags
- Use tables for structured data
- Use lists for sequential steps

### Code Examples

- Include comments for clarity
- Show expected output when helpful
- Use realistic examples, not foo/bar
- Test all commands before submitting

## Review Process

1. **Automated checks**: Linting and validation
2. **Manual review**: Maintainers review for quality
3. **Feedback**: Address any requested changes
4. **Merge**: Approved contributions are merged

## Code of Conduct

- Be respectful and constructive
- Focus on improving the project
- Accept feedback gracefully
- Help others learn and grow

## Questions?

- Open an issue for discussion
- Check existing personalities/skills for examples
- Read the [AgentSkills spec](https://github.com/stencilwashcoder/agent-skills-spec)

## Recognition

Contributors will be recognized in our README and release notes.

Thank you for helping make AI agents more capable! 🐀

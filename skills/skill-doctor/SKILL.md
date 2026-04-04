---
name: skill-doctor
description: Self-diagnosis and health check tool for OpenClaw skills. Validates skill structure, YAML frontmatter, script syntax, and reference integrity. Use when (1) Skills are behaving unexpectedly, (2) Before packaging a skill for distribution, (3) After making changes to multiple skills, (4) When "you keep breaking" and need to identify what's wrong, (5) Periodic health checks on the skill ecosystem.
---

# Skill Doctor 🔧

Validates all installed OpenClaw skills for structural and syntax errors.

## What It Checks

- **YAML Frontmatter**: Validates required fields (`name`, `description`), checks for extra fields
- **Script Syntax**: Python and Bash syntax validation
- **Reference Integrity**: Ensures referenced files in `references/` actually exist
- **Extraneous Files**: Flags documentation files that shouldn't be in skills (README.md, CHANGELOG.md, etc.)
- **Directory Structure**: Validates skill follows the standard layout

## Usage

Run the diagnosis script:

```bash
python3 ~/.openclaw/workspace/skills/skill-doctor/scripts/diagnose.py
```

Or from any skill-doctor location:

```bash
./scripts/diagnose.py
```

## Output

The tool produces a report showing:
- Total skills checked
- Healthy skills count
- Errors and warnings with details
- Exit code 0 if all healthy, 1 if issues found

## Report Format

```
🔧 SKILL DOCTOR DIAGNOSIS REPORT
==================================================
Skills checked: 15
Healthy: 12
Issues found: 3

❌ ERRORS:

  broken-skill
    - [frontmatter] Missing 'name' field
    - [script] Syntax error: invalid syntax (line 42)

⚠️  WARNINGS:

  messy-skill
    - [frontmatter] Extra fields in frontmatter: {'version'}

✅ HEALTHY (12 skills):
  ✓ skill-doctor
  ✓ weather
  ...
```

## Skill Locations Checked

The doctor searches these directories for skills:

1. `/usr/lib/node_modules/openclaw/skills` (system skills)
2. `~/.openclaw/skills` (user skills)
3. `~/.openclaw/workspace/skills` (workspace skills)

## Fixing Issues

### Frontmatter Errors
- Ensure YAML is between `---` markers
- Only `name` and `description` fields allowed
- No extra blank lines in frontmatter

### Script Syntax Errors
- Run `python3 -m py_compile script.py` for details
- For bash: `bash -n script.sh`

### Missing References
- Create the referenced file in `references/`
- Or remove the broken link from SKILL.md

### Extraneous Files
- Delete README.md, CHANGELOG.md, etc. from skill directories
- Skills should only contain SKILL.md and functional resources
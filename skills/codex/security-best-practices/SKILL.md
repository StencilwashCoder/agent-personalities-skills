---
name: codex-security-best-practices
description: Security review and hardening workflows for OpenAI Codex. Use when reviewing code for vulnerabilities, implementing authentication, or handling sensitive data. Provides OWASP-aligned security patterns optimized for AI-assisted security audits.
---

# Security Best Practices (Codex)

Security workflows designed for Codex users. Review code for vulnerabilities, implement secure patterns, and don't get pwned.

## Quick Security Audits

### Code Review with Codex

```bash
# Security review a file
codex "Security review this code: $(cat src/auth/login.js)"

# Check for common vulnerabilities
codex "Check for SQL injection in: $(cat src/api/users.js)"

# Review authentication implementation
codex "Review this JWT implementation for security: $(cat src/middleware/auth.js)"
```

### Vulnerability Scanning

```bash
# OWASP Top 10 check
codex "Check this code against OWASP Top 10: $(cat src/routes/*.js)"

# Input validation review
codex "Are all user inputs properly validated here? $(cat src/controllers/*.js)"
```

## Codex-Specific Patterns

### Security Context Sharing

```bash
# Full security audit context
codex "Security audit:

Code to review:
$(cat src/api/payment.js)

Threat model:
- Public API
- Handles credit card data
- PCI DSS requirements

Focus areas:
- Input validation
- SQL injection
- XSS prevention
- Authentication bypass"
```

### Remediation Workflow

```bash
# Step 1: Find
codex "Find security issues in $(cat src/auth.js)"

# Step 2: Fix
codex "Fix the SQL injection vulnerability you found"

# Step 3: Verify
codex "Verify the fix is correct and complete"
```

## Security Checklist

Before shipping, ask Codex:

```bash
codex "Check this PR for:
1. Hardcoded secrets
2. SQL injection risks
3. XSS vulnerabilities
4. Missing auth checks
5. Insecure dependencies

$(git diff HEAD~1)"
```

## See Also

- [Universal Security Guide](../universal/security-best-practices/SKILL.md)

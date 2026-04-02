---
name: codex-performance-optimization
description: Performance optimization workflows for OpenAI Codex. Use when diagnosing slow code, optimizing bottlenecks, or improving application speed. Provides profiling techniques, caching strategies, and algorithm improvements specifically for AI-assisted optimization sessions.
---

# Performance Optimization (Codex)

Performance optimization workflows designed for Codex users. Find bottlenecks fast and fix them faster.

## Quick Commands

### Profile with Codex

```bash
# Share performance issue with Codex
codex "This endpoint is slow, help me profile it: $(cat src/api/slow-endpoint.js)"

# Analyze a function
codex "Optimize this function for performance: $(cat src/utils/heavy-computation.js)"

# Database query optimization
codex "These queries are slow, add indexes: $(cat src/models/queries.sql)"
```

### Common Bottlenecks

**N+1 Query Detection:**
```bash
# Codex will spot these patterns
codex "Check for N+1 queries in: $(cat src/services/user-service.js)"
```

**Memory Leak Analysis:**
```bash
# Share heap snapshot analysis
codex "Help me analyze this memory profile: $(cat heap-profile.txt)"
```

## Codex-Specific Patterns

### Request Context Sharing

```bash
# Full context for complex optimization
codex "Optimize this:

Current code:
$(cat src/bottleneck.js)

Flame graph hotspots:
$(cat profile.txt | head -50)

Requirements:
- Must handle 10k req/s
- Memory limit 512MB
- P95 latency < 100ms"
```

### Iterative Optimization

```bash
# Step 1: Identify
codex "Find the performance bottleneck in $(cat src/api.js)"

# Step 2: Fix
codex "Apply the optimization you suggested"

# Step 3: Verify
codex "The query is still slow, profile this: $(cat query.log)"
```

## See Also

- [Universal Performance Guide](../universal/performance-optimization/SKILL.md)

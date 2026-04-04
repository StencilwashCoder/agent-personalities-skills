## Action 3: SEO Backlink - Dev.to Article

### Article Title
`Building 12 MCP Servers: A Deep Dive into AI Infrastructure`

### Publication Platform
**dev.to** (high-authority developer community, dofollow links)

### Article Content
```markdown
---
title: "Building 12 MCP Servers: A Deep Dive into AI Infrastructure"
published: true
description: "Lessons learned from building 12+ Model Context Protocol servers for infrastructure, security, Bitcoin, and AI orchestration"
tags: ai, claude, mcp, infrastructure, security, bitcoin
---

# Building 12 MCP Servers: A Deep Dive into AI Infrastructure

I've spent the last year building infrastructure that lets AI agents actually *do* things. Not chat. Not summarize. Execute.

The Model Context Protocol (MCP) has become the standard for extending Claude Code, Cursor, and other AI clients with real capabilities. Here's what I learned building 12 production MCP servers.

## What MCP Actually Enables

MCP servers are the bridge between AI agents and the real world. They expose tools that Claude can invoke directly:

- Spin up a Kali Linux instance and run nmap
- Query prediction markets across 5 platforms
- Manage Proxmox VMs through natural language
- Execute Bitcoin transactions via OP_RETURN

The AI doesn't just know about these things. It can *do* them.

## The Servers I Built

### Infrastructure: mcp-proxmox-admin

The most complex infrastructure server I've built. 16 tools for VM management:

```javascript
// Claude: "Start the web server VM and create a snapshot"
await tools.start_vm({ vmid: 100 });
await tools.create_snapshot({ 
  vmid: 100, 
  snapname: "pre-deploy-2026-03-27" 
});
```

Hybrid SSH/REST transport with optional read-only mode. Production-tested on clusters with 50+ VMs.

### Security: mcp-kali-orchestration

This one was fun. 50+ professional security tools exposed through natural language:

- **Recon**: nmap, amass, theHarvester
- **Web**: sqlmap, nuclei, gobuster, wpscan
- **Exploitation**: Metasploit, msfvenom, searchsploit
- **Passwords**: hydra, john, hashcat
- **Post-exploitation**: impacket, crackmapexec, BloodHound

```bash
# Claude: "Scan example.com for SQL injection"
Claude uses kali_start → sqlmap_scan → kali_destroy
```

Fresh container per engagement. No persistent attack surface.

### Finance: mcp-predictive-market

Aggregates Polymarket, Manifold, Metaculus, PredictIt, and Kalshi:

```python
# Claude: "Find arbitrage opportunities on AI regulation"
arbitrage = await tools.find_arbitrage({
    keyword: "AI regulation",
    min_spread: 0.1
})
```

Side-by-side odds comparison. Real edge detection.

### Bitcoin: mcp-bitcoin-cli

Native Bitcoin operations without intermediaries:

- OP_RETURN messaging (immutable on-chain text)
- BRC-20 token operations
- Block analysis and transaction inspection
- Timestamping

```javascript
// Claude: "Timestamp this contract hash to Bitcoin"
await tools.op_return_broadcast({
    message: "sha256:abc123...def456",
    fee_rate: 10
});
```

## Architecture Decisions

### 1. Always Use Isolation

The server-delegation pattern spins up fresh Proxmox VMs per task. Untrusted code never touches the host. Automatic cleanup guarantees no residue.

### 2. Rate Limit Everything

Each adapter has per-platform rate limiting. The predictive market server distributes 60 requests/minute across 5 platforms intelligently.

### 3. Unified Error Handling

All servers implement the same error taxonomy:
- `MCPError` - Base exception
- `ToolError` - Tool execution failure
- `AdapterError` - External API failure
- `RateLimitError` - Throttling

### 4. Environment Over Configuration

No config files. Everything via environment variables:

```bash
PROXMOX_HOST=192.168.1.100
PROXMOX_TOKEN_ID=root@pam!mcp
KALI_BACKEND=docker
POLYMARKET_API_KEY=...
```

## What I Got Wrong

**Early mistake**: Building servers that tried to do too much. The first version of mcp-proxmox-admin had 40+ tools. Unmaintainable.

**Solution**: Split into focused servers. Proxmox-admin for infrastructure. Server-delegation for untrusted code. SSH for persistent connections.

**Another mistake**: Not versioning tool schemas. Broke clients on updates.

**Solution**: Semantic versioning for tool definitions. Migration paths for breaking changes.

## The Plugin Marketplace

All 12 servers are part of the Claude Code Plugin Marketplace:

```bash
/plugin install mcp-proxmox-admin@agents-skills-plugins
/plugin install mcp-kali-orchestration@agents-skills-plugins
/plugin install mcp-predictive-market@agents-skills-plugins
```

49 plugins total. 100+ MCP tools. Community maintained.

## Resources

- **My work**: https://ericgrill.com - Articles on AI, Bitcoin, and infrastructure
- **GitHub**: https://github.com/EricGrill - All 12 MCP servers
- **Marketplace**: https://github.com/EricGrill/agents-skills-plugins

## What's Next

Building an autonomous security testing agent. Goal: Full pentest report from a single prompt. Infrastructure enumeration, vulnerability scanning, exploitation, documentation. All through natural language.

The future isn't AI assistants that chat. It's AI agents that execute.

---

*Eric Grill builds infrastructure at Chainbytes LLC. Navy veteran. IBJJF champion. Writing about systems that survive when everything else breaks.*
```

### SEO Metadata
- **URL slug:** `building-12-mcp-servers-ai-infrastructure-deep-dive`
- **Tags:** `ai`, `claude`, `mcp`, `model-context-protocol`, `infrastructure`, `security`, `bitcoin`, `devops`
- **Canonical:** Links to ericgrill.com (primary domain for SEO authority)

### Backlinks Included
1. ✅ **Primary:** https://ericgrill.com (in resources section)
2. **Secondary:** https://github.com/EricGrill
3. **Secondary:** https://github.com/EricGrill/agents-skills-plugins

### Status: ✅ READY TO PUBLISH
**Action:** Create dev.to account → Publish article → Share on social

### Estimated SEO Impact
- **Domain Authority:** dev.to (DA 85+)
- **Backlink Type:** Dofollow from high-authority domain
- **Target Anchor:** "My work" linking to ericgrill.com
- **Expected Index Time:** 24-48 hours

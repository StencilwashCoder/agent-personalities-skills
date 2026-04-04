---
title: "I Built 9 MCP Servers So Claude Can Control Everything"
published: true
description: "How I gave Claude Code the ability to control Bitcoin nodes, government APIs, QuickBooks, Kali Linux, and more through the Model Context Protocol."
tags: ai, mcp, claude, automation, bitcoin
cover_image: https://ericgrill.com/images/mcp-servers-banner.png
series: Claude Code Plugins
---

# I Built 9 MCP Servers So Claude Can Control Everything

*Giving AI agents real-world superpowers through the Model Context Protocol*

---

## The Problem: AI Assistants That Can't Touch the Real World

I got tired of asking Claude Code to help me with something, only to hit a wall when it needed to:
- Check a Bitcoin transaction
- Query real-time weather data
- Access my QuickBooks records
- Run a security scan with Kali Linux tools
- Manage my Proxmox VMs

The Model Context Protocol (MCP) changed everything.

---

## What I Built

Over the past few months, I've created **9 production-ready MCP servers** that extend Claude Code's capabilities:

### 💰 Bitcoin & Finance
**[mcp-bitcoin-cli](https://github.com/EricGrill/mcp-bitcoin-cli)** - Full Bitcoin node control through Claude. OP_RETURN operations, BRC-20 tokens, document timestamping on-chain.

**[mcp-predictive-market](https://github.com/EricGrill/mcp-predictive-market)** - Query 5 prediction markets (Manifold, Polymarket, Metaculus, Kalshi, PredictIt) with arbitrage detection.

**[quickbooks-online-mcp-server](https://github.com/EricGrill/quickbooks-online-mcp-server)** - 143+ tools for AI bookkeeping. The official Intuit MCP server was broken, so I built a better one.

### 🏛️ Government & Data
**[mcp-civic-data](https://github.com/EricGrill/mcp-civic-data)** - 12 government APIs in one interface. NOAA weather, US Census, NASA imagery, World Bank economics, USGS earthquakes, air quality, and more.

### 🔒 Security & Infrastructure
**[mcp-kali-orchestration](https://github.com/EricGrill/mcp-kali-orchestration)** - 50+ Kali Linux security tools accessible through Claude. Run nmap, metasploit, burp suite via Docker or Proxmox VMs.

**[mcp-proxmox-admin](https://github.com/EricGrill/mcp-proxmox-admin)** - Full Proxmox VE administration. Manage VMs, containers, storage, and networking through natural language.

**[mcp-multi-agent-ssh](https://github.com/EricGrill/mcp-multi-agent-ssh)** - Stateful SSH connections for Claude Code. Manage multiple server sessions persistently.

### 🧠 AI & Memory
**[mcp-memvid-state-service](https://github.com/EricGrill/mcp-memvid-state-service)** - Portable AI memory with vector search and Ollama support. Single-file state management.

---

## Why MCP Changes Everything

Before MCP, every AI tool integration was bespoke:
- Custom APIs
- Authentication nightmares  
- Different formats for every service

MCP standardizes this. One protocol, infinite possibilities.

```bash
# Install any MCP server in seconds
/plugin install mcp-bitcoin-cli@agents-skills-plugins
/plugin install mcp-civic-data@agents-skills-plugins
```

---

## Real-World Use Cases

### Automated Bookkeeping
> "Claude, reconcile last month's invoices and flag any discrepancies over $500."

The QuickBooks MCP server gives Claude 143 tools to handle customers, invoices, bills, journal entries, and more. What used to take hours now takes a conversation.

### Security Auditing
> "Run a vulnerability scan on my web server and generate a remediation report."

The Kali orchestration server delegates security tasks to isolated VMs. Claude can run nmap, nikto, sqlmap, and compile findings without touching your host system.

### Market Intelligence
> "Compare Bitcoin sentiment across prediction markets and flag arbitrage opportunities."

The predictive market server queries 5 platforms simultaneously. Claude detects when markets disagree about the same event.

### On-Chain Operations
> "Timestamp this contract hash on Bitcoin testnet and verify the transaction."

The Bitcoin CLI server handles OP_RETURN operations, document storage, and timestamping. Immutable proof of existence in one command.

---

## Technical Architecture

All servers follow the FastMCP pattern:

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("my-server")

@mcp.tool()
async def my_tool(param: str) -> dict:
    """Tool description for Claude."""
    return {"result": process(param)}

if __name__ == "__main__":
    mcp.run()
```

The protocol handles:
- Tool discovery and schemas
- Type-safe parameter passing
- Streaming responses
- Error handling

---

## Installation

### Via Claude Code Plugins
```bash
/plugin install mcp-bitcoin-cli@agents-skills-plugins
/plugin install mcp-civic-data@agents-skills-plugins
/plugin install mcp-kali-orchestration@agents-skills-plugins
```

### Manual Installation
```bash
# Clone and install any server
git clone https://github.com/EricGrill/mcp-bitcoin-cli
cd mcp-bitcoin-cli
pip install -e .

# Add to Claude Code settings
claude mcp add bitcoin-cli ./src/mcp_bitcoin_cli/server.py
```

---

## What's Next

I'm currently building:
- **MCP server for drone swarm coordination** (PX4/MAVLink)
- **Lightning Network message queue** 
- **Decentralized prediction markets** on Bitcoin

All with the same goal: **removing friction between AI agents and real-world systems.**

---

## Resources

- **All MCP Servers:** [agents-skills-plugins](https://github.com/EricGrill/agents-skills-plugins)
- **My Blog:** [ericgrill.com/blog](https://ericgrill.com/blog)
- **Claude Code:** [Anthropic Documentation](https://docs.anthropic.com/en/docs/agents-and-tools/claude-code/overview)

---

*Building systems that survive when everything else breaks.*

**[Follow me on X](https://x.com/ericgrill)** for more AI infrastructure experiments.

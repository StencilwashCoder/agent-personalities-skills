# Hacker News Comment Drafts

## Thread 1: "Show HN: I built an AI tool that manages my homelab"

**Comment:**

I've been doing something similar with MCP (Model Context Protocol) servers. Built a fleet that lets Claude control my Proxmox cluster, Bitcoin node, and even SSH into multiple boxes simultaneously.

The "aha" moment was realizing I could say:
"Check disk space on all nodes and alert me if any are over 80%"

And get actual actionable results, not just instructions on how to do it myself.

Open sourced everything: https://github.com/EricGrill

My Proxmox MCP server has been particularly useful — natural language VM management is surprisingly efficient once you get used to it.

---

## Thread 2: "Ask HN: What are you using AI coding assistants for?"

**Comment:**

Two big use cases:

**1. Infrastructure management via MCP**
Built MCP servers for Proxmox, SSH fleet management, and Bitcoin Core. Being able to say "restart the web VM and show me the logs" and have it actually happen is game-changing.

**2. Civic data analysis**
Built an MCP server that plugs into 100+ government APIs (FEMA, USGS, Congress, etc.). Great for quick research:
"Show me all earthquakes magnitude 4+ in California this month"
"What legislation was introduced about AI regulation last week?"

The key insight: MCP turns Claude from a chatbot into an operator that can actually DO things.

Repos: https://github.com/EricGrill

---

## Thread 3: "The State of Bitcoin Development Tools"

**Comment:**

Been working on making Bitcoin dev more accessible through AI. Built an MCP server that exposes Bitcoin Core RPC through natural language.

Instead of memorizing:
```
bitcoin-cli getmempoolinfo
```

You just ask:
"What's the mempool looking like?"
"Create a transaction sending 0.01 BTC to bc1q..."
"Show me recent blocks with high fee transactions"

It's early, but the feedback from devs has been positive. Abstracting away RPC complexity without losing power.

https://github.com/EricGrill/mcp-bitcoin-cli

Also experimenting with BRC-20 token support and hardware wallet integrations.

---

## Thread 4: "What infrastructure tools are you excited about?"

**Comment:**

MCP (Model Context Protocol) is changing how I think about infrastructure management.

Built Proxmox and SSH MCP servers that let me manage my homelab through conversation:

- "Start all VMs with 'web' in the name"
- "Show me resource usage across all nodes"
- "Snapshot the database VM before this upgrade"

The Proxmox integration is particularly nice because the API is... quirky. Having Claude handle the translation from intent to API calls saves so much mental overhead.

All open source: https://github.com/EricGrill

Would love to see more infrastructure tools adopt MCP. The standard is young but the potential is huge.

---

**Posting Strategy:**
- Find active HN threads related to AI, Bitcoin, DevOps, homelab
- Add genuine value first, subtle link second
- Don't self-promote too hard
- Focus on insights, not marketing

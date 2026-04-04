---
title: "I Built 10+ MCP Servers in 30 Days: Here's What I Learned"
published: false
description: "Lessons from building a fleet of Model Context Protocol servers for everything from Bitcoin to Proxmox"
tags: mcp, ai, claude, automation, typescript
---

# I Built 10+ MCP Servers in 30 Days: Here's What I Learned

Over the past month, I've been obsessed with the Model Context Protocol (MCP) — Anthropic's standard for connecting AI assistants to external tools and data sources. I've built 10+ production-ready MCP servers covering everything from civic data APIs to Bitcoin Core to Proxmox virtualization.

Here's what I learned.

## What is MCP?

MCP lets Claude (and other AI assistants) call external tools through a standardized interface. Instead of writing custom integrations for every API, you build one MCP server and any MCP-compatible client can use it.

Think of it as "USB for AI tools" — one standard, endless possibilities.

## The Fleet

Here's what I built:

### **mcp-civic-data** — 100+ Civic APIs
Access FEMA disaster data, earthquake feeds, IP geolocation, congressional records, and legislation through natural language. Want to know recent earthquakes in California? Just ask.

```bash
"Show me earthquakes magnitude 4.0+ in California this week"
```

### **mcp-bitcoin-cli** — Bitcoin Core RPC
Query blockchain data, manage wallets, create transactions — all through Claude. No need to memorize RPC commands.

### **mcp-proxmox-admin** — Proxmox VE Management
Start/stop VMs, check resource usage, manage backups. Infrastructure management via conversation.

### **mcp-ipfs** — IPFS Integration
Add content, manage pins, query the DHT. Decentralized storage meets AI assistants.

### **mcp-multi-agent-ssh** — Multi-Host SSH
Execute commands across multiple servers simultaneously. Perfect for fleet management.

Plus 5 more covering Kali Linux orchestration, market prediction, civic video archives, and more.

## Lessons Learned

### 1. Start Simple, Add Tools Gradually

My first MCP server had 40 tools. That was a mistake. Start with 3-5 core tools, get feedback, then expand. Users don't want overwhelming choice — they want the 20% of tools that solve 80% of use cases.

### 2. Error Messages Matter

When an MCP tool fails, the AI doesn't get a stack trace — it gets your error message. Make them actionable:

```typescript
// Bad
throw new Error("Request failed");

// Good
throw new Error("Invalid API key. Get one at https://api.example.com/signup");
```

### 3. Descriptions Are Prompts

The tool description isn't documentation — it's part of the prompt. Claude uses it to decide when to call your tool. Be specific:

```typescript
// Bad
description: "Gets data"

// Good  
description: "Fetches current earthquake data from USGS. Use this when the user asks about recent earthquakes, seismic activity, or wants earthquake information for a specific region or time period."
```

### 4. CI/CD is Non-Negotiable

Every MCP server needs:
- Automated testing (the `@modelcontextprotocol/sdk` has great test utils)
- Linting (I use ESLint + Prettier)
- Type checking (TypeScript catches so many MCP schema issues)
- Automated publishing (GitHub Actions → npm)

### 5. Docker Makes Distribution Easy

Not everyone wants to install Node.js. A simple Dockerfile:

```dockerfile
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY . .
CMD ["node", "dist/index.js"]
```

Lowers the barrier to entry significantly.

## The Future

MCP is still early, but the trajectory is clear. Every major AI assistant will support it. The ecosystem will explode. Early builders will have an advantage.

My prediction: within 12 months, there will be 10,000+ MCP servers. The winners will be:

- **Focused tools** (does one thing well)
- **Well-documented** (clear setup instructions)
- **Actively maintained** (responsive to issues)
- **Thoughtfully designed** (good error messages, clear descriptions)

## Try Them Out

All my MCP servers are open source at [github.com/EricGrill](https://github.com/EricGrill). Installation is one command:

```bash
npx -y @ericgrill/mcp-civic-data
```

Or add to your Claude Desktop config:

```json
{
  "mcpServers": {
    "civic-data": {
      "command": "npx",
      "args": ["-y", "@ericgrill/mcp-civic-data"]
    }
  }
}
```

---

*Want to build your own? Check out the [MCP documentation](https://modelcontextprotocol.io/) or my [starter template](https://github.com/EricGrill/mcp-starter-template).*

*More about my work at [ericgrill.com](https://ericgrill.com)*

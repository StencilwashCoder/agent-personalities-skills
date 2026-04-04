# Stack Overflow Answers — Drafts

## Question 1: "How to query Bitcoin blockchain data programmatically?"

**Answer:**

You have a few options depending on your use case:

**1. Bitcoin Core RPC**
If you're running a node, use the JSON-RPC API:
```bash
bitcoin-cli getblockchaininfo
bitcoin-cli getmempoolinfo
```

Or programmatically with any HTTP client.

**2. Block Explorers (APIs)**
- Blockstream.info API (free, no auth)
- mempool.space API
- Blockchain.info API

**3. MCP (Model Context Protocol)**
If you're building AI-powered tools, I created an MCP server that exposes Bitcoin Core RPC through natural language:

```typescript
// Instead of:
bitcoin-cli getmempoolinfo

// You can say:
"What's the mempool looking like?"
"Show me recent high-fee transactions"
```

https://github.com/EricGrill/mcp-bitcoin-cli

**Recommendation:**
- For production apps → Use Bitcoin Core RPC directly
- For prototyping → Blockstream API is solid
- For AI assistants → MCP abstraction is convenient

---

## Question 2: "Best way to manage Proxmox VMs programmatically?"

**Answer:**

Proxmox has a REST API, but it's... quirky. Here's what works:

**1. Direct API**
```bash
curl -k -H "Authorization: PVEAPIToken=USER@REALM!TOKENID=UUID" \
  https://proxmox:8006/api2/json/nodes
```

**2. Python Proxmoxer**
```python
from proxmoxer import ProxmoxAPI
proxmox = ProxmoxAPI('proxmox', user='root@pam', token_value='secret')
for vm in proxmox.nodes('pve').qemu.get():
    print(vm['vmid'], vm['name'])
```

**3. MCP (Model Context Protocol)**
If you want natural language control:

I built an MCP server that lets you say:
```
"Start all web servers"
"Show me resource usage on node pve1"
"Create a snapshot of VM 100 before upgrading"
```

It handles the API quirks for you: https://github.com/EricGrill/mcp-proxmox-admin

**Gotchas:**
- API tokens need correct permissions (VMAdmin minimum for most operations)
- CSRF tokens required for POST requests
- Some operations are async (check task status)

---

## Question 3: "How do I access government data APIs for civic projects?"

**Answer:**

There's a treasure trove of US government APIs:

**FEMA:** disaster declarations, assistance data
```
https://www.fema.gov/api/open
```

**USGS:** earthquakes, geological data
```
https://earthquake.usgs.gov/fdsnws/event/1/
```

**Congress.gov:** legislation, members
```
https://api.congress.gov/
```

**IP Geolocation:**
```
https://ipapi.co/json/
```

**Combined Access:**
I built an MCP server that aggregates 100+ civic APIs into one interface:

```typescript
// Ask things like:
"Show me recent FEMA disaster declarations"
"What earthquakes happened in California this week?"
"Who represents ZIP code 90210 in Congress?"
```

https://github.com/EricGrill/mcp-civic-data

**Rate Limits:**
Most are generous (1000+ req/day), but check each API's docs.

---

## Question 4: "What is the Model Context Protocol (MCP)?"

**Answer:**

MCP is Anthropic's open standard for connecting AI assistants to external tools and data sources.

**The Problem:**
Every AI integration was custom. Want Claude to query your database? Write custom code. Want it to control your infrastructure? More custom code.

**MCP Solution:**
One standard protocol. Build an MCP server once, any MCP-compatible client can use it.

**How it works:**
1. You build an MCP server that exposes "tools" (functions)
2. Each tool has a schema (name, description, parameters)
3. AI assistants discover and call these tools automatically
4. Your server executes the function and returns results

**Example:**
```typescript
// MCP Tool definition
{
  name: "get_earthquakes",
  description: "Fetches earthquake data from USGS",
  parameters: {
    magnitude: { type: "number", minimum: 0 },
    region: { type: "string" }
  }
}

// User asks:
"Show me earthquakes magnitude 4+ in California"

// Claude automatically calls your tool with:
{ magnitude: 4, region: "California" }
```

**Ecosystem:**
- Official SDKs: TypeScript, Python
- Servers: GitHub, Slack, PostgreSQL, and 1000+ community servers
- Clients: Claude Desktop, Cursor, and growing

**Getting Started:**
https://modelcontextprotocol.io/introduction

---

**Posting Strategy:**
- Search for relevant questions daily
- Provide genuine value first
- Link only when truly relevant
- Build reputation gradually

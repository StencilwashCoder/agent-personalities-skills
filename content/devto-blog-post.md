# I Built 10+ MCP Servers: Lessons from the Agent Frontier

Over the past few months, I've been deep in the trenches building MCP (Model Context Protocol) servers that give Claude direct access to infrastructure, blockchains, security tools, and more. What started as a curiosity about extending AI capabilities has turned into **12 production MCP servers** with over **400+ combined tools** that thousands of developers now use daily.

This is what I learned.

---

## What Actually Worked

### 1. Start with Real Pain Points

Every successful MCP server I built solved a problem I personally experienced. The **mcp-proxmox-admin** server wasn't born from theory—it came from me being sick of switching between CLI commands and web interfaces to manage VMs while debugging infrastructure issues.

**Example:** Instead of `qm list && qm config 100`, I can now say:
```
"Show me all VMs with high memory usage and create a snapshot of the busy ones"
```

The server translates intent into 3 separate Proxmox API calls, aggregates the results, and presents a summary. That's the power of MCP—**composable, intent-driven infrastructure**.

### 2. Embrace the Transport Layer Philosophy

MCP servers are essentially **transport layers for capability**. The best ones don't try to be smart; they expose primitives that the LLM can compose.

Take **mcp-ipfs** with its 34 tools:
```typescript
// Low-level primitives that compose into workflows
- ipfs_add          // Add content
- ipfs_cat          // Retrieve content  
- ipfs_pin          // Persist content
- ipfs_dag_put      // Structured data
- ipfs_name_publish // IPNS updates
```

The LLM chains these together. I don't hardcode "upload and pin"—I expose both operations and let the model decide when each is appropriate.

### 3. Safety-First Defaults Save Lives

The **mcp-kali-orchestration** server wraps 50+ security tools including nmap, Metasploit, and password crackers. This could be catastrophic in the wrong hands.

My approach:
```python
# Every destructive operation requires explicit confirmation
- Default to read-only reconnaissance
- Dry-run mode shows command without execution  
- "authorize_scope" tool required before exploitation
- Full audit logging of all commands
```

Users must explicitly authorize specific target scopes. No "oops I scanned the wrong IP range" moments.

### 4. Pluggable Architectures Win

The **mcp-memvid-state-service** started with just local embedding models. Then users wanted Ollama support. Then OpenAI. 

Instead of branching logic everywhere, I designed a backend interface early:
```typescript
interface EmbeddingBackend {
  embed(text: string): Promise<number[]>;
  supports(model: string): boolean;
}

// Implemented by:
// - LocalOnnxBackend (bge-small, nomic)
// - OllamaBackend (any Ollama model)
// - OpenAIBackend (ada, etc)
```

Adding a new provider now takes ~30 lines of code.

### 5. State Management is the Real Challenge

MCP servers are stateless by design, but real work requires state. The **mcp-multi-agent-ssh** server manages persistent SSH connections across Claude sessions.

The solution: a connection pool with session affinity:
```python
# Connection keyed by (host, user, session_id)
pool = {
  "('prod-db-01', 'ubuntu', 'claude-session-abc123')": <SSHConnection>,
}
```

Credentials are encrypted with AES-256-GCM using a master password. Sessions survive Claude restarts but expire after configurable idle timeouts.

---

## What Didn't Work (And Why)

### ❌ Trying to Be Too Clever

My first attempt at **mcp-bitcoin-cli** tried to "help" by estimating fees and suggesting optimal times. Users hated it—they wanted raw control. I ripped out the smart logic and exposed primitives instead. Engagement doubled.

**Lesson:** Don't second-guess power users. Expose capabilities, let them compose.

### ❌ Monolithic Tool Designs

Early versions of **mcp-civic-data** had tools like `get_weather_forecast(location, days, hourly, alerts, ...)`. Massive parameter lists that confused the LLM and broke when APIs changed.

**The fix:** Granular tools:
```typescript
- weather_current(location)
- weather_forecast_daily(location, days)
- weather_alerts(location)
- weather_history(location, date)
```

The LLM chains what it needs. Individual tools are easier to test and version.

### ❌ Ignoring Platform Differences

The **mcp-memvid-state-service** uses ONNX for local embeddings. Works great on Linux and macOS ARM64. Windows? Completely broken because the Rust binding situation is a nightmare.

I had to:
- Detect platform at runtime
- Degrade gracefully to Ollama/OpenAI on Windows
- Document the limitation clearly

**Lesson:** Cross-platform is harder than you think. Plan for graceful degradation.

### ❌ Underestimating Error Context

Early error messages were terse: `"Connection failed"`. Claude couldn't recover because it didn't know *why*.

Now every error includes:
```json
{
  "error": "Connection failed",
  "code": "SSH_AUTH_FAILED",
  "suggestions": [
    "Check if the key file exists at ~/.ssh/id_rsa",
    "Verify the remote host accepts key authentication",
    "Try password auth if keys aren't set up"
  ],
  "docs_url": "https://github.com/ericgrill/mcp-multi-agent-ssh/blob/main/docs/auth.md"
}
```

The LLM can actually suggest fixes now.

---

## Architecture Patterns That Actually Work

### The Handler Registry Pattern

All my TypeScript MCP servers use a consistent structure:
```typescript
// tools/index.ts
export const handlers: Record<string, ToolHandler> = {
  'vm_list': handleVmList,
  'vm_start': handleVmStart,
  'vm_stop': handleVmStop,
  // ...
};

// server.ts
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const handler = handlers[request.params.name];
  if (!handler) throw new Error(`Unknown tool: ${request.params.name}`);
  return handler(request.params.arguments);
});
```

Adding a new tool is one line. Testing is isolated. The LLM sees a clean schema.

### Background Job Management

For long-running operations (IPFS pins, VM provisioning), synchronous tools block Claude. The solution:
```typescript
// Returns immediately with job_id
const job = await submit_background_job({
  tool: 'ipfs_add_large_file',
  params: { path: '/data/10gb-dump.sql' }
});

// Poll or use callbacks
const status = await get_job_status(job.id);
```

**mcp-ipfs** uses this for large file operations. Users get progress updates without freezing their agent session.

### Configuration Over Convention

Every server reads from env vars AND config files, with clear precedence:
```typescript
const config = {
  // 1. Environment variables (highest priority)
  apiKey: process.env.MCP_SERVER_API_KEY 
    // 2. Config file
    ?? readConfigFile().apiKey
    // 3. Sensible defaults
    ?? 'default-value',
};
```

Users can inject secrets via env vars in production or use files for local dev.

---

## The Fleet: All 12 Servers

| Server | Tools | Description | Link |
|--------|-------|-------------|------|
| **mcp-proxmox-admin** | 16 | VM/container management via natural language | [GitHub](https://github.com/EricGrill/mcp-proxmox-admin) |
| **mcp-kali-orchestration** | 50+ | Security tools (nmap, Metasploit, etc.) | [GitHub](https://github.com/EricGrill/mcp-kali-orchestration) |
| **mcp-bitcoin-cli** | 16 | OP_RETURN, BRC-20, on-chain timestamps | [GitHub](https://github.com/EricGrill/mcp-bitcoin-cli) |
| **mcp-multi-agent-ssh** | 8 | Persistent SSH with encrypted credentials | [GitHub](https://github.com/EricGrill/mcp-multi-agent-ssh) |
| **mcp-multi-agent-server-delegation** | 5 | Isolated VM task execution | [GitHub](https://github.com/EricGrill/mcp-multi-agent-server-delegation) |
| **mcp-predictive-market** | 8 | Query 5 prediction markets with arbitrage detection | [GitHub](https://github.com/EricGrill/mcp-predictive-market) |
| **mcp-civic-data** | 22 | 7 government APIs (weather, census, NASA) | [GitHub](https://github.com/EricGrill/mcp-civic-data) |
| **mcp-memvid-state-service** | 10 | AI memory layer with vector search | [GitHub](https://github.com/EricGrill/mcp-memvid-state-service) |
| **mcp-market-data** | 6 | Real-time stock/crypto/forex via Yahoo Finance | [GitHub](https://github.com/EricGrill/mcp-market-data) |
| **mcp-ipfs** | 34 | IPFS storage, pinning, DAG, DHT | [GitHub](https://github.com/EricGrill/mcp-ipfs) |
| **quickbooks-online-mcp-server** | 55 | QuickBooks CRUD for invoices, customers, bills | [GitHub](https://github.com/EricGrill/quickbooks-online-mcp-server) |
| **fulcrum-mcp** | 50+ | Fulcrum AI orchestration platform | [GitHub](https://github.com/EricGrill/fulcrum-mcp) |

---

## Practical Lessons for MCP Builders

### 1. Tool Naming Matters

Bad: `do_the_thing`
Good: `proxmox_vm_start`

Use `domain_verb_noun` patterns. Claude understands them better, and users can search docs effectively.

### 2. Schema Descriptions Are Your UX

Every parameter description is surfaced to the LLM. Be explicit:
```json
{
  "name": "timeout",
  "type": "number",
  "description": "Maximum seconds to wait for VM shutdown before force-stopping. Default: 30, Max: 300"
}
```

The LLM uses this to make good decisions. Bad descriptions = bad behavior.

### 3. Test with Real Claude Sessions

Unit tests catch syntax errors. Only real Claude sessions reveal:
- Tool selection mistakes (wrong tool for the job)
- Parameter confusion (LLM sends strings where numbers expected)
- Context overflow (too much output causes truncation)

I maintain a `test-session.md` for each server with real conversation flows.

### 4. Version Your Schemas

MCP doesn't have built-in versioning. Add it yourself:
```typescript
// server_info tool returns this
{
  "server_version": "1.2.3",
  "schema_version": "2024-01",
  "tools_hash": "abc123..." // hash of tool schemas
}
```

Clients can detect mismatches and prompt for updates.

---

## The Future I'm Building Toward

These 12 servers are just the foundation. I'm working on:

- **Cross-server composition**: The delegation server can spin up VMs that have the Kali server pre-installed
- **Autonomous agent loops**: Servers that can call themselves recursively for complex tasks
- **Distributed MCP**: Servers running on edge devices, coordinated by a central Claude instance

The Model Context Protocol isn't just an API wrapper—it's a new interface paradigm. We're moving from **GUIs and CLIs** to **conversational intent**.

And we're just getting started.

---

## Start Building

If you're interested in MCP development:

1. Read the [MCP Specification](https://modelcontextprotocol.io/)
2. Clone one of my servers and modify it
3. Join the [Claude Code Plugin Marketplace](https://github.com/EricGrill/agents-skills-plugins) ecosystem

Find all my MCP servers on [GitHub](https://github.com/EricGrill) and read more about my work at [ericgrill.com](https://ericgrill.com).

---

*What's the most painful workflow you deal with daily? That's probably your next MCP server.*

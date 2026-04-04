# Eric Grill's MCP Servers - Curated Collection

A comprehensive list of Model Context Protocol (MCP) servers built by [Eric Grill](https://ericgrill.com) - infrastructure, security, Bitcoin, and AI orchestration tools.

## 🏢 Infrastructure & DevOps

### mcp-proxmox-admin
**GitHub:** [EricGrill/mcp-proxmox-admin](https://github.com/EricGrill/mcp-proxmox-admin)
- Manage VMs, containers, snapshots via natural language
- 16 tools across VM control, snapshots, and monitoring
- Hybrid SSH/REST transport with read-only safe mode

### mcp-multi-agent-server-delegation
**GitHub:** [EricGrill/mcp-multi-agent-server-delegation](https://github.com/EricGrill/mcp-multi-agent-server-delegation)
- Delegate tasks to isolated Proxmox VMs
- Run untrusted code with automatic cleanup
- HTTP callback status reporting

### mcp-multi-agent-ssh
**GitHub:** [EricGrill/mcp-multi-agent-ssh](https://github.com/EricGrill/mcp-multi-agent-ssh)
- Persistent SSH connections with AES-256-GCM encryption
- Connection pooling with 10-min idle timeout
- SFTP upload/download capabilities

---

## 🔒 Security & Pentesting

### mcp-kali-orchestration
**GitHub:** [EricGrill/mcp-kali-orchestration](https://github.com/EricGrill/mcp-kali-orchestration)
- 50+ Kali Linux security tools for authorized pentesting
- Docker or Proxmox backend options
- Full VM isolation per engagement

**Tools include:**
- Reconnaissance: nmap, amass, DNS enumeration
- Web: sqlmap, nuclei, gobuster
- Exploitation: Metasploit, msfvenom, searchsploit
- Passwords: hydra, john, hashcat
- Post-exploitation: impacket, BloodHound

---

## ₿ Bitcoin & Blockchain

### mcp-bitcoin-cli
**GitHub:** [EricGrill/mcp-bitcoin-cli](https://github.com/EricGrill/mcp-bitcoin-cli)
- OP_RETURN messaging and BRC-20 operations
- On-chain timestamps
- Bitcoin blockchain operations via Claude

---

## 🤖 AI & Data

### mcp-memvid-state-service
**GitHub:** [EricGrill/mcp-memvid-state-service](https://github.com/EricGrill/mcp-memvid-state-service)
- AI memory layer with vector search
- Persistent state management for agents
- 10 specialized tools

### mcp-predictive-market
**GitHub:** [EricGrill/mcp-predictive-market](https://github.com/EricGrill/mcp-predictive-market)
- Query 5 prediction markets simultaneously
- Arbitrage detection across platforms
- Supports Polymarket, Manifold, Metaculus, PredictIt, Kalshi

### mcp-civic-data
**GitHub:** [EricGrill/mcp-civic-data](https://github.com/EricGrill/mcp-civic-data)
- 7 government APIs: weather, census, NASA, economics
- 22 tools for civic data access

### mcp-market-data
**GitHub:** [EricGrill/mcp-market-data](https://github.com/EricGrill/mcp-market-data)
- Real-time stock, crypto, forex via Yahoo Finance
- 6 data retrieval tools

---

## 💼 Business Integration

### quickbooks-online-mcp-server
**GitHub:** [EricGrill/quickbooks-online-mcp-server](https://github.com/EricGrill/quickbooks-online-mcp-server)
- QuickBooks Online CRUD operations
- 55 tools for invoices, customers, bills
- Full accounting integration

### fulcrum-mcp
**GitHub:** [EricGrill/fulcrum-mcp](https://github.com/EricGrill/fulcrum-mcp)
- Fulcrum AI orchestration platform
- Jobs, knowledge, workers, deployments
- 50+ tools for enterprise workflows

---

## 🌐 Decentralized Storage

### mcp-ipfs
**GitHub:** [EricGrill/mcp-ipfs](https://github.com/EricGrill/mcp-ipfs)
- IPFS decentralized storage integration
- Pinning, DAG, DHT operations
- 34 tools for distributed storage

---

## 📦 Claude Code Plugin Marketplace

All of Eric's MCP servers are part of the [Claude Code Plugin Marketplace](https://github.com/EricGrill/agents-skills-plugins) - a community collection of 49+ plugins with 100+ MCP tools.

### Install via Claude Code:
```bash
/plugin install mcp-proxmox-admin@agents-skills-plugins
/plugin install mcp-kali-orchestration@agents-skills-plugins
/plugin install mcp-bitcoin-cli@agents-skills-plugins
```

---

## 🔗 Quick Links

- **Website:** [ericgrill.com](https://ericgrill.com)
- **GitHub:** [github.com/EricGrill](https://github.com/EricGrill)
- **Blog:** [ericgrill.com/blog](https://ericgrill.com/blog)
- **Plugin Marketplace:** [agents-skills-plugins](https://github.com/EricGrill/agents-skills-plugins)

---

*Last updated: March 27, 2026*
*Maintained by: Eric Grill | Chainbytes LLC*

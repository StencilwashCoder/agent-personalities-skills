# PR Content for Eric Grill's MCP Servers

> **Note:** The target repository `punkpeye/awesome-mcp-servers` does not exist. The most popular and actively maintained `awesome-mcp-servers` repo is `appcypher/awesome-mcp-servers` (5.3k stars). These PRs are prepared for that repository.

---

## PR 1: Add mcp-proxmox-admin

### Title
Add mcp-proxmox-admin: Proxmox VE management via Claude

### Branch Name
`add-mcp-proxmox-admin`

### README Addition (in Sandbox & Virtualization section)
```markdown
- [mcp-proxmox-admin](https://github.com/EricGrill/mcp-proxmox-admin) - Manage Proxmox VE infrastructure through Claude - VMs, containers, snapshots, and cluster health via natural language with 16 tools
```

### PR Description
```markdown
**Add mcp-proxmox-admin to Sandbox & Virtualization section**

This PR adds [mcp-proxmox-admin](https://github.com/EricGrill/mcp-proxmox-admin) - an MCP server that enables Claude to manage Proxmox VE infrastructure.

**Features:**
- 16 tools for VM and container management
- Full VM control (start, stop, shutdown, restart)
- LXC container management
- Snapshot operations (create, restore, delete)
- Hybrid transport (SSH + REST API auto-selection)
- Safe mode for read-only monitoring
- Works with Claude Desktop, Cursor, and any MCP-compatible client

**Repository:** https://github.com/EricGrill/mcp-proxmox-admin
**License:** MIT
**Language:** TypeScript
```

---

## PR 2: Add mcp-bitcoin-cli

### Title
Add mcp-bitcoin-cli: Bitcoin Core RPC integration

### Branch Name
`add-mcp-bitcoin-cli`

### README Addition (in Finance section)
```markdown
- [mcp-bitcoin-cli](https://github.com/EricGrill/mcp-bitcoin-cli) - Bitcoin blockchain operations via Claude - OP_RETURN data embedding, BRC-20 tokens, timestamps, and custom protocols with 16 tools
```

### PR Description
```markdown
**Add mcp-bitcoin-cli to Finance section**

This PR adds [mcp-bitcoin-cli](https://github.com/EricGrill/mcp-bitcoin-cli) - an MCP server for Bitcoin OP_RETURN data operations and blockchain interaction.

**Features:**
- 16 tools for Bitcoin operations
- OP_RETURN data embedding (up to 100KB)
- BRC-20 token operations (deploy, mint, transfer)
- SHA-256/SHA3 timestamping and verification
- Document storage on blockchain
- BTCD envelope format for data discoverability
- Testnet default with dry-run safety mode
- Works with Claude Desktop, Cursor, and any MCP-compatible client

**Repository:** https://github.com/EricGrill/mcp-bitcoin-cli
**License:** MIT
**Language:** Python 3.11+
```

---

## PR 3: Add mcp-kali-orchestration

### Title
Add mcp-kali-orchestration: Security tool orchestration

### Branch Name
`add-mcp-kali-orchestration`

### README Addition (in Security section)
```markdown
- [mcp-kali-orchestration](https://github.com/EricGrill/mcp-kali-orchestration) - Orchestrate Kali Linux security tools via MCP - 50+ pentesting tools including nmap, Metasploit, sqlmap with Docker/Proxmox backend
```

### PR Description
```markdown
**Add mcp-kali-orchestration to Security section**

This PR adds [mcp-kali-orchestration](https://github.com/EricGrill/mcp-kali-orchestration) - an MCP server that spins up Kali Linux instances and exposes 50+ professional security tools to Claude.

**Features:**
- 50+ security tools exposed via natural language
- Categories: Reconnaissance (9), Web Testing (12), Exploitation (4), Password Attacks (7), Post-Exploitation (7), Network (7)
- Dual backend: Docker (fast, local) or Proxmox (full VM isolation)
- On-demand instance lifecycle management
- Tools include: nmap, metasploit, sqlmap, nikto, nuclei, gobuster, hydra, john, hashcat, bloodhound, impacket, and more
- Intended for authorized penetration testing, CTFs, and security research

**Repository:** https://github.com/EricGrill/mcp-kali-orchestration
**License:** MIT
**Language:** TypeScript
```

---

## PR 4: Add mcp-multi-agent-ssh

### Title
Add mcp-multi-agent-ssh: SSH agent coordination with persistent connections

### Branch Name
`add-mcp-multi-agent-ssh`

### README Addition (in System Automation section)
```markdown
- [mcp-multi-agent-ssh](https://github.com/EricGrill/mcp-multi-agent-ssh) - Stateful SSH connections for Claude Code with AES-256-GCM encrypted credentials, auto-reconnect, and SFTP support
```

### PR Description
```markdown
**Add mcp-multi-agent-ssh to System Automation section**

This PR adds [mcp-multi-agent-ssh](https://github.com/EricGrill/mcp-multi-agent-ssh) - an MCP server providing persistent SSH connections for Claude Code.

**Features:**
- 10 tools for SSH connection management and file operations
- Persistent connections (stay open for 10 minutes of inactivity)
- AES-256-GCM encrypted credential storage
- Auto-reconnect when connections expire or drop
- SFTP support for file upload/download/list
- Host-based authentication matching
- Available via NPX or Docker
- Works with Claude Desktop, Cursor, and any MCP-compatible client

**Security:**
- PBKDF2 key derivation with 100,000 iterations
- File permissions 600 on credential storage
- Per-host credential isolation

**Repository:** https://github.com/EricGrill/mcp-multi-agent-ssh
**License:** MIT
**Language:** Python 3.10+
```

---

## PR 5: Add mcp-civic-data

### Title
Add mcp-civic-data: Civic data integration with 13 government APIs

### Branch Name
`add-mcp-civic-data`

### README Addition (in Research & Data section)
```markdown
- [mcp-civic-data](https://github.com/EricGrill/mcp-civic-data) - Access 13 free government and open data APIs including weather, earthquakes, air quality, NASA, census, and economics data
```

### PR Description
```markdown
**Add mcp-civic-data to Research & Data section**

This PR adds [mcp-civic-data](https://github.com/EricGrill/mcp-civic-data) - an MCP server connecting AI agents to 13 free, authoritative government data APIs.

**Features:**
- 40 tools across 13 data sources
- Earth & Environment: NOAA Weather, OpenWeather, OpenAQ, USGS Water, Safecast
- Hazards & Events: USGS Earthquakes, NASA FIRMS, NOAA Space Weather
- Demographics & Economics: US Census, World Bank
- Open Data: Data.gov, EU Open Data, NASA (APOD, Mars rover)
- No API keys required for 11 of 13 sources
- High-level tools for common queries + raw query access

**Use Cases:**
- Weather forecasts and severe weather alerts
- Real-time earthquake monitoring
- Air quality and radiation level checks
- Wildfire tracking from satellite data
- Demographic and economic analysis
- Space weather monitoring

**Repository:** https://github.com/EricGrill/mcp-civic-data
**License:** MIT
**Language:** Python 3.11+
```

---

## How to Submit These PRs

Since the GitHub CLI account is suspended, you'll need to submit these PRs manually:

### Option 1: Web Interface (Easiest)

1. **Fork the repository:**
   - Go to https://github.com/appcypher/awesome-mcp-servers
   - Click the "Fork" button
   - Wait for the fork to be created

2. **Edit the README for each PR:**
   - Navigate to your fork: `https://github.com/YOUR_USERNAME/awesome-mcp-servers`
   - Click on `README.md`
   - Click the pencil icon (Edit)
   - Find the appropriate section for each server
   - Add the entry in the correct alphabetical/format position
   - Commit with message: `Add [server-name] to [section]`

3. **Create Pull Request:**
   - Go back to https://github.com/appcypher/awesome-mcp-servers
   - Click "New Pull Request"
   - Click "compare across forks"
   - Select your fork and branch
   - Fill in the PR title and description from above
   - Submit

### Option 2: Command Line (with your own GitHub token)

```bash
# Set your GitHub token
export GITHUB_TOKEN=your_personal_access_token

# Clone your fork
git clone https://github.com/YOUR_USERNAME/awesome-mcp-servers.git
cd awesome-mcp-servers

# Create a branch for the first PR
git checkout -b add-mcp-proxmox-admin

# Edit README.md to add the entry
# ... edit the file ...

# Commit and push
git add README.md
git commit -m "Add mcp-proxmox-admin to Sandbox & Virtualization section"
git push origin add-mcp-proxmox-admin

# Create PR via gh CLI (if you have auth) or web interface
gh pr create --title "Add mcp-proxmox-admin: Proxmox VE management via Claude" \
             --body-file pr-description.md \
             --repo appcypher/awesome-mcp-servers

# Repeat for the other 4 servers
```

---

## Category Mapping Summary

| Server | Category | Section Header |
|--------|----------|----------------|
| mcp-proxmox-admin | Sandbox & Virtualization | `### 📦 Sandbox & Virtualization` |
| mcp-bitcoin-cli | Finance | `### 💹 Finance` |
| mcp-kali-orchestration | Security | `### 🔒 Security` |
| mcp-multi-agent-ssh | System Automation | `### 🤖 System Automation` |
| mcp-civic-data | Research & Data | `### 🧬 Research & Data` |

---

## Verification Checklist

- [ ] All 5 repositories exist and are publicly accessible
- [ ] All repos have MIT licenses
- [ ] Descriptions are accurate and concise
- [ ] Format matches existing entries (icon + link + description)
- [ ] Each PR is submitted separately (as requested)

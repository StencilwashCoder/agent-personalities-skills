# Awesome MCP Servers - PR Submission Details

This document contains the exact content to add Eric Grill's MCP servers to punkpeye/awesome-mcp-servers.

## Repository Information

- **Target Repo:** https://github.com/punkpeye/awesome-mcp-servers
- **Fork URL:** https://github.com/EricGrill/awesome-mcp-servers (create if doesn't exist)
- **Author Website:** https://ericgrill.com

---

## MCP Server Entries (in awesome-list format)

### 1. mcp-proxmox-admin
**Category:** Developer Tools / Cloud Platforms

**Entry to add:**
```markdown
- EricGrill/mcp-proxmox-admin 📇 ☁️ 🐧 - Proxmox VE infrastructure management with 16+ tools for VMs, containers, snapshots, and cluster monitoring. Hybrid SSH/REST transport with read-only safe mode.
```

**PR Title:** `Add mcp-proxmox-admin`

**PR Description:**
```markdown
## Description

Add [mcp-proxmox-admin](https://github.com/EricGrill/mcp-proxmox-admin) to the awesome MCP servers list.

**Features:**
- 16+ tools for Proxmox VE management
- VM control (start, stop, restart, migrate)
- LXC container management
- Snapshot operations (create, rollback, delete)
- Node, storage, and cluster monitoring
- Hybrid SSH/REST transport
- Optional read-only safe mode
- API token or SSH key authentication

**Links:**
- GitHub: https://github.com/EricGrill/mcp-proxmox-admin
- Author: https://ericgrill.com
- Guide: Claude Code Rescued My Proxmox Cluster

---
Submitted by @EricGrill
```

---

### 2. mcp-bitcoin-cli
**Category:** Finance & Fintech

**Entry to add:**
```markdown
- EricGrill/mcp-bitcoin-cli 📇 ☁️ ₿ - Bitcoin blockchain operations via OP_RETURN, BRC-20 tokens, and on-chain timestamping. Document storage up to 100KB with testnet default for safety.
```

**PR Title:** `Add mcp-bitcoin-cli`

**PR Description:**
```markdown
## Description

Add [mcp-bitcoin-cli](https://github.com/EricGrill/mcp-bitcoin-cli) to the awesome MCP servers list.

**Features:**
- Document storage on Bitcoin blockchain (up to 100KB)
- SHA-256/SHA3 timestamping
- BRC-20 token operations (deploy, mint, transfer)
- Custom BTCD envelope protocol
- Testnet default for safety
- Dry-run mode for testing
- Fee warnings and data size validation
- Supports mainnet, testnet, signet, regtest

**Links:**
- GitHub: https://github.com/EricGrill/mcp-bitcoin-cli
- Author: https://ericgrill.com
- Guide: From OP_RETURN to Lightning

---
Submitted by @EricGrill
```

---

### 3. mcp-kali-orchestration
**Category:** Security

**Entry to add:**
```markdown
- EricGrill/mcp-kali-orchestration 📇 🏠 ☁️ 🐧 - Kali Linux security tool orchestration with 50+ professional tools. nmap, Metasploit, sqlmap, nuclei for authorized pentesting via Docker/Proxmox backends.
```

**PR Title:** `Add mcp-kali-orchestration`

**PR Description:**
```markdown
## Description

Add [mcp-kali-orchestration](https://github.com/EricGrill/mcp-kali-orchestration) to the awesome MCP servers list.

**Features:**
- 50+ Kali Linux security tools exposed via MCP
- Tool categories:
  - Reconnaissance: nmap, amass, DNS enumeration
  - Web Application: sqlmap, nuclei, gobuster
  - Exploitation: Metasploit, msfvenom
  - Password Attacks: hydra, john, hashcat
  - Post-Exploitation: impacket, crackmapexec, BloodHound
  - Network: tcpdump, Wireshark, responder
- Dual backends: Docker (fast) or Proxmox (full VM isolation)
- Natural language control through Claude

**Links:**
- GitHub: https://github.com/EricGrill/mcp-kali-orchestration
- Author: https://ericgrill.com
- Guide: I Gave Claude Code 50+ Kali Linux Tools

**Security Notice:** For authorized penetration testing, CTFs, and security research only.

---
Submitted by @EricGrill
```

---

### 4. mcp-multi-agent-ssh
**Category:** Developer Tools

**Entry to add:**
```markdown
- EricGrill/mcp-multi-agent-ssh 📇 🏠 🐧 - Persistent SSH connections with AES-256-GCM encrypted credential storage. Connection pooling with 10-min idle timeout, SFTP support, and PBKDF2 key derivation.
```

**PR Title:** `Add mcp-multi-agent-ssh`

**PR Description:**
```markdown
## Description

Add [mcp-multi-agent-ssh](https://github.com/EricGrill/mcp-multi-agent-ssh) to the awesome MCP servers list.

**Features:**
- Persistent SSH connections (no more open/close per command)
- AES-256-GCM encryption for stored credentials
- PBKDF2 key derivation (100k iterations)
- Master password protection
- Connection pooling with auto-reconnection
- 10-minute idle timeout
- SFTP upload/download support
- File permissions (600) for security

**Links:**
- GitHub: https://github.com/EricGrill/mcp-multi-agent-ssh
- Author: https://ericgrill.com

---
Submitted by @EricGrill
```

---

### 5. mcp-civic-data
**Category:** Data & Research (or Cloud Platforms if no Data category)

**Entry to add:**
```markdown
- EricGrill/mcp-civic-data 📇 ☁️ - 7 government APIs in one MCP server. Weather, Census, NASA, economic indicators. Most features require no API keys - free access to open government data.
```

**PR Title:** `Add mcp-civic-data`

**PR Description:**
```markdown
## Description

Add [mcp-civic-data](https://github.com/EricGrill/mcp-civic-data) to the awesome MCP servers list.

**Features:**
- 22 tools across 7 government/open data APIs
- NOAA Weather API (forecasts, alerts, observations)
- US Census Bureau (demographics, population data)
- NASA APIs (APOD, imagery, earth data)
- Federal Reserve Economic Data (FRED)
- Most features require no API keys
- Free access to open government data

**Links:**
- GitHub: https://github.com/EricGrill/mcp-civic-data
- Author: https://ericgrill.com
- Guide: I Got Tired of Hunting for API Code

---
Submitted by @EricGrill
```

---

## Emoji Legend Reference

Based on the awesome-mcp-servers format:
- 📇 - TypeScript codebase
- 🐍 - Python codebase
- 🏠 - Local Service (runs locally)
- ☁️ - Cloud Service (uses remote APIs)
- 🐧 - For Linux
- ₿ - Bitcoin-related (custom for mcp-bitcoin-cli)

---

## Manual Submission Steps (if script fails)

1. **Fork the repo:**
   ```bash
   gh repo fork punkpeye/awesome-mcp-servers
   ```

2. **Clone your fork:**
   ```bash
   gh repo clone EricGrill/awesome-mcp-servers
   cd awesome-mcp-servers
   ```

3. **Create a branch for each MCP server:**
   ```bash
   git checkout -b add-mcp-proxmox-admin
   ```

4. **Edit README.md** - Find the appropriate category section and add the entry

5. **Commit and push:**
   ```bash
   git add README.md
   git commit -m "Add mcp-proxmox-admin to awesome-mcp-servers list"
   git push -u origin add-mcp-proxmox-admin
   ```

6. **Create PR via web or CLI:**
   ```bash
   gh pr create --repo punkpeye/awesome-mcp-servers \
     --title "Add mcp-proxmox-admin" \
     --body "..."
   ```

7. **Repeat for all 5 servers**

---

## Expected PR URLs After Submission

After creating the PRs, they will be available at:
- https://github.com/punkpeye/awesome-mcp-servers/pull/XXX (mcp-proxmox-admin)
- https://github.com/punkpeye/awesome-mcp-servers/pull/XXX (mcp-bitcoin-cli)
- https://github.com/punkpeye/awesome-mcp-servers/pull/XXX (mcp-kali-orchestration)
- https://github.com/punkpeye/awesome-mcp-servers/pull/XXX (mcp-multi-agent-ssh)
- https://github.com/punkpeye/awesome-mcp-servers/pull/XXX (mcp-civic-data)

---

## Verification Checklist

- [ ] All 5 PRs created
- [ ] Each PR has proper title format: "Add {repo-name}"
- [ ] Each PR links to ericgrill.com
- [ ] Each PR links to the GitHub repo
- [ ] Entries use correct emoji format
- [ ] Entries are placed in appropriate categories
- [ ] Descriptions are concise but informative

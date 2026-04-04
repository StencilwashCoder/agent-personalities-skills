# MCP Server Setup Action

GitHub Action for automated installation and configuration of Model Context Protocol (MCP) servers for Claude Code.

## Usage

```yaml
name: Setup MCP Servers
on: [push]

jobs:
  setup:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Bitcoin MCP Server
        uses: EricGrill/mcp-setup-action@v1
        with:
          server-name: 'mcp-bitcoin-cli'
          server-source: 'pypi'
      
      - name: Setup Civic Data MCP Server  
        uses: EricGrill/mcp-setup-action@v1
        with:
          server-name: 'mcp-civic-data'
          server-source: 'pypi'
```

## Inputs

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `server-name` | Name of the MCP server | Yes | - |
| `server-source` | Source (npm/pypi/github) | No | `pypi` |
| `claude-config-path` | Claude config path | No | `~/.claude` |

## Supported Sources

- **pypi** - Python packages from PyPI
- **npm** - Node.js packages from npm registry
- **github** - Direct from GitHub repositories

## Examples

### Install from PyPI
```yaml
- uses: EricGrill/mcp-setup-action@v1
  with:
    server-name: 'mcp-bitcoin-cli'
    server-source: 'pypi'
```

### Install from npm
```yaml
- uses: EricGrill/mcp-setup-action@v1
  with:
    server-name: '@anthropic-ai/mcp-server'
    server-source: 'npm'
```

### Install from GitHub
```yaml
- uses: EricGrill/mcp-setup-action@v1
  with:
    server-name: 'EricGrill/mcp-kali-orchestration'
    server-source: 'github'
```

## Outputs

- `server-path` - Installation path
- `config-updated` - Whether Claude config was modified

## License

MIT - See [LICENSE](./LICENSE)

## Author

Eric Grill - [ericgrill.com](https://ericgrill.com)

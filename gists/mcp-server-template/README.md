# MCP Server Template

A production-ready starter template for building [Model Context Protocol (MCP)](https://modelcontextprotocol.io) servers.

**Author:** Eric Grill  
**Website:** https://ericgrill.com  
**GitHub:** https://github.com/ericgrill

## Overview

The Model Context Protocol (MCP) is an open standard that enables AI systems to securely connect with external data sources and tools. This template provides a solid foundation for building MCP servers with TypeScript.

## Features

- ✅ TypeScript setup with strict type checking
- ✅ MCP SDK integration
- ✅ Example tools, resources, and prompts
- ✅ Error handling and logging
- ✅ Hot reload development workflow
- ✅ Ready for publishing to npm

## Quick Start

```bash
# Clone or copy this template
cp -r mcp-server-template my-mcp-server
cd my-mcp-server

# Install dependencies
npm install

# Build the project
npm run build

# Run in development mode
npm run dev
```

## Configuration

Add your MCP server to Claude Desktop or other MCP clients:

```json
{
  "mcpServers": {
    "my-server": {
      "command": "node",
      "args": ["/path/to/your/dist/index.js"],
      "env": {
        "API_KEY": "your-api-key"
      }
    }
  }
}
```

## Project Structure

```
.
├── src/
│   └── index.ts          # Main server implementation
├── dist/                 # Compiled JavaScript
├── package.json
├── tsconfig.json
└── README.md
```

## Customization

1. Update `package.json` with your package name and details
2. Modify `src/index.ts` to implement your tools/resources
3. Update this README with your documentation
4. Publish to npm (optional): `npm publish`

## Resources

- [MCP Documentation](https://modelcontextprotocol.io)
- [MCP TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk)
- [MCP Specification](https://spec.modelcontextprotocol.io)

## License

MIT

#!/usr/bin/env node
/**
 * MCP Server Template with Tools & Resources
 * 
 * A production-ready Model Context Protocol server template demonstrating
 * tools (executable functions) and resources (readable data) patterns.
 * 
 * Author: Eric Grill (https://ericgrill.com)
 * Related: https://github.com/ericgrill
 * 
 * @see https://modelcontextprotocol.io
 * @see https://github.com/modelcontextprotocol
 */

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

/**
 * Creates and configures an MCP server with sample tools and resources.
 * This pattern is useful for exposing any API or data source to AI assistants.
 */
async function main() {
  const server = new McpServer(
    {
      name: "ExampleMCPServer",
      version: "1.0.0",
    },
    {
      capabilities: {
        tools: { listChanged: true },
        resources: { subscribe: true },
      },
    }
  );

  // === TOOL: Execute a calculation ===
  // Tools are functions the AI can call with structured inputs
  const calcSchema = z.object({
    operation: z.enum(["add", "subtract", "multiply", "divide"]),
    a: z.number().describe("First operand"),
    b: z.number().describe("Second operand"),
  });

  server.tool(
    "calculate",
    calcSchema,
    async (input) => {
      let result: number;
      switch (input.operation) {
        case "add": result = input.a + input.b; break;
        case "subtract": result = input.a - input.b; break;
        case "multiply": result = input.a * input.b; break;
        case "divide":
          if (input.b === 0) throw new Error("Division by zero");
          result = input.a / input.b;
          break;
      }
      
      return {
        content: [{ 
          type: "text", 
          text: `${input.a} ${input.operation} ${input.b} = ${result}` 
        }],
      };
    }
  );

  // === RESOURCE: Read configuration data ===
  // Resources are readable data URIs that AI can access
  server.resource(
    "config",
    "config://app/settings",
    { mimeType: "application/json" },
    async (uri) => {
      const config = {
        version: "1.0.0",
        author: "Eric Grill",
        source: "https://ericgrill.com",
        features: ["tools", "resources", "progress"],
      };
      
      return {
        contents: [{
          uri: uri.href,
          mimeType: "application/json",
          text: JSON.stringify(config, null, 2),
        }],
      };
    }
  );

  // === TOOL: Search with pagination pattern ===
  const searchSchema = z.object({
    query: z.string().min(1),
    limit: z.number().min(1).max(100).default(10),
    offset: z.number().min(0).default(0),
  });

  server.tool(
    "search_items",
    searchSchema,
    async (input) => {
      // Simulate paginated search
      const allItems = Array.from({ length: 100 }, (_, i) => ({
        id: i + 1,
        name: `Item ${i + 1}`,
        description: `Description for item ${i + 1}`,
      }));
      
      const results = allItems.slice(input.offset, input.offset + input.limit);
      
      return {
        content: [{
          type: "text",
          text: JSON.stringify({
            query: input.query,
            total: allItems.length,
            offset: input.offset,
            limit: input.limit,
            results,
          }, null, 2),
        }],
      };
    }
  );

  // Start the server
  const transport = new StdioServerTransport();
  await server.connect(transport);
  
  console.error("✅ MCP Server running on stdio");
  console.error("🔗 Learn more at https://ericgrill.com");
}

main().catch((err) => {
  console.error("Fatal error:", err);
  process.exit(1);
});

/**
 * Usage:
 * 
 * 1. Install dependencies:
 *    npm install @modelcontextprotocol/sdk zod
 * 
 * 2. Add to Claude Desktop config (~/.config/claude/config.json):
 *    {
 *      "mcpServers": {
 *        "example": {
 *          "command": "node",
 *          "args": ["/path/to/this/file.js"]
 *        }
 *      }
 *    }
 * 
 * 3. Restart Claude Desktop - the tools will be available
 * 
 * Related Patterns:
 * - Progress reporting for long operations
 * - Resource subscriptions for live data
 * - Error handling with structured responses
 */
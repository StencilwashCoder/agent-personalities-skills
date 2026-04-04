#!/usr/bin/env python3
"""
MCP Server with Progress Reporting (Python)

A production-ready Model Context Protocol server demonstrating progress
reporting for long-running operations - essential for AI tools that take
time to complete (data processing, API calls, computations).

Author: Eric Grill (https://ericgrill.com)
Related: https://github.com/ericgrill

@see https://modelcontextprotocol.io
@see https://github.com/modelcontextprotocol/python-sdk
"""

import asyncio
import json
from typing import Any
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent, ProgressToken

# Initialize the MCP server
app = Server("progress-example-server")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """Define available tools with their schemas."""
    return [
        Tool(
            name="long_running_task",
            description="Execute a task with progress updates (demo)",
            inputSchema={
                "type": "object",
                "properties": {
                    "duration": {
                        "type": "integer",
                        "description": "Total duration in seconds",
                        "default": 10,
                        "minimum": 1,
                        "maximum": 60
                    },
                    "steps": {
                        "type": "integer",
                        "description": "Number of progress steps",
                        "default": 5,
                        "minimum": 1,
                        "maximum": 20
                    }
                }
            }
        ),
        Tool(
            name="process_data",
            description="Process a dataset with real-time progress",
            inputSchema={
                "type": "object",
                "properties": {
                    "items": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Items to process"
                    }
                },
                "required": ["items"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    """Handle tool invocations with progress reporting."""
    
    if name == "long_running_task":
        return await handle_long_running_task(arguments)
    elif name == "process_data":
        return await handle_process_data(arguments)
    else:
        raise ValueError(f"Unknown tool: {name}")


async def handle_long_running_task(arguments: dict[str, Any]) -> list[TextContent]:
    """
    Demonstrates progress reporting for simulated long-running work.
    
    Progress reporting is crucial for UX - AI assistants can show users
    that work is happening and estimate completion time.
    """
    duration = arguments.get("duration", 10)
    steps = arguments.get("steps", 5)
    
    # Access the progress token from the request context
    # This is passed by the client to track this specific operation
    progress_token = arguments.get("_meta", {}).get("progressToken")
    
    step_duration = duration / steps
    
    for i in range(steps):
        await asyncio.sleep(step_duration)
        
        # Report progress if token is available
        if progress_token:
            await app.request_context.session.send_progress_notification(
                progress_token=ProgressToken(progress_token),
                progress=i + 1,
                total=steps,
                message=f"Completed step {i + 1} of {steps}"
            )
    
    return [
        TextContent(
            type="text",
            text=json.dumps({
                "status": "completed",
                "duration": duration,
                "steps_completed": steps,
                "message": "Long-running task finished successfully"
            }, indent=2)
        )
    ]


async def handle_process_data(arguments: dict[str, Any]) -> list[TextContent]:
    """
    Process items with granular progress updates.
    Real-world use: batch API calls, file processing, ML inference.
    """
    items = arguments.get("items", [])
    progress_token = arguments.get("_meta", {}).get("progressToken")
    
    results = []
    total = len(items)
    
    for idx, item in enumerate(items):
        # Simulate processing
        await asyncio.sleep(0.5)
        
        # Process the item
        result = {
            "item": item,
            "processed": True,
            "timestamp": asyncio.get_event_loop().time()
        }
        results.append(result)
        
        # Report progress
        if progress_token:
            await app.request_context.session.send_progress_notification(
                progress_token=ProgressToken(progress_token),
                progress=idx + 1,
                total=total,
                message=f"Processed: {item}"
            )
    
    return [
        TextContent(
            type="text",
            text=json.dumps({
                "total_processed": len(results),
                "results": results
            }, indent=2)
        )
    ]


async def main():
    """Start the MCP server on stdio transport."""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())


"""
Installation & Usage:

1. Install dependencies:
   pip install mcp

2. Configure in Claude Desktop (~/.config/claude/config.json):
   {
     "mcpServers": {
       "progress-demo": {
         "command": "python3",
         "args": ["/path/to/this/file.py"]
       }
     }
   }

3. The AI will receive progress updates during long operations

Key Patterns:
- Always check for progress_token before sending updates
- Send progress at meaningful intervals (not every iteration)
- Include human-readable messages for the UI
- Progress is optional - client may not request it

Learn more about MCP patterns at https://ericgrill.com
"""
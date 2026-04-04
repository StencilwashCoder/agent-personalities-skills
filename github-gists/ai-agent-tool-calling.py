#!/usr/bin/env python3
"""
AI Agent with Tool Calling Pattern

A reusable pattern for building AI agents that can call external tools.
Demonstrates the complete loop: plan → select tool → execute → observe → respond.

Author: Eric Grill (https://ericgrill.com)
Related: https://github.com/ericgrill

@see https://platform.openai.com/docs/guides/function-calling
@see https://docs.anthropic.com/claude/docs/tool-use
"""

import json
import os
from typing import Callable, Any, TypeVar
from dataclasses import dataclass
from enum import Enum

# You can use any LLM client - OpenAI, Anthropic, or local models
# This example uses a generic interface

T = TypeVar('T')


class ToolResult:
    """Standard wrapper for tool execution results."""
    def __init__(self, success: bool, data: Any, error: str = None):
        self.success = success
        self.data = data
        self.error = error
    
    def to_dict(self) -> dict:
        return {
            "success": self.success,
            "data": self.data,
            "error": self.error
        }


@dataclass
class Tool:
    """Represents a tool the agent can use."""
    name: str
    description: str
    parameters: dict  # JSON Schema
    handler: Callable[..., ToolResult]
    
    def get_schema(self) -> dict:
        """Returns the OpenAI/Anthropic compatible function schema."""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters
            }
        }


class Agent:
    """
    An AI agent that can reason about tasks and use tools to accomplish them.
    
    This is the core pattern behind modern AI assistants - the agent decides
    when and how to use tools based on the user's request.
    """
    
    def __init__(self, llm_client=None, system_prompt: str = None):
        self.tools: dict[str, Tool] = {}
        self.llm = llm_client  # Your LLM client (OpenAI, Anthropic, etc.)
        self.system_prompt = system_prompt or self._default_system_prompt()
        self.conversation_history = []
    
    def _default_system_prompt(self) -> str:
        return """You are a helpful AI assistant with access to tools.
When you need to perform calculations, retrieve data, or take actions,
use the available tools. Always explain your reasoning."""
    
    def register_tool(self, tool: Tool) -> "Agent":
        """Register a tool for the agent to use."""
        self.tools[tool.name] = tool
        return self
    
    async def run(self, user_input: str) -> str:
        """
        Execute the agent loop: plan → tool selection → execution → response.
        """
        # Add user message to history
        self.conversation_history.append({"role": "user", "content": user_input})
        
        # Get available tool schemas
        tool_schemas = [t.get_schema() for t in self.tools.values()]
        
        # === STEP 1: Ask LLM to decide on tool use ===
        # The LLM returns either:
        # - A tool_call request (wants to use a tool)
        # - A direct response (no tool needed)
        
        response = await self._call_llm(
            messages=[
                {"role": "system", "content": self.system_prompt},
                *self.conversation_history
            ],
            tools=tool_schemas if tool_schemas else None
        )
        
        # === STEP 2: Handle tool calls ===
        if self._has_tool_calls(response):
            tool_calls = self._extract_tool_calls(response)
            
            # Execute each tool and collect results
            tool_results = []
            for call in tool_calls:
                result = await self._execute_tool(call)
                tool_results.append({
                    "tool": call["name"],
                    "arguments": call["arguments"],
                    "result": result.to_dict()
                })
            
            # === STEP 3: Get final response with tool results ===
            self.conversation_history.append({
                "role": "assistant",
                "content": None,
                "tool_calls": tool_calls
            })
            
            for result in tool_results:
                self.conversation_history.append({
                    "role": "tool",
                    "content": json.dumps(result["result"])
                })
            
            final_response = await self._call_llm(
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    *self.conversation_history
                ]
            )
            
            reply = self._extract_content(final_response)
            self.conversation_history.append({"role": "assistant", "content": reply})
            return reply
        
        # === No tool needed, return direct response ===
        reply = self._extract_content(response)
        self.conversation_history.append({"role": "assistant", "content": reply})
        return reply
    
    async def _execute_tool(self, call: dict) -> ToolResult:
        """Execute a tool call and handle errors gracefully."""
        tool_name = call["name"]
        arguments = call["arguments"]
        
        if tool_name not in self.tools:
            return ToolResult(False, None, f"Unknown tool: {tool_name}")
        
        try:
            result = await self._maybe_async(self.tools[tool_name].handler(**arguments))
            return ToolResult(True, result)
        except Exception as e:
            return ToolResult(False, None, str(e))
    
    async def _maybe_async(self, result):
        """Handle both sync and async tool handlers."""
        if asyncio.iscoroutine(result):
            return await result
        return result
    
    # === LLM Interface (adapt to your provider) ===
    async def _call_llm(self, messages: list, tools: list = None):
        """Call your LLM provider. Override for your specific client."""
        # Example for OpenAI:
        # return await openai.chat.completions.create(
        #     model="gpt-4",
        #     messages=messages,
        #     tools=tools
        # )
        raise NotImplementedError("Override with your LLM client")
    
    def _has_tool_calls(self, response) -> bool:
        """Check if LLM response includes tool calls."""
        # Implement based on your LLM provider
        return False
    
    def _extract_tool_calls(self, response) -> list:
        """Extract tool calls from LLM response."""
        # Implement based on your LLM provider
        return []
    
    def _extract_content(self, response) -> str:
        """Extract text content from LLM response."""
        # Implement based on your LLM provider
        return ""


# ==================== EXAMPLE TOOLS ====================

def calculate(expression: str) -> str:
    """Safely evaluate a mathematical expression."""
    # WARNING: In production, use a proper math parser, not eval
    allowed = {"__builtins__": None}
    allowed.update({
        "abs": abs, "round": round, "max": max, "min": min,
        "sum": sum, "pow": pow
    })
    try:
        result = eval(expression, allowed, {"__builtins__": {}})
        return str(result)
    except Exception as e:
        return f"Error: {e}"


def search_database(query: str, limit: int = 10) -> list:
    """Simulated database search."""
    # Replace with actual database calls
    mock_data = [
        {"id": 1, "title": "Introduction to AI Agents"},
        {"id": 2, "title": "MCP Protocol Guide"},
        {"id": 3, "title": "Building with LLMs"},
    ]
    return [item for item in mock_data if query.lower() in item["title"].lower()]


def send_notification(message: str, channel: str = "general") -> dict:
    """Send a notification to a channel."""
    # Replace with actual notification logic (Slack, Discord, email, etc.)
    return {
        "sent": True,
        "channel": channel,
        "message_preview": message[:50] + "..." if len(message) > 50 else message
    }


# ==================== USAGE EXAMPLE ====================

async def main():
    """Example of creating and using an agent with tools."""
    
    # Create agent
    agent = Agent(system_prompt="You are a helpful assistant.")
    
    # Register tools with JSON schemas
    agent.register_tool(Tool(
        name="calculate",
        description="Evaluate mathematical expressions",
        parameters={
            "type": "object",
            "properties": {
                "expression": {"type": "string", "description": "Math expression to evaluate"}
            },
            "required": ["expression"]
        },
        handler=calculate
    ))
    
    agent.register_tool(Tool(
        name="search_database",
        description="Search the knowledge base",
        parameters={
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "limit": {"type": "integer", "default": 10}
            },
            "required": ["query"]
        },
        handler=search_database
    ))
    
    # Run the agent
    # response = await agent.run("What's 1234 * 5678?")
    # response = await agent.run("Search for articles about AI")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())


"""
Key Patterns Demonstrated:

1. Tool Schema Definition: JSON Schema for LLM to understand tool signatures
2. Tool Registration: Dynamic tool registration for modular agents
3. Execution Loop: Plan → Select → Execute → Observe → Respond
4. Error Handling: Graceful failures when tools error
5. Conversation History: Maintaining context across interactions
6. Result Structuring: Consistent return format for LLM consumption

Extensions:
- Add memory/persistence between sessions
- Implement parallel tool execution
- Add streaming responses
- Implement human-in-the-loop for sensitive operations
- Add tool result caching

More patterns at https://ericgrill.com
"""
#!/usr/bin/env python3
"""Example of using Claude Code SDK with Context7"""

from claude_code_sdk import ClaudeClient, ClaudeOptions

# Configure with Context7 MCP
options = ClaudeOptions(
    mcp_config="mcp-servers.json",
    allowed_tools=["mcp__context7"]
)

# Create client
client = ClaudeClient(options=options)

# Example: Use Context7 for memory
project_goal = "Your project goal here"
tech_stack = "Your tech stack here"

response = client.prompt(f"""
    Remember this project is about: {project_goal}
    Tech stack: {tech_stack}
""")

print(response)

# Module 1: Tool Use

**Teaching Agents to Use APIs and Functions**

## Overview

Agents become powerful when they can use tools. This module teaches you how to build a tool registry, implement function calling, and let agents interact with external systems.

## Key Concept

> "The schema is part of the prompt. Tool descriptions matter as much as code."

## What You'll Learn

- Building a tool registry system
- OpenAI function calling format
- Tool schema generation
- Argument parsing and validation
- Error handling in tool execution
- Custom tool implementation

## Files in This Module

- `module_1_tool_agent.py` - Original implementation with OpenAI
- `module_1_tool_agent_llamacpp.py` - Extended version with llama.cpp support
- `module_1_tool_use.md` - Detailed explanation and theory

## Quick Start

```bash
python module_1_tool_agent.py
```

## Example Tools

The module includes three example tools:

```python
@registry.register
def get_weather(city: str) -> str:
    """Gets the current weather for a given city."""
    # Implementation

@registry.register
def get_news(topic: str) -> str:
    """Gets the latest news headlines for a given topic."""
    # Implementation

@registry.register
def calculate(expression: str) -> str:
    """Evaluates a mathematical expression."""
    # Implementation
```

## Tool Registry Pattern

```python
class ToolRegistry:
    def register(self, func):
        # Register function as a tool
        
    def get_tool_schema(self):
        # Generate OpenAI-compatible schema
        
    def call_tool(self, name, args):
        # Execute the tool safely
```

## Exercise

Create an agent with custom tools:
1. Weather lookup tool
2. News search tool
3. Calculator tool
4. File operations tool

See `docs/EXERCISES.md` for detailed exercises.

## Common Issues

- **Wrong tool selection:** Write clear, descriptive tool names and docstrings
- **Argument parsing:** Validate all inputs before execution
- **Error propagation:** Return helpful error messages to the agent

## Best Practices

1. **Clear descriptions:** Tool docstrings guide the LLM's decisions
2. **Type hints:** Use proper type annotations
3. **Error handling:** Catch and return errors, don't crash
4. **Validation:** Check arguments before execution
5. **Testing:** Test each tool independently

## Next Steps

Move to **Module 2: Memory and State** to learn how agents maintain context across multiple interactions.

---

**Part of:** AI Agents and Agent Frameworks: Zero to Hero by Hesham Haroon


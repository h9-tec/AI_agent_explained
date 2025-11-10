# Examples

**Complete, production-ready agent implementations**

## Overview

This directory contains advanced examples that combine concepts from multiple modules. Each example is a complete, working application that demonstrates real-world use cases.

## Available Examples

### advanced_example_full_agent.py

A comprehensive agent system that combines:
- Agent loop (Module 0)
- Tool use (Module 1)
- Memory management (Module 2)
- ReAct reasoning (Module 3)

**Features:**
- Unified tool registry
- Sliding window memory
- Statistics tracking
- Interactive mode
- Error handling

**Usage:**
```bash
python advanced_example_full_agent.py
```

## More Examples

For additional examples, see:
- **[docs/EXAMPLES.md](../docs/EXAMPLES.md)** - Complete code for:
  - Personal Research Assistant
  - Code Review Agent
  - Data Analysis Agent
  - Customer Support Bot
  - Content Generation Pipeline

## Building Your Own

Use these examples as templates for your own agents:

1. **Start with the advanced example** - Understand the complete structure
2. **Modify the tools** - Add your own custom tools
3. **Adjust the system prompt** - Tailor behavior to your use case
4. **Add domain logic** - Implement your specific requirements
5. **Test thoroughly** - Use the debugging techniques from the course

## Example Structure

A complete agent typically includes:

```python
# 1. Tool Registry
registry = ToolRegistry()

@registry.register
def your_tool(arg: str) -> str:
    """Tool description."""
    # Implementation

# 2. Agent Class
class YourAgent:
    def __init__(self):
        self.tools = registry
        self.memory = Memory()
    
    def run(self, query: str) -> str:
        # Agent logic

# 3. Main Execution
if __name__ == "__main__":
    agent = YourAgent()
    result = agent.run("Your query")
```

## Best Practices

1. **Modular design:** Separate tools, memory, and agent logic
2. **Error handling:** Catch and handle all exceptions
3. **Logging:** Add comprehensive logging
4. **Testing:** Test each component independently
5. **Documentation:** Document your tools and agent behavior

## Contributing

Have a great example? Consider contributing:
1. Ensure it's complete and working
2. Add clear documentation
3. Include usage examples
4. Test with both OpenAI and llama.cpp (if applicable)

---

**Part of:** AI Agents and Agent Frameworks: Zero to Hero by Hesham Haroon


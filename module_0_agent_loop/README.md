# Module 0: The Agent Loop

**The Foundation: Understanding the Basic Agent Architecture**

## Overview

This module introduces the most fundamental concept in AI agents: the Think-Act-Observe cycle. We build the simplest possible agent—a 50-line loop—to understand how agents work at their core.

## Key Concept

> "An agent is just a while loop with an LLM inside it."

## What You'll Learn

- The basic agent loop architecture
- How agents interact with LLMs
- Code execution and observation
- Iteration and termination conditions
- Error handling in agent loops

## Files in This Module

- `module_0_agent.py` - Original implementation using OpenAI
- `module_0_agent_llamacpp.py` - Extended version supporting both OpenAI and llama.cpp
- `module_0_agent_loop.md` - Detailed explanation and theory

## Quick Start

### Using OpenAI:
```bash
export OPENAI_API_KEY="your-key-here"
python module_0_agent.py
```

### Using llama.cpp:
```bash
# Configure .env file first
python module_0_agent_llamacpp.py
```

## The Agent Loop

```python
while not done:
    # 1. THINK: LLM decides what to do
    response = llm(messages)
    
    # 2. ACT: Execute the action
    if has_code(response):
        result = execute(code)
        
        # 3. OBSERVE: Get the result
        messages.append(result)
    else:
        done = True
```

## Exercise

Build a calculator agent that can:
1. Solve multi-step math problems
2. Show its reasoning
3. Handle errors gracefully

See `docs/EXERCISES.md` for detailed exercises.

## Common Issues

- **Infinite loops:** Always set `max_iterations`
- **Silent failures:** Add comprehensive logging
- **Security:** Never use `eval()` with untrusted input

## Next Steps

Once you understand the basic loop, move to **Module 1: Tool Use** to learn how agents can use external tools and APIs.

---

**Part of:** AI Agents and Agent Frameworks: Zero to Hero by Hesham Haroon


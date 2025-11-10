# Module 3: Planning and Reasoning

**The ReAct Pattern: Reason + Act**

## Overview

This module implements the ReAct (Reasoning and Acting) pattern, where agents explicitly reason about their actions before taking them. This enables multi-step problem solving and complex reasoning.

## Key Concept

> "ReAct is powerful but not magic. It fails in predictable ways."

## What You'll Learn

- ReAct pattern implementation
- Reasoning trace generation
- Action parsing and execution
- Multi-step problem solving
- Debugging reasoning failures
- Convergence criteria

## Files in This Module

- `module_3_react_agent.py` - Original implementation with OpenAI
- `module_3_react_agent_llamacpp.py` - Extended version with llama.cpp support
- `module_3_planning_reasoning.md` - Detailed explanation and theory

## Quick Start

```bash
python module_3_react_agent.py
```

## The ReAct Format

```
Thought: [Reasoning about what to do next]
Action: tool_name(arg1="value1", arg2="value2")
Observation: [Result from the system]

... repeat as needed ...

Thought: I now have enough information
Final Answer: [The answer to the original question]
```

## ReAct Agent

```python
class ReActAgent:
    def __init__(self, tools: dict, max_iterations: int = 10):
        self.tools = tools
        self.max_iterations = max_iterations
    
    def run(self, question: str) -> str:
        # Execute ReAct loop
        # Parse thoughts and actions
        # Execute tools
        # Return final answer
```

## Example Questions

The module includes three example questions that require multi-step reasoning:

1. "What was the most popular programming language in the year the first iPhone was released?"
   - Search for iPhone release year → 2007
   - Search for popular language in 2007 → Java

2. "Who was the CEO of OpenAI when GPT-3 was released?"
   - Search for GPT-3 release → June 2020
   - Search for OpenAI CEO in 2020 → Sam Altman

3. "How many years ago was the first iPhone released?"
   - Get current year → 2024
   - Search for iPhone release → 2007
   - Calculate difference → 17 years

## Exercise

Build a research agent that can:
1. Break down complex questions
2. Search for information step by step
3. Perform calculations
4. Synthesize final answers

See `docs/EXERCISES.md` for detailed exercises.

## Common Failure Modes

1. **Infinite loops:** Agent repeats same actions
2. **Wrong tool selection:** Uses inappropriate tools
3. **Hallucinated tools:** Tries to use non-existent tools
4. **Premature termination:** Stops before finding answer
5. **No final answer:** Keeps searching indefinitely

## Debugging ReAct

- Print reasoning traces
- Visualize thought → action → observation
- Check for repeated patterns
- Verify tool availability
- Set max iterations

## Best Practices

1. **Clear system prompt:** Explain the format precisely
2. **Good tool descriptions:** Help agent choose correctly
3. **Max iterations:** Prevent infinite loops
4. **Deterministic output:** Use temperature=0 for debugging
5. **Reasoning traces:** Log everything for analysis

## Next Steps

Move to **Module 4: Multi-Agent Systems** to learn how to orchestrate multiple specialized agents working together.

---

**Part of:** AI Agents and Agent Frameworks: Zero to Hero by Hesham Haroon


# Module 2: Memory and State

**Making Agents Stateful and Context-Aware**

## Overview

Agents need memory to maintain context across conversations. This module teaches you how to implement memory systems, sliding windows, and stateful agents.

## Key Concept

> "Memory is a leaky abstraction. You must understand what gets remembered and what gets forgotten."

## What You'll Learn

- Conversation history management
- Sliding window implementation
- Context window optimization
- Stateful agent design
- Memory clearing and reset
- Token counting and limits

## Files in This Module

- `module_2_memory_agent.py` - Original implementation with OpenAI
- `module_2_memory_agent_llamacpp.py` - Extended version with llama.cpp support
- `module_2_memory_state.md` - Detailed explanation and theory

## Quick Start

```bash
python module_2_memory_agent.py
```

## Memory System

```python
class Memory:
    def __init__(self, window_size: int = 10):
        self.messages = []
        self.window_size = window_size
    
    def add_message(self, role: str, content: str):
        # Add to history
        
    def get_messages(self):
        # Return windowed messages
        # Always include system prompt
```

## Stateful Agent

```python
class StatefulAgent:
    def __init__(self, system_prompt: str, window_size: int = 10):
        self.memory = Memory(window_size, system_prompt)
    
    def chat(self, user_message: str) -> str:
        # Maintain conversation context
        
    def reset(self):
        # Clear memory, keep system prompt
```

## Example: Customer Service Bot

The module includes a complete customer service demo that:
- Remembers customer information
- Maintains conversation context
- Handles multiple turns
- Can reset conversation

## Exercise

Build a customer service agent that:
1. Remembers user's name and order number
2. Maintains context across 10+ messages
3. Can summarize the conversation
4. Handles memory overflow gracefully

See `docs/EXERCISES.md` for detailed exercises.

## Common Issues

- **Context overflow:** Messages exceed token limit
- **Lost information:** Important data outside window
- **System prompt loss:** Always preserve system message
- **Memory leaks:** Unbounded growth of history

## Memory Strategies

1. **Sliding Window:** Keep last N messages (simple, fast)
2. **Summarization:** Compress old messages (complex, slower)
3. **Hybrid:** Window + summaries (best of both)
4. **Vector Store:** Semantic search (for large contexts)

## Best Practices

- Set appropriate window size (5-20 messages)
- Always include system prompt
- Monitor token usage
- Implement reset functionality
- Test memory boundaries

## Next Steps

Move to **Module 3: Planning and Reasoning** to learn how agents can reason through multi-step problems using the ReAct pattern.

---

**Part of:** AI Agents and Agent Frameworks: Zero to Hero by Hesham Haroon


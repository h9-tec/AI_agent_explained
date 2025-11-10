# Debugging AI Agents: A Practical Guide

**The Problem:** Agents fail silently. No stack trace. No error message. Just... wrong output.

**The Solution:** Systematic debugging with visualization and logging.

**By Hesham Haroon**

---

## The Systematic Debugging Method

1. **Understand what should happen** - Write down expected behavior
2. **Observe what actually happens** - Print everything
3. **Find the divergence** - Where does it go wrong?
4. **Form a hypothesis** - Why did it go wrong?
5. **Test the hypothesis** - Add a fix, verify it works
6. **Repeat** - Until it works on all test cases

---

## Common Agent Failure Modes

### 1. Silent Failures

**Symptom:** Agent stops responding or returns empty output.

**Causes:**
- API key issues
- Rate limiting
- Network errors
- Invalid message format

**Debug:**
```python
def debug_llm_call(messages):
    print(f"[DEBUG] Calling LLM with {len(messages)} messages")
    print(f"[DEBUG] Last message: {messages[-1]}")
    
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages
        )
        print(f"[DEBUG] Response received: {len(response.choices[0].message.content)} chars")
        return response
    except Exception as e:
        print(f"[ERROR] LLM call failed: {e}")
        raise
```

### 2. Infinite Loops

**Symptom:** Agent never finishes, keeps calling tools forever.

**Causes:**
- No termination condition
- LLM doesn't recognize completion
- Tool outputs trigger more tool calls

**Debug:**
```python
def debug_agent_loop(prompt, max_iterations=10):
    messages = [{"role": "user", "content": prompt}]
    
    for i in range(max_iterations):
        print(f"\n{'='*60}")
        print(f"ITERATION {i+1}/{max_iterations}")
        print(f"{'='*60}")
        
        response = get_llm_response(messages)
        print(f"LLM Response:\n{response}\n")
        
        # Check for completion
        if "final answer" in response.lower():
            print("[DEBUG] Found final answer, stopping")
            return response
        
        # Parse tool calls
        tool_call = parse_tool_call(response)
        if tool_call:
            print(f"[DEBUG] Tool call: {tool_call}")
            result = execute_tool(tool_call)
            print(f"[DEBUG] Tool result: {result}")
            messages.append({"role": "user", "content": f"Result: {result}"})
        else:
            print("[WARNING] No tool call and no final answer!")
            break
    
    print("[ERROR] Max iterations reached!")
    return "Failed to complete"
```

### 3. Wrong Tool Selection

**Symptom:** Agent uses the wrong tool for the task.

**Causes:**
- Unclear tool descriptions
- Similar tool names
- LLM confusion

**Debug:**
```python
def debug_tool_selection(agent_response, available_tools):
    print("\n[DEBUG] Tool Selection Analysis")
    print(f"Agent wants to use: {parse_tool_name(agent_response)}")
    print(f"\nAvailable tools:")
    for name, tool in available_tools.items():
        print(f"  - {name}: {tool.__doc__}")
    
    # Check if tool exists
    requested_tool = parse_tool_name(agent_response)
    if requested_tool not in available_tools:
        print(f"\n[ERROR] Tool '{requested_tool}' not found!")
        print(f"Did you mean one of these?")
        for name in available_tools.keys():
            if similar(name, requested_tool):
                print(f"  - {name}")
```

### 4. Memory Issues

**Symptom:** Agent forgets important information.

**Causes:**
- Sliding window too small
- Important info outside window
- No summarization

**Debug:**
```python
def debug_memory(memory):
    print("\n[DEBUG] Memory Analysis")
    print(f"Total messages: {len(memory.get_full_history())}")
    print(f"Window size: {memory.window_size}")
    print(f"Messages in window: {len(memory.get_window())}")
    
    print("\n[DEBUG] Current window:")
    for i, msg in enumerate(memory.get_window()):
        role = msg['role']
        content = msg['content'][:50] + "..." if len(msg['content']) > 50 else msg['content']
        print(f"  {i+1}. [{role}] {content}")
    
    print("\n[DEBUG] Dropped messages:")
    full = memory.get_full_history()
    window = memory.get_window()
    dropped = [m for m in full if m not in window]
    print(f"  {len(dropped)} messages dropped")
    if dropped:
        print(f"  First dropped: {dropped[0]['content'][:50]}...")
```

### 5. Hallucinated Information

**Symptom:** Agent makes up facts or tool results.

**Causes:**
- No grounding in real data
- LLM fills in gaps
- Unclear instructions

**Debug:**
```python
def verify_facts(agent_response, ground_truth):
    print("\n[DEBUG] Fact Verification")
    
    # Extract claims from response
    claims = extract_claims(agent_response)
    
    for claim in claims:
        print(f"\nClaim: {claim}")
        
        # Check against ground truth
        if claim in ground_truth:
            print("  ✓ Verified")
        else:
            print("  ✗ Cannot verify - possible hallucination")
            print(f"  Source: {find_source(claim)}")
```

---

## Visualization Techniques

### 1. Reasoning Trace Visualization

```python
def visualize_reasoning_trace(agent_run):
    """
    Shows the agent's thought process step by step.
    """
    print("\n" + "="*80)
    print("REASONING TRACE")
    print("="*80)
    
    for i, step in enumerate(agent_run.steps, 1):
        print(f"\n[Step {i}]")
        print(f"Thought: {step.thought}")
        
        if step.action:
            print(f"Action: {step.action.tool}({step.action.args})")
            print(f"Result: {step.observation}")
        
        if step.is_final:
            print(f"Final Answer: {step.final_answer}")

# Example output:
# [Step 1]
# Thought: I need to find the capital of France
# Action: search(query="capital of France")
# Result: Paris
#
# [Step 2]
# Thought: Now I have the answer
# Final Answer: The capital of France is Paris
```

### 2. Message Flow Diagram

```python
def visualize_message_flow(messages):
    """
    Shows how messages flow through the conversation.
    """
    print("\n" + "="*80)
    print("MESSAGE FLOW")
    print("="*80)
    
    for i, msg in enumerate(messages):
        role = msg['role']
        content = msg['content'][:60] + "..." if len(msg['content']) > 60 else msg['content']
        
        if role == "system":
            print(f"\n[SYSTEM] {content}")
        elif role == "user":
            print(f"\n  USER → {content}")
        elif role == "assistant":
            print(f"\n    ASSISTANT → {content}")
        elif role == "tool":
            print(f"\n      TOOL → {content}")
```

### 3. Tool Call Graph

```python
def visualize_tool_calls(agent_run):
    """
    Shows which tools were called and in what order.
    """
    print("\n" + "="*80)
    print("TOOL CALL GRAPH")
    print("="*80)
    
    tools_used = {}
    for step in agent_run.steps:
        if step.action:
            tool = step.action.tool
            tools_used[tool] = tools_used.get(tool, 0) + 1
    
    print("\nTools used:")
    for tool, count in tools_used.items():
        bar = "█" * count
        print(f"  {tool:20} {bar} ({count})")
    
    print("\nCall sequence:")
    for i, step in enumerate(agent_run.steps, 1):
        if step.action:
            print(f"  {i}. {step.action.tool}")
```

### 4. Memory Window Visualization

```python
def visualize_memory_window(memory):
    """
    Shows what's in the memory window vs. what's been dropped.
    """
    print("\n" + "="*80)
    print("MEMORY WINDOW")
    print("="*80)
    
    full = memory.get_full_history()
    window = memory.get_window()
    
    print(f"\nTotal messages: {len(full)}")
    print(f"Window size: {memory.window_size}")
    print(f"In window: {len(window)}")
    print(f"Dropped: {len(full) - len(window)}")
    
    print("\n[In Window]")
    for msg in window:
        role = msg['role']
        preview = msg['content'][:40] + "..." if len(msg['content']) > 40 else msg['content']
        print(f"  ✓ [{role}] {preview}")
    
    dropped = [m for m in full if m not in window]
    if dropped:
        print("\n[Dropped]")
        for msg in dropped[:3]:  # Show first 3
            role = msg['role']
            preview = msg['content'][:40] + "..." if len(msg['content']) > 40 else msg['content']
            print(f"  ✗ [{role}] {preview}")
        if len(dropped) > 3:
            print(f"  ... and {len(dropped) - 3} more")
```

---

## Logging Best Practices

### 1. Structured Logging

```python
import logging
import json
from datetime import datetime

# Setup
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('agent.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Usage
def agent_with_logging(prompt):
    logger.info(f"Agent started with prompt: {prompt}")
    
    try:
        response = llm_call(prompt)
        logger.debug(f"LLM response: {response[:100]}...")
        
        if tool_call_detected(response):
            tool_name, args = parse_tool_call(response)
            logger.info(f"Calling tool: {tool_name} with args {args}")
            
            result = execute_tool(tool_name, args)
            logger.info(f"Tool result: {result}")
        
        logger.info("Agent completed successfully")
        return response
        
    except Exception as e:
        logger.error(f"Agent failed: {e}", exc_info=True)
        raise
```

### 2. Performance Logging

```python
import time

class PerformanceLogger:
    def __init__(self):
        self.timings = {}
    
    def log_time(self, operation):
        def decorator(func):
            def wrapper(*args, **kwargs):
                start = time.time()
                result = func(*args, **kwargs)
                elapsed = time.time() - start
                
                if operation not in self.timings:
                    self.timings[operation] = []
                self.timings[operation].append(elapsed)
                
                logger.debug(f"{operation}: {elapsed:.3f}s")
                return result
            return wrapper
        return decorator
    
    def print_summary(self):
        print("\n" + "="*80)
        print("PERFORMANCE SUMMARY")
        print("="*80)
        
        for op, times in self.timings.items():
            avg = sum(times) / len(times)
            total = sum(times)
            print(f"{op:30} Avg: {avg:.3f}s  Total: {total:.3f}s  Calls: {len(times)}")

# Usage
perf = PerformanceLogger()

@perf.log_time("llm_call")
def call_llm(messages):
    return client.chat.completions.create(messages=messages)

@perf.log_time("tool_execution")
def execute_tool(name, args):
    return tools[name](**args)
```

---

## Testing Strategies

### 1. Unit Tests for Components

```python
import pytest

def test_tool_registry():
    registry = ToolRegistry()
    
    @registry.register
    def add(a: int, b: int) -> int:
        """Adds two numbers."""
        return a + b
    
    # Test registration
    assert "add" in registry.tools
    
    # Test schema generation
    schema = registry.get_tool_schema()
    assert len(schema) == 1
    assert schema[0]["function"]["name"] == "add"
    
    # Test execution
    result = registry.call_tool("add", {"a": 2, "b": 3})
    assert result == "5"

def test_memory_window():
    memory = Memory(window_size=3)
    
    # Add messages
    for i in range(5):
        memory.add_message("user", f"Message {i}")
    
    # Check window size
    window = memory.get_messages()
    assert len(window) <= 3
    
    # Check recent messages are kept
    assert "Message 4" in window[-1]["content"]
```

### 2. Integration Tests

```python
def test_agent_with_tools():
    # Setup
    agent = ToolAgent(tools={"search": mock_search})
    
    # Test
    result = agent.run("What is Python?")
    
    # Verify
    assert "programming language" in result.lower()
    assert agent.tool_calls > 0  # Tool was used

def test_agent_memory():
    agent = StatefulAgent("You are helpful.", window_size=5)
    
    # First interaction
    agent.chat("My name is Alice")
    
    # Second interaction
    response = agent.chat("What's my name?")
    
    # Verify memory
    assert "alice" in response.lower()
```

### 3. End-to-End Tests

```python
def test_research_agent_e2e():
    """
    Test the complete research agent workflow.
    """
    agent = ResearchAgent()
    
    # Complex multi-step query
    result = agent.research(
        "What was the most popular programming language "
        "in the year the first iPhone was released?"
    )
    
    # Verify reasoning steps
    assert agent.steps_taken >= 3  # Should take multiple steps
    assert "search" in [s.tool for s in agent.steps]  # Used search
    assert "2007" in result  # Found the year
    assert "java" in result.lower()  # Found the language
```

---

## Debugging Checklist

When your agent fails, check:

- [ ] **API Key:** Is it set and valid?
- [ ] **Model:** Is the model name correct?
- [ ] **Messages:** Are messages in the right format?
- [ ] **Tools:** Are tool schemas correct?
- [ ] **Memory:** Is the window size appropriate?
- [ ] **Termination:** Does the agent have a stop condition?
- [ ] **Error Handling:** Are exceptions caught and logged?
- [ ] **Rate Limits:** Are you hitting API limits?
- [ ] **Context Length:** Are you exceeding token limits?
- [ ] **Tool Outputs:** Are tool results in the right format?

---

## Advanced Debugging Techniques

### 1. Replay Failed Runs

```python
def save_agent_run(agent_run, filename):
    """Save agent run for later replay."""
    with open(filename, 'w') as f:
        json.dump({
            'prompt': agent_run.prompt,
            'messages': agent_run.messages,
            'steps': agent_run.steps,
            'result': agent_run.result
        }, f, indent=2)

def replay_agent_run(filename):
    """Replay a saved agent run for debugging."""
    with open(filename) as f:
        data = json.load(f)
    
    print("Replaying agent run...")
    visualize_reasoning_trace(data)
```

### 2. Diff Tool Outputs

```python
def compare_tool_outputs(expected, actual):
    """Compare expected vs actual tool outputs."""
    print("\n[DEBUG] Tool Output Comparison")
    print(f"Expected: {expected}")
    print(f"Actual:   {actual}")
    
    if expected == actual:
        print("✓ Match")
    else:
        print("✗ Mismatch")
        # Show diff
        import difflib
        diff = difflib.unified_diff(
            expected.splitlines(),
            actual.splitlines(),
            lineterm=''
        )
        print('\n'.join(diff))
```

### 3. A/B Test Prompts

```python
def ab_test_prompts(prompt_a, prompt_b, test_cases):
    """Compare two prompts on the same test cases."""
    results_a = []
    results_b = []
    
    for test in test_cases:
        result_a = agent.run(test, system_prompt=prompt_a)
        result_b = agent.run(test, system_prompt=prompt_b)
        
        results_a.append(result_a)
        results_b.append(result_b)
    
    # Compare
    print("\n[DEBUG] A/B Test Results")
    print(f"Prompt A success rate: {success_rate(results_a)}")
    print(f"Prompt B success rate: {success_rate(results_b)}")
```

---

## Remember

1. **Print everything** - You can't debug what you can't see
2. **Start simple** - Minimal test case that reproduces the bug
3. **One change at a time** - Change one thing, test, repeat
4. **Read the logs** - The answer is usually in the logs
5. **Understand, don't guess** - Form hypotheses, test them
6. **Document failures** - Save failed runs for later analysis

**The goal:** Understand exactly what the agent is doing at every step.

Happy debugging! 🐛🔍


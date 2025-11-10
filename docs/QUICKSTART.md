# Quick Start Guide

**Get up and running with the AI Agents course in 5 minutes**

---

## Prerequisites

- Python 3.8 or higher
- OpenAI API key
- Basic Python knowledge

---

## Setup (2 minutes)

### 1. Install Dependencies

```bash
pip install openai
```

That's it! We keep dependencies minimal.

### 2. Set Your API Key

**Option A: Environment Variable (Recommended)**

```bash
export OPENAI_API_KEY="your-api-key-here"
```

**Option B: In Code (Not recommended for production)**

```python
import os
os.environ["OPENAI_API_KEY"] = "your-api-key-here"
```

### 3. Verify Setup

```bash
python -c "import openai; print('Setup complete!')"
```

---

## Your First Agent (3 minutes)

### Run the Simplest Agent

```bash
python module_0_agent.py
```

This runs a 50-line agent that can solve multi-step math problems. Watch it think, act, and observe!

**Expected Output:**
```
--- Iteration 1 ---
Thinking...
Assistant: Okay, let's break this down...
```

### Try the Tool-Using Agent

```bash
python module_1_tool_agent.py
```

This agent can use multiple tools (weather, news, calculator) to answer questions.

### Experience Memory

```bash
python module_2_memory_agent.py
```

This starts an interactive customer service agent that remembers your conversation.

### See ReAct in Action

```bash
python module_3_react_agent.py
```

Watch an agent reason step-by-step through complex questions.

---

## Understanding the Code

### The Basic Agent Loop

Every agent follows this pattern:

```python
for iteration in range(max_iterations):
    # 1. THINK: LLM decides what to do
    response = llm.call(messages)
    
    # 2. ACT: Execute any tool calls
    if response.has_tool_calls():
        results = execute_tools(response.tool_calls)
        
        # 3. OBSERVE: Add results to context
        messages.append(results)
    else:
        # Done!
        return response.content
```

That's it. Everything else is elaboration on this fundamental loop.

---

## Course Structure

Follow the modules in order:

| Module | File | Concept | Time |
|--------|------|---------|------|
| 0 | `module_0_*` | Agent loop basics | 30 min |
| 1 | `module_1_*` | Tool use | 45 min |
| 2 | `module_2_*` | Memory & state | 30 min |
| 3 | `module_3_*` | ReAct pattern | 45 min |

Each module has:
- `.md` file: Concepts and explanations
- `.py` file: Working code implementation

---

## Common Issues

### "Module 'openai' not found"

```bash
pip install --upgrade openai
```

### "API key not found"

Make sure you've set the environment variable:

```bash
echo $OPENAI_API_KEY  # Should print your key
```

### "Rate limit exceeded"

You're making too many requests. Wait a minute and try again, or add delays:

```python
import time
time.sleep(1)  # Wait 1 second between calls
```

### Code doesn't run

Make sure you're using Python 3.8+:

```bash
python --version  # Should be 3.8 or higher
```

---

## Next Steps

### 1. Read the Concepts

Open `module_0_agent_loop.md` and read the explanations. Understanding the "why" is as important as the "how."

### 2. Modify the Code

Don't just run it - change it! Try:
- Adding new tools
- Changing the prompts
- Breaking things (seriously!)
- Fixing what you broke

### 3. Complete the Projects

Each module has a project. These are where the real learning happens.

### 4. Read the Full Course

Once you've completed the first 3 modules, read `COURSE_SUMMARY.md` for the complete picture.

---

## Tips for Success

### 1. Be Patient

This is Karpathy-style learning. We build from scratch. It takes time. Don't rush.

### 2. Visualize Everything

Print statements are your friend. See what the agent is thinking at each step.

```python
print(f"Messages: {messages}")
print(f"Response: {response}")
print(f"Tool calls: {tool_calls}")
```

### 3. Start Simple

Don't try to build a complex multi-agent system on day 1. Master the basics first.

### 4. Debug Systematically

When something goes wrong:
1. Read the error message
2. Check the reasoning trace
3. Verify your assumptions
4. Add more logging
5. Simplify until it works

### 5. Experiment

The code is yours to modify. Try things. Break things. Learn from failures.

---

## Example Session

Here's what a typical learning session looks like:

```bash
# 1. Read the module
$ cat module_0_agent_loop.md

# 2. Run the code
$ python module_0_agent.py

# 3. Modify and experiment
$ nano module_0_agent.py  # or your favorite editor

# 4. Run again to see changes
$ python module_0_agent.py

# 5. Complete the project
$ nano my_calculator_agent.py
$ python my_calculator_agent.py
```

---

## Getting Help

### Check the Documentation

- `README.md`: Full course overview
- `COURSE_SUMMARY.md`: Complete concept reference
- Module `.md` files: Detailed explanations

### Debug with Prints

Add print statements everywhere:

```python
print(f"[DEBUG] Current state: {state}")
print(f"[DEBUG] About to call: {tool_name}")
print(f"[DEBUG] Result: {result}")
```

### Simplify

If something doesn't work, simplify:
- Remove tools
- Reduce max_iterations
- Use simpler prompts
- Test with easier questions

---

## Advanced Example

Once you're comfortable with the basics, try the advanced example:

```bash
python advanced_example_full_agent.py
```

This combines all concepts (tools, memory, ReAct) into one complete system.

---

## What You'll Learn

By the end of the first 3 modules, you'll be able to:

✅ Build an agent from scratch (no frameworks)  
✅ Give agents tools to interact with the world  
✅ Implement memory for multi-turn conversations  
✅ Use the ReAct pattern for reasoning  
✅ Debug agent failures systematically  

---

## Ready to Start?

1. Make sure your API key is set
2. Run `python module_0_agent.py`
3. Read `module_0_agent_loop.md`
4. Modify the code
5. Complete the project

**Remember:** Patience and attention to detail are the most important qualities for success.

Now go build something amazing! 🚀

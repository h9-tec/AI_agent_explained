# Hands-On Exercises: Build, Break, Fix

**The Philosophy:** You learn by doing. These exercises follow the proven method: start simple, break things, understand why they broke, fix them.

**By Hesham Haroon**

---

## Module 0: The Agent Loop

### Exercise 0.1: The Simplest Possible Agent

**Goal:** Understand the basic loop.

```python
# Your task: Complete this agent (10 lines)
def simple_agent(prompt: str) -> str:
    messages = [{"role": "user", "content": prompt}]
    
    # TODO: Add the loop
    # TODO: Call the LLM
    # TODO: Return the response
    
    pass

# Test it
print(simple_agent("What is 2+2?"))
```

**Success criteria:** Agent responds to simple questions.

**Common mistakes:**
- Forgetting to add messages to history
- Not handling the response format
- Infinite loops (add max_iterations!)

### Exercise 0.2: Break It

**Goal:** Understand failure modes.

Try these inputs and observe what happens:
```python
simple_agent("")  # Empty input
simple_agent("a" * 10000)  # Very long input
simple_agent("Keep saying 'hello' forever")  # Infinite loop
```

**Questions to answer:**
1. What happens with each input?
2. Why does it fail?
3. How would you fix it?

### Exercise 0.3: Add Code Execution

**Goal:** Build Module 0's calculator agent yourself.

```python
def calculator_agent(prompt: str) -> str:
    # TODO: Detect code blocks in response
    # TODO: Execute the code
    # TODO: Feed result back to agent
    # TODO: Repeat until done
    pass

# Test
calculator_agent("What is (123 * 456) + 789?")
```

**Hints:**
- Use regex to find code blocks: `r"```python\n(.*?)\n```"`
- Use `eval()` to execute (but understand the security risk!)
- Add the result back as a user message

---

## Module 1: Tool Use

### Exercise 1.1: Build a Tool Registry

**Goal:** Understand how tools work.

```python
class SimpleToolRegistry:
    def __init__(self):
        self.tools = {}
    
    def register(self, func):
        # TODO: Store the function
        # TODO: Extract its name and docstring
        # TODO: Return the function (for decorator use)
        pass
    
    def get_schema(self):
        # TODO: Generate OpenAI-compatible schema
        pass
    
    def call(self, name: str, args: dict):
        # TODO: Call the tool with args
        # TODO: Handle errors
        pass

# Test it
registry = SimpleToolRegistry()

@registry.register
def add(a: int, b: int) -> int:
    """Adds two numbers."""
    return a + b

print(registry.get_schema())
print(registry.call("add", {"a": 5, "b": 3}))
```

### Exercise 1.2: Add Your Own Tools

**Goal:** Practice tool design.

Create these tools:
```python
@registry.register
def get_time() -> str:
    """Returns the current time."""
    # TODO: Implement

@registry.register
def search_wikipedia(query: str) -> str:
    """Searches Wikipedia for a query."""
    # TODO: Implement (mock is fine)

@registry.register
def save_to_file(filename: str, content: str) -> str:
    """Saves content to a file."""
    # TODO: Implement
```

**Test:** Build an agent that uses all three tools.

### Exercise 1.3: Debug Tool Calling

**Goal:** Understand why tools fail.

Given this broken tool:
```python
@registry.register
def divide(a: int, b: int) -> float:
    """Divides a by b."""
    return a / b
```

**Tasks:**
1. What happens when `b=0`?
2. Fix it with proper error handling
3. Test with an agent: "What is 10 divided by 0?"
4. Observe how the agent handles the error

---

## Module 2: Memory and State

### Exercise 2.1: Build a Memory System

**Goal:** Understand sliding windows.

```python
class Memory:
    def __init__(self, window_size: int = 5):
        self.messages = []
        self.window_size = window_size
    
    def add(self, role: str, content: str):
        # TODO: Add message to history
        pass
    
    def get_window(self):
        # TODO: Return last N messages
        # TODO: Always include system message if present
        pass
    
    def get_stats(self):
        # TODO: Return useful statistics
        # - Total messages
        # - Messages in window
        # - Estimated tokens
        pass

# Test it
memory = Memory(window_size=3)
for i in range(10):
    memory.add("user", f"Message {i}")
    print(f"Window size: {len(memory.get_window())}")
```

### Exercise 2.2: Memory Experiments

**Goal:** Understand memory limits.

```python
# Experiment 1: What gets forgotten?
agent = StatefulAgent("You are helpful.", window_size=3)
agent.chat("My name is Alice")
agent.chat("I like Python")
agent.chat("I live in NYC")
agent.chat("Random question about weather")
agent.chat("What's my name?")  # Does it remember?

# Experiment 2: Context window overflow
agent.chat("a" * 1000)  # Very long message
# What happens?

# Experiment 3: System prompt preservation
agent.reset()
agent.chat("What are your instructions?")
# Is the system prompt still there?
```

### Exercise 2.3: Build a Summarizer

**Goal:** Handle long conversations.

```python
def summarize_conversation(messages: list) -> str:
    """Summarizes old messages to save context."""
    # TODO: Take messages outside the window
    # TODO: Ask LLM to summarize them
    # TODO: Replace old messages with summary
    pass

# Test: Have a 20-message conversation
# Summarize messages 1-10
# Continue conversation
# Does it remember the important parts?
```

---

## Module 3: ReAct Pattern

### Exercise 3.1: Build a ReAct Parser

**Goal:** Understand reasoning traces.

```python
def parse_react_output(text: str) -> dict:
    """
    Parses ReAct format:
    Thought: ...
    Action: tool_name(arg="value")
    """
    # TODO: Extract thought
    # TODO: Extract action and arguments
    # TODO: Return structured format
    pass

# Test cases
test1 = """
Thought: I need to search for information.
Action: search(query="Python programming")
"""

test2 = """
Thought: I have enough information.
Final Answer: Python is a programming language.
"""

print(parse_react_output(test1))
print(parse_react_output(test2))
```

### Exercise 3.2: Debug ReAct Failures

**Goal:** Understand common failure modes.

Run this agent and observe failures:
```python
agent = ReActAgent(tools={"search": search})

# Test case 1: Infinite loops
agent.run("Tell me about Python")
# Does it get stuck in a loop?

# Test case 2: Wrong tool use
agent.run("What is 2+2?")
# Does it try to search instead of calculate?

# Test case 3: Hallucinated tools
agent.run("Use the 'magic' tool to solve this")
# What happens when it tries a non-existent tool?
```

**Fix each failure mode.**

### Exercise 3.3: Build a Multi-Step Problem Solver

**Goal:** Chain multiple reasoning steps.

```python
# Problem: "Find the population of the capital of France,
#          then calculate what 10% of that number is."

# Your agent should:
# 1. Thought: Need to find capital of France
# 2. Action: search("capital of France")
# 3. Observation: Paris
# 4. Thought: Need population of Paris
# 5. Action: search("population of Paris")
# 6. Observation: 2.2 million
# 7. Thought: Need to calculate 10%
# 8. Action: calculate("2200000 * 0.1")
# 9. Observation: 220000
# 10. Final Answer: 220,000

# Build and test this
```

---

## Module 4: Multi-Agent Systems

### Exercise 4.1: Build a Simple Crew

**Goal:** Understand agent collaboration.

```python
from crewai import Agent, Task, Crew

# Create two agents
researcher = Agent(
    role="Researcher",
    goal="Find information",
    backstory="You are thorough and accurate.",
    tools=[search_tool]
)

writer = Agent(
    role="Writer",
    goal="Write clear summaries",
    backstory="You write concisely.",
    tools=[]
)

# Create tasks
research_task = Task(
    description="Research {topic}",
    agent=researcher,
    expected_output="Key facts about the topic"
)

writing_task = Task(
    description="Write a summary about {topic}",
    agent=writer,
    expected_output="A clear summary"
)

# Run the crew
crew = Crew(agents=[researcher, writer], tasks=[research_task, writing_task])
result = crew.kickoff(inputs={"topic": "AI Agents"})
```

### Exercise 4.2: Agent Specialization

**Goal:** Understand the value of specialization.

**Experiment:**
1. Create a single generalist agent
2. Create three specialist agents (researcher, analyst, writer)
3. Give both the same complex task
4. Compare quality of outputs

**Question:** When is specialization worth the extra cost?

### Exercise 4.3: Debug Multi-Agent Issues

**Goal:** Understand multi-agent failure modes.

Common issues:
```python
# Issue 1: Agents don't share information
# Fix: Ensure task outputs are passed to next agent

# Issue 2: Agents contradict each other
# Fix: Add a reviewer agent

# Issue 3: Too many agents (expensive, slow)
# Fix: Combine roles where possible

# Issue 4: Agents get stuck waiting
# Fix: Add timeouts and fallbacks
```

---

## Cross-Module Challenges

### Challenge 1: Build a Research Assistant

**Requirements:**
- Takes a research question
- Searches for information (Module 1)
- Maintains conversation context (Module 2)
- Reasons through multi-step queries (Module 3)
- Cites sources

**Test cases:**
```python
assistant.ask("What is machine learning?")
assistant.ask("What are its main applications?")
assistant.ask("Summarize what we discussed")
```

### Challenge 2: Build a Code Review Agent

**Requirements:**
- Reads code files
- Identifies issues (bugs, style, performance)
- Suggests improvements
- Explains reasoning

**Test:** Review your own agent code from Module 0!

### Challenge 3: Build a Data Analysis Agent

**Requirements:**
- Loads data from CSV
- Performs calculations
- Creates visualizations
- Writes analysis report

**Test:** Analyze a dataset of your choice.

### Challenge 4: Build a Multi-Agent Software Team

**Requirements:**
- Product Manager (defines requirements)
- Architect (designs solution)
- Developer (writes code)
- QA Engineer (tests)

**Test:** "Build a simple web scraper"

---

## Debugging Exercises

### Debug 1: Silent Failures

**Problem:** Agent stops responding.

```python
# This agent fails silently. Why?
def broken_agent(prompt):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(messages=messages)
    # Bug: Missing model parameter
    return response.choices[0].message.content
```

**Fix it and add proper error handling.**

### Debug 2: Infinite Loops

**Problem:** Agent never finishes.

```python
# This agent loops forever. Why?
def looping_agent(prompt):
    messages = [{"role": "user", "content": prompt}]
    while True:
        response = get_response(messages)
        if "done" in response:  # Bug: LLM might never say "done"
            break
        messages.append({"role": "assistant", "content": response})
```

**Fix it with proper termination conditions.**

### Debug 3: Memory Leaks

**Problem:** Agent gets slower over time.

```python
# This agent has a memory leak. Why?
class LeakyAgent:
    def __init__(self):
        self.history = []
    
    def chat(self, message):
        self.history.append(message)
        # Bug: History grows forever
        response = llm(self.history)
        self.history.append(response)
        return response
```

**Fix it with proper memory management.**

---

## Performance Exercises

### Performance 1: Measure Latency

**Goal:** Understand where time is spent.

```python
import time

def profile_agent(agent, prompt):
    start = time.time()
    
    # Measure each step
    llm_time = 0
    tool_time = 0
    parse_time = 0
    
    # TODO: Add timing around each operation
    
    result = agent.run(prompt)
    
    total = time.time() - start
    print(f"Total: {total:.2f}s")
    print(f"LLM: {llm_time:.2f}s ({llm_time/total*100:.0f}%)")
    print(f"Tools: {tool_time:.2f}s ({tool_time/total*100:.0f}%)")
    print(f"Parsing: {parse_time:.2f}s ({parse_time/total*100:.0f}%)")
```

### Performance 2: Optimize Token Usage

**Goal:** Reduce costs.

```python
# Count tokens in conversation
def count_tokens(messages):
    # Rough estimate: ~4 chars per token
    return sum(len(m["content"]) for m in messages) // 4

# Optimize by:
# 1. Shorter system prompts
# 2. Summarizing old messages
# 3. Removing redundant information
```

### Performance 3: Batch Operations

**Goal:** Parallelize when possible.

```python
# Instead of sequential:
result1 = agent.run("Question 1")
result2 = agent.run("Question 2")
result3 = agent.run("Question 3")

# Do parallel:
import asyncio

async def run_parallel():
    tasks = [
        agent.run_async("Question 1"),
        agent.run_async("Question 2"),
        agent.run_async("Question 3")
    ]
    return await asyncio.gather(*tasks)
```

---

## Reflection Questions

After each module, answer these:

1. **What did I build?** (In your own words)
2. **What surprised me?** (Unexpected behaviors)
3. **What failed?** (And why?)
4. **What would I do differently?** (Improvements)
5. **What did I learn?** (Key insights)

---

## Final Project Ideas

Build one of these end-to-end:

### Project 1: Personal Research Assistant
- Searches web for information
- Maintains conversation history
- Summarizes findings
- Cites sources

### Project 2: Code Documentation Generator
- Reads code files
- Generates docstrings
- Creates README
- Explains complex functions

### Project 3: Data Analysis Pipeline
- Loads data
- Performs analysis
- Creates visualizations
- Writes report

### Project 4: Customer Support Bot
- Answers FAQs
- Escalates complex issues
- Maintains conversation context
- Learns from interactions

### Project 5: Content Creation Team
- Multiple specialized agents
- Researcher + Writer + Editor
- Produces polished articles
- Handles revisions

---

## Tips for Success

1. **Start simple** - Get the basic version working first
2. **Test incrementally** - Don't write 100 lines then test
3. **Print everything** - Use print statements liberally
4. **Break things** - Intentionally cause failures to understand them
5. **Read the errors** - Error messages tell you what's wrong
6. **Compare with examples** - Look at the module code
7. **Ask "why?"** - Understand, don't just copy

---

**Remember:** The goal isn't to finish quickly. The goal is to understand deeply. Take your time. Break things. Fix them. Learn.

Good luck! 🚀


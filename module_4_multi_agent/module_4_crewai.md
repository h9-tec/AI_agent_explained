# Module 4: Multi-Agent Orchestration with CrewAI

## The Problem

You've built agents (Modules 0-3). They work. But you'll notice something: **single agents hit a wall**.

Try asking your Module 3 ReAct agent to:
1. Research a complex topic
2. Analyze the findings
3. Write a comprehensive report

It can do it, but the quality suffers. Why? Because you're asking one generalist to do three specialist jobs.

**The insight:** Some problems need multiple perspectives, not just multiple steps.

---

## The Solution (And Why We Waited)

**Multi-agent systems:** Multiple specialized agents working together.

**Why Module 4, not Module 1?**

Because you needed to understand:
- What an agent is (Module 0)
- How agents use tools (Module 1)
- How agents maintain state (Module 2)
- How agents reason (Module 3)

Now you can understand what a multi-agent framework is doing: **orchestrating agents you already know how to build**.

This is the right way: understand the primitives before composing them.

---

## What CrewAI Actually Does

Strip away the marketing, and CrewAI does three things:

1. **Manages agent state** - You built this in Module 2
2. **Routes messages between agents** - Just function calls
3. **Executes workflows** - Sequential, hierarchical, or parallel

**That's it.** No magic. Just good engineering.

Let's build a crew and see exactly what's happening.

---

## What is CrewAI?

CrewAI is a framework that treats AI agents as a "crew" working together. Think of it like a software development team:

- **Product Manager** defines requirements
- **Architect** designs the system
- **Developer** writes the code
- **QA Engineer** tests everything

Each role is specialized, and they work together in a coordinated way.

### Key Concepts

#### 1. Agent
An agent in CrewAI has:
- **Role:** What they do (e.g., "Senior Researcher")
- **Goal:** What they're trying to achieve
- **Backstory:** Context that shapes their behavior
- **Tools:** Functions they can use
- **Delegation:** Whether they can assign work to others

```python
researcher = Agent(
    role="Senior Researcher",
    goal="Gather comprehensive information on assigned topics",
    backstory="You are an experienced researcher with a keen eye for detail.",
    tools=[search_tool],
    verbose=True
)
```

#### 2. Task
A task defines work to be done:
- **Description:** What needs to be accomplished
- **Agent:** Who will do it
- **Expected Output:** What the result should look like

```python
research_task = Task(
    description="Research the topic: {topic}",
    agent=researcher,
    expected_output="A comprehensive research summary"
)
```

#### 3. Crew
A crew brings agents and tasks together:
- **Agents:** The team members
- **Tasks:** The work to be done
- **Process:** How tasks are executed (sequential, hierarchical, etc.)

```python
crew = Crew(
    agents=[researcher, analyst, writer],
    tasks=[research_task, analysis_task, writing_task],
    process=Process.sequential
)
```

#### 4. Process
How tasks are executed:
- **Sequential:** One task at a time, in order
- **Hierarchical:** A manager agent delegates to workers
- **Consensus:** Agents collaborate to reach agreement

---

## Building Your First Crew

Let's build a research crew that can investigate a topic and produce a report.

### Step 1: Define Custom Tools

```python
from crewai_tools import tool

@tool("Search Tool")
def search_tool(query: str) -> str:
    """Searches for information on a given query."""
    # Implementation here
    return "Search results..."
```

### Step 2: Create Specialized Agents

```python
from crewai import Agent

researcher = Agent(
    role="Senior Researcher",
    goal="Gather comprehensive information",
    backstory="You excel at finding relevant information.",
    tools=[search_tool],
    verbose=True
)

analyst = Agent(
    role="Data Analyst",
    goal="Analyze information and extract insights",
    backstory="You identify patterns and draw conclusions.",
    tools=[calculator_tool],
    verbose=True
)

writer = Agent(
    role="Technical Writer",
    goal="Create clear, engaging reports",
    backstory="You transform complex info into accessible content.",
    tools=[writing_tool],
    verbose=True
)
```

### Step 3: Define Tasks

```python
from crewai import Task

research_task = Task(
    description="Research the topic: {topic}",
    agent=researcher,
    expected_output="A comprehensive research summary"
)

analysis_task = Task(
    description="Analyze the research findings",
    agent=analyst,
    expected_output="Detailed analysis with insights"
)

writing_task = Task(
    description="Create a final report",
    agent=writer,
    expected_output="A polished final report"
)
```

### Step 4: Create and Run the Crew

```python
from crewai import Crew, Process

crew = Crew(
    agents=[researcher, analyst, writer],
    tasks=[research_task, analysis_task, writing_task],
    process=Process.sequential,
    verbose=2
)

# Run the crew
result = crew.kickoff(inputs={"topic": "AI Agents"})
print(result)
```

---

## Execution Processes

### Sequential Process

Tasks are executed one after another. Each agent completes their task before the next begins.

**Use when:**
- Tasks have clear dependencies
- Each task builds on the previous one
- You want predictable execution order

**Example:** Research → Analysis → Writing

### Hierarchical Process

A manager agent coordinates worker agents, delegating tasks and reviewing results.

**Use when:**
- Tasks can be parallelized
- You need dynamic task allocation
- Quality control is important

**Example:** Manager assigns research topics to multiple researchers

### Consensus Process

Agents collaborate and reach agreement on decisions.

**Use when:**
- Multiple perspectives are valuable
- Decisions need validation
- Quality through peer review

**Example:** Multiple reviewers evaluating a proposal

---

## Best Practices

### 1. Clear Role Definition

Make each agent's role specific and distinct:

✅ **Good:** "Senior Python Developer specializing in API design"  
❌ **Bad:** "Developer"

### 2. Specific Goals

Goals should be measurable and achievable:

✅ **Good:** "Create a REST API with authentication and rate limiting"  
❌ **Bad:** "Build something good"

### 3. Rich Backstories

Backstories shape agent behavior:

✅ **Good:** "You have 10 years of experience in distributed systems and always consider scalability, fault tolerance, and monitoring."  
❌ **Bad:** "You are experienced."

### 4. Appropriate Tools

Give agents only the tools they need:

- Researcher → search_tool
- Analyst → calculator_tool, data_tool
- Writer → writing_tool, grammar_tool

### 5. Clear Task Descriptions

Tasks should specify:
- What to do
- What information to include
- What format to use
- What quality standards to meet

### 6. Expected Outputs

Define what success looks like:

```python
Task(
    description="Analyze user data",
    expected_output="A report with: 1) Key metrics, 2) Trends, 3) Recommendations"
)
```

---

## Common Patterns

### Research and Report Pattern

**Agents:** Researcher → Analyst → Writer  
**Use case:** Investigating topics and producing reports

### Software Development Pattern

**Agents:** Architect → Developer → QA Engineer  
**Use case:** Building software systems

### Content Creation Pattern

**Agents:** Researcher → Content Creator → Editor  
**Use case:** Creating articles, documentation, marketing content

### Customer Support Pattern

**Agents:** Triage Agent → Specialist Agent → Quality Reviewer  
**Use case:** Handling customer inquiries

---

## Comparison: Single Agent vs. Multi-Agent

| Aspect | Single Agent | Multi-Agent (CrewAI) |
|--------|--------------|----------------------|
| **Complexity** | Simple tasks | Complex, multi-step tasks |
| **Specialization** | Generalist | Specialists for each role |
| **Quality** | Good | Better (through specialization) |
| **Scalability** | Limited | High (add more agents) |
| **Coordination** | Not needed | Built-in orchestration |
| **Cost** | Lower | Higher (more LLM calls) |

---

## When to Use CrewAI

### ✅ Use CrewAI When:

- Tasks require multiple areas of expertise
- Quality benefits from specialization
- Work can be divided into clear stages
- You need reproducible workflows
- Collaboration improves outcomes

### ❌ Don't Use CrewAI When:

- Task is simple and straightforward
- Single agent can handle it well
- Cost is a major concern
- Real-time response is critical
- Task doesn't benefit from multiple perspectives

---

## Integration with llama.cpp

CrewAI works with both OpenAI and local models via llama.cpp. However:

**Considerations for llama.cpp:**
- Use capable models (Mistral 7B Instruct or larger)
- Expect longer execution times
- May need to adjust prompts for local models
- Test thoroughly with your specific model

**Recommended setup:**
```python
# In your .env file
LLM_BACKEND=llamacpp
LLAMA_MODEL_PATH=./models/mistral-7b-instruct-v0.2.Q4_K_M.gguf
LLAMA_TEMPERATURE=0.7
```

---

## Exercises

### Exercise 1: Custom Research Crew

Create a crew that researches a technology topic:
1. Researcher gathers information
2. Analyst identifies pros and cons
3. Writer creates a comparison report

### Exercise 2: Code Review Crew

Build a crew for code review:
1. Reviewer checks for bugs
2. Security expert checks for vulnerabilities
3. Performance expert checks for optimization opportunities

### Exercise 3: Content Creation Crew

Design a crew for blog posts:
1. SEO specialist researches keywords
2. Writer creates the content
3. Editor polishes and optimizes

---

## Key Takeaways

1. **Multi-agent systems** divide complex tasks among specialized agents
2. **CrewAI** provides a framework for orchestrating agent collaboration
3. **Agents** have roles, goals, backstories, and tools
4. **Tasks** define work with clear descriptions and expected outputs
5. **Processes** determine how tasks are executed (sequential, hierarchical, etc.)
6. **Specialization** improves quality through focused expertise
7. **Coordination** is handled automatically by the framework

---

## Next Steps

- Experiment with different agent roles and tasks
- Try different execution processes
- Build a multi-agent system for your own use case
- Compare single-agent vs. multi-agent approaches
- Explore advanced CrewAI features (memory, callbacks, etc.)

---

## Resources

- **CrewAI Documentation:** https://docs.crewai.com/
- **CrewAI GitHub:** https://github.com/joaomdmoura/crewAI
- **CrewAI Tools:** https://github.com/joaomdmoura/crewai-tools
- **Example Projects:** https://github.com/crewAIInc/crewAI-examples

---

**Congratulations!** You now understand how to build multi-agent systems with CrewAI. You've progressed from simple agent loops to sophisticated collaborative AI systems. This is a powerful pattern for tackling complex real-world problems.

In the next modules (5-9), we'll explore advanced patterns, production considerations, and real-world applications. Keep building! 🚀


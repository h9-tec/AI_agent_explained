# Module 4: Multi-Agent Orchestration

**Building Collaborative Agent Teams with CrewAI**

## Overview

Single agents hit limits with complex tasks. This module teaches you how to build multi-agent systems where specialized agents collaborate to solve problems that would overwhelm a single agent.

## Key Concept

> "Some problems need multiple perspectives, not just multiple steps."

## What You'll Learn

- Multi-agent system design
- Agent specialization and roles
- Task orchestration
- Sequential and hierarchical workflows
- Inter-agent communication
- CrewAI framework

## Files in This Module

- `module_4_crewai_agents.py` - Complete multi-agent implementation
- `module_4_crewai.md` - Detailed explanation and theory

## Quick Start

```bash
pip install crewai crewai-tools
python module_4_crewai_agents.py
```

## Why Multi-Agent?

**Single Agent Problem:**
- One generalist doing multiple specialist jobs
- Quality suffers on complex tasks
- No peer review or validation

**Multi-Agent Solution:**
- Specialized agents for specific roles
- Higher quality through expertise
- Built-in review and validation

## CrewAI Concepts

### Agent
```python
researcher = Agent(
    role="Senior Researcher",
    goal="Gather comprehensive information",
    backstory="You are an experienced researcher...",
    tools=[search_tool],
    verbose=True
)
```

### Task
```python
research_task = Task(
    description="Research {topic}",
    agent=researcher,
    expected_output="Comprehensive research notes"
)
```

### Crew
```python
crew = Crew(
    agents=[researcher, analyst, writer],
    tasks=[research_task, analysis_task, writing_task],
    process=Process.sequential
)
```

## Example Crews

### 1. Research Crew
- **Researcher:** Gathers information
- **Analyst:** Identifies insights
- **Writer:** Creates final report

### 2. Software Development Crew
- **Architect:** Designs solution
- **Developer:** Implements code
- **QA Engineer:** Tests and validates

## Exercise

Build a content creation crew:
1. SEO Specialist (keyword research)
2. Writer (creates content)
3. Editor (polishes and optimizes)

See `docs/EXERCISES.md` for detailed exercises.

## Execution Processes

### Sequential
Tasks execute one after another. Each agent completes their task before the next begins.

**Use when:** Tasks have clear dependencies

### Hierarchical
A manager agent coordinates worker agents, delegating tasks dynamically.

**Use when:** Tasks can be parallelized

### Consensus
Agents collaborate and reach agreement on decisions.

**Use when:** Multiple perspectives needed

## Common Issues

- **Agents don't share information:** Ensure task outputs pass to next agent
- **Agents contradict each other:** Add reviewer agent
- **Too expensive:** Combine roles where possible
- **Slow execution:** Consider parallel processes

## Best Practices

1. **Clear roles:** Each agent has specific expertise
2. **Specific goals:** Measurable, achievable objectives
3. **Rich backstories:** Shape agent behavior
4. **Appropriate tools:** Give agents what they need
5. **Clear task descriptions:** Specify format and quality

## When to Use Multi-Agent

✅ **Use when:**
- Task requires multiple areas of expertise
- Quality benefits from specialization
- Work can be divided into clear stages
- Collaboration improves outcomes

❌ **Don't use when:**
- Task is simple and straightforward
- Single agent can handle it well
- Cost is a major concern
- Real-time response is critical

## Integration with llama.cpp

CrewAI works with both OpenAI and local models. For best results with llama.cpp:
- Use capable models (Mistral 7B Instruct or larger)
- Expect longer execution times
- Test thoroughly with your specific model

## Next Steps

You've completed the core modules! Now explore:
- `docs/EXAMPLES.md` - Real-world applications
- `docs/DEBUGGING_GUIDE.md` - Troubleshooting techniques
- `docs/EXERCISES.md` - Advanced challenges

---

**Part of:** AI Agents and Agent Frameworks: Zero to Hero by Hesham Haroon


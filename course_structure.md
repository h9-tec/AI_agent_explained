# AI Agents and Agent Frameworks: Zero to Hero
## A Course by "Andrej Karpathy" Style Teaching

---

## Course Philosophy

This course follows the principle: **Build everything from scratch, in code**. We will not use any high-level agent frameworks until we've built our own from first principles. By the end, you'll understand exactly what's happening under the hood of every agent system, and you'll be able to debug, customize, and build production-grade agents with confidence.

**Prerequisites:**
- Solid Python programming
- Basic understanding of LLMs and APIs
- Familiarity with async programming (helpful but not required)
- Intro-level understanding of prompting

**What makes this different:**
- Every concept is implemented from scratch before using frameworks
- Step-by-step spelled-out explanations with no hand-waving
- Heavy emphasis on visualization and debugging
- Build intuition through experimentation
- Real code that you can run and modify

---

## Course Structure (10 Modules)

### Module 0: The Agent Loop - Building Your First Agent (2 hours)
**Philosophy: Start with the simplest possible thing that works**

- What is an agent? (Not what you think)
- The fundamental agent loop: Think -> Act -> Observe
- Building a 50-line agent from scratch (no frameworks)
- Understanding why agents "fail silently"
- Visualizing agent reasoning
- **Project:** Build a calculator agent that can do multi-step math

**Key Insight:** An agent is just a while loop with an LLM inside it.

---

### Module 1: Tool Use - Teaching Agents to Use APIs (2.5 hours)
**Philosophy: Become one with the data (tool outputs)**

- Function calling: How LLMs learn to use tools
- Building a tool registry from scratch
- Tool schemas and why they matter
- Handling tool errors gracefully
- Visualizing tool call patterns
- Common pitfalls: Too many tools, ambiguous descriptions
- **Project:** Build a weather + news agent that chains tool calls

**Key Insight:** Tools are just functions, but the schema is everything.

---

### Module 2: Memory and State - Making Agents Stateful (2 hours)
**Philosophy: Verify everything about your state management**

- Why agents need memory
- Building a conversation buffer from scratch
- Implementing sliding window memory
- Vector memory for long-term recall
- State serialization and persistence
- Debugging memory issues
- **Project:** Build a customer service agent with conversation history

**Key Insight:** Memory is a leaky abstraction - you need to understand what gets remembered and what gets forgotten.

---

### Module 3: Planning and Reasoning - ReAct Pattern Deep Dive (3 hours)
**Philosophy: Build from simple to complex, verify at each step**

- The ReAct pattern: Reason + Act
- Implementing ReAct from scratch (100 lines)
- Chain-of-thought prompting for agents
- When planning helps vs. when it hurts
- Visualizing the reasoning trace
- Common failure modes and how to debug them
- **Project:** Build a research agent that can answer complex questions

**Key Insight:** ReAct is powerful but not magic - it fails in predictable ways.

---

### Module 4: Agent Orchestration - Multi-Step Workflows (2.5 hours)
**Philosophy: Introduce complexity incrementally, test each component**

- Sequential vs. parallel execution
- Building a state machine for agents
- Conditional branching in agent flows
- Error handling and retries
- Implementing timeouts and guardrails
- **Project:** Build a data analysis agent with multi-step workflow

**Key Insight:** Orchestration is about control flow - treat it like any other programming problem.

---

### Module 5: Multi-Agent Systems - Agents Working Together (3 hours)
**Philosophy: Generalize from special cases**

- Why multiple agents?
- Manager-worker pattern from scratch
- Agent-to-agent communication
- Shared vs. isolated state
- Conflict resolution and consensus
- Visualizing multi-agent interactions
- **Project:** Build a software development team (planner, coder, tester agents)

**Key Insight:** Multi-agent systems are just single agents with extra steps - don't over-complicate.

---

### Module 6: Advanced Patterns - Reflection, Self-Critique, and Iteration (2.5 hours)
**Philosophy: Understand the failure modes before adding complexity**

- The reflection pattern: Agents critiquing themselves
- Implementing self-correction loops
- When to stop iterating (convergence criteria)
- Avoiding infinite loops
- Cost vs. quality tradeoffs
- **Project:** Build a code review agent that improves its own suggestions

**Key Insight:** Reflection is expensive - use it strategically.

---

### Module 7: Production Considerations - Making Agents Reliable (3 hours)
**Philosophy: Be thorough, defensive, and paranoid**

- Testing agent systems (it's harder than you think)
- Monitoring and observability
- Rate limiting and cost control
- Handling API failures gracefully
- Security considerations (prompt injection, tool access)
- Versioning and rollback strategies
- **Project:** Add production-grade error handling to previous agents

**Key Insight:** Agents fail silently - you need comprehensive logging and monitoring.

---

### Module 8: Agent Frameworks - LangGraph Deep Dive (3 hours)
**Philosophy: Now that you understand the internals, use the tools**

- Why use a framework (and when not to)
- LangGraph architecture and design philosophy
- Migrating our scratch implementations to LangGraph
- Advanced LangGraph patterns
- Debugging LangGraph agents
- **Project:** Rebuild the multi-agent system using LangGraph

**Key Insight:** Frameworks are useful, but only if you understand what they're abstracting.

---

### Module 9: Real-World Applications and Case Studies (3 hours)
**Philosophy: Learn from production deployments**

- Customer service automation
- Code generation and debugging
- Research and data analysis
- Content creation and editing
- What works in production vs. demos
- Common failure modes and solutions
- Cost analysis and optimization
- **Project:** Build an end-to-end application of your choice

**Key Insight:** Production agents are 80% error handling and 20% happy path.

---

## Course Deliverables

### For Each Module:
1. **Detailed written explanations** (Karpathy blog post style)
2. **Complete, runnable code** (every line explained)
3. **Jupyter notebooks** for interactive exploration
4. **Visualization tools** for debugging
5. **Exercises** with solutions
6. **Common pitfalls** section

### Final Project:
Build a complete agent system that:
- Uses multiple agents
- Has proper error handling
- Includes monitoring and logging
- Demonstrates real-world value
- Is production-ready (or close to it)

---

## Teaching Methodology

### The "Recipe" Approach (inspired by Karpathy):

1. **Become one with the problem**
   - Understand what agents are good at (and bad at)
   - Inspect real agent traces manually
   - Develop intuition before coding

2. **Start with the simplest thing**
   - Build a 50-line agent before using frameworks
   - Verify it works on toy examples
   - Understand every failure mode

3. **Build incrementally**
   - Add one feature at a time
   - Test thoroughly before moving on
   - Visualize everything

4. **Overfit, then generalize**
   - Get it working on one example first
   - Then make it robust
   - Then make it efficient

5. **Be paranoid**
   - Agents fail silently
   - Log everything
   - Verify assumptions constantly

---

## Code Structure

All code will be:
- **Self-contained**: Each module's code runs independently
- **Heavily commented**: Every non-obvious line explained
- **Progressively complex**: Start simple, build up
- **Debuggable**: Extensive logging and visualization
- **Tested**: Unit tests for critical components

---

## Estimated Time Commitment

- **Total video content**: ~25 hours
- **Coding exercises**: ~20 hours
- **Projects**: ~15 hours
- **Total**: ~60 hours for complete mastery

---

## Success Criteria

By the end of this course, you will be able to:

1. Build an agent system from scratch (no frameworks)
2. Debug agent failures systematically
3. Design multi-agent architectures
4. Implement production-grade error handling
5. Choose the right tools and patterns for your use case
6. Understand exactly what LangGraph (and other frameworks) are doing
7. Deploy agents that actually work in production

---

## What This Course Is NOT

- Not a survey of agent frameworks
- Not a collection of demos that "just work"
- Not high-level theory without implementation
- Not using frameworks as black boxes

This is a **ground-up, implementation-first** course that builds real understanding through code.

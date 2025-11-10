# AI Agents and Agent Frameworks: Zero to Hero

**By Hesham Haroon**

---

## Welcome

This is a comprehensive, implementation-first course on building AI agents from scratch. We build everything from first principles, in code, with step-by-step explanations. No hand-waving. No black boxes. Just pure, fundamental understanding.

## Philosophy

> "The qualities that correlate most strongly to success in AI are patience and attention to detail."

This course embodies that philosophy. We start with the simplest possible agent (a 50-line loop) and progressively build up to production-grade multi-agent systems. At every step, we verify our assumptions, visualize our results, and develop deep intuition about how agents work and why they fail.

**Core principle:** Build it yourself first. Then use frameworks. This way, you understand what they're doing and can debug them when they fail.

## Course Structure

The course consists of 10 modules, each building on the previous one:

| Module | Topic | Duration | Key Concepts |
|--------|-------|----------|--------------|
| **0** | The Agent Loop | 2 hours | Basic agent architecture, Think-Act-Observe cycle |
| **1** | Tool Use | 2.5 hours | Function calling, tool registry, API integration |
| **2** | Memory and State | 2 hours | Conversation history, sliding windows, state management |
| **3** | Planning and Reasoning | 3 hours | ReAct pattern, reasoning traces, multi-step problems |
| **4** | Agent Orchestration | 2.5 hours | Workflows, state machines, error handling |
| **5** | Multi-Agent Systems | 3 hours | Agent collaboration, manager-worker patterns |
| **6** | Advanced Patterns | 2.5 hours | Reflection, self-critique, iterative improvement |
| **7** | Production Considerations | 3 hours | Testing, monitoring, security, reliability |
| **8** | Agent Frameworks | 3 hours | LangGraph deep dive, framework comparison |
| **9** | Real-World Applications | 3 hours | Case studies, production deployments |

**Total Time:** ~60 hours for complete mastery (25 hours of content + 35 hours of projects)

## What Makes This Course Different

### 1. Build Everything from Scratch

We don't use frameworks until Module 8. By then, you'll understand exactly what they're abstracting and why they're useful. You'll be able to debug framework code because you've built the same thing yourself.

### 2. Code-First, Always

Every concept is implemented in code. We don't just talk about agents; we build them, run them, watch them fail, and fix them. The code is heavily commented and designed to be read and understood, not just executed.

### 3. Visualization and Debugging

Agents fail silently. The only way to understand them is to visualize their internal state. We build visualization tools for every major concept: reasoning traces, tool call patterns, memory windows, and multi-agent interactions.

### 4. Incremental Complexity

We follow the "recipe" approach:
- Start with the simplest thing that could possibly work
- Verify it works on toy examples
- Understand every failure mode
- Only then add complexity

### 5. Real Production Considerations

Most courses stop at demos. We go further. We cover testing, monitoring, error handling, security, and all the unglamorous but critical aspects of deploying agents in production.

## Prerequisites

- **Solid Python programming:** You should be comfortable with classes, decorators, and basic data structures
- **Basic understanding of LLMs:** You should know what a language model is and how to use an API
- **Intro-level math:** Basic probability and calculus (though we don't go deep into theory)
- **Async programming (helpful):** Some modules use async/await, but we explain it when needed

## Setup

### Option 1: Original Course (OpenAI Only)

The simplest way to start. Just one dependency:

```bash
pip install openai
export OPENAI_API_KEY="your-api-key-here"
python module_0_agent.py
```

### Option 2: Extended Course (Local Models + Frameworks)

Want to run models locally or explore multi-agent systems? See `SETUP_GUIDE.md` for:
- **llama.cpp integration** - Run models on your own hardware (free, private)
- **CrewAI framework** - Build collaborative multi-agent systems
- **Unified interface** - Switch between OpenAI and local models with one config change

```bash
pip install -r requirements.txt
cp .env.example .env
# Edit .env to configure your backend
python module_0_agent_llamacpp.py
```

**Philosophy:** We build everything from scratch first (Modules 0-3), then introduce frameworks (Module 4+). This way, you understand what the frameworks are doing under the hood.

## Repository Structure

```
ai_agents_course/
├── module_0_agent_loop/          # The basic agent loop
│   ├── README.md                 # Module overview and exercises
│   ├── module_0_agent.py         # Original OpenAI version
│   ├── module_0_agent_llamacpp.py # Extended llama.cpp version
│   └── module_0_agent_loop.md    # Detailed theory
│
├── module_1_tool_use/            # Tool calling and APIs
│   ├── README.md
│   ├── module_1_tool_agent.py
│   ├── module_1_tool_agent_llamacpp.py
│   └── module_1_tool_use.md
│
├── module_2_memory_state/        # Memory and conversation state
│   ├── README.md
│   ├── module_2_memory_agent.py
│   ├── module_2_memory_agent_llamacpp.py
│   └── module_2_memory_state.md
│
├── module_3_planning_reasoning/  # ReAct pattern
│   ├── README.md
│   ├── module_3_react_agent.py
│   ├── module_3_react_agent_llamacpp.py
│   └── module_3_planning_reasoning.md
│
├── module_4_multi_agent/         # Multi-agent with CrewAI
│   ├── README.md
│   ├── module_4_crewai_agents.py
│   └── module_4_crewai.md
│
├── docs/                         # All documentation
│   ├── README.md                 # Documentation index
│   ├── EXERCISES.md              # Hands-on exercises
│   ├── EXAMPLES.md               # Real-world examples
│   ├── DEBUGGING_GUIDE.md        # Troubleshooting
│   ├── SETUP_GUIDE.md            # Installation and setup
│   ├── QUICK_REFERENCE.md        # Command cheat sheet
│   └── [More guides...]
│
├── examples/                     # Complete applications
│   ├── README.md
│   └── advanced_example_full_agent.py
│
├── config.py                     # Configuration system
├── llm_client.py                 # Unified LLM client
├── requirements.txt              # Dependencies
└── README.md                     # This file
```

**The Pattern:** Build it yourself → Understand it deeply → Use frameworks wisely

## How to Use This Course

### For Self-Study

1. **Start with a module** - Read the module's `README.md`
2. **Study the theory** - Read the detailed `.md` file
3. **Run the code** - Execute both versions (OpenAI and llama.cpp)
4. **Complete exercises** - See `docs/EXERCISES.md`
5. **Debug issues** - Use `docs/DEBUGGING_GUIDE.md`
6. **Study examples** - Check `docs/EXAMPLES.md`
7. **Move to next module** - Only when you feel confident

**Learning Path:**
```
Module README → Theory → Code → Exercises → Debug → Examples → Next Module
```

**Key Resources:**
- Each module has its own `README.md` with quick start and exercises
- `docs/` folder contains all guides and references
- `examples/` folder has complete applications

### For Teaching

This course is designed to be taught in a workshop or classroom setting:

- Each module is ~2-3 hours of content
- Mix lecture with live coding
- Have students complete projects in pairs
- Use the visualization tools to debug together
- Emphasize the "recipe" approach: verify everything before moving on

## Key Insights

Throughout this course, you'll encounter key insights that are fundamental to understanding agents:

- **"An agent is just a while loop with an LLM inside it"** - Don't over-complicate
- **"Agents fail silently"** - You need comprehensive logging and visualization
- **"The schema is part of the prompt"** - Tool descriptions matter as much as code
- **"Memory is a leaky abstraction"** - You must understand what gets remembered
- **"ReAct is powerful but not magic"** - It fails in predictable ways
- **"Production agents are 80% error handling"** - The happy path is the easy part

## Projects

Each module includes a hands-on project:

**Core Modules (Build from Scratch):**
- **Module 0:** Build a calculator agent (understand the loop)
- **Module 1:** Build a weather + news agent (understand tools)
- **Module 2:** Build a customer service agent with memory (understand state)
- **Module 3:** Build a research agent that can answer complex questions (understand reasoning)

**Extended Modules (Apply Your Knowledge):**
- **Module 4:** Build a collaborative research team with CrewAI (understand orchestration)
- **Module 5:** Build a software development team (multiple agents)
- **Module 6:** Build a code review agent with self-correction
- **Module 7:** Add production-grade error handling to previous agents
- **Module 8:** Migrate agents to LangGraph (now you know what it's doing!)
- **Module 9:** Build an end-to-end application of your choice

**The Philosophy:** You can't debug what you don't understand. Build it first, then use the framework.

## Common Pitfalls (And How to Avoid Them)

### 1. Premature Abstraction
**Problem:** Using frameworks before understanding the fundamentals  
**Solution:** Build from scratch first (Modules 0-7), then use frameworks (Module 8+)

### 2. Silent Failures
**Problem:** Agent doesn't work, but no error messages  
**Solution:** Comprehensive logging, visualization, and reasoning traces

### 3. Poor Tool Design
**Problem:** Agent can't figure out which tool to use  
**Solution:** Clear, descriptive tool names and schemas

### 4. Memory Issues
**Problem:** Agent forgets important information or runs out of context  
**Solution:** Proper memory management with sliding windows or vector stores

### 5. Infinite Loops
**Problem:** Agent gets stuck in a reasoning loop  
**Solution:** Max iterations, convergence criteria, and monitoring

## Success Criteria

By the end of this course, you will be able to:

✅ Build an agent system from scratch without frameworks  
✅ Debug agent failures systematically using reasoning traces  
✅ Design multi-agent architectures for complex tasks  
✅ Implement production-grade error handling and monitoring  
✅ Choose the right tools and patterns for your use case  
✅ Understand exactly what frameworks like LangGraph are doing under the hood  
✅ Deploy agents that actually work in production (not just demos)

## Course Extensions

### Why Local Models? (llama.cpp)

After building agents with OpenAI (Modules 0-3), you understand the fundamentals. Now you can ask: **"What if I want to run this on my own hardware?"**

This is the right way: understand the abstraction, then build your own version.

- **`llm_client.py`** - We build a unified client from scratch. You'll see exactly how to abstract different backends.
- **`config.py`** - Simple configuration system. No magic, just environment variables and validation.
- **`module_*_llamacpp.py`** - Same agents, different backend. See how little actually changes.

**The lesson:** Good abstractions are portable. Bad abstractions leak everywhere.

### Why Multi-Agent? (CrewAI)

After building single agents (Modules 0-3), you'll hit limits: some tasks need multiple perspectives, specialized expertise, or parallel work.

- **Module 4** introduces CrewAI, but only after you've built agents yourself
- You'll understand what the framework is doing (orchestration, message passing, state management)
- You can debug it because you've built similar systems

**The lesson:** Frameworks are useful when you understand what they're solving.

## Resources

- **OpenAI Agents Guide:** https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf
- **ReAct Paper:** https://arxiv.org/abs/2210.03629
- **LangGraph Documentation:** https://langchain-ai.github.io/langgraph/
- **llama.cpp:** https://github.com/ggerganov/llama.cpp
- **CrewAI:** https://docs.crewai.com/

## About the Author

**Hesham Haroon** - AI Engineer and Educator

This course represents years of experience building and deploying AI agents in production environments. The methodology is based on practical, hands-on learning that has proven effective for developers at all levels.

## Contributing

Found a bug? Have a suggestion? Want to add a module? Contributions are welcome! This course is designed to evolve with the field.

## License

This course is provided for educational purposes. The code is free to use, modify, and distribute. Attribution is appreciated but not required.

---

## Final Thoughts

Building agents is hard. They fail in unexpected ways. They're expensive to run. They require careful prompt engineering, robust error handling, and constant monitoring. But when they work, they're magical. They can solve problems that would be impossible with traditional software.

The key to success is patience, attention to detail, and a willingness to dig deep into the fundamentals. Don't rush. Don't skip modules. Build everything from scratch. Understand every line of code. Visualize everything. Be paranoid about failures.

And most importantly: **have fun**. Building agents is one of the most exciting frontiers in AI. You're learning to create systems that can reason, plan, and act autonomously. That's pretty cool.

Now, let's get started. Open `module_0_agent_loop.md` and begin your journey from zero to hero.

Good luck! 🚀

# Module 3: Planning and Reasoning - ReAct Pattern Deep Dive

**A Course by "Andrej Karpathy" Style Teaching**

---

Alright, let's take a moment to appreciate how far we've come. We've built an agent loop from scratch, given it tools, and endowed it with memory. Our agent is no longer a simple stateless script; it's a stateful system that can interact with its environment and remember past events. But it's still missing a key ingredient: **reasoning**. Right now, our agent is purely reactive. It sees a prompt, it calls a tool. It sees another prompt, it calls another tool. It doesn't have a high-level plan. It's just taking things one step at a time.

To build agents that can solve complex, multi-step problems, we need to teach them how to **plan**. We need to give them the ability to reason about their goal, break it down into smaller steps, and then execute those steps in a logical order. This is where the **ReAct** pattern comes in. ReAct, which stands for **Reason + Act**, is a simple but incredibly powerful paradigm for building reasoning agents. And, of course, we're going to build it from scratch.

## The ReAct Pattern: A Simple Idea

The core idea behind ReAct is to augment the agent's context with its own internal monologue. Before taking an action, the agent first 
thinks about what it should do and why. This "thought" is then added to the prompt, giving the LLM more context for its next decision. The cycle looks like this:

1.  **Thought:** The agent analyzes the current situation and its goal, and formulates a plan or a next step. This is a private, internal monologue.
2.  **Action:** Based on its thought, the agent decides to take an action (e.g., call a tool).
3.  **Observation:** The agent receives the result of its action.

This loop continues until the agent has reached its goal. The key difference from our previous agent is the explicit "Thought" step. By forcing the agent to articulate its reasoning, we make its behavior more predictable, debuggable, and effective.

## Implementing ReAct from Scratch (100 lines)

Let's modify our agent to incorporate this reasoning step. The changes are surprisingly minimal. We just need to update our system prompt to instruct the model to follow the Thought-Action-Observation format, and then parse its output accordingly.

Here's how we can structure the prompt:

```
You are a helpful assistant. You have access to the following tools:

[...tool schemas...]

To solve the problem, you must use the following format:

Thought: Your reasoning and plan for the next step.
Action: The tool call you want to make, in the format `ToolName(arg1=value1, arg2=value2)`.
Observation: The result of the tool call (this will be provided by the system).
... (this Thought/Action/Observation cycle can repeat N times)
Thought: I now have the final answer.
Final Answer: The final answer to the original question.
```

Our agent loop will now need to parse this structure. In each iteration, we'll look for a "Thought" and an "Action". We'll execute the action, get the observation, and then append it to the message history before the next iteration. This gives the LLM a complete picture of its own reasoning process.

## Visualizing the Reasoning Trace

As always, visualization is key. The beauty of the ReAct pattern is that it makes the agent's reasoning explicit. The series of Thoughts, Actions, and Observations forms a **reasoning trace**. This trace is our primary tool for debugging. If the agent gets stuck or makes a mistake, we can simply read the trace to understand why. It's like looking at a stack trace for an agent.

Here's an example of what a reasoning trace might look like for a research question:

**Question:** Who was the CEO of OpenAI when GPT-3 was released?

**Trace:**

**Thought:** I need to find out when GPT-3 was released and who the CEO of OpenAI was at that time. I'll start by searching for the release date of GPT-3.
**Action:** `search(query="GPT-3 release date")`
**Observation:** GPT-3 was released in June 2020.

**Thought:** Now that I know GPT-3 was released in June 2020, I need to find out who the CEO of OpenAI was at that time. I'll search for "OpenAI CEO June 2020".
**Action:** `search(query="OpenAI CEO June 2020")`
**Observation:** Sam Altman was the CEO of OpenAI in June 2020.

**Thought:** I have found the answer. The CEO of OpenAI when GPT-3 was released was Sam Altman.
**Final Answer:** Sam Altman

This trace is a clear, step-by-step record of the agent's reasoning process. It's incredibly valuable for understanding and debugging agent behavior.

## Project: Build a Research Agent

Your project for this module is to build an agent that can answer complex research questions by searching the web. This will bring together everything we've learned so far: tool use, memory, and now, planning.

You'll need to:

1.  **Implement a `search` tool.** You can use a real search API (like Google or Bing) or just a mock function that returns pre-defined results for specific queries.
2.  **Update your agent to use the ReAct pattern.** This will involve modifying your system prompt and your agent loop to handle the Thought/Action/Observation format.
3.  **Give your agent a complex research question** that requires multiple steps to answer (e.g., "What was the most popular programming language in the year the first iPhone was released?").
4.  **Print out the full reasoning trace** as the agent works through the problem. This is your primary debugging tool.

This project will be challenging. You'll likely run into issues with prompt engineering, parsing the LLM's output, and handling unexpected tool results. This is normal. This is where the real learning happens. Embrace the struggle. Be patient. Pay attention to the details. And most importantly, visualize everything.

In the next module, we'll look at how to orchestrate more complex, multi-step workflows. But a solid understanding of the ReAct pattern is the prerequisite for everything that follows. Master this, and you'll be well on your way to building truly intelligent agents.

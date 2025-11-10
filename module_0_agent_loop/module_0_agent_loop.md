# Module 0: The Agent Loop - Building Your First Agent

**A Course by "Andrej Karpathy" Style Teaching**

---

Welcome. In this first module, we're going to do something that might seem a little counterintuitive. We're going to build an AI agent without using any fancy frameworks, libraries, or even a GPU. We're going to write about 50 lines of plain Python to build a system that can reason, act, and learn from its environment. Why? Because the most common failure mode I see in this field is what I call "premature abstraction." Developers jump into complex frameworks like LangChain or AutoGen without a fundamental, first-principles understanding of what's actually happening. And when things go wrong—which they always do—they're completely lost. Neural nets, and by extension agent systems, are leaky abstractions. They fail silently and in the most unexpected ways. The only way to debug them is to have a deep, intuitive understanding of the underlying mechanics.

So, we're going to start with the absolute basics. We're going to build an agent from scratch. We're going to watch it fail. We're going to understand *why* it fails. And then, and only then, will we start to add complexity. This is the Karpathy way. Patience, attention to detail, and a healthy dose of paranoia. Let's get started.

## What is an Agent? (Not What You Think)

Forget the science fiction image of a digital butler. At its core, an agent is a very simple concept: it's a loop. That's it. A loop that performs three steps over and over again:

1.  **Think:** The agent observes its current state and decides what to do next.
2.  **Act:** The agent takes an action in its environment.
3.  **Observe:** The agent sees the result of its action.

This is often called the **Reason-Act (ReAct)** loop. Everything else—tool use, memory, multi-agent systems—is just an elaboration on this fundamental cycle. If you understand this loop, you understand 90% of what makes an agent tick.

Let's formalize this a bit. An agent has a **goal**. It exists in an **environment**. It can take a set of **actions**. It receives **observations** from the environment. Its job is to choose actions that will lead it closer to its goal. The "thinking" part is where the Large Language Model (LLM) comes in. The LLM is the agent's brain. It takes the current state and the history of observations and decides on the next action.

## Building a 50-Line Agent from Scratch

Talk is cheap. Let's build one. We're going to build a simple agent that can solve basic arithmetic problems. The only tool it will have is a Python interpreter. This is a classic example, but we're going to build it from the ground up to really understand what's going on.

Here's the entire agent in about 50 lines of Python. We'll use the OpenAI API for our LLM, but you could use any model.

```python
import openai
import re

# You'll need to set your OPENAI_API_KEY environment variable
client = openai.OpenAI()

def execute_python(code: str) -> str:
    """Executes a string of Python code and returns the output."""
    try:
        # WARNING: This is a security risk. Only run trusted code.
        # In a real application, you would use a sandboxed environment.
        result = str(eval(code))
        return result
    except Exception as e:
        return str(e)

def agent(prompt: str, max_iterations: int = 5) -> str:
    """A simple agent that can solve math problems."""
    # The agent's internal state is just a list of messages
    messages = [{"role": "user", "content": prompt}]
    
    for i in range(max_iterations):
        print(f"--- Iteration {i+1} ---")
        
        # 1. Think
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=messages
        )
        response_text = response.choices[0].message.content
        messages.append({"role": "assistant", "content": response_text})
        print(f"Assistant: {response_text}")

        # 2. Act
        # Check if the assistant wants to execute code
        code_match = re.search(r"```python\n(.*?)\n```", response_text, re.DOTALL)
        if code_match:
            code = code_match.group(1)
            print(f"Executing code: {code}")
            
            # 3. Observe
            observation = execute_python(code)
            print(f"Observation: {observation}")
            messages.append({"role": "user", "content": f"Observation: {observation}"}) # In ReAct, this is a tool role
        else:
            # If no code to execute, the agent is done
            return response_text

    return "Agent reached maximum iterations."

if __name__ == "__main__":
    # Let's give it a problem
    problem = "What is (3 * 4) + (5 - 2)? And then what is that number squared?"
    result = agent(problem)
    print(f"\n--- Final Answer ---\
{result}")

```

Let's break this down. The `agent` function is our main loop. The `messages` list is the agent's entire world. It's the history of everything that's happened. In each iteration, we call the LLM (`Think`), check if it produced code to run (`Act`), and if so, execute it and feed the result back into the message history (`Observe`). That's it. That's the core of every agent system.

## Why Agents Fail Silently

Now, let's talk about why this is so fragile. What if the LLM produces code that doesn't work? What if it gets stuck in a loop? What if the regular expression fails to find the code block? Our simple agent has no good way to handle these failures. It will just keep trying until it hits the `max_iterations` limit. This is a silent failure. The agent doesn't crash; it just doesn't produce the right answer.

In a more complex system, these silent failures are a nightmare to debug. The problem could be in the prompt, the model, the tools, or the orchestration logic. Without a deep understanding of the agent loop, you're just shooting in the dark. This is why we start here. By building from scratch, you develop an intuition for where things can go wrong.

## Visualizing Agent Reasoning

How do we debug these systems? The most powerful tool we have is visualization. We need to be able to see the agent's "thoughts" at each step. In our simple agent, we're just printing the messages to the console. This is the most basic form of visualization. Let's look at the output for our problem:

```
--- Iteration 1 ---
Assistant: Okay, let's break this down.

First, I'll calculate (3 * 4) + (5 - 2).
```python
print((3 * 4) + (5 - 2))
```
Executing code: print((3 * 4) + (5 - 2))
Observation: 15
--- Iteration 2 ---
Assistant: The result of the first part is 15.

Now, I'll square that number.
```python
print(15**2)
```
Executing code: print(15**2)
Observation: 225
--- Iteration 3 ---
Assistant: The final answer is 225.

--- Final Answer ---
The final answer is 225.
```

By reading this trace, we can follow the agent's reasoning step-by-step. We see it correctly break the problem down, execute the first part, get the result, and then execute the second part. This is the key to debugging agent systems. If the agent had made a mistake, we would see it in this trace. In more advanced systems, we'll use more sophisticated visualization tools, but the principle is the same: **make the agent's reasoning visible**.

## Project: Build a Calculator Agent

Now it's your turn. Take the code from this module and extend it. Here are some ideas:

1.  **Add more tools:** Give your agent tools for addition, subtraction, multiplication, and division as separate functions. See how the LLM chooses which tool to use.
2.  **Improve the prompting:** The current prompt is very simple. Experiment with different system prompts to make the agent more reliable.
3.  **Handle errors:** What happens if the agent tries to divide by zero? Modify the `execute_python` function to return a more informative error message and see how the agent reacts.
4.  **Implement a better stopping condition:** The current agent stops when it doesn't produce code. Can you think of a more robust way to determine when the agent has finished its task?

Spend time with this simple agent. Break it. Fix it. Understand its limitations. This is the most important step in your journey to becoming an expert in agent systems. In the next module, we'll dive deeper into tool use and build a more sophisticated system for managing and calling tools. But for now, become one with the loop.

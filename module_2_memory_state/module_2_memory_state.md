# Module 2: Memory and State - Making Agents Stateful

**A Course by "Andrej Karpathy" Style Teaching**

---

So far, our agent has a significant limitation: it's stateless. Every time we run it, it starts from a blank slate. It has no memory of past conversations or interactions. This is like having a conversation with someone who has severe amnesia; you have to re-explain everything every few seconds. To build agents that can engage in coherent, multi-turn conversations, we need to give them **memory**.

In the context of agent systems, "memory" is just a fancy word for **state management**. It's the process of storing and retrieving information from past turns of the conversation. This is one of the most critical and often overlooked aspects of building robust agents. As we've seen, neural nets fail silently, and memory systems are no exception. A bug in your memory implementation won't crash your program; it will just cause your agent to behave in strange and unpredictable ways. So, as always, we're going to be thorough, defensive, and paranoid. We're going to build our memory system from scratch.

## Why Agents Need Memory

At a high level, agents need memory for two reasons:

1.  **To maintain context:** In a multi-turn conversation, the agent needs to remember what was said earlier to understand the user's current intent. For example, if a user says, "What about in London?", the agent needs to remember that the previous question was about the weather.
2.  **To learn from experience:** An agent can improve its performance over time by remembering which actions led to successful outcomes and which did not. This is a more advanced topic that we'll touch on later, but the foundation is a solid memory system.

There are many different types of memory, but we're going to focus on the most fundamental: **conversation history**.

## Building a Conversation Buffer from Scratch

The simplest form of memory is just to store the entire history of messages. This is what we've been doing so far in our simple agent. The `messages` list is a basic **conversation buffer**. For short conversations, this works surprisingly well. The LLM can use the full context of the conversation to generate its next response.

However, this approach has a major drawback: it's not scalable. LLMs have a finite context window. If the conversation gets too long, we'll exceed the context limit and get an error. We need a more sophisticated way to manage the conversation history.

## Implementing Sliding Window Memory

One common technique is to use a **sliding window**. Instead of sending the entire message history to the LLM, we only send the most recent `k` messages. This is a simple and effective way to keep the context size under control. Let's build a `Memory` class that implements this.

```python
class Memory:
    def __init__(self, window_size: int = 10):
        self.messages = []
        self.window_size = window_size

    def add_message(self, role: str, content: str):
        """Adds a message to the memory."""
        self.messages.append({"role": role, "content": content})

    def get_messages(self) -> list:
        """Retrieves the messages within the current window."""
        # This is a simple sliding window implementation
        return self.messages[-self.window_size:]

    def clear(self):
        """Clears the memory."""
        self.messages = []
```

This is a very basic implementation, but it illustrates the core idea. We can now integrate this `Memory` class into our agent. In each iteration, instead of appending to a local `messages` list, we'll add messages to our `memory` object and then use `memory.get_messages()` to retrieve the current context for the LLM.

## Vector Memory for Long-Term Recall

Sliding window memory is good for maintaining short-term context, but what about long-term memory? What if the agent needs to remember something from the beginning of a very long conversation? This is where **vector memory** comes in. The idea is to embed the messages into a vector space and then use a vector database to retrieve the most relevant messages based on the current query. This is a more advanced technique, but it's a powerful way to give your agent a long-term memory.

We won't implement a full vector memory system from scratch in this module, as it involves setting up a vector database like Pinecone or Chroma. However, the principle is simple: when a new message comes in, you embed it and store it in the database. When you need to retrieve relevant context, you embed the current query and perform a similarity search on the database. This is a powerful pattern that we'll explore in more detail in a later module.

## Project: Build a Customer Service Agent

Your project for this module is to build a customer service agent that can handle a multi-turn conversation. The agent should be able to remember the user's name, their order number, and the nature of their problem.

You'll need to:

1.  **Implement the `Memory` class** with a sliding window.
2.  **Integrate the `Memory` class** into your agent from Module 1.
3.  **Give your agent a personality** through the system prompt. It should be a helpful and patient customer service representative.
4.  **Test your agent** with a simulated customer service conversation. See if it can remember the user's information across multiple turns. For example:
    *   User: "Hi, my name is John."
    *   Agent: "Hello John, how can I help you today?"
    *   User: "I have a problem with my order."
    *   Agent: "I can help with that. What is your order number?"
    *   User: "It's 12345."
    *   Agent: "Thank you, John. I'm looking up order number 12345 now. What seems to be the problem?"

As you work on this project, think about the limitations of sliding window memory. What happens if the user's name is mentioned outside of the window? How could you solve this problem? These are the kinds of questions that will lead you to a deeper understanding of agent memory systems.

In the next module, we'll dive into the ReAct pattern and build a more sophisticated agent that can plan and reason about its actions. But first, make sure you have a solid understanding of how to manage state. It's the foundation of any non-trivial agent.

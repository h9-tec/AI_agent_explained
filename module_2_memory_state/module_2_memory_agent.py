# Module 2: Memory and State - Making Agents Stateful
# This module implements a memory system for agents to maintain conversation history.

import openai
import json
from typing import List, Dict

# Initialize the OpenAI client
client = openai.OpenAI()


class Memory:
    """
    A simple memory system for agents.
    Implements a sliding window to keep the context size manageable.
    """
    def __init__(self, window_size: int = 10, system_prompt: str = ""):
        self.messages = []
        self.window_size = window_size
        self.system_prompt = system_prompt
        
        # If a system prompt is provided, add it as the first message
        if system_prompt:
            self.messages.append({"role": "system", "content": system_prompt})

    def add_message(self, role: str, content: str, **kwargs):
        """Adds a message to the memory."""
        message = {"role": role, "content": content}
        message.update(kwargs)  # Add any additional fields (like tool_call_id)
        self.messages.append(message)

    def get_messages(self) -> List[Dict]:
        """
        Retrieves the messages within the current window.
        Always includes the system prompt if it exists.
        """
        if not self.messages:
            return []
        
        # If we have a system prompt, always include it
        if self.messages[0]["role"] == "system":
            system_msg = [self.messages[0]]
            recent_messages = self.messages[1:][-self.window_size:]
            return system_msg + recent_messages
        else:
            return self.messages[-self.window_size:]

    def clear(self):
        """Clears the memory, keeping only the system prompt if it exists."""
        if self.messages and self.messages[0]["role"] == "system":
            system_msg = self.messages[0]
            self.messages = [system_msg]
        else:
            self.messages = []

    def get_full_history(self) -> List[Dict]:
        """Returns the complete message history (for debugging)."""
        return self.messages.copy()


class StatefulAgent:
    """
    An agent with memory that can maintain context across multiple interactions.
    """
    def __init__(self, system_prompt: str, window_size: int = 10):
        self.memory = Memory(window_size=window_size, system_prompt=system_prompt)
        self.model = "gpt-4.1-mini"

    def chat(self, user_message: str) -> str:
        """
        Processes a user message and returns the agent's response.
        The conversation history is maintained in memory.
        """
        # Add the user's message to memory
        self.memory.add_message("user", user_message)
        
        # Get the current context window
        messages = self.memory.get_messages()
        
        print(f"\n[DEBUG] Sending {len(messages)} messages to LLM")
        
        # Call the LLM
        response = client.chat.completions.create(
            model=self.model,
            messages=messages
        )
        
        assistant_message = response.choices[0].message.content
        
        # Add the assistant's response to memory
        self.memory.add_message("assistant", assistant_message)
        
        return assistant_message

    def reset(self):
        """Resets the agent's memory."""
        self.memory.clear()
        print("[INFO] Memory has been reset.")


def customer_service_demo():
    """
    A demo of a customer service agent with memory.
    This agent can remember information across multiple turns.
    """
    system_prompt = """You are a helpful and patient customer service representative for TechCorp, 
    an online electronics store. You should:
    - Be polite and professional
    - Remember information the customer tells you (like their name, order number, etc.)
    - Help resolve their issues
    - Ask clarifying questions when needed
    
    When the customer provides their order number, acknowledge it and say you're looking it up.
    """
    
    agent = StatefulAgent(system_prompt=system_prompt, window_size=10)
    
    print("=== Customer Service Agent Demo ===")
    print("Type 'quit' to exit, 'reset' to clear memory, or 'history' to see full conversation.\n")
    
    while True:
        user_input = input("Customer: ")
        
        if user_input.lower() == 'quit':
            print("Goodbye!")
            break
        elif user_input.lower() == 'reset':
            agent.reset()
            continue
        elif user_input.lower() == 'history':
            print("\n[FULL CONVERSATION HISTORY]")
            for i, msg in enumerate(agent.memory.get_full_history()):
                print(f"{i+1}. {msg['role']}: {msg['content'][:100]}...")
            print()
            continue
        
        # Get the agent's response
        response = agent.chat(user_input)
        print(f"Agent: {response}\n")


def memory_test():
    """
    A test to demonstrate how sliding window memory works.
    """
    print("=== Memory Sliding Window Test ===\n")
    
    # Create a memory with a very small window size
    memory = Memory(window_size=3, system_prompt="You are a helpful assistant.")
    
    # Add several messages
    memory.add_message("user", "Message 1")
    memory.add_message("assistant", "Response 1")
    memory.add_message("user", "Message 2")
    memory.add_message("assistant", "Response 2")
    memory.add_message("user", "Message 3")
    memory.add_message("assistant", "Response 3")
    memory.add_message("user", "Message 4")
    
    print("Full history:")
    for msg in memory.get_full_history():
        print(f"  {msg['role']}: {msg['content']}")
    
    print(f"\nCurrent window (size={memory.window_size}):")
    for msg in memory.get_messages():
        print(f"  {msg['role']}: {msg['content']}")
    
    print("\nNotice how the system prompt is always included,")
    print("but only the most recent messages are in the window.")


if __name__ == "__main__":
    # Run the memory test first to understand how it works
    memory_test()
    
    print("\n" + "="*50 + "\n")
    
    # Then run the customer service demo
    customer_service_demo()

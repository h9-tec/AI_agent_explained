# Advanced Example: A Complete Agent System
# This combines all concepts from Modules 0-3: Agent loop, tools, memory, and ReAct pattern

import openai
import json
import re
from typing import Optional, Tuple, List, Dict
from datetime import datetime

client = openai.OpenAI()


class ToolRegistry:
    """Manages tools that the agent can use."""
    
    def __init__(self):
        self.tools = {}
    
    def register(self, func):
        """Decorator to register a tool."""
        self.tools[func.__name__] = func
        return func
    
    def get_openai_schema(self):
        """Generate OpenAI function calling schema."""
        import inspect
        schemas = []
        
        for name, func in self.tools.items():
            sig = inspect.signature(func)
            doc = inspect.getdoc(func) or "No description"
            
            parameters = {
                "type": "object",
                "properties": {},
                "required": []
            }
            
            for param_name, param in sig.parameters.items():
                parameters["properties"][param_name] = {
                    "type": "string",
                    "description": f"The {param_name} parameter"
                }
                if param.default == inspect.Parameter.empty:
                    parameters["required"].append(param_name)
            
            schemas.append({
                "type": "function",
                "function": {
                    "name": name,
                    "description": doc.split('\n')[0],
                    "parameters": parameters
                }
            })
        
        return schemas
    
    def call(self, name: str, args: dict) -> str:
        """Execute a tool."""
        if name not in self.tools:
            return f"Error: Tool '{name}' not found"
        try:
            return str(self.tools[name](**args))
        except Exception as e:
            return f"Error: {str(e)}"


class Memory:
    """Manages conversation history with sliding window."""
    
    def __init__(self, window_size: int = 10):
        self.messages = []
        self.window_size = window_size
    
    def add(self, role: str, content: str, **kwargs):
        """Add a message to memory."""
        msg = {"role": role, "content": content}
        msg.update(kwargs)
        self.messages.append(msg)
    
    def get_window(self) -> List[Dict]:
        """Get recent messages within window."""
        if not self.messages:
            return []
        
        # Always include system message if present
        if self.messages[0]["role"] == "system":
            return [self.messages[0]] + self.messages[1:][-self.window_size:]
        return self.messages[-self.window_size:]
    
    def get_all(self) -> List[Dict]:
        """Get complete history."""
        return self.messages.copy()


class AdvancedAgent:
    """
    A complete agent that combines:
    - Tool use (Module 1)
    - Memory management (Module 2)
    - ReAct reasoning pattern (Module 3)
    """
    
    def __init__(self, tools: ToolRegistry, system_prompt: str, window_size: int = 10):
        self.tools = tools
        self.memory = Memory(window_size)
        self.model = "gpt-4.1-mini"
        
        # Add system prompt to memory
        self.memory.add("system", system_prompt)
        
        # Statistics
        self.stats = {
            "total_iterations": 0,
            "tool_calls": 0,
            "tokens_used": 0,
            "start_time": None
        }
    
    def run(self, user_input: str, max_iterations: int = 10, verbose: bool = True) -> str:
        """
        Run the agent with a user query.
        Uses ReAct pattern with tool calling.
        """
        self.stats["start_time"] = datetime.now()
        
        # Add user input to memory
        self.memory.add("user", user_input)
        
        if verbose:
            print(f"\n{'='*80}")
            print(f"User: {user_input}")
            print(f"{'='*80}\n")
        
        # Main agent loop
        for iteration in range(max_iterations):
            self.stats["total_iterations"] += 1
            
            if verbose:
                print(f"--- Iteration {iteration + 1} ---\n")
            
            # Get current context window
            messages = self.memory.get_window()
            
            # Call LLM with tools
            response = client.chat.completions.create(
                model=self.model,
                messages=messages,
                tools=self.tools.get_openai_schema(),
                tool_choice="auto",
                temperature=0
            )
            
            message = response.choices[0].message
            self.memory.add("assistant", message.content or "", tool_calls=message.tool_calls)
            
            if verbose and message.content:
                print(f"Assistant: {message.content}\n")
            
            # Check for tool calls
            if message.tool_calls:
                if verbose:
                    print(f"→ Calling {len(message.tool_calls)} tool(s):\n")
                
                for tool_call in message.tool_calls:
                    tool_name = tool_call.function.name
                    tool_args = json.loads(tool_call.function.arguments)
                    
                    if verbose:
                        print(f"  • {tool_name}({tool_args})")
                    
                    # Execute tool
                    result = self.tools.call(tool_name, tool_args)
                    self.stats["tool_calls"] += 1
                    
                    if verbose:
                        print(f"    → Result: {result}\n")
                    
                    # Add tool result to memory
                    self.memory.add(
                        "tool",
                        result,
                        tool_call_id=tool_call.id,
                        name=tool_name
                    )
            else:
                # No tool calls, agent is done
                if verbose:
                    print(f"\n{'='*80}")
                    print(f"✓ Task completed in {iteration + 1} iterations")
                    print(f"{'='*80}\n")
                
                return message.content
        
        # Max iterations reached
        if verbose:
            print(f"\n{'='*80}")
            print(f"⚠ Reached maximum iterations ({max_iterations})")
            print(f"{'='*80}\n")
        
        return "Task incomplete: reached maximum iterations"
    
    def get_stats(self) -> dict:
        """Get agent statistics."""
        if self.stats["start_time"]:
            elapsed = (datetime.now() - self.stats["start_time"]).total_seconds()
            self.stats["elapsed_seconds"] = elapsed
        return self.stats.copy()
    
    def reset(self):
        """Reset the agent's memory."""
        system_msg = self.memory.messages[0] if self.memory.messages else None
        self.memory = Memory(self.memory.window_size)
        if system_msg:
            self.memory.messages.append(system_msg)
        
        self.stats = {
            "total_iterations": 0,
            "tool_calls": 0,
            "tokens_used": 0,
            "start_time": None
        }


# Create and register tools
registry = ToolRegistry()


@registry.register
def search(query: str) -> str:
    """Search the internet for information."""
    # Mock search results
    knowledge = {
        "python": "Python is a high-level programming language created by Guido van Rossum in 1991.",
        "agents": "AI agents are systems that can independently accomplish tasks using LLMs, tools, and reasoning.",
        "openai": "OpenAI is an AI research company founded in 2015, known for GPT models and ChatGPT.",
        "react": "ReAct (Reason + Act) is an agent pattern that combines reasoning traces with action execution.",
    }
    
    query_lower = query.lower()
    for key, value in knowledge.items():
        if key in query_lower:
            return value
    
    return f"No specific information found for '{query}'. Try searching for: python, agents, openai, or react."


@registry.register
def calculate(expression: str) -> str:
    """Evaluate a mathematical expression."""
    try:
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Calculation error: {str(e)}"


@registry.register
def get_time() -> str:
    """Get the current time."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@registry.register
def save_note(content: str) -> str:
    """Save a note to memory (simulated)."""
    # In a real system, this would save to a database
    return f"Note saved: '{content[:50]}...'" if len(content) > 50 else f"Note saved: '{content}'"


# Example usage
if __name__ == "__main__":
    system_prompt = """You are a helpful AI assistant with access to various tools.

You should:
1. Think step by step about how to answer the user's question
2. Use tools when you need external information or capabilities
3. Provide clear, accurate answers
4. Be concise but thorough

When you need to use a tool, just call it - the system will execute it and provide the result.
"""
    
    agent = AdvancedAgent(
        tools=registry,
        system_prompt=system_prompt,
        window_size=10
    )
    
    # Example 1: Simple query
    print("\n" + "#"*80)
    print("# Example 1: Information Retrieval")
    print("#"*80)
    
    result = agent.run("What is Python? Also, what time is it right now?")
    print(f"\nFinal Answer: {result}")
    
    # Show statistics
    stats = agent.get_stats()
    print(f"\nStatistics:")
    print(f"  - Iterations: {stats['total_iterations']}")
    print(f"  - Tool calls: {stats['tool_calls']}")
    print(f"  - Time: {stats.get('elapsed_seconds', 0):.2f}s")
    
    # Example 2: Multi-step reasoning
    print("\n\n" + "#"*80)
    print("# Example 2: Multi-Step Calculation")
    print("#"*80)
    
    agent.reset()  # Reset for new conversation
    
    result = agent.run(
        "Calculate (123 * 456) + (789 - 321), then tell me if that number is divisible by 3."
    )
    print(f"\nFinal Answer: {result}")
    
    stats = agent.get_stats()
    print(f"\nStatistics:")
    print(f"  - Iterations: {stats['total_iterations']}")
    print(f"  - Tool calls: {stats['tool_calls']}")
    print(f"  - Time: {stats.get('elapsed_seconds', 0):.2f}s")
    
    # Example 3: Interactive mode
    print("\n\n" + "#"*80)
    print("# Example 3: Interactive Mode")
    print("#"*80)
    print("\nType 'quit' to exit, 'reset' to clear memory, 'stats' to see statistics\n")
    
    agent.reset()
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() == 'quit':
                print("Goodbye!")
                break
            elif user_input.lower() == 'reset':
                agent.reset()
                print("Memory reset.")
                continue
            elif user_input.lower() == 'stats':
                stats = agent.get_stats()
                print(f"\nAgent Statistics:")
                for key, value in stats.items():
                    print(f"  {key}: {value}")
                continue
            elif not user_input:
                continue
            
            result = agent.run(user_input, verbose=True)
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {str(e)}")

# Module 3: Planning and Reasoning - ReAct Pattern Deep Dive (llama.cpp version)
# This module implements the ReAct (Reason + Act) pattern from scratch.

import re
from typing import Optional, Tuple
from llm_client import UnifiedClient
from config import config

# Initialize the unified client
client = UnifiedClient()


class ReActAgent:
    """
    An agent that implements the ReAct (Reason + Act) pattern.
    The agent explicitly reasons about its actions before taking them.
    Works with both OpenAI and llama.cpp backends.
    """
    
    def __init__(self, tools: dict, max_iterations: int = 10):
        """
        Initialize the ReAct agent.
        
        Args:
            tools: A dictionary mapping tool names to functions
            max_iterations: Maximum number of reasoning cycles
        """
        self.tools = tools
        self.max_iterations = max_iterations
        
        # Build the tool descriptions for the prompt
        tool_descriptions = []
        for name, func in tools.items():
            doc = func.__doc__ or "No description available"
            tool_descriptions.append(f"- {name}: {doc.strip()}")
        self.tool_descriptions = "\n".join(tool_descriptions)

    def _create_system_prompt(self) -> str:
        """Creates the system prompt that explains the ReAct format."""
        return f"""You are a helpful assistant that solves problems step by step.

You have access to the following tools:
{self.tool_descriptions}

To solve the problem, you MUST use the following format:

Thought: [Your reasoning about what to do next]
Action: [The tool to use, in the format: tool_name(arg1="value1", arg2="value2")]
Observation: [The result will be provided by the system]

You can repeat the Thought/Action/Observation cycle as many times as needed.

When you have enough information to answer the question, use this format:

Thought: I now have all the information needed to answer the question.
Final Answer: [Your final answer to the original question]

Important:
- Always start with a Thought
- Only use tools that are available
- Be specific in your reasoning
- When you have the answer, provide a Final Answer
"""

    def _parse_action(self, text: str) -> Optional[Tuple[str, dict]]:
        """
        Parses an action from the agent's output.
        
        Returns:
            A tuple of (tool_name, arguments) or None if no action found
        """
        # Look for the Action: line
        action_match = re.search(r"Action:\s*(\w+)\((.*?)\)", text, re.DOTALL)
        if not action_match:
            return None
        
        tool_name = action_match.group(1)
        args_str = action_match.group(2)
        
        # Parse the arguments (simple key="value" format)
        args = {}
        for arg_match in re.finditer(r'(\w+)="([^"]*)"', args_str):
            key = arg_match.group(1)
            value = arg_match.group(2)
            args[key] = value
        
        return tool_name, args

    def _execute_tool(self, tool_name: str, args: dict) -> str:
        """Executes a tool and returns the result."""
        if tool_name not in self.tools:
            return f"Error: Tool '{tool_name}' not found. Available tools: {list(self.tools.keys())}"
        
        try:
            result = self.tools[tool_name](**args)
            return str(result)
        except Exception as e:
            return f"Error executing {tool_name}: {str(e)}"

    def run(self, question: str) -> str:
        """
        Runs the ReAct agent on a question.
        
        Returns:
            The final answer or an error message
        """
        # Initialize the conversation
        messages = [
            {"role": "system", "content": self._create_system_prompt()},
            {"role": "user", "content": question}
        ]
        
        reasoning_trace = []
        
        print(f"Question: {question}\n")
        print("=" * 80)
        
        for iteration in range(self.max_iterations):
            print(f"\n--- Iteration {iteration + 1} ---\n")
            
            # Get the agent's response
            response = client.chat.completions.create(
                model="",  # Model determined by config
                messages=messages,
                temperature=0,  # Use deterministic output for debugging
                max_tokens=config.LLAMA_MAX_TOKENS if config.LLM_BACKEND == "llamacpp" else None
            )
            
            agent_output = response.choices[0].message.content
            messages.append({"role": "assistant", "content": agent_output})
            
            print(agent_output)
            reasoning_trace.append(agent_output)
            
            # Check if we have a final answer
            if "Final Answer:" in agent_output:
                # Extract the final answer
                final_answer_match = re.search(r"Final Answer:\s*(.+)", agent_output, re.DOTALL)
                if final_answer_match:
                    final_answer = final_answer_match.group(1).strip()
                    print("\n" + "=" * 80)
                    print(f"\n✓ Task completed in {iteration + 1} iterations")
                    return final_answer
            
            # Parse and execute the action
            action = self._parse_action(agent_output)
            if action:
                tool_name, args = action
                print(f"\n→ Executing: {tool_name}({args})")
                
                # Execute the tool
                observation = self._execute_tool(tool_name, args)
                print(f"← Observation: {observation}\n")
                
                # Add the observation to the conversation
                observation_message = f"Observation: {observation}"
                messages.append({"role": "user", "content": observation_message})
                reasoning_trace.append(observation_message)
            else:
                # No action found and no final answer - something went wrong
                print("\n⚠ Warning: No action or final answer found in agent output")
                break
        
        print("\n" + "=" * 80)
        print(f"\n✗ Agent reached maximum iterations ({self.max_iterations})")
        return "Failed to find an answer within the iteration limit."


# Define some example tools for the agent

def search(query: str) -> str:
    """Searches the internet for information about a query."""
    # This is a mock search function. In a real implementation,
    # you would call a search API like Google or Bing.
    
    query_lower = query.lower()
    
    # Mock database of facts
    knowledge_base = {
        "gpt-3 release": "GPT-3 was released by OpenAI in June 2020.",
        "openai ceo": "Sam Altman is the CEO of OpenAI (as of 2020-2024).",
        "first iphone": "The first iPhone was released by Apple on June 29, 2007.",
        "python release": "Python was first released in 1991 by Guido van Rossum.",
        "popular language 2007": "According to the TIOBE index, Java was the most popular programming language in 2007.",
        "eiffel tower height": "The Eiffel Tower is 330 meters (1,083 feet) tall including antennas.",
        "paris population": "Paris has a population of approximately 2.2 million people in the city proper.",
    }
    
    # Find matching facts
    for key, value in knowledge_base.items():
        if key in query_lower:
            return value
    
    return f"No specific information found for '{query}'. Try rephrasing your search."


def calculate(expression: str) -> str:
    """Evaluates a mathematical expression."""
    try:
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"


def get_current_year() -> str:
    """Returns the current year."""
    return "2024"


if __name__ == "__main__":
    # Validate configuration
    try:
        config.validate()
        config.print_config()
    except Exception as e:
        print(f"\n✗ Configuration error: {e}")
        print("\nPlease check your .env file and model setup.")
        exit(1)
    
    print("\n" + "=" * 80)
    print("Module 3: ReAct Agent with llama.cpp")
    print("=" * 80 + "\n")
    
    # Create a ReAct agent with some tools
    tools = {
        "search": search,
        "calculate": calculate,
        "get_current_year": get_current_year,
    }
    
    agent = ReActAgent(tools=tools, max_iterations=10)
    
    # Test with a complex question that requires multiple steps
    questions = [
        "What was the most popular programming language in the year the first iPhone was released?",
        "Who was the CEO of OpenAI when GPT-3 was released?",
        "How many years ago was the first iPhone released? (Use get_current_year tool)",
    ]
    
    for i, question in enumerate(questions, 1):
        print(f"\n\n{'#' * 80}")
        print(f"# Example {i}")
        print(f"{'#' * 80}\n")
        
        answer = agent.run(question)
        
        print(f"\n{'=' * 80}")
        print(f"FINAL ANSWER: {answer}")
        print(f"{'=' * 80}")
        
        if i < len(questions):
            input("\nPress Enter to continue to the next example...")


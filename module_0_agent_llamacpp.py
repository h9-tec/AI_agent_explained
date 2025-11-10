# Module 0: The Agent Loop - Adapted for llama.cpp
# This is the same agent as module_0_agent.py, but using llama.cpp instead of OpenAI

import re
from llm_client import UnifiedClient
from config import config

# Initialize the unified client (will use llama.cpp or OpenAI based on config)
client = UnifiedClient()


def execute_python(code: str) -> str:
    """Executes a string of Python code and returns the output."""
    try:
        # WARNING: This is a security risk. Only run trusted code.
        # In a real application, you would use a sandboxed environment like a Docker container.
        # The `eval` function can execute any code, so it's dangerous if the LLM is compromised.
        result = str(eval(code))
        return result
    except Exception as e:
        # If the code fails, we return the error message to the agent.
        # This allows the agent to debug and correct its own code.
        return str(e)


def agent(prompt: str, max_iterations: int = 5) -> str:
    """A simple agent that can solve math problems by writing and executing Python code."""
    
    # The agent's entire world is its message history.
    # We start with a system prompt to set the context and a user prompt with the problem.
    messages = [
        {
            "role": "system", 
            "content": """You are a helpful AI assistant that can solve math problems. 
            You can use a Python interpreter to help you. 
            When you need to execute code, enclose it in ```python\n...\n``` blocks. 
            I will execute the code for you and return the observation. 
            Once you have the final answer, just state it without any code blocks."""
        },
        {"role": "user", "content": prompt}
    ]
    
    # This is the main agent loop.
    for i in range(max_iterations):
        print(f"\n--- Iteration {i+1} ---")
        
        # 1. THINK: The LLM decides what to do next.
        # We send the entire message history to the LLM.
        print("Thinking...")
        response = client.chat.completions.create(
            model="",  # Model is determined by config
            messages=messages,
            temperature=config.LLAMA_TEMPERATURE,
            max_tokens=config.LLAMA_MAX_TOKENS
        )
        response_text = response.choices[0].message.content
        
        # We add the assistant's response to the message history.
        messages.append({"role": "assistant", "content": response_text})
        print(f"Assistant: {response_text}")

        # 2. ACT: The agent checks if it should take an action (execute code).
        # We use a simple regex to find a Python code block in the assistant's response.
        code_match = re.search(r"```python\n(.*?)\n```", response_text, re.DOTALL)
        
        if code_match:
            # If a code block is found, we execute it.
            code = code_match.group(1)
            print(f"Executing code: \n---\n{code}\n---")
            
            # 3. OBSERVE: The agent gets the result of its action.
            observation = execute_python(code)
            print(f"Observation: {observation}")
            
            # We add the observation back into the message history for the next iteration.
            # This is how the agent learns from its actions.
            messages.append({"role": "user", "content": f"Observation: {observation}"})
        else:
            # If no code block is found, the agent has likely finished.
            # We can return its final response.
            print("No code to execute. Agent has finished.")
            return response_text

    # If the agent reaches the maximum number of iterations, it stops.
    return "Agent reached maximum iterations without a final answer."


if __name__ == "__main__":
    # Validate configuration
    try:
        config.validate()
        config.print_config()
    except Exception as e:
        print(f"\n✗ Configuration error: {e}")
        print("\nPlease check your .env file and ensure:")
        print("1. LLM_BACKEND is set to 'llamacpp' or 'openai'")
        print("2. If using llamacpp, LLAMA_MODEL_PATH points to a valid GGUF model")
        print("3. If using openai, OPENAI_API_KEY is set")
        exit(1)
    
    print("\n" + "=" * 80)
    print("Module 0: Agent Loop with llama.cpp")
    print("=" * 80 + "\n")
    
    # Let's give the agent a multi-step problem to solve.
    problem = "What is the result of (123 * 4) + (567 - 89)? After that, what is that number squared?"
    
    # Run the agent.
    final_result = agent(problem)
    
    # Print the final answer.
    print(f"\n--- Final Answer ---\n{final_result}")


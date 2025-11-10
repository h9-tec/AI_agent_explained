# Module 1: Tool Use - Teaching Agents to Use APIs (llama.cpp version)
# This module implements a proper tool registry and an agent that can use multiple tools.

import json
import inspect
from llm_client import UnifiedClient
from config import config

# Initialize the unified client
client = UnifiedClient()


class ToolRegistry:
    """
    A registry for managing tools (functions) that an agent can use.
    This class handles registration, schema generation, and tool execution.
    """
    def __init__(self):
        self.tools = {}

    def register(self, func):
        """
        A decorator to register a function as a tool.
        Usage: @registry.register
        """
        tool_name = func.__name__
        self.tools[tool_name] = func
        return func

    def get_tool_schema(self):
        """
        Generates the schema for all registered tools in OpenAI's format.
        This schema works with both OpenAI and llama.cpp backends.
        """
        schemas = []
        for tool_name, func in self.tools.items():
            signature = inspect.signature(func)
            docstring = inspect.getdoc(func)
            
            # Extract the description from the first line of the docstring
            description = docstring.split('\n')[0] if docstring else "No description provided."

            # Build the parameters schema
            parameters = {
                "type": "object",
                "properties": {},
                "required": [],
            }

            for name, param in signature.parameters.items():
                # For simplicity, we assume all parameters are strings
                # In a production system, you'd handle different types properly
                param_type = "string"
                parameters["properties"][name] = {
                    "type": param_type,
                    "description": f"The {name} parameter"
                }
                
                # If the parameter has no default value, it's required
                if param.default == inspect.Parameter.empty:
                    parameters["required"].append(name)

            # Build the tool schema in OpenAI's format
            schemas.append({
                "type": "function",
                "function": {
                    "name": tool_name,
                    "description": description,
                    "parameters": parameters,
                }
            })
        
        return schemas

    def call_tool(self, tool_name: str, arguments: dict) -> str:
        """
        Calls a tool with the given arguments.
        Returns the result as a string, or an error message if something goes wrong.
        """
        if tool_name not in self.tools:
            return f"Error: Tool '{tool_name}' not found."
        
        try:
            # Call the tool function with the provided arguments
            result = self.tools[tool_name](**arguments)
            return str(result)
        except Exception as e:
            # If the tool execution fails, return a helpful error message
            return f"Error calling tool {tool_name}: {str(e)}"


# Create a global tool registry
registry = ToolRegistry()


# Register some example tools
@registry.register
def get_weather(city: str) -> str:
    """Gets the current weather for a given city."""
    # In a real application, this would call a weather API like OpenWeatherMap
    # For this example, we'll just return mock data
    city_lower = city.lower()
    
    if "san francisco" in city_lower or "sf" in city_lower:
        return "It's 65 degrees and sunny in San Francisco. Perfect weather!"
    elif "new york" in city_lower or "nyc" in city_lower:
        return "It's 45 degrees and cloudy in New York. Bring a jacket!"
    elif "london" in city_lower:
        return "It's 55 degrees and raining in London. Classic British weather."
    else:
        return f"Sorry, I don't have weather data for {city}. Try San Francisco, New York, or London."


@registry.register
def get_news(topic: str) -> str:
    """Gets the latest news headlines for a given topic."""
    # In a real application, this would call a news API like NewsAPI
    # For this example, we'll return mock headlines
    topic_lower = topic.lower()
    
    if "tech" in topic_lower or "technology" in topic_lower:
        return "Top tech news: 1) New AI model breaks records. 2) Major tech company announces layoffs. 3) Startup raises $100M in funding."
    elif "sports" in topic_lower:
        return "Top sports news: 1) Local team wins championship. 2) Star player announces retirement. 3) Olympics preparations underway."
    elif "politics" in topic_lower:
        return "Top political news: 1) New legislation passes. 2) Election results announced. 3) International summit concludes."
    else:
        return f"Here are some general headlines about {topic}: 1) Breaking news story. 2) Important development. 3) Ongoing situation."


@registry.register
def calculate(expression: str) -> str:
    """Evaluates a mathematical expression and returns the result."""
    try:
        # WARNING: eval is dangerous. Only use with trusted input.
        result = eval(expression)
        return str(result)
    except Exception as e:
        return f"Error evaluating expression: {str(e)}"


def agent_with_tools(prompt: str, max_iterations: int = 10) -> str:
    """
    An agent that can use tools to answer questions.
    Works with both OpenAI function calling and llama.cpp tool use.
    """
    # Start with a system message and the user's prompt
    messages = [
        {
            "role": "system",
            "content": """You are a helpful AI assistant with access to various tools. 
            Use the tools when needed to answer the user's questions accurately. 
            Think step by step and use multiple tools if necessary.
            
            After using tools and getting results, provide a final answer to the user."""
        },
        {"role": "user", "content": prompt}
    ]
    
    # Get the tool schemas for the LLM
    tools = registry.get_tool_schema()
    
    # Main agent loop
    for i in range(max_iterations):
        print(f"\n--- Iteration {i+1} ---")
        
        # Call the LLM with the current messages and available tools
        response = client.chat.completions.create(
            model="",  # Model determined by config
            messages=messages,
            tools=tools,
            tool_choice="auto",
            temperature=config.LLAMA_TEMPERATURE if config.LLM_BACKEND == "llamacpp" else 0.7,
            max_tokens=config.LLAMA_MAX_TOKENS if config.LLM_BACKEND == "llamacpp" else None
        )
        
        response_message = response.choices[0].message
        
        # Add assistant message to history
        messages.append({
            "role": "assistant",
            "content": response_message.content or ""
        })
        
        # Check if the model wants to call any tools
        if response_message.tool_calls and len(response_message.tool_calls) > 0:
            print(f"Assistant wants to call {len(response_message.tool_calls)} tool(s)")
            
            # Execute each tool call
            for tool_call in response_message.tool_calls:
                tool_name = tool_call["function"]["name"]
                tool_args = json.loads(tool_call["function"]["arguments"])
                
                print(f"Calling tool: {tool_name}({tool_args})")
                
                # Execute the tool
                tool_result = registry.call_tool(tool_name, tool_args)
                print(f"Tool result: {tool_result}")
                
                # Add the tool result to the message history
                # For llama.cpp, we use a simpler format
                messages.append({
                    "role": "user",
                    "content": f"Tool {tool_name} returned: {tool_result}"
                })
        else:
            # No more tool calls, the agent has finished
            final_response = response_message.content
            print(f"\nAssistant: {final_response}")
            return final_response
    
    return "Agent reached maximum iterations without completing the task."


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
    print("Module 1: Tool Use Agent with llama.cpp")
    print("=" * 80 + "\n")
    
    # Test the agent with a question that requires multiple tool calls
    question = "What's the weather like in San Francisco? Also, what are the latest tech news?"
    
    print(f"User: {question}\n")
    result = agent_with_tools(question)
    
    print(f"\n=== Final Answer ===\n{result}")


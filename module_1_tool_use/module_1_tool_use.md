# Module 1: Tool Use - Teaching Agents to Use APIs

**A Course by "Andrej Karpathy" Style Teaching**

---

In the last module, we built a very simple agent. It was just a loop. But it had a critical limitation: its only tool was a Python `eval` function. This is powerful, but also incredibly dangerous and not very structured. To build truly useful agents, we need to give them the ability to interact with the world in a more controlled way. We need to give them **tools**.

A tool can be anything: a function that calls a weather API, a database query, another AI model, or even a function that sends an email. The key is that we expose these tools to the agent in a way that it can understand and use them effectively. This is where the concept of **function calling** comes in.

## Function Calling: How LLMs Learn to Use Tools

Modern LLMs have been trained to understand a special syntax for describing functions. When you provide a list of available tools and their schemas to the model, it can decide when to use them and what arguments to pass. The model's output will contain a special structure indicating which tool it wants to call and with what parameters. Our job is to parse this structure, execute the corresponding function, and then feed the result back to the model.

This is a crucial concept. The LLM doesn't *execute* the tool; it just *tells us* which tool to execute. We are still in control. This is a much safer and more structured approach than the `eval` hack we used in the last module.

## Building a Tool Registry from Scratch

Let's get practical. How do we manage these tools? We're going to build a simple `ToolRegistry` class. This class will do two things:

1.  Store our tools in a dictionary, so we can easily look them up by name.
2.  Generate the schema that the LLM needs to understand the tools.

Here's how we can start building it. We'll use Python's `inspect` module to automatically generate the schema from our function definitions. This is a bit of a power move, but it saves us a lot of manual work and reduces the chance of errors.

```python
import inspect
import json

class ToolRegistry:
    def __init__(self):
        self.tools = {}

    def register(self, func):
        """A decorator to register a function as a tool."""
        tool_name = func.__name__
        self.tools[tool_name] = func
        return func

    def get_tool_schema(self):
        """Generates the schema for all registered tools."""
        schemas = []
        for tool_name, func in self.tools.items():
            signature = inspect.signature(func)
            docstring = inspect.getdoc(func)
            
            # A simple way to parse the docstring for a description
            description = docstring.split('\n')[0] if docstring else ""

            parameters = {
                "type": "object",
                "properties": {},
                "required": [],
            }

            for name, param in signature.parameters.items():
                # We'll assume all parameters are strings for simplicity
                # In a real system, you'd handle different types
                parameters["properties"][name] = {"type": "string"}
                if param.default == inspect.Parameter.empty:
                    parameters["required"].append(name)

            schemas.append({
                "type": "function",
                "function": {
                    "name": tool_name,
                    "description": description,
                    "parameters": parameters,
                }
            })
        return schemas

    def call_tool(self, tool_name: str, arguments: str) -> str:
        """Calls a tool with the given arguments."""
        if tool_name not in self.tools:
            return f"Error: Tool '{tool_name}' not found."
        
        try:
            args_dict = json.loads(arguments)
            result = self.tools[tool_name](**args_dict)
            return str(result)
        except Exception as e:
            return f"Error calling tool {tool_name}: {e}"

```

This `ToolRegistry` gives us a clean way to define, register, and call our tools. The `register` method is a decorator, which is a very Pythonic way to add functionality to our functions. The `get_tool_schema` method is the real magic. It uses introspection to build the JSON schema that the OpenAI API expects. This is a great example of building a powerful abstraction from simple, fundamental building blocks.

## The Agent with Tools

Now, let's update our agent from Module 0 to use this `ToolRegistry`. The core loop is the same, but the "Act" and "Observe" steps are now more sophisticated.

```python
# (ToolRegistry class from above)

# Create a registry and register some tools
registry = ToolRegistry()

@registry.register
def get_weather(city: str) -> str:
    """Gets the current weather for a given city."""
    # In a real application, this would call a weather API
    if "san francisco" in city.lower():
        return "It's 65 degrees and sunny in San Francisco."
    else:
        return f"Sorry, I don't know the weather in {city}."

@registry.register
def get_news(topic: str) -> str:
    """Gets the latest news headlines for a given topic."""
    # This would call a news API
    return f"Here are the top 5 headlines for {topic}..."

# (The rest of the agent code, modified to use the registry)
```

In our agent loop, instead of looking for a Python code block, we'll now check if the LLM's response includes a `tool_calls` attribute. If it does, we'll iterate through the requested tool calls, use our `registry` to execute them, and then append the results to the message history. This is a much more robust and extensible pattern.

## Project: Build a Weather + News Agent

Your project for this module is to build a fully functional agent that can answer questions about both weather and news. You'll need to:

1.  **Implement the `ToolRegistry` class** as shown above.
2.  **Create at least two tools:** `get_weather` and `get_news`. You can just use placeholder data like in the example, or you can try integrating with real APIs.
3.  **Modify the agent loop** to handle tool calls. The agent should be able to call multiple tools in a single turn if needed.
4.  **Write a good system prompt** that explains to the agent what tools it has and how to use them.
5.  **Test your agent** with a variety of prompts. See if it can chain tool calls (e.g., "What's the weather in the city where the latest tech news is happening?"). This is a tricky problem that will test your implementation.

As you work on this project, pay close attention to the schemas. The quality of your tool descriptions and parameter names will have a huge impact on the agent's performance. This is a key insight: **the schema is part of the prompt**. Garbage in, garbage out. Take the time to write clear, descriptive schemas, and you'll be rewarded with a much more reliable agent.

In the next module, we'll tackle memory. We'll give our agent the ability to remember past interactions, which will unlock a whole new level of capabilities. But first, master the art of tool use. It's the foundation of everything that follows.

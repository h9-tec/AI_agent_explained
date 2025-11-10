"""
Unified LLM Client that supports both OpenAI and llama.cpp backends.
This wrapper provides a consistent interface regardless of the backend.
"""

import json
from typing import List, Dict, Optional, Any, Union
from abc import ABC, abstractmethod

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    from llama_cpp import Llama, ChatCompletionRequestMessage
    LLAMACPP_AVAILABLE = True
except ImportError:
    LLAMACPP_AVAILABLE = False

from config import config


class Message:
    """Unified message format."""
    
    def __init__(self, role: str, content: str, **kwargs):
        self.role = role
        self.content = content
        self.extra = kwargs
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format."""
        result = {"role": self.role, "content": self.content}
        result.update(self.extra)
        return result


class ChatCompletion:
    """Unified chat completion response."""
    
    def __init__(self, content: str, tool_calls: Optional[List[Dict]] = None):
        self.content = content
        self.tool_calls = tool_calls or []
    
    @property
    def message(self):
        """Provides OpenAI-style message access."""
        class MessageWrapper:
            def __init__(self, content: str, tool_calls: List[Dict]):
                self.content = content
                self.tool_calls = tool_calls
        
        return MessageWrapper(self.content, self.tool_calls)


class LLMClient(ABC):
    """Abstract base class for LLM clients."""
    
    @abstractmethod
    def chat_completions_create(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        tools: Optional[List[Dict]] = None,
        tool_choice: str = "auto",
        **kwargs
    ) -> ChatCompletion:
        """Create a chat completion."""
        pass


class OpenAIClient(LLMClient):
    """OpenAI API client wrapper."""
    
    def __init__(self, api_key: str, model: str = "gpt-4-turbo-preview"):
        if not OPENAI_AVAILABLE:
            raise ImportError("openai package not installed. Run: pip install openai")
        
        self.client = openai.OpenAI(api_key=api_key)
        self.model = model
    
    def chat_completions_create(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        tools: Optional[List[Dict]] = None,
        tool_choice: str = "auto",
        **kwargs
    ) -> ChatCompletion:
        """Create a chat completion using OpenAI API."""
        params = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
        }
        
        if max_tokens:
            params["max_tokens"] = max_tokens
        
        if tools:
            params["tools"] = tools
            params["tool_choice"] = tool_choice
        
        response = self.client.chat.completions.create(**params)
        message = response.choices[0].message
        
        # Extract tool calls if present
        tool_calls = []
        if hasattr(message, 'tool_calls') and message.tool_calls:
            for tc in message.tool_calls:
                tool_calls.append({
                    "id": tc.id,
                    "type": "function",
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments
                    }
                })
        
        return ChatCompletion(
            content=message.content or "",
            tool_calls=tool_calls
        )


class LlamaCppClient(LLMClient):
    """llama.cpp client wrapper with function calling support."""
    
    def __init__(
        self,
        model_path: str,
        n_ctx: int = 4096,
        n_gpu_layers: int = 0,
        n_threads: int = 4,
        verbose: bool = False
    ):
        if not LLAMACPP_AVAILABLE:
            raise ImportError(
                "llama-cpp-python not installed. Run: pip install llama-cpp-python"
            )
        
        self.llm = Llama(
            model_path=model_path,
            n_ctx=n_ctx,
            n_gpu_layers=n_gpu_layers,
            n_threads=n_threads,
            verbose=verbose,
            chat_format="chatml"  # Use ChatML format for better compatibility
        )
        self.verbose = verbose
    
    def _format_tools_for_prompt(self, tools: Optional[List[Dict]]) -> str:
        """Format tools as text for inclusion in the prompt."""
        if not tools:
            return ""
        
        tool_descriptions = ["You have access to the following tools:"]
        for tool in tools:
            func = tool.get("function", {})
            name = func.get("name", "unknown")
            desc = func.get("description", "No description")
            params = func.get("parameters", {}).get("properties", {})
            
            param_str = ", ".join([f"{k}: {v.get('type', 'string')}" for k, v in params.items()])
            tool_descriptions.append(f"- {name}({param_str}): {desc}")
        
        tool_descriptions.append(
            "\nTo use a tool, respond with: TOOL_CALL: tool_name(arg1=\"value1\", arg2=\"value2\")"
        )
        return "\n".join(tool_descriptions)
    
    def _extract_tool_calls(self, text: str) -> List[Dict]:
        """Extract tool calls from the model's response."""
        import re
        
        tool_calls = []
        # Look for TOOL_CALL: pattern
        pattern = r"TOOL_CALL:\s*(\w+)\((.*?)\)"
        matches = re.finditer(pattern, text, re.DOTALL)
        
        for i, match in enumerate(matches):
            tool_name = match.group(1)
            args_str = match.group(2)
            
            # Parse arguments
            args = {}
            for arg_match in re.finditer(r'(\w+)="([^"]*)"', args_str):
                key = arg_match.group(1)
                value = arg_match.group(2)
                args[key] = value
            
            tool_calls.append({
                "id": f"call_{i}",
                "type": "function",
                "function": {
                    "name": tool_name,
                    "arguments": json.dumps(args)
                }
            })
        
        return tool_calls
    
    def chat_completions_create(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        tools: Optional[List[Dict]] = None,
        tool_choice: str = "auto",
        **kwargs
    ) -> ChatCompletion:
        """Create a chat completion using llama.cpp."""
        # If tools are provided, inject them into the system message
        if tools:
            tool_prompt = self._format_tools_for_prompt(tools)
            
            # Find or create system message
            system_msg_idx = None
            for i, msg in enumerate(messages):
                if msg["role"] == "system":
                    system_msg_idx = i
                    break
            
            if system_msg_idx is not None:
                messages[system_msg_idx]["content"] += f"\n\n{tool_prompt}"
            else:
                messages.insert(0, {"role": "system", "content": tool_prompt})
        
        # Call llama.cpp
        response = self.llm.create_chat_completion(
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens or config.LLAMA_MAX_TOKENS,
        )
        
        # Extract response
        content = response["choices"][0]["message"]["content"]
        
        # Extract tool calls if present
        tool_calls = self._extract_tool_calls(content) if tools else []
        
        # Remove tool call text from content if tools were called
        if tool_calls:
            import re
            content = re.sub(r"TOOL_CALL:.*?\)", "", content, flags=re.DOTALL).strip()
        
        return ChatCompletion(content=content, tool_calls=tool_calls)


def get_llm_client() -> LLMClient:
    """
    Factory function to get the appropriate LLM client based on configuration.
    
    Returns:
        LLMClient: Either OpenAIClient or LlamaCppClient based on config
    """
    if config.LLM_BACKEND == "openai":
        if not config.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY not set in configuration")
        
        return OpenAIClient(
            api_key=config.OPENAI_API_KEY,
            model=config.OPENAI_MODEL
        )
    
    elif config.LLM_BACKEND == "llamacpp":
        return LlamaCppClient(
            model_path=config.LLAMA_MODEL_PATH,
            n_ctx=config.LLAMA_N_CTX,
            n_gpu_layers=config.LLAMA_N_GPU_LAYERS,
            n_threads=config.LLAMA_N_THREADS,
            verbose=config.VERBOSE
        )
    
    else:
        raise ValueError(f"Unknown LLM backend: {config.LLM_BACKEND}")


# Convenience wrapper that mimics OpenAI's interface
class UnifiedClient:
    """Unified client with OpenAI-style interface."""
    
    def __init__(self):
        self.llm_client = get_llm_client()
    
    class ChatCompletions:
        """Nested class to mimic OpenAI's client.chat.completions structure."""
        
        def __init__(self, llm_client: LLMClient):
            self.llm_client = llm_client
        
        def create(self, model: str = "", **kwargs) -> Any:
            """Create a chat completion."""
            # Ignore model parameter for llama.cpp
            completion = self.llm_client.chat_completions_create(**kwargs)
            
            # Wrap in OpenAI-style response object
            class Response:
                def __init__(self, completion: ChatCompletion):
                    self.choices = [type('obj', (object,), {
                        'message': completion.message
                    })]
            
            return Response(completion)
    
    @property
    def chat(self):
        """Provides client.chat.completions.create() interface."""
        class Chat:
            def __init__(self, llm_client: LLMClient):
                self.completions = UnifiedClient.ChatCompletions(llm_client)
        
        return Chat(self.llm_client)


if __name__ == "__main__":
    # Test the unified client
    print("Testing Unified LLM Client\n")
    
    try:
        config.validate()
        config.print_config()
        
        client = UnifiedClient()
        
        print("\n" + "=" * 80)
        print("Testing basic chat completion...")
        print("=" * 80 + "\n")
        
        response = client.chat.completions.create(
            model="",  # Ignored for llama.cpp
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Say hello in one sentence."}
            ],
            temperature=0.7,
            max_tokens=100
        )
        
        print(f"Response: {response.choices[0].message.content}")
        print("\n✓ Client test successful!")
        
    except Exception as e:
        print(f"\n✗ Client test failed: {e}")
        import traceback
        traceback.print_exc()


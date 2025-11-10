"""
Configuration module for AI Agents Course.
Handles environment variables and model configuration.
"""

import os
from pathlib import Path
from typing import Literal
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Configuration class for the AI agents course."""
    
    # LLM Backend Selection
    LLM_BACKEND: Literal["openai", "llamacpp"] = os.getenv("LLM_BACKEND", "llamacpp")
    
    # OpenAI Configuration
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview")
    
    # Llama.cpp Configuration
    LLAMA_MODEL_PATH: str = os.getenv(
        "LLAMA_MODEL_PATH",
        str(Path(__file__).parent / "models" / "llama-2-7b-chat.Q4_K_M.gguf")
    )
    LLAMA_N_CTX: int = int(os.getenv("LLAMA_N_CTX", "4096"))
    LLAMA_N_GPU_LAYERS: int = int(os.getenv("LLAMA_N_GPU_LAYERS", "0"))
    LLAMA_N_THREADS: int = int(os.getenv("LLAMA_N_THREADS", "4"))
    LLAMA_TEMPERATURE: float = float(os.getenv("LLAMA_TEMPERATURE", "0.7"))
    LLAMA_TOP_P: float = float(os.getenv("LLAMA_TOP_P", "0.95"))
    LLAMA_MAX_TOKENS: int = int(os.getenv("LLAMA_MAX_TOKENS", "2048"))
    
    # General Settings
    VERBOSE: bool = os.getenv("VERBOSE", "true").lower() == "true"
    
    @classmethod
    def validate(cls) -> None:
        """Validates the configuration."""
        if cls.LLM_BACKEND == "openai" and not cls.OPENAI_API_KEY:
            raise ValueError(
                "OPENAI_API_KEY must be set when using OpenAI backend. "
                "Set it in your .env file or as an environment variable."
            )
        
        if cls.LLM_BACKEND == "llamacpp":
            model_path = Path(cls.LLAMA_MODEL_PATH)
            if not model_path.exists():
                raise FileNotFoundError(
                    f"Llama model not found at {cls.LLAMA_MODEL_PATH}. "
                    f"Please download a GGUF model and update LLAMA_MODEL_PATH in your .env file."
                )
    
    @classmethod
    def print_config(cls) -> None:
        """Prints the current configuration."""
        print("=" * 80)
        print("AI Agents Course Configuration")
        print("=" * 80)
        print(f"LLM Backend: {cls.LLM_BACKEND}")
        
        if cls.LLM_BACKEND == "openai":
            print(f"OpenAI Model: {cls.OPENAI_MODEL}")
            print(f"API Key: {'*' * 20}{cls.OPENAI_API_KEY[-4:] if cls.OPENAI_API_KEY else 'NOT SET'}")
        else:
            print(f"Llama Model Path: {cls.LLAMA_MODEL_PATH}")
            print(f"Context Size: {cls.LLAMA_N_CTX}")
            print(f"GPU Layers: {cls.LLAMA_N_GPU_LAYERS}")
            print(f"CPU Threads: {cls.LLAMA_N_THREADS}")
            print(f"Temperature: {cls.LLAMA_TEMPERATURE}")
        
        print(f"Verbose: {cls.VERBOSE}")
        print("=" * 80)


# Create a global config instance
config = Config()


if __name__ == "__main__":
    # Test configuration
    try:
        config.validate()
        config.print_config()
        print("\n✓ Configuration is valid!")
    except Exception as e:
        print(f"\n✗ Configuration error: {e}")


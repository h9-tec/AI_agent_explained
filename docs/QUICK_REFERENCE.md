# Quick Reference Guide

**By Hesham Haroon**

## Setup Commands

### Installation
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\Activate.ps1  # Windows

# Install dependencies
pip install -r requirements.txt

# Download a model (example)
mkdir models
wget https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q4_K_M.gguf -O models/llama-2-7b-chat.Q4_K_M.gguf
```

### Configuration
```bash
# Copy example config
cp .env.example .env

# Edit .env file
# Set LLM_BACKEND=llamacpp or openai
# Set LLAMA_MODEL_PATH or OPENAI_API_KEY
```

---

## Running Modules

```bash
# Test configuration
python config.py

# Test LLM client
python llm_client.py

# Run modules
python module_0_agent_llamacpp.py
python module_1_tool_agent_llamacpp.py
python module_2_memory_agent_llamacpp.py
python module_3_react_agent_llamacpp.py
python module_4_crewai_agents.py
```

---

## Configuration Options

### .env File

```bash
# Backend selection
LLM_BACKEND=llamacpp  # or "openai"

# llama.cpp settings
LLAMA_MODEL_PATH=./models/llama-2-7b-chat.Q4_K_M.gguf
LLAMA_N_CTX=4096
LLAMA_N_GPU_LAYERS=0  # 0=CPU, 35+=GPU
LLAMA_N_THREADS=4
LLAMA_TEMPERATURE=0.7
LLAMA_MAX_TOKENS=2048

# OpenAI settings
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4-turbo-preview

# General
VERBOSE=true
```

---

## Model Recommendations

| Model | Size | RAM | Use Case |
|-------|------|-----|----------|
| Llama 2 7B Q4 | 4GB | 8GB | Learning, testing |
| Mistral 7B Q4 | 4GB | 8GB | Better reasoning |
| Llama 2 13B Q4 | 7GB | 16GB | Production |
| CodeLlama 7B Q4 | 4GB | 8GB | Code tasks |

---

## GPU Configuration

### NVIDIA (CUDA)
```bash
# Install with CUDA support
CMAKE_ARGS="-DLLAMA_CUBLAS=on" pip install llama-cpp-python --force-reinstall --no-cache-dir

# In .env
LLAMA_N_GPU_LAYERS=35  # Adjust for your GPU
```

### Apple Silicon (Metal)
```bash
# Install with Metal support
CMAKE_ARGS="-DLLAMA_METAL=on" pip install llama-cpp-python --force-reinstall --no-cache-dir

# In .env
LLAMA_N_GPU_LAYERS=1
```

---

## Code Examples

### Using the Unified Client

```python
from llm_client import UnifiedClient
from config import config

# Initialize client
client = UnifiedClient()

# Create completion
response = client.chat.completions.create(
    model="",  # Ignored, uses config
    messages=[
        {"role": "system", "content": "You are helpful."},
        {"role": "user", "content": "Hello!"}
    ],
    temperature=0.7
)

print(response.choices[0].message.content)
```

### Creating a Simple Agent

```python
from llm_client import UnifiedClient

client = UnifiedClient()

def simple_agent(prompt: str) -> str:
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]
    
    response = client.chat.completions.create(
        model="",
        messages=messages
    )
    
    return response.choices[0].message.content

# Use it
answer = simple_agent("What is 2+2?")
print(answer)
```

### Creating a CrewAI Agent

```python
from crewai import Agent, Task, Crew, Process
from crewai_tools import tool

@tool("Calculator")
def calculator(expression: str) -> str:
    return str(eval(expression))

agent = Agent(
    role="Mathematician",
    goal="Solve math problems accurately",
    backstory="You are an expert mathematician.",
    tools=[calculator],
    verbose=True
)

task = Task(
    description="Calculate 123 * 456",
    agent=agent,
    expected_output="The numerical result"
)

crew = Crew(
    agents=[agent],
    tasks=[task],
    process=Process.sequential
)

result = crew.kickoff()
print(result)
```

---

## Troubleshooting

### Model not found
```bash
# Check file exists
ls -lh models/

# Use absolute path in .env
LLAMA_MODEL_PATH=/absolute/path/to/model.gguf
```

### Out of memory
```bash
# Use smaller model
# Reduce context size
LLAMA_N_CTX=2048

# Reduce GPU layers
LLAMA_N_GPU_LAYERS=20
```

### Slow inference
```bash
# Increase threads
LLAMA_N_THREADS=8

# Use GPU
LLAMA_N_GPU_LAYERS=35

# Use smaller model
```

### Import errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

---

## Performance Optimization

### CPU
- Use Q4 quantization
- Set threads = CPU cores
- Context ≤ 4096
- Use 7B models

### GPU
- Set layers based on VRAM:
  - 8GB: 20-25 layers
  - 12GB: 30-35 layers
  - 16GB+: 40+ layers
- Use Q4/Q5 quantization
- Increase context to 8192+

---

## Useful Commands

```bash
# Check Python version
python --version

# Check GPU
nvidia-smi  # NVIDIA
system_profiler SPDisplaysDataType  # Mac

# Monitor resources
htop  # CPU/RAM
nvidia-smi -l 1  # GPU

# Test model loading
python -c "from llama_cpp import Llama; l = Llama('models/model.gguf'); print('OK')"
```

---

## File Structure

```
ai_agents_course/
├── config.py                          # Configuration
├── llm_client.py                      # Unified LLM client
├── requirements.txt                   # Dependencies
├── .env                               # Your config (create from .env.example)
├── .env.example                       # Example config
│
├── module_0_agent_llamacpp.py         # Basic agent
├── module_1_tool_agent_llamacpp.py    # Tool use
├── module_2_memory_agent_llamacpp.py  # Memory
├── module_3_react_agent_llamacpp.py   # ReAct
├── module_4_crewai_agents.py          # CrewAI
│
├── SETUP_GUIDE.md                     # Full setup guide
├── EXTENSION_SUMMARY.md               # What's new
├── QUICK_REFERENCE.md                 # This file
│
└── models/                            # Your models (create this)
    └── *.gguf                         # GGUF model files
```

---

## Common Workflows

### Testing a New Model
```bash
# 1. Download model
wget URL -O models/model.gguf

# 2. Update .env
LLAMA_MODEL_PATH=./models/model.gguf

# 3. Test
python config.py
python llm_client.py
python module_0_agent_llamacpp.py
```

### Switching Backends
```bash
# Edit .env
LLM_BACKEND=openai  # or llamacpp

# Test
python config.py
python module_0_agent_llamacpp.py
```

### Creating a New Agent
```python
# 1. Import
from llm_client import UnifiedClient

# 2. Initialize
client = UnifiedClient()

# 3. Create agent function
def my_agent(prompt):
    # Your logic here
    pass

# 4. Run
result = my_agent("Your prompt")
```

---

## Resources

- **Setup Guide:** `SETUP_GUIDE.md`
- **Extension Summary:** `EXTENSION_SUMMARY.md`
- **Original README:** `README.md`
- **Module Docs:** `module_*_.md`

---

## Getting Help

1. Check `SETUP_GUIDE.md` troubleshooting section
2. Validate config: `python config.py`
3. Test client: `python llm_client.py`
4. Check model file exists
5. Try smaller model
6. Check GitHub issues for llama.cpp and CrewAI

---

**Quick Start:** Copy `.env.example` to `.env`, download a model, run `python config.py`, then run any module!


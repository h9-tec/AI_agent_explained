# Setup Guide: Running Agents Locally

**The Goal:** Run the same agents you built in Modules 0-3, but on your own hardware. No API costs, no data leaving your machine, full control.

**The Philosophy:** We built everything from scratch first. Now we're adding one more layer: the ability to swap backends. You'll understand exactly what's happening because you built it yourself.

**Author:** Hesham Haroon

---

## Quick Start (5 Minutes)

Already did Modules 0-3? Here's the fastest path:

```bash
# Install local model support
pip install llama-cpp-python

# Download a model (4GB)
mkdir models && cd models
wget https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q4_K_M.gguf
cd ..

# Configure
echo "LLM_BACKEND=llamacpp" > .env
echo "LLAMA_MODEL_PATH=./models/llama-2-7b-chat.Q4_K_M.gguf" >> .env

# Run
python module_0_agent_llamacpp.py
```

That's it. Same agent, local model.

---

## What You Need

**Minimum (for learning):**
- Python 3.10+
- 8GB RAM
- 10GB disk space
- Any OS (Linux, macOS, Windows)

**Better (for real work):**
- 16GB RAM
- GPU (NVIDIA or Apple Silicon)
- More patience for model downloads

**The Trade-off:** Local models are slower than OpenAI's API, but they're free and private. On a laptop CPU, expect 2-5 tokens/second. On a GPU, 20-100 tokens/second. OpenAI? Instant.

---

## Understanding What We Built

Before installing anything, let's understand what changed:

### What Stayed the Same
- The agent loop (still a while loop)
- Tool calling (still function calls)
- Memory management (still a list of messages)
- ReAct pattern (still Thought → Action → Observation)

### What Changed
- **One file:** `llm_client.py` - abstracts OpenAI vs. llama.cpp
- **One config:** `.env` - switches backends
- **Same interface:** Your agent code barely changes

**The Point:** Good abstractions are thin. If we had to rewrite everything, the abstraction would be wrong.

Look at the diff between `module_0_agent.py` and `module_0_agent_llamacpp.py`. It's tiny. That's the sign of a good abstraction.

---

## Installation

### Step 1: Clone or Download the Course

```bash
cd ~/Downloads/ai_agents_course
```

### Step 2: Create a Virtual Environment

**On Linux/macOS:**
```bash
python -m venv venv
source venv/bin/activate
```

**On Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### Step 3: Install Dependencies

```bash
# Install core dependencies
pip install -r requirements.txt
```

### Step 4: Install llama-cpp-python with GPU Support (Optional)

**For NVIDIA GPU (CUDA):**
```bash
CMAKE_ARGS="-DLLAMA_CUBLAS=on" pip install llama-cpp-python --force-reinstall --no-cache-dir
```

**For Apple Silicon (Metal):**
```bash
CMAKE_ARGS="-DLLAMA_METAL=on" pip install llama-cpp-python --force-reinstall --no-cache-dir
```

**For CPU only (default):**
```bash
pip install llama-cpp-python
```

---

## Downloading Models

### Option 1: Download from Hugging Face (Recommended)

We recommend using quantized GGUF models for efficiency. Here are some good options:

#### Small Models (Good for Learning, 4-8GB RAM)

**Llama 2 7B Chat (Q4 quantization):**
```bash
# Create models directory
mkdir -p models

# Download using wget or curl
wget https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q4_K_M.gguf -O models/llama-2-7b-chat.Q4_K_M.gguf
```

**Mistral 7B Instruct (Q4 quantization):**
```bash
wget https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.2-GGUF/resolve/main/mistral-7b-instruct-v0.2.Q4_K_M.gguf -O models/mistral-7b-instruct-v0.2.Q4_K_M.gguf
```

#### Medium Models (Better Performance, 16GB+ RAM)

**Llama 2 13B Chat (Q4 quantization):**
```bash
wget https://huggingface.co/TheBloke/Llama-2-13B-chat-GGUF/resolve/main/llama-2-13b-chat.Q4_K_M.gguf -O models/llama-2-13b-chat.Q4_K_M.gguf
```

### Option 2: Using Hugging Face CLI

```bash
# Install huggingface-cli
pip install huggingface-hub

# Download a model
huggingface-cli download TheBloke/Llama-2-7B-Chat-GGUF llama-2-7b-chat.Q4_K_M.gguf --local-dir models --local-dir-use-symlinks False
```

### Recommended Models for This Course

| Model | Size | RAM Required | Best For |
|-------|------|--------------|----------|
| Llama 2 7B Chat Q4 | ~4GB | 8GB | Learning, testing |
| Mistral 7B Instruct Q4 | ~4GB | 8GB | Better reasoning |
| Llama 2 13B Chat Q4 | ~7GB | 16GB | Production quality |
| CodeLlama 7B Q4 | ~4GB | 8GB | Code generation |

---

## Configuration

### Step 1: Copy the Example Environment File

```bash
cp .env.example .env
```

### Step 2: Edit the .env File

Open `.env` in your favorite text editor and configure:

#### For llama.cpp (Local Models):

```bash
# Use llama.cpp backend
LLM_BACKEND=llamacpp

# Path to your downloaded model
LLAMA_MODEL_PATH=./models/llama-2-7b-chat.Q4_K_M.gguf

# Model parameters
LLAMA_N_CTX=4096          # Context window size
LLAMA_N_GPU_LAYERS=0      # 0 for CPU, 35+ for GPU
LLAMA_N_THREADS=4         # Number of CPU threads
LLAMA_TEMPERATURE=0.7     # Sampling temperature
LLAMA_TOP_P=0.95          # Top-p sampling
LLAMA_MAX_TOKENS=2048     # Max tokens to generate

# Verbose logging
VERBOSE=true
```

#### For OpenAI (Cloud API):

```bash
# Use OpenAI backend
LLM_BACKEND=openai

# Your OpenAI API key
OPENAI_API_KEY=sk-your-api-key-here
OPENAI_MODEL=gpt-4-turbo-preview
```

### Step 3: GPU Configuration (Optional)

If you have a GPU and want to use it:

**For NVIDIA GPU:**
```bash
# In your .env file
LLAMA_N_GPU_LAYERS=35  # Adjust based on your GPU memory
```

**For Apple Silicon:**
```bash
# Metal is automatically used, just ensure you installed with Metal support
LLAMA_N_GPU_LAYERS=1  # Use 1 to enable Metal
```

---

## Testing Your Setup

### Test 1: Validate Configuration

```bash
python config.py
```

Expected output:
```
================================================================================
AI Agents Course Configuration
================================================================================
LLM Backend: llamacpp
Llama Model Path: ./models/llama-2-7b-chat.Q4_K_M.gguf
Context Size: 4096
GPU Layers: 0
CPU Threads: 4
Temperature: 0.7
Verbose: True
================================================================================

✓ Configuration is valid!
```

### Test 2: Test the LLM Client

```bash
python llm_client.py
```

This will test basic chat completion. You should see a response from the model.

### Test 3: Run Module 0

```bash
python module_0_agent_llamacpp.py
```

This will run the basic agent loop and solve a math problem.

---

## Troubleshooting

### Issue: "Model file not found"

**Solution:**
1. Check that the model file exists: `ls -lh models/`
2. Verify the path in your `.env` file matches the actual file location
3. Use absolute paths if relative paths don't work

### Issue: "Out of memory" or "Segmentation fault"

**Solution:**
1. Use a smaller model (Q4 quantization or 7B instead of 13B)
2. Reduce `LLAMA_N_CTX` to 2048 or lower
3. Reduce `LLAMA_N_GPU_LAYERS` if using GPU
4. Close other applications to free up RAM

### Issue: "Slow inference" (CPU only)

**Solution:**
1. Increase `LLAMA_N_THREADS` to match your CPU cores
2. Use a smaller model or lower quantization (Q4 instead of Q5)
3. Reduce `LLAMA_N_CTX` to 2048
4. Consider using GPU acceleration if available

### Issue: "ImportError: No module named 'llama_cpp'"

**Solution:**
```bash
pip install llama-cpp-python
```

### Issue: "GPU not being used"

**Solution:**
1. Verify GPU installation:
   ```bash
   python -c "from llama_cpp import Llama; print(Llama.supports_gpu_offload())"
   ```
2. Reinstall with GPU support (see Installation Step 4)
3. Set `LLAMA_N_GPU_LAYERS` > 0 in `.env`

### Issue: "CrewAI not working with llama.cpp"

**Solution:**
CrewAI is optimized for OpenAI models. For best results:
1. Use OpenAI backend for Module 4: `LLM_BACKEND=openai`
2. Or use a highly capable local model like Mistral 7B Instruct
3. Increase temperature for more creative responses

---

## Running the Modules

### Module 0: Basic Agent Loop

```bash
python module_0_agent_llamacpp.py
```

Tests: Basic agent loop, code execution, multi-step reasoning

### Module 1: Tool Use

```bash
python module_1_tool_agent_llamacpp.py
```

Tests: Function calling, tool registry, multi-tool workflows

### Module 2: Memory and State

```bash
python module_2_memory_agent_llamacpp.py
```

Tests: Conversation memory, sliding windows, stateful agents

### Module 3: ReAct Pattern

```bash
python module_3_react_agent_llamacpp.py
```

Tests: Reasoning traces, action parsing, multi-step problem solving

### Module 4: CrewAI Multi-Agent

```bash
python module_4_crewai_agents.py
```

Tests: Multi-agent collaboration, role-based agents, complex workflows

---

## Performance Tips

### For CPU Inference:
- Use Q4 quantized models
- Set `LLAMA_N_THREADS` to your CPU core count
- Keep `LLAMA_N_CTX` at 2048 or lower
- Close unnecessary applications

### For GPU Inference:
- Set `LLAMA_N_GPU_LAYERS` based on your GPU memory:
  - 8GB VRAM: 20-25 layers
  - 12GB VRAM: 30-35 layers
  - 16GB+ VRAM: 40+ layers (full offload)
- Increase `LLAMA_N_CTX` for longer contexts
- Use Q4 or Q5 quantization

### For Apple Silicon:
- Install with Metal support
- Use Q4 or Q5 quantization
- Set `LLAMA_N_GPU_LAYERS=1` to enable Metal
- 8GB unified memory: 7B models
- 16GB+ unified memory: 13B models

---

## Next Steps

1. **Complete the modules in order** (0 → 1 → 2 → 3 → 4)
2. **Experiment with different models** to see how they perform
3. **Try both backends** (llama.cpp and OpenAI) to compare
4. **Modify the code** to build your own agents
5. **Build a project** using the patterns you've learned

---

## Additional Resources

- **llama.cpp Documentation:** https://github.com/ggerganov/llama.cpp
- **llama-cpp-python:** https://github.com/abetlen/llama-cpp-python
- **CrewAI Documentation:** https://docs.crewai.com/
- **Hugging Face Models:** https://huggingface.co/models?library=gguf
- **Original Course README:** See `README.md`

---

## Getting Help

If you encounter issues:

1. Check the [Troubleshooting](#troubleshooting) section
2. Verify your configuration with `python config.py`
3. Test with a smaller model first
4. Check the llama.cpp and llama-cpp-python GitHub issues
5. Ensure your Python version is 3.10+

Happy learning! 🚀


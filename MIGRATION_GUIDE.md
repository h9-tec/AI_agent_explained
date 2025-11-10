# Migration Guide: Moving to llama.cpp and CrewAI

**By Hesham Haroon**

This guide helps you transition from the original OpenAI-only course to the extended version with llama.cpp and CrewAI support.

---

## Overview

The extended course maintains **full backward compatibility** with the original modules while adding:

- ✅ Support for local models via llama.cpp
- ✅ Unified client interface
- ✅ Configuration-based backend switching
- ✅ CrewAI multi-agent framework
- ✅ Enhanced documentation

**Original modules still work!** You can continue using them with OpenAI.

---

## Migration Paths

### Path 1: Keep Using OpenAI (No Changes Required)

If you're happy with OpenAI, **no migration needed**. Continue using:
- `module_0_agent.py`
- `module_1_tool_agent.py`
- `module_2_memory_agent.py`
- `module_3_react_agent.py`

### Path 2: Switch to Unified Client (Recommended)

Use the new modules that support both backends:
- `module_0_agent_llamacpp.py`
- `module_1_tool_agent_llamacpp.py`
- `module_2_memory_agent_llamacpp.py`
- `module_3_react_agent_llamacpp.py`

**Benefits:**
- Switch between OpenAI and llama.cpp anytime
- Same code works with both backends
- Future-proof your projects

### Path 3: Add Multi-Agent Capabilities

Extend your agents with CrewAI:
- `module_4_crewai_agents.py`

**Benefits:**
- Build collaborative agent teams
- Specialized agents for complex tasks
- Production-ready orchestration

---

## Step-by-Step Migration

### Step 1: Install New Dependencies

```bash
# Activate your virtual environment
source venv/bin/activate  # Linux/Mac
.\venv\Scripts\Activate.ps1  # Windows

# Install new dependencies
pip install -r requirements.txt
```

### Step 2: Create Configuration File

```bash
# Copy example configuration
cp .env.example .env

# Edit .env and set your preferences
nano .env  # or use any text editor
```

**For OpenAI (no change in behavior):**
```bash
LLM_BACKEND=openai
OPENAI_API_KEY=your-api-key-here
OPENAI_MODEL=gpt-4-turbo-preview
```

**For llama.cpp (new capability):**
```bash
LLM_BACKEND=llamacpp
LLAMA_MODEL_PATH=./models/llama-2-7b-chat.Q4_K_M.gguf
LLAMA_N_CTX=4096
LLAMA_N_GPU_LAYERS=0
```

### Step 3: Test Configuration

```bash
python config.py
```

Expected output:
```
================================================================================
AI Agents Course Configuration
================================================================================
LLM Backend: openai (or llamacpp)
...
✓ Configuration is valid!
```

### Step 4: Test Unified Client

```bash
python llm_client.py
```

This tests that the LLM client works with your chosen backend.

### Step 5: Run Extended Modules

```bash
# Test each module
python module_0_agent_llamacpp.py
python module_1_tool_agent_llamacpp.py
python module_2_memory_agent_llamacpp.py
python module_3_react_agent_llamacpp.py
```

---

## Code Migration Examples

### Example 1: Basic Agent

**Original (OpenAI only):**
```python
import openai

client = openai.OpenAI()

response = client.chat.completions.create(
    model="gpt-4-turbo-preview",
    messages=[{"role": "user", "content": "Hello"}]
)
```

**Migrated (Unified):**
```python
from llm_client import UnifiedClient
from config import config

client = UnifiedClient()

response = client.chat.completions.create(
    model="",  # Model determined by config
    messages=[{"role": "user", "content": "Hello"}]
)
```

**Changes:**
1. Import `UnifiedClient` instead of `openai.OpenAI`
2. Import `config` for configuration
3. Model parameter can be empty (uses config)
4. Everything else stays the same!

### Example 2: Tool Use

**Original:**
```python
import openai

client = openai.OpenAI()

response = client.chat.completions.create(
    model="gpt-4-turbo-preview",
    messages=messages,
    tools=tools,
    tool_choice="auto"
)
```

**Migrated:**
```python
from llm_client import UnifiedClient

client = UnifiedClient()

response = client.chat.completions.create(
    model="",  # Uses config
    messages=messages,
    tools=tools,
    tool_choice="auto"
)
```

**Changes:**
- Only the import and client initialization!
- Tool calling works the same way

### Example 3: Custom Agent Class

**Original:**
```python
import openai

class MyAgent:
    def __init__(self):
        self.client = openai.OpenAI()
    
    def run(self, prompt):
        response = self.client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
```

**Migrated:**
```python
from llm_client import UnifiedClient

class MyAgent:
    def __init__(self):
        self.client = UnifiedClient()
    
    def run(self, prompt):
        response = self.client.chat.completions.create(
            model="",  # Uses config
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
```

**Changes:**
- Import statement
- Client initialization
- Remove hardcoded model name

---

## Configuration Patterns

### Pattern 1: Development vs. Production

**Development (.env):**
```bash
LLM_BACKEND=llamacpp
LLAMA_MODEL_PATH=./models/llama-2-7b-chat.Q4_K_M.gguf
```

**Production (.env.production):**
```bash
LLM_BACKEND=openai
OPENAI_API_KEY=sk-prod-key-here
OPENAI_MODEL=gpt-4-turbo-preview
```

Switch by copying the appropriate file:
```bash
cp .env.production .env
```

### Pattern 2: Multiple Backends

Keep both configured and switch via environment variable:

```bash
# Use llama.cpp
export LLM_BACKEND=llamacpp
python my_agent.py

# Use OpenAI
export LLM_BACKEND=openai
python my_agent.py
```

### Pattern 3: Per-Project Configuration

Different projects can have different `.env` files:

```
project1/
  .env  # Uses llama.cpp
  agent.py

project2/
  .env  # Uses OpenAI
  agent.py
```

---

## Backward Compatibility

### What Still Works

✅ All original modules (`module_0_agent.py`, etc.)  
✅ OpenAI API key in environment variable  
✅ All existing code patterns  
✅ All tool implementations  
✅ All agent patterns (ReAct, etc.)

### What's New (Optional)

🆕 Unified client for backend flexibility  
🆕 Configuration file for easier management  
🆕 llama.cpp support for local models  
🆕 CrewAI for multi-agent systems  
🆕 Enhanced documentation

### Breaking Changes

❌ **None!** The original modules are untouched.

---

## Common Migration Scenarios

### Scenario 1: "I just want to try llama.cpp"

```bash
# 1. Install dependencies
pip install llama-cpp-python

# 2. Download a model
mkdir models
wget https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q4_K_M.gguf -O models/llama-2-7b-chat.Q4_K_M.gguf

# 3. Create .env
echo "LLM_BACKEND=llamacpp" > .env
echo "LLAMA_MODEL_PATH=./models/llama-2-7b-chat.Q4_K_M.gguf" >> .env

# 4. Run
python module_0_agent_llamacpp.py
```

### Scenario 2: "I want to use both OpenAI and llama.cpp"

```bash
# In your .env
LLM_BACKEND=openai  # or llamacpp

# Switch anytime by editing .env
# Or use environment variable:
LLM_BACKEND=llamacpp python my_agent.py
```

### Scenario 3: "I want to build multi-agent systems"

```bash
# 1. Install CrewAI
pip install crewai crewai-tools

# 2. Configure backend (OpenAI recommended for CrewAI)
echo "LLM_BACKEND=openai" > .env
echo "OPENAI_API_KEY=your-key" >> .env

# 3. Run CrewAI example
python module_4_crewai_agents.py
```

### Scenario 4: "I have existing agents to migrate"

1. **Keep original code working** (no changes needed)
2. **Create new versions** using `UnifiedClient`
3. **Test both versions** side by side
4. **Switch when ready**

---

## Troubleshooting Migration Issues

### Issue: "Module not found"

**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: "Configuration error"

**Solution:**
```bash
# Validate configuration
python config.py

# Check .env file exists
ls -la .env

# Verify .env contents
cat .env
```

### Issue: "Original modules still use OpenAI"

**Expected!** Original modules are unchanged. Use the new `*_llamacpp.py` versions for unified backend support.

### Issue: "llama.cpp not working"

**Solution:**
```bash
# Check model file exists
ls -lh models/

# Test llama-cpp-python installation
python -c "from llama_cpp import Llama; print('OK')"

# Try with absolute path in .env
LLAMA_MODEL_PATH=/absolute/path/to/model.gguf
```

---

## Best Practices

### 1. Test Before Migrating

Run the new modules alongside your existing code:
```bash
# Original
python module_0_agent.py

# New (with OpenAI backend)
LLM_BACKEND=openai python module_0_agent_llamacpp.py

# Should produce similar results
```

### 2. Use Configuration Files

Don't hardcode API keys or model paths:
```python
# ❌ Bad
client = openai.OpenAI(api_key="sk-...")

# ✅ Good
from llm_client import UnifiedClient
client = UnifiedClient()  # Uses .env config
```

### 3. Version Control Your .env.example

```bash
# Commit
git add .env.example

# Don't commit
echo ".env" >> .gitignore
```

### 4. Document Your Backend Choice

In your project README:
```markdown
## Setup

1. Copy `.env.example` to `.env`
2. Configure your backend (OpenAI or llama.cpp)
3. Run `python config.py` to validate
```

---

## Migration Checklist

- [ ] Install new dependencies (`pip install -r requirements.txt`)
- [ ] Create `.env` file from `.env.example`
- [ ] Configure backend (OpenAI or llama.cpp)
- [ ] Test configuration (`python config.py`)
- [ ] Test LLM client (`python llm_client.py`)
- [ ] Run extended modules to verify
- [ ] Update your own code (optional)
- [ ] Test both backends (optional)
- [ ] Try CrewAI (optional)
- [ ] Update documentation

---

## Getting Help

1. **Check documentation:**
   - `SETUP_GUIDE.md` - Complete setup instructions
   - `EXTENSION_SUMMARY.md` - What's new
   - `QUICK_REFERENCE.md` - Quick commands

2. **Validate setup:**
   ```bash
   python config.py
   python llm_client.py
   ```

3. **Test with original modules first:**
   ```bash
   python module_0_agent.py  # Should still work
   ```

4. **Then test new modules:**
   ```bash
   python module_0_agent_llamacpp.py
   ```

---

## Summary

**Migration is optional and non-breaking:**

- ✅ Original modules still work
- ✅ New modules add flexibility
- ✅ Switch backends anytime
- ✅ No code changes required (unless you want them)

**Recommended approach:**

1. Install dependencies
2. Create `.env` file
3. Test with OpenAI backend first
4. Try llama.cpp when ready
5. Explore CrewAI for multi-agent systems

**You're in control!** Use what works for you.

---

Happy migrating! 🚀


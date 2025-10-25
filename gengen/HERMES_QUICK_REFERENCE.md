# Quick Reference: Hermes LLM in AetherOS

## What is Hermes?

Hermes (specifically Nous-Hermes-2-Pro-Mistral-7B) is an unfiltered, creative language model that powers all text generation in AetherOS. It enhances prompts, generates scripts, decomposes stories, and creates intelligent task plans.

## Quick Start

### Option 1: With Ollama (5 minutes)

```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull Hermes
ollama pull hermes2-pro-mistral:latest

# Run AetherOS
python3 aetheros_minimal.py
```

### Option 2: Without LLM (0 minutes)

```bash
# Just run - uses mock mode
python3 aetheros_minimal.py
```

## What Hermes Does

| Feature | Description | Example |
|---------|-------------|---------|
| **Prompt Enhancement** | Expands your idea with detail | "A wizard" → Full narrative with beats |
| **Script Generation** | Creates formatted scripts | Proper scene headings, dialogue, action |
| **Story Breakdown** | Splits into scenes | 60s story → 3 scenes with timing |
| **Meta-Prompting** | Plans task execution | Generates SPARC-based strategies |
| **Analysis** | Evaluates content | Quality, ethics, themes |

## Configuration

Create `.env` file:

```bash
# Provider (ollama or huggingface)
LLM_PROVIDER=ollama

# Model name
LLM_MODEL_NAME=hermes2-pro-mistral:latest

# Server URL (for Ollama)
OLLAMA_BASE_URL=http://localhost:11434

# Generation settings
LLM_TEMPERATURE=0.7      # Creativity (0.0-1.0)
LLM_MAX_TOKENS=2048      # Max length
```

## Usage in Code

```python
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from core.llm import get_llm_service

# Get service
llm = get_llm_service()
await llm.initialize()

# Enhance prompt
enhanced = await llm.enhance_prompt(
    prompt="Your story idea",
    style="cinematic",
    emotional_tone="wonder"
)

# Generate script
script = await llm.generate_script(
    prompt="Your concept",
    duration=60,
    style="adventure"
)

# Decompose story
scenes = await llm.decompose_story(
    prompt="Your narrative",
    duration=120,
    num_scenes=5
)
```

## Models

| Model | Size | Speed | Quality | Use Case |
|-------|------|-------|---------|----------|
| `hermes2-pro-mistral:latest` | 7B | Fast | High | **Recommended** |
| `nous-hermes2:latest` | 7B | Fast | High | Alternative |
| `dolphin-hermes:latest` | 7B | Fast | High | Uncensored |

To switch models:
```bash
ollama pull nous-hermes2:latest
# Update .env: LLM_MODEL_NAME=nous-hermes2:latest
```

## Troubleshooting

### "Ollama not responding"
```bash
ollama serve
```

### "Using mock LLM generation"
This is normal if Ollama isn't installed. The system works in mock mode with rule-based generation.

### "Out of memory"
```bash
# Use quantized model
ollama pull hermes2-pro-mistral:7b-q4_0
```

### "Slow generation"
- Reduce `LLM_MAX_TOKENS` in .env
- Use smaller model variant
- Check system resources

## Advanced

### Remote Server
```bash
# Point to remote Ollama
OLLAMA_BASE_URL=http://your-server:11434
```

### HuggingFace Backend
```bash
# Install dependencies
pip install transformers bitsandbytes

# Configure
LLM_PROVIDER=huggingface
HF_MODEL_ID=NousResearch/Hermes-2-Pro-Mistral-7B
```

### Custom System Prompt
Edit `src/core/llm/llm_config.py`:
```python
system_prompt: str = "Your custom prompt here"
```

## Resources

- **Setup Guide**: `LLM_SETUP.md`
- **Full Summary**: `HERMES_INTEGRATION_SUMMARY.md`
- **Test Suite**: `python3 test_llm_integration.py`
- **Ollama**: https://ollama.ai
- **Model Page**: https://huggingface.co/NousResearch/Hermes-2-Pro-Mistral-7B

## Key Benefits

✅ **Unfiltered**: Creative freedom without restrictions  
✅ **Local**: Runs on your machine, no telemetry  
✅ **Fast**: 1-5 second generation time  
✅ **Smart**: Excellent instruction following  
✅ **Open**: Fully open-source model and code  
✅ **Flexible**: Works with or without LLM  

## Status Check

```bash
# Run integration tests
python3 test_llm_integration.py

# Check service status
python3 -c "
import asyncio
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from core.llm import get_llm_service

async def check():
    llm = get_llm_service()
    await llm.initialize()
    status = llm.get_status()
    print(f'Provider: {status[\"provider\"]}')
    print(f'Model: {status[\"model\"]}')
    print(f'Initialized: {status[\"initialized\"]}')

asyncio.run(check())
"
```

---

**Ready to create?** Just run `python3 aetheros_minimal.py` 🚀

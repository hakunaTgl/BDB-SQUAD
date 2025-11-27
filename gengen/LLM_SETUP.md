# AetherOS LLM Setup Guide

## Quick Start with Hermes Model

AetherOS now integrates the Hermes LLM model for intelligent text generation, prompt enhancement, and meta-prompting.

### Option 1: Using Ollama (Recommended)

Ollama provides the easiest way to run Hermes locally.

#### Install Ollama

```bash
# macOS/Linux
curl -fsSL https://ollama.ai/install.sh | sh

# Or visit https://ollama.ai for other platforms
```

#### Pull Hermes Model

```bash
# Pull the Hermes-2-Pro model (recommended)
ollama pull hermes2-pro-mistral:latest

# Or try other Hermes variants:
# ollama pull nous-hermes2:latest
# ollama pull dolphin-hermes:latest
```

#### Configure AetherOS

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env if needed (defaults work for standard Ollama setup)
```

#### Start Using

```bash
# Make sure Ollama is running (it usually starts automatically)
ollama serve

# In another terminal, run AetherOS
python3 aetheros_minimal.py
```

### Option 2: Using HuggingFace Transformers

For more control or GPU optimization, you can run Hermes directly via HuggingFace.

#### Install Dependencies

```bash
pip install transformers bitsandbytes accelerate sentencepiece
```

#### Configure

Edit `.env`:
```bash
LLM_PROVIDER=huggingface
HF_MODEL_ID=NousResearch/Hermes-2-Pro-Mistral-7B
```

#### Run

```bash
python3 aetheros_minimal.py
```

Note: The model will download on first run (~4-14GB depending on quantization).

### Option 3: Mock Mode (No LLM Required)

AetherOS works without an LLM using rule-based fallbacks.

```bash
# Just run - it will automatically use mock mode if LLM unavailable
python3 aetheros_minimal.py
```

## LLM Features

The Hermes model is used for:

1. **Prompt Enhancement** - Expands creative prompts with rich detail
2. **Script Generation** - Creates properly formatted scripts
3. **Story Decomposition** - Breaks stories into scenes
4. **Meta-Prompting** - Generates intelligent task execution plans
5. **Content Analysis** - Analyzes quality, ethics, and themes

## Model Selection

### Hermes-2-Pro-Mistral (Recommended)
- **Size**: 7B parameters
- **Strengths**: Excellent instruction following, creative writing
- **RAM**: 4GB (quantized) to 14GB (full precision)
- **Best for**: General creative tasks

### Nous-Hermes2
- **Size**: 7B-70B parameters
- **Strengths**: Balanced reasoning and creativity
- **Best for**: Complex narratives

### Dolphin-Hermes
- **Size**: 7B+ parameters  
- **Strengths**: Uncensored responses, technical tasks
- **Best for**: Unrestricted creative exploration

## Performance Tips

### For Low-End Systems
```bash
# Use smallest quantized model
ollama pull hermes2-pro-mistral:latest

# Reduce max tokens in .env
LLM_MAX_TOKENS=1024
```

### For High-End Systems
```bash
# Use larger models
ollama pull nous-hermes2:70b

# Increase quality
LLM_TEMPERATURE=0.8
LLM_MAX_TOKENS=4096
```

### For Cloud/Server
```bash
# Point to remote Ollama instance
OLLAMA_BASE_URL=http://your-server:11434
```

## Troubleshooting

### "Ollama not responding"
```bash
# Start Ollama service
ollama serve

# Check if running
curl http://localhost:11434/api/tags
```

### "Model not found"
```bash
# Pull the model
ollama pull hermes2-pro-mistral:latest

# List available models
ollama list
```

### "Out of memory"
```bash
# Use 4-bit quantization (HuggingFace)
# Edit .env: HF_USE_QUANTIZED=true

# Or use smaller Ollama model
ollama pull hermes2-pro-mistral:7b-q4_0
```

## Advanced Configuration

See `src/core/llm/llm_config.py` for all available options.

## More Information

- Hermes Models: https://huggingface.co/NousResearch
- Ollama: https://ollama.ai
- Model Cards: https://huggingface.co/NousResearch/Hermes-2-Pro-Mistral-7B

---

**Ready to create?** Run `python3 aetheros_minimal.py` and let Hermes enhance your imagination!

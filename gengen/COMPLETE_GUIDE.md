# 📖 AetherOS Complete Guide

**The Comprehensive Documentation for AetherOS Creative AI System**

---

## Table of Contents

1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Core Architecture](#core-architecture)
4. [User Interfaces](#user-interfaces)
5. [Features & Capabilities](#features--capabilities)
6. [Advanced Usage](#advanced-usage)
7. [Development & Contributing](#development--contributing)
8. [Troubleshooting](#troubleshooting)
9. [Reference](#reference)

---

## Introduction

### What is AetherOS?

AetherOS is a fully open-source, multimodal creative AI system designed to democratize imagination. It enables anyone—regardless of coding ability—to create professional-quality stories, videos, and audio content through natural language prompts.

### Key Philosophy

- **Open & Free:** 100% open-source with transparent licensing
- **No Coding Required:** Natural language interface for all users
- **Multimodal:** Seamlessly integrates text, audio, and video
- **Ethical AI:** Built-in cultural sensitivity and age-appropriateness
- **Memory-Powered:** Learns and remembers context across sessions

### Use Cases

- **Creative Writing:** Generate complete narratives with emotional depth
- **Video Production:** Create cinematic storyboards and animations
- **Audio Stories:** Produce podcast-quality audio narratives
- **Educational Content:** Build engaging learning materials
- **Entertainment:** Develop games, stories, and interactive experiences

---

## Getting Started

### Quick Start Path

```bash
# 1. Navigate to the project directory
cd gengen/

# 2. Launch with one command
./studio.sh

# 3. Follow the interactive prompts
# 4. Start creating!
```

### Installation Modes

#### Minimal Mode (0 MB)
No installation needed! Uses pure Python.

```bash
python3 aetheros_minimal.py
```

**Pros:** Instant start, zero disk space  
**Cons:** Terminal-only interface

#### Web Interface Mode (~50 MB)
Beautiful GUI in your browser.

```bash
pip install gradio
python3 aetheros_interface.py
```

**Pros:** Best user experience, visual interface  
**Cons:** Requires Gradio installation

#### Full Mode (~5 GB)
All advanced features and pipelines.

```bash
pip install -r requirements.txt
python3 aetheros_interface.py
```

**Pros:** Complete functionality, all pipelines  
**Cons:** Large disk space requirement

---

## Core Architecture

### Neural Graph Memory (NGM)

The memory system that gives AetherOS its intelligence.

**Key Features:**
- Graph-based episodic memory
- Vector embeddings for semantic search
- Automatic importance weighting
- Temporal and causal relationship tracking
- 90%+ token cost reduction

**How It Works:**
1. Every generation creates a memory node
2. Nodes are connected by relationships (temporal, semantic, causal)
3. FAISS index enables fast similarity search
4. Graph structure preserves context across sessions

**Code Location:** `src/core/ngm/graph_memory.py`

### Affective Processing Unit (APU)

Emotional intelligence layer for understanding and generating content.

**Key Features:**
- Multi-dimensional emotion detection
- Cultural context awareness
- Valence, arousal, dominance scoring
- Intent extraction
- Age-appropriateness filtering

**How It Works:**
1. Analyzes input text for emotional markers
2. Identifies primary and secondary emotions
3. Evaluates cultural sensitivity
4. Determines narrative tone
5. Assigns age rating

**Code Location:** `src/core/apu/affective_layer.py`

### Recursive Meta-Prompting (RMP) Orchestrator

The cognitive control layer that manages agent swarms.

**Key Features:**
- Self-optimizing task delegation
- Utility-based agent selection
- Dynamic priority management
- Performance tracking and learning
- Parallel execution support

**How It Works:**
1. Breaks complex tasks into subtasks
2. Assigns tasks to specialized agents
3. Monitors execution and performance
4. Adjusts strategies based on results
5. Continuously improves through meta-prompts

**Code Location:** `src/agents/orchestrator.py`

### Agent Swarm

Specialized agents for different creative tasks.

**Available Agents:**
- **PIGC Architect:** Prompt engineering and refinement
- **Memory Agent:** Retrieval and storage operations
- **Ethics Agent:** Content analysis and validation
- **Video Generator:** Visual content creation
- **Audio Generator:** Music and sound synthesis
- **Voice Synthesizer:** Speech and narration
- **Quality Evaluator:** Output assessment and scoring

**Code Location:** `src/agents/orchestrator.py`

---

## User Interfaces

### Web Interface (`aetheros_interface.py`)

**Launch:**
```bash
python3 aetheros_interface.py
# Opens at http://localhost:7860
```

**Features:**

#### Create Tab
- Prompt input field
- Style selection (cinematic, fantastical, noir, etc.)
- Emotional tone controls
- Duration slider
- Output format checkboxes (video, audio, script)
- Generate button

#### History Tab
- List of all generations
- Timestamp and status
- Quick preview
- Re-generate option
- Export functionality

#### Statistics Tab
- Total generations
- Memory usage
- Agent performance
- System metrics
- Processing times

#### Examples Tab
- Pre-made prompts
- Genre templates
- One-click try
- Customize and generate

#### About Tab
- System information
- Version details
- Documentation links
- Credits

### Terminal Interface (`aetheros_minimal.py`)

**Launch:**
```bash
python3 aetheros_minimal.py
```

**Features:**
- Interactive menu system
- Full feature parity with web interface
- Works without external dependencies
- Keyboard navigation
- Status indicators

**Menu Options:**
1. Generate new content
2. View history
3. View statistics
4. About AetherOS
5. Exit

### Smart Launcher (`launch_studio.py`)

**Launch:**
```bash
./studio.sh
# or
python3 launch_studio.py
```

**What It Does:**
1. Checks Python version
2. Detects installed packages
3. Shows disk space
4. Offers installation options
5. Launches best available interface

**Interactive Prompts:**
- Install Gradio? (Yes/No)
- Launch web or terminal? (Auto-selected)
- Install full dependencies? (Optional)

---

## Features & Capabilities

### Content Generation

#### Video Generation
- **Styles:** Cinematic, fantastical, noir, documentary, anime, realistic
- **Formats:** MP4, WebM
- **Resolution:** Up to 1920x1080
- **Duration:** 15-300 seconds
- **Features:** Camera movements, scene transitions, visual effects

#### Audio Generation
- **Types:** Background music, sound effects, ambient audio
- **Formats:** MP3, WAV
- **Quality:** 48kHz, stereo
- **Duration:** 15-300 seconds
- **Features:** Mood-matched music, spatial audio, dynamic mixing

#### Script Generation
- **Formats:** Plain text, JSON, Markdown
- **Elements:** Narrative text, dialogue, scene descriptions
- **Length:** 100-10,000 words
- **Features:** Emotional annotations, character development, plot structure

### Emotional Intelligence

**Emotion Categories:**
- Joy, Trust, Fear, Surprise
- Sadness, Disgust, Anger, Anticipation
- Neutral

**Emotional Dimensions:**
- **Valence:** Negative to Positive (-1 to +1)
- **Arousal:** Calm to Excited (0 to 1)
- **Dominance:** Submissive to Dominant (0 to 1)

**Applications:**
- Mood-appropriate content generation
- Emotional arc planning
- Tone consistency
- Cultural sensitivity

### Memory & Context

**Memory Features:**
- Persistent across sessions
- Automatic context retrieval
- Relationship tracking
- Importance scoring
- Decay management

**Benefits:**
- No need to repeat information
- Builds on previous conversations
- Maintains character/world consistency
- Reduces token usage by 90%+

### Multimodal Integration

**Supported Modalities:**
- Text (prompts, scripts, narration)
- Audio (music, speech, sound effects)
- Video (scenes, animations, effects)
- Images (stills, storyboards, concept art)

**Integration Points:**
- Audio-driven animation (speech to character performance)
- Storyboard-to-video (scene planning to rendering)
- Script-to-audio (text to narration)
- Cross-modal memory (shared context)

---

## Advanced Usage

### Customizing Prompts

**Prompt Structure:**
```
[NARRATIVE] + [STYLE] + [TONE] + [DURATION]
```

**Example:**
```
Narrative: "A lone astronaut discovers an ancient alien artifact"
Style: "cinematic"
Tone: "wonder, mystery, isolation"
Duration: 120 seconds
```

### Working with Memory

**Manual Memory Operations:**
```python
from aetheros_minimal import AetherOS

aether = AetherOS(memory_enabled=True)

# Store important context
aether.memory.store_memory(
    content="The protagonist is afraid of water",
    importance=0.9
)

# Retrieve relevant memories
memories = aether.memory.retrieve(
    query="swimming scene",
    top_k=5
)
```

### Agent Orchestration

**Custom Agent Registration:**
```python
from src.agents.orchestrator import RecursiveMetaPromptingOrchestrator, BaseAgent, AgentRole

orchestrator = RecursiveMetaPromptingOrchestrator()

# Create custom agent
class CustomVideoAgent(BaseAgent):
    async def execute_task(self, task):
        # Custom logic
        pass

# Register
orchestrator.register_agent(
    CustomVideoAgent(AgentRole.VIDEO_GENERATOR, ["rendering", "effects"])
)
```

### Pipeline Development

**Creating Custom Pipelines:**

1. Create pipeline file in `src/pipelines/`
2. Implement pipeline interface
3. Register in orchestrator
4. Document and test

**Example Structure:**
```python
class CustomPipeline:
    def __init__(self, config):
        self.config = config
    
    async def generate(self, input_data):
        # Pipeline logic
        return result
```

---

## Development & Contributing

### Development Setup

```bash
# Clone and navigate
cd gengen/

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install dev tools
pip install black ruff pytest pytest-cov
```

### Code Style

**Formatter:** Black (line length: 88)
```bash
black .
```

**Linter:** Ruff
```bash
ruff check .
ruff check --fix .  # Auto-fix
```

### Testing

```bash
# Run all tests
pytest

# With coverage
pytest --cov=src

# Specific test file
pytest tests/test_memory.py
```

### Project Structure

```
gengen/
├── src/                    # Core source code
│   ├── core/              # Core systems
│   │   ├── ngm/          # Neural Graph Memory
│   │   └── apu/          # Affective Processing
│   ├── agents/            # Agent implementations
│   ├── orchestrator/      # RMP orchestrator
│   └── pipelines/         # Media pipelines
├── aetheros_interface.py  # Web UI
├── aetheros_minimal.py    # Terminal UI
├── run_aetheros.py        # Quick start
├── launch_studio.py       # Launcher
├── requirements.txt       # Dependencies
└── docs/                  # Documentation
```

---

## Troubleshooting

### Installation Issues

**Problem:** "Gradio not found"
```bash
pip install gradio
```

**Problem:** "Out of disk space"
- Use minimal mode (0 MB)
- Install Gradio only (~50 MB)
- Free up space for full install

**Problem:** "Python version error"
```bash
python3 --version  # Check version
# Need 3.8+
```

### Runtime Issues

**Problem:** "Out of memory"
- Reduce duration
- Generate one format at a time
- Use minimal mode
- Close other applications

**Problem:** "GPU not detected"
- Check CUDA installation
- Verify GPU drivers
- System will fall back to CPU

**Problem:** "Port 7860 in use"
```bash
# Check if already running
lsof -i :7860

# Kill existing process
pkill -f aetheros_interface

# Or use different port
python3 aetheros_interface.py --port 8080
```

### Generation Issues

**Problem:** "Generation failed"
- Check prompt length (not too short/long)
- Verify output format selected
- Check available disk space
- Review error message

**Problem:** "Poor quality output"
- Use more descriptive prompts
- Try different styles
- Adjust emotional tones
- Increase duration

---

## Reference

### Command Line Options

**Web Interface:**
```bash
python3 aetheros_interface.py [OPTIONS]

Options:
  --port PORT        Port number (default: 7860)
  --debug           Enable debug mode
  --no-browser      Don't auto-open browser
```

**Launcher:**
```bash
python3 launch_studio.py [OPTIONS]

Options:
  --help            Show help message
  --minimal         Force minimal mode
  --web             Force web mode
  --no-install      Skip installation prompts
```

### Environment Variables

```bash
# Default style
export AETHEROS_DEFAULT_STYLE="cinematic"

# Output directory
export AETHEROS_OUTPUT_DIR="./outputs"

# Memory capacity
export AETHEROS_MEMORY_CAPACITY="100000"

# Debug mode
export AETHEROS_DEBUG="1"
```

### File Formats

**Input:**
- Text prompts (UTF-8)
- Audio files (MP3, WAV, FLAC)
- Configuration (JSON, YAML)

**Output:**
- Video: MP4, WebM
- Audio: MP3, WAV
- Script: TXT, MD, JSON
- Metadata: JSON

### API Reference

**AetherOS Class:**
```python
class AetherOS:
    def __init__(self, mode="creative", memory_enabled=True)
    async def generate(prompt, output_formats, style, duration, emotional_tone)
    def get_statistics()
    def get_history()
```

**Orchestrator Class:**
```python
class RecursiveMetaPromptingOrchestrator:
    def __init__(self)
    def register_agent(agent)
    async def execute(description, priority, metadata)
```

### Glossary

- **NGM:** Neural Graph Memory
- **APU:** Affective Processing Unit
- **RMP:** Recursive Meta-Prompting
- **PIGC:** Prompt Injection Growth Cycle
- **Valence:** Emotional positivity/negativity
- **Arousal:** Emotional intensity
- **Viseme:** Visual representation of phoneme

---

## Additional Resources

### Documentation Files

- `README.md` - Project overview
- `START_HERE.md` - Quick introduction
- `QUICKSTART.md` - Getting started guide
- `LAUNCH_GUIDE.md` - Launch options
- `ROADMAP.md` - Future development
- `STATUS.md` - Current capabilities

### External Resources

- Python Documentation: https://docs.python.org/3/
- Gradio Documentation: https://gradio.app/docs/
- PyTorch Documentation: https://pytorch.org/docs/

---

**Version:** 1.0.0-alpha  
**Last Updated:** November 2024

*"The future of creativity is open, ethical, and free."*

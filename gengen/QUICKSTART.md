# ⚡ AetherOS Quick Start Guide

Get up and running with AetherOS in under 5 minutes!

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- 4 GB RAM minimum

### Quick Install

```bash
# Clone the repository (if you haven't already)
cd gengen/

# Option 1: Minimal (No dependencies needed!)
python3 aetheros_minimal.py

# Option 2: Web Interface (Recommended)
pip install gradio
python3 aetheros_interface.py

# Option 3: Full Installation (Advanced features)
pip install -r requirements.txt
python3 aetheros_interface.py
```

## First Run

### Using the Launcher (Easiest)

```bash
./studio.sh
```

The launcher will:
1. Check your Python environment
2. Detect installed dependencies
3. Offer to install Gradio (optional)
4. Launch the best interface for your setup

### Direct Launch Options

**Web Interface** (if Gradio installed):
```bash
python3 aetheros_interface.py
# Opens at: http://localhost:7860
```

**Terminal Interface** (no dependencies):
```bash
python3 aetheros_minimal.py
```

**Quick Demo** (production example):
```bash
python3 run_aetheros.py
```

## Creating Your First Story

### Example 1: Fantasy Story

```
Prompt: "A young wizard discovers an ancient book that can rewrite reality"
Style: fantastical
Tone: wonder, mystery
Duration: 120 seconds
Outputs: video, audio, script
```

### Example 2: Sci-Fi Adventure

```
Prompt: "An astronaut on Mars discovers signals from beneath the surface"
Style: cinematic
Tone: wonder, fear
Duration: 150 seconds
Outputs: video, script
```

### Example 3: Mystery Thriller

```
Prompt: "A detective receives an anonymous letter about a 20-year-old cold case"
Style: noir
Tone: suspense, mystery
Duration: 90 seconds
Outputs: video, audio, script
```

## Understanding the Output

After generation, you'll receive:

### 📹 Video Output
- Cinematic scene renderings
- Camera movements and transitions
- Visual storytelling

### 🎵 Audio Output
- Background music
- Sound effects
- Ambient audio

### 📝 Script Output
- Full narrative text
- Scene descriptions
- Dialogue (if applicable)

### 📊 Metadata
- Generation ID
- Emotional analysis
- Memory node reference
- Processing statistics

## Configuration Tips

### Performance Tuning

**Low-End System (4-8 GB RAM):**
- Use minimal interface: `python3 aetheros_minimal.py`
- Select shorter durations (30-60 seconds)
- Generate one format at a time

**Mid-Range System (8-16 GB RAM):**
- Use web interface
- Standard durations (60-120 seconds)
- Multiple output formats

**High-End System (16+ GB RAM, GPU):**
- Full web interface
- Extended durations (120-300 seconds)
- All output formats simultaneously

### Output Formats

Choose based on your needs:

- **Script only** - Fastest, minimal resources
- **Audio + Script** - Good for podcasts/audio stories
- **Video + Script** - Full cinematic experience
- **All formats** - Complete multimedia package

## Troubleshooting

### "Gradio not found"
```bash
pip install gradio
```

### "Out of memory"
- Use terminal interface (minimal mode)
- Reduce duration
- Generate one format at a time

### "Port 7860 already in use"
The web interface is already running, or another app is using that port.
- Check: http://localhost:7860
- Or kill existing process: `pkill -f aetheros_interface`

### Python version error
```bash
# Check version
python3 --version

# Upgrade if needed (Ubuntu/Debian)
sudo apt update
sudo apt install python3.8
```

## Next Steps

Now that you're up and running:

1. **Experiment** with different prompts and styles
2. **Review** your generation history
3. **Explore** the statistics tab (web interface)
4. **Read** `LAUNCH_GUIDE.md` for detailed features
5. **Check** `ROADMAP.md` for upcoming features

## Keyboard Shortcuts (Web Interface)

- `Ctrl+Enter` - Submit prompt
- `Ctrl+H` - View history
- `Ctrl+S` - View statistics
- `Ctrl+?` - Show help

## Advanced Usage

### Command Line Arguments

```bash
# Run with custom port
python3 aetheros_interface.py --port 8080

# Enable debug mode
python3 aetheros_interface.py --debug

# Check launcher help
python3 launch_studio.py --help
```

### Environment Variables

```bash
# Set default style
export AETHEROS_DEFAULT_STYLE="cinematic"

# Set output directory
export AETHEROS_OUTPUT_DIR="./my_creations"
```

## Getting Help

- **Documentation**: See `README.md` for complete docs
- **Launch Help**: Run `python3 launch_studio.py --help`
- **Examples**: Check the Examples tab in web interface
- **Issues**: Report bugs on GitHub

---

**Happy Creating!** 🎨🚀

*"The future of creativity is open, ethical, and free."*

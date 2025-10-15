#!/bin/bash
# AetherOS - Universal Launcher: Starts all system components at once

# Activate venv if exists
if [ -d "venv" ]; then
  source venv/bin/activate
fi

# Install required packages if missing
pip install --quiet --upgrade pip
pip install --quiet loguru gradio

# Start orchestrator (background)
python3 src/agents/orchestrator.py &

# Start web interface (foreground)
python3 aetheros_interface.py

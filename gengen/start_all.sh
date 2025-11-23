#!/bin/bash
# AetherOS - Universal Launcher
# Starts all system components at once (orchestrator + web interface)
# Note: This is for advanced users. Most users should use ./studio.sh instead

echo "🚀 AetherOS Universal Launcher"
echo "Starting all system components..."
echo ""

# Activate venv if exists
if [ -d "venv" ]; then
  echo "✓ Activating virtual environment..."
  source venv/bin/activate
fi

# Install required packages if missing
echo "✓ Checking dependencies..."
# Optional: Upgrade pip (non-blocking)
pip install --quiet --upgrade pip 2>/dev/null || true

# Required packages for start_all mode
REQUIRED_PACKAGES="loguru gradio"
if ! pip install --quiet $REQUIRED_PACKAGES; then
  echo "❌ Error: Failed to install required packages ($REQUIRED_PACKAGES)"
  echo "Please install manually: pip install $REQUIRED_PACKAGES"
  exit 1
fi

echo "✓ Starting orchestrator (background)..."
# Start orchestrator (background)
python3 src/agents/orchestrator.py &

echo "✓ Starting web interface..."
echo ""
# Start web interface (foreground)
python3 aetheros_interface.py

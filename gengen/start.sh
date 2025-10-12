#!/bin/bash
# AetherOS - Quick Start Script
# Run this to start the system

echo "🚀 Starting AetherOS..."
echo ""

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python 3 detected"
echo ""

# Run the minimal demo
python3 aetheros_minimal.py

echo ""
echo "✨ AetherOS run complete!"
echo ""
echo "📚 Next steps:"
echo "  • Modify prompts in aetheros_minimal.py"
echo "  • Read QUICKSTART.md for full guide"
echo "  • Explore src/ for complete implementation"
echo ""

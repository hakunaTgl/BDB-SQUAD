#!/bin/bash
# AetherOS Quick Start Script
# This is a simple wrapper that calls the studio launcher

echo "🚀 Starting AetherOS..."
echo ""
echo "Tip: For more options, use './studio.sh' directly"
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Call the studio launcher
./studio.sh "$@"

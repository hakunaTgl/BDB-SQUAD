#!/bin/bash
# AetherOS Quick Start Script
# This is a simple wrapper that calls the studio launcher

echo "🚀 Starting AetherOS..."
echo ""
echo "Tip: For more options, use './studio.sh' directly"
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Change to the script directory
if ! cd "$SCRIPT_DIR"; then
  echo "❌ Error: Could not change to script directory"
  exit 1
fi

# Call the studio launcher
./studio.sh "$@"

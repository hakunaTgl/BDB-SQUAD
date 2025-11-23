#!/bin/bash
# AetherOS Quick Start Script
# This is a simple wrapper that calls the studio launcher

echo "🚀 Starting AetherOS..."
echo ""
echo "Tip: For more options, use './studio.sh' directly"
echo ""

# Change to the script directory
# Use BASH_SOURCE for consistency with studio.sh
SCRIPT_DIR="$(dirname "${BASH_SOURCE[0]}")"
if ! cd "$SCRIPT_DIR"; then
  echo "❌ Error: Could not change to script directory"
  exit 1
fi

# Call the studio launcher
./studio.sh "$@"

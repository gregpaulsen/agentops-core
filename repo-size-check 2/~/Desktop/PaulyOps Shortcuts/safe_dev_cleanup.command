#!/bin/bash

# PaulyOps Safe Dev Cleanup - Desktop Shortcut
# This shortcut runs the safe cleanup from the new PaulyOps location

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🧹 PaulyOps Safe Dev Cleanup${NC}"
echo "=================================="

# Run from the new PaulyOps location
cd "$HOME/PaulyOps/Coding_Commands"

# Run the Python script with arguments
python3 safe_dev_cleanup.py "$@"

echo -e "${GREEN}✅ Safe cleanup complete${NC}"

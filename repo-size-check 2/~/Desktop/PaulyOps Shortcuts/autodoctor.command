#!/bin/bash

# PaulyOps Auto-Doctor - Desktop Shortcut
# Self-healing agent that fixes common issues before health checks

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🩺 PaulyOps Auto-Doctor${NC}"
echo "=========================="

# Check for dry-run flag
if [[ "$*" == *"--dry-run"* ]]; then
    echo -e "${YELLOW}🔍 DRY RUN MODE - No changes will be made${NC}"
fi

# Run from the PaulyOps location
cd "$HOME/PaulyOps/Coding_Commands"

# Run the Python script with all arguments
python3 system_autodoctor.py "$@"

echo -e "${GREEN}✅ Auto-Doctor complete!${NC}"

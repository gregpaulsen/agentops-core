#!/bin/bash

# PaulyOps System Health - Desktop Shortcut
# This shortcut runs the system health audit from the new PaulyOps location

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔍 PaulyOps System Health Audit${NC}"
echo "====================================="

# Run from the new PaulyOps location
cd "$HOME/PaulyOps/Coding_Commands"

# Ensure we're in the correct directory for Git checks
cd "$HOME/Desktop/repo-size-check"

# Run the Python script
python3 "$HOME/PaulyOps/Coding_Commands/system_health.py"

echo -e "${GREEN}✅ System health audit complete${NC}"
echo "📄 Report saved to: ~/PaulyOps/System_Health_Report.md"

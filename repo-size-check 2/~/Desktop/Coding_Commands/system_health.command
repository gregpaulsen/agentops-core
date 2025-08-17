#!/bin/bash

# System Health Command Wrapper
# This script runs the system health audit from the correct directory

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔍 Running System Health Audit${NC}"
echo "=================================="

# Ensure we're in the correct directory for Git checks
cd "$HOME/Desktop/repo-size-check"

# Run the Python script
python3 "$HOME/Desktop/Coding_Commands/system_health.py"

echo -e "${GREEN}✅ System health audit complete${NC}"
echo "📄 Report saved to: ~/Desktop/System_Health_Report.md"

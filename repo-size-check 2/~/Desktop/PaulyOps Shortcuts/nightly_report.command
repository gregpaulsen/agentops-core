#!/bin/bash

# PaulyOps Nightly Report - Desktop Shortcut
# This shortcut runs the nightly email report from the new PaulyOps location

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}📧 PaulyOps Nightly Report${NC}"
echo "==============================="

# Run from the new PaulyOps location
cd "$HOME/PaulyOps/Coding_Commands"

# Run the Python script
python3 nightly_report.py

echo -e "${GREEN}✅ Nightly report complete${NC}"
echo "📄 Report saved to: ~/PaulyOps/Reports/Nightly_Update_Report_$(date +%Y-%m-%d).md"

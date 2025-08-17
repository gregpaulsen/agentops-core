#!/bin/bash

# Nightly Report Command Wrapper
# This script runs the nightly email report

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}📧 Running Nightly Report${NC}"
echo "=============================="

# Run the Python script
python3 "$HOME/Desktop/Coding_Commands/nightly_report.py"

echo -e "${GREEN}✅ Nightly report complete${NC}"
echo "📄 Report saved to: ~/Desktop/Reports/Nightly_Update_Report_$(date +%Y-%m-%d).md"

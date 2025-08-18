#!/bin/bash

# Nightly Report Command Wrapper
# This script runs the nightly report Python script and logs the output

set -e

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/nightly_report.py"
LOG_DIR="$HOME/Desktop/Reports"
LOG_FILE="$LOG_DIR/nightly_report_$(date +%Y%m%d_%H%M%S).log"

# Ensure log directory exists
mkdir -p "$LOG_DIR"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo "🌙 Nightly Report Command Wrapper"
echo "=================================="
echo "Started: $(date)"
echo "Python Script: $PYTHON_SCRIPT"
echo "Log File: $LOG_FILE"
echo ""

# Check if Python script exists
if [[ ! -f "$PYTHON_SCRIPT" ]]; then
    echo -e "${RED}❌ Error: Python script not found at $PYTHON_SCRIPT${NC}"
    exit 1
fi

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Error: Python 3 is not installed or not in PATH${NC}"
    exit 1
fi

# Run the nightly report script
echo -e "${BLUE}🚀 Running nightly report script...${NC}"
echo ""

# Execute the Python script and capture output
if python3 "$PYTHON_SCRIPT" 2>&1 | tee "$LOG_FILE"; then
    echo ""
    echo -e "${GREEN}✅ Nightly report completed successfully!${NC}"
    echo -e "${GREEN}📝 Log saved to: $LOG_FILE${NC}"
    
    # Show log file location
    echo ""
    echo "📄 Report Files:"
    ls -la "$LOG_DIR"/Nightly_Update_Report_*.md 2>/dev/null || echo "  No report files found"
    
    # Show sent marker
    if [[ -f "$LOG_DIR/.nightly_last_sent" ]]; then
        marker_time=$(stat -f "%Sm" "$LOG_DIR/.nightly_last_sent")
        echo -e "${GREEN}📧 Email sent marker updated: $marker_time${NC}"
    fi
    
    exit 0
else
    echo ""
    echo -e "${RED}❌ Nightly report failed!${NC}"
    echo -e "${RED}📝 Check log file for details: $LOG_FILE${NC}"
    exit 1
fi

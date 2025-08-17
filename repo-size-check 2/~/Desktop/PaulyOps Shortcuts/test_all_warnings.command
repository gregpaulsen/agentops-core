#!/bin/bash

# PaulyOps Test All Warnings - Desktop Shortcut
# This shortcut tests all system warnings and shows current status

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🧪 PaulyOps Test All Warnings${NC}"
echo "=================================="

# Run from the new PaulyOps location
cd "$HOME/Desktop/repo-size-check"

# Run the Python script
python3 "$HOME/PaulyOps/Coding_Commands/system_health.py"

echo ""
echo -e "${BLUE}📊 Status Summary:${NC}"
echo "======================"

# Check status flags
echo -e "${YELLOW}📋 Status Flags:${NC}"
if [[ -f "$HOME/PaulyOps/config/status_flags.json" ]]; then
    cat "$HOME/PaulyOps/config/status_flags.json" | python3 -m json.tool
else
    echo "❌ Status flags file not found"
fi

echo ""
echo -e "${YELLOW}📁 Success Markers:${NC}"
ls -la "$HOME/PaulyOps/Reports/".* 2>/dev/null | grep -E "\.(backup|router|nightly)" || echo "No success markers found"

echo ""
echo -e "${GREEN}✅ Test complete!${NC}"

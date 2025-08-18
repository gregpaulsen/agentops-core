#!/bin/bash
# PaulyOps System Integrity Checker
# Verifies that critical files haven't been modified or deleted

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}🔍 PaulyOps System Integrity Check${NC}"
echo "====================================="

PAULYOPS_ROOT="$HOME/PaulyOps"
INTEGRITY_FAILED=false

# Check if protection marker exists
if [ ! -f "$PAULYOPS_ROOT/.protected" ]; then
    echo -e "${RED}❌ System protection marker missing!${NC}"
    INTEGRITY_FAILED=true
else
    echo -e "${GREEN}✅ Protection marker found${NC}"
fi

# Check critical files
CRITICAL_FILES=(
    "scripts/system_health.py"
    "scripts/system_autodoctor.py"
    "scripts/nightly_report.py"
    "config/status_flags.json"
    "config/.env"
)

for file in "${CRITICAL_FILES[@]}"; do
    if [ ! -f "$PAULYOPS_ROOT/$file" ]; then
        echo -e "${RED}❌ Critical file missing: $file${NC}"
        INTEGRITY_FAILED=true
    else
        echo -e "${GREEN}✅ Found: $file${NC}"
    fi
done

# Check LaunchAgent
if [ ! -f "$HOME/Library/LaunchAgents/com.paulyops.nightlyreport.plist" ]; then
    echo -e "${RED}❌ LaunchAgent missing!${NC}"
    INTEGRITY_FAILED=true
else
    echo -e "${GREEN}✅ LaunchAgent found${NC}"
fi

# Check desktop shortcuts
SHORTCUTS=(
    "system_health.command"
    "autodoctor.command"
    "nightly_report.command"
)

for shortcut in "${SHORTCUTS[@]}"; do
    if [ ! -f "$HOME/Desktop/PaulyOps Shortcuts/$shortcut" ]; then
        echo -e "${RED}❌ Desktop shortcut missing: $shortcut${NC}"
        INTEGRITY_FAILED=true
    else
        echo -e "${GREEN}✅ Found: $shortcut${NC}"
    fi
done

if [ "$INTEGRITY_FAILED" = true ]; then
    echo -e "${RED}❌ System integrity check FAILED${NC}"
    echo -e "${YELLOW}⚠️ Run recover_system.command to restore missing files${NC}"
    exit 1
else
    echo -e "${GREEN}✅ System integrity check PASSED${NC}"
fi

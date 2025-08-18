#!/bin/bash
# PaulyOps Emergency Recovery
# Automatically triggered if system integrity is compromised

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${RED}🚨 PAULYOPS EMERGENCY RECOVERY${NC}"
echo "=================================="

PAULYOPS_ROOT="$HOME/PaulyOps"

# Check if PaulyOps root exists
if [ ! -d "$PAULYOPS_ROOT" ]; then
    echo -e "${RED}❌ CRITICAL: PaulyOps root directory missing!${NC}"
    echo -e "${YELLOW}⚠️ Attempting to restore from backup...${NC}"
    
    # Try to restore from backup
    if [ -d "/Volumes/BigSkyAgSSD/BigSkyAg/00_Admin/Backups" ]; then
        echo "Found backup location, attempting restore..."
        # This would restore the PaulyOps structure
        echo -e "${YELLOW}⚠️ Manual intervention required to restore PaulyOps${NC}"
    else
        echo -e "${RED}❌ No backup location found${NC}"
    fi
    exit 1
fi

# Run system recovery
echo -e "${BLUE}🔄 Running system recovery...${NC}"
cd "$PAULYOPS_ROOT/scripts"
./recover_system.command

echo -e "${GREEN}✅ Emergency recovery complete!${NC}"

#!/bin/bash
# PaulyOps System Integrity Check - Desktop Shortcut
set -e
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'
echo -e "${BLUE}🔍 PaulyOps System Integrity Check${NC}"
echo "====================================="
cd "$HOME/PaulyOps/scripts"
./check_integrity.command

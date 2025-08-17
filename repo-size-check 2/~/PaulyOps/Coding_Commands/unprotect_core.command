#!/bin/bash

# PaulyOps Core Unprotection Script
# Removes protection flags for development or updates
# Use with caution - only run when you need to modify core files

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${YELLOW}⚠️  PaulyOps Core Unprotection${NC}"
echo "====================================="
echo -e "${RED}⚠️  WARNING: This removes protection from critical files${NC}"
echo -e "${RED}⚠️  Only run this when you need to modify core files${NC}"
echo ""

read -p "Are you sure you want to remove protection? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo -e "${BLUE}❌ Protection removal cancelled${NC}"
    exit 1
fi

echo -e "${BLUE}🔓 Removing immutable flags from critical files...${NC}"

# Core Python scripts
chflags nouchg ~/PaulyOps/Coding_Commands/system_health.py
chflags nouchg ~/PaulyOps/Coding_Commands/system_autodoctor.py
chflags nouchg ~/PaulyOps/Coding_Commands/nightly_report.py
chflags nouchg ~/PaulyOps/Coding_Commands/create_backup_zip_cleaned.py

# Configuration files
chflags nouchg ~/PaulyOps/config/status_flags.json
chflags nouchg ~/PaulyOps/config/.env

# LaunchAgent
chflags nouchg ~/Library/LaunchAgents/com.paulyops.nightlyreport.plist

# Desktop shortcuts
chflags nouchg ~/Desktop/PaulyOps\ Shortcuts/system_health.command
chflags nouchg ~/Desktop/PaulyOps\ Shortcuts/autodoctor.command
chflags nouchg ~/Desktop/PaulyOps\ Shortcuts/nightly_report.command
chflags nouchg ~/Desktop/PaulyOps\ Shortcuts/recover_system.command

echo -e "${GREEN}✅ Immutable flags removed from critical files${NC}"

# Set write permissions on config directory
echo -e "${BLUE}📁 Setting write permissions on config directory...${NC}"
chmod 644 ~/PaulyOps/config/*.json
chmod 644 ~/PaulyOps/config/.env

echo -e "${GREEN}✅ Configuration files set to writable${NC}"

# Remove protection marker
echo -e "${BLUE}🏷️  Removing protection marker...${NC}"
chflags nouchg ~/PaulyOps/.protected
rm -f ~/PaulyOps/.protected

echo -e "${GREEN}✅ Core unprotection complete!${NC}"
echo -e "${YELLOW}⚠️  Remember to run protect_core.command when done${NC}"

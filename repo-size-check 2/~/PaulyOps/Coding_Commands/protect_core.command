#!/bin/bash

# PaulyOps Core Protection Script
# Prevents accidental deletion or modification of critical system files
# Run this to lock down the system for production use

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🛡️  PaulyOps Core Protection${NC}"
echo "=================================="

# Set immutable flags on critical files
echo -e "${BLUE}🔒 Setting immutable flags on critical files...${NC}"

# Core Python scripts
chflags uchg ~/PaulyOps/Coding_Commands/system_health.py
chflags uchg ~/PaulyOps/Coding_Commands/system_autodoctor.py
chflags uchg ~/PaulyOps/Coding_Commands/nightly_report.py
chflags uchg ~/PaulyOps/Coding_Commands/create_backup_zip_cleaned.py

# Configuration files
chflags uchg ~/PaulyOps/config/status_flags.json
chflags uchg ~/PaulyOps/config/.env

# LaunchAgent
chflags uchg ~/Library/LaunchAgents/com.paulyops.nightlyreport.plist

# Desktop shortcuts
chflags uchg ~/Desktop/PaulyOps\ Shortcuts/system_health.command
chflags uchg ~/Desktop/PaulyOps\ Shortcuts/autodoctor.command
chflags uchg ~/Desktop/PaulyOps\ Shortcuts/nightly_report.command
chflags uchg ~/Desktop/PaulyOps\ Shortcuts/recover_system.command

echo -e "${GREEN}✅ Critical files protected with immutable flags${NC}"

# Set read-only on config directory
echo -e "${BLUE}📁 Setting read-only on config directory...${NC}"
chmod 444 ~/PaulyOps/config/*.json
chmod 444 ~/PaulyOps/config/.env

echo -e "${GREEN}✅ Configuration files set to read-only${NC}"

# Create protection marker
echo -e "${BLUE}🏷️  Creating protection marker...${NC}"
echo "PaulyOps Core Protection Active - $(date)" > ~/PaulyOps/.protected
chflags uchg ~/PaulyOps/.protected

echo -e "${GREEN}✅ Core protection complete!${NC}"
echo -e "${YELLOW}⚠️  To remove protection, run: unprotect_core.command${NC}"

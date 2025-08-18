#!/bin/bash

# Quick Fix Script for Immediate Critical Issues
# This script addresses the 3 critical failures found in system health check

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo "🔧 Quick Fix Script for Critical Issues"
echo "======================================="
echo "Started: $(date)"
echo ""

# Function to create directory if it doesn't exist
create_dir_if_missing() {
    local dir="$1"
    local description="$2"
    
    if [[ ! -d "$dir" ]]; then
        echo -e "${BLUE}📁 Creating $description: $dir${NC}"
        mkdir -p "$dir"
        echo -e "${GREEN}✅ Created: $dir${NC}"
    else
        echo -e "${GREEN}✅ $description already exists: $dir${NC}"
    fi
}

# Function to check Git repository status
check_git_repo() {
    local repo_dir="$1"
    echo -e "${BLUE}🔍 Checking Git repository: $repo_dir${NC}"
    
    cd "$repo_dir"
    
    if [[ -d ".git" ]]; then
        echo -e "${GREEN}✅ Git repository found${NC}"
        git status --porcelain | head -5
        echo ""
    else
        echo -e "${YELLOW}⚠️  Not a Git repository${NC}"
        echo -e "${BLUE}🔧 Initializing Git repository...${NC}"
        git init
        echo -e "${GREEN}✅ Git repository initialized${NC}"
    fi
}

echo "🚀 Starting fixes for critical issues..."
echo ""

# Fix 1: Create missing directories
echo "📁 FIX 1: Creating missing directories"
echo "----------------------------------------"
create_dir_if_missing "$HOME/Desktop/BigSkyAgDropzone" "BigSkyAg Dropzone"
create_dir_if_missing "$HOME/Desktop/Backups" "Backups Directory"
create_dir_if_missing "$HOME/Desktop/Archives" "Archives Directory"
create_dir_if_missing "logs" "Logs Directory"
echo ""

# Fix 2: Check Git repository
echo "🔧 FIX 2: Verifying Git repository"
echo "-----------------------------------"
check_git_repo "$HOME/Desktop/repo-size-check"
echo ""

# Fix 3: Create basic log files if they don't exist
echo "📝 FIX 3: Creating basic log files"
echo "-----------------------------------"
if [[ ! -f "logs/backup.log" ]]; then
    echo -e "${BLUE}📝 Creating backup.log${NC}"
    echo "# Backup Log - Created $(date)" > logs/backup.log
    echo -e "${GREEN}✅ Created: logs/backup.log${NC}"
else
    echo -e "${GREEN}✅ backup.log already exists${NC}"
fi

if [[ ! -f "logs/router.log" ]]; then
    echo -e "${BLUE}📝 Creating router.log${NC}"
    echo "# Router Log - Created $(date)" > logs/router.log
    echo -e "${GREEN}✅ Created: logs/router.log${NC}"
else
    echo -e "${GREEN}✅ router.log already exists${NC}"
fi
echo ""

# Summary
echo "🎯 QUICK FIXES COMPLETED"
echo "========================="
echo "✅ Created missing directories"
echo "✅ Verified Git repository"
echo "✅ Created basic log files"
echo ""

echo -e "${BLUE}🔍 Now running system health check to verify fixes...${NC}"
echo ""

# Run system health check
if ~/Desktop/Coding_Commands/system_health.command; then
    echo ""
    echo -e "${GREEN}🎉 SUCCESS! All critical issues resolved!${NC}"
    echo -e "${GREEN}🚀 System is now ready for UI development!${NC}"
else
    echo ""
    echo -e "${YELLOW}⚠️  Some issues remain - check the health report above${NC}"
    echo -e "${BLUE}🔧 Additional fixes may be needed${NC}"
fi

echo ""
echo "📋 NEXT STEPS:"
echo "1. Review the system health report above"
echo "2. Test backup functionality if needed"
echo "3. Verify dropzone file processing"
echo "4. Begin UI development once all checks pass"

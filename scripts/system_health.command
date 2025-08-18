#!/bin/bash

# Enhanced System Health Check Command Wrapper
# This script runs the comprehensive system health checker

set -e

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_SCRIPT="$SCRIPT_DIR/system_health.py"
PROJECT_ROOT="$SCRIPT_DIR/../.."
LOG_DIR="$HOME/Desktop/Reports"

# Ensure log directory exists
mkdir -p "$LOG_DIR"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo "🔍 Enhanced System Health Check"
echo "================================"
echo "Started: $(date)"
echo "Python Script: $PYTHON_SCRIPT"
echo "Project Root: $PROJECT_ROOT"
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

# Change to project root directory
echo -e "${BLUE}📁 Changing to project directory: $PROJECT_ROOT${NC}"
cd "$PROJECT_ROOT"

# Ensure we're in the repo directory for Git checks
if [[ -d ".git" ]]; then
    echo -e "${GREEN}✅ Found Git repository in current directory${NC}"
else
    echo -e "${YELLOW}⚠️  No Git repository found, checking parent directories...${NC}"
    # Look for Git repository in parent directories
    cd "$HOME/Desktop/repo-size-check"
    if [[ -d ".git" ]]; then
        echo -e "${GREEN}✅ Found Git repository in repo-size-check${NC}"
    else
        echo -e "${RED}❌ No Git repository found${NC}"
    fi
fi

# Run the system health check
echo -e "${BLUE}🚀 Running enhanced system health check...${NC}"
echo ""

# Execute the Python script
if python3 "$PYTHON_SCRIPT"; then
    echo ""
    echo -e "${GREEN}✅ System health check completed successfully!${NC}"
    
    # Show generated reports
    echo ""
    echo "📄 Generated Reports:"
    ls -la "$LOG_DIR"/system_health_*.md 2>/dev/null | tail -3 || echo "  No health reports found"
    
    # Show nightly email status
    if [[ -f "$LOG_DIR/.nightly_last_sent" ]]; then
        marker_time=$(stat -f "%Sm" "$LOG_DIR/.nightly_last_sent")
        echo -e "${GREEN}📧 Last nightly email sent: $marker_time${NC}"
    else
        echo -e "${YELLOW}⚠️  No nightly email sent marker found${NC}"
    fi
    
    exit 0
else
    echo ""
    echo -e "${RED}❌ System health check failed!${NC}"
    echo -e "${RED}🔧 Please review the output above and fix any critical issues${NC}"
    exit 1
fi

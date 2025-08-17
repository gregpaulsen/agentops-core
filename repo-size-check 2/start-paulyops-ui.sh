#!/bin/bash

# PaulyOps UI Startup Script
# This script ensures everything runs from the correct directory

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 PaulyOps UI Startup Script${NC}"
echo "=================================="

# Check if we're in the right directory
if [[ ! -f "package.json" ]] || [[ ! -d "server" ]]; then
    echo -e "${RED}❌ Error: Not in paulyops-ui directory${NC}"
    echo "Please run this script from: /Users/gregpaulsen/Desktop/paulyops-ui"
    exit 1
fi

echo -e "${GREEN}✅ Correct directory confirmed${NC}"

# Check if dependencies are installed
if [[ ! -d "node_modules" ]]; then
    echo -e "${YELLOW}📦 Installing dependencies...${NC}"
    npm install
fi

# Check if server files exist
if [[ ! -f "server/server.cjs" ]]; then
    echo -e "${RED}❌ Error: server/server.cjs not found${NC}"
    exit 1
fi

echo -e "${GREEN}✅ All files present${NC}"

# Function to start backend
start_backend() {
    echo -e "${BLUE}🔧 Starting backend server...${NC}"
    echo "Backend will run on: http://localhost:8787"
    echo "Press Ctrl+C to stop"
    echo ""
    node server/server.cjs
}

# Function to start frontend
start_frontend() {
    echo -e "${BLUE}🎨 Starting frontend...${NC}"
    echo "Frontend will run on: http://localhost:5173"
    echo "Press Ctrl+C to stop"
    echo ""
    npm run dev
}

# Check command line arguments
case "${1:-both}" in
    "backend"|"server")
        start_backend
        ;;
    "frontend"|"dev")
        start_frontend
        ;;
    "both"|"")
        echo -e "${YELLOW}📋 Starting both frontend and backend...${NC}"
        echo "You'll need two terminal windows:"
        echo ""
        echo "Terminal 1 (Backend):"
        echo "  ./start-paulyops-ui.sh backend"
        echo ""
        echo "Terminal 2 (Frontend):"
        echo "  ./start-paulyops-ui.sh frontend"
        echo ""
        echo "Or use: npm run server-simple (backend) and npm run dev (frontend)"
        echo ""
        echo -e "${GREEN}🎯 Quick start:${NC}"
        echo "1. Backend:  npm run server-simple"
        echo "2. Frontend: npm run dev"
        echo "3. Open:     http://localhost:5173"
        ;;
    *)
        echo "Usage: $0 [backend|frontend|both]"
        echo "  backend  - Start backend server only"
        echo "  frontend - Start frontend only"
        echo "  both     - Show instructions for both (default)"
        ;;
esac

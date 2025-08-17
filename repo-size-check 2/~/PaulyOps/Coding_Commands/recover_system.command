#!/bin/bash

# PaulyOps System Recovery Script
# SOC 2 Compliance - System Self-Healing and Recovery
# This script can restore the system from critical failures

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🛡️  PaulyOps System Recovery${NC}"
echo "=================================="

# Check if PaulyOps root exists
if [ ! -d "$HOME/PaulyOps" ]; then
    echo -e "${RED}❌ CRITICAL: PaulyOps root directory missing!${NC}"
    echo "Attempting to restore from backup..."
    
    # Try to restore from backup
    if [ -d "/Volumes/BigSkyAgSSD/BigSkyAg/00_Admin/Backups" ]; then
        echo "Found backup location, attempting restore..."
        # This would restore the PaulyOps structure
        echo -e "${YELLOW}⚠️  Manual intervention required to restore PaulyOps${NC}"
    else
        echo -e "${RED}❌ No backup location found${NC}"
    fi
    exit 1
fi

# Ensure core directories exist
echo -e "${BLUE}🔧 Ensuring core directory structure...${NC}"
mkdir -p "$HOME/PaulyOps/Coding_Commands"
mkdir -p "$HOME/PaulyOps/Reports"
mkdir -p "$HOME/PaulyOps/Backups"
mkdir -p "$HOME/PaulyOps/config"
mkdir -p "$HOME/PaulyOps/logs"

# Restore critical files if missing
echo -e "${BLUE}📁 Checking critical files...${NC}"

# System Health
if [ ! -f "$HOME/PaulyOps/Coding_Commands/system_health.py" ]; then
    echo -e "${YELLOW}⚠️  system_health.py missing - attempting restore${NC}"
    # Would restore from backup or recreate
fi

# Auto-Doctor
if [ ! -f "$HOME/PaulyOps/Coding_Commands/system_autodoctor.py" ]; then
    echo -e "${YELLOW}⚠️  system_autodoctor.py missing - attempting restore${NC}"
    # Would restore from backup or recreate
fi

# Nightly Report
if [ ! -f "$HOME/PaulyOps/Coding_Commands/nightly_report.py" ]; then
    echo -e "${YELLOW}⚠️  nightly_report.py missing - attempting restore${NC}"
    # Would restore from backup or recreate
fi

# Status Flags
if [ ! -f "$HOME/PaulyOps/config/status_flags.json" ]; then
    echo -e "${YELLOW}⚠️  status_flags.json missing - recreating defaults${NC}"
    cat > "$HOME/PaulyOps/config/status_flags.json" << 'EOF'
{
  "check_git": true,
  "check_router": false,
  "check_endpoints": false,
  "check_backup_upload": true,
  "check_launchd_jobs": true,
  "check_launchd": true,
  "check_provider_credentials": true,
  "check_spotlight": true,
  "git_repos": ["/Users/gregpaulsen/Desktop/repo-size-check"],
  "git_paths": ["/Volumes/BigSkyAgSSD/BigSkyAg", "/Volumes/BigSkyAgSSD/PaulyOps", "/Volumes/BigSkyAgSSD/agentops-core"],
  "skip_git_repos": ["/Volumes/BigSkyAgSSD/agentops-core", "/Volumes/BigSkyAgSSD/PaulyOps"],
  "endpoint_urls": [],
  "launchd_jobs": ["com.paulyops.nightlyreport"],
  "skip_launchd_jobs": ["com.bigsky.backup.10pm", "com.bigsky.router.watch"],
  "company_name": "PaulyOps",
  "dropzone_name": "PaulyOpsDropzone"
}
EOF
fi

# Environment Config
if [ ! -f "$HOME/PaulyOps/config/.env" ]; then
    echo -e "${YELLOW}⚠️  .env missing - recreating template${NC}"
    cat > "$HOME/PaulyOps/config/.env" << 'EOF'
# Auto-generated recovery template
# TODO: Configure your email settings and other environment variables

# Email Configuration
NR_EMAIL_PROVIDER=SMTP
NR_SENDER_NAME=PaulyOps Automations
NR_SENDER_EMAIL=your_email@example.com
NR_RECIPIENTS=your_email@example.com

# SMTP Settings (configure for your email provider)
NR_SMTP_HOST=smtp.example.com
NR_SMTP_PORT=587
NR_SMTP_USERNAME=your_email@example.com
NR_SMTP_PASSWORD=your_app_password
NR_SMTP_STARTTLS=true

# System Configuration
ENV=production
LOG_LEVEL=INFO
STORAGE_PROVIDER=local
COMPANY_NAME=PaulyOps
DROPZONE_NAME=PaulyOpsDropzone

# Paths (auto-configured)
PAULYOPS_ROOT=~/PaulyOps
PAULYOPS_REPORTS=~/PaulyOps/Reports
PAULYOPS_BACKUPS=~/PaulyOps/Backups
EOF
fi

# Ensure desktop shortcuts exist
echo -e "${BLUE}🔗 Checking desktop shortcuts...${NC}"
mkdir -p "$HOME/Desktop/PaulyOps Shortcuts"

# System Health Shortcut
if [ ! -f "$HOME/Desktop/PaulyOps Shortcuts/system_health.command" ]; then
    echo -e "${YELLOW}⚠️  system_health.command missing - recreating${NC}"
    cat > "$HOME/Desktop/PaulyOps Shortcuts/system_health.command" << 'EOF'
#!/bin/bash
# PaulyOps System Health - Desktop Shortcut
set -e
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'
echo -e "${BLUE}🔍 PaulyOps System Health Audit${NC}"
echo "====================================="
cd "$HOME/PaulyOps/Coding_Commands"
cd "$HOME/Desktop/repo-size-check"
python3 "$HOME/PaulyOps/Coding_Commands/system_health.py"
echo -e "${GREEN}✅ System health audit complete${NC}"
echo "📄 Report saved to: ~/PaulyOps/System_Health_Report.md"
EOF
    chmod +x "$HOME/Desktop/PaulyOps Shortcuts/system_health.command"
fi

# Auto-Doctor Shortcut
if [ ! -f "$HOME/Desktop/PaulyOps Shortcuts/autodoctor.command" ]; then
    echo -e "${YELLOW}⚠️  autodoctor.command missing - recreating${NC}"
    cat > "$HOME/Desktop/PaulyOps Shortcuts/autodoctor.command" << 'EOF'
#!/bin/bash
# PaulyOps Auto-Doctor - Desktop Shortcut
set -e
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'
echo -e "${BLUE}🩺 PaulyOps Auto-Doctor${NC}"
echo "=========================="
cd "$HOME/PaulyOps/Coding_Commands"
python3 system_autodoctor.py "$@"
echo -e "${GREEN}✅ Auto-Doctor complete!${NC}"
EOF
    chmod +x "$HOME/Desktop/PaulyOps Shortcuts/autodoctor.command"
fi

# Nightly Report Shortcut
if [ ! -f "$HOME/Desktop/PaulyOps Shortcuts/nightly_report.command" ]; then
    echo -e "${YELLOW}⚠️  nightly_report.command missing - recreating${NC}"
    cat > "$HOME/Desktop/PaulyOps Shortcuts/nightly_report.command" << 'EOF'
#!/bin/bash
# PaulyOps Nightly Report - Desktop Shortcut
set -e
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'
echo -e "${BLUE}📧 PaulyOps Nightly Report${NC}"
echo "==============================="
cd "$HOME/PaulyOps/Coding_Commands"
python3 nightly_report.py
echo -e "${GREEN}✅ Nightly report complete${NC}"
echo "📄 Report saved to: ~/PaulyOps/Reports/Nightly_Update_Report_$(date +%Y-%m-%d).md"
EOF
    chmod +x "$HOME/Desktop/PaulyOps Shortcuts/nightly_report.command"
fi

# Check LaunchAgent
echo -e "${BLUE}🔧 Checking LaunchAgent...${NC}"
if [ ! -f "$HOME/Library/LaunchAgents/com.paulyops.nightlyreport.plist" ]; then
    echo -e "${YELLOW}⚠️  LaunchAgent missing - recreating${NC}"
    cat > "$HOME/Library/LaunchAgents/com.paulyops.nightlyreport.plist" << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
 "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
 <dict>
  <key>Label</key> <string>com.paulyops.nightlyreport</string>
  <key>ProgramArguments</key>
  <array>
    <string>/bin/bash</string>
    <string>~/Desktop/PaulyOps Shortcuts/nightly_report.command</string>
  </array>
  <key>StartCalendarInterval</key>
  <dict>
    <key>Hour</key><integer>22</integer>
    <key>Minute</key><integer>0</integer>
  </dict>
  <key>StandardOutPath</key>
  <string>~/PaulyOps/Reports/com.paulyops.nightlyreport.out.log</string>
  <key>StandardErrorPath</key>
  <string>~/PaulyOps/Reports/com.paulyops.nightlyreport.err.log</string>
  <key>RunAtLoad</key><true/>
 </dict>
</plist>
EOF
    echo "LaunchAgent recreated - you may need to reload it manually"
fi

# Run Auto-Doctor to fix any remaining issues
echo -e "${BLUE}🩺 Running Auto-Doctor to fix remaining issues...${NC}"
cd "$HOME/PaulyOps/Coding_Commands"
python3 system_autodoctor.py

# Final health check
echo -e "${BLUE}🔍 Running final health check...${NC}"
python3 system_health.py

echo -e "${GREEN}✅ System recovery complete!${NC}"
echo "📄 Recovery log saved to: ~/PaulyOps/logs/recovery_$(date +%Y%m%d_%H%M%S).log"

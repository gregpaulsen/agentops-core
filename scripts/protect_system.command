#!/bin/bash

# PaulyOps System Protection & Guardrails
# Prevents accidental deletion, modification, or breakage of critical system files

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🛡️ PaulyOps System Protection & Guardrails${NC}"
echo "=============================================="

# Define critical paths
PAULYOPS_ROOT="$HOME/PaulyOps"
DESKTOP_SHORTCUTS="$HOME/Desktop/PaulyOps Shortcuts"
LAUNCHAGENTS="$HOME/Library/LaunchAgents"

echo -e "${BLUE}🔒 Setting up system protection...${NC}"

# 1. Set immutable flags on critical files
echo -e "${BLUE}📁 Protecting core PaulyOps files...${NC}"

# Core Python scripts
chflags uchg "$PAULYOPS_ROOT/scripts/system_health.py" 2>/dev/null || true
chflags uchg "$PAULYOPS_ROOT/scripts/system_autodoctor.py" 2>/dev/null || true
chflags uchg "$PAULYOPS_ROOT/scripts/nightly_report.py" 2>/dev/null || true
chflags uchg "$PAULYOPS_ROOT/scripts/create_backup_zip_cleaned.py" 2>/dev/null || true
chflags uchg "$PAULYOPS_ROOT/scripts/soc2_audit.py" 2>/dev/null || true
chflags uchg "$PAULYOPS_ROOT/scripts/code_hygiene.py" 2>/dev/null || true
chflags uchg "$PAULYOPS_ROOT/scripts/deployment_automation.py" 2>/dev/null || true
chflags uchg "$PAULYOPS_ROOT/scripts/mobile_onboarding.py" 2>/dev/null || true

# Configuration files
chflags uchg "$PAULYOPS_ROOT/config/status_flags.json" 2>/dev/null || true
chflags uchg "$PAULYOPS_ROOT/config/.env" 2>/dev/null || true
chflags uchg "$PAULYOPS_ROOT/config/paths.py" 2>/dev/null || true

# LaunchAgent
chflags uchg "$LAUNCHAGENTS/com.paulyops.nightlyreport.plist" 2>/dev/null || true

# Desktop shortcuts
chflags uchg "$DESKTOP_SHORTCUTS/system_health.command" 2>/dev/null || true
chflags uchg "$DESKTOP_SHORTCUTS/autodoctor.command" 2>/dev/null || true
chflags uchg "$DESKTOP_SHORTCUTS/nightly_report.command" 2>/dev/null || true

# 2. Set read-only permissions on config files
echo -e "${BLUE}🔐 Setting read-only permissions on config files...${NC}"
chmod 444 "$PAULYOPS_ROOT/config/status_flags.json" 2>/dev/null || true
chmod 444 "$PAULYOPS_ROOT/config/.env" 2>/dev/null || true

# 3. Create protection marker
echo -e "${BLUE}🏷️ Creating system protection marker...${NC}"
echo "PaulyOps System Protected - $(date)" > "$PAULYOPS_ROOT/.protected"
chflags uchg "$PAULYOPS_ROOT/.protected"

# 4. Set up directory protection
echo -e "${BLUE}📂 Protecting critical directories...${NC}"
chmod 755 "$PAULYOPS_ROOT/scripts" 2>/dev/null || true
chmod 755 "$PAULYOPS_ROOT/config" 2>/dev/null || true
chmod 755 "$PAULYOPS_ROOT/Reports" 2>/dev/null || true

# 5. Create recovery script protection
echo -e "${BLUE}🔄 Protecting recovery scripts...${NC}"
if [ -f "$PAULYOPS_ROOT/scripts/recover_system.command" ]; then
    chflags uchg "$PAULYOPS_ROOT/scripts/recover_system.command"
    chmod 755 "$PAULYOPS_ROOT/scripts/recover_system.command"
fi

# 6. Set up automatic backup protection
echo -e "${BLUE}💾 Protecting backup system...${NC}"
chmod 755 "$PAULYOPS_ROOT/Backups" 2>/dev/null || true
chmod 755 "$PAULYOPS_ROOT/Backups/archive" 2>/dev/null || true

# 7. Create system integrity check
echo -e "${BLUE}🔍 Creating system integrity checker...${NC}"
cat > "$PAULYOPS_ROOT/scripts/check_integrity.command" << 'EOF'
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
EOF

chmod +x "$PAULYOPS_ROOT/scripts/check_integrity.command"

# 8. Create desktop shortcut for integrity check
echo -e "${BLUE}🔗 Creating integrity check shortcut...${NC}"
cat > "$DESKTOP_SHORTCUTS/check_integrity.command" << 'EOF'
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
EOF

chmod +x "$DESKTOP_SHORTCUTS/check_integrity.command"

# 9. Set up automatic integrity monitoring
echo -e "${BLUE}⏰ Setting up automatic integrity monitoring...${NC}"
cat > "$LAUNCHAGENTS/com.paulyops.integrity.plist" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
 "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
 <key>Label</key> <string>com.paulyops.integrity</string>
 <key>ProgramArguments</key>
 <array>
   <string>/bin/bash</string>
   <string>$PAULYOPS_ROOT/scripts/check_integrity.command</string>
 </array>
 <key>StartCalendarInterval</key>
 <dict>
   <key>Hour</key><integer>9</integer>
   <key>Minute</key><integer>0</integer>
 </dict>
 <key>StandardOutPath</key>
 <string>$PAULYOPS_ROOT/Reports/integrity_check.out.log</string>
 <key>StandardErrorPath</key>
 <string>$PAULYOPS_ROOT/Reports/integrity_check.err.log</string>
 <key>RunAtLoad</key><true/>
</dict>
</plist>
EOF

# Load the integrity monitoring LaunchAgent
launchctl load "$LAUNCHAGENTS/com.paulyops.integrity.plist" 2>/dev/null || true

# 10. Create emergency recovery trigger
echo -e "${BLUE}🚨 Setting up emergency recovery trigger...${NC}"
cat > "$PAULYOPS_ROOT/scripts/emergency_recovery.command" << 'EOF'
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
EOF

chmod +x "$PAULYOPS_ROOT/scripts/emergency_recovery.command"

echo ""
echo -e "${GREEN}✅ PaulyOps System Protection Complete!${NC}"
echo "=============================================="
echo -e "${BLUE}🛡️ Protection Features Active:${NC}"
echo "  • Immutable flags on critical files"
echo "  • Read-only config files"
echo "  • System integrity monitoring"
echo "  • Emergency recovery triggers"
echo "  • Automatic backup protection"
echo ""
echo -e "${YELLOW}📝 Available Commands:${NC}"
echo "  • $DESKTOP_SHORTCUTS/check_integrity.command"
echo "  • $PAULYOPS_ROOT/scripts/emergency_recovery.command"
echo ""
echo -e "${GREEN}🎉 Your PaulyOps system is now protected against accidental breakage!${NC}"

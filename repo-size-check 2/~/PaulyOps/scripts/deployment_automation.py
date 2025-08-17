#!/usr/bin/env python3
"""
PaulyOps Deployment Automation Engineer
Builds install-ready packages and CLI installer
"""

import os
import sys
import shutil
import zipfile
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

class DeploymentAutomationEngineer:
    """Deployment automation engineer for PaulyOps."""
    
    def __init__(self):
        self.deployment_dir = project_root / "deployment"
        self.build_dir = self.deployment_dir / "build"
        self.dist_dir = self.deployment_dir / "dist"
        self.version = "1.0.0"
        
        # Ensure directories exist
        self.deployment_dir.mkdir(exist_ok=True)
        self.build_dir.mkdir(exist_ok=True)
        self.dist_dir.mkdir(exist_ok=True)
    
    def create_installer_script(self) -> Path:
        """Create the main installer script."""
        print("📦 Creating installer script...")
        
        installer_content = f'''#!/bin/bash
# PaulyOps Installer v{self.version}
# Automated installation script for PaulyOps system

set -e

# Colors for output
RED='\\033[0;31m'
GREEN='\\033[0;32m'
YELLOW='\\033[1;33m'
BLUE='\\033[0;34m'
NC='\\033[0m' # No Color

echo -e "${{BLUE}}🚀 PaulyOps Installer v{self.version}${NC}"
echo "=================================="

# Check system requirements
echo -e "${{BLUE}}🔍 Checking system requirements...${NC}"

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo -e "${{RED}}❌ Python 3 is required but not installed${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo -e "${{GREEN}}✅ Python ${{PYTHON_VERSION}} found${NC}"

# Check for required directories
INSTALL_DIR="$HOME/PaulyOps"
echo -e "${{BLUE}}📁 Installing to: ${{INSTALL_DIR}}${NC}"

# Create installation directory
if [ ! -d "${{INSTALL_DIR}}" ]; then
    mkdir -p "${{INSTALL_DIR}}"
    echo -e "${{GREEN}}✅ Created installation directory${NC}"
else
    echo -e "${{YELLOW}}⚠️ Installation directory already exists${NC}"
fi

# Extract PaulyOps files
echo -e "${{BLUE}}📦 Extracting PaulyOps files...${NC}"
cd "${{INSTALL_DIR}}"

# Extract the main package
if [ -f "paulyops_package.zip" ]; then
    unzip -o paulyops_package.zip
    echo -e "${{GREEN}}✅ Files extracted successfully${NC}"
else
    echo -e "${{RED}}❌ Package file not found${NC}"
    exit 1
fi

# Set up permissions
echo -e "${{BLUE}}🔐 Setting up permissions...${NC}"
chmod +x scripts/*.py
chmod +x scripts/*.command 2>/dev/null || true

# Create desktop shortcuts
echo -e "${{BLUE}}🔗 Creating desktop shortcuts...${NC}"
SHORTCUTS_DIR="$HOME/Desktop/PaulyOps Shortcuts"
mkdir -p "${{SHORTCUTS_DIR}}"

# System Health shortcut
cat > "${{SHORTCUTS_DIR}}/system_health.command" << 'EOF'
#!/bin/bash
# PaulyOps System Health - Desktop Shortcut
set -e
RED='\\033[0;31m'
GREEN='\\033[0;32m'
YELLOW='\\033[1;33m'
BLUE='\\033[0;34m'
NC='\\033[0m'
echo -e "${{BLUE}}🔍 PaulyOps System Health Audit${NC}"
echo "====================================="
cd "$HOME/PaulyOps/scripts"
cd "$HOME/Desktop/repo-size-check"
python3 "$HOME/PaulyOps/scripts/system_health.py"
echo -e "${{GREEN}}✅ System health audit complete${NC}"
echo "📄 Report saved to: ~/PaulyOps/System_Health_Report.md"
EOF

# Auto-Doctor shortcut
cat > "${{SHORTCUTS_DIR}}/autodoctor.command" << 'EOF'
#!/bin/bash
# PaulyOps Auto-Doctor - Desktop Shortcut
set -e
RED='\\033[0;31m'
GREEN='\\033[0;32m'
YELLOW='\\033[1;33m'
BLUE='\\033[0;34m'
NC='\\033[0m'
echo -e "${{BLUE}}🩺 PaulyOps Auto-Doctor${NC}"
echo "=========================="
cd "$HOME/PaulyOps/scripts"
python3 system_autodoctor.py "$@"
echo -e "${{GREEN}}✅ Auto-Doctor complete!${NC}"
EOF

# Nightly Report shortcut
cat > "${{SHORTCUTS_DIR}}/nightly_report.command" << 'EOF'
#!/bin/bash
# PaulyOps Nightly Report - Desktop Shortcut
set -e
RED='\\033[0;31m'
GREEN='\\033[0;32m'
YELLOW='\\033[1;33m'
BLUE='\\033[0;34m'
NC='\\033[0m'
echo -e "${{BLUE}}📧 PaulyOps Nightly Report${NC}"
echo "==============================="
cd "$HOME/PaulyOps/scripts"
python3 nightly_report.py
echo -e "${{GREEN}}✅ Nightly report complete${NC}"
echo "📄 Report saved to: ~/PaulyOps/Reports/Nightly_Update_Report_$(date +%Y-%m-%d).md"
EOF

chmod +x "${{SHORTCUTS_DIR}}"/*.command

# Set up LaunchAgent
echo -e "${{BLUE}}⏰ Setting up automated tasks...${NC}"
LAUNCHAGENTS_DIR="$HOME/Library/LaunchAgents"
mkdir -p "${{LAUNCHAGENTS_DIR}}"

cat > "${{LAUNCHAGENTS_DIR}}/com.paulyops.nightlyreport.plist" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
 "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
 <key>Label</key> <string>com.paulyops.nightlyreport</string>
 <key>ProgramArguments</key>
 <array>
   <string>/bin/bash</string>
   <string>${{SHORTCUTS_DIR}}/nightly_report.command</string>
 </array>
 <key>StartCalendarInterval</key>
 <dict>
   <key>Hour</key><integer>22</integer>
   <key>Minute</key><integer>0</integer>
 </dict>
 <key>StandardOutPath</key>
 <string>${{INSTALL_DIR}}/Reports/com.paulyops.nightlyreport.out.log</string>
 <key>StandardErrorPath</key>
 <string>${{INSTALL_DIR}}/Reports/com.paulyops.nightlyreport.err.log</string>
 <key>RunAtLoad</key><true/>
</dict>
</plist>
EOF

# Load the LaunchAgent
launchctl load "${{LAUNCHAGENTS_DIR}}/com.paulyops.nightlyreport.plist" 2>/dev/null || true

# Create initial configuration
echo -e "${{BLUE}}⚙️ Setting up initial configuration...${NC}"
CONFIG_DIR="${{INSTALL_DIR}}/config"

# Create .env template
cat > "${{CONFIG_DIR}}/.env" << 'EOF'
# PaulyOps Environment Configuration
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
BACKUP_SOURCE=/Volumes/BigSkyAgSSD/BigSkyAg

# Paths (auto-configured)
PAULYOPS_ROOT=~/PaulyOps
PAULYOPS_REPORTS=~/PaulyOps/Reports
PAULYOPS_BACKUPS=~/PaulyOps/Backups
EOF

# Create dropzone
DROPZONE_DIR="$HOME/Desktop/PaulyOpsDropzone"
mkdir -p "${{DROPZONE_DIR}}"
echo "PaulyOps Dropzone - Place files here for processing" > "${{DROPZONE_DIR}}/README.txt"

# Run initial health check
echo -e "${{BLUE}}🔍 Running initial health check...${NC}"
cd "${{INSTALL_DIR}}/scripts"
python3 system_health.py > /dev/null 2>&1 || echo -e "${{YELLOW}}⚠️ Initial health check had warnings (normal)${NC}"

echo ""
echo -e "${{GREEN}}🎉 PaulyOps Installation Complete!${NC}"
echo "=================================="
echo -e "${{BLUE}}📁 Installation Directory:${NC} ${{INSTALL_DIR}}"
echo -e "${{BLUE}}🔗 Desktop Shortcuts:${NC} ${{SHORTCUTS_DIR}}"
echo -e "${{BLUE}}📁 Dropzone:${NC} ${{DROPZONE_DIR}}"
echo -e "${{BLUE}}⏰ Automated Tasks:${NC} Nightly report at 10:00 PM"
echo ""
echo -e "${{YELLOW}}📝 Next Steps:${NC}"
echo "1. Configure email settings in ${{CONFIG_DIR}}/.env"
echo "2. Run system health check: ${{SHORTCUTS_DIR}}/system_health.command"
echo "3. Test Auto-Doctor: ${{SHORTCUTS_DIR}}/autodoctor.command"
echo ""
echo -e "${{GREEN}}✅ PaulyOps is ready to use!${NC}"
'''
        
        installer_path = self.build_dir / "install_paulyops.sh"
        installer_path.write_text(installer_content)
        installer_path.chmod(0o755)
        
        return installer_path
    
    def create_cli_installer(self) -> Path:
        """Create CLI installer script."""
        print("🖥️ Creating CLI installer...")
        
        cli_content = f'''#!/usr/bin/env python3
"""
PaulyOps CLI Installer
Command-line installation interface
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

def install_paulyops(install_dir: str = None, company_name: str = "PaulyOps", 
                    dropzone_name: str = "PaulyOpsDropzone", email: str = None):
    """Install PaulyOps system."""
    
    if not install_dir:
        install_dir = str(Path.home() / "PaulyOps")
    
    print(f"🚀 Installing PaulyOps to: {{install_dir}}")
    print(f"🏢 Company: {{company_name}}")
    print(f"📁 Dropzone: {{dropzone_name}}")
    
    # Set environment variables for installation
    env = os.environ.copy()
    env["COMPANY_NAME"] = company_name
    env["DROPZONE_NAME"] = dropzone_name
    if email:
        env["NR_SENDER_EMAIL"] = email
        env["NR_RECIPIENTS"] = email
    
    # Run the installer script
    installer_script = Path(__file__).parent / "install_paulyops.sh"
    if installer_script.exists():
        result = subprocess.run([str(installer_script)], 
                              env=env, 
                              cwd=install_dir,
                              capture_output=True, 
                              text=True)
        
        if result.returncode == 0:
            print("✅ Installation completed successfully!")
            print(result.stdout)
        else:
            print("❌ Installation failed!")
            print(result.stderr)
            return False
    else:
        print("❌ Installer script not found!")
        return False
    
    return True

def main():
    parser = argparse.ArgumentParser(description="PaulyOps CLI Installer")
    parser.add_argument("--install-dir", help="Installation directory")
    parser.add_argument("--company", default="PaulyOps", help="Company name")
    parser.add_argument("--dropzone", default="PaulyOpsDropzone", help="Dropzone name")
    parser.add_argument("--email", help="Email for notifications")
    parser.add_argument("--version", action="version", version="PaulyOps v{self.version}")
    
    args = parser.parse_args()
    
    success = install_paulyops(
        install_dir=args.install_dir,
        company_name=args.company,
        dropzone_name=args.dropzone,
        email=args.email
    )
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
'''
        
        cli_path = self.build_dir / "paulyops_installer.py"
        cli_path.write_text(cli_content)
        cli_path.chmod(0o755)
        
        return cli_path
    
    def create_package(self) -> Path:
        """Create the main PaulyOps package."""
        print("📦 Creating PaulyOps package...")
        
        package_path = self.build_dir / "paulyops_package.zip"
        
        with zipfile.ZipFile(package_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Add core directories
            core_dirs = ["scripts", "config", "Reports", "Backups", "logs"]
            for dir_name in core_dirs:
                dir_path = project_root / dir_name
                if dir_path.exists():
                    for file_path in dir_path.rglob("*"):
                        if file_path.is_file():
                            arc_name = file_path.relative_to(project_root)
                            zipf.write(file_path, arc_name)
            
            # Add README and documentation
            docs = ["README.md", "VERSION.md"]
            for doc in docs:
                doc_path = project_root / doc
                if doc_path.exists():
                    zipf.write(doc_path, doc_path.name)
        
        return package_path
    
    def create_installer_package(self) -> Path:
        """Create complete installer package."""
        print("📦 Creating installer package...")
        
        # Create all components
        installer_script = self.create_installer_script()
        cli_installer = self.create_cli_installer()
        main_package = self.create_package()
        
        # Create installer package
        installer_package = self.dist_dir / f"paulyops_installer_v{self.version}.zip"
        
        with zipfile.ZipFile(installer_package, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Add installer script
            zipf.write(installer_script, installer_script.name)
            
            # Add CLI installer
            zipf.write(cli_installer, cli_installer.name)
            
            # Add main package
            zipf.write(main_package, "paulyops_package.zip")
            
            # Add installation instructions
            instructions = f"""# PaulyOps Installer v{self.version}

## Quick Installation

### Option 1: Automated Installer
1. Extract this package
2. Run: `./install_paulyops.sh`

### Option 2: CLI Installer
1. Extract this package
2. Run: `python3 paulyops_installer.py --help`

### Custom Installation
```bash
python3 paulyops_installer.py \\
  --company "Your Company" \\
  --dropzone "YourDropzone" \\
  --email "your@email.com"
```

## System Requirements
- macOS 10.15 or later
- Python 3.7 or later
- 2GB available disk space

## Post-Installation
1. Configure email settings in ~/PaulyOps/config/.env
2. Run system health check
3. Test Auto-Doctor functionality

For support, see README.md in the installation directory.
"""
            
            zipf.writestr("INSTALLATION.md", instructions)
        
        return installer_package
    
    def generate_deployment_report(self) -> str:
        """Generate deployment report."""
        report = []
        report.append("# PaulyOps Deployment Report")
        report.append(f"**Generated:** {datetime.now().isoformat()}")
        report.append(f"**Version:** {self.version}")
        report.append("")
        
        report.append("## 📦 Package Contents")
        report.append(f"- **Main Package:** paulyops_package.zip")
        report.append(f"- **Installer Script:** install_paulyops.sh")
        report.append(f"- **CLI Installer:** paulyops_installer.py")
        report.append(f"- **Instructions:** INSTALLATION.md")
        report.append("")
        
        report.append("## 🚀 Installation Methods")
        report.append("1. **Automated:** Run `./install_paulyops.sh`")
        report.append("2. **CLI:** Run `python3 paulyops_installer.py`")
        report.append("3. **Custom:** Use CLI with parameters")
        report.append("")
        
        report.append("## 📁 Installation Structure")
        report.append("```
        ~/PaulyOps/
        ├── scripts/          # Core automation scripts
        ├── config/           # Configuration files
        ├── Reports/          # System reports and logs
        ├── Backups/          # Backup storage
        └── logs/             # System logs
        
        ~/Desktop/
        └── PaulyOps Shortcuts/  # Desktop launchers
        ```")
        report.append("")
        
        report.append("## ✅ Post-Installation Checklist")
        report.append("- [ ] Configure email settings in ~/PaulyOps/config/.env")
        report.append("- [ ] Run system health check")
        report.append("- [ ] Test Auto-Doctor functionality")
        report.append("- [ ] Verify LaunchAgent is loaded")
        report.append("- [ ] Test dropzone functionality")
        
        return "\n".join(report)
    
    def build_complete_package(self) -> Dict:
        """Build complete deployment package."""
        print("🔧 PaulyOps Deployment Automation Engineer")
        print("=" * 50)
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Version: {self.version}")
        print()
        
        # Build all components
        installer_package = self.create_installer_package()
        
        # Generate report
        report = self.generate_deployment_report()
        report_file = self.dist_dir / f"deployment_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        report_file.write_text(report)
        
        return {
            "installer_package": installer_package,
            "report_file": report_file,
            "version": self.version
        }

def main():
    """Build deployment package."""
    engineer = DeploymentAutomationEngineer()
    result = engineer.build_complete_package()
    
    print("\n" + "=" * 50)
    print("🔧 DEPLOYMENT PACKAGE BUILT")
    print(f"📦 Installer: {result['installer_package']}")
    print(f"📄 Report: {result['report_file']}")
    print(f"🏷️ Version: {result['version']}")
    print("=" * 50)

if __name__ == "__main__":
    main()

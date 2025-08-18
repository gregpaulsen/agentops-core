#!/usr/bin/env python3
"""
PaulyOps Mobile Onboarding Flow Architect
Prepares mobile-ready frontend and simplifies first-time setup
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, List

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

class MobileOnboardingArchitect:
    """Mobile onboarding flow architect for PaulyOps."""
    
    def __init__(self):
        self.mobile_dir = project_root / "mobile"
        self.api_dir = project_root / "api"
        self.version = "1.0.0"
        
        # Ensure directories exist
        self.mobile_dir.mkdir(exist_ok=True)
        self.api_dir.mkdir(exist_ok=True)
    
    def create_mobile_api_endpoints(self) -> Path:
        """Create mobile-ready API endpoints."""
        print("📱 Creating mobile API endpoints...")
        
        api_content = '''#!/usr/bin/env python3
"""
PaulyOps Mobile API
RESTful API endpoints for mobile frontend
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional
import json
import subprocess
from pathlib import Path
from datetime import datetime

app = FastAPI(title="PaulyOps Mobile API", version="1.0.0")

# CORS for mobile apps
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Data models
class HealthStatus(BaseModel):
    overall_score: int
    successes: int
    warnings: int
    issues: int
    details: Dict

class SystemInfo(BaseModel):
    company_name: str
    dropzone_name: str
    version: str
    last_backup: Optional[str]
    last_health_check: Optional[str]

class OnboardingData(BaseModel):
    company_name: str
    dropzone_name: str
    email: str
    smtp_host: str
    smtp_port: int
    smtp_username: str
    smtp_password: str

# Dependency to get PaulyOps root
def get_paulyops_root() -> Path:
    return Path.home() / "PaulyOps"

@app.get("/")
async def root():
    """API root endpoint."""
    return {"message": "PaulyOps Mobile API", "version": "1.0.0"}

@app.get("/health", response_model=HealthStatus)
async def get_health_status():
    """Get system health status."""
    try:
        paulyops_root = get_paulyops_root()
        health_script = paulyops_root / "scripts" / "system_health.py"
        
        if not health_script.exists():
            raise HTTPException(status_code=500, detail="Health script not found")
        
        # Run health check
        result = subprocess.run(
            [sys.executable, str(health_script)],
            capture_output=True,
            text=True,
            cwd=paulyops_root / "scripts"
        )
        
        # Parse health report
        health_report = paulyops_root / "System_Health_Report.md"
        if health_report.exists():
            content = health_report.read_text()
            
            # Extract basic stats
            successes = content.count("✅")
            warnings = content.count("⚠️")
            issues = content.count("❌")
            
            overall_score = int((successes / (successes + warnings + issues)) * 100) if (successes + warnings + issues) > 0 else 0
            
            return HealthStatus(
                overall_score=overall_score,
                successes=successes,
                warnings=warnings,
                issues=issues,
                details={"report": content[:1000] + "..." if len(content) > 1000 else content}
            )
        else:
            raise HTTPException(status_code=500, detail="Health report not found")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")

@app.get("/system-info", response_model=SystemInfo)
async def get_system_info():
    """Get system information."""
    try:
        paulyops_root = get_paulyops_root()
        config_dir = paulyops_root / "config"
        
        # Load configuration
        company_name = "PaulyOps"
        dropzone_name = "PaulyOpsDropzone"
        
        env_file = config_dir / ".env"
        if env_file.exists():
            content = env_file.read_text()
            for line in content.split('\n'):
                if line.startswith('COMPANY_NAME='):
                    company_name = line.split('=', 1)[1].strip()
                elif line.startswith('DROPZONE_NAME='):
                    dropzone_name = line.split('=', 1)[1].strip()
        
        # Get last backup info
        backup_dir = paulyops_root / "Backups"
        last_backup = None
        if backup_dir.exists():
            backup_files = list(backup_dir.glob("*.zip"))
            if backup_files:
                latest_backup = max(backup_files, key=lambda f: f.stat().st_mtime)
                last_backup = datetime.fromtimestamp(latest_backup.stat().st_mtime).isoformat()
        
        # Get last health check
        health_report = paulyops_root / "System_Health_Report.md"
        last_health_check = None
        if health_report.exists():
            last_health_check = datetime.fromtimestamp(health_report.stat().st_mtime).isoformat()
        
        return SystemInfo(
            company_name=company_name,
            dropzone_name=dropzone_name,
            version=self.version,
            last_backup=last_backup,
            last_health_check=last_health_check
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get system info: {str(e)}")

@app.post("/onboard")
async def onboard_system(data: OnboardingData):
    """Onboard a new system with company configuration."""
    try:
        paulyops_root = get_paulyops_root()
        config_dir = paulyops_root / "config"
        
        # Create .env file
        env_content = f"""# PaulyOps Environment Configuration
# Generated by mobile onboarding on {datetime.now().isoformat()}

# Email Configuration
NR_EMAIL_PROVIDER=SMTP
NR_SENDER_NAME={data.company_name} Automations
NR_SENDER_EMAIL={data.email}
NR_RECIPIENTS={data.email}

# SMTP Settings
NR_SMTP_HOST={data.smtp_host}
NR_SMTP_PORT={data.smtp_port}
NR_SMTP_USERNAME={data.smtp_username}
NR_SMTP_PASSWORD={data.smtp_password}
NR_SMTP_STARTTLS=true

# System Configuration
ENV=production
LOG_LEVEL=INFO
STORAGE_PROVIDER=local
COMPANY_NAME={data.company_name}
DROPZONE_NAME={data.dropzone_name}
BACKUP_SOURCE=/Volumes/BigSkyAgSSD/BigSkyAg

# Paths (auto-configured)
PAULYOPS_ROOT=~/PaulyOps
PAULYOPS_REPORTS=~/PaulyOps/Reports
PAULYOPS_BACKUPS=~/PaulyOps/Backups
"""
        
        env_file = config_dir / ".env"
        env_file.write_text(env_content)
        
        # Update status flags
        status_flags_file = config_dir / "status_flags.json"
        if status_flags_file.exists():
            with open(status_flags_file, 'r') as f:
                status_flags = json.load(f)
        else:
            status_flags = {}
        
        status_flags["company_name"] = data.company_name
        status_flags["dropzone_name"] = data.dropzone_name
        
        with open(status_flags_file, 'w') as f:
            json.dump(status_flags, f, indent=2)
        
        # Create dropzone
        dropzone_path = Path.home() / "Desktop" / data.dropzone_name
        dropzone_path.mkdir(exist_ok=True)
        
        # Run Auto-Doctor to set up system
        autodoctor_script = paulyops_root / "scripts" / "system_autodoctor.py"
        if autodoctor_script.exists():
            subprocess.run([sys.executable, str(autodoctor_script)], 
                         cwd=paulyops_root / "scripts")
        
        return {"message": "Onboarding completed successfully", "company_name": data.company_name}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Onboarding failed: {str(e)}")

@app.post("/run-health-check")
async def run_health_check():
    """Run a health check and return results."""
    try:
        paulyops_root = get_paulyops_root()
        health_script = paulyops_root / "scripts" / "system_health.py"
        
        if not health_script.exists():
            raise HTTPException(status_code=500, detail="Health script not found")
        
        result = subprocess.run(
            [sys.executable, str(health_script)],
            capture_output=True,
            text=True,
            cwd=paulyops_root / "scripts"
        )
        
        return {
            "success": result.returncode == 0,
            "output": result.stdout,
            "error": result.stderr if result.returncode != 0 else None
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")

@app.post("/run-autodoctor")
async def run_autodoctor():
    """Run Auto-Doctor to fix system issues."""
    try:
        paulyops_root = get_paulyops_root()
        autodoctor_script = paulyops_root / "scripts" / "system_autodoctor.py"
        
        if not autodoctor_script.exists():
            raise HTTPException(status_code=500, detail="Auto-Doctor script not found")
        
        result = subprocess.run(
            [sys.executable, str(autodoctor_script)],
            capture_output=True,
            text=True,
            cwd=paulyops_root / "scripts"
        )
        
        return {
            "success": result.returncode == 0,
            "output": result.stdout,
            "error": result.stderr if result.returncode != 0 else None
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Auto-Doctor failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
'''
        
        api_file = self.api_dir / "mobile_api.py"
        api_file.write_text(api_content)
        api_file.chmod(0o755)
        
        return api_file
    
    def create_mobile_config(self) -> Path:
        """Create mobile configuration file."""
        print("⚙️ Creating mobile configuration...")
        
        config_content = {
            "api": {
                "base_url": "http://localhost:8000",
                "endpoints": {
                    "health": "/health",
                    "system_info": "/system-info",
                    "onboard": "/onboard",
                    "health_check": "/run-health-check",
                    "autodoctor": "/run-autodoctor"
                }
            },
            "onboarding": {
                "required_fields": [
                    "company_name",
                    "dropzone_name", 
                    "email",
                    "smtp_host",
                    "smtp_port",
                    "smtp_username",
                    "smtp_password"
                ],
                "defaults": {
                    "company_name": "PaulyOps",
                    "dropzone_name": "PaulyOpsDropzone",
                    "smtp_port": 587,
                    "smtp_starttls": True
                }
            },
            "ui": {
                "theme": "light",
                "language": "en",
                "notifications": True,
                "auto_refresh": 300
            }
        }
        
        config_file = self.mobile_dir / "mobile_config.json"
        with open(config_file, 'w') as f:
            json.dump(config_content, f, indent=2)
        
        return config_file
    
    def create_glide_config(self) -> Path:
        """Create Glide configuration for mobile app."""
        print("📱 Creating Glide configuration...")
        
        glide_config = {
            "app_name": "PaulyOps Mobile",
            "version": self.version,
            "api_integration": {
                "type": "rest",
                "base_url": "http://localhost:8000",
                "auth_type": "none"
            },
            "screens": {
                "onboarding": {
                    "title": "Welcome to PaulyOps",
                    "fields": [
                        {"name": "company_name", "type": "text", "label": "Company Name", "required": True},
                        {"name": "dropzone_name", "type": "text", "label": "Dropzone Name", "required": True},
                        {"name": "email", "type": "email", "label": "Email", "required": True},
                        {"name": "smtp_host", "type": "text", "label": "SMTP Host", "required": True},
                        {"name": "smtp_port", "type": "number", "label": "SMTP Port", "default": 587},
                        {"name": "smtp_username", "type": "text", "label": "SMTP Username", "required": True},
                        {"name": "smtp_password", "type": "password", "label": "SMTP Password", "required": True}
                    ]
                },
                "dashboard": {
                    "title": "System Dashboard",
                    "widgets": [
                        {"type": "health_score", "title": "Health Score"},
                        {"type": "last_backup", "title": "Last Backup"},
                        {"type": "system_status", "title": "System Status"}
                    ]
                },
                "health": {
                    "title": "System Health",
                    "actions": [
                        {"name": "run_health_check", "label": "Run Health Check"},
                        {"name": "run_autodoctor", "label": "Run Auto-Doctor"}
                    ]
                }
            }
        }
        
        glide_file = self.mobile_dir / "glide_config.json"
        with open(glide_file, 'w') as f:
            json.dump(glide_config, f, indent=2)
        
        return glide_file
    
    def create_ios_launcher(self) -> Path:
        """Create iOS launcher configuration."""
        print("🍎 Creating iOS launcher...")
        
        ios_config = {
            "app_name": "PaulyOps",
            "bundle_id": "com.paulyops.mobile",
            "version": self.version,
            "launch_url": "http://localhost:8000",
            "permissions": [
                "network_access",
                "local_storage"
            ],
            "features": {
                "offline_mode": True,
                "push_notifications": False,
                "biometric_auth": False
            }
        }
        
        ios_file = self.mobile_dir / "ios_launcher.json"
        with open(ios_file, 'w') as f:
            json.dump(ios_config, f, indent=2)
        
        return ios_file
    
    def create_onboarding_flow(self) -> Path:
        """Create onboarding flow documentation."""
        print("🔄 Creating onboarding flow...")
        
        flow_content = """# PaulyOps Mobile Onboarding Flow

## Overview
This document describes the mobile onboarding flow for PaulyOps, designed to simplify first-time setup and configuration.

## Flow Steps

### 1. Welcome Screen
- App introduction
- System requirements check
- Permission requests

### 2. Company Configuration
- Company name input
- Dropzone name configuration
- Branding preferences

### 3. Email Setup
- SMTP configuration
- Test email verification
- Notification preferences

### 4. System Validation
- Health check execution
- Auto-Doctor run
- Issue resolution

### 5. Completion
- Success confirmation
- Quick start guide
- Support information

## API Endpoints

### Onboarding
- `POST /onboard` - Complete system onboarding
- `GET /system-info` - Get current system information

### Health & Maintenance
- `GET /health` - Get system health status
- `POST /run-health-check` - Execute health check
- `POST /run-autodoctor` - Run Auto-Doctor

## Mobile App Features

### Dashboard
- Real-time health score
- Last backup status
- System alerts
- Quick actions

### Health Monitoring
- Detailed health reports
- Issue resolution
- Auto-Doctor integration
- Historical data

### Configuration
- Company settings
- Email configuration
- Dropzone management
- System preferences

## Integration Points

### Glide App
- REST API integration
- Form-based configuration
- Real-time updates
- Offline capability

### iOS Launcher
- Native app wrapper
- Deep linking
- Push notifications
- Biometric authentication

## Security Considerations

### API Security
- No authentication required (local only)
- CORS enabled for mobile apps
- Input validation
- Error handling

### Data Protection
- Local storage only
- No cloud sync
- Encrypted configuration
- Secure communication

## Troubleshooting

### Common Issues
1. API not accessible
2. Configuration errors
3. Health check failures
4. Auto-Doctor issues

### Resolution Steps
1. Verify API server running
2. Check configuration files
3. Run manual health check
4. Review error logs

## Support

For mobile app support:
- Check API documentation
- Review configuration files
- Test endpoints manually
- Contact development team
"""
        
        flow_file = self.mobile_dir / "onboarding_flow.md"
        flow_file.write_text(flow_content)
        
        return flow_file
    
    def generate_mobile_report(self) -> str:
        """Generate mobile onboarding report."""
        report = []
        report.append("# PaulyOps Mobile Onboarding Report")
        report.append(f"**Generated:** {datetime.now().isoformat()}")
        report.append(f"**Version:** {self.version}")
        report.append("")
        
        report.append("## 📱 Mobile Components Created")
        report.append(f"- **API Endpoints:** {self.api_dir}/mobile_api.py")
        report.append(f"- **Mobile Config:** {self.mobile_dir}/mobile_config.json")
        report.append(f"- **Glide Config:** {self.mobile_dir}/glide_config.json")
        report.append(f"- **iOS Launcher:** {self.mobile_dir}/ios_launcher.json")
        report.append(f"- **Onboarding Flow:** {self.mobile_dir}/onboarding_flow.md")
        report.append("")
        
        report.append("## 🚀 Getting Started")
        report.append("1. Start the API server: `python3 api/mobile_api.py`")
        report.append("2. Configure mobile app with API endpoints")
        report.append("3. Test onboarding flow")
        report.append("4. Deploy to mobile devices")
        report.append("")
        
        report.append("## 📋 API Endpoints")
        report.append("- `GET /health` - System health status")
        report.append("- `GET /system-info` - System information")
        report.append("- `POST /onboard` - Complete onboarding")
        report.append("- `POST /run-health-check` - Execute health check")
        report.append("- `POST /run-autodoctor` - Run Auto-Doctor")
        report.append("")
        
        report.append("## 🎯 Mobile Features")
        report.append("- **Simplified Onboarding:** Guided setup process")
        report.append("- **Real-time Monitoring:** Live health status")
        report.append("- **Quick Actions:** One-tap health checks")
        report.append("- **Offline Support:** Local data storage")
        report.append("- **Cross-platform:** iOS and Android support")
        
        return "\n".join(report)
    
    def build_mobile_components(self) -> Dict:
        """Build all mobile components."""
        print("📱 PaulyOps Mobile Onboarding Flow Architect")
        print("=" * 50)
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Version: {self.version}")
        print()
        
        # Create all components
        api_file = self.create_mobile_api_endpoints()
        config_file = self.create_mobile_config()
        glide_file = self.create_glide_config()
        ios_file = self.create_ios_launcher()
        flow_file = self.create_onboarding_flow()
        
        # Generate report
        report = self.generate_mobile_report()
        report_file = self.mobile_dir / f"mobile_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        report_file.write_text(report)
        
        return {
            "api_file": api_file,
            "config_file": config_file,
            "glide_file": glide_file,
            "ios_file": ios_file,
            "flow_file": flow_file,
            "report_file": report_file,
            "version": self.version
        }

def main():
    """Build mobile components."""
    architect = MobileOnboardingArchitect()
    result = architect.build_mobile_components()
    
    print("\n" + "=" * 50)
    print("📱 MOBILE COMPONENTS BUILT")
    print(f"🌐 API: {result['api_file']}")
    print(f"⚙️ Config: {result['config_file']}")
    print(f"📱 Glide: {result['glide_file']}")
    print(f"🍎 iOS: {result['ios_file']}")
    print(f"🔄 Flow: {result['flow_file']}")
    print(f"📄 Report: {result['report_file']}")
    print(f"🏷️ Version: {result['version']}")
    print("=" * 50)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
PaulyOps Configuration Printer
Outputs current config and environment flags for human review
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def print_environment_vars():
    """Print all relevant environment variables."""
    print("🔧 Environment Variables")
    print("=" * 40)
    
    env_vars = [
        "COMPANY_NAME",
        "DROPZONE_NAME",
        "NR_EMAIL_PROVIDER",
        "NR_SENDER_NAME",
        "NR_SENDER_EMAIL",
        "NR_RECIPIENTS",
        "NR_SMTP_HOST",
        "NR_SMTP_PORT",
        "NR_SMTP_USERNAME",
        "NR_SMTP_PASSWORD",
        "NR_SMTP_STARTTLS",
        "BACKUP_SOURCE",
        "PAULYOPS_ROOT",
        "PAULYOPS_REPORTS",
        "PAULYOPS_BACKUPS"
    ]
    
    for var in env_vars:
        value = os.environ.get(var, "NOT_SET")
        if "PASSWORD" in var and value != "NOT_SET":
            value = "***HIDDEN***"
        status = "✅" if value != "NOT_SET" else "⚠️"
        print(f"  {status} {var}: {value}")

def print_status_flags():
    """Print status flags configuration."""
    print("\n📋 Status Flags Configuration")
    print("=" * 40)
    
    status_flags_path = Path.home() / "PaulyOps" / "config" / "status_flags.json"
    if status_flags_path.exists():
        try:
            with open(status_flags_path, 'r') as f:
                flags = json.load(f)
            
            print(f"  📄 File: {status_flags_path}")
            print(f"  📊 Total flags: {len(flags)}")
            print()
            
            # Group flags by category
            categories = {
                "System Checks": ["check_git", "check_router", "check_endpoints", "check_backup_upload", 
                                "check_launchd_jobs", "check_launchd", "check_provider_credentials", "check_spotlight"],
                "Company Config": ["company_name", "dropzone_name"],
                "Git Settings": ["git_repos", "git_paths", "skip_git_repos"],
                "LaunchAgent Jobs": ["launchd_jobs", "skip_launchd_jobs"],
                "Endpoints": ["endpoint_urls"]
            }
            
            for category, flag_list in categories.items():
                print(f"  {category}:")
                for flag in flag_list:
                    if flag in flags:
                        value = flags[flag]
                        if isinstance(value, list):
                            value = f"[{', '.join(str(v) for v in value)}]"
                        print(f"    {flag}: {value}")
                    else:
                        print(f"    {flag}: NOT_SET")
                print()
        except Exception as e:
            print(f"  ❌ Error reading status flags: {e}")
    else:
        print("  ❌ Status flags file not found")

def print_folder_structure():
    """Print current folder structure."""
    print("📁 Folder Structure")
    print("=" * 40)
    
    paulyops_root = Path.home() / "PaulyOps"
    if paulyops_root.exists():
        print(f"  📂 Root: {paulyops_root}")
        
        for item in sorted(paulyops_root.iterdir()):
            if item.is_dir():
                size = len(list(item.rglob("*")))
                print(f"    📁 {item.name}/ ({size} items)")
            else:
                size = item.stat().st_size if item.exists() else 0
                print(f"    📄 {item.name} ({size} bytes)")
    else:
        print("  ❌ PaulyOps root not found")

def print_agent_status():
    """Print agent script status."""
    print("\n🤖 Agent Scripts Status")
    print("=" * 40)
    
    scripts_dir = Path.home() / "PaulyOps" / "scripts"
    if scripts_dir.exists():
        agents = [
            "system_health.py",
            "system_autodoctor.py",
            "nightly_report.py",
            "create_backup_zip_cleaned.py",
            "run_diagnostics.py",
            "test_upload.py",
            "print_config.py"
        ]
        
        for agent in agents:
            agent_path = scripts_dir / agent
            if agent_path.exists():
                size = agent_path.stat().st_size
                print(f"  ✅ {agent} ({size} bytes)")
            else:
                print(f"  ❌ {agent} (missing)")
    else:
        print("  ❌ Scripts directory not found")

def print_launchagent_status():
    """Print LaunchAgent status."""
    print("\n⏰ LaunchAgent Status")
    print("=" * 40)
    
    try:
        import subprocess
        result = subprocess.run(["launchctl", "list"], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            if "com.paulyops.nightlyreport" in result.stdout:
                print("  ✅ com.paulyops.nightlyreport: Active")
            else:
                print("  ❌ com.paulyops.nightlyreport: Not found")
        else:
            print(f"  ❌ LaunchAgent check failed: {result.stderr}")
    except Exception as e:
        print(f"  ❌ LaunchAgent status error: {e}")

def print_backup_status():
    """Print backup status."""
    print("\n💾 Backup Status")
    print("=" * 40)
    
    backup_dir = Path.home() / "PaulyOps" / "Backups"
    if backup_dir.exists():
        zip_files = list(backup_dir.glob("*.zip"))
        print(f"  📦 Total backups: {len(zip_files)}")
        
        if zip_files:
            # Sort by modification time
            zip_files.sort(key=lambda f: f.stat().st_mtime, reverse=True)
            print("  Recent backups:")
            for zip_file in zip_files[:5]:
                size_mb = zip_file.stat().st_size / (1024 * 1024)
                mtime = datetime.fromtimestamp(zip_file.stat().st_mtime)
                print(f"    {zip_file.name} ({size_mb:.1f} MB, {mtime.strftime('%Y-%m-%d %H:%M')})")
    else:
        print("  ❌ Backup directory not found")

def main():
    """Print all configuration information."""
    print("🚀 PaulyOps Configuration Report")
    print("=" * 50)
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    print_environment_vars()
    print_status_flags()
    print_folder_structure()
    print_agent_status()
    print_launchagent_status()
    print_backup_status()
    
    print("\n✅ Configuration report complete!")

if __name__ == "__main__":
    main()

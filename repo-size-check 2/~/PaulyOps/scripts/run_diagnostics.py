#!/usr/bin/env python3
"""
PaulyOps System Diagnostics
Tests all folder paths, config flags, and provider connectivity
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_folder_paths():
    """Test all critical folder paths."""
    print("🔍 Testing folder paths...")
    
    paths = {
        "PaulyOps Root": Path.home() / "PaulyOps",
        "Scripts": Path.home() / "PaulyOps" / "scripts",
        "Config": Path.home() / "PaulyOps" / "config",
        "Reports": Path.home() / "PaulyOps" / "Reports",
        "Backups": Path.home() / "PaulyOps" / "Backups",
        "Logs": Path.home() / "PaulyOps" / "logs",
        "UI": Path.home() / "PaulyOps" / "ui",
        "API": Path.home() / "PaulyOps" / "api",
        "Providers": Path.home() / "PaulyOps" / "providers",
        "Tests": Path.home() / "PaulyOps" / "tests",
        "Lib": Path.home() / "PaulyOps" / "lib",
        "Bin": Path.home() / "PaulyOps" / "bin",
    }
    
    results = {}
    for name, path in paths.items():
        exists = path.exists()
        writable = os.access(path, os.W_OK) if exists else False
        results[name] = {"exists": exists, "writable": writable}
        status = "✅" if exists else "❌"
        print(f"  {status} {name}: {path}")
    
    return results

def test_config_flags():
    """Test configuration flags and environment variables."""
    print("\n🔧 Testing configuration flags...")
    
    # Test status flags
    status_flags_path = Path.home() / "PaulyOps" / "config" / "status_flags.json"
    if status_flags_path.exists():
        try:
            with open(status_flags_path, 'r') as f:
                flags = json.load(f)
            print(f"  ✅ Status flags loaded: {len(flags)} items")
            
            # Test key flags
            key_flags = ["company_name", "dropzone_name", "check_git", "check_launchd_jobs"]
            for flag in key_flags:
                value = flags.get(flag, "NOT_SET")
                print(f"    {flag}: {value}")
        except Exception as e:
            print(f"  ❌ Status flags error: {e}")
    else:
        print("  ❌ Status flags file not found")
    
    # Test environment variables
    env_vars = [
        "COMPANY_NAME",
        "DROPZONE_NAME", 
        "NR_EMAIL_PROVIDER",
        "NR_SENDER_EMAIL",
        "BACKUP_SOURCE"
    ]
    
    print("  Environment variables:")
    for var in env_vars:
        value = os.environ.get(var, "NOT_SET")
        status = "✅" if value != "NOT_SET" else "⚠️"
        print(f"    {status} {var}: {value}")

def test_provider_connectivity():
    """Test storage provider connectivity."""
    print("\n☁️ Testing provider connectivity...")
    
    # Test local storage
    local_backup_dir = Path.home() / "PaulyOps" / "Backups"
    if local_backup_dir.exists():
        print(f"  ✅ Local storage: {local_backup_dir}")
        try:
            test_file = local_backup_dir / ".test_write"
            test_file.write_text("test")
            test_file.unlink()
            print("    ✅ Write test passed")
        except Exception as e:
            print(f"    ❌ Write test failed: {e}")
    else:
        print("  ❌ Local storage not found")
    
    # Test Google Drive (if configured)
    drive_script = Path.home() / "PaulyOps" / "scripts" / "upload_backup_to_drive_v3.py"
    if drive_script.exists():
        print("  ⚠️ Google Drive script found (manual test required)")
    else:
        print("  ℹ️ Google Drive script not found")

def test_agent_health():
    """Test all agent scripts."""
    print("\n🤖 Testing agent health...")
    
    agents = [
        "system_health.py",
        "system_autodoctor.py", 
        "nightly_report.py",
        "create_backup_zip_cleaned.py"
    ]
    
    scripts_dir = Path.home() / "PaulyOps" / "scripts"
    
    for agent in agents:
        agent_path = scripts_dir / agent
        if agent_path.exists():
            try:
                # Test import
                result = subprocess.run([sys.executable, "-c", f"import sys; sys.path.insert(0, '{scripts_dir}'); import {agent.replace('.py', '')}"], 
                                      capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    print(f"  ✅ {agent}: Import successful")
                else:
                    print(f"  ❌ {agent}: Import failed - {result.stderr.strip()}")
            except Exception as e:
                print(f"  ❌ {agent}: Test failed - {e}")
        else:
            print(f"  ❌ {agent}: Not found")

def test_launchagent():
    """Test LaunchAgent status."""
    print("\n⏰ Testing LaunchAgent...")
    
    try:
        result = subprocess.run(["launchctl", "list"], capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            if "com.paulyops.nightlyreport" in result.stdout:
                print("  ✅ com.paulyops.nightlyreport: Active")
            else:
                print("  ❌ com.paulyops.nightlyreport: Not found")
        else:
            print(f"  ❌ LaunchAgent check failed: {result.stderr}")
    except Exception as e:
        print(f"  ❌ LaunchAgent test failed: {e}")

def test_desktop_shortcuts():
    """Test desktop shortcuts."""
    print("\n🔗 Testing desktop shortcuts...")
    
    shortcuts_dir = Path.home() / "Desktop" / "PaulyOps Shortcuts"
    if shortcuts_dir.exists():
        shortcuts = list(shortcuts_dir.glob("*.command"))
        print(f"  ✅ Found {len(shortcuts)} shortcuts:")
        for shortcut in shortcuts:
            if os.access(shortcut, os.X_OK):
                print(f"    ✅ {shortcut.name}: Executable")
            else:
                print(f"    ❌ {shortcut.name}: Not executable")
    else:
        print("  ❌ Shortcuts directory not found")

def main():
    """Run all diagnostics."""
    print("🚀 PaulyOps System Diagnostics")
    print("=" * 40)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Run all tests
    folder_results = test_folder_paths()
    test_config_flags()
    test_provider_connectivity()
    test_agent_health()
    test_launchagent()
    test_desktop_shortcuts()
    
    # Summary
    print("\n📊 Summary:")
    total_paths = len(folder_results)
    existing_paths = sum(1 for r in folder_results.values() if r["exists"])
    print(f"  Folders: {existing_paths}/{total_paths} exist")
    
    print("\n✅ Diagnostics complete!")

if __name__ == "__main__":
    main()

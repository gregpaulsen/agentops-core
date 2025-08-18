#!/usr/bin/env python3
"""
PaulyOps Auto-Doctor Agent - Self-Healing Core
Automatically repairs common issues before health checks.
"""

import os
import sys
import json
import shutil
import subprocess
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Define paths
ROOT = Path.home() / "PaulyOps"
REPORTS_DIR = ROOT / "Reports"
BACKUPS_DIR = ROOT / "Backups"
CONFIG_DIR = ROOT / "config"

def load_status_flags():
    """Load status flags from config file."""
    try:
        flags_path = CONFIG_DIR / "status_flags.json"
        if flags_path.exists():
            with open(flags_path, 'r') as f:
                return json.load(f)
    except Exception as e:
        print(f"Warning: Could not load status flags: {e}")
    
            # Default flags
        return {
            "check_git": True,
            "check_router": False,
            "check_endpoints": False,
            "check_launchd": True,
            "launchd_jobs": ["com.paulyops.nightlyreport"],
            "skip_launchd_jobs": ["com.bigsky.backup.10pm", "com.bigsky.router.watch"],
            "company_name": "PaulyOps",
            "dropzone_name": "PaulyOpsDropzone"
        }

def log(message):
    """Log message with timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    log_entry = f"[{timestamp}] {message}"
    print(log_entry)
    
    # Write to log file
    log_file = REPORTS_DIR / f".autodoctor_log_{datetime.now().strftime('%Y%m%d')}.txt"
    with open(log_file, 'a') as f:
        f.write(log_entry + '\n')

def ensure_folders():
    """Ensure all required folders exist."""
    folders = [REPORTS_DIR, BACKUPS_DIR, CONFIG_DIR, BACKUPS_DIR / "archive"]
    
    for folder in folders:
        if not folder.exists():
            folder.mkdir(parents=True, exist_ok=True)
            log(f"folder: created {folder}")

def reconcile_backup_rotation():
    """Ensure only 1 active backup, move others to archive."""
    if not BACKUPS_DIR.exists():
        return
    
    # Find all zip files
    zip_files = list(BACKUPS_DIR.glob("*.zip"))
    
    if len(zip_files) <= 1:
        log("rotation: no action needed (1 or fewer backups)")
        return
    
    # Sort by modification time (oldest first)
    zip_files.sort(key=lambda f: f.stat().st_mtime)
    
    # Move all but the newest to archive
    archive_dir = BACKUPS_DIR / "archive"
    if not archive_dir.exists():
        archive_dir.mkdir(parents=True, exist_ok=True)
    
    moved_count = 0
    for zip_file in zip_files[:-1]:  # All but the newest
        try:
            archive_path = archive_dir / zip_file.name
            zip_file.rename(archive_path)
            log(f"rotation: moved '{zip_file.name}' -> archive/")
            moved_count += 1
        except Exception as e:
            log(f"rotation: error moving {zip_file.name}: {e}")
    
    # Verify only 1 backup remains
    remaining_backups = list(BACKUPS_DIR.glob("*.zip"))
    if len(remaining_backups) > 1:
        log(f"rotation: WARNING - {len(remaining_backups)} backups still active, removing extras")
        for backup in remaining_backups[1:]:
            try:
                backup.unlink()
                log(f"rotation: removed extra backup '{backup.name}'")
            except Exception as e:
                log(f"rotation: error removing {backup.name}: {e}")
    
    # Create rotation success marker
    rotation_marker = REPORTS_DIR / ".backup_rotation_last_success"
    rotation_marker.touch()
    log(f"rotation: completed - {moved_count} moved to archive, 1 active backup maintained")

def check_launchagents():
    """Check and repair LaunchAgent jobs."""
    status_flags = load_status_flags()
    
    if not status_flags.get("check_launchd", True):
        log("launchd: skipped (flag)")
        return
    
    launchd_jobs = status_flags.get("launchd_jobs", ["com.paulyops.nightlyreport"])
    launch_agents_dir = Path.home() / "Library" / "LaunchAgents"
    
    if not launch_agents_dir.exists():
        log("launchd: LaunchAgents directory not found")
        return
    
    for job in launchd_jobs:
        plist_path = launch_agents_dir / f"{job}.plist"
        
        if plist_path.exists():
            # Check if plist is valid
            try:
                result = subprocess.run(["plutil", "-lint", str(plist_path)], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    log(f"launchd: {job} is valid")
                else:
                    log(f"launchd: {job} is invalid - {result.stderr.strip()}")
            except Exception as e:
                log(f"launchd: error checking {job} - {e}")
        else:
            log(f"launchd: {job}.plist not found")

def check_router_endpoints():
    """Handle router and endpoint flags."""
    status_flags = load_status_flags()
    
    if not status_flags.get("check_router", False):
        log("router: disabled (flag)")
        # Create disabled marker
        disabled_marker = REPORTS_DIR / ".router_disabled"
        if not disabled_marker.exists():
            disabled_marker.touch()
            log("router: created disabled marker")
    
    if not status_flags.get("check_endpoints", False):
        log("endpoints: disabled (flag)")

def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="PaulyOps Auto-Doctor - Self-healing agent")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be changed without making changes")
    args = parser.parse_args()
    
    if args.dry_run:
        print("🔍 DRY RUN MODE - No changes will be made")
        return
    
    log("🚀 Starting Auto-Doctor self-healing checks...")
    
    # Run all checks
    ensure_folders()
    reconcile_backup_rotation()
    check_launchagents()
    check_router_endpoints()
    
    log("🎉 Auto-Doctor complete!")

if __name__ == "__main__":
    main()

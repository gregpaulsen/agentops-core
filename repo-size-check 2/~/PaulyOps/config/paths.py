#!/usr/bin/env python3
"""
PaulyOps & BigSkyAg - Centralized Path Configuration
All scripts should import and use these paths for consistency.
"""

from pathlib import Path
import os

# ===== PROJECT ROOT =====
ROOT = Path.home() / "PaulyOps"

# ===== CORE PATHS =====
paths = {
    # Core directories
    "root": ROOT,
    "commands": ROOT / "Coding_Commands",
    "reports": ROOT / "Reports", 
    "backups": ROOT / "Backups",
    "config": ROOT / "config",
    "ui": ROOT / "UI",
    "server": ROOT / "server",
    
    # Key files
    "system_health": ROOT / "System_Health_Report.md",
    "nightly_sent_marker": ROOT / "Reports" / ".nightly_last_sent",
    
    # External paths (DO NOT CHANGE)
    "dropzone": Path.home() / "Desktop" / "BigSkyAgDropzone",
    "desktop": Path.home() / "Desktop",
    "documents": Path.home() / "Documents",
    
    # Backup locations
    "backup_root": Path("/Volumes/BigSkyAgSSD/BigSkyAg/00_Admin/Backups"),
    "backup_archive": Path("/Volumes/BigSkyAgSSD/BigSkyAg/00_Admin/Backups/Archive"),
    
    # Git repositories
    "repo_root": Path.home() / "Desktop" / "repo-size-check",
}

# ===== ENVIRONMENT CONFIG =====
def get_env_path(key, default=None):
    """Get path from environment variable or use default"""
    env_val = os.environ.get(f"PAULYOPS_{key.upper()}")
    if env_val:
        return Path(env_val)
    return default or paths.get(key)

# ===== PATH VALIDATION =====
def ensure_paths_exist():
    """Create any missing directories"""
    for key, path in paths.items():
        if isinstance(path, Path) and key not in ['system_health', 'nightly_sent_marker']:
            if path.suffix == '':  # Directory
                path.mkdir(parents=True, exist_ok=True)
                print(f"✅ Ensured directory: {path}")

def get_safe_path(key):
    """Get path and ensure parent directory exists"""
    path = paths[key]
    if path.suffix:  # File
        path.parent.mkdir(parents=True, exist_ok=True)
    else:  # Directory
        path.mkdir(parents=True, exist_ok=True)
    return path

# ===== CONFIG FILE PATHS =====
config_files = {
    "env": ROOT / "config" / ".env",
    "smtp": ROOT / "config" / "smtp.json",
    "providers": ROOT / "config" / "providers.json",
}

# ===== LOGGING PATHS =====
log_paths = {
    "system_health": ROOT / "Reports" / "system_health.log",
    "nightly_report": ROOT / "Reports" / "nightly_report.log",
    "backup": ROOT / "Reports" / "backup.log",
    "router": ROOT / "Reports" / "router.log",
}

# Auto-create paths on import
if __name__ != "__main__":
    ensure_paths_exist()

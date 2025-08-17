#!/usr/bin/env python3
"""
Status Flags Module for PaulyOps
Loads and manages configuration flags for system checks.
"""

import json
from pathlib import Path

def load_status_flags():
    """Load status flags from config file."""
    try:
        # Get config directory
        config_dir = Path.home() / "PaulyOps" / "config"
        flags_path = config_dir / "status_flags.json"
        
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
        "check_backup_upload": True,
        "check_launchd_jobs": True,
        "check_launchd": True,
        "check_provider_credentials": True,
        "check_spotlight": True,
        "git_repos": ["/Users/gregpaulsen/Desktop/repo-size-check"],
        "git_paths": ["/Volumes/BigSkyAgSSD/BigSkyAg", "/Volumes/BigSkyAgSSD/PaulyOps", "/Volumes/BigSkyAgSSD/agentops-core"],
        "skip_git_repos": ["/Volumes/BigSkyAgSSD/agentops-core", "/Volumes/BigSkyAgSSD/PaulyOps"],
        "endpoint_urls": [],
        "launchd_jobs": ["com.bigsky.nightlyreport"],
        "skip_launchd_jobs": ["com.bigsky.backup.10pm", "com.bigsky.router.watch"]
    }

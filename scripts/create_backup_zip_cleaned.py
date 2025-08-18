import sys
from pathlib import Path
import os
from zipfile import ZipFile
from datetime import datetime

# Allow imports from Coding_Commands folder
sys.path.append(str(Path.home() / "Desktop" / "Coding_Commands"))

from bigsky_path_utils import (
    find_bigsky_root,
    get_bigsky_subfolder,
    safe_print_bigsky_path,
    backup_script
)

def should_exclude_file(file_path, folder_path):
    """Check if file should be excluded from backup."""
    rel_path = os.path.relpath(file_path, folder_path)
    
    # Exclude backup folders and files
    exclude_patterns = [
        "00_Admin/Backups/",  # Don't backup the backup folder
        "00_Admin/Backups/*.zip",  # Don't backup zip files
        "00_Admin/Backups/*.chunk_*",  # Don't backup chunk files
        ".git/",  # Don't backup git folder (can be large)
        ".DS_Store",  # macOS system files
        "Thumbs.db",  # Windows system files
        "*.tmp",  # Temporary files
        "*.temp",  # Temporary files
        "*.log",  # Log files (optional)
        "__pycache__/",  # Python cache
        "*.pyc",  # Python compiled files
        "node_modules/",  # Node.js modules
        ".Trash/",  # Trash folder
        "~",  # Backup files
    ]
    
    for pattern in exclude_patterns:
        if pattern.endswith("/") and rel_path.startswith(pattern):
            return True
        elif pattern.startswith("*") and rel_path.endswith(pattern[1:]):
            return True
        elif rel_path == pattern:
            return True
        elif pattern in rel_path:
            return True
    
    return False

def zip_folder_verbose(folder_path, output_zip_path):
    with ZipFile(output_zip_path, 'w') as zipf:
        for foldername, subfolders, filenames in os.walk(folder_path, followlinks=True):
            for filename in filenames:
                file_path = os.path.join(foldername, filename)

                # Check if file should be excluded
                if should_exclude_file(file_path, folder_path):
                    print(f"🚫 Excluded: {os.path.relpath(file_path, folder_path)}")
                    continue

                try:
                    arcname = os.path.relpath(file_path, folder_path)
                    print(f"📦 Adding: {arcname}")
                    zipf.write(file_path, arcname)
                except Exception as e:
                    print(f"⚠️ Skipped: {file_path} → {e}")
    print(f"✅ Backup complete: {output_zip_path}")
    size = os.path.getsize(output_zip_path) / (1024 ** 3)
    print(f"📏 Total size: {size:.2f} GB")

def prune_old_backups(folder: Path, keep: int = 2):
    backups = sorted(folder.glob("BigSkyAg_Backup_*.zip"), key=lambda f: f.stat().st_mtime, reverse=True)
    for old_backup in backups[keep:]:
        print(f"🗑️  Deleting old backup: {old_backup.name}")
        old_backup.unlink()

# --- MAIN SCRIPT ---
if __name__ == "__main__":
    source = get_bigsky_subfolder("")
    backup_dir = get_bigsky_subfolder("00_Admin/Backups")
    today = datetime.now().strftime("%Y-%m-%d")
    output_file = os.path.join(backup_dir, f"BigSkyAg_Backup_{today}.zip")

    print(f"🚀 Starting backup: {source}")
    print(f"📁 Excluding backup folder and system files...")
    zip_folder_verbose(str(source), output_file)
    prune_old_backups(Path(backup_dir), keep=2)


import sys
from pathlib import Path

# Ensure we can import from the same folder
sys.path.insert(0, str(Path(__file__).resolve().parent))
from bigsky_path_utils import get_bigsky_subfolder

def prune_old_backups(folder: Path, keep: int = 2):
    backups = sorted(folder.glob("BigSkyAg_Backup_*.zip"), key=lambda f: f.stat().st_mtime, reverse=True)
    for old_backup in backups[keep:]:
        print(f"🗑️  Deleting old backup: {old_backup.name}")
        old_backup.unlink()

# Test just the cleanup part
if __name__ == "__main__":
    backup_dir = get_bigsky_subfolder("00_Admin/Backups")
    prune_old_backups(Path(backup_dir), keep=2)


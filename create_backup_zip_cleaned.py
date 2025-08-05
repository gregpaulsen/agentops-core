import sys
from pathlib import Path
sys.path.append(str(Path.home() / "Desktop" / "Coding_Commands"))

from bigsky_path_utils import (
    find_agent_root,
    get_agent_subfolder,
    find_bigsky_root,
    get_bigsky_subfolder,
    safe_print_bigsky_path,
    backup_script
)

from pathlib import Path
sys.path.append(str(Path.home() / "Desktop" / "Coding_Commands"))

from bigsky_path_utils import (
    find_agent_root,
    get_agent_subfolder,
    find_bigsky_root,
    get_bigsky_subfolder,
    safe_print_bigsky_path,
    backup_script
)

import os
from pathlib import Path
from zipfile import ZipFile
from datetime import datetime

# Ensure local import path works
sys.path.insert(0, str(Path(__file__).resolve().parent))
from bigsky_path_utils import get_bigsky_subfolder

def zip_folder_verbose(folder_path, output_zip_path):
    with ZipFile(output_zip_path, 'w') as zipf:
        for foldername, subfolders, filenames in os.walk(folder_path):
            for filename in filenames:
                file_path = os.path.join(foldername, filename)
                arcname = os.path.relpath(file_path, folder_path)
                print(f"📦 Adding: {arcname}")
                zipf.write(file_path, arcname)
    print(f"✅ Backup complete: {output_zip_path}")
    size = os.path.getsize(output_zip_path) / (1024 ** 3)
    print(f"📏 Total size: {size:.2f} GB")

def prune_old_backups(folder: Path, keep: int = 2):
    backups = sorted(folder.glob("BigSkyAg_Backup_*.zip"), key=lambda f: f.stat().st_mtime, reverse=True)
    for old_backup in backups[keep:]:
        print(f"🗑️  Deleting old backup: {old_backup.name}")
        old_backup.unlink()

# Main execution
if __name__ == "__main__":
    source = get_bigsky_subfolder("")
    backup_dir = get_bigsky_subfolder("00_Admin/Backups")
    today = datetime.now().strftime("%Y-%m-%d")
    output_file = os.path.join(backup_dir, f"BigSkyAg_Backup_{today}.zip")

    print(f"🚀 Starting backup: {source}")
    zip_folder_verbose(str(source), output_file)
    prune_old_backups(Path(backup_dir), keep=2)


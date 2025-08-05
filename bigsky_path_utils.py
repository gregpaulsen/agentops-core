from pathlib import Path
import shutil
import datetime

# Default structure for Big Sky Ag and white-label users
DEFAULT_REQUIRED_SUBFOLDERS = ["00_Admin", "DropZone"]

# 📦 Universal AgentOps – detects ANY valid agent folder
def find_agent_root(required_folders=None):
    """
    Scans all mounted drives to find a folder with the required structure.
    Used for white-label AgentOps setups.
    """
    volumes = Path("/Volumes")
    required = required_folders or DEFAULT_REQUIRED_SUBFOLDERS

    for vol in volumes.iterdir():
        if vol.is_dir():
            for sub in vol.iterdir():
                if sub.is_dir():
                    if all((sub / r).exists() for r in required):
                        return sub.resolve()
    raise FileNotFoundError("❌ No valid agent folder found on any mounted drive.")

# 🏷️ Big Sky Ag – legacy compatibility
def find_bigsky_root():
    """
    Looks specifically for the 'BigSkyAg' folder on mounted drives.
    Used by original BigSky scripts.
    """
    volumes = Path("/Volumes")
    for vol in volumes.iterdir():
        if vol.is_dir():
            candidate = vol / "BigSkyAg"
            if all((candidate / r).exists() for r in DEFAULT_REQUIRED_SUBFOLDERS):
                return candidate.resolve()
    raise FileNotFoundError("❌ No valid BigSkyAg folder found on any mounted drive.")

# 📂 Get subfolder inside Big Sky Ag
def get_bigsky_subfolder(subfolder: str) -> Path:
    """
    Returns the absolute path to a subfolder inside BigSkyAg root.
    """
    root = find_bigsky_root()
    path = root / subfolder
    if not path.exists():
        raise FileNotFoundError(f"❌ Subfolder not found: {path}")
    return path.resolve()

# 📂 Get subfolder inside any agent (white-label compatible)
def get_agent_subfolder(subfolder: str, required_folders=None) -> Path:
    """
    Returns the absolute path to a subfolder inside any valid AgentOps root.
    Accepts custom required folder list for flexibility.
    """
    root = find_agent_root(required_folders=required_folders)
    path = root / subfolder
    if not path.exists():
        raise FileNotFoundError(f"❌ Subfolder not found: {path}")
    return path.resolve()

# 🧪 Simple test for BigSkyAg path
def safe_print_bigsky_path():
    try:
        root = find_bigsky_root()
        print(f"✅ BigSkyAg path found: {root}")
    except FileNotFoundError as e:
        print(str(e))

# 🛡️ Backup script before editing
def backup_script(file_path: Path):
    """
    Creates a timestamped backup copy of any file you plan to patch or overwrite.
    """
    if not file_path.exists():
        print(f"⚠️ File not found for backup: {file_path}")
        return
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = file_path.with_name(file_path.stem + f"_backup_{timestamp}" + file_path.suffix)
    shutil.copy2(file_path, backup_path)
    print(f"🔒 Backup created: {backup_path}")

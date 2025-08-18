from pathlib import Path

def find_bigsky_root():
    """
    Locates the BigSkyAg root folder in preferred order:
    1. External SSD (/Volumes/BigSkyAgSSD)
    2. Local non-synced folder (~/BigSkyAg)
    3. Cloud fallback (Google Drive iCloud-synced) — last resort only
    """
    # ✅ Primary: External SSD
    ssd_path = Path("/Volumes/BigSkyAgSSD/BigSkyAg")
    if ssd_path.exists():
        return ssd_path

    # ✅ Secondary: Local folder (not cloud-synced)
    local_path = Path.home() / "BigSkyAg"
    if local_path.exists():
        return local_path

    # ❌ LAST resort: Cloud-synced Google Drive folder
    cloud_path = Path.home() / "Library/CloudStorage/GoogleDrive-gregpaulsen26@gmail.com/My Drive/BigSkyAg"
    if cloud_path.exists():
        return cloud_path

    raise FileNotFoundError("❌ BigSkyAg root not found in any expected location.")

def get_bigsky_subfolder(relative_path=""):
    """
    Returns the full path to a subfolder within BigSkyAg root
    """
    return find_bigsky_root() / relative_path

# Optional utility function to print and return path safely
def safe_print_bigsky_path(relative_path=""):
    path = get_bigsky_subfolder(relative_path)
    print(f"📂 Path: {path}")
    return path

# Placeholder for any backup-related utility logic
def backup_script():
    print("🧠 Placeholder for backup-specific logic (not used yet)")


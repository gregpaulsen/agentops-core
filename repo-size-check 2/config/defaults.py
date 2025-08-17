"""Default configuration values for PaulyOps."""

from pathlib import Path

# Environment
ENV = "dev"
LOG_LEVEL = "INFO"

# Storage
STORAGE_PROVIDER = "local"  # local | google | dropbox | s3

# Paths
BACKUP_DIR = "00_Admin/Backups"
ARCHIVE_DIR = "00_Admin/Backups/archive"
INGEST_FOLDER_NAME = "BigSkyAgDropzone"

# Provider-specific defaults
GOOGLE_DRIVE_FOLDER_ID = ""
DROPBOX_ROOT_PATH = ""
S3_BUCKET = ""
S3_PREFIX = ""

# Backup settings
BACKUP_RETENTION_DAYS = 30
MAX_BACKUP_SIZE_GB = 10

# Validation
REQUIRED_FOLDERS = [
    "00_Admin",
    "00_Admin/Backups",
    "00_Admin/Backups/archive",
]

# Company-specific
COMPANY_NAME = "BigSkyAg"

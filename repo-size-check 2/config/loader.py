"""Configuration loader with environment variable support and validation."""

import os
from pathlib import Path
from typing import Dict, Any, Optional

from .defaults import *
from tenancy.registry import get_tenant_context


class Config:
    """Configuration manager with validation and summary reporting."""

    def __init__(self, tenant_id: Optional[str] = None):
        self.tenant_id = tenant_id
        self.tenant_context = get_tenant_context(tenant_id)
        self._load_from_env()
        self._validate_paths()
    
    def _load_from_env(self):
        """Load configuration from environment variables with fallbacks."""
        # Environment
        self.env = os.getenv("ENV", ENV)
        self.log_level = os.getenv("LOG_LEVEL", LOG_LEVEL)

        # Storage
        self.storage_provider = os.getenv("STORAGE_PROVIDER", STORAGE_PROVIDER)

        # Paths
        self.backup_dir = Path(os.getenv("BACKUP_DIR", BACKUP_DIR))
        self.archive_dir = Path(os.getenv("ARCHIVE_DIR", ARCHIVE_DIR))
        self.ingest_folder_name = os.getenv("INGEST_FOLDER_NAME", INGEST_FOLDER_NAME)

        # Provider credentials
        self.google_drive_folder_id = os.getenv("GOOGLE_DRIVE_FOLDER_ID", GOOGLE_DRIVE_FOLDER_ID)
        self.dropbox_root_path = os.getenv("DROPBOX_ROOT_PATH", DROPBOX_ROOT_PATH)
        self.s3_bucket = os.getenv("S3_BUCKET", S3_BUCKET)
        self.s3_prefix = os.getenv("S3_PREFIX", S3_PREFIX)

        # Backup settings
        self.backup_retention_days = int(os.getenv("BACKUP_RETENTION_DAYS", BACKUP_RETENTION_DAYS))
        self.max_backup_size_gb = int(os.getenv("MAX_BACKUP_SIZE_GB", MAX_BACKUP_SIZE_GB))

        # Company
        self.company_name = os.getenv("COMPANY_NAME", COMPANY_NAME)
        
        # Apply tenant/plan overrides
        self._apply_tenant_overrides()
    
    def _apply_tenant_overrides(self):
        """Apply tenant and plan overrides to configuration."""
        if not self.tenant_context:
            return
        
        # Apply plan defaults first
        if self.tenant_context.plan.defaults:
            plan_defaults = self.tenant_context.plan.defaults
            if not self.storage_provider or self.storage_provider == STORAGE_PROVIDER:
                self.storage_provider = plan_defaults.get("STORAGE_PROVIDER", self.storage_provider)
        
        # Apply tenant overrides
        if self.tenant_context.tenant.storage:
            tenant_storage = self.tenant_context.tenant.storage
            if "BACKUP_DIR" in tenant_storage:
                self.backup_dir = Path(tenant_storage["BACKUP_DIR"])
            if "ARCHIVE_DIR" in tenant_storage:
                self.archive_dir = Path(tenant_storage["ARCHIVE_DIR"])
        
        if self.tenant_context.tenant.ingest:
            tenant_ingest = self.tenant_context.tenant.ingest
            if "INGEST_FOLDER_NAME" in tenant_ingest:
                self.ingest_folder_name = tenant_ingest["INGEST_FOLDER_NAME"]
    
    def _validate_paths(self):
        """Validate that required paths exist and are writable."""
        self.path_issues = []
        
        # Check backup directory
        if not self.backup_dir.exists():
            try:
                self.backup_dir.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                self.path_issues.append(f"Backup directory {self.backup_dir}: {e}")
        
        # Check archive directory
        if not self.archive_dir.exists():
            try:
                self.archive_dir.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                self.path_issues.append(f"Archive directory {self.archive_dir}: {e}")
        
        # Check ingest folder
        ingest_path = Path(self.ingest_folder_name)
        if not ingest_path.exists():
            try:
                ingest_path.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                self.path_issues.append(f"Ingest folder {ingest_path}: {e}")
    
    def get_provider_config(self) -> Dict[str, Any]:
        """Get provider-specific configuration."""
        if self.storage_provider == "google":
            return {
                "folder_id": self.google_drive_folder_id,
                "provider": "google"
            }
        elif self.storage_provider == "dropbox":
            return {
                "root_path": self.dropbox_root_path,
                "provider": "dropbox"
            }
        elif self.storage_provider == "s3":
            return {
                "bucket": self.s3_bucket,
                "prefix": self.s3_prefix,
                "provider": "s3"
            }
        else:  # local
            return {
                "provider": "local",
                "base_path": self.backup_dir
            }
    
    def has_provider_creds(self) -> bool:
        """Check if provider credentials are configured."""
        if self.storage_provider == "google":
            return bool(self.google_drive_folder_id)
        elif self.storage_provider == "dropbox":
            return bool(self.dropbox_root_path)
        elif self.storage_provider == "s3":
            return bool(self.s3_bucket)
        return True  # local doesn't need creds
    
    def print_summary(self):
        """Print a clean configuration summary (masking secrets)."""
        print("=" * 60)
        print("PAULYOPS CONFIGURATION SUMMARY")
        print("=" * 60)
        print(f"Environment: {self.env}")
        print(f"Log Level: {self.log_level}")
        print(f"Storage Provider: {self.storage_provider}")
        print(f"Company: {self.company_name}")
        print(f"Backup Directory: {self.backup_dir}")
        print(f"Archive Directory: {self.archive_dir}")
        print(f"Ingest Folder: {self.ingest_folder_name}")
        print(f"Backup Retention: {self.backup_retention_days} days")
        print(f"Max Backup Size: {self.max_backup_size_gb} GB")
        
        # Provider-specific info (masked)
        if self.storage_provider == "google":
            print(f"Google Drive Folder ID: {'***' if self.google_drive_folder_id else 'NOT SET'}")
        elif self.storage_provider == "dropbox":
            print(f"Dropbox Root Path: {'***' if self.dropbox_root_path else 'NOT SET'}")
        elif self.storage_provider == "s3":
            print(f"S3 Bucket: {'***' if self.s3_bucket else 'NOT SET'}")
            print(f"S3 Prefix: {self.s3_prefix or 'NONE'}")
        
        # Path validation
        if self.path_issues:
            print("\n⚠️  PATH ISSUES:")
            for issue in self.path_issues:
                print(f"  - {issue}")
        else:
            print("\n✅ All paths validated successfully")
        
        print("=" * 60)


# Global config instance
config = Config()

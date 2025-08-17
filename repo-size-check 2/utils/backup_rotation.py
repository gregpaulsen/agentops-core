"""Backup rotation utility for PaulyOps."""

import shutil
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from config.loader import config


class BackupRotator:
    """Manages backup rotation: keeps one current, moves others to archive."""
    
    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.backup_dir = config.backup_dir
        self.archive_dir = config.archive_dir
    
    def rotate_backups(self, new_backup_path: Path) -> List[Path]:
        """
        Rotate backups: move existing backups to archive, keep new one current.
        
        Args:
            new_backup_path: Path to the new backup file
            
        Returns:
            List of paths that were moved to archive
        """
        moved_files = []
        
        # Find existing backup files (excluding the new one)
        existing_backups = self._find_existing_backups()
        
        if not existing_backups:
            if not self.dry_run:
                print(f"ℹ️  No existing backups to rotate")
            else:
                print(f"ℹ️  [DRY-RUN] No existing backups to rotate")
            return moved_files
        
        # Move existing backups to archive
        for backup_file in existing_backups:
            archive_path = self.archive_dir / backup_file.name
            
            if self.dry_run:
                print(f"ℹ️  [DRY-RUN] Would move {backup_file} to {archive_path}")
            else:
                try:
                    shutil.move(str(backup_file), str(archive_path))
                    print(f"✅ Moved {backup_file.name} to archive")
                    moved_files.append(archive_path)
                except Exception as e:
                    print(f"❌ Failed to move {backup_file.name}: {e}")
        
        return moved_files
    
    def _find_existing_backups(self) -> List[Path]:
        """Find existing backup files in the backup directory."""
        if not self.backup_dir.exists():
            return []
        
        # Look for common backup file patterns
        backup_patterns = [
            "*.zip",
            "*.tar.gz",
            "*_backup_*.zip",
            "*_backup_*.tar.gz",
            "backup_*.zip",
            "backup_*.tar.gz"
        ]
        
        existing_backups = []
        for pattern in backup_patterns:
            existing_backups.extend(self.backup_dir.glob(pattern))
        
        return sorted(existing_backups, key=lambda p: p.stat().st_mtime, reverse=True)
    
    def cleanup_old_archives(self, max_age_days: Optional[int] = None) -> List[Path]:
        """
        Clean up old archive files based on age.
        
        Args:
            max_age_days: Maximum age in days (uses config if None)
            
        Returns:
            List of paths that were deleted
        """
        if max_age_days is None:
            max_age_days = config.backup_retention_days
        
        if not self.archive_dir.exists():
            return []
        
        cutoff_time = datetime.now().timestamp() - (max_age_days * 24 * 3600)
        deleted_files = []
        
        for archive_file in self.archive_dir.iterdir():
            if archive_file.is_file() and archive_file.stat().st_mtime < cutoff_time:
                if self.dry_run:
                    print(f"ℹ️  [DRY-RUN] Would delete old archive: {archive_file}")
                else:
                    try:
                        archive_file.unlink()
                        print(f"🗑️  Deleted old archive: {archive_file.name}")
                        deleted_files.append(archive_file)
                    except Exception as e:
                        print(f"❌ Failed to delete {archive_file.name}: {e}")
        
        return deleted_files
    
    def get_backup_summary(self) -> dict:
        """Get a summary of current backup state."""
        current_backups = self._find_existing_backups()
        archive_files = list(self.archive_dir.glob("*")) if self.archive_dir.exists() else []
        
        return {
            "current_backups": len(current_backups),
            "archive_files": len(archive_files),
            "backup_dir": str(self.backup_dir),
            "archive_dir": str(self.archive_dir),
            "total_size_gb": self._calculate_total_size_gb(current_backups + archive_files)
        }
    
    def _calculate_total_size_gb(self, files: List[Path]) -> float:
        """Calculate total size of files in GB."""
        total_bytes = sum(f.stat().st_size for f in files if f.is_file())
        return round(total_bytes / (1024**3), 2)

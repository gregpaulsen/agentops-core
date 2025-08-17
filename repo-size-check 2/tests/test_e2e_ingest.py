"""End-to-end integration tests for PaulyOps ingest system."""

import json
import shutil
import tempfile
from pathlib import Path
from datetime import datetime

import pytest

from config.loader import config
from utils.backup_rotation import BackupRotator
from utils.logging import logger


class TestE2EIngest:
    """End-to-end tests for the ingest system."""
    
    @pytest.fixture
    def temp_ingest_dir(self):
        """Create a temporary ingest directory for testing."""
        temp_dir = Path(tempfile.mkdtemp())
        ingest_dir = temp_dir / config.ingest_folder_name
        ingest_dir.mkdir()
        yield ingest_dir
        shutil.rmtree(temp_dir)
    
    @pytest.fixture
    def sample_files(self):
        """Get paths to sample test files."""
        fixture_dir = Path(__file__).parent / "fixtures" / "sample_ingest"
        return {
            "txt": fixture_dir / "sample_document.txt",
            "json": fixture_dir / "sample_data.json",
            "yaml": fixture_dir / "sample_config.yaml"
        }
    
    def test_imports(self):
        """Test that all required modules can be imported."""
        # This test ensures our basic imports work
        assert config is not None
        assert BackupRotator is not None
        assert logger is not None
    
    def test_config_loading(self):
        """Test that configuration loads correctly."""
        assert config.storage_provider in ["local", "google", "dropbox", "s3"]
        assert config.backup_dir.exists() or config.backup_dir.parent.exists()
        assert config.ingest_folder_name == "BigSkyAgDropzone"
    
    def test_backup_rotation_dry_run(self):
        """Test backup rotation in dry-run mode."""
        rotator = BackupRotator(dry_run=True)
        summary = rotator.get_backup_summary()
        
        assert "current_backups" in summary
        assert "archive_files" in summary
        assert "backup_dir" in summary
        assert "archive_dir" in summary
        assert "total_size_gb" in summary
    
    def test_sample_files_exist(self, sample_files):
        """Test that sample files exist for testing."""
        for file_type, file_path in sample_files.items():
            assert file_path.exists(), f"Sample {file_type} file not found: {file_path}"
    
    def test_ingest_folder_creation(self, temp_ingest_dir):
        """Test that ingest folder can be created and used."""
        assert temp_ingest_dir.exists()
        assert temp_ingest_dir.is_dir()
        
        # Test file creation
        test_file = temp_ingest_dir / "test.txt"
        test_file.write_text("test content")
        assert test_file.exists()
    
    @pytest.mark.local
    def test_local_storage_ingest(self, temp_ingest_dir, sample_files):
        """Test local storage ingest workflow."""
        if config.storage_provider != "local":
            pytest.skip("Not using local storage provider")
        
        # Copy sample files to ingest directory
        ingested_files = []
        for file_type, source_file in sample_files.items():
            dest_file = temp_ingest_dir / source_file.name
            shutil.copy2(source_file, dest_file)
            ingested_files.append(dest_file)
            assert dest_file.exists()
        
        # Simulate routing (for now, just verify files exist)
        for file_path in ingested_files:
            assert file_path.exists()
            assert file_path.stat().st_size > 0
        
        # Test backup rotation
        rotator = BackupRotator(dry_run=True)
        summary = rotator.get_backup_summary()
        assert summary["backup_dir"] == str(config.backup_dir)
    
    @pytest.mark.s3
    def test_s3_storage_ingest(self, temp_ingest_dir, sample_files):
        """Test S3 storage ingest workflow."""
        if config.storage_provider != "s3":
            pytest.skip("Not using S3 storage provider")
        
        if not config.s3_bucket:
            pytest.skip("S3 bucket not configured")
        
        # This would test actual S3 operations
        # For now, just verify configuration
        assert config.storage_provider == "s3"
        assert config.s3_bucket
    
    @pytest.mark.dropbox
    def test_dropbox_storage_ingest(self, temp_ingest_dir, sample_files):
        """Test Dropbox storage ingest workflow."""
        if config.storage_provider != "dropbox":
            pytest.skip("Not using Dropbox storage provider")
        
        if not config.dropbox_root_path:
            pytest.skip("Dropbox root path not configured")
        
        # This would test actual Dropbox operations
        # For now, just verify configuration
        assert config.storage_provider == "dropbox"
        assert config.dropbox_root_path
    
    @pytest.mark.google
    def test_google_storage_ingest(self, temp_ingest_dir, sample_files):
        """Test Google Drive storage ingest workflow."""
        if config.storage_provider != "google":
            pytest.skip("Not using Google storage provider")
        
        if not config.google_drive_folder_id:
            pytest.skip("Google Drive folder ID not configured")
        
        # This would test actual Google Drive operations
        # For now, just verify configuration
        assert config.storage_provider == "google"
        assert config.google_drive_folder_id
    
    def test_backup_rotation_workflow(self):
        """Test the complete backup rotation workflow."""
        rotator = BackupRotator(dry_run=True)
        
        # Test rotation with a dummy file
        dummy_backup = Path("dummy_backup.zip")
        try:
            dummy_backup.write_text("dummy content")
            moved_files = rotator.rotate_backups(dummy_backup)
            # In dry-run mode, no files should actually be moved
            assert isinstance(moved_files, list)
        finally:
            if dummy_backup.exists():
                dummy_backup.unlink()
    
    def test_logging_integration(self):
        """Test that logging works correctly."""
        logger.info("Test log message")
        # If we get here without error, logging is working
    
    def test_config_validation(self):
        """Test configuration validation."""
        # Test that required paths can be created
        assert config.backup_dir.parent.exists() or config.backup_dir.parent.parent.exists()
        assert config.archive_dir.parent.exists() or config.archive_dir.parent.parent.exists()
        
        # Test that ingest folder name is valid
        assert config.ingest_folder_name
        assert len(config.ingest_folder_name) > 0

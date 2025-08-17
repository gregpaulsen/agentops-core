#!/usr/bin/env python3
"""System health check for PaulyOps."""

import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple

from config.loader import config
from utils.logging import logger


class SystemHealthChecker:
    """Comprehensive system health checker for PaulyOps."""
    
    def __init__(self):
        self.issues = []
        self.warnings = []
        self.successes = []
    
    def check_environment(self) -> bool:
        """Check environment variables and configuration."""
        logger.info("🔍 Checking environment configuration...")
        
        # Check required environment variables
        required_vars = ["ENV", "LOG_LEVEL", "STORAGE_PROVIDER"]
        for var in required_vars:
            if os.getenv(var):
                self.successes.append(f"✅ {var} is set")
            else:
                self.warnings.append(f"⚠️  {var} not set (using default)")
        
        # Check storage provider configuration
        provider = config.storage_provider
        if provider == "local":
            self.successes.append("✅ Local storage provider configured")
        elif provider in ["google", "dropbox", "s3"]:
            if config.has_provider_creds():
                self.successes.append(f"✅ {provider} credentials configured")
            else:
                self.issues.append(f"❌ {provider} credentials not configured")
        else:
            self.issues.append(f"❌ Unknown storage provider: {provider}")
        
        return len(self.issues) == 0
    
    def check_paths(self) -> bool:
        """Check that required paths exist and are writable."""
        logger.info("🔍 Checking file system paths...")
        
        required_paths = [
            config.backup_dir,
            config.archive_dir,
            Path(config.ingest_folder_name)
        ]
        
        for path in required_paths:
            if path.exists():
                if os.access(path, os.W_OK):
                    self.successes.append(f"✅ {path} exists and is writable")
                else:
                    self.issues.append(f"❌ {path} exists but is not writable")
            else:
                try:
                    path.mkdir(parents=True, exist_ok=True)
                    self.successes.append(f"✅ Created {path}")
                except Exception as e:
                    self.issues.append(f"❌ Cannot create {path}: {e}")
        
        return len(self.issues) == 0
    
    def check_provider_credentials(self) -> bool:
        """Check provider-specific credentials."""
        logger.info("🔍 Checking provider credentials...")
        
        provider = config.storage_provider
        
        if provider == "google":
            if not config.google_drive_folder_id:
                self.issues.append("❌ Google Drive folder ID not configured")
            else:
                self.successes.append("✅ Google Drive folder ID configured")
                
        elif provider == "dropbox":
            if not config.dropbox_root_path:
                self.issues.append("❌ Dropbox root path not configured")
            else:
                self.successes.append("✅ Dropbox root path configured")
                
        elif provider == "s3":
            if not config.s3_bucket:
                self.issues.append("❌ S3 bucket not configured")
            else:
                self.successes.append("✅ S3 bucket configured")
                
        elif provider == "local":
            self.successes.append("✅ Local storage (no credentials needed)")
        
        return len(self.issues) == 0
    
    def check_dependencies(self) -> bool:
        """Check that required Python packages are available."""
        logger.info("🔍 Checking Python dependencies...")
        
        required_packages = [
            "fastapi",
            "uvicorn",
            "pydantic",
            "loguru",
            "pathlib"
        ]
        
        for package in required_packages:
            try:
                __import__(package)
                self.successes.append(f"✅ {package} available")
            except ImportError:
                self.issues.append(f"❌ {package} not available")
        
        # Check optional provider packages
        provider_packages = {
            "google": ["google.auth", "googleapiclient"],
            "dropbox": ["dropbox"],
            "s3": ["boto3"]
        }
        
        provider = config.storage_provider
        if provider in provider_packages:
            for package in provider_packages[provider]:
                try:
                    __import__(package)
                    self.successes.append(f"✅ {package} available for {provider}")
                except ImportError:
                    self.warnings.append(f"⚠️  {package} not available for {provider}")
        
        return len(self.issues) == 0
    
    def check_backup_status(self) -> bool:
        """Check current backup status."""
        logger.info("🔍 Checking backup status...")
        
        from utils.backup_rotation import BackupRotator
        
        rotator = BackupRotator(dry_run=True)
        summary = rotator.get_backup_summary()
        
        self.successes.append(f"✅ Backup directory: {summary['backup_dir']}")
        self.successes.append(f"✅ Archive directory: {summary['archive_dir']}")
        self.successes.append(f"✅ Current backups: {summary['current_backups']}")
        self.successes.append(f"✅ Archive files: {summary['archive_files']}")
        self.successes.append(f"✅ Total size: {summary['total_size_gb']} GB")
        
        return True
    
    def run_all_checks(self) -> Dict[str, any]:
        """Run all health checks and return results."""
        logger.info("🚀 Starting comprehensive system health check...")
        
        checks = [
            ("Environment", self.check_environment),
            ("Paths", self.check_paths),
            ("Provider Credentials", self.check_provider_credentials),
            ("Dependencies", self.check_dependencies),
            ("Backup Status", self.check_backup_status)
        ]
        
        results = {}
        for check_name, check_func in checks:
            try:
                results[check_name] = check_func()
            except Exception as e:
                logger.error(f"Error in {check_name} check: {e}")
                self.issues.append(f"❌ {check_name} check failed: {e}")
                results[check_name] = False
        
        return results
    
    def generate_report(self) -> str:
        """Generate a Markdown health report."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        report = f"""# PaulyOps System Health Report

**Generated**: {timestamp}  
**Environment**: {config.env}  
**Storage Provider**: {config.storage_provider}

## Summary

- ✅ **Successes**: {len(self.successes)}
- ⚠️  **Warnings**: {len(self.warnings)}
- ❌ **Issues**: {len(self.issues)}

## Configuration

```
Environment: {config.env}
Log Level: {config.log_level}
Storage Provider: {config.storage_provider}
Company: {config.company_name}
Backup Directory: {config.backup_dir}
Archive Directory: {config.archive_dir}
Ingest Folder: {config.ingest_folder_name}
```

## Results

### ✅ Successes
"""
        
        for success in self.successes:
            report += f"- {success}\n"
        
        if self.warnings:
            report += "\n### ⚠️  Warnings\n"
            for warning in self.warnings:
                report += f"- {warning}\n"
        
        if self.issues:
            report += "\n### ❌ Issues\n"
            for issue in self.issues:
                report += f"- {issue}\n"
        
        report += "\n## Recommendations\n"
        
        if self.issues:
            report += "**Critical**: Fix all issues before proceeding with operations.\n\n"
        elif self.warnings:
            report += "**Warning**: Address warnings for optimal operation.\n\n"
        else:
            report += "**Success**: System is healthy and ready for operations.\n\n"
        
        return report
    
    def save_report(self, report: str):
        """Save the health report to file."""
        reports_dir = Path("reports")
        reports_dir.mkdir(exist_ok=True)
        
        report_file = reports_dir / "system_health.md"
        with open(report_file, "w") as f:
            f.write(report)
        
        logger.info(f"📄 Health report saved to {report_file}")


def main():
    """Main health check function."""
    checker = SystemHealthChecker()
    
    # Run all checks
    results = checker.run_all_checks()
    
    # Generate and save report
    report = checker.generate_report()
    checker.save_report(report)
    
    # Print summary to console
    print("\n" + "=" * 60)
    print("PAULYOPS SYSTEM HEALTH CHECK")
    print("=" * 60)
    
    print(f"✅ Successes: {len(checker.successes)}")
    print(f"⚠️  Warnings: {len(checker.warnings)}")
    print(f"❌ Issues: {len(checker.issues)}")
    
    if checker.issues:
        print("\n❌ CRITICAL ISSUES FOUND:")
        for issue in checker.issues:
            print(f"  - {issue}")
        sys.exit(1)
    elif checker.warnings:
        print("\n⚠️  WARNINGS (system will work but may have issues):")
        for warning in checker.warnings:
            print(f"  - {warning}")
    else:
        print("\n🎉 SYSTEM IS HEALTHY!")
    
    print(f"\n📄 Full report saved to: reports/system_health.md")


if __name__ == "__main__":
    main()

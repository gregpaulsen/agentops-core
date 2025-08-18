#!/usr/bin/env python3
"""Enhanced System Health Checker for PaulyOps with Nightly Email Audit."""

import os
import sys
import time
import json
import smtplib
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Add the project root to the path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

try:
    from config.loader import config
    from utils.logging import logger
except ImportError:
    # Fallback if imports fail
    class Config:
        def __init__(self):
            self.env = os.getenv("ENV", "development")
            self.log_level = os.getenv("LOG_LEVEL", "INFO")
            self.storage_provider = os.getenv("STORAGE_PROVIDER", "local")
            self.company_name = os.getenv("COMPANY_NAME", "BigSky")
            self.backup_dir = Path.home() / "Desktop" / "Backups"
            self.archive_dir = Path.home() / "Desktop" / "Archives"
            self.ingest_folder_name = "BigSkyAgDropzone"
    
    config = Config()
    
    class Logger:
        def info(self, msg): print(f"INFO: {msg}")
        def error(self, msg): print(f"ERROR: {msg}")
        def warning(self, msg): print(f"WARNING: {msg}")
    
    logger = Logger()


class EnhancedSystemHealthChecker:
    """Comprehensive system health checker with nightly email audit."""
    
    def __init__(self):
        self.issues = []
        self.warnings = []
        self.successes = []
        self.home = Path.home()
        self.desktop = self.home / "Desktop"
        self.paulyops_root = self.home / "PaulyOps"
        self.reports_dir = self.paulyops_root / "Reports"
        self.backup_dir = self.paulyops_root / "Backups"
        self.archive_dir = self.backup_dir / "archive"
        
        # Ensure directories exist
        self.reports_dir.mkdir(exist_ok=True)
        self.backup_dir.mkdir(exist_ok=True)
        self.archive_dir.mkdir(exist_ok=True)
    
    def add_check(self, name: str, passed: bool, message: str):
        """Add a check result."""
        if passed:
            self.successes.append(f"✅ {name}: {message}")
        else:
            self.issues.append(f"❌ {name}: {message}")
    
    def add_warning(self, name: str, message: str):
        """Add a warning."""
        self.warnings.append(f"⚠️  {name}: {message}")
    
    def check_dropzone(self) -> bool:
        """Check dropzone status."""
        logger.info("🔍 Checking dropzone...")
        
        # Check for PaulyOpsDropzone first, then BigSkyAgDropzone
        dropzone = self.desktop / "PaulyOpsDropzone"
        if not dropzone.exists():
            dropzone = self.desktop / "BigSkyAgDropzone"
            if not dropzone.exists():
                self.add_warning("Dropzone", "No dropzone directory found")
                return True
        
        # Check for recent files
        recent_files = list(dropzone.glob("*"))
        if not recent_files:
            self.add_warning("BigSkyAgDropzone", "No files found in dropzone")
        else:
            latest_file = max(recent_files, key=lambda f: f.stat().st_mtime if f.is_file() else 0)
            age_hours = (time.time() - latest_file.stat().st_mtime) / 3600
            self.add_check("BigSkyAgDropzone", True, f"Found {len(recent_files)} files, latest: {latest_file.name} ({age_hours:.1f}h ago)")
        
        return True
    
    def check_backups(self) -> bool:
        """Check backup status and rotation."""
        logger.info("🔍 Checking backup status...")
        
        # Check backup directory
        if not self.backup_dir.exists():
            self.add_check("Backup Directory", False, "Backup directory not found")
            return False
        
        # Check backup files (exclude archive directory)
        backup_files = [f for f in self.backup_dir.glob("*.zip") if f.parent == self.backup_dir]
        if not backup_files:
            self.add_warning("Backup Files", "No backup files found")
        else:
            latest_backup = max(backup_files, key=lambda f: f.stat().st_mtime)
            backup_age_hours = (time.time() - latest_backup.stat().st_mtime) / 3600
            backup_size_mb = latest_backup.stat().st_size / (1024 * 1024)
            
            self.add_check("Backup Files", True, 
                          f"Found {len(backup_files)} active backup(s), latest: {latest_backup.name} "
                          f"({backup_age_hours:.1f}h ago, {backup_size_mb:.1f}MB)")
        
        # Check archive directory
        if self.archive_dir.exists():
            archive_files = list(self.archive_dir.glob("*.zip"))
            self.add_check("Archive Directory", True, f"Found {len(archive_files)} archived backups")
        else:
            self.add_warning("Archive Directory", "Archive directory not found")
        
        return True
    
    def check_logs(self) -> bool:
        """Check log files and rotation."""
        logger.info("🔍 Checking log files...")
        
        logs_dir = Path("logs")
        if not logs_dir.exists():
            self.add_warning("Logs Directory", "Logs directory not found")
            return True
        
        log_files = list(logs_dir.glob("*.log"))
        if not log_files:
            self.add_warning("Log Files", "No log files found")
        else:
            latest_log = max(log_files, key=lambda f: f.stat().st_mtime)
            log_age_hours = (time.time() - latest_log.stat().st_mtime) / 3600
            log_size_mb = latest_log.stat().st_size / (1024 * 1024)
            
            self.add_check("Log Files", True, 
                          f"Found {len(log_files)} logs, latest: {latest_log.name} "
                          f"({log_age_hours:.1f}h ago, {log_size_mb:.1f}MB)")
        
        return True
    
    def check_launchd_jobs(self) -> bool:
        """Check launchd job status."""
        logger.info("🔍 Checking launchd jobs...")
        
        launch_agents = Path.home() / "Library" / "LaunchAgents"
        if not launch_agents.exists():
            self.add_warning("LaunchAgents", "LaunchAgents directory not found")
            return True
        
        # Check for BigSky/PaulyOps related jobs
        bigsky_jobs = list(launch_agents.glob("com.bigsky.*.plist"))
        paulyops_jobs = list(launch_agents.glob("com.paulyops.*.plist"))
        
        all_jobs = bigsky_jobs + paulyops_jobs
        
        if not all_jobs:
            self.add_warning("Launchd Jobs", "No BigSky/PaulyOps launchd jobs found")
        else:
            for job in all_jobs:
                # Check if job is loaded
                try:
                    result = subprocess.run(["launchctl", "list", job.stem], 
                                          capture_output=True, text=True)
                    if result.returncode == 0:
                        self.add_check(f"Launchd Job: {job.stem}", True, "Job is loaded and running")
                    else:
                        self.add_warning(f"Launchd Job: {job.stem}", "Job exists but not loaded")
                except Exception as e:
                    self.add_warning(f"Launchd Job: {job.stem}", f"Error checking job: {e}")
        
        return True
    
    def check_provider_credentials(self) -> bool:
        """Check storage provider credentials."""
        logger.info("🔍 Checking provider credentials...")
        
        # Check for credential files
        cred_paths = [
            Path.home() / ".config" / "bigsky" / "credentials.json",
            Path.home() / ".bigsky" / "credentials.json",
            Path("auth") / "credentials.json"
        ]
        
        cred_found = False
        for cred_path in cred_paths:
            if cred_path.exists():
                self.add_check("Provider Credentials", True, f"Found credentials at {cred_path}")
                cred_found = True
                break
        
        if not cred_found:
            self.add_warning("Provider Credentials", "No credential files found")
        
        return True
    
    def check_router_logs(self) -> bool:
        """Check router logs and success markers."""
        logger.info("🔍 Checking router logs...")
        
        # Check for router logs in various locations
        router_log_paths = [
            Path("logs") / "router.log",
            Path("bigsky-agent") / "05_Automation" / "Scripts" / "router.log",
            Path("98_Tests") / "router_log.txt"
        ]
        
        router_found = False
        for log_path in router_log_paths:
            if log_path.exists():
                log_size = log_path.stat().st_size
                log_age_hours = (time.time() - log_path.stat().st_mtime) / 3600
                
                self.add_check("Router Logs", True, 
                              f"Found router log: {log_path} ({log_size} bytes, {log_age_hours:.1f}h ago)")
                router_found = True
                break
        
        if not router_found:
            self.add_warning("Router Logs", "No router logs found")
        
        return True
    
    def check_git_repo_health(self) -> bool:
        """Check Git repository health."""
        logger.info("🔍 Checking Git repository health...")
        
        # Check if we're in a Git repository
        current_dir = Path.cwd()
        git_dir = current_dir / ".git"
        
        logger.info(f"Current directory: {current_dir}")
        logger.info(f"Looking for .git at: {git_dir}")
        logger.info(f".git exists: {git_dir.exists()}")
        
        if not git_dir.exists():
            # Try to find a Git repository in parent directories
            parent = current_dir.parent
            while parent != parent.parent:  # Stop at root
                if (parent / ".git").exists():
                    self.add_check("Git Repository", True, f"Found in parent directory: {parent.name}")
                    return True
                parent = parent.parent
            
            self.add_warning("Git Repository", "Not in a Git repository")
            return True
        
        try:
            # Check for uncommitted changes
            result = subprocess.run(["git", "status", "--porcelain"], 
                                  capture_output=True, text=True)
            if result.stdout.strip():
                self.add_warning("Git Status", f"Uncommitted changes: {len(result.stdout.strip().split())} files")
            else:
                self.add_check("Git Status", True, "Working directory clean")
            
            # Check last commit
            result = subprocess.run(["git", "log", "-1", "--format=%H %s %cr"], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                commit_info = result.stdout.strip()
                self.add_check("Git Commits", True, f"Last commit: {commit_info}")
            else:
                self.add_warning("Git Commits", "No commits found")
            
            # Check remote status
            result = subprocess.run(["git", "remote", "-v"], 
                                  capture_output=True, text=True)
            if result.returncode == 0 and result.stdout.strip():
                self.add_check("Git Remote", True, "Remote configured")
            else:
                self.add_warning("Git Remote", "No remote configured")
                
        except Exception as e:
            self.add_warning("Git Health", f"Error checking Git: {e}")
        
        return True
    
    def check_endpoints(self) -> bool:
        """Check API endpoints."""
        logger.info("🔍 Checking API endpoints...")
        
        # Check if API server is running
        try:
            result = subprocess.run(["curl", "-s", "http://localhost:8000/health"], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                self.add_check("API Endpoint", True, "API server responding on port 8000")
            else:
                self.add_warning("API Endpoint", "API server not responding on port 8000")
        except Exception:
            self.add_warning("API Endpoint", "API server not running or not accessible")
        
        return True
    
    def check_spotlight(self) -> bool:
        """Check Spotlight indexing."""
        logger.info("🔍 Checking Spotlight indexing...")
        
        try:
            result = subprocess.run(["mdutil", "-as"], capture_output=True, text=True)
            if result.returncode == 0:
                if "Indexing enabled" in result.stdout:
                    self.add_check("Spotlight", True, "Spotlight indexing enabled")
                else:
                    self.add_warning("Spotlight", "Spotlight indexing disabled")
            else:
                self.add_warning("Spotlight", "Could not check Spotlight status")
        except Exception as e:
            self.add_warning("Spotlight", f"Error checking Spotlight: {e}")
        
        return True
    
    def check_nightly_email_sent(self) -> bool:
        """Check if nightly email was sent recently."""
        logger.info("🔍 Checking nightly email status...")
        
        nightly_marker = self.reports_dir / ".nightly_last_sent"
        
        if nightly_marker.exists():
            marker_age_hours = (time.time() - nightly_marker.stat().st_mtime) / 3600
            
            if marker_age_hours <= 26:  # Within 26 hours
                self.add_check("Nightly Email Sent", True, 
                              f"Last sent {marker_age_hours:.1f} hours ago")
                return True
            else:
                self.add_check("Nightly Email Sent", False, 
                              f"Last sent {marker_age_hours:.1f} hours ago (too old)")
                return False
        else:
            self.add_check("Nightly Email Sent", False, "No send marker found")
            return False
    
    def run_all_checks(self) -> Dict[str, bool]:
        """Run all health checks and return results."""
        logger.info("🚀 Starting comprehensive system health check...")
        
        checks = [
            ("DropZone", self.check_dropzone),
            ("Backups", self.check_backups),
            ("Logs", self.check_logs),
            ("Launchd Jobs", self.check_launchd_jobs),
            ("Provider Credentials", self.check_provider_credentials),
            ("Router Logs", self.check_router_logs),
            ("Git Repository", self.check_git_repo_health),
            ("API Endpoints", self.check_endpoints),
            ("Spotlight", self.check_spotlight),
            ("Nightly Email", self.check_nightly_email_sent)
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
        """Generate a comprehensive Markdown health report."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        report = f"""# PaulyOps Enhanced System Health Report

**Generated**: {timestamp}  
**Environment**: {config.env}  
**Storage Provider**: {config.storage_provider}

## Summary

- ✅ **Successes**: {len(self.successes)}
- ⚠️  **Warnings**: {len(self.warnings)}
- ❌ **Issues**: {len(self.issues)}

## System Status

| Component | Status | Details |
|-----------|--------|---------|
"""
        
        # Add all check results to the table
        for success in self.successes:
            if success.startswith("✅"):
                parts = success.split(": ", 1)
                component = parts[0].replace("✅ ", "")
                details = parts[1] if len(parts) > 1 else "OK"
                report += f"| {component} | ✅ PASS | {details} |\n"
        
        for warning in self.warnings:
            if warning.startswith("⚠️"):
                parts = warning.split(": ", 1)
                component = parts[0].replace("⚠️ ", "")
                details = parts[1] if len(parts) > 1 else "Warning"
                report += f"| {component} | ⚠️ WARN | {details} |\n"
        
        for issue in self.issues:
            if issue.startswith("❌"):
                parts = issue.split(": ", 1)
                component = parts[0].replace("❌ ", "")
                details = parts[1] if len(parts) > 1 else "Failed"
                report += f"| {component} | ❌ FAIL | {details} |\n"
        
        report += "\n## Detailed Results\n\n"
        
        if self.successes:
            report += "### ✅ Successes\n"
            for success in self.successes:
                report += f"- {success}\n"
            report += "\n"
        
        if self.warnings:
            report += "### ⚠️  Warnings\n"
            for warning in self.warnings:
                report += f"- {warning}\n"
            report += "\n"
        
        if self.issues:
            report += "### ❌ Issues\n"
            for issue in self.issues:
                report += f"- {issue}\n"
            report += "\n"
        
        report += "## Recommendations\n"
        
        if self.issues:
            report += "**Critical**: Fix all issues before proceeding with operations.\n\n"
        elif self.warnings:
            report += "**Warning**: Address warnings for optimal operation.\n\n"
        else:
            report += "**Success**: System is healthy and ready for operations.\n\n"
        
        return report
    
    def save_report(self, report: str):
        """Save the health report to file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = self.reports_dir / f"system_health_{timestamp}.md"
        
        with open(report_file, "w") as f:
            f.write(report)
        
        logger.info(f"📄 Health report saved to {report_file}")
        return report_file


def main():
    """Main health check function."""
    checker = EnhancedSystemHealthChecker()
    
    # Run all checks
    results = checker.run_all_checks()
    
    # Generate and save report
    report = checker.generate_report()
    report_file = checker.save_report(report)
    
    # Print summary to console
    print("\n" + "=" * 60)
    print("PAULYOPS ENHANCED SYSTEM HEALTH CHECK")
    print("=" * 60)
    
    print(f"✅ Successes: {len(checker.successes)}")
    print(f"⚠️  Warnings: {len(checker.warnings)}")
    print(f"❌ Issues: {len(checker.issues)}")
    
    if checker.issues:
        print("\n❌ CRITICAL ISSUES FOUND:")
        for issue in checker.issues:
            print(f"  - {issue}")
        print("\n🔧 FIX PLAN:")
        print("  1. Address all critical issues above")
        print("  2. Run system health check again")
        print("  3. Verify all components are working")
        sys.exit(1)
    elif checker.warnings:
        print("\n⚠️  WARNINGS (system will work but may have issues):")
        for warning in checker.warnings:
            print(f"  - {warning}")
    else:
        print("\n🎉 SYSTEM IS HEALTHY!")
    
    print(f"\n📄 Full report saved to: {report_file}")
    print("📧 Nightly email system ready for 10pm delivery")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Comprehensive system function check for PaulyOps."""

import json
import shutil
import tempfile
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

from config.loader import config
from utils.logging import logger
from utils.backup_rotation import BackupRotator
from dashboards.update import update_summary, create_status_report


class SystemFunctionChecker:
    """Comprehensive system function checker for PaulyOps."""
    
    def __init__(self):
        self.results = {}
        self.start_time = time.time()
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def run_health_check(self) -> bool:
        """Run system health check."""
        logger.info("🔍 Running system health check...")
        
        try:
            from system_health import SystemHealthChecker
            checker = SystemHealthChecker()
            health_results = checker.run_all_checks()
            
            self.results["health_check"] = {
                "success": all(health_results.values()),
                "details": health_results,
                "issues": len(checker.issues),
                "warnings": len(checker.warnings)
            }
            
            if checker.issues:
                logger.error(f"❌ Health check found {len(checker.issues)} issues")
                return False
            else:
                logger.info("✅ Health check passed")
                return True
                
        except Exception as e:
            logger.error(f"❌ Health check failed: {e}")
            self.results["health_check"] = {"success": False, "error": str(e)}
            return False
    
    def run_sample_ingest_dry_run(self) -> bool:
        """Run sample ingest in dry-run mode."""
        logger.info("🔍 Running sample ingest dry-run...")
        
        try:
            # Create temporary ingest directory
            temp_dir = Path(tempfile.mkdtemp())
            ingest_dir = temp_dir / config.ingest_folder_name
            ingest_dir.mkdir()
            
            # Copy sample files
            fixture_dir = Path("tests/fixtures/sample_ingest")
            sample_files = ["sample_document.txt", "sample_data.json", "sample_config.yaml"]
            
            copied_files = []
            for filename in sample_files:
                source = fixture_dir / filename
                if source.exists():
                    dest = ingest_dir / filename
                    shutil.copy2(source, dest)
                    copied_files.append(dest)
            
            # Simulate routing (dry-run)
            routed_files = []
            for file_path in copied_files:
                # In dry-run, we just log what would happen
                logger.info(f"ℹ️  [DRY-RUN] Would route {file_path.name} to storage")
                routed_files.append(str(file_path))
            
            self.results["sample_ingest_dry_run"] = {
                "success": True,
                "files_processed": len(copied_files),
                "routed_files": routed_files
            }
            
            # Cleanup
            shutil.rmtree(temp_dir)
            
            logger.info(f"✅ Sample ingest dry-run completed: {len(copied_files)} files")
            return True
            
        except Exception as e:
            logger.error(f"❌ Sample ingest dry-run failed: {e}")
            self.results["sample_ingest_dry_run"] = {"success": False, "error": str(e)}
            return False
    
    def run_sample_ingest_real(self) -> bool:
        """Run sample ingest in real mode."""
        logger.info("🔍 Running sample ingest (real mode)...")
        
        try:
            # Create temporary ingest directory
            temp_dir = Path(tempfile.mkdtemp())
            ingest_dir = temp_dir / config.ingest_folder_name
            ingest_dir.mkdir()
            
            # Copy sample files
            fixture_dir = Path("tests/fixtures/sample_ingest")
            sample_files = ["sample_document.txt", "sample_data.json", "sample_config.yaml"]
            
            copied_files = []
            for filename in sample_files:
                source = fixture_dir / filename
                if source.exists():
                    dest = ingest_dir / filename
                    shutil.copy2(source, dest)
                    copied_files.append(dest)
            
            # Simulate routing (real mode - just move to backup dir for now)
            routed_files = []
            for file_path in copied_files:
                # Move to backup directory as a simple routing simulation
                backup_dest = config.backup_dir / file_path.name
                shutil.move(str(file_path), str(backup_dest))
                routed_files.append(str(backup_dest))
                logger.info(f"✅ Routed {file_path.name} to {backup_dest}")
            
            self.results["sample_ingest_real"] = {
                "success": True,
                "files_processed": len(copied_files),
                "routed_files": routed_files
            }
            
            # Cleanup temp directory
            shutil.rmtree(temp_dir)
            
            logger.info(f"✅ Sample ingest completed: {len(copied_files)} files")
            return True
            
        except Exception as e:
            logger.error(f"❌ Sample ingest failed: {e}")
            self.results["sample_ingest_real"] = {"success": False, "error": str(e)}
            return False
    
    def run_rotation_test(self) -> bool:
        """Test backup rotation functionality."""
        logger.info("🔍 Running backup rotation test...")
        
        try:
            rotator = BackupRotator(dry_run=True)
            
            # Create a dummy backup file for testing
            dummy_backup = config.backup_dir / f"test_backup_{self.timestamp}.zip"
            dummy_backup.write_text("test backup content")
            
            # Test rotation
            moved_files = rotator.rotate_backups(dummy_backup)
            
            # Cleanup
            if dummy_backup.exists():
                dummy_backup.unlink()
            
            self.results["rotation_test"] = {
                "success": True,
                "files_moved": len(moved_files),
                "backup_created": True
            }
            
            logger.info("✅ Backup rotation test completed")
            return True
            
        except Exception as e:
            logger.error(f"❌ Backup rotation test failed: {e}")
            self.results["rotation_test"] = {"success": False, "error": str(e)}
            return False
    
    def run_dashboard_update_test(self) -> bool:
        """Test dashboard update functionality."""
        logger.info("🔍 Running dashboard update test...")
        
        try:
            # Create a test status report
            test_results = {
                "operation": "system_function_check",
                "files_processed": 3,
                "backups_rotated": 1,
                "status": "success"
            }
            
            status_report_path = create_status_report("test_operation", test_results)
            
            # Update dashboard
            dashboard_result = update_summary(status_report_path)
            
            self.results["dashboard_update_test"] = {
                "success": "error" not in dashboard_result,
                "status_report_created": status_report_path,
                "dashboard_updated": dashboard_result
            }
            
            logger.info("✅ Dashboard update test completed")
            return True
            
        except Exception as e:
            logger.error(f"❌ Dashboard update test failed: {e}")
            self.results["dashboard_update_test"] = {"success": False, "error": str(e)}
            return False
    
    def run_all_checks(self) -> Dict[str, Any]:
        """Run all system function checks."""
        logger.info("🚀 Starting comprehensive system function check...")
        
        checks = [
            ("Health Check", self.run_health_check),
            ("Sample Ingest Dry-Run", self.run_sample_ingest_dry_run),
            ("Sample Ingest Real", self.run_sample_ingest_real),
            ("Rotation Test", self.run_rotation_test),
            ("Dashboard Update Test", self.run_dashboard_update_test)
        ]
        
        for check_name, check_func in checks:
            try:
                start_time = time.time()
                success = check_func()
                duration = time.time() - start_time
                
                if check_name not in self.results:
                    self.results[check_name] = {"success": success, "duration": duration}
                else:
                    self.results[check_name]["duration"] = duration
                    
            except Exception as e:
                logger.error(f"Error in {check_name}: {e}")
                self.results[check_name] = {"success": False, "error": str(e)}
        
        return self.results
    
    def generate_report(self) -> str:
        """Generate a comprehensive Markdown report."""
        total_duration = time.time() - self.start_time
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Count successes and failures
        successes = sum(1 for result in self.results.values() if result.get("success", False))
        failures = len(self.results) - successes
        
        report = f"""# PaulyOps System Function Check Report

**Generated**: {timestamp}  
**Duration**: {total_duration:.2f} seconds  
**Environment**: {config.env}  
**Storage Provider**: {config.storage_provider}

## Summary

- ✅ **Successful Checks**: {successes}
- ❌ **Failed Checks**: {failures}
- 📊 **Total Checks**: {len(self.results)}

## Check Results

"""
        
        for check_name, result in self.results.items():
            status = "✅ PASS" if result.get("success", False) else "❌ FAIL"
            duration = result.get("duration", 0)
            
            report += f"### {check_name}\n"
            report += f"**Status**: {status}\n"
            report += f"**Duration**: {duration:.2f}s\n"
            
            if "error" in result:
                report += f"**Error**: {result['error']}\n"
            
            if "details" in result:
                report += f"**Details**: {json.dumps(result['details'], indent=2)}\n"
            
            report += "\n"
        
        report += "## Configuration\n\n"
        report += f"```\n"
        report += f"Environment: {config.env}\n"
        report += f"Storage Provider: {config.storage_provider}\n"
        report += f"Backup Directory: {config.backup_dir}\n"
        report += f"Archive Directory: {config.archive_dir}\n"
        report += f"Ingest Folder: {config.ingest_folder_name}\n"
        report += f"```\n\n"
        
        report += "## Recommendations\n\n"
        
        if failures > 0:
            report += "**Critical**: Fix failed checks before proceeding with operations.\n\n"
        else:
            report += "**Success**: All system functions are working correctly.\n\n"
        
        report += "## Next Steps\n\n"
        report += "1. Review any failed checks\n"
        report += "2. Verify configuration settings\n"
        report += "3. Test with actual data if all checks pass\n"
        report += "4. Proceed with UI development\n"
        
        return report
    
    def save_report(self, report: str):
        """Save the function check report to file."""
        reports_dir = Path("reports")
        reports_dir.mkdir(exist_ok=True)
        
        report_file = reports_dir / f"system_check_{self.timestamp}.md"
        with open(report_file, "w") as f:
            f.write(report)
        
        logger.info(f"📄 Function check report saved to {report_file}")
        return str(report_file)


def main():
    """Main system function check."""
    checker = SystemFunctionChecker()
    
    # Run all checks
    results = checker.run_all_checks()
    
    # Generate and save report
    report = checker.generate_report()
    report_file = checker.save_report(report)
    
    # Print summary to console
    print("\n" + "=" * 60)
    print("PAULYOPS SYSTEM FUNCTION CHECK")
    print("=" * 60)
    
    successes = sum(1 for result in results.values() if result.get("success", False))
    failures = len(results) - successes
    
    print(f"✅ Successful Checks: {successes}")
    print(f"❌ Failed Checks: {failures}")
    print(f"📊 Total Checks: {len(results)}")
    print(f"⏱️  Total Duration: {time.time() - checker.start_time:.2f}s")
    
    if failures > 0:
        print("\n❌ SOME CHECKS FAILED:")
        for check_name, result in results.items():
            if not result.get("success", False):
                print(f"  - {check_name}: {result.get('error', 'Unknown error')}")
        print("\n📄 Full report saved to:", report_file)
        return 1
    else:
        print("\n🎉 ALL CHECKS PASSED!")
        print("\n📄 Full report saved to:", report_file)
        return 0


if __name__ == "__main__":
    exit(main())

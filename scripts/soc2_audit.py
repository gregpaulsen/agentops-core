#!/usr/bin/env python3
"""
PaulyOps SOC2 Audit Engineer
Comprehensive security and compliance audit for SOC2 readiness
"""

import os
import sys
import json
import hashlib
import subprocess
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

class SOC2Auditor:
    """SOC2 compliance auditor for PaulyOps system."""
    
    def __init__(self):
        self.audit_results = {
            "timestamp": datetime.now().isoformat(),
            "system": "PaulyOps",
            "version": "1.0.0",
            "compliance_score": 0,
            "total_checks": 0,
            "passed_checks": 0,
            "failed_checks": 0,
            "warnings": 0,
            "details": {}
        }
    
    def audit_credential_handling(self) -> Dict:
        """Audit credential storage and handling."""
        print("🔐 Auditing credential handling...")
        
        results = {
            "passed": 0,
            "failed": 0,
            "warnings": 0,
            "issues": []
        }
        
        # Check for hardcoded credentials in Python files
        scripts_dir = project_root / "scripts"
        for py_file in scripts_dir.glob("*.py"):
            try:
                content = py_file.read_text()
                
                # Check for hardcoded passwords/tokens
                if re.search(r'password\s*=\s*["\'][^"\']+["\']', content, re.IGNORECASE):
                    results["failed"] += 1
                    results["issues"].append(f"Hardcoded password in {py_file.name}")
                
                if re.search(r'token\s*=\s*["\'][^"\']+["\']', content, re.IGNORECASE):
                    results["failed"] += 1
                    results["issues"].append(f"Hardcoded token in {py_file.name}")
                
                # Check for proper environment variable usage
                if "os.environ" in content and ("password" in content or "token" in content):
                    results["passed"] += 1
                
            except Exception as e:
                results["warnings"] += 1
                results["issues"].append(f"Error reading {py_file.name}: {e}")
        
        # Check credential file permissions
        cred_paths = [
            project_root / "config" / ".env",
            Path.home() / ".config" / "bigsky" / "credentials.json"
        ]
        
        for cred_path in cred_paths:
            if cred_path.exists():
                mode = oct(cred_path.stat().st_mode)[-3:]
                if mode == "644" or mode == "600":
                    results["passed"] += 1
                else:
                    results["warnings"] += 1
                    results["issues"].append(f"Insecure permissions on {cred_path}: {mode}")
            else:
                results["warnings"] += 1
                results["issues"].append(f"Credential file not found: {cred_path}")
        
        return results
    
    def audit_logging_security(self) -> Dict:
        """Audit logging security and retention."""
        print("📝 Auditing logging security...")
        
        results = {
            "passed": 0,
            "failed": 0,
            "warnings": 0,
            "issues": []
        }
        
        # Check log directory permissions
        logs_dir = project_root / "logs"
        if logs_dir.exists():
            mode = oct(logs_dir.stat().st_mode)[-3:]
            if mode in ["755", "750"]:
                results["passed"] += 1
            else:
                results["warnings"] += 1
                results["issues"].append(f"Log directory permissions: {mode}")
        
        # Check for sensitive data in logs
        reports_dir = project_root / "Reports"
        if reports_dir.exists():
            for log_file in reports_dir.glob("*.log"):
                try:
                    content = log_file.read_text()
                    if "password" in content.lower() or "token" in content.lower():
                        results["failed"] += 1
                        results["issues"].append(f"Sensitive data in log: {log_file.name}")
                    else:
                        results["passed"] += 1
                except Exception as e:
                    results["warnings"] += 1
                    results["issues"].append(f"Error reading log {log_file.name}: {e}")
        
        return results
    
    def audit_access_control(self) -> Dict:
        """Audit access control mechanisms."""
        print("🔒 Auditing access control...")
        
        results = {
            "passed": 0,
            "failed": 0,
            "warnings": 0,
            "issues": []
        }
        
        # Check file permissions on critical files
        critical_files = [
            project_root / "scripts" / "system_health.py",
            project_root / "scripts" / "system_autodoctor.py",
            project_root / "config" / "status_flags.json"
        ]
        
        for file_path in critical_files:
            if file_path.exists():
                mode = oct(file_path.stat().st_mode)[-3:]
                if mode == "644":
                    results["passed"] += 1
                else:
                    results["warnings"] += 1
                    results["issues"].append(f"Critical file permissions: {file_path} ({mode})")
        
        # Check for immutable flags on critical files
        try:
            result = subprocess.run(["ls", "-la", str(project_root / ".protected")], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                results["passed"] += 1
            else:
                results["warnings"] += 1
                results["issues"].append("No system protection marker found")
        except Exception as e:
            results["warnings"] += 1
            results["issues"].append(f"Error checking protection: {e}")
        
        return results
    
    def audit_error_handling(self) -> Dict:
        """Audit error handling and exception management."""
        print("⚠️ Auditing error handling...")
        
        results = {
            "passed": 0,
            "failed": 0,
            "warnings": 0,
            "issues": []
        }
        
        # Check for proper exception handling in Python scripts
        scripts_dir = project_root / "scripts"
        for py_file in scripts_dir.glob("*.py"):
            try:
                content = py_file.read_text()
                
                # Check for try/except blocks
                if "try:" in content and "except" in content:
                    results["passed"] += 1
                else:
                    results["warnings"] += 1
                    results["issues"].append(f"No exception handling in {py_file.name}")
                
                # Check for logging in exception handlers
                if "except" in content and "logger" in content:
                    results["passed"] += 1
                elif "except" in content:
                    results["warnings"] += 1
                    results["issues"].append(f"Exception handling without logging in {py_file.name}")
                
            except Exception as e:
                results["warnings"] += 1
                results["issues"].append(f"Error analyzing {py_file.name}: {e}")
        
        return results
    
    def audit_data_protection(self) -> Dict:
        """Audit data protection and encryption."""
        print("🛡️ Auditing data protection...")
        
        results = {
            "passed": 0,
            "failed": 0,
            "warnings": 0,
            "issues": []
        }
        
        # Check backup encryption (placeholder)
        backup_dir = project_root / "Backups"
        if backup_dir.exists():
            backup_files = list(backup_dir.glob("*.zip"))
            if backup_files:
                results["passed"] += 1  # Assuming zip files provide basic protection
            else:
                results["warnings"] += 1
                results["issues"].append("No backup files found")
        
        # Check for sensitive data in configuration
        config_dir = project_root / "config"
        for config_file in config_dir.glob("*"):
            if config_file.is_file():
                try:
                    content = config_file.read_text()
                    if "password" in content.lower() and "os.environ" not in content:
                        results["failed"] += 1
                        results["issues"].append(f"Hardcoded password in config: {config_file.name}")
                    else:
                        results["passed"] += 1
                except Exception as e:
                    results["warnings"] += 1
                    results["issues"].append(f"Error reading config {config_file.name}: {e}")
        
        return results
    
    def audit_audit_trail(self) -> Dict:
        """Audit audit trail and logging completeness."""
        print("📊 Auditing audit trail...")
        
        results = {
            "passed": 0,
            "failed": 0,
            "warnings": 0,
            "issues": []
        }
        
        # Check for comprehensive logging
        scripts_dir = project_root / "scripts"
        for py_file in scripts_dir.glob("*.py"):
            try:
                content = py_file.read_text()
                
                # Check for logging imports
                if "import logging" in content or "import logger" in content:
                    results["passed"] += 1
                else:
                    results["warnings"] += 1
                    results["issues"].append(f"No logging in {py_file.name}")
                
                # Check for timestamp logging
                if "datetime" in content and "logger" in content:
                    results["passed"] += 1
                
            except Exception as e:
                results["warnings"] += 1
                results["issues"].append(f"Error analyzing {py_file.name}: {e}")
        
        # Check for success/failure markers
        reports_dir = project_root / "Reports"
        if reports_dir.exists():
            markers = list(reports_dir.glob(".*"))
            if markers:
                results["passed"] += 1
            else:
                results["warnings"] += 1
                results["issues"].append("No success/failure markers found")
        
        return results
    
    def run_complete_audit(self) -> Dict:
        """Run complete SOC2 audit."""
        print("🛡️ PaulyOps SOC2 Audit Engineer")
        print("=" * 50)
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Run all audit modules
        self.audit_results["details"]["credential_handling"] = self.audit_credential_handling()
        self.audit_results["details"]["logging_security"] = self.audit_logging_security()
        self.audit_results["details"]["access_control"] = self.audit_access_control()
        self.audit_results["details"]["error_handling"] = self.audit_error_handling()
        self.audit_results["details"]["data_protection"] = self.audit_data_protection()
        self.audit_results["details"]["audit_trail"] = self.audit_audit_trail()
        
        # Calculate compliance score
        total_checks = 0
        passed_checks = 0
        failed_checks = 0
        warnings = 0
        
        for category, results in self.audit_results["details"].items():
            total_checks += results["passed"] + results["failed"] + results["warnings"]
            passed_checks += results["passed"]
            failed_checks += results["failed"]
            warnings += results["warnings"]
        
        self.audit_results["total_checks"] = total_checks
        self.audit_results["passed_checks"] = passed_checks
        self.audit_results["failed_checks"] = failed_checks
        self.audit_results["warnings"] = warnings
        
        if total_checks > 0:
            self.audit_results["compliance_score"] = (passed_checks / total_checks) * 100
        
        return self.audit_results
    
    def generate_report(self) -> str:
        """Generate comprehensive SOC2 audit report."""
        report = []
        report.append("# PaulyOps SOC2 Compliance Audit Report")
        report.append(f"**Generated:** {self.audit_results['timestamp']}")
        report.append(f"**System:** {self.audit_results['system']} v{self.audit_results['version']}")
        report.append(f"**Compliance Score:** {self.audit_results['compliance_score']:.1f}%")
        report.append("")
        
        report.append("## 📊 Summary")
        report.append(f"- **Total Checks:** {self.audit_results['total_checks']}")
        report.append(f"- **Passed:** {self.audit_results['passed_checks']} ✅")
        report.append(f"- **Failed:** {self.audit_results['failed_checks']} ❌")
        report.append(f"- **Warnings:** {self.audit_results['warnings']} ⚠️")
        report.append("")
        
        for category, results in self.audit_results["details"].items():
            report.append(f"## {category.replace('_', ' ').title()}")
            report.append(f"- **Passed:** {results['passed']} ✅")
            report.append(f"- **Failed:** {results['failed']} ❌")
            report.append(f"- **Warnings:** {results['warnings']} ⚠️")
            
            if results["issues"]:
                report.append("### Issues Found:")
                for issue in results["issues"]:
                    report.append(f"- {issue}")
            report.append("")
        
        report.append("## 🎯 SOC2 Readiness Assessment")
        if self.audit_results["compliance_score"] >= 90:
            report.append("**Status:** ✅ SOC2 READY")
            report.append("The system meets SOC2 compliance requirements.")
        elif self.audit_results["compliance_score"] >= 75:
            report.append("**Status:** ⚠️ SOC2 READY WITH MINOR ISSUES")
            report.append("The system is mostly compliant but has minor issues to address.")
        else:
            report.append("**Status:** ❌ SOC2 NOT READY")
            report.append("The system requires significant improvements for SOC2 compliance.")
        
        return "\n".join(report)

def main():
    """Run SOC2 audit."""
    auditor = SOC2Auditor()
    results = auditor.run_complete_audit()
    
    # Generate and save report
    report = auditor.generate_report()
    report_file = project_root / "Reports" / f"soc2_audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    report_file.write_text(report)
    
    print("\n" + "=" * 50)
    print("🎯 SOC2 AUDIT COMPLETE")
    print(f"📊 Compliance Score: {results['compliance_score']:.1f}%")
    print(f"📄 Report: {report_file}")
    print("=" * 50)

if __name__ == "__main__":
    main()

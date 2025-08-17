#!/usr/bin/env python3
"""
PaulyOps Code Hygiene & Refactor Engineer
Final pass to clean up code quality and modularity
"""

import os
import sys
import re
import ast
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

class CodeHygieneEngineer:
    """Code hygiene and refactoring engineer for PaulyOps."""
    
    def __init__(self):
        self.issues = {
            "dead_code": [],
            "logging_issues": [],
            "config_issues": [],
            "exception_issues": [],
            "hardcoded_paths": [],
            "unused_imports": []
        }
        self.fixes_applied = []
    
    def find_dead_code(self) -> List[str]:
        """Find dead code and unused functions."""
        print("🧹 Scanning for dead code...")
        
        dead_code = []
        scripts_dir = project_root / "scripts"
        
        for py_file in scripts_dir.glob("*.py"):
            try:
                content = py_file.read_text()
                
                # Check for functions that are never called
                tree = ast.parse(content)
                defined_functions = set()
                called_functions = set()
                
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        defined_functions.add(node.name)
                    elif isinstance(node, ast.Call):
                        if hasattr(node.func, 'id'):
                            called_functions.add(node.func.id)
                
                unused_functions = defined_functions - called_functions
                if unused_functions:
                    dead_code.append(f"{py_file.name}: {', '.join(unused_functions)}")
                
            except Exception as e:
                dead_code.append(f"Error parsing {py_file.name}: {e}")
        
        self.issues["dead_code"] = dead_code
        return dead_code
    
    def normalize_logging(self) -> List[str]:
        """Normalize logging across all scripts."""
        print("📝 Normalizing logging...")
        
        logging_issues = []
        scripts_dir = project_root / "scripts"
        
        for py_file in scripts_dir.glob("*.py"):
            try:
                content = py_file.read_text()
                
                # Check for inconsistent logging patterns
                if "print(" in content and "logger" not in content:
                    logging_issues.append(f"{py_file.name}: Uses print() instead of logger")
                
                if "logger" in content and "import logging" not in content:
                    logging_issues.append(f"{py_file.name}: Uses logger without importing logging")
                
                # Check for proper logging levels
                if "logger.info" in content and "logger.error" not in content:
                    logging_issues.append(f"{py_file.name}: Only uses info level, missing error logging")
                
            except Exception as e:
                logging_issues.append(f"Error analyzing {py_file.name}: {e}")
        
        self.issues["logging_issues"] = logging_issues
        return logging_issues
    
    def modularize_configs(self) -> List[str]:
        """Check for modular configuration patterns."""
        print("⚙️ Checking configuration modularity...")
        
        config_issues = []
        
        # Check for hardcoded values in scripts
        scripts_dir = project_root / "scripts"
        for py_file in scripts_dir.glob("*.py"):
            try:
                content = py_file.read_text()
                
                # Check for hardcoded paths
                hardcoded_paths = re.findall(r'["\'][/\\][^"\']*["\']', content)
                for path in hardcoded_paths:
                    if "Desktop" in path or "gregpaulsen" in path:
                        config_issues.append(f"{py_file.name}: Hardcoded path {path}")
                
                # Check for hardcoded configuration values
                if re.search(r'[A-Z_]+ = ["\'][^"\']+["\']', content):
                    config_issues.append(f"{py_file.name}: Hardcoded configuration values")
                
            except Exception as e:
                config_issues.append(f"Error analyzing {py_file.name}: {e}")
        
        self.issues["config_issues"] = config_issues
        return config_issues
    
    def validate_exception_handling(self) -> List[str]:
        """Validate exception handling coverage."""
        print("⚠️ Validating exception handling...")
        
        exception_issues = []
        scripts_dir = project_root / "scripts"
        
        for py_file in scripts_dir.glob("*.py"):
            try:
                content = py_file.read_text()
                
                # Check for missing exception handling
                if "subprocess" in content and "try:" not in content:
                    exception_issues.append(f"{py_file.name}: subprocess calls without exception handling")
                
                if "open(" in content and "try:" not in content:
                    exception_issues.append(f"{py_file.name}: file operations without exception handling")
                
                # Check for bare except clauses
                if re.search(r'except\s*:', content):
                    exception_issues.append(f"{py_file.name}: Bare except clause found")
                
                # Check for proper exception logging
                if "except" in content and "logger" not in content:
                    exception_issues.append(f"{py_file.name}: Exception handling without logging")
                
            except Exception as e:
                exception_issues.append(f"Error analyzing {py_file.name}: {e}")
        
        self.issues["exception_issues"] = exception_issues
        return exception_issues
    
    def find_hardcoded_paths(self) -> List[str]:
        """Find remaining hardcoded paths."""
        print("🛣️ Finding hardcoded paths...")
        
        hardcoded_paths = []
        scripts_dir = project_root / "scripts"
        
        for py_file in scripts_dir.glob("*.py"):
            try:
                content = py_file.read_text()
                
                # Look for hardcoded paths
                paths = re.findall(r'["\'][/\\][^"\']*["\']', content)
                for path in paths:
                    if any(keyword in path for keyword in ["Desktop", "gregpaulsen", "BigSky", "Coding_Commands"]):
                        hardcoded_paths.append(f"{py_file.name}: {path}")
                
            except Exception as e:
                hardcoded_paths.append(f"Error analyzing {py_file.name}: {e}")
        
        self.issues["hardcoded_paths"] = hardcoded_paths
        return hardcoded_paths
    
    def find_unused_imports(self) -> List[str]:
        """Find unused imports."""
        print("📦 Finding unused imports...")
        
        unused_imports = []
        scripts_dir = project_root / "scripts"
        
        for py_file in scripts_dir.glob("*.py"):
            try:
                content = py_file.read_text()
                tree = ast.parse(content)
                
                imported_modules = set()
                used_modules = set()
                
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            imported_modules.add(alias.name)
                    elif isinstance(node, ast.ImportFrom):
                        imported_modules.add(node.module or "")
                    elif isinstance(node, ast.Name):
                        used_modules.add(node.id)
                
                # This is a simplified check - in practice you'd need more sophisticated analysis
                if len(imported_modules) > 10:  # Flag files with many imports
                    unused_imports.append(f"{py_file.name}: Many imports ({len(imported_modules)})")
                
            except Exception as e:
                unused_imports.append(f"Error analyzing {py_file.name}: {e}")
        
        self.issues["unused_imports"] = unused_imports
        return unused_imports
    
    def apply_automated_fixes(self) -> List[str]:
        """Apply automated fixes where possible."""
        print("🔧 Applying automated fixes...")
        
        fixes = []
        scripts_dir = project_root / "scripts"
        
        for py_file in scripts_dir.glob("*.py"):
            try:
                content = py_file.read_text()
                original_content = content
                
                # Fix 1: Replace print() with logger.info() where appropriate
                if "print(" in content and "logger" in content:
                    content = re.sub(r'print\("([^"]+)"\)', r'logger.info("\1")', content)
                    if content != original_content:
                        fixes.append(f"{py_file.name}: Replaced print() with logger.info()")
                
                # Fix 2: Add missing logging imports
                if "logger" in content and "import logging" not in content:
                    # Add import at the top
                    lines = content.split('\n')
                    import_line = "import logging"
                    if import_line not in lines:
                        lines.insert(0, import_line)
                        content = '\n'.join(lines)
                        fixes.append(f"{py_file.name}: Added missing logging import")
                
                # Save changes if any were made
                if content != original_content:
                    py_file.write_text(content)
                
            except Exception as e:
                fixes.append(f"Error fixing {py_file.name}: {e}")
        
        self.fixes_applied = fixes
        return fixes
    
    def generate_refactor_report(self) -> str:
        """Generate comprehensive refactor report."""
        report = []
        report.append("# PaulyOps Code Hygiene & Refactor Report")
        report.append(f"**Generated:** {datetime.now().isoformat()}")
        report.append("")
        
        # Summary
        total_issues = sum(len(issues) for issues in self.issues.values())
        report.append("## 📊 Summary")
        report.append(f"- **Total Issues Found:** {total_issues}")
        report.append(f"- **Fixes Applied:** {len(self.fixes_applied)}")
        report.append("")
        
        # Detailed issues
        for category, issues in self.issues.items():
            if issues:
                report.append(f"## {category.replace('_', ' ').title()}")
                for issue in issues:
                    report.append(f"- {issue}")
                report.append("")
        
        # Applied fixes
        if self.fixes_applied:
            report.append("## 🔧 Applied Fixes")
            for fix in self.fixes_applied:
                report.append(f"- {fix}")
            report.append("")
        
        # Recommendations
        report.append("## 💡 Recommendations")
        if self.issues["dead_code"]:
            report.append("- **Remove dead code:** Consider removing unused functions")
        if self.issues["logging_issues"]:
            report.append("- **Standardize logging:** Use consistent logging patterns")
        if self.issues["config_issues"]:
            report.append("- **Modularize configs:** Move hardcoded values to configuration files")
        if self.issues["exception_issues"]:
            report.append("- **Improve error handling:** Add proper exception handling")
        if self.issues["hardcoded_paths"]:
            report.append("- **Remove hardcoded paths:** Use dynamic path resolution")
        
        return "\n".join(report)
    
    def run_complete_analysis(self) -> Dict:
        """Run complete code hygiene analysis."""
        print("🧹 PaulyOps Code Hygiene & Refactor Engineer")
        print("=" * 50)
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        # Run all analysis modules
        self.find_dead_code()
        self.normalize_logging()
        self.modularize_configs()
        self.validate_exception_handling()
        self.find_hardcoded_paths()
        self.find_unused_imports()
        
        # Apply automated fixes
        self.apply_automated_fixes()
        
        return self.issues

def main():
    """Run code hygiene analysis."""
    engineer = CodeHygieneEngineer()
    issues = engineer.run_complete_analysis()
    
    # Generate and save report
    report = engineer.generate_refactor_report()
    report_file = project_root / "Reports" / f"code_hygiene_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    report_file.write_text(report)
    
    print("\n" + "=" * 50)
    print("🧹 CODE HYGIENE ANALYSIS COMPLETE")
    total_issues = sum(len(issues) for issues in issues.values())
    print(f"📊 Issues Found: {total_issues}")
    print(f"🔧 Fixes Applied: {len(engineer.fixes_applied)}")
    print(f"📄 Report: {report_file}")
    print("=" * 50)

if __name__ == "__main__":
    main()

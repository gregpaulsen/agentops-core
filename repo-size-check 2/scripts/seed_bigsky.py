#!/usr/bin/env python3
"""Seed demo data for Big Sky Ag tenant."""

import json
import shutil
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Any

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config.loader import config
from utils.logging import logger
from tenancy.registry import get_tenant_context


def create_demo_files():
    """Create demo files in the ingest folder."""
    ingest_dir = Path(config.ingest_folder_name)
    ingest_dir.mkdir(exist_ok=True)
    
    # Create sample documents
    demo_files = {
        "field_report_2024_12_12.pdf": "Field inspection report for December 12, 2024",
        "crop_analysis.json": json.dumps({
            "crop": "wheat",
            "field": "North Field",
            "analysis_date": "2024-12-12",
            "health_score": 85,
            "recommendations": ["Apply fertilizer", "Monitor moisture"]
        }, indent=2),
        "equipment_maintenance.txt": """Equipment Maintenance Log
Date: 2024-12-12
Equipment: Tractor #3
Issue: Hydraulic fluid leak
Status: Scheduled for repair
Priority: Medium""",
        "financial_summary.csv": """Month,Revenue,Expenses,Profit
November,125000,89000,36000
December,98000,75000,23000""",
        "weather_data.yaml": """weather:
  date: 2024-12-12
  temperature: 65
  humidity: 45
  wind_speed: 8
  conditions: partly_cloudy
forecast:
  - date: 2024-12-13
    high: 68
    low: 42
    precipitation: 0.1"""
    }
    
    for filename, content in demo_files.items():
        file_path = ingest_dir / filename
        if isinstance(content, str):
            file_path.write_text(content)
        else:
            file_path.write_text(str(content))
        
        logger.info(f"✅ Created demo file: {filename}")
    
    return len(demo_files)


def create_demo_backups():
    """Create demo backup files."""
    backup_dir = Path(config.backup_dir)
    backup_dir.mkdir(parents=True, exist_ok=True)
    
    # Create demo backup files
    backup_files = [
        "bigsky_backup_2024_12_10.zip",
        "bigsky_backup_2024_12_11.zip",
        "bigsky_backup_2024_12_12.zip"
    ]
    
    for backup_file in backup_files:
        file_path = backup_dir / backup_file
        file_path.write_text(f"Demo backup content for {backup_file}")
        logger.info(f"✅ Created demo backup: {backup_file}")
    
    return len(backup_files)


def create_demo_operations():
    """Create demo operation logs."""
    operations = [
        {
            "id": "op_001",
            "operation": "file_ingest",
            "status": "completed",
            "timestamp": (datetime.now() - timedelta(hours=2)).isoformat(),
            "duration": 1.2,
            "details": "Processed 5 files from ingest folder"
        },
        {
            "id": "op_002", 
            "operation": "backup_rotation",
            "status": "completed",
            "timestamp": (datetime.now() - timedelta(hours=4)).isoformat(),
            "duration": 0.8,
            "details": "Rotated 2 backup files to archive"
        },
        {
            "id": "op_003",
            "operation": "storage_sync",
            "status": "completed", 
            "timestamp": (datetime.now() - timedelta(hours=6)).isoformat(),
            "duration": 2.1,
            "details": "Synced 15 files to cloud storage"
        },
        {
            "id": "op_004",
            "operation": "health_check",
            "status": "completed",
            "timestamp": (datetime.now() - timedelta(hours=8)).isoformat(),
            "duration": 0.3,
            "details": "System health check passed"
        }
    ]
    
    # Save operations to reports directory
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)
    
    operations_file = reports_dir / "demo_operations.json"
    with open(operations_file, "w") as f:
        json.dump(operations, f, indent=2)
    
    logger.info(f"✅ Created {len(operations)} demo operations")
    return operations


def create_demo_dashboard_data():
    """Create demo dashboard data."""
    dashboard_data = {
        "tenant": "bigsky",
        "plan": "starter",
        "status": "active",
        "stats": {
            "total_files": 25,
            "total_backups": 3,
            "storage_used_gb": 2.4,
            "storage_limit_gb": 50,
            "operations_today": 4,
            "last_backup": "2024-12-12T10:00:00Z"
        },
        "recent_activity": [
            {
                "type": "file_upload",
                "description": "Uploaded field_report_2024_12_12.pdf",
                "timestamp": datetime.now().isoformat()
            },
            {
                "type": "backup_created",
                "description": "Created daily backup",
                "timestamp": (datetime.now() - timedelta(hours=2)).isoformat()
            },
            {
                "type": "system_check",
                "description": "Health check completed",
                "timestamp": (datetime.now() - timedelta(hours=4)).isoformat()
            }
        ],
        "feature_flags": {
            "ENABLE_SSO": False,
            "ENABLE_AUDIT_LOG": True,
            "ENABLE_SCIM": False,
            "ENABLE_DLP": False,
            "ENABLE_RATE_LIMITS": False,
            "ENABLE_DASHBOARDS_PRO": False
        },
        "limits": {
            "MAX_USERS": 10,
            "MAX_STORAGE_GB": 50,
            "MAX_API_QPS": 50,
            "MAX_AI_TOKENS_PER_DAY": 100000
        }
    }
    
    # Save dashboard data
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)
    
    dashboard_file = reports_dir / "dashboard_summary.json"
    with open(dashboard_file, "w") as f:
        json.dump(dashboard_data, f, indent=2)
    
    logger.info("✅ Created demo dashboard data")
    return dashboard_data


def main():
    """Main seeding function."""
    logger.info("🌱 Starting Big Sky Ag demo data seeding...")
    
    # Get tenant context
    tenant_context = get_tenant_context("bigsky")
    if not tenant_context:
        logger.error("❌ Big Sky Ag tenant not found")
        return False
    
    logger.info(f"📋 Seeding data for tenant: {tenant_context.tenant.name}")
    logger.info(f"📋 Plan: {tenant_context.plan.name}")
    
    try:
        # Create demo files
        num_files = create_demo_files()
        logger.info(f"📁 Created {num_files} demo files in {config.ingest_folder_name}")
        
        # Create demo backups
        num_backups = create_demo_backups()
        logger.info(f"💾 Created {num_backups} demo backup files")
        
        # Create demo operations
        operations = create_demo_operations()
        logger.info(f"📊 Created {len(operations)} demo operations")
        
        # Create dashboard data
        dashboard_data = create_demo_dashboard_data()
        logger.info("📈 Created demo dashboard data")
        
        # Print summary
        print("\n" + "=" * 60)
        print("BIG SKY AG DEMO DATA SEEDING COMPLETE")
        print("=" * 60)
        print(f"✅ Tenant: {tenant_context.tenant.name}")
        print(f"✅ Plan: {tenant_context.plan.name}")
        print(f"✅ Demo Files: {num_files}")
        print(f"✅ Demo Backups: {num_backups}")
        print(f"✅ Demo Operations: {len(operations)}")
        print(f"✅ Dashboard Data: Created")
        print(f"✅ Ingest Folder: {config.ingest_folder_name}")
        print(f"✅ Backup Directory: {config.backup_dir}")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Error seeding demo data: {e}")
        return False


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)

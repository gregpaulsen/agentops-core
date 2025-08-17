"""Dashboard update functionality for PaulyOps."""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

from utils.logging import logger


def update_summary(report_path: str) -> Dict[str, Any]:
    """
    Update dashboard summary from a JSON status report.
    
    Args:
        report_path: Path to the JSON status report
        
    Returns:
        Dictionary with update status
    """
    logger.info(f"🔄 Updating dashboard summary from {report_path}")
    
    try:
        # Read the status report
        with open(report_path, 'r') as f:
            status_data = json.load(f)
        
        # Process the status data
        summary = {
            "timestamp": datetime.now().isoformat(),
            "status": "updated",
            "source_report": report_path,
            "processed_data": status_data
        }
        
        # Save the updated summary
        summary_path = Path("reports") / "dashboard_summary.json"
        summary_path.parent.mkdir(exist_ok=True)
        
        with open(summary_path, 'w') as f:
            json.dump(summary, f, indent=2)
        
        logger.info(f"✅ Dashboard summary updated: {summary_path}")
        print(f"📊 Dashboard updated from {report_path}")
        
        return summary
        
    except FileNotFoundError:
        logger.error(f"❌ Status report not found: {report_path}")
        return {"error": "Status report not found"}
    except json.JSONDecodeError as e:
        logger.error(f"❌ Invalid JSON in status report: {e}")
        return {"error": "Invalid JSON in status report"}
    except Exception as e:
        logger.error(f"❌ Error updating dashboard: {e}")
        return {"error": str(e)}


def get_dashboard_status() -> Dict[str, Any]:
    """
    Get current dashboard status.
    
    Returns:
        Dictionary with current dashboard status
    """
    summary_path = Path("reports") / "dashboard_summary.json"
    
    if summary_path.exists():
        try:
            with open(summary_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"❌ Error reading dashboard status: {e}")
    
    return {
        "timestamp": datetime.now().isoformat(),
        "status": "no_data",
        "message": "No dashboard data available"
    }


def create_status_report(operation: str, results: Dict[str, Any]) -> str:
    """
    Create a status report for dashboard consumption.
    
    Args:
        operation: Name of the operation performed
        results: Results of the operation
        
    Returns:
        Path to the created status report
    """
    timestamp = datetime.now().isoformat()
    
    status_data = {
        "timestamp": timestamp,
        "operation": operation,
        "results": results,
        "status": "completed"
    }
    
    # Save status report
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)
    
    report_path = reports_dir / f"run_status_{timestamp[:10]}.json"
    
    with open(report_path, 'w') as f:
        json.dump(status_data, f, indent=2)
    
    logger.info(f"📄 Status report created: {report_path}")
    return str(report_path)

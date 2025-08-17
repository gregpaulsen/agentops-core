#!/usr/bin/env python3
"""
Simple Dropzone Processor
Process files that have been sitting in the Dropzone since last night
"""

import os
import shutil
import json
from pathlib import Path
from datetime import datetime

def create_enterprise_structure():
    """Create the enterprise folder structure"""
    base_path = Path("/Users/gregpaulsen/Desktop")
    enterprise_path = base_path / "EnterpriseSystem"
    
    # Create main structure
    folders = [
        "Companies/BigSkyAg",
        "Companies/PaulyOps", 
        "Companies/General",
        "Core/AgentFramework",
        "Core/Security",
        "Core/Routing",
        "Core/UI",
        "Agents/BuiltIn",
        "Agents/External",
        "Agents/Marketplace",
        "CloudSync/GoogleDrive",
        "CloudSync/Dropbox", 
        "CloudSync/iCloud",
        "Documentation",
        "Logs",
        "Backups"
    ]
    
    for folder in folders:
        (enterprise_path / folder).mkdir(parents=True, exist_ok=True)
    
    # Create company-specific subfolders
    company_subfolders = [
        "Finance", "Legal", "Marketing", "Technical", 
        "Operations", "Communications", "Documents", 
        "Data", "Images", "General"
    ]
    
    for company in ["BigSkyAg", "PaulyOps", "General"]:
        company_path = enterprise_path / "Companies" / company
        for subfolder in company_subfolders:
            (company_path / subfolder).mkdir(exist_ok=True)
    
    print("✓ Enterprise structure created")

def analyze_file_content(file_path):
    """Simple content analysis based on filename and extension"""
    filename = file_path.name.lower()
    extension = file_path.suffix.lower()
    
    # Company detection
    if any(term in filename for term in ["pauly", "ops", "email", "inbox", "ai", "agent"]):
        company = "paulyops"
        folder = "PaulyOps"
    elif any(term in filename for term in ["big", "sky", "ag", "agriculture", "farming", "crop", "ndvi"]):
        company = "big_sky_ag"
        folder = "BigSkyAg"
    else:
        company = "unknown"
        folder = "General"
    
    # Content type detection
    if any(term in filename for term in ["invoice", "receipt", "payment", "billing"]):
        subfolder = "Finance"
    elif any(term in filename for term in ["contract", "legal", "agreement"]):
        subfolder = "Legal"
    elif any(term in filename for term in ["presentation", "marketing", "brochure"]):
        subfolder = "Marketing"
    elif any(term in filename for term in ["code", "script", "technical", "api"]):
        subfolder = "Technical"
    elif any(term in filename for term in ["report", "analysis", "data", "metrics"]):
        subfolder = "Operations"
    elif extension in ['.jpg', '.jpeg', '.png', '.gif']:
        subfolder = "Images"
    elif extension in ['.pdf', '.doc', '.docx']:
        subfolder = "Documents"
    elif extension in ['.xls', '.xlsx', '.csv']:
        subfolder = "Data"
    else:
        subfolder = "General"
    
    return {
        "company": company,
        "folder": folder,
        "subfolder": subfolder,
        "confidence": 0.8 if company != "unknown" else 0.3
    }

def process_dropzone(dropzone_name):
    """Process files in a specific dropzone"""
    base_path = Path("/Users/gregpaulsen/Desktop")
    dropzone_path = base_path / dropzone_name
    enterprise_path = base_path / "EnterpriseSystem"
    
    if not dropzone_path.exists():
        print(f"✗ Dropzone not found: {dropzone_name}")
        return
    
    print(f"\nProcessing {dropzone_name}...")
    
    processed_files = []
    errors = []
    
    # Process all items in dropzone
    for item in dropzone_path.iterdir():
        if item.name.startswith('.'):
            continue
            
        if item.is_file():
            # Process single file
            result = process_single_file(item, enterprise_path)
            if result["success"]:
                processed_files.append(result)
            else:
                errors.append(result)
        elif item.is_dir():
            # Process directory contents
            for file_item in item.rglob('*'):
                if file_item.is_file() and not file_item.name.startswith('.'):
                    result = process_single_file(file_item, enterprise_path)
                    if result["success"]:
                        processed_files.append(result)
                    else:
                        errors.append(result)
    
    # Print results
    print(f"  ✓ Successfully processed: {len(processed_files)} files")
    print(f"  ✗ Errors: {len(errors)} files")
    
    for result in processed_files:
        print(f"    ✓ {result['source']} -> {result['target']}")
    
    for result in errors:
        print(f"    ✗ {result['source']}: {result['error']}")
    
    return {
        "dropzone": dropzone_name,
        "processed": processed_files,
        "errors": errors
    }

def process_single_file(file_path, enterprise_path):
    """Process a single file"""
    try:
        # Analyze file content
        analysis = analyze_file_content(file_path)
        
        # Determine target location
        target_dir = enterprise_path / "Companies" / analysis["folder"] / analysis["subfolder"]
        target_dir.mkdir(parents=True, exist_ok=True)
        
        # Handle filename conflicts
        target_path = target_dir / file_path.name
        counter = 1
        while target_path.exists():
            stem = file_path.stem
            suffix = file_path.suffix
            target_path = target_dir / f"{stem}_{counter}{suffix}"
            counter += 1
        
        # Move file
        shutil.move(str(file_path), str(target_path))
        
        # Create backup
        backup_dir = enterprise_path / "Backups" / datetime.now().strftime("%Y-%m-%d")
        backup_dir.mkdir(parents=True, exist_ok=True)
        backup_path = backup_dir / f"{file_path.stem}_{datetime.now().strftime('%H%M%S')}{file_path.suffix}"
        shutil.copy2(str(target_path), str(backup_path))
        
        return {
            "success": True,
            "source": str(file_path),
            "target": str(target_path),
            "analysis": analysis
        }
        
    except Exception as e:
        return {
            "success": False,
            "source": str(file_path),
            "error": str(e)
        }

def main():
    """Main function"""
    print("=== Enterprise System Dropzone Processor ===")
    print(f"Timestamp: {datetime.now()}")
    
    # Create enterprise structure
    create_enterprise_structure()
    
    # Show current dropzone status
    base_path = Path("/Users/gregpaulsen/Desktop")
    dropzones = ["BigSkyAgDropzone", "PaulyOpsDropzone"]
    
    print("\nCurrent Dropzone Status:")
    for dropzone in dropzones:
        dropzone_path = base_path / dropzone
        if dropzone_path.exists():
            files = [f.name for f in dropzone_path.iterdir() if f.is_file() and not f.name.startswith('.')]
            dirs = [d.name for d in dropzone_path.iterdir() if d.is_dir() and not d.name.startswith('.')]
            
            print(f"  {dropzone}:")
            print(f"    Files: {len(files)}")
            print(f"    Directories: {len(dirs)}")
            if files:
                print(f"    Files: {', '.join(files)}")
            if dirs:
                print(f"    Directories: {', '.join(dirs)}")
    
    # Ask for confirmation
    print("\n" + "="*50)
    print("Files have been detected in the Dropzones since 10:24 PM last night.")
    print("The intelligent routing system will now process these files.")
    print("="*50)
    
    response = input("\nProceed with processing? (y/N): ").strip().lower()
    
    if response in ['y', 'yes']:
        # Process each dropzone
        all_results = []
        for dropzone in dropzones:
            results = process_dropzone(dropzone)
            if results:
                all_results.append(results)
        
        # Save results to log
        log_file = base_path / "EnterpriseSystem" / "Logs" / f"processing_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        log_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(log_file, 'w') as f:
            json.dump(all_results, f, indent=2)
        
        print("\n" + "="*50)
        print("Processing complete!")
        print(f"Results saved to: {log_file}")
        print("Files have been routed to the Enterprise System structure.")
        print("="*50)
        
    else:
        print("Processing cancelled.")

if __name__ == "__main__":
    main()

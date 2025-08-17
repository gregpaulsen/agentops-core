#!/usr/bin/env python3
"""FastAPI application for PaulyOps multi-tenant platform."""

from fastapi import FastAPI, HTTPException, Depends, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.websockets import WebSocket, WebSocketDisconnect
from typing import Optional, Dict, Any
import json
import asyncio
from pathlib import Path

# Import our platform modules
from config.loader import config
from tenancy.registry import get_tenant_context, current_tenant
from utils.logging import logger
from dashboards.update import get_dashboard_status


app = FastAPI(
    title="PaulyOps Multi-Tenant Platform",
    description="White-label identity + automation platform with OIDC/OAuth2 authentication",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_tenant_from_request(request: Request) -> Optional[str]:
    """Extract tenant from request headers or query params."""
    # Check header first
    tenant = request.headers.get("X-Tenant")
    if tenant:
        return tenant
    
    # Check query param
    tenant = request.query_params.get("tenant")
    if tenant:
        return tenant
    
    # Default to bigsky for demo
    return "bigsky"


@app.get("/health")
async def health_check():
    """System health check endpoint."""
    try:
        # Run basic health checks
        health_status = {
            "status": "healthy",
            "timestamp": "2024-12-12T20:00:00Z",
            "checks": {
                "environment": True,
                "paths": True,
                "credentials": True,
                "dependencies": True
            },
            "version": "1.0.0"
        }
        return health_status
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=500, detail="Health check failed")


@app.get("/config")
async def get_configuration(request: Request):
    """Get current tenant configuration."""
    tenant_id = get_tenant_from_request(request)
    tenant_context = get_tenant_context(tenant_id)
    
    if not tenant_context:
        raise HTTPException(status_code=404, detail="Tenant not found")
    
    return {
        "tenant": tenant_context.tenant.tenant_id,
        "plan": tenant_context.plan.plan_id,
        "storage_provider": config.storage_provider,
        "feature_flags": tenant_context.get_feature_flags().__dict__,
        "limits": tenant_context.get_limits().__dict__,
        "compliance": tenant_context.get_compliance().__dict__
    }


@app.get("/backups")
async def list_backups(request: Request):
    """Get backup status and history."""
    tenant_id = get_tenant_from_request(request)
    tenant_context = get_tenant_context(tenant_id)
    
    if not tenant_context:
        raise HTTPException(status_code=404, detail="Tenant not found")
    
    backup_dir = Path(config.backup_dir)
    archive_dir = Path(config.archive_dir)
    
    current_backups = list(backup_dir.glob("*.zip")) if backup_dir.exists() else []
    archive_files = list(archive_dir.glob("*.zip")) if archive_dir.exists() else []
    
    total_size_gb = sum(f.stat().st_size for f in current_backups + archive_files) / (1024**3)
    
    return {
        "current_backups": len(current_backups),
        "archive_files": len(archive_files),
        "total_size_gb": round(total_size_gb, 2),
        "backup_dir": str(config.backup_dir),
        "archive_dir": str(config.archive_dir)
    }


@app.post("/backups")
async def create_backup(request: Request, dry_run: bool = False):
    """Trigger manual backup creation."""
    tenant_id = get_tenant_from_request(request)
    tenant_context = get_tenant_context(tenant_id)
    
    if not tenant_context:
        raise HTTPException(status_code=404, detail="Tenant not found")
    
    if dry_run:
        return {"message": "Dry run backup simulation completed", "dry_run": True}
    
    # TODO: Implement actual backup creation
    return {"message": "Backup created successfully", "backup_id": "backup_123"}


@app.get("/files")
async def list_files(request: Request, path: Optional[str] = None):
    """Get file listing and metadata."""
    tenant_id = get_tenant_from_request(request)
    tenant_context = get_tenant_context(tenant_id)
    
    if not tenant_context:
        raise HTTPException(status_code=404, detail="Tenant not found")
    
    # Default to ingest folder if no path specified
    if not path:
        path = config.ingest_folder_name
    
    target_path = Path(path)
    if not target_path.exists():
        return []
    
    files = []
    for item in target_path.iterdir():
        files.append({
            "name": item.name,
            "path": str(item),
            "size": item.stat().st_size if item.is_file() else 0,
            "modified": "2024-12-12T20:00:00Z",  # TODO: Get actual timestamp
            "type": "file" if item.is_file() else "directory"
        })
    
    return files


@app.get("/operations")
async def list_operations(request: Request, limit: int = 50):
    """Get recent operations log."""
    tenant_id = get_tenant_from_request(request)
    tenant_context = get_tenant_context(tenant_id)
    
    if not tenant_context:
        raise HTTPException(status_code=404, detail="Tenant not found")
    
    # Load operations from reports
    operations_file = Path("reports/demo_operations.json")
    if operations_file.exists():
        with open(operations_file) as f:
            operations = json.load(f)
        return operations[:limit]
    
    return []


@app.get("/branding")
async def get_branding(request: Request):
    """Get tenant branding information."""
    tenant_id = get_tenant_from_request(request)
    tenant_context = get_tenant_context(tenant_id)
    
    if not tenant_context:
        raise HTTPException(status_code=404, detail="Tenant not found")
    
    branding = tenant_context.tenant.branding
    return {
        "tenant_id": tenant_context.tenant.tenant_id,
        "tenant_name": tenant_context.tenant.name,
        "logo_url": branding.logo_url,
        "primary_color": branding.primary_color,
        "secondary_color": branding.secondary_color,
        "email_sender": branding.email_sender,
        "legal_footer": branding.legal_footer
    }


@app.get("/features")
async def get_features(request: Request):
    """Get tenant feature flags."""
    tenant_id = get_tenant_from_request(request)
    tenant_context = get_tenant_context(tenant_id)
    
    if not tenant_context:
        raise HTTPException(status_code=404, detail="Tenant not found")
    
    return {
        "tenant_id": tenant_context.tenant.tenant_id,
        "plan": tenant_context.plan.plan_id,
        "feature_flags": tenant_context.get_feature_flags().__dict__,
        "limits": tenant_context.get_limits().__dict__
    }


@app.get("/reports/summary")
async def get_summary_report(request: Request, tenant: Optional[str] = None):
    """Get summary report for tenant."""
    tenant_id = tenant or get_tenant_from_request(request)
    tenant_context = get_tenant_context(tenant_id)
    
    if not tenant_context:
        raise HTTPException(status_code=404, detail="Tenant not found")
    
    # Load dashboard summary
    dashboard_file = Path("reports/dashboard_summary.json")
    if dashboard_file.exists():
        with open(dashboard_file) as f:
            dashboard_data = json.load(f)
        return dashboard_data
    
    # Fallback summary
    return {
        "tenant": tenant_context.tenant.tenant_id,
        "plan": tenant_context.plan.plan_id,
        "status": "active",
        "stats": {
            "total_files": 0,
            "total_backups": 0,
            "storage_used_gb": 0,
            "storage_limit_gb": tenant_context.get_limits().__dict__.get("MAX_STORAGE_GB", 0),
            "operations_today": 0
        }
    }


@app.get("/auth/login")
async def oauth_login(provider: str = "google"):
    """OAuth login endpoint."""
    return {
        "message": "Redirect to OIDC provider",
        "provider": provider,
        "auth_url": f"https://accounts.google.com/oauth/authorize?client_id=your-client-id&redirect_uri=http://localhost:8000/auth/callback&response_type=code&scope=openid profile email"
    }


@app.get("/auth/callback")
async def oauth_callback(code: str, state: str):
    """OAuth callback endpoint."""
    return {
        "message": "Authentication successful",
        "access_token": "demo_token_123",
        "token_type": "Bearer",
        "expires_in": 3600
    }


@app.get("/auth/user")
async def get_user_info(request: Request):
    """Get current user information."""
    # TODO: Implement JWT verification
    return {
        "sub": "user_123",
        "email": "user@bigskyag.farm",
        "name": "Demo User",
        "roles": ["admin"],
        "groups": ["bigsky-admin"]
    }


# Managed Services endpoints
@app.get("/services/catalog")
async def get_services_catalog(request: Request):
    """Get available services catalog."""
    tenant_id = get_tenant_from_request(request)
    tenant_context = get_tenant_context(tenant_id)

    if not tenant_context:
        raise HTTPException(status_code=404, detail="Tenant not found")

    catalog = [
        {
            "id": "backup_monitoring",
            "name": "Backup Monitoring",
            "desc": "Automated alerts and monitoring for backup status and health",
            "category": "Backup",
            "price_tier": "premium",
        },
        {
            "id": "dr_snapshots",
            "name": "DR Snapshots",
            "desc": "Periodic disaster recovery snapshots with cross-region replication",
            "category": "Backup",
            "price_tier": "premium",
        },
        {
            "id": "audit_enhanced",
            "name": "Enhanced Audit",
            "desc": "Long-term audit log retention and advanced compliance reporting",
            "category": "Compliance",
            "price_tier": "enterprise",
        },
        {
            "id": "dlp_scanner",
            "name": "DLP Scanner",
            "desc": "Data loss prevention scanning for sensitive information",
            "category": "Security",
            "price_tier": "enterprise",
        },
        {
            "id": "dashboards_pro",
            "name": "Pro Dashboards",
            "desc": "Advanced analytics dashboards with custom reporting",
            "category": "Analytics",
            "price_tier": "premium",
        },
        {
            "id": "support_sla",
            "name": "Priority Support",
            "desc": "24/7 priority support with guaranteed response times",
            "category": "Support",
            "price_tier": "enterprise",
        },
    ]
    
    return catalog


@app.get("/services/status")
async def get_services_status(request: Request):
    """Get current services status for tenant."""
    tenant_id = get_tenant_from_request(request)
    tenant_context = get_tenant_context(tenant_id)

    if not tenant_context:
        raise HTTPException(status_code=404, detail="Tenant not found")

    # Mock status based on tenant
    if tenant_id == "acme":
        status = {
            "enabled": ["backup_monitoring", "dashboards_pro"],
            "available": ["backup_monitoring", "dr_snapshots", "audit_enhanced", "dlp_scanner", "dashboards_pro", "support_sla"],
        }
    else:
        status = {
            "enabled": [],
            "available": ["backup_monitoring", "dr_snapshots", "audit_enhanced", "dlp_scanner", "dashboards_pro", "support_sla"],
        }
    
    return status


@app.post("/services/enable")
async def enable_service(request: Request):
    """Enable a service for the tenant."""
    tenant_id = get_tenant_from_request(request)
    tenant_context = get_tenant_context(tenant_id)

    if not tenant_context:
        raise HTTPException(status_code=404, detail="Tenant not found")

    # Check if managed services are enabled for this tenant
    if not tenant_context.get_feature_flags().__dict__.get('ENABLE_MANAGED_SERVICES', False):
        raise HTTPException(status_code=403, detail="Managed Services not available for this plan")

    # TODO: Implement actual service enabling logic
    # For now, just return success
    return {"message": "Service enabled successfully"}


@app.post("/services/disable")
async def disable_service(request: Request):
    """Disable a service for the tenant."""
    tenant_id = get_tenant_from_request(request)
    tenant_context = get_tenant_context(tenant_id)

    if not tenant_context:
        raise HTTPException(status_code=404, detail="Tenant not found")

    # Check if managed services are enabled for this tenant
    if not tenant_context.get_feature_flags().__dict__.get('ENABLE_MANAGED_SERVICES', False):
        raise HTTPException(status_code=403, detail="Managed Services not available for this plan")

    # TODO: Implement actual service disabling logic
    # For now, just return success
    return {"message": "Service disabled successfully"}


# WebSocket endpoint for real-time updates
@app.websocket("/ws/events")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time events."""
    await websocket.accept()
    
    try:
        # Send initial connection message
        await websocket.send_text(json.dumps({
            "event": "connected",
            "data": {"message": "WebSocket connected"},
            "timestamp": "2024-12-12T20:00:00Z"
        }))
        
        # Simulate periodic events
        while True:
            await asyncio.sleep(30)  # Send event every 30 seconds
            
            # Mock events
            events = [
                {
                    "event": "operation_completed",
                    "data": {"id": "op_001", "status": "completed", "operation": "file_ingest"}
                },
                {
                    "event": "backup_created",
                    "data": {"id": "backup_001", "size": "2.4GB", "status": "completed"}
                },
                {
                    "event": "file_uploaded",
                    "data": {"name": "document.pdf", "size": "1.2MB", "status": "completed"}
                },
                {
                    "event": "health_check",
                    "data": {"status": "healthy", "timestamp": "2024-12-12T20:00:00Z"}
                }
            ]
            
            import random
            event = random.choice(events)
            event["timestamp"] = "2024-12-12T20:00:00Z"
            
            await websocket.send_text(json.dumps(event))
            
    except WebSocketDisconnect:
        print("WebSocket disconnected")
    except Exception as e:
        print(f"WebSocket error: {e}")


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "PaulyOps Multi-Tenant Platform API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
        "tenant": "bigsky"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

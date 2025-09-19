"""
Admin endpoints for DocuBotAI system management.
"""
from fastapi import APIRouter, HTTPException, Depends, Security
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
from typing import List, Dict
from sqlalchemy.orm import Session
import psutil
import os

from docubotai.core.database import get_db
from docubotai.core.config import settings
from docubotai.models.database import SystemMetrics

router = APIRouter(prefix="/admin", tags=["admin"])

# Security
api_key_header = APIKeyHeader(name="X-API-Key")

async def get_api_key(api_key: str = Security(api_key_header)):
    """Validate API key."""
    if api_key != settings.ADMIN_API_KEY:
        raise HTTPException(
            status_code=403,
            detail="Invalid API key"
        )
    return api_key

class SystemStatus(BaseModel):
    """System status model."""
    cpu_usage: float
    memory_usage: float
    disk_usage: float
    active_tasks: int
    queue_size: int
    uptime: float

class MaintenanceMode(BaseModel):
    """Maintenance mode settings."""
    enabled: bool
    message: str = "System is under maintenance"

@router.get("/status", response_model=SystemStatus)
async def get_system_status(
    db: Session = Depends(get_db),
    _: str = Depends(get_api_key)
):
    """Get system status metrics."""
    metrics = {
        "cpu_usage": psutil.cpu_percent(),
        "memory_usage": psutil.virtual_memory().percent,
        "disk_usage": psutil.disk_usage("/").percent,
        "active_tasks": db.query(SystemMetrics).filter(
            SystemMetrics.status == "running"
        ).count(),
        "queue_size": db.query(SystemMetrics).filter(
            SystemMetrics.status == "pending"
        ).count(),
        "uptime": psutil.boot_time()
    }
    
    # Store metrics
    db_metrics = SystemMetrics(**metrics)
    db.add(db_metrics)
    db.commit()
    
    return SystemStatus(**metrics)

@router.post("/maintenance")
async def set_maintenance_mode(
    settings: MaintenanceMode,
    _: str = Depends(get_api_key)
):
    """Enable/disable maintenance mode."""
    # Update maintenance mode in settings
    os.environ["MAINTENANCE_MODE"] = str(settings.enabled)
    os.environ["MAINTENANCE_MESSAGE"] = settings.message
    
    return {
        "status": "success",
        "maintenance_mode": settings.enabled,
        "message": settings.message
    }

@router.post("/reload-config")
async def reload_configuration(
    _: str = Depends(get_api_key)
):
    """Reload system configuration."""
    try:
        settings.reload()
        return {"status": "success", "message": "Configuration reloaded"}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to reload configuration: {str(e)}"
        )

@router.get("/logs")
async def get_system_logs(
    limit: int = 100,
    level: str = "ERROR",
    _: str = Depends(get_api_key)
):
    """Get system logs."""
    # Implementation depends on logging setup
    return {
        "status": "success",
        "message": "Log retrieval not implemented yet"
    }
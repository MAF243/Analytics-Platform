import time
from typing import Any, Dict

import psutil
from fastapi import APIRouter, Depends, Request

from backend.app.api.dependencies import get_processing_time, get_request_id
from backend.app.core.config import settings
from backend.app.core.responses import ApiResponse

# Record app startup time for uptime metric
APP_START_TIME = time.time()

router = APIRouter(tags=["System"])


@router.get("/health", response_model=ApiResponse[Any])
async def health_check(
    request: Request,
    request_id: str = Depends(get_request_id),
    processing_time: float = Depends(get_processing_time),
) -> ApiResponse[Any]:
    """Basic health check endpoint with enterprise metrics."""
    memory = psutil.virtual_memory()
    uptime = time.time() - APP_START_TIME

    return ApiResponse(
        success=True,
        message="System is healthy",
        data={
            "status": "OK",
            "uptime_seconds": round(uptime, 2),
            "memory": {
                "total_mb": round(memory.total / (1024 * 1024), 2),
                "available_mb": round(memory.available / (1024 * 1024), 2),
                "percent": memory.percent,
            },
            "dependencies": {
                "storage": "OK",  # In a real app, ping the DB/Storage here
            },
        },
        request_id=request_id,
        processing_time=processing_time,
        version=settings.version,
        status=200,
    )


@router.get("/ready", response_model=ApiResponse[str])
async def readiness_check(
    request: Request,
    request_id: str = Depends(get_request_id),
    processing_time: float = Depends(get_processing_time),
) -> ApiResponse[str]:
    """Readiness check endpoint for orchestrators (e.g., K8s, Docker)."""
    return ApiResponse(
        success=True,
        message="System is ready to accept traffic",
        data="READY",
        request_id=request_id,
        processing_time=processing_time,
        version=settings.version,
        status=200,
    )



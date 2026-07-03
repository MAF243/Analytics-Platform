from typing import Any, Dict

from fastapi import APIRouter, Depends, Request

from backend.app.api.dependencies import (
    get_analytics_artifact_use_case,
    get_dashboard_use_case,
    get_processing_time,
    get_request_id,
    get_run_analytics_use_case,
)
from backend.app.application.use_cases.get_dashboard import (
    GetAnalyticsArtifactUseCase,
    GetDashboardUseCase,
)
from backend.app.application.use_cases.run_analytics import RunAnalyticsUseCase
from backend.app.core.config import settings
from backend.app.core.rate_limit import limiter
from backend.app.core.responses import ApiResponse

router = APIRouter(tags=["Analytics"])


@router.post("/analysis/{dataset_id}", response_model=ApiResponse[Dict[str, Any]])
@limiter.limit("5/minute")
async def run_analysis(
    dataset_id: str,
    request: Request,
    request_id: str = Depends(get_request_id),
    processing_time: float = Depends(get_processing_time),
    use_case: RunAnalyticsUseCase = Depends(get_run_analytics_use_case),
) -> ApiResponse[Dict[str, Any]]:
    """Runs the full analytics pipeline synchronously for the dataset."""
    dashboard = use_case.execute(dataset_id)
    return ApiResponse(
        success=True,
        message="Analytics pipeline completed successfully",
        data=dashboard,
        request_id=request_id,
        processing_time=processing_time,
        version=settings.version,
        status=200,
    )


@router.get("/dashboard/{dataset_id}", response_model=ApiResponse[Dict[str, Any]])
@limiter.limit("20/minute")
async def get_dashboard(
    dataset_id: str,
    request: Request,
    request_id: str = Depends(get_request_id),
    processing_time: float = Depends(get_processing_time),
    use_case: GetDashboardUseCase = Depends(get_dashboard_use_case),
) -> ApiResponse[Dict[str, Any]]:
    """Retrieves the pre-computed dashboard DTO."""
    dashboard = use_case.execute(dataset_id)
    return ApiResponse(
        success=True,
        message="Dashboard retrieved successfully",
        data=dashboard,
        request_id=request_id,
        processing_time=processing_time,
        version=settings.version,
        status=200,
    )


@router.get("/profiling/{dataset_id}", response_model=ApiResponse[Dict[str, Any]])
async def get_profiling(
    dataset_id: str,
    request: Request,
    request_id: str = Depends(get_request_id),
    processing_time: float = Depends(get_processing_time),
    use_case: GetAnalyticsArtifactUseCase = Depends(get_analytics_artifact_use_case),
) -> ApiResponse[Dict[str, Any]]:
    artifact = use_case.execute(dataset_id, "profiling.json")
    return ApiResponse(
        success=True,
        message="Profiling artifact retrieved successfully",
        data=artifact,
        request_id=request_id,
        processing_time=processing_time,
        version=settings.version,
        status=200,
    )


@router.get("/summary/{dataset_id}", response_model=ApiResponse[Dict[str, Any]])
async def get_summary(
    dataset_id: str,
    request: Request,
    request_id: str = Depends(get_request_id),
    processing_time: float = Depends(get_processing_time),
    use_case: GetAnalyticsArtifactUseCase = Depends(get_analytics_artifact_use_case),
) -> ApiResponse[Dict[str, Any]]:
    artifact = use_case.execute(dataset_id, "summary.json")
    return ApiResponse(
        success=True,
        message="Summary artifact retrieved successfully",
        data=artifact,
        request_id=request_id,
        processing_time=processing_time,
        version=settings.version,
        status=200,
    )


@router.get("/clusters/{dataset_id}", response_model=ApiResponse[Dict[str, Any]])
async def get_clusters(
    dataset_id: str,
    request: Request,
    request_id: str = Depends(get_request_id),
    processing_time: float = Depends(get_processing_time),
    use_case: GetAnalyticsArtifactUseCase = Depends(get_analytics_artifact_use_case),
) -> ApiResponse[Dict[str, Any]]:
    artifact = use_case.execute(dataset_id, "clustering.json")
    return ApiResponse(
        success=True,
        message="Clustering artifact retrieved successfully",
        data=artifact,
        request_id=request_id,
        processing_time=processing_time,
        version=settings.version,
        status=200,
    )

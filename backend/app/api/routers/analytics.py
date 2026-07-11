from typing import Any, Dict

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request

from backend.app.api.dependencies import (
    get_analysis_executor,
    get_analysis_job_repository,
    get_analytics_artifact_use_case,
    get_dashboard_use_case,
    get_processing_time,
    get_request_id,
)
from backend.app.application.orchestration.analysis_executor import AnalysisExecutor
from backend.app.application.ports.analysis_job_repository import AnalysisJobRepository
from backend.app.application.use_cases.get_dashboard import (
    GetAnalyticsArtifactUseCase,
    GetDashboardUseCase,
)
from backend.app.core.config import settings
from backend.app.core.rate_limit import limiter
from backend.app.core.responses import ApiResponse

router = APIRouter(tags=["Analytics"])


@router.post(
    "/analysis/{dataset_id}",
    response_model=ApiResponse[Dict[str, Any]],
    status_code=202,
)
@limiter.limit("5/minute")
async def run_analysis(
    dataset_id: str,
    request: Request,
    background_tasks: BackgroundTasks,
    request_id: str = Depends(get_request_id),
    processing_time: float = Depends(get_processing_time),
    executor: AnalysisExecutor = Depends(get_analysis_executor),
) -> ApiResponse[Dict[str, Any]]:
    """Queues the analytics pipeline for background execution."""
    job = executor.initialize_job(dataset_id)
    correlation_id = getattr(request.state, "correlation_id", "unknown")
    background_tasks.add_task(
        executor.execute_pipeline, dataset_id, job.job_id, request_id, correlation_id
    )

    return ApiResponse(
        success=True,
        message="Analytics pipeline queued successfully",
        data={"dataset_id": dataset_id, "status": job.status.value},
        request_id=request_id,
        processing_time=processing_time,
        version=settings.version,
        status=202,
    )


@router.get("/analysis/{dataset_id}/status", response_model=ApiResponse[Dict[str, Any]])
async def get_analysis_status(
    dataset_id: str,
    request: Request,
    request_id: str = Depends(get_request_id),
    processing_time: float = Depends(get_processing_time),
    job_repo: AnalysisJobRepository = Depends(get_analysis_job_repository),
) -> ApiResponse[Dict[str, Any]]:
    """Retrieves the current execution status of the analytics pipeline."""
    job = job_repo.get_latest_for_dataset(dataset_id)
    if not job:
        raise HTTPException(
            status_code=404, detail="Analysis status not found for dataset"
        )

    from dataclasses import asdict

    status_dict = asdict(job)
    if job.started_at:
        status_dict["started_at"] = job.started_at.isoformat()
    if job.updated_at:
        status_dict["updated_at"] = job.updated_at.isoformat()
    if job.finished_at:
        status_dict["finished_at"] = job.finished_at.isoformat()

    return ApiResponse(
        success=True,
        message="Analysis status retrieved successfully",
        data=status_dict,
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

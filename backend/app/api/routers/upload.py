from fastapi import APIRouter, Depends, File, Request, UploadFile

from backend.app.api.dependencies import (
    get_processing_time,
    get_request_id,
    get_upload_use_case,
)
from backend.app.application.dtos.upload_response import UploadResponse
from backend.app.application.use_cases.upload_dataset import UploadDatasetUseCase
from backend.app.core.config import settings
from backend.app.core.responses import ApiResponse
from backend.app.core.rate_limit import limiter

router = APIRouter(tags=["Dataset"])


@router.post("/upload", response_model=ApiResponse[UploadResponse])
@limiter.limit("10/minute")
async def upload_dataset(
    request: Request,
    file: UploadFile = File(...),
    use_case: UploadDatasetUseCase = Depends(get_upload_use_case),
    request_id: str = Depends(get_request_id),
    processing_time: float = Depends(get_processing_time),
) -> ApiResponse[UploadResponse]:
    """Uploads a CSV dataset for analysis."""

    # Process upload via use case (synchronously in memory for MVP constraints)
    response_dto = use_case.execute(
        file_stream=file.file,
        filename=file.filename or "unknown.csv",
        content_type=file.content_type or "application/octet-stream",
        size_bytes=file.size or 0,
    )

    return ApiResponse(
        success=True,
        message="Dataset uploaded successfully",
        data=response_dto,
        request_id=request_id,
        processing_time=processing_time,
        version=settings.version,
        status=200,
    )

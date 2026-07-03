from fastapi import APIRouter, Depends, File, Request, UploadFile
from loguru import logger

from backend.app.api.dependencies import (
    get_processing_time,
    get_request_id,
    get_upload_use_case,
)
from backend.app.application.dtos.upload_response import UploadResponse
from backend.app.application.use_cases.upload_dataset import UploadDatasetUseCase
from backend.app.core.config import settings
from backend.app.core.rate_limit import limiter
from backend.app.core.responses import ApiResponse

router = APIRouter(tags=["Dataset"])


@router.post("/upload-test")
async def upload_test(request: Request):
    logger.info(
        "UPLOAD ROUTER REACHED",
        extra={
            "path": request.url.path,
            "method": request.method,
            "content_type": request.headers.get("content-type"),
            "content_length": request.headers.get("content-length")
        }
    )
    return {
        "ok": True,
        "message": "router reached"
    }


@router.post("/upload-debug")
async def upload_debug(request: Request):
    logger.info(
        "UPLOAD ROUTER REACHED",
        extra={
            "path": request.url.path,
            "method": request.method,
            "content_type": request.headers.get("content-type"),
            "content_length": request.headers.get("content-length")
        }
    )
    body = await request.body()
    logger.info(
        "UPLOAD DEBUG",
        extra={
            "content_length": request.headers.get("content-length"),
            "content_type": request.headers.get("content-type"),
            "first_100_bytes": body[:100],
        }
    )
    return {"received": True}


@router.post("/body-test")
async def body_test(request: Request):
    body = await request.body()
    logger.info(len(body))
    logger.info(request.headers.get("content-type"))
    logger.info(request.headers.get("content-length"))
    return {"received": len(body)}


@router.post("/multipart-test")
async def multipart_test(request: Request):
    form = await request.form()
    logger.info(form.keys())
    return {"keys": list(form.keys())}


async def pre_upload_logging(request: Request):
    logger.info("UPLOAD ROUTER ENTER")
    logger.info(request.headers)
    logger.info(request.headers.get("content-length"))
    logger.info(request.headers.get("content-type"))


@router.post("/upload", response_model=ApiResponse[UploadResponse], dependencies=[Depends(pre_upload_logging)])
@limiter.limit("10/minute")
async def upload_dataset(
    request: Request,
    file: UploadFile = File(...),
    use_case: UploadDatasetUseCase = Depends(get_upload_use_case),
    request_id: str = Depends(get_request_id),
    processing_time: float = Depends(get_processing_time),
) -> ApiResponse[UploadResponse]:
    """Uploads a CSV dataset for analysis."""
    logger.info(
        "UPLOAD ROUTER REACHED",
        extra={
            "path": request.url.path,
            "method": request.method,
            "content_type": request.headers.get("content-type"),
            "content_length": request.headers.get("content-length")
        }
    )

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

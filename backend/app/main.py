import os
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

import sentry_sdk
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from backend.app.api.routers import analytics, health, upload
from backend.app.core.config import settings
from backend.app.core.exceptions import ApplicationException, ValidationException
from backend.app.core.logging import setup_logging
from backend.app.core.middleware import (
    LoggingMiddleware,
    ProcessingTimeMiddleware,
    RequestIDMiddleware,
    SecurityHeadersMiddleware,
)
from backend.app.core.rate_limit import limiter
from backend.app.core.responses import ApiResponse, ErrorDetails


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Lifespan event handler for the FastAPI application."""
    setup_logging()

    sentry_dsn = os.environ.get("SENTRY_DSN")
    if sentry_dsn:
        sentry_sdk.init(
            dsn=sentry_dsn,
            traces_sample_rate=1.0,
            environment=settings.env,
            release=settings.version,
        )
        logger.info("Sentry initialized.")

    yield
    # Cleanup tasks can go here


def create_app() -> FastAPI:
    """Application factory for FastAPI."""
    app = FastAPI(
        title=settings.app_name,
        version=settings.version,
        lifespan=lifespan,
        docs_url=f"{settings.api_v1_prefix}/docs",
        openapi_url=f"{settings.api_v1_prefix}/openapi.json",
    )

    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)  # type: ignore

    # Middlewares
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(LoggingMiddleware)
    app.add_middleware(ProcessingTimeMiddleware)
    app.add_middleware(RequestIDMiddleware)
    app.add_middleware(SecurityHeadersMiddleware)

    # Routers
    app.include_router(health.router, prefix=settings.api_v1_prefix)
    app.include_router(upload.router, prefix=settings.api_v1_prefix)
    app.include_router(analytics.router, prefix=settings.api_v1_prefix)

    # Exception Handlers
    @app.exception_handler(ValidationException)
    async def validation_exception_handler(
        request: Request, exc: ValidationException
    ) -> JSONResponse:
        return _build_error_response(request, 422, "VALIDATION_ERROR", exc.message)

    @app.exception_handler(ApplicationException)
    async def application_exception_handler(
        request: Request, exc: ApplicationException
    ) -> JSONResponse:
        return _build_error_response(request, 400, "BUSINESS_ERROR", exc.message)

    @app.exception_handler(Exception)
    async def global_exception_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        return _build_error_response(
            request, 500, "INTERNAL_ERROR", "An unexpected error occurred."
        )

    return app


def _build_error_response(
    request: Request, status_code: int, code: str, details: str
) -> JSONResponse:
    request_id = getattr(request.state, "request_id", "unknown")
    processing_time = getattr(request.state, "processing_time", 0.0)

    response = ApiResponse[Any](
        success=False,
        message="Request failed",
        error=ErrorDetails(code=code, details=details),
        request_id=request_id,
        processing_time=processing_time,
        version=settings.version,
        status=status_code,
    )
    return JSONResponse(
        status_code=status_code, content=response.model_dump(mode="json")
    )


app = create_app()

import logging
import os
import time
import traceback
import uuid
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

import sentry_sdk
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from loguru import logger
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from starlette.types import ASGIApp, Receive, Scope, Send

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

    # Route Uvicorn logs to Loguru
    class InterceptHandler(logging.Handler):
        def emit(self, record: logging.LogRecord) -> None:
            try:
                level = logger.level(record.levelname).name
            except ValueError:
                level = str(record.levelno)
            frame, depth = logging.currentframe(), 2
            while frame and frame.f_code.co_filename == logging.__file__:
                frame = frame.f_back
                depth += 1
            logger.opt(depth=depth, exception=record.exc_info).log(
                level, record.getMessage()
            )

    logging.getLogger("uvicorn.access").handlers = [InterceptHandler()]
    logging.getLogger("uvicorn.access").propagate = False
    logging.getLogger("uvicorn.error").handlers = [InterceptHandler()]
    logging.getLogger("uvicorn.error").propagate = False

    logger.info("===== ASGI STARTUP =====")

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
    logger.info("===== ASGI SHUTDOWN =====")


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

    @app.exception_handler(RateLimitExceeded)
    async def custom_rate_limit_exceeded_handler(
        request: Request, exc: RateLimitExceeded
    ) -> Response:
        logger.warning(f"SlowAPI Rate limit exceeded for {request.url.path}")
        return _rate_limit_exceeded_handler(request, exc)

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

    @app.get(f"{settings.api_v1_prefix}/debug/ping")
    async def debug_ping(request: Request):
        return {
            "ok": True,
            "method": request.method,
            "path": request.url.path,
            "headers": dict(request.headers),
        }

    @app.post(f"{settings.api_v1_prefix}/debug/raw")
    async def debug_raw(request: Request):
        logger.info("RAW BODY RECEIVED")
        body = await request.body()
        logger.info(len(body))
        return {"received": len(body)}

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


class RawASGILoggingMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        request_id = str(uuid.uuid4())
        method = scope.get("method")
        path = scope.get("path")
        client = scope.get("client")

        headers = {}
        for k, v in scope.get("headers", []):
            try:
                headers[k.decode("utf-8")] = v.decode("utf-8")
            except Exception:
                pass

        start_time = time.time()
        logger.info(
            f"RAW ASGI REQUEST: req_id={request_id} method={method} path={path} "
            f"client={client} headers={headers} timestamp={start_time}"
        )

        status_code = 500

        async def custom_send(message: dict[str, Any]):
            nonlocal status_code
            if message["type"] == "http.response.start":
                status_code = message.get("status", 500)
            await send(message)

        try:
            await self.app(scope, receive, custom_send)
        except Exception as e:
            logger.error(
                f"RAW ASGI EXCEPTION: req_id={request_id} error={str(e)}\n"
                f"{traceback.format_exc()}"
            )
            raise
        finally:
            elapsed_time = time.time() - start_time
            logger.info(
                f"RAW ASGI RESPONSE: req_id={request_id} status={status_code} "
                f"elapsed_time={elapsed_time:.4f}s"
            )


app = create_app()
app = RawASGILoggingMiddleware(app)

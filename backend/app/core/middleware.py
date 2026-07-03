import time
import uuid
from typing import Awaitable, Callable

from fastapi import Request, Response
from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware


class RequestIDMiddleware(BaseHTTPMiddleware):
    """Injects a unique request ID into every request."""

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id
        
        # Extract or generate Correlation ID
        correlation_id = request.headers.get("X-Correlation-ID", request_id)
        request.state.correlation_id = correlation_id
        
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        response.headers["X-Correlation-ID"] = correlation_id
        return response


class ProcessingTimeMiddleware(BaseHTTPMiddleware):
    """Tracks and injects the request processing time."""

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        start_time = time.perf_counter()
        response = await call_next(request)
        process_time = time.perf_counter() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        request.state.processing_time = process_time
        return response


class LoggingMiddleware(BaseHTTPMiddleware):
    """Logs incoming requests and their outcomes."""

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        request_id = getattr(request.state, "request_id", "unknown")
        correlation_id = getattr(request.state, "correlation_id", "unknown")
        logger_context = logger.bind(
            request_id=request_id,
            correlation_id=correlation_id,
            method=request.method,
            path=request.url.path,
        )

        logger_context.info("Request started")
        try:
            response = await call_next(request)

            process_time = getattr(request.state, "processing_time", 0.0)
            logger_context.info(
                "Request completed",
                status_code=response.status_code,
                duration=f"{process_time:.4f}s",
            )
            return response
        except Exception as e:
            logger_context.exception(f"Request failed with unexpected error: {str(e)}")
            raise

class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Injects strict security headers including CSP."""
    
    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        response = await call_next(request)
        
        # CSP Configuration (can be overridden by env vars in a real setup)
        csp = (
            "default-src 'self'; "
            "script-src 'self'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data:; "
            "connect-src 'self'; "
            "object-src 'none'; "
            "frame-ancestors 'none'; "
            "base-uri 'self'"
        )
        
        response.headers["Content-Security-Policy"] = csp
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = (
            "max-age=31536000; includeSubDomains"
        )
        
        return response

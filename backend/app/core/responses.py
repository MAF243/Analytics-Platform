from datetime import datetime
from typing import Generic, Optional, TypeVar

from pydantic import BaseModel, Field

T = TypeVar("T")


class ErrorDetails(BaseModel):
    code: str
    details: Optional[str] = None


class ApiResponse(BaseModel, Generic[T]):
    """Standardized generic API response envelope."""

    success: bool
    message: str
    data: Optional[T] = None
    error: Optional[ErrorDetails] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    request_id: str
    processing_time: float
    version: str
    status: int

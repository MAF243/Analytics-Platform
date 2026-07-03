from datetime import datetime

from pydantic import BaseModel


class UploadResponse(BaseModel):
    """DTO for the upload response."""

    dataset_id: str
    filename: str
    size_bytes: int
    created_at: datetime

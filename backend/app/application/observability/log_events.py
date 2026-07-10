from dataclasses import asdict, dataclass
from typing import Any


@dataclass(slots=True, frozen=True, kw_only=True)
class LogEvent:
    event: str

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True, frozen=True, kw_only=True)
class UploadValidationCompletedLog(LogEvent):
    event: str = "upload.validation.completed"
    status: str
    filename: str
    extension: str
    encoding: str
    delimiter: str
    rows_detected: int
    column_count: int
    numeric_column_count: int
    upload_size_bytes: int
    client_content_type: str
    decision: str
    validation_result: str


@dataclass(slots=True, frozen=True, kw_only=True)
class UnexpectedMimeLog(LogEvent):
    event: str = "upload.mime.unexpected"
    expected_mime_types: list[str]
    received_mime: str
    filename: str
    extension: str
    decision: str


@dataclass(slots=True, frozen=True, kw_only=True)
class RequestCompletedLog(LogEvent):
    event: str = "request.completed"
    status_code: int
    duration: str


@dataclass(slots=True, frozen=True, kw_only=True)
class RequestFailedLog(LogEvent):
    event: str = "request.failed"
    error: str


@dataclass(slots=True, frozen=True, kw_only=True)
class RequestStartedLog(LogEvent):
    event: str = "request.started"
    method: str
    path: str

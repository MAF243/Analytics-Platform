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


@dataclass(slots=True, frozen=True, kw_only=True)
class AnalysisJobLifecycleLog(LogEvent):
    dataset_id: str
    job_id: str


@dataclass(slots=True, frozen=True, kw_only=True)
class AnalysisJobCreatedLog(AnalysisJobLifecycleLog):
    event: str = "analysis.job.created"


@dataclass(slots=True, frozen=True, kw_only=True)
class AnalysisJobStartedLog(AnalysisJobLifecycleLog):
    event: str = "analysis.job.started"


@dataclass(slots=True, frozen=True, kw_only=True)
class AnalysisStageStartedLog(AnalysisJobLifecycleLog):
    event: str = "analysis.stage.started"
    stage: str


@dataclass(slots=True, frozen=True, kw_only=True)
class AnalysisStageCompletedLog(AnalysisJobLifecycleLog):
    event: str = "analysis.stage.completed"
    stage: str
    progress: int
    steps_completed: int
    total_steps: int
    estimated_remaining_seconds: float | None


@dataclass(slots=True, frozen=True, kw_only=True)
class AnalysisJobCompletedLog(AnalysisJobLifecycleLog):
    event: str = "analysis.job.completed"
    total_steps: int


@dataclass(slots=True, frozen=True, kw_only=True)
class AnalysisJobFailedLog(AnalysisJobLifecycleLog):
    event: str = "analysis.job.failed"
    error_message: str
    failed_at_step: str
    progress: int


@dataclass(slots=True, frozen=True, kw_only=True)
class AnalysisJobCancelledLog(AnalysisJobLifecycleLog):
    event: str = "analysis.job.cancelled"
    cancelled_at_step: str


@dataclass(slots=True, frozen=True, kw_only=True)
class AnalysisJobCleanedLog(AnalysisJobLifecycleLog):
    event: str = "analysis.job.cleaned"

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional


class AnalysisJobStatus(str, Enum):
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class AnalysisStage(str, Enum):
    VALIDATION = "validation"
    CLEANING = "cleaning"
    PROFILING = "profiling"
    FEATURE_ENGINEERING = "feature_engineering"
    SCALING = "scaling"
    PCA = "pca"
    ELBOW = "elbow"
    CLUSTERING = "clustering"
    SUMMARY = "summary"
    DASHBOARD = "dashboard"


@dataclass
class AnalysisJob:
    job_id: str
    dataset_id: str
    status: AnalysisJobStatus
    progress: int
    current_step: Optional[str]
    steps_completed: int
    total_steps: int
    started_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    estimated_remaining_seconds: Optional[float] = None
    error_message: Optional[str] = None
    is_cancelled: bool = False

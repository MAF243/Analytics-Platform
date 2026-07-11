from datetime import datetime

from backend.app.domain.entities.analysis_job import AnalysisJob, AnalysisJobStatus


class JobLifecyclePolicy:
    """Manages TTL and cleanup decisions for Analysis Jobs."""

    COMPLETED_TTL_SECONDS = 600  # 10 minutes
    FAILED_TTL_SECONDS = 1800  # 30 minutes
    CANCELLED_TTL_SECONDS = 1800  # 30 minutes

    @classmethod
    def is_expired(cls, job: AnalysisJob) -> bool:
        """Determines if a job should be removed based on TTL."""
        if job.status in (AnalysisJobStatus.QUEUED, AnalysisJobStatus.RUNNING):
            return False

        if not job.updated_at:
            return False

        elapsed = (datetime.utcnow() - job.updated_at).total_seconds()

        if (
            job.status == AnalysisJobStatus.COMPLETED
            and elapsed > cls.COMPLETED_TTL_SECONDS
        ):
            return True
        if job.status == AnalysisJobStatus.FAILED and elapsed > cls.FAILED_TTL_SECONDS:
            return True
        if (
            job.status == AnalysisJobStatus.CANCELLED
            and elapsed > cls.CANCELLED_TTL_SECONDS
        ):
            return True

        return False

import uuid
from datetime import datetime

from backend.app.domain.entities.analysis_job import (
    AnalysisJob,
    AnalysisJobStatus,
)


class AnalysisJobFactory:
    """Factory for creating AnalysisJob instances safely."""

    @staticmethod
    def create_new(dataset_id: str, total_steps: int) -> AnalysisJob:
        return AnalysisJob(
            job_id=str(uuid.uuid4()),
            dataset_id=dataset_id,
            status=AnalysisJobStatus.QUEUED,
            progress=0,
            current_step=None,
            steps_completed=0,
            total_steps=total_steps,
            updated_at=datetime.utcnow(),
            is_cancelled=False,
        )

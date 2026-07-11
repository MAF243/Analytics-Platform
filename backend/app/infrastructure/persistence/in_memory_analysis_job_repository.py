from typing import Dict, Optional

from backend.app.application.ports.analysis_job_repository import AnalysisJobRepository
from backend.app.domain.entities.analysis_job import AnalysisJob, AnalysisJobStatus
from backend.app.domain.policies.job_lifecycle_policy import JobLifecyclePolicy


class InMemoryAnalysisJobRepository(AnalysisJobRepository):
    """In-memory adapter for tracking analysis jobs (singleton dictionary)."""

    def __init__(self) -> None:
        self._store: Dict[str, AnalysisJob] = {}

    def save(self, job: AnalysisJob) -> None:
        self.cleanup_expired()
        self._store[job.job_id] = job

    def get_by_job_id(self, job_id: str) -> Optional[AnalysisJob]:
        self.cleanup_expired()
        job = self._store.get(job_id)
        if job and JobLifecyclePolicy.is_expired(job):
            del self._store[job_id]
            return None
        return job

    def get_latest_for_dataset(self, dataset_id: str) -> Optional[AnalysisJob]:
        self.cleanup_expired()

        # Filter jobs for this dataset
        dataset_jobs = [
            job for job in self._store.values() if job.dataset_id == dataset_id
        ]

        if not dataset_jobs:
            return None

        # Sort by updated_at descending (latest first)
        dataset_jobs.sort(
            key=lambda j: j.updated_at.timestamp() if j.updated_at else 0.0,
            reverse=True,
        )
        return dataset_jobs[0]

    def cancel(self, job_id: str) -> None:
        job = self.get_by_job_id(job_id)
        if job and job.status in (AnalysisJobStatus.QUEUED, AnalysisJobStatus.RUNNING):
            job.status = AnalysisJobStatus.CANCELLED
            job.is_cancelled = True
            self.save(job)

    def cleanup_expired(self) -> None:
        """Removes expired jobs according to the lifecycle policy."""
        expired_keys = [
            k for k, v in self._store.items() if JobLifecyclePolicy.is_expired(v)
        ]
        for k in expired_keys:
            del self._store[k]

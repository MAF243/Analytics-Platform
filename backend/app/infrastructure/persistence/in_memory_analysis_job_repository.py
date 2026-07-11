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

    def find(self, job_id: str) -> Optional[AnalysisJob]:
        self.cleanup_expired()
        job = self._store.get(job_id)
        if job and JobLifecyclePolicy.is_expired(job):
            del self._store[job_id]
            return None
        return job

    def find_active_job(self, dataset_id: str) -> Optional[AnalysisJob]:
        active_statuses = (AnalysisJobStatus.QUEUED, AnalysisJobStatus.RUNNING)
        jobs = self.find_jobs(dataset_id, limit=1)
        if jobs and jobs[0].status in active_statuses:
            return jobs[0]
        return None

    def find_latest_job(self, dataset_id: str) -> Optional[AnalysisJob]:
        jobs = self.find_jobs(dataset_id, limit=1)
        return jobs[0] if jobs else None

    def find_jobs(
        self,
        dataset_id: str,
        status: Optional[AnalysisJobStatus] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        newest_first: bool = True,
    ) -> list[AnalysisJob]:
        self.cleanup_expired()

        # Filter
        jobs = [job for job in self._store.values() if job.dataset_id == dataset_id]

        if status:
            jobs = [job for job in jobs if job.status == status]

        # Sort
        jobs.sort(
            key=lambda j: j.updated_at.timestamp() if j.updated_at else 0.0,
            reverse=newest_first,
        )

        # Pagination
        start = offset or 0
        end = start + limit if limit else len(jobs)
        return jobs[start:end]

    def cancel(self, job_id: str) -> None:
        job = self.find(job_id)
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

from abc import ABC, abstractmethod
from typing import List, Optional

from backend.app.domain.entities.analysis_job import AnalysisJob, AnalysisJobStatus


class AnalysisJobRepository(ABC):
    """Abstract interface for managing AnalysisJob persistence."""

    @abstractmethod
    def save(self, job: AnalysisJob) -> None:
        """Saves or updates the analysis job."""
        pass

    @abstractmethod
    def find(self, job_id: str) -> Optional[AnalysisJob]:
        """Retrieves an analysis job by its specific ID."""
        pass

    @abstractmethod
    def find_active_job(self, dataset_id: str) -> Optional[AnalysisJob]:
        """Retrieves the currently running or queued job for a dataset, if any."""
        pass

    @abstractmethod
    def find_latest_job(self, dataset_id: str) -> Optional[AnalysisJob]:
        """Retrieves the most recently updated job for a dataset."""
        pass

    @abstractmethod
    def find_jobs(
        self,
        dataset_id: str,
        status: Optional[AnalysisJobStatus] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        newest_first: bool = True,
    ) -> List[AnalysisJob]:
        """Retrieves a list of jobs matching the query criteria."""
        pass

    @abstractmethod
    def cancel(self, job_id: str) -> None:
        """Marks a job as cancelled."""
        pass

    @abstractmethod
    def cleanup_expired(self) -> None:
        """Removes expired jobs according to the lifecycle policy."""
        pass

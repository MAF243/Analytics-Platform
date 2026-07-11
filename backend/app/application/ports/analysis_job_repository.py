from abc import ABC, abstractmethod
from typing import Optional

from backend.app.domain.entities.analysis_job import AnalysisJob


class AnalysisJobRepository(ABC):
    """Abstract interface for managing AnalysisJob persistence."""

    @abstractmethod
    def save(self, job: AnalysisJob) -> None:
        """Saves or updates the analysis job."""
        pass

    @abstractmethod
    def get_by_job_id(self, job_id: str) -> Optional[AnalysisJob]:
        """Retrieves an analysis job by its specific ID."""
        pass

    @abstractmethod
    def get_latest_for_dataset(self, dataset_id: str) -> Optional[AnalysisJob]:
        """Retrieves the most recently created or active job for a dataset."""
        pass

    @abstractmethod
    def cancel(self, job_id: str) -> None:
        """Marks a job as cancelled."""
        pass

    @abstractmethod
    def cleanup_expired(self) -> None:
        """Removes expired jobs according to the lifecycle policy."""
        pass

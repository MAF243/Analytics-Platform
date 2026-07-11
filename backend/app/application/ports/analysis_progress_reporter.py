from abc import ABC, abstractmethod

from backend.app.domain.entities.analysis_job import AnalysisStage


class AnalysisProgressReporter(ABC):
    """Abstract interface for reporting progress within the analytics pipeline."""

    @abstractmethod
    def report_stage_started(self, stage: AnalysisStage) -> None:
        """Called when a new stage begins."""
        pass

    @abstractmethod
    def report_stage_completed(self, stage: AnalysisStage) -> None:
        """Called when a stage is fully completed."""
        pass

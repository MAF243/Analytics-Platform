import time
from typing import Optional

from backend.app.domain.entities.analysis_job import AnalysisStage


class ProgressPolicy:
    """Handles progress and ETA calculation for analysis jobs."""

    # Default order of stages, though we just care about total count here
    # Since the prompt said "Use a list of stages", we'll track the pipeline length
    STAGES = [
        AnalysisStage.VALIDATION,
        AnalysisStage.CLEANING,
        AnalysisStage.PROFILING,
        AnalysisStage.FEATURE_ENGINEERING,
        AnalysisStage.SCALING,
        AnalysisStage.PCA,
        AnalysisStage.ELBOW,
        AnalysisStage.CLUSTERING,
        AnalysisStage.SUMMARY,
        AnalysisStage.DASHBOARD,
    ]

    @classmethod
    def get_total_steps(cls) -> int:
        return len(cls.STAGES)

    @staticmethod
    def calculate_progress(steps_completed: int, total_steps: int) -> int:
        """Calculates percentage complete."""
        if total_steps <= 0:
            return 0
        progress = int((steps_completed / total_steps) * 100)
        return min(progress, 100)

    @staticmethod
    def calculate_eta(
        start_time: float, steps_completed: int, total_steps: int
    ) -> Optional[float]:
        """Estimates remaining seconds."""
        if steps_completed == 0 or total_steps <= steps_completed:
            return None

        elapsed_seconds = time.perf_counter() - start_time
        time_per_step = elapsed_seconds / steps_completed
        remaining_steps = total_steps - steps_completed
        return round(time_per_step * remaining_steps, 2)

import time
from datetime import datetime
from typing import Optional

from loguru import logger

from backend.app.application.observability.log_events import (
    AnalysisJobCancelledLog,
    AnalysisJobCompletedLog,
    AnalysisJobCreatedLog,
    AnalysisJobFailedLog,
    AnalysisJobStartedLog,
    AnalysisStageCompletedLog,
    AnalysisStageStartedLog,
)
from backend.app.application.ports.analysis_job_repository import AnalysisJobRepository
from backend.app.application.ports.analysis_progress_reporter import (
    AnalysisProgressReporter,
)
from backend.app.application.use_cases.run_analytics import RunAnalyticsUseCase
from backend.app.core.exceptions import ApplicationException
from backend.app.domain.entities.analysis_job import (
    AnalysisJob,
    AnalysisJobStatus,
    AnalysisStage,
)
from backend.app.domain.factories.analysis_job_factory import AnalysisJobFactory
from backend.app.domain.policies.progress_policy import ProgressPolicy


class JobCancelledException(ApplicationException):
    pass


class AnalysisExecutor(AnalysisProgressReporter):
    """
    Orchestrates the background execution of the analytics pipeline,
    manages status persistence, and emits structured lifecycle logs.
    """

    def __init__(
        self,
        use_case: RunAnalyticsUseCase,
        status_repository: AnalysisJobRepository,
    ):
        self.use_case = use_case
        self.status_repository = status_repository

        # State per execution
        self._current_dataset_id: Optional[str] = None
        self._current_job_id: Optional[str] = None
        self._start_time: float = 0.0

    def initialize_job(self, dataset_id: str) -> AnalysisJob:
        """Called synchronously by the router to queue the analysis."""
        total_steps = ProgressPolicy.get_total_steps()
        job = AnalysisJobFactory.create_new(dataset_id, total_steps)
        self.status_repository.save(job)

        log = AnalysisJobCreatedLog(
            dataset_id=dataset_id,
            job_id=job.job_id,
        )
        logger.bind(**log.as_dict(), job_id=job.job_id).info("Analysis job created")

        return job

    def execute_pipeline(
        self, dataset_id: str, job_id: str, request_id: str, correlation_id: str
    ) -> None:
        """Executed in the background."""
        self._current_dataset_id = dataset_id
        self._current_job_id = job_id
        self._start_time = time.perf_counter()

        # Restore contextual logger for the background thread
        with logger.contextualize(
            request_id=request_id,
            correlation_id=correlation_id,
            start_time=self._start_time,
            job_id=self._current_job_id,
        ):
            job = self.status_repository.get_by_job_id(job_id)
            if not job:
                return

            if job.is_cancelled:
                return

            job.status = AnalysisJobStatus.RUNNING
            job.started_at = datetime.utcnow()
            job.updated_at = datetime.utcnow()
            self.status_repository.save(job)

            start_log = AnalysisJobStartedLog(
                dataset_id=dataset_id,
                job_id=job_id,
            )
            logger.bind(**start_log.as_dict()).info("Analysis job started")

            try:
                # Execute the use case, passing self as the progress reporter
                self.use_case.execute(dataset_id, reporter=self)

                # Fetch latest to ensure we don't overwrite if cancelled concurrently
                job = self.status_repository.get_by_job_id(job_id)
                if not job or job.is_cancelled:
                    raise JobCancelledException("Job was cancelled during execution")

                # Mark completed
                job.status = AnalysisJobStatus.COMPLETED
                job.progress = 100
                job.finished_at = datetime.utcnow()
                job.updated_at = datetime.utcnow()
                job.estimated_remaining_seconds = 0.0
                self.status_repository.save(job)

                completed_log = AnalysisJobCompletedLog(
                    dataset_id=dataset_id,
                    job_id=job_id,
                    total_steps=job.total_steps,
                )
                logger.bind(**completed_log.as_dict()).info(
                    "Analysis job completed successfully"
                )

            except JobCancelledException as e:
                # Refresh job from DB to mark it
                job = self.status_repository.get_by_job_id(job_id)
                if job:
                    job.status = AnalysisJobStatus.CANCELLED
                    job.finished_at = datetime.utcnow()
                    job.updated_at = datetime.utcnow()
                    self.status_repository.save(job)

                    cancel_log = AnalysisJobCancelledLog(
                        dataset_id=dataset_id,
                        job_id=job_id,
                        cancelled_at_step=job.current_step or "unknown",
                    )
                    logger.bind(**cancel_log.as_dict()).info(
                        f"Analysis job cancelled: {str(e)}"
                    )

            except Exception as e:
                # Mark failed
                job = self.status_repository.get_by_job_id(job_id)
                if job:
                    job.status = AnalysisJobStatus.FAILED
                    job.error_message = str(e)
                    job.finished_at = datetime.utcnow()
                    job.updated_at = datetime.utcnow()
                    self.status_repository.save(job)

                    failed_log = AnalysisJobFailedLog(
                        dataset_id=dataset_id,
                        job_id=job_id,
                        error_message=str(e),
                        failed_at_step=job.current_step or "unknown",
                        progress=job.progress,
                    )
                    logger.bind(**failed_log.as_dict()).exception(
                        f"Analysis job failed: {str(e)}"
                    )

    def _check_cancellation(self) -> AnalysisJob:
        job = self.status_repository.get_by_job_id(self._current_job_id)  # type: ignore
        if not job:
            raise ApplicationException("Job not found")
        if job.is_cancelled:
            raise JobCancelledException("Job has been cancelled")
        return job

    def report_stage_started(self, stage: AnalysisStage) -> None:
        """Called by the RunAnalyticsUseCase when a stage begins."""
        job = self._check_cancellation()
        job.current_step = stage.value
        job.updated_at = datetime.utcnow()
        self.status_repository.save(job)

        log = AnalysisStageStartedLog(
            dataset_id=self._current_dataset_id or "unknown",
            job_id=self._current_job_id or "unknown",
            stage=stage.value,
        )
        logger.bind(**log.as_dict()).info(f"Analysis stage started: {stage.value}")

    def report_stage_completed(self, stage: AnalysisStage) -> None:
        """Called by the RunAnalyticsUseCase when a stage completes."""
        job = self._check_cancellation()

        job.steps_completed += 1
        job.progress = ProgressPolicy.calculate_progress(
            job.steps_completed, job.total_steps
        )
        job.estimated_remaining_seconds = ProgressPolicy.calculate_eta(
            self._start_time, job.steps_completed, job.total_steps
        )
        job.updated_at = datetime.utcnow()
        self.status_repository.save(job)

        log = AnalysisStageCompletedLog(
            dataset_id=self._current_dataset_id or "unknown",
            job_id=self._current_job_id or "unknown",
            stage=stage.value,
            progress=job.progress,
            steps_completed=job.steps_completed,
            total_steps=job.total_steps,
            estimated_remaining_seconds=job.estimated_remaining_seconds,
        )
        logger.bind(**log.as_dict()).info(f"Analysis stage completed: {stage.value}")

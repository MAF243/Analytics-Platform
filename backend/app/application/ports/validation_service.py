from abc import ABC, abstractmethod
from typing import BinaryIO

from backend.app.application.dtos.validation_metadata import ValidationMetadata


class ValidationService(ABC):
    """Abstract interface for dataset validation orchestration."""

    @abstractmethod
    def validate_upload(
        self, file_stream: BinaryIO, filename: str, content_type: str
    ) -> ValidationMetadata:
        """
        Validates an uploaded file's structure, size, mime type, and integrity.
        Raises ValidationException if validation fails.
        Returns a dictionary containing validation metadata (e.g., encoding, delimiter, rows_detected).
        """
        pass

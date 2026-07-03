from abc import ABC, abstractmethod
from typing import BinaryIO


class ValidationService(ABC):
    """Abstract interface for dataset validation orchestration."""

    @abstractmethod
    def validate_upload(
        self, file_stream: BinaryIO, filename: str, content_type: str
    ) -> None:
        """
        Validates an uploaded file's structure, size, mime type, and integrity.
        Raises ValidationException if validation fails.
        """
        pass

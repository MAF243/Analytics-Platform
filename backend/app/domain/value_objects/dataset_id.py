import uuid
from dataclasses import dataclass

from backend.app.core.exceptions import ValidationException


@dataclass(frozen=True)
class DatasetId:
    """Value object representing a valid Dataset UUID."""

    value: str

    def __post_init__(self) -> None:
        if not self._is_valid_uuid(self.value):
            raise ValidationException(f"Invalid dataset ID format: {self.value}")

    @staticmethod
    def _is_valid_uuid(val: str) -> bool:
        try:
            uuid.UUID(str(val))
            return True
        except ValueError:
            return False

    def __str__(self) -> str:
        return self.value

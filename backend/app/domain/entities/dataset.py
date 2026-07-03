from dataclasses import dataclass, field
from datetime import datetime

from backend.app.domain.value_objects.dataset_id import DatasetId


@dataclass
class Dataset:
    """Core domain entity representing an uploaded dataset."""

    id: DatasetId
    filename: str
    size_bytes: int
    created_at: datetime = field(default_factory=datetime.utcnow)

    @property
    def is_empty(self) -> bool:
        return self.size_bytes == 0

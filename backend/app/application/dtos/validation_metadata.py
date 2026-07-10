from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ValidationMetadata:
    """Immutable DTO representing the outcome and metadata of a validation."""

    filename: str = ""
    extension: str = ""
    encoding: str = ""
    delimiter: str = ""
    rows_detected: int = 0
    column_count: int = 0
    header_count: int = 0
    numeric_column_count: int = 0
    file_size_bytes: int = 0
    csv_valid: bool = False

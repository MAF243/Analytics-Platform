import csv
import io
from abc import ABC, abstractmethod
from typing import BinaryIO

from backend.app.core.constants import (
    MAX_UPLOAD_SIZE_BYTES,
    MIN_NUMERIC_COLUMNS,
    SUPPORTED_EXTENSIONS,
    SUPPORTED_MIME_TYPES,
)
from backend.app.core.exceptions import ValidationException
from backend.app.domain.interfaces.validation_service import ValidationService


class BaseValidator(ABC):
    @abstractmethod
    def validate(self, file_stream: BinaryIO, filename: str, content_type: str) -> None:
        pass


class FileTypeValidator(BaseValidator):
    def validate(self, file_stream: BinaryIO, filename: str, content_type: str) -> None:
        if content_type not in SUPPORTED_MIME_TYPES:
            raise ValidationException(f"Unsupported MIME type: {content_type}")

        ext = filename[filename.rfind(".") :].lower() if "." in filename else ""
        if ext not in SUPPORTED_EXTENSIONS:
            raise ValidationException(f"Unsupported file extension: {ext}")


class FileSizeValidator(BaseValidator):
    def validate(self, file_stream: BinaryIO, filename: str, content_type: str) -> None:
        file_stream.seek(0, 2)  # Seek to end
        size = file_stream.tell()
        file_stream.seek(0)  # Reset

        if size == 0:
            raise ValidationException("The uploaded file is empty.")

        if size > MAX_UPLOAD_SIZE_BYTES:
            raise ValidationException(
                f"File size exceeds the {MAX_UPLOAD_SIZE_BYTES / (1024*1024)} MB limit."
            )


class EncodingValidator(BaseValidator):
    def validate(self, file_stream: BinaryIO, filename: str, content_type: str) -> None:
        # Simplistic check for valid utf-8 decoding on the first chunk
        chunk = file_stream.read(1024)
        file_stream.seek(0)
        try:
            chunk.decode("utf-8")
        except UnicodeDecodeError:
            raise ValidationException("File must be valid UTF-8 encoded.")


class CSVStructureValidator(BaseValidator):
    def validate(self, file_stream: BinaryIO, filename: str, content_type: str) -> None:
        file_stream.seek(0)
        try:
            text_stream = io.TextIOWrapper(file_stream, encoding="utf-8")
            reader = csv.reader(text_stream)
            try:
                header = next(reader)
            except StopIteration:
                raise ValidationException("CSV file is completely empty.")

            if not header or len(header) == 0:
                raise ValidationException("CSV file has an empty header row.")

            num_cols = len(header)
            row_count = 0

            for row in reader:
                row_count += 1
                if len(row) != num_cols:
                    raise ValidationException(
                        f"Inconsistent column count at row {row_count + 1}."
                    )

            if row_count == 0:
                raise ValidationException("CSV file contains no data rows.")

        except csv.Error as e:
            raise ValidationException(f"Malformed CSV syntax: {str(e)}")
        finally:
            text_stream.detach()
            file_stream.seek(0)


class HeaderValidator(BaseValidator):
    def validate(self, file_stream: BinaryIO, filename: str, content_type: str) -> None:
        file_stream.seek(0)
        text_stream = io.TextIOWrapper(file_stream, encoding="utf-8")
        reader = csv.reader(text_stream)

        try:
            header = next(reader)
        except StopIteration:
            text_stream.detach()
            file_stream.seek(0)
            return  # Will be caught by CSVStructureValidator

        seen_headers = set()
        for col in header:
            if not col or not col.strip():
                text_stream.detach()
                file_stream.seek(0)
                raise ValidationException(
                    "CSV file contains blank or whitespace-only header names."
                )
            if col in seen_headers:
                text_stream.detach()
                file_stream.seek(0)
                raise ValidationException(
                    f"CSV file contains duplicate header: '{col}'."
                )
            seen_headers.add(col)

        text_stream.detach()
        file_stream.seek(0)


class NumericColumnValidator(BaseValidator):
    def validate(self, file_stream: BinaryIO, filename: str, content_type: str) -> None:
        file_stream.seek(0)
        text_stream = io.TextIOWrapper(file_stream, encoding="utf-8")
        reader = csv.reader(text_stream)

        try:
            next(reader)  # Skip header
            first_row = next(reader)
        except StopIteration:
            text_stream.detach()
            file_stream.seek(0)
            return

        numeric_count = 0
        for val in first_row:
            val = val.strip()
            if not val:
                continue
            try:
                float(val)
                numeric_count += 1
            except ValueError:
                pass

        if numeric_count < MIN_NUMERIC_COLUMNS:
            text_stream.detach()
            file_stream.seek(0)
            raise ValidationException(
                f"Dataset must contain >= {MIN_NUMERIC_COLUMNS} numeric cols."
            )

        text_stream.detach()
        file_stream.seek(0)


class CSVValidationService(ValidationService):
    """Orchestrates specific validators to ensure file integrity."""

    def __init__(self) -> None:
        self.validators = [
            FileTypeValidator(),
            FileSizeValidator(),
            EncodingValidator(),
            CSVStructureValidator(),
            HeaderValidator(),
            NumericColumnValidator(),
        ]

    def validate_upload(
        self, file_stream: BinaryIO, filename: str, content_type: str
    ) -> None:
        for validator in self.validators:
            validator.validate(file_stream, filename, content_type)

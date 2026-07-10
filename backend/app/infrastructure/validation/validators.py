import csv
import io
from abc import ABC, abstractmethod
from dataclasses import replace
from typing import BinaryIO

from backend.app.application.dtos.validation_metadata import ValidationMetadata
from backend.app.application.ports.validation_service import ValidationService
from backend.app.core.constants import (
    MAX_UPLOAD_SIZE_BYTES,
    MIN_NUMERIC_COLUMNS,
    SUPPORTED_EXTENSIONS,
)
from backend.app.core.exceptions import ValidationException


class BaseValidator(ABC):
    @abstractmethod
    def validate(
        self,
        file_stream: BinaryIO,
        filename: str,
        content_type: str,
        result: ValidationMetadata,
    ) -> ValidationMetadata:
        pass


class FileExtensionValidator(BaseValidator):
    def validate(
        self,
        file_stream: BinaryIO,
        filename: str,
        content_type: str,
        result: ValidationMetadata,
    ) -> ValidationMetadata:
        ext = filename[filename.rfind(".") :].lower() if "." in filename else ""
        if ext not in SUPPORTED_EXTENSIONS:
            raise ValidationException(f"Unsupported file extension: {ext}")
        return replace(result, extension=ext, filename=filename)


class FileSizeValidator(BaseValidator):
    def validate(
        self,
        file_stream: BinaryIO,
        filename: str,
        content_type: str,
        result: ValidationMetadata,
    ) -> ValidationMetadata:
        file_stream.seek(0, 2)  # Seek to end
        size = file_stream.tell()
        file_stream.seek(0)  # Reset

        if size == 0:
            raise ValidationException("The uploaded file is empty.")

        if size > MAX_UPLOAD_SIZE_BYTES:
            raise ValidationException(
                f"File size exceeds the {MAX_UPLOAD_SIZE_BYTES / (1024*1024)} MB limit."
            )
        return replace(result, file_size_bytes=size)


class EncodingValidator(BaseValidator):
    def validate(
        self,
        file_stream: BinaryIO,
        filename: str,
        content_type: str,
        result: ValidationMetadata,
    ) -> ValidationMetadata:
        # Simplistic check for valid utf-8 decoding on the first chunk
        chunk = file_stream.read(1024)
        file_stream.seek(0)
        try:
            chunk.decode("utf-8")
        except UnicodeDecodeError:
            raise ValidationException("File must be valid UTF-8 encoded.")
        return replace(result, encoding="utf-8")


class CSVStructureValidator(BaseValidator):
    def validate(
        self,
        file_stream: BinaryIO,
        filename: str,
        content_type: str,
        result: ValidationMetadata,
    ) -> ValidationMetadata:
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

            return replace(
                result,
                csv_valid=True,
                rows_detected=row_count,
                column_count=num_cols,
                delimiter=(
                    reader.dialect.delimiter
                    if hasattr(reader, "dialect")
                    and hasattr(reader.dialect, "delimiter")
                    else ","
                ),
            )

        except csv.Error as e:
            raise ValidationException(f"Malformed CSV syntax: {str(e)}")
        finally:
            text_stream.detach()
            file_stream.seek(0)


class HeaderValidator(BaseValidator):
    def validate(
        self,
        file_stream: BinaryIO,
        filename: str,
        content_type: str,
        result: ValidationMetadata,
    ) -> ValidationMetadata:
        file_stream.seek(0)
        text_stream = io.TextIOWrapper(file_stream, encoding="utf-8")
        reader = csv.reader(text_stream)

        try:
            header = next(reader)
        except StopIteration:
            text_stream.detach()
            file_stream.seek(0)
            return result  # Will be caught by CSVStructureValidator

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
        return replace(result, header_count=len(seen_headers))


class NumericColumnValidator(BaseValidator):
    def validate(
        self,
        file_stream: BinaryIO,
        filename: str,
        content_type: str,
        result: ValidationMetadata,
    ) -> ValidationMetadata:
        file_stream.seek(0)
        text_stream = io.TextIOWrapper(file_stream, encoding="utf-8")
        reader = csv.reader(text_stream)

        try:
            next(reader)  # Skip header
            first_row = next(reader)
        except StopIteration:
            text_stream.detach()
            file_stream.seek(0)
            return result

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
        return replace(result, numeric_column_count=numeric_count)


class ValidationPipeline:
    """Orchestrates the execution of a series of validators."""

    def __init__(self) -> None:
        self.validators: list[BaseValidator] = [
            FileExtensionValidator(),
            FileSizeValidator(),
            EncodingValidator(),
            CSVStructureValidator(),
            HeaderValidator(),
            NumericColumnValidator(),
        ]

    def execute(
        self, file_stream: BinaryIO, filename: str, content_type: str
    ) -> ValidationMetadata:
        metadata = ValidationMetadata()
        for validator in self.validators:
            metadata = validator.validate(file_stream, filename, content_type, metadata)
        return metadata


class CSVValidationService(ValidationService):
    """Provides the application port implementation for CSV validation."""

    def __init__(self) -> None:
        self.pipeline = ValidationPipeline()

    def validate_upload(
        self, file_stream: BinaryIO, filename: str, content_type: str
    ) -> ValidationMetadata:
        return self.pipeline.execute(file_stream, filename, content_type)

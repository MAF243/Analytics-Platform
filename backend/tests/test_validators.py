import io

import pytest

from backend.app.core.exceptions import ValidationException
from backend.app.infrastructure.validation.validators import (
    CSVStructureValidator,
    HeaderValidator,
    NumericColumnValidator,
)


def create_stream(content: str) -> io.BytesIO:
    return io.BytesIO(content.encode("utf-8"))


def test_csv_structure_validator_success() -> None:
    validator = CSVStructureValidator()
    stream = create_stream("a,b,c\n1,2,3\n4,5,6")
    validator.validate(stream, "test.csv", "text/csv")


def test_csv_structure_validator_empty() -> None:
    validator = CSVStructureValidator()
    stream = create_stream("")
    with pytest.raises(ValidationException, match="completely empty"):
        validator.validate(stream, "test.csv", "text/csv")


def test_csv_structure_validator_empty_header() -> None:
    validator = CSVStructureValidator()
    stream = create_stream("\n1,2,3")
    with pytest.raises(ValidationException, match="empty header row"):
        validator.validate(stream, "test.csv", "text/csv")


def test_csv_structure_validator_inconsistent_cols() -> None:
    validator = CSVStructureValidator()
    stream = create_stream("a,b\n1,2,3")
    with pytest.raises(ValidationException, match="Inconsistent column count"):
        validator.validate(stream, "test.csv", "text/csv")


def test_csv_structure_validator_no_data() -> None:
    validator = CSVStructureValidator()
    stream = create_stream("a,b\n")
    with pytest.raises(ValidationException, match="no data rows"):
        validator.validate(stream, "test.csv", "text/csv")


def test_header_validator_success() -> None:
    validator = HeaderValidator()
    stream = create_stream("col1,col2,col3\n1,2,3")
    validator.validate(stream, "test.csv", "text/csv")


def test_header_validator_duplicate() -> None:
    validator = HeaderValidator()
    stream = create_stream("col1,col1,col3\n1,2,3")
    with pytest.raises(ValidationException, match="duplicate header"):
        validator.validate(stream, "test.csv", "text/csv")


def test_header_validator_blank() -> None:
    validator = HeaderValidator()
    stream = create_stream("col1, ,col3\n1,2,3")
    with pytest.raises(ValidationException, match="blank or whitespace-only"):
        validator.validate(stream, "test.csv", "text/csv")


def test_numeric_column_validator_success() -> None:
    validator = NumericColumnValidator()
    stream = create_stream("id,age,score\nxyz,25,99.5")
    validator.validate(stream, "test.csv", "text/csv")


def test_numeric_column_validator_insufficient() -> None:
    validator = NumericColumnValidator()
    stream = create_stream("id,name,score\nxyz,john,99.5")
    with pytest.raises(ValidationException, match=">= 2 numeric cols"):
        validator.validate(stream, "test.csv", "text/csv")

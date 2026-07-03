class ApplicationException(Exception):
    """Base exception for all application-level errors."""

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class ValidationException(ApplicationException):
    """Raised when input data validation fails."""

    pass


class BusinessException(ApplicationException):
    """Raised when business rules are violated."""

    pass


class StorageException(ApplicationException):
    """Raised when storage operations fail."""

    pass


class InfrastructureException(ApplicationException):
    """Raised when infrastructure dependencies (e.g., file system, APIs) fail."""

    pass

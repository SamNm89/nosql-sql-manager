"""Custom exceptions for the banking application."""

class BankingAppError(Exception):
    """Base exception for banking application."""
    def __init__(self, message: str, error_code: str = None):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)

class DatabaseError(BankingAppError):
    """Database-related errors."""
    def __init__(self, message: str, original_error: Exception = None):
        self.original_error = original_error
        super().__init__(message, "DB_ERROR")

class ValidationError(BankingAppError):
    """Data validation errors."""
    def __init__(self, message: str, field: str = None):
        self.field = field
        super().__init__(message, "VALIDATION_ERROR")

class ClientNotFoundError(BankingAppError):
    """Client not found error."""
    def __init__(self, client_id: int = None):
        message = f"Client not found" if client_id is None else f"Client with ID {client_id} not found"
        super().__init__(message, "CLIENT_NOT_FOUND")

class ConnectionError(BankingAppError):
    """Database connection errors."""
    def __init__(self, message: str, original_error: Exception = None):
        self.original_error = original_error
        super().__init__(message, "CONNECTION_ERROR")

class ConfigurationError(BankingAppError):
    """Configuration-related errors."""
    def __init__(self, message: str):
        super().__init__(message, "CONFIG_ERROR")

class UIOperationError(BankingAppError):
    """UI operation errors."""
    def __init__(self, message: str, operation: str = None):
        self.operation = operation
        super().__init__(message, "UI_ERROR") 
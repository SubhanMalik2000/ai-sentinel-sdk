"""
Custom exception hierarchy for the AI Sentinel SDK.

Provides typed errors so consumers can handle configuration, transport,
and validation failures without catching broad Exception types.
"""


class SentinelError(Exception):
    """Base exception for all AI Sentinel SDK errors."""

    def __init__(self, message: str = "An error occurred in the AI Sentinel SDK.") -> None:
        """
        Initialize the base SDK exception.

        Args:
            message: Human-readable description of the error.
        """
        super().__init__(message)


class ConfigurationError(SentinelError):
    """Raised when SDK configuration is invalid or incomplete."""

    def __init__(self, message: str = "Invalid or incomplete SDK configuration.") -> None:
        """
        Initialize a configuration error.

        Args:
            message: Human-readable description of the configuration problem.
        """
        super().__init__(message)


class AuthenticationError(SentinelError):
    """Raised when API authentication fails."""

    def __init__(self, message: str = "Authentication with the AI Sentinel API failed.") -> None:
        """
        Initialize an authentication error.

        Args:
            message: Human-readable description of the auth failure.
        """
        super().__init__(message)


class TransportError(SentinelError):
    """Raised when event transmission to the backend fails."""

    def __init__(self, message: str = "Failed to transmit event to the AI Sentinel backend.") -> None:
        """
        Initialize a transport error.

        Args:
            message: Human-readable description of the transmission failure.
        """
        super().__init__(message)


class ValidationError(SentinelError):
    """Raised when event or request data fails validation."""

    def __init__(self, message: str = "Event or request data failed validation.") -> None:
        """
        Initialize a validation error.

        Args:
            message: Human-readable description of the validation failure.
        """
        super().__init__(message)


# TODO: Add RateLimitError with retry-after metadata.
# TODO: Add BackendError for non-2xx API responses with status codes.

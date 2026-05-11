"""Custom exceptions raised by the QrMaint API client."""
from __future__ import annotations


class QrMaintError(Exception):
    """Base exception for all QrMaint API errors."""


class AuthenticationError(QrMaintError):
    """Raised when the API token is missing, invalid, or expired (HTTP 401)."""


class NotFoundError(QrMaintError):
    """Raised when the requested resource does not exist (HTTP 404)."""


class RateLimitError(QrMaintError):
    """Raised when the API rate limit is exceeded (HTTP 429).

    Attributes:
        retry_after: Seconds to wait before retrying, if provided by the server.
    """

    def __init__(self, retry_after: float | None = None) -> None:
        """Initialize the error with an optional retry delay.

        Args:
            retry_after: Seconds until the rate limit resets, taken from the
                ``Retry-After`` response header.  ``None`` when the header is
                absent.
        """
        self.retry_after = retry_after
        msg = (
            f"Rate limit exceeded. Retry after {retry_after}s"
            if retry_after
            else "Rate limit exceeded."
        )
        super().__init__(msg)


class APIError(QrMaintError):
    """Raised for any unexpected HTTP error response (4xx / 5xx).

    Attributes:
        status_code: The HTTP status code returned by the server.
        message: The error message extracted from the response body.
    """

    def __init__(self, status_code: int, message: str) -> None:
        """Initialize the error with the HTTP status code and server message.

        Args:
            status_code: HTTP status code (e.g. 400, 500).
            message: Human-readable error description from the response.
        """
        self.status_code = status_code
        self.message = message
        super().__init__(f"API error {status_code}: {message}")

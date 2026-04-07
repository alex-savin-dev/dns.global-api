"""Application-level exception classes.

All exceptions follow a consistent structure so the global exception handler
can serialize them into the standard error response format.
"""

from typing import Any


class DnsGlobalError(Exception):
    """Base exception for all DNS.GLOBAL errors."""

    status_code: int = 500
    error_code: str = "internal_error"
    message: str = "An internal error occurred."

    def __init__(self, message: str | None = None, detail: Any = None) -> None:
        self.message = message or self.__class__.message
        self.detail = detail
        super().__init__(self.message)

    def to_dict(self) -> dict:
        payload: dict[str, Any] = {
            "error": self.error_code,
            "message": self.message,
        }
        if self.detail:
            payload["detail"] = self.detail
        return payload


class NotFoundError(DnsGlobalError):
    status_code = 404
    error_code = "not_found"
    message = "The requested resource was not found."


class ConflictError(DnsGlobalError):
    status_code = 409
    error_code = "conflict"
    message = "The request conflicts with the current state."


class ValidationError(DnsGlobalError):
    status_code = 422
    error_code = "validation_error"
    message = "Request validation failed."


class AuthenticationError(DnsGlobalError):
    status_code = 401
    error_code = "authentication_error"
    message = "Authentication failed."


class AuthorizationError(DnsGlobalError):
    status_code = 403
    error_code = "authorization_error"
    message = "You do not have permission to perform this action."


class RateLimitError(DnsGlobalError):
    status_code = 429
    error_code = "rate_limit_exceeded"
    message = "Rate limit exceeded. Please retry later."


class ProviderError(DnsGlobalError):
    status_code = 502
    error_code = "provider_error"
    message = "The DNS provider returned an error."

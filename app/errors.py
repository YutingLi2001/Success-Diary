"""
Error handling system for Success-Diary application.

This module provides a unified error handling approach that supports both HTMX
and traditional JSON responses with comprehensive error categorization and
user-friendly recovery patterns.
"""

import logging
import uuid
from typing import Optional
from fastapi import Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

logger = logging.getLogger(__name__)
templates = Jinja2Templates(directory="templates")


class ErrorData:
    """
    Structured error data container for consistent error handling.
    
    Attributes:
        error_id: Unique identifier for tracking and debugging
        code: Error code for programmatic handling
        message: User-friendly error message
        severity: Error severity level (error, warning, info)
        ui_hint: UI display preference (inline, toast, modal)
        recoverable: Whether the error can be recovered from
        context: Error context for specific handling (validation, auth, network, server)
    """
    
    def __init__(
        self,
        code: str,
        message: str,
        severity: str = "error",
        ui_hint: str = "inline",
        recoverable: bool = True,
        context: str = "general"
    ):
        self.error_id = str(uuid.uuid4())[:8]  # Short ID for tracking
        self.code = code
        self.message = message
        self.severity = severity  # error, warning, info
        self.ui_hint = ui_hint    # inline, toast, modal
        self.recoverable = recoverable
        self.context = context    # general, validation, auth, network, server
    
    def to_dict(self) -> dict:
        """Convert ErrorData to dictionary for JSON responses."""
        return {
            "error_id": self.error_id,
            "code": self.code,
            "message": self.message,
            "severity": self.severity,
            "ui_hint": self.ui_hint,
            "recoverable": self.recoverable,
            "context": self.context
        }


async def handle_error(request: Request, error: ErrorData, status_code: int = 400) -> HTMLResponse | JSONResponse:
    """
    Unified error handler that returns appropriate response based on request type.
    
    Args:
        request: FastAPI request object
        error: ErrorData instance containing error details
        status_code: HTTP status code to return
    
    Returns:
        HTMLResponse for HTMX requests, JSONResponse for API calls
    """
    
    # Log error for debugging (with error ID for tracking)
    log_message = f"Error {error.error_id}: {error.code} - {error.message}"
    if error.severity == "error":
        logger.error(log_message)
    elif error.severity == "warning":
        logger.warning(log_message)
    else:
        logger.info(log_message)
    
    error_dict = error.to_dict()
    
    # HTMX request detection - return HTML fragment
    if request.headers.get("HX-Request"):
        try:
            return templates.TemplateResponse(
                f"errors/{error.ui_hint}.html",
                {
                    "request": request,
                    "error": error_dict
                },
                status_code=status_code
            )
        except Exception as template_error:
            logger.error(f"Error template rendering failed: {template_error}")
            # Fallback to simple HTML response
            return HTMLResponse(
                content=f'<div class="bg-red-50 border border-red-200 text-red-800 p-4 rounded-lg">'
                       f'<p>{error.message}</p></div>',
                status_code=status_code
            )
    
    # Standard JSON response for API calls
    return JSONResponse(
        content={"error": error_dict},
        status_code=status_code
    )


# Custom Exception Classes

class AuthenticationError(Exception):
    """Raised when authentication is required or has failed."""
    
    def __init__(self, message: str = "Authentication required"):
        self.message = message
        super().__init__(self.message)


class ValidationError(Exception):
    """Raised when input validation fails."""
    
    def __init__(self, message: str, field: Optional[str] = None):
        self.message = message
        self.field = field
        super().__init__(self.message)


class NetworkError(Exception):
    """Raised when network or connectivity issues occur."""
    
    def __init__(self, message: str = "Network connection failed"):
        self.message = message
        super().__init__(self.message)


# Error Handler Functions

async def http_exception_handler(request: Request, exc: HTTPException) -> HTMLResponse | JSONResponse:
    """Handle standard HTTP exceptions."""
    
    # Map common HTTP status codes to user-friendly messages
    status_messages = {
        400: "Invalid request. Please check your input and try again.",
        401: "Authentication required. Please sign in to continue.",
        403: "Access denied. You don't have permission for this action.",
        404: "The requested resource was not found.",
        422: "Invalid input data. Please review and correct your entries.",
        429: "Too many requests. Please wait a moment and try again.",
        500: "Internal server error. Please try again later.",
        502: "Service unavailable. Please try again later.",
        503: "Service temporarily unavailable. Please try again later."
    }
    
    user_message = status_messages.get(exc.status_code, exc.detail)
    
    # Determine UI hint based on status code
    ui_hint = "modal" if exc.status_code == 401 else "toast" if exc.status_code >= 500 else "inline"
    
    error_data = ErrorData(
        code=f"HTTP_{exc.status_code}",
        message=user_message,
        severity="error" if exc.status_code >= 400 else "warning",
        ui_hint=ui_hint,
        recoverable=exc.status_code < 500,
        context="server" if exc.status_code >= 500 else "general"
    )
    
    return await handle_error(request, error_data, exc.status_code)


async def authentication_error_handler(request: Request, exc: AuthenticationError) -> HTMLResponse | JSONResponse:
    """Handle authentication errors with modal display."""
    
    error_data = ErrorData(
        code="AUTHENTICATION_REQUIRED",
        message=exc.message,
        severity="warning",
        ui_hint="modal",
        recoverable=True,
        context="auth"
    )
    
    return await handle_error(request, error_data, 401)


async def validation_error_handler(request: Request, exc: ValidationError) -> HTMLResponse | JSONResponse:
    """Handle validation errors with inline display."""
    
    error_data = ErrorData(
        code="VALIDATION_ERROR",
        message=exc.message,
        severity="warning",
        ui_hint="inline",
        recoverable=True,
        context="validation"
    )
    
    return await handle_error(request, error_data, 400)


async def network_error_handler(request: Request, exc: NetworkError) -> HTMLResponse | JSONResponse:
    """Handle network errors with toast display."""
    
    error_data = ErrorData(
        code="NETWORK_ERROR",
        message=exc.message,
        severity="error",
        ui_hint="toast",
        recoverable=True,
        context="network"
    )
    
    return await handle_error(request, error_data, 503)


async def general_exception_handler(request: Request, exc: Exception) -> HTMLResponse | JSONResponse:
    """Handle unexpected exceptions with graceful fallback."""
    
    # Log the actual error for debugging
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    
    error_data = ErrorData(
        code="INTERNAL_ERROR",
        message="Something went wrong. Please try again.",
        severity="error",
        ui_hint="toast",
        recoverable=True,
        context="server"
    )
    
    return await handle_error(request, error_data, 500)


# Helper Functions

def create_validation_error(field: str, message: str) -> ValidationError:
    """Create a validation error with field context."""
    return ValidationError(message=f"{field}: {message}", field=field)


def create_auth_error(message: str = "Please sign in to continue") -> AuthenticationError:
    """Create an authentication error."""
    return AuthenticationError(message=message)


def create_network_error(operation: str = "request") -> NetworkError:
    """Create a network error with operation context."""
    return NetworkError(message=f"Network error during {operation}. Please check your connection and try again.")


# Quick error creation functions for common scenarios
def validation_required(field: str) -> ValidationError:
    """Create error for required field validation."""
    return create_validation_error(field, "This field is required")


def validation_invalid_format(field: str, expected: str) -> ValidationError:
    """Create error for invalid format validation."""
    return create_validation_error(field, f"Invalid format. Expected: {expected}")


def validation_too_long(field: str, max_length: int) -> ValidationError:
    """Create error for field too long validation."""
    return create_validation_error(field, f"Maximum length is {max_length} characters")


def validation_too_short(field: str, min_length: int) -> ValidationError:
    """Create error for field too short validation."""
    return create_validation_error(field, f"Minimum length is {min_length} characters")
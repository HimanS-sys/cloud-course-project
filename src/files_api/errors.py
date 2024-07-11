"""Module to handle custom exceptions."""

from fastapi import (
    Request,
    status,
)
from fastapi.responses import JSONResponse
from pydantic import ValidationError


async def handle_broad_exceptions(request: Request, call_next):
    """Handle any exception that goes unhandled by a more specific exception handler."""
    try:
        return await call_next(request)
    except Exception:  # pylint: disable=broad-except
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Internal server error"},
        )


# pylint: disable=unused-argument
async def handle_custom_pydantic_validation_errors(request: Request, exc: ValidationError):
    """Handle pydantic validation Errors that come from custom validators because FastAPI does not by default."""
    errors = exc.errors()
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "message": "error",
            "error_type": "422 Unprocessable Entity",
            "errors": [err["msg"] for err in errors],
        },
    )

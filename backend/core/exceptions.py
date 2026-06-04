"""
Custom exception handler — CleanMail by Samod.

Wraps DRF's default exception handler to ensure all API error responses
use a consistent JSON structure with Spanish messages.
"""

from rest_framework.views import exception_handler as drf_exception_handler


def custom_exception_handler(exc, context):
    """
    Override the default DRF exception handler to wrap errors in a
    consistent ``{"error": ..., "detalle": ...}`` envelope.
    """
    response = drf_exception_handler(exc, context)

    if response is not None:
        # Build a normalised error body
        detail = response.data

        # DRF sometimes returns a dict with "detail" key, sometimes a list
        if isinstance(detail, dict):
            message = detail.get("detail", detail)
        elif isinstance(detail, list):
            message = detail
        else:
            message = str(detail)

        response.data = {
            "error": True,
            "detalle": message,
        }

    return response

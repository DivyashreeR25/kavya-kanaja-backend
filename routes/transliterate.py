"""
POST /transliterate
Converts Kannada script ↔ Roman script.
"""

import logging
from fastapi import APIRouter, HTTPException, status
from models.schemas import (
    TransliterateRequest,
    TransliterateResponse,
    ErrorResponse,
)
from services.groq_service import GroqService

logger = logging.getLogger(__name__)
router = APIRouter()

_groq_service: GroqService | None = None

def set_groq_service(service: GroqService):
    global _groq_service
    _groq_service = service


@router.post(
    "/transliterate",
    response_model=TransliterateResponse,
    responses={
        200: {"description": "Transliteration successful"},
        400: {"model": ErrorResponse, "description": "Invalid request"},
        429: {"model": ErrorResponse, "description": "Rate limit exceeded"},
        500: {"model": ErrorResponse, "description": "Server error"},
    },
    summary="Transliterate Kannada ↔ Roman",
    description=(
        "Converts Kannada script to Roman transliteration (or vice versa). "
        "Choose 'readable' style for general use or 'iast' for scholarly use."
    ),
)
async def transliterate(request: TransliterateRequest) -> TransliterateResponse:
    """
    POST /transliterate

    Request body:
        {
            "text": "ಕನ್ನಡ ನಾಡು ನಮ್ಮ ನಾಡು",
            "direction": "kn_to_roman",
            "style": "readable"
        }
    """
    if _groq_service is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server not initialized.",
        )

    logger.info(
        f"POST /transliterate | direction={request.direction} | "
        f"style={request.style} | len={len(request.text)}"
    )

    try:
        return await _groq_service.transliterate(request)

    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    except RuntimeError as e:
        msg = str(e)
        status_code = (
            status.HTTP_429_TOO_MANY_REQUESTS
            if "busy" in msg.lower()
            else status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        raise HTTPException(status_code=status_code, detail=msg)

    except Exception as e:
        logger.exception(f"Unexpected error in /transliterate: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred.",
        )
"""
API route for poem/word explanation.

This is the only endpoint the Android app calls.
It receives the request, passes it to the service layer,
and returns the structured JSON response.

Endpoint: POST /explain
"""

import logging
from fastapi import APIRouter, HTTPException, status

from models.schemas import ExplainRequest, ExplainResponse, ErrorResponse
from services.groq_service import GroqService

logger = logging.getLogger(__name__)

# APIRouter — lets us group routes and include them in main.py cleanly
router = APIRouter()

# The GroqService instance is injected from main.py
# This is set once at startup (see main.py)
_groq_service: GroqService | None = None


def set_groq_service(service: GroqService):
    """
    Called from main.py at startup to inject the GroqService.
    This avoids creating multiple Groq clients.
    """
    global _groq_service
    _groq_service = service


@router.post(
    "/explain",
    response_model=ExplainResponse,
    responses={
        200: {"description": "Explanation generated successfully"},
        400: {"model": ErrorResponse, "description": "Invalid request"},
        429: {"model": ErrorResponse, "description": "Rate limit exceeded"},
        500: {"model": ErrorResponse, "description": "Server or AI error"},
    },
    summary="Explain a Kannada poem or word",
    description=(
        "Sends a Kannada poem or word to the AI and returns a structured explanation. "
        "Set mode='full' for complete poem explanation, mode='word' for single word meaning."
    ),
)
async def explain_poem(request: ExplainRequest) -> ExplainResponse:
    """
    POST /explain

    Accepts a poem or word and returns an AI-generated structured explanation.

    Request body:
        {
            "text": "ಕತ್ತಲೆಯ ನಡುವೆ ಒಂದು ಕಿರಣ...",
            "language": "en",
            "mode": "full"
        }

    Response body:
        {
            "meaning": "...",
            "line_explanation": "...",
            "word_meanings": "...",
            "theme": "...",
            "summary": "...",
            "story": "..."
        }
    """

    # Safety check — service must be initialized
    if _groq_service is None:
        logger.critical("GroqService not initialized! Check main.py startup.")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server not properly initialized. Please try again later.",
        )

    logger.info(
        f"Explain request received | mode={request.mode} | "
        f"lang={request.language} | text_len={len(request.text)}"
    )

    try:
        # Delegate all AI work to the service layer
        response = await _groq_service.explain(request)

        logger.info("Explanation generated successfully")
        return response

    except ValueError as e:
        # Bad input or unparseable AI response
        logger.warning(f"ValueError in explain: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    except RuntimeError as e:
        # Groq API errors (rate limit, connection, etc.)
        error_msg = str(e)
        logger.error(f"RuntimeError in explain: {error_msg}")

        # Surface rate limit errors as 429, everything else as 500
        if "busy" in error_msg.lower() or "rate" in error_msg.lower():
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=error_msg,
            )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=error_msg,
        )

    except Exception as e:
        # Catch-all for unexpected errors — always log these
        logger.exception(f"Unexpected error in explain endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred. Please try again.",
        )
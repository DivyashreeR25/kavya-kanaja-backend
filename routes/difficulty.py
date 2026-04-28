"""
POST /difficulty
AI scores the difficulty of a Kannada poem.
"""

import logging
from fastapi import APIRouter, HTTPException, status
from models.schemas import DifficultyRequest, DifficultyResponse, ErrorResponse
from services.groq_service import GroqService

logger = logging.getLogger(__name__)
router = APIRouter()

_groq_service: GroqService | None = None

def set_groq_service(service: GroqService):
    global _groq_service
    _groq_service = service


@router.post(
    "/difficulty",
    response_model=DifficultyResponse,
    responses={
        200: {"description": "Difficulty scored successfully"},
        400: {"model": ErrorResponse, "description": "Invalid request"},
        429: {"model": ErrorResponse, "description": "Rate limit exceeded"},
        500: {"model": ErrorResponse, "description": "Server error"},
    },
    summary="Score poem difficulty",
    description=(
        "Uses AI to rate how difficult a Kannada poem is to understand. "
        "Returns Easy / Medium / Hard with a 1-10 score and reasoning."
    ),
)
async def score_difficulty(request: DifficultyRequest) -> DifficultyResponse:
    """
    POST /difficulty

    Request body:
        {
            "poem_text": "ಕತ್ತಲೆಯ ನಡುವೆ...",
            "language": "en"
        }
    """
    if _groq_service is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server not initialized.",
        )

    logger.info(f"POST /difficulty | lang={request.language}")

    try:
        return await _groq_service.score_difficulty(request)

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
        logger.exception(f"Unexpected error in /difficulty: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred.",
        )
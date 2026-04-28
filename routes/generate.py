"""
POST /generate
Generates a new poem in the style of a given Kannada poet.
"""

import logging
from fastapi import APIRouter, HTTPException, status
from models.schemas import GenerateRequest, GenerateResponse, ErrorResponse
from services.groq_service import GroqService

logger = logging.getLogger(__name__)
router = APIRouter()

_groq_service: GroqService | None = None

def set_groq_service(service: GroqService):
    global _groq_service
    _groq_service = service


@router.post(
    "/generate",
    response_model=GenerateResponse,
    responses={
        200: {"description": "Poem generated successfully"},
        400: {"model": ErrorResponse, "description": "Invalid request"},
        429: {"model": ErrorResponse, "description": "Rate limit exceeded"},
        500: {"model": ErrorResponse, "description": "Server error"},
    },
    summary="Generate poem in poet's style",
    description=(
        "Generates a new original poem on a given topic written in the "
        "distinctive style of a specified Kannada poet."
    ),
)
async def generate_poem(request: GenerateRequest) -> GenerateResponse:
    """
    POST /generate

    Request body:
        {
            "poet_name": "Kuvempu",
            "topic": "Nature and rivers",
            "language": "en",
            "length": "short"
        }
    """
    if _groq_service is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server not initialized.",
        )

    logger.info(
        f"POST /generate | poet={request.poet_name} | "
        f"topic={request.topic} | length={request.length}"
    )

    try:
        return await _groq_service.generate_poem(request)

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
        logger.exception(f"Unexpected error in /generate: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred.",
        )
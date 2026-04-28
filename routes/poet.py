"""
POST /poet
Returns a structured intelligence profile of a Kannada poet.
"""

import logging
from fastapi import APIRouter, HTTPException, status
from models.schemas import PoetRequest, PoetResponse, ErrorResponse
from services.groq_service import GroqService

logger = logging.getLogger(__name__)
router = APIRouter()

_groq_service: GroqService | None = None

def set_groq_service(service: GroqService):
    global _groq_service
    _groq_service = service


@router.post(
    "/poet",
    response_model=PoetResponse,
    responses={
        200: {"description": "Poet profile generated successfully"},
        400: {"model": ErrorResponse, "description": "Invalid request"},
        429: {"model": ErrorResponse, "description": "Rate limit exceeded"},
        500: {"model": ErrorResponse, "description": "Server error"},
    },
    summary="Get poet profile",
    description=(
        "Returns a detailed AI-generated profile of a Kannada poet including "
        "biography, writing style, famous works, era, and fun facts."
    ),
)
async def get_poet_profile(request: PoetRequest) -> PoetResponse:
    """
    POST /poet

    Request body:
        {
            "poet_name": "Kuvempu",
            "language": "en"
        }
    """
    if _groq_service is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server not initialized.",
        )

    logger.info(f"POST /poet | poet={request.poet_name} | lang={request.language}")

    try:
        return await _groq_service.get_poet_profile(request)

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
        logger.exception(f"Unexpected error in /poet: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred.",
        )
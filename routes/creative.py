"""
POST /dialogue
Converts a Kannada poem into a dramatic dialogue/script.
"""

import logging
from fastapi import APIRouter, HTTPException, status
from models.schemas import DialogueRequest, DialogueResponse, ErrorResponse
from services.groq_service import GroqService

logger = logging.getLogger(__name__)
router = APIRouter()

_groq_service: GroqService | None = None

def set_groq_service(service: GroqService):
    global _groq_service
    _groq_service = service


@router.post(
    "/dialogue",
    response_model=DialogueResponse,
    responses={
        200: {"description": "Dialogue generated successfully"},
        400: {"model": ErrorResponse, "description": "Invalid request"},
        429: {"model": ErrorResponse, "description": "Rate limit exceeded"},
        500: {"model": ErrorResponse, "description": "Server error"},
    },
    summary="Convert poem to dialogue",
    description=(
        "Converts a Kannada poem into a dramatic dialogue script between "
        "2 to 4 characters, with stage notes and setting description."
    ),
)
async def generate_dialogue(request: DialogueRequest) -> DialogueResponse:
    """
    POST /dialogue

    Request body:
        {
            "poem_text": "ಕತ್ತಲೆಯ ನಡುವೆ...",
            "language": "en",
            "num_characters": 2
        }
    """
    if _groq_service is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server not initialized.",
        )

    logger.info(
        f"POST /dialogue | characters={request.num_characters} | "
        f"lang={request.language}"
    )

    try:
        return await _groq_service.generate_dialogue(request)

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
        logger.exception(f"Unexpected error in /dialogue: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred.",
        )
"""
POST /quiz
Generates MCQ + True/False questions from a Kannada poem.
"""

import logging
from fastapi import APIRouter, HTTPException, status
from models.schemas import QuizRequest, QuizResponse, ErrorResponse
from services.groq_service import GroqService

logger = logging.getLogger(__name__)
router = APIRouter()

_groq_service: GroqService | None = None

def set_groq_service(service: GroqService):
    global _groq_service
    _groq_service = service


@router.post(
    "/quiz",
    response_model=QuizResponse,
    responses={
        200: {"description": "Quiz generated successfully"},
        400: {"model": ErrorResponse, "description": "Invalid request"},
        429: {"model": ErrorResponse, "description": "Rate limit exceeded"},
        500: {"model": ErrorResponse, "description": "Server error"},
    },
    summary="Generate quiz from poem",
    description=(
        "Generates multiple choice and true/false questions from a Kannada poem. "
        "Supports easy, medium, and hard difficulty levels."
    ),
)
async def generate_quiz(request: QuizRequest) -> QuizResponse:
    """
    POST /quiz

    Request body:
        {
            "poem_text": "ಕತ್ತಲೆಯ ನಡುವೆ...",
            "language": "en",
            "num_questions": 5,
            "difficulty": "medium"
        }
    """
    if _groq_service is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Server not initialized.",
        )

    logger.info(
        f"POST /quiz | difficulty={request.difficulty} | "
        f"num_q={request.num_questions} | lang={request.language}"
    )

    try:
        return await _groq_service.generate_quiz(request)

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
        logger.exception(f"Unexpected error in /quiz: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred.",
        )
"""
Poems endpoints — no AI involved, pure data.

GET  /poems              → paginated list with filters
GET  /poems/daily        → today's featured poem
GET  /poems/meta         → all categories and poets
GET  /poems/related/{id} → related poems by category/tags
GET  /poems/{id}         → single poem by ID
"""

import logging
from fastapi import APIRouter, HTTPException, Query, status
from models.schemas import (
    PoemData,
    PoemsListResponse,
    PoemsMetaResponse,
    ErrorResponse,
)
from data.poems_data import (
    get_all_poems,
    get_poem_by_id,
    get_daily_poem,
    get_all_categories,
    get_all_poets,
    get_related_poems,
    POEMS,
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/poems", tags=["Poems"])


@router.get(
    "",
    response_model=PoemsListResponse,
    summary="Get all poems",
    description=(
        "Returns a paginated list of poems. "
        "Supports filtering by search query, category, difficulty, and poet."
    ),
)
async def list_poems(
    search: str = Query(default="", description="Search in title, poet, tags"),
    category: str = Query(default="", description="Filter by category"),
    difficulty: str = Query(default="", description="Filter: easy / medium / hard"),
    poet: str = Query(default="", description="Filter by poet name"),
    page: int = Query(default=1, ge=1, description="Page number"),
    page_size: int = Query(default=10, ge=1, le=20, description="Items per page"),
) -> PoemsListResponse:
    """
    GET /poems?search=nature&category=Philosophy&page=1&page_size=10

    All query params are optional — returns all poems if none provided.
    """
    logger.info(
        f"GET /poems | search='{search}' | category='{category}' | "
        f"difficulty='{difficulty}' | poet='{poet}' | page={page}"
    )

    result = get_all_poems(
        search=search,
        category=category,
        difficulty=difficulty,
        poet=poet,
        page=page,
        page_size=page_size,
    )

    return PoemsListResponse(
        poems=[PoemData(**p) for p in result["poems"]],
        total=result["total"],
        page=result["page"],
        page_size=result["page_size"],
        total_pages=result["total_pages"],
        has_next=result["has_next"],
        has_prev=result["has_prev"],
    )


@router.get(
    "/daily",
    response_model=PoemData,
    summary="Get today's poem",
    description=(
        "Returns today's featured poem. "
        "Changes automatically every day at midnight — no database needed."
    ),
)
async def daily_poem() -> PoemData:
    """GET /poems/daily"""
    logger.info("GET /poems/daily")
    poem = get_daily_poem()
    return PoemData(**poem)


@router.get(
    "/meta",
    response_model=PoemsMetaResponse,
    summary="Get filter metadata",
    description=(
        "Returns all available categories and poet names. "
        "Use this to populate filter dropdowns in the Android app."
    ),
)
async def poems_meta() -> PoemsMetaResponse:
    """GET /poems/meta"""
    logger.info("GET /poems/meta")
    return PoemsMetaResponse(
        categories=get_all_categories(),
        poets=get_all_poets(),
        total_poems=len(POEMS),
    )


@router.get(
    "/related/{poem_id}",
    response_model=list[PoemData],
    summary="Get related poems",
    description=(
        "Returns up to 3 poems related to the given poem "
        "based on shared category and tags."
    ),
    responses={
        404: {"model": ErrorResponse, "description": "Poem not found"},
    },
)
async def related_poems(poem_id: int) -> list[PoemData]:
    """GET /poems/related/1"""
    logger.info(f"GET /poems/related/{poem_id}")

    # Verify the poem exists first
    poem = get_poem_by_id(poem_id)
    if not poem:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Poem with id {poem_id} not found.",
        )

    related = get_related_poems(poem_id)
    return [PoemData(**p) for p in related]


@router.get(
    "/{poem_id}",
    response_model=PoemData,
    summary="Get poem by ID",
    description="Returns a single poem by its ID.",
    responses={
        404: {"model": ErrorResponse, "description": "Poem not found"},
    },
)
async def get_poem(poem_id: int) -> PoemData:
    """GET /poems/1"""
    logger.info(f"GET /poems/{poem_id}")

    poem = get_poem_by_id(poem_id)
    if not poem:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Poem with id {poem_id} not found.",
        )

    return PoemData(**poem)
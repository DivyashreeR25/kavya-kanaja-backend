"""
Kavya-Kanaja Backend — FastAPI Application Entry Point
UPDATED (Group C): Added 3 new routers — poems, difficulty, transliterate.
"""

import logging
import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ── Route imports ──────────────────────────────────────────────────────────
from routes.explain      import router as explain_router,      set_groq_service as explain_sgs
from routes.story        import router as story_router,        set_groq_service as story_sgs
from routes.poet         import router as poet_router,         set_groq_service as poet_sgs
from routes.quiz         import router as quiz_router,         set_groq_service as quiz_sgs
from routes.creative     import router as creative_router,     set_groq_service as creative_sgs
from routes.generate     import router as generate_router,     set_groq_service as generate_sgs
from routes.poems        import router as poems_router                              # NEW (no AI injection needed)
from routes.difficulty   import router as difficulty_router,   set_groq_service as difficulty_sgs   # NEW
from routes.transliterate import router as transliterate_router, set_groq_service as transliterate_sgs  # NEW

from services.groq_service import GroqService

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Kavya-Kanaja backend...")

    if not GROQ_API_KEY:
        logger.critical("GROQ_API_KEY is not set!")
        raise RuntimeError("GROQ_API_KEY environment variable is required.")

    groq_service = GroqService(api_key=GROQ_API_KEY)

    # Inject into all AI-powered route modules
    explain_sgs(groq_service)
    story_sgs(groq_service)
    poet_sgs(groq_service)
    quiz_sgs(groq_service)
    creative_sgs(groq_service)
    generate_sgs(groq_service)
    difficulty_sgs(groq_service)        # NEW
    transliterate_sgs(groq_service)     # NEW
    # Note: poems_router needs no injection — it's pure data, no AI

    logger.info("All services initialized.")
    logger.info("Kavya-Kanaja backend is ready! 🪷")

    yield

    logger.info("Shutting down Kavya-Kanaja backend...")


app = FastAPI(
    title="Kavya-Kanaja API",
    description=(
        "AI-powered backend for Kavya-Kanaja — a Kannada poetry learning app. "
        "Poems list, explanations, stories, quizzes, poet profiles, "
        "difficulty scoring, and transliteration using Groq + Llama."
    ),
    version="3.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# ── Register all routers ───────────────────────────────────────────────────
app.include_router(explain_router)
app.include_router(story_router)
app.include_router(poet_router)
app.include_router(quiz_router)
app.include_router(creative_router)
app.include_router(generate_router)
app.include_router(poems_router)            # NEW
app.include_router(difficulty_router)       # NEW
app.include_router(transliterate_router)    # NEW


@app.get("/", summary="Health check")
async def root():
    return {
        "status": "ok",
        "app": "Kavya-Kanaja Backend",
        "version": "3.0.0",
        "total_endpoints": 14,
        "endpoints": {
            "AI powered": [
                "POST /explain",
                "POST /story",
                "POST /poet",
                "POST /quiz",
                "POST /dialogue",
                "POST /generate",
                "POST /difficulty",
                "POST /transliterate",
            ],
            "Data": [
                "GET /poems",
                "GET /poems/daily",
                "GET /poems/meta",
                "GET /poems/related/{id}",
                "GET /poems/{id}",
            ],
            "Health": ["GET /", "GET /health"],
        },
        "message": "ಕಾವ್ಯ ಕಣಜಕ್ಕೆ ಸ್ವಾಗತ! 🪷"
    }


@app.get("/health", summary="Detailed health check")
async def health():
    return {
        "status": "healthy",
        "groq_configured": bool(GROQ_API_KEY),
        "model": GroqService.MODEL,
        "version": "3.0.0",
    }
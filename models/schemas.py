"""
Pydantic models for all request/response shapes.
UPDATED (Group B): Added 5 new request+response model pairs.
"""

from pydantic import BaseModel, field_validator
from typing import Optional, List


# ─────────────────────────────────────────────────────────────
# ORIGINAL MODELS (unchanged)
# ─────────────────────────────────────────────────────────────

class ExplainRequest(BaseModel):
    """
    Modes:
        full / word / emotion / lesson /
        simplify / modernize / visualize / background
    """
    text: str
    language: str = "en"
    mode: str = "full"

    @field_validator("language")
    @classmethod
    def validate_language(cls, v: str) -> str:
        allowed = {"en", "kn"}
        if v not in allowed:
            raise ValueError(f"language must be one of {allowed}, got '{v}'")
        return v

    @field_validator("mode")
    @classmethod
    def validate_mode(cls, v: str) -> str:
        allowed = {
            "full", "word",
            "emotion", "lesson", "simplify",
            "modernize", "visualize", "background",
        }
        if v not in allowed:
            raise ValueError(f"mode must be one of {allowed}, got '{v}'")
        return v

    @field_validator("text")
    @classmethod
    def validate_text(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("text cannot be empty")
        if len(v) > 5000:
            raise ValueError("text is too long (max 5000 characters)")
        return v.strip()


class ExplainResponse(BaseModel):
    meaning: Optional[str] = None
    line_explanation: Optional[str] = None
    word_meanings: Optional[str] = None
    theme: Optional[str] = None
    summary: Optional[str] = None
    story: Optional[str] = None


class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None


# ─────────────────────────────────────────────────────────────
# GROUP B — NEW MODELS
# ─────────────────────────────────────────────────────────────

# ── 1. Story Generator ────────────────────────────────────────

class StoryRequest(BaseModel):
    """
    POST /story
    Converts a Kannada poem into a short narrative story.
    """
    poem_text: str
    language: str = "en"
    style: str = "simple"       # "simple" | "dramatic" | "children"

    @field_validator("language")
    @classmethod
    def validate_language(cls, v: str) -> str:
        if v not in {"en", "kn"}:
            raise ValueError(f"language must be 'en' or 'kn', got '{v}'")
        return v

    @field_validator("style")
    @classmethod
    def validate_style(cls, v: str) -> str:
        allowed = {"simple", "dramatic", "children"}
        if v not in allowed:
            raise ValueError(f"style must be one of {allowed}, got '{v}'")
        return v

    @field_validator("poem_text")
    @classmethod
    def validate_poem_text(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("poem_text cannot be empty")
        if len(v) > 5000:
            raise ValueError("poem_text too long (max 5000 characters)")
        return v.strip()


class StoryResponse(BaseModel):
    """
    Response for POST /story.
    title        → story title
    story        → the full narrative story
    characters   → list of characters in the story
    moral        → the lesson/moral of the story
    setting      → where and when the story takes place
    """
    title: Optional[str] = None
    story: Optional[str] = None
    characters: Optional[str] = None
    moral: Optional[str] = None
    setting: Optional[str] = None


# ── 2. Poet Profile ───────────────────────────────────────────

class PoetRequest(BaseModel):
    """
    POST /poet
    Returns a detailed AI-generated profile of a Kannada poet.
    """
    poet_name: str
    language: str = "en"

    @field_validator("language")
    @classmethod
    def validate_language(cls, v: str) -> str:
        if v not in {"en", "kn"}:
            raise ValueError(f"language must be 'en' or 'kn', got '{v}'")
        return v

    @field_validator("poet_name")
    @classmethod
    def validate_poet_name(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("poet_name cannot be empty")
        if len(v) > 200:
            raise ValueError("poet_name too long")
        return v.strip()


class PoetResponse(BaseModel):
    """
    Response for POST /poet.
    name         → full name of the poet
    biography    → life story and background
    writing_style → how they write — themes, forms, language used
    famous_works → their most notable poems and books
    era          → time period and literary movement
    fun_fact     → one interesting fact about the poet
    simple_intro → explain this poet to a beginner in 2 sentences
    """
    name: Optional[str] = None
    biography: Optional[str] = None
    writing_style: Optional[str] = None
    famous_works: Optional[str] = None
    era: Optional[str] = None
    fun_fact: Optional[str] = None
    simple_intro: Optional[str] = None


# ── 3. Quiz Generator ─────────────────────────────────────────

class QuizRequest(BaseModel):
    """
    POST /quiz
    Generates MCQ + True/False questions from a poem.
    """
    poem_text: str
    language: str = "en"
    num_questions: int = 5      # How many MCQs to generate (1-10)
    difficulty: str = "medium"  # "easy" | "medium" | "hard"

    @field_validator("language")
    @classmethod
    def validate_language(cls, v: str) -> str:
        if v not in {"en", "kn"}:
            raise ValueError(f"language must be 'en' or 'kn', got '{v}'")
        return v

    @field_validator("difficulty")
    @classmethod
    def validate_difficulty(cls, v: str) -> str:
        if v not in {"easy", "medium", "hard"}:
            raise ValueError(f"difficulty must be easy/medium/hard, got '{v}'")
        return v

    @field_validator("num_questions")
    @classmethod
    def validate_num_questions(cls, v: int) -> int:
        if not 1 <= v <= 10:
            raise ValueError("num_questions must be between 1 and 10")
        return v

    @field_validator("poem_text")
    @classmethod
    def validate_poem_text(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("poem_text cannot be empty")
        if len(v) > 5000:
            raise ValueError("poem_text too long (max 5000 characters)")
        return v.strip()


class QuizQuestion(BaseModel):
    """Single MCQ question."""
    question: str
    option_a: str
    option_b: str
    option_c: str
    option_d: str
    correct_answer: str     # "A" | "B" | "C" | "D"
    explanation: str        # Why this answer is correct


class TrueFalseQuestion(BaseModel):
    """Single True/False question."""
    statement: str
    answer: bool            # True or False
    explanation: str


class QuizResponse(BaseModel):
    """
    Response for POST /quiz.
    mcq_questions → list of multiple choice questions
    tf_questions  → list of true/false questions
    poem_summary  → quick summary to help answer questions
    difficulty    → difficulty level used
    """
    mcq_questions: Optional[List[QuizQuestion]] = None
    tf_questions: Optional[List[TrueFalseQuestion]] = None
    poem_summary: Optional[str] = None
    difficulty: Optional[str] = None


# ── 4. Dialogue / Drama ───────────────────────────────────────

class DialogueRequest(BaseModel):
    """
    POST /dialogue
    Converts a poem into a dramatic dialogue between characters.
    """
    poem_text: str
    language: str = "en"
    num_characters: int = 2     # How many characters in the dialogue (2-4)

    @field_validator("language")
    @classmethod
    def validate_language(cls, v: str) -> str:
        if v not in {"en", "kn"}:
            raise ValueError(f"language must be 'en' or 'kn', got '{v}'")
        return v

    @field_validator("num_characters")
    @classmethod
    def validate_num_characters(cls, v: int) -> int:
        if not 2 <= v <= 4:
            raise ValueError("num_characters must be between 2 and 4")
        return v

    @field_validator("poem_text")
    @classmethod
    def validate_poem_text(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("poem_text cannot be empty")
        if len(v) > 5000:
            raise ValueError("poem_text too long (max 5000 characters)")
        return v.strip()


class DialogueResponse(BaseModel):
    """
    Response for POST /dialogue.
    characters   → names and descriptions of characters
    dialogue     → the full dramatic dialogue script
    setting      → scene description (where/when this takes place)
    stage_notes  → director's notes for how to perform it
    theme        → central theme expressed through the dialogue
    """
    characters: Optional[str] = None
    dialogue: Optional[str] = None
    setting: Optional[str] = None
    stage_notes: Optional[str] = None
    theme: Optional[str] = None


# ── 5. Write Like Poet ────────────────────────────────────────

class GenerateRequest(BaseModel):
    """
    POST /generate
    Generates a new poem in the style of a given Kannada poet.
    """
    poet_name: str
    topic: str
    language: str = "en"
    length: str = "short"       # "short" (4-8 lines) | "medium" (8-16) | "long" (16+)

    @field_validator("language")
    @classmethod
    def validate_language(cls, v: str) -> str:
        if v not in {"en", "kn"}:
            raise ValueError(f"language must be 'en' or 'kn', got '{v}'")
        return v

    @field_validator("length")
    @classmethod
    def validate_length(cls, v: str) -> str:
        if v not in {"short", "medium", "long"}:
            raise ValueError(f"length must be short/medium/long, got '{v}'")
        return v

    @field_validator("poet_name")
    @classmethod
    def validate_poet_name(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("poet_name cannot be empty")
        return v.strip()

    @field_validator("topic")
    @classmethod
    def validate_topic(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("topic cannot be empty")
        if len(v) > 500:
            raise ValueError("topic too long (max 500 characters)")
        return v.strip()


class GenerateResponse(BaseModel):
    """
    Response for POST /generate.
    poem          → the generated poem in poet's style
    style_notes   → what stylistic elements were used
    poet_profile  → brief note on the poet's actual style
    translation   → English translation if poem is in Kannada
    """
    poem: Optional[str] = None
    style_notes: Optional[str] = None
    poet_profile: Optional[str] = None
    translation: Optional[str] = None



# ─────────────────────────────────────────────────────────────
# GROUP C — NEW MODELS
# Add these to the bottom of schemas.py
# ─────────────────────────────────────────────────────────────

from typing import List   # already imported above, just confirming

# ── 1. Poem data model (for API responses) ────────────────────

class PoemData(BaseModel):
    """
    Represents a single poem returned from the poems API.
    Matches the structure in data/poems_data.py.
    """
    id: int
    title_en: str
    title_kn: str
    poet: str
    text: str
    category: str
    difficulty: str
    is_featured: bool
    tags: List[str]
    era: str


# ── 2. Poems list response ────────────────────────────────────

class PoemsListResponse(BaseModel):
    """
    Paginated response for GET /poems.
    """
    poems: List[PoemData]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool


# ── 3. Poems metadata response ────────────────────────────────

class PoemsMetaResponse(BaseModel):
    """
    Response for GET /poems/meta.
    Returns all available categories and poets for filter dropdowns.
    """
    categories: List[str]
    poets: List[str]
    total_poems: int


# ── 4. Difficulty scorer ──────────────────────────────────────

class DifficultyRequest(BaseModel):
    """
    POST /difficulty
    Asks AI to rate how difficult a poem is to understand.
    """
    poem_text: str
    language: str = "en"

    @field_validator("language")
    @classmethod
    def validate_language(cls, v: str) -> str:
        if v not in {"en", "kn"}:
            raise ValueError(f"language must be 'en' or 'kn', got '{v}'")
        return v

    @field_validator("poem_text")
    @classmethod
    def validate_poem_text(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("poem_text cannot be empty")
        if len(v) > 5000:
            raise ValueError("poem_text too long (max 5000 characters)")
        return v.strip()


class DifficultyResponse(BaseModel):
    """
    Response for POST /difficulty.
    level        → Easy / Medium / Hard
    score        → numeric score 1-10
    reasoning    → why this difficulty was assigned
    hard_words   → words that make it difficult
    suggestions  → what to study before reading this poem
    """
    level: Optional[str] = None
    score: Optional[int] = None
    reasoning: Optional[str] = None
    hard_words: Optional[str] = None
    suggestions: Optional[str] = None


# ── 5. Transliteration ────────────────────────────────────────

class TransliterateRequest(BaseModel):
    """
    POST /transliterate
    Converts Kannada script to Roman (IAST or readable) transliteration.
    Also supports Roman → Kannada direction.
    """
    text: str
    direction: str = "kn_to_roman"   # "kn_to_roman" | "roman_to_kn"
    style: str = "readable"           # "readable" | "iast" (scholarly)

    @field_validator("direction")
    @classmethod
    def validate_direction(cls, v: str) -> str:
        allowed = {"kn_to_roman", "roman_to_kn"}
        if v not in allowed:
            raise ValueError(f"direction must be one of {allowed}, got '{v}'")
        return v

    @field_validator("style")
    @classmethod
    def validate_style(cls, v: str) -> str:
        allowed = {"readable", "iast"}
        if v not in allowed:
            raise ValueError(f"style must be one of {allowed}, got '{v}'")
        return v

    @field_validator("text")
    @classmethod
    def validate_text(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("text cannot be empty")
        if len(v) > 2000:
            raise ValueError("text too long (max 2000 characters)")
        return v.strip()


class TransliterateResponse(BaseModel):
    """
    Response for POST /transliterate.
    original         → the input text
    transliterated   → the converted text
    direction        → which direction was used
    pronunciation_guide → how to pronounce key sounds
    """
    original: Optional[str] = None
    transliterated: Optional[str] = None
    direction: Optional[str] = None
    pronunciation_guide: Optional[str] = None
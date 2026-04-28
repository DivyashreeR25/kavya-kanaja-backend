"""
Groq API service layer.
UPDATED (Group C): Added 2 new service methods — difficulty and transliterate.
"""

import json
import logging
from groq import Groq, APIError, APIConnectionError, RateLimitError

from models.schemas import (
    ExplainRequest, ExplainResponse,
    StoryRequest, StoryResponse,
    PoetRequest, PoetResponse,
    QuizRequest, QuizResponse, QuizQuestion, TrueFalseQuestion,
    DialogueRequest, DialogueResponse,
    GenerateRequest, GenerateResponse,
    DifficultyRequest, DifficultyResponse,      # NEW
    TransliterateRequest, TransliterateResponse, # NEW
)
from prompts.poetry_prompts import (
    get_full_explanation_prompt,
    get_word_meaning_prompt,
    get_emotion_prompt,
    get_lesson_prompt,
    get_simplify_prompt,
    get_modernize_prompt,
    get_visualize_prompt,
    get_background_prompt,
    get_story_prompt,
    get_poet_profile_prompt,
    get_quiz_prompt,
    get_dialogue_prompt,
    get_generate_poem_prompt,
    get_difficulty_prompt,       # NEW
    get_transliterate_prompt,    # NEW
    get_system_prompt,
)

logger = logging.getLogger(__name__)


class GroqService:

    MODEL = "llama-3.3-70b-versatile"
    MAX_TOKENS = 1500
    TEMPERATURE = 0.3

    def __init__(self, api_key: str):
        self.client = Groq(api_key=api_key)
        logger.info(f"GroqService initialized with model: {self.MODEL}")

    # ── ALL ORIGINAL + GROUP B METHODS (unchanged) ────────────
    # Keep explain(), generate_story(), get_poet_profile(),
    # generate_quiz(), generate_dialogue(), generate_poem()
    # exactly as they were — paste them here unchanged

    async def explain(self, request: ExplainRequest) -> ExplainResponse:
        mode = request.mode
        text = request.text
        lang = request.language

        if mode == "full":
            user_prompt = get_full_explanation_prompt(text, lang)
        elif mode == "word":
            user_prompt = get_word_meaning_prompt(text, lang)
        elif mode == "emotion":
            user_prompt = get_emotion_prompt(text, lang)
        elif mode == "lesson":
            user_prompt = get_lesson_prompt(text, lang)
        elif mode == "simplify":
            user_prompt = get_simplify_prompt(text, lang)
        elif mode == "modernize":
            user_prompt = get_modernize_prompt(text, lang)
        elif mode == "visualize":
            user_prompt = get_visualize_prompt(text, lang)
        elif mode == "background":
            user_prompt = get_background_prompt(text, lang)
        else:
            raise ValueError(f"Unknown mode: {mode}")

        logger.info(f"explain | mode={mode} | lang={lang} | len={len(text)}")
        raw = await self._call_groq(user_prompt)
        parsed = self._parse_json_response(raw)

        return ExplainResponse(
            meaning=parsed.get("meaning"),
            line_explanation=parsed.get("line_explanation"),
            word_meanings=parsed.get("word_meanings"),
            theme=parsed.get("theme"),
            summary=parsed.get("summary"),
            story=parsed.get("story"),
        )

    async def generate_story(self, request: StoryRequest) -> StoryResponse:
        logger.info(f"generate_story | style={request.style} | lang={request.language}")
        prompt = get_story_prompt(request.poem_text, request.language, request.style)
        raw = await self._call_groq(prompt, temperature=0.7)
        parsed = self._parse_json_response(raw)
        return StoryResponse(
            title=parsed.get("title"),
            story=parsed.get("story"),
            characters=parsed.get("characters"),
            moral=parsed.get("moral"),
            setting=parsed.get("setting"),
        )

    async def get_poet_profile(self, request: PoetRequest) -> PoetResponse:
        logger.info(f"get_poet_profile | poet={request.poet_name}")
        prompt = get_poet_profile_prompt(request.poet_name, request.language)
        raw = await self._call_groq(prompt, temperature=0.2)
        parsed = self._parse_json_response(raw)
        return PoetResponse(
            name=parsed.get("name"),
            biography=parsed.get("biography"),
            writing_style=parsed.get("writing_style"),
            famous_works=parsed.get("famous_works"),
            era=parsed.get("era"),
            fun_fact=parsed.get("fun_fact"),
            simple_intro=parsed.get("simple_intro"),
        )

    async def generate_quiz(self, request: QuizRequest) -> QuizResponse:
        logger.info(f"generate_quiz | difficulty={request.difficulty}")
        prompt = get_quiz_prompt(
            request.poem_text, request.language,
            request.num_questions, request.difficulty
        )
        raw = await self._call_groq(prompt, temperature=0.4, max_tokens=2000)
        parsed = self._parse_json_response(raw)

        mcq_list = []
        for q in parsed.get("mcq_questions", []):
            try:
                mcq_list.append(QuizQuestion(
                    question=q.get("question", ""),
                    option_a=q.get("option_a", ""),
                    option_b=q.get("option_b", ""),
                    option_c=q.get("option_c", ""),
                    option_d=q.get("option_d", ""),
                    correct_answer=q.get("correct_answer", "A"),
                    explanation=q.get("explanation", ""),
                ))
            except Exception as e:
                logger.warning(f"Skipping malformed MCQ: {e}")

        tf_list = []
        for q in parsed.get("tf_questions", []):
            try:
                answer_raw = q.get("answer", True)
                answer = answer_raw.lower() == "true" if isinstance(answer_raw, str) else bool(answer_raw)
                tf_list.append(TrueFalseQuestion(
                    statement=q.get("statement", ""),
                    answer=answer,
                    explanation=q.get("explanation", ""),
                ))
            except Exception as e:
                logger.warning(f"Skipping malformed T/F: {e}")

        return QuizResponse(
            mcq_questions=mcq_list or None,
            tf_questions=tf_list or None,
            poem_summary=parsed.get("poem_summary"),
            difficulty=parsed.get("difficulty", request.difficulty),
        )

    async def generate_dialogue(self, request: DialogueRequest) -> DialogueResponse:
        logger.info(f"generate_dialogue | characters={request.num_characters}")
        prompt = get_dialogue_prompt(
            request.poem_text, request.language, request.num_characters
        )
        raw = await self._call_groq(prompt, temperature=0.7, max_tokens=2000)
        parsed = self._parse_json_response(raw)
        return DialogueResponse(
            characters=parsed.get("characters"),
            dialogue=parsed.get("dialogue"),
            setting=parsed.get("setting"),
            stage_notes=parsed.get("stage_notes"),
            theme=parsed.get("theme"),
        )

    async def generate_poem(self, request: GenerateRequest) -> GenerateResponse:
        logger.info(f"generate_poem | poet={request.poet_name} | topic={request.topic}")
        prompt = get_generate_poem_prompt(
            request.poet_name, request.topic,
            request.language, request.length
        )
        raw = await self._call_groq(prompt, temperature=0.9)
        parsed = self._parse_json_response(raw)
        return GenerateResponse(
            poem=parsed.get("poem"),
            style_notes=parsed.get("style_notes"),
            poet_profile=parsed.get("poet_profile"),
            translation=parsed.get("translation"),
        )

    # ── GROUP C — NEW METHODS ─────────────────────────────────

    async def score_difficulty(
        self, request: DifficultyRequest
    ) -> DifficultyResponse:
        """
        Rates the difficulty of a Kannada poem.
        Uses low temperature for consistent, factual scoring.
        """
        logger.info(
            f"score_difficulty | lang={request.language} | "
            f"len={len(request.poem_text)}"
        )

        prompt = get_difficulty_prompt(
            poem_text=request.poem_text,
            language=request.language,
        )

        # Low temperature for consistent scoring
        raw = await self._call_groq(prompt, temperature=0.2)
        parsed = self._parse_json_response(raw)

        # Safely parse the score — LLM might return string instead of int
        score_raw = parsed.get("score", 5)
        try:
            score = int(score_raw)
            score = max(1, min(10, score))   # clamp to 1-10
        except (ValueError, TypeError):
            score = 5                         # default to medium if parse fails

        return DifficultyResponse(
            level=parsed.get("level"),
            score=score,
            reasoning=parsed.get("reasoning"),
            hard_words=parsed.get("hard_words"),
            suggestions=parsed.get("suggestions"),
        )

    async def transliterate(
        self, request: TransliterateRequest
    ) -> TransliterateResponse:
        """
        Converts Kannada script to Roman or Roman to Kannada.
        Uses very low temperature for accuracy and consistency.
        """
        logger.info(
            f"transliterate | direction={request.direction} | "
            f"style={request.style} | len={len(request.text)}"
        )

        prompt = get_transliterate_prompt(
            text=request.text,
            direction=request.direction,
            style=request.style,
        )

        # Very low temperature — this is linguistic conversion, not creative
        raw = await self._call_groq(prompt, temperature=0.1)
        parsed = self._parse_json_response(raw)

        return TransliterateResponse(
            original=parsed.get("original", request.text),
            transliterated=parsed.get("transliterated"),
            direction=parsed.get("direction", request.direction),
            pronunciation_guide=parsed.get("pronunciation_guide"),
        )

    # ── PRIVATE HELPERS (unchanged from Group B) ──────────────

    async def _call_groq(
        self,
        user_prompt: str,
        temperature: float = None,
        max_tokens: int = None,
    ) -> str:
        try:
            completion = self.client.chat.completions.create(
                model=self.MODEL,
                messages=[
                    {"role": "system", "content": get_system_prompt()},
                    {"role": "user",   "content": user_prompt},
                ],
                max_tokens=max_tokens or self.MAX_TOKENS,
                temperature=temperature if temperature is not None else self.TEMPERATURE,
                response_format={"type": "json_object"},
            )
        except RateLimitError as e:
            logger.warning(f"Groq rate limit: {e}")
            raise RuntimeError("The AI service is busy. Please try again.")
        except APIConnectionError as e:
            logger.error(f"Groq connection error: {e}")
            raise RuntimeError("Could not connect to AI service.")
        except APIError as e:
            logger.error(f"Groq API error: {e}")
            raise RuntimeError(f"AI service error: {str(e)}")

        raw = completion.choices[0].message.content
        if not raw:
            raise ValueError("AI returned empty response. Please try again.")
        logger.debug(f"Groq response preview: {raw[:200]}")
        return raw

    def _parse_json_response(self, raw: str) -> dict:
        cleaned = raw.strip()
        if cleaned.startswith("```"):
            lines = cleaned.split("\n")
            cleaned = "\n".join(lines[1:-1]).strip()
        try:
            return json.loads(cleaned)
        except json.JSONDecodeError as e:
            logger.error(f"JSON parse error: {e} | Response: {cleaned[:300]}")
            raise ValueError("AI returned unexpected format. Please try again.")
"""
Prompt templates for Kavya-Kanaja AI features.

UPDATED (Group A):
  Added 6 new prompt functions:
  - get_emotion_prompt()     → emotion + tone detection
  - get_lesson_prompt()      → life lesson / moral extractor
  - get_simplify_prompt()    → explain like reader is 10 years old
  - get_modernize_prompt()   → rewrite in modern Kannada
  - get_visualize_prompt()   → scene / imagery description
  - get_background_prompt()  → historical context of poem

All prompts follow the same rules:
  1. Return ONLY valid JSON — no markdown, no extra text
  2. Respond in the language specified (en or kn)
  3. Use the same ExplainResponse JSON shape throughout
  4. Be beginner-friendly and culturally respectful
"""


# ─────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────

def _lang_instruction(language: str) -> str:
    """Returns the language instruction line for any prompt."""
    if language == "kn":
        return (
            "ಉತ್ತರವನ್ನು ಸಂಪೂರ್ಣವಾಗಿ ಕನ್ನಡದಲ್ಲಿ ನೀಡಿ. "
            "(Respond entirely in Kannada.)"
        )
    return "Respond entirely in English."


def _json_rules(language: str) -> str:
    """Common rules block injected into every prompt."""
    return f"""CRITICAL RULES:
1. Return ONLY valid JSON. No markdown, no code blocks, no text outside the JSON.
2. {_lang_instruction(language)}
3. Write in simple, clear language suitable for students.
4. Be culturally respectful of Kannada literary traditions.
5. Every JSON value must be a plain string (no nested objects, no arrays)."""


def get_system_prompt() -> str:
    """
    System prompt sent on every request.
    Sets the AI's global role and behaviour.
    """
    return (
        "You are a Kannada poetry expert and literature teacher. "
        "You help students understand Kannada poems with clear, "
        "culturally respectful, and beginner-friendly explanations. "
        "You ALWAYS respond with valid JSON and nothing else. "
        "Never include markdown, code fences, or text outside the JSON object."
    )


# ─────────────────────────────────────────────────────────────
# ORIGINAL PROMPTS (unchanged)
# ─────────────────────────────────────────────────────────────

def get_full_explanation_prompt(poem_text: str, language: str) -> str:
    """Full structured explanation of a poem."""
    return f"""You are an expert Kannada literature teacher.
Analyze the given Kannada poem and return a structured JSON explanation.

{_json_rules(language)}

Return this exact JSON structure:
{{
    "meaning": "Simple overall meaning in 2-3 sentences.",
    "line_explanation": "Line by line explanation. Use: 1. [line] - [meaning]. 2. [line] - [meaning].",
    "word_meanings": "Important words and meanings. Format: word1 = meaning1, word2 = meaning2.",
    "theme": "Central theme or message in 1-2 sentences.",
    "summary": "Flowing summary in 3-5 sentences.",
    "story": "Background story or legend if any. Empty string if none."
}}

Analyze this Kannada poem:
\"\"\"{poem_text}\"\"\""""


def get_word_meaning_prompt(word: str, language: str) -> str:
    """Meaning of a single Kannada word."""
    return f"""You are an expert Kannada language teacher.
Explain the meaning of a Kannada word in the context of classical poetry.

{_json_rules(language)}

Return this exact JSON structure:
{{
    "meaning": "1) Literal meaning. 2) Poetic usage. 3) Alternative meanings. Under 100 words.",
    "line_explanation": "",
    "word_meanings": "",
    "theme": "",
    "summary": "",
    "story": ""
}}

Explain this Kannada word: \"{word}\""""


# ─────────────────────────────────────────────────────────────
# GROUP A — NEW PROMPTS
# ─────────────────────────────────────────────────────────────

def get_emotion_prompt(poem_text: str, language: str) -> str:
    """
    FEATURE: Emotion Detection
    Detects the primary emotion, tone, and emotional intensity of a poem.

    Response fields used:
        meaning  → primary emotion label + one-line reason
        theme    → tone (philosophical / melancholic / joyful / devotional etc.)
        summary  → emotional intensity (low/medium/high) + what triggers it
        story    → advice: what mood to be in when reading this poem
    """
    return f"""You are an expert in Kannada literature and emotional analysis of poetry.
Analyze the emotional content of the given Kannada poem.

{_json_rules(language)}

Return this exact JSON structure:
{{
    "meaning": "Primary emotion of the poem (e.g. Hopeful, Melancholic, Devotional, Joyful, Philosophical, Nostalgic). Then in 1-2 sentences, explain why you identified this emotion.",
    "line_explanation": "Which specific lines or words carry the strongest emotion? List 2-3 examples with brief explanation.",
    "word_meanings": "",
    "theme": "Overall tone of the poem. Choose from: Philosophical / Devotional / Romantic / Melancholic / Patriotic / Nature-loving / Spiritual / Nostalgic / Celebratory. Explain in 1 sentence.",
    "summary": "Emotional intensity: Low / Medium / High. Explain what creates this intensity in the poem — imagery, word choice, rhythm, or subject matter.",
    "story": "Reading advice: What kind of mood or mindset should a reader bring to this poem? When is the best time to read it (morning reflection, difficult times, celebration etc.)?"
}}

Analyze the emotions in this Kannada poem:
\"\"\"{poem_text}\"\"\""""


def get_lesson_prompt(poem_text: str, language: str) -> str:
    """
    FEATURE: Life Lesson Extractor
    Extracts the moral, life lesson, and real-world application from a poem.

    Response fields used:
        meaning  → the core moral / lesson in one clear sentence
        theme    → the universal human value it represents
        summary  → how to apply this lesson in real daily life
        story    → a short modern real-life example that mirrors the poem's lesson
    """
    return f"""You are a Kannada literature teacher and life coach.
Extract the life lessons and moral wisdom from the given Kannada poem.

{_json_rules(language)}

Return this exact JSON structure:
{{
    "meaning": "The single most important life lesson or moral from this poem. State it as a clear, memorable principle in 1-2 sentences.",
    "line_explanation": "Which lines directly express this lesson? Quote 1-2 lines and explain how they convey the wisdom.",
    "word_meanings": "",
    "theme": "The universal human value this poem represents. Examples: Perseverance, Gratitude, Humility, Hope, Compassion, Self-awareness, Faith. Explain in 1 sentence.",
    "summary": "How can a student or young person apply this lesson in their daily life today? Give 2-3 practical, specific suggestions.",
    "story": "Give a short modern real-life scenario (3-5 sentences) that illustrates the same lesson the poem teaches. Make it relatable to a young Indian student."
}}

Extract life lessons from this Kannada poem:
\"\"\"{poem_text}\"\"\""""


def get_simplify_prompt(poem_text: str, language: str) -> str:
    """
    FEATURE: Simplify for Kids / Beginners
    Re-explains the poem as if the reader is 10 years old.
    No literary terms, no complex vocabulary.

    Response fields used:
        meaning          → super simple explanation of what the poem says
        line_explanation → each line explained in 1 simple sentence a child understands
        summary          → one single sentence summary a child can remember
        story            → a short fun comparison to make it memorable
    """
    return f"""You are a friendly Kannada teacher explaining poetry to a 10-year-old child.
Use very simple words. No difficult terms. Make it fun and easy to understand.

{_json_rules(language)}

Return this exact JSON structure:
{{
    "meaning": "What is this poem saying? Explain it simply as if talking to a 10-year-old. Use everyday words. No literary terms. 3-4 simple sentences.",
    "line_explanation": "Explain each line or couplet in ONE very simple sentence a child can understand. Use friendly, everyday language. Format: Line 1: [simple explanation]. Line 2: [simple explanation].",
    "word_meanings": "Are there any hard words in the poem? List them with super simple meanings a child would understand. Format: hard_word = simple meaning.",
    "theme": "",
    "summary": "Sum up the whole poem in ONE simple sentence. Like explaining it to your little sister or brother.",
    "story": "Compare this poem to something from a child's daily life — school, games, family, nature. Make a fun connection in 2-3 sentences to help them remember it."
}}

Explain this Kannada poem simply for a young child:
\"\"\"{poem_text}\"\"\""""


def get_modernize_prompt(poem_text: str, language: str) -> str:
    """
    FEATURE: Rewrite in Modern Language
    Converts classical/old Kannada into simple, modern everyday Kannada.
    Also explains what changed and why it was hard to understand originally.

    Response fields used:
        meaning          → the modern rewritten version of the poem
        line_explanation → original line vs modern version, side by side
        summary          → what made the original hard (archaic words, grammar etc.)
        story            → what was lost/changed in modernization (poetic nuance)
    """
    return f"""You are a Kannada language expert who specializes in modernizing classical Kannada poetry.
Convert the given poem into simple, modern everyday Kannada that anyone can understand today.

{_json_rules(language)}

Return this exact JSON structure:
{{
    "meaning": "The complete poem rewritten in modern, simple Kannada (or English if language=en). Keep the same meaning and emotion but use words people use today. Preserve the line structure.",
    "line_explanation": "Show the transformation line by line. Format: Original: [line] | Modern: [modernized line]. Do this for every line.",
    "word_meanings": "List all archaic, classical, or difficult words from the original with their modern equivalents. Format: old_word = modern_word.",
    "theme": "",
    "summary": "What made this poem difficult to understand in its original form? Explain the archaic grammar, old vocabulary, or classical references that needed modernizing.",
    "story": "What poetic beauty, rhythm, or nuance was present in the original that is harder to capture in the modern version? What did we gain and what did we lose in translation?"
}}

Modernize this Kannada poem into simple language:
\"\"\"{poem_text}\"\"\""""


def get_visualize_prompt(poem_text: str, language: str) -> str:
    """
    FEATURE: Scene / Poem Visualizer
    Converts poem into a rich visual description — what you would SEE
    if this poem were painted or filmed.

    Response fields used:
        meaning  → the main visual scene described in detail
        theme    → mood / atmosphere of the scene
        summary  → colour palette and lighting description
        story    → what a film director would do with this scene
    """
    return f"""You are a creative director and Kannada literature expert.
Read this poem and describe the visual scene it creates — as if painting it or filming it.

{_json_rules(language)}

Return this exact JSON structure:
{{
    "meaning": "Describe the main visual scene this poem creates. What do you SEE? Describe the location, people (if any), objects, nature elements. Be specific and vivid. 4-6 sentences.",
    "line_explanation": "Go through the poem and identify the key visual images line by line. What specific visual does each line create? Format: Line: [line] → Visual: [what you see].",
    "word_meanings": "",
    "theme": "What is the overall mood and atmosphere of this scene? (e.g. Peaceful and serene at golden hour / Dark and stormy with tension / Bright and celebratory). Describe the emotional atmosphere in 2-3 sentences.",
    "summary": "Describe the colour palette and lighting of this scene. What colours dominate? What time of day is it? What is the quality of light? (e.g. Warm amber tones of a setting sun, long shadows, soft diffused light...)",
    "story": "If a film director were to shoot this poem as a short film scene: What camera angles would they use? What sounds would be in the background? What would the opening shot look like? Describe in 4-5 sentences."
}}

Visualize the scene in this Kannada poem:
\"\"\"{poem_text}\"\"\""""


def get_background_prompt(poem_text: str, language: str) -> str:
    """
    FEATURE: Historical Background / Story Behind the Poem
    Explains the historical context, the poet's motivation,
    the era it was written in, and why it matters today.

    Response fields used:
        meaning  → why the poet wrote this poem (motivation/context)
        theme    → historical era and literary movement it belongs to
        summary  → why this poem is still relevant and important today
        story    → full historical background narrative
    """
    return f"""You are a Kannada literature historian and scholar.
Explain the historical background and context of the given poem.

{_json_rules(language)}

Return this exact JSON structure:
{{
    "meaning": "Why did the poet likely write this poem? What personal experience, historical event, social situation, or philosophical thought may have inspired it? Be specific. 3-4 sentences.",
    "line_explanation": "Are there any lines that have specific historical, cultural, or personal references? Identify them and explain what they refer to. If none, explain the broader cultural context the poem emerged from.",
    "word_meanings": "Are there any words that have specific historical, regional, or classical Kannada literary significance? List them with their historical context. Format: word = historical meaning/context.",
    "theme": "What literary era, movement, or school of thought does this poem belong to? (e.g. Navodaya movement, Navya poetry, Bandaya sahitya, Vachana tradition, Bhakti movement). Explain what that movement stood for.",
    "summary": "Why does this poem still matter today? What makes it timeless? How has its meaning or reception changed over time? 3-4 sentences.",
    "story": "Tell the complete historical story behind this poem in 5-8 sentences. Include: the poet's life situation when writing it, the historical period, any notable events connected to it, how it was received when first published, and its place in Kannada literary history."
}}

Explain the historical background of this Kannada poem:
\"\"\"{poem_text}\"\"\""""


# ─────────────────────────────────────────────────────────────
# GROUP B — NEW PROMPT FUNCTIONS
# Add these to the bottom of poetry_prompts.py
# ─────────────────────────────────────────────────────────────

def get_story_prompt(poem_text: str, language: str, style: str) -> str:
    """
    FEATURE: Poem → Story Generator
    Converts a Kannada poem into a short narrative story.

    style options:
        simple    → straightforward narrative for general readers
        dramatic  → theatrical, emotional, vivid storytelling
        children  → simple, fun, age-appropriate for kids
    """
    style_instructions = {
        "simple": (
            "Write a clear, engaging short story with a natural narrative flow. "
            "Suitable for general adult readers."
        ),
        "dramatic": (
            "Write a theatrical, emotionally rich story with vivid descriptions, "
            "tension, and powerful language. Make it feel like a film scene."
        ),
        "children": (
            "Write a simple, fun, and gentle story suitable for children aged 8-12. "
            "Use easy words, friendly characters, and a clear moral."
        ),
    }

    return f"""You are a creative Kannada literature expert and storyteller.
Convert the given Kannada poem into a meaningful short story.

{_json_rules(language)}

Story style: {style_instructions.get(style, style_instructions["simple"])}

Return this exact JSON structure:
{{
    "title": "A creative title for the story (not the same as the poem title).",
    "story": "The complete short story in 200-350 words. Include characters, setting, conflict, and resolution. The story should capture the emotion and message of the poem.",
    "characters": "List the characters in the story and their role. Format: Character Name: [role and brief description]. One per line.",
    "moral": "The moral or lesson of this story in one clear sentence.",
    "setting": "Where and when does this story take place? Describe the time period, location, and atmosphere in 2-3 sentences."
}}

Convert this Kannada poem into a story:
\"\"\"{poem_text}\"\"\""""


def get_poet_profile_prompt(poet_name: str, language: str) -> str:
    """
    FEATURE: Poet Intelligence Profile
    Returns a rich, structured profile of a Kannada poet.
    """
    return f"""You are a Kannada literature historian and scholar with deep knowledge
of all major Kannada poets from ancient times to the present day.

{_json_rules(language)}

Return this exact JSON structure:
{{
    "name": "Full name of the poet including any pen names or honorific titles they are known by.",
    "biography": "Life story in 4-6 sentences. Include: birth year and place, family background, education, major life events, death (if applicable), and awards/recognition received (especially Jnanpith Award if applicable).",
    "writing_style": "Describe how this poet writes in 3-4 sentences. What themes do they explore? What literary forms do they use (vachanas, sonnets, free verse, haiku-style)? What is their unique voice or signature? What language style — classical, modern, colloquial?",
    "famous_works": "List their 4-6 most famous poems, books, or works. Format: 1. [Work name] - [one line about it]. 2. [Work name] - [one line]. Continue for each work.",
    "era": "What literary era and movement do they belong to? (e.g. Navodaya, Navya, Bandaya, Vachana, Bhakti, contemporary). Explain what that movement stood for and how this poet fits into it. 2-3 sentences.",
    "fun_fact": "One surprising, interesting, or lesser-known fact about this poet that most people don't know.",
    "simple_intro": "Explain who this poet is to a complete beginner in exactly 2 sentences. Pretend you are introducing them to someone who has never heard of them."
}}

Generate a complete profile for this Kannada poet: \"{poet_name}\""""


def get_quiz_prompt(
    poem_text: str,
    language: str,
    num_questions: int,
    difficulty: str
) -> str:
    """
    FEATURE: Quiz Generator
    Generates MCQ and True/False questions from a poem.

    difficulty levels:
        easy   → basic comprehension, literal meaning
        medium → inference, theme, word meanings
        hard   → literary analysis, historical context, poetic devices
    """
    difficulty_guide = {
        "easy": (
            "Focus on literal comprehension: what the poem directly says, "
            "basic word meanings, and who/what/where questions."
        ),
        "medium": (
            "Focus on inference and interpretation: what the poem implies, "
            "theme identification, emotional tone, and key word meanings."
        ),
        "hard": (
            "Focus on literary analysis: poetic devices (metaphor, simile, alliteration), "
            "historical context, comparison with other works, and deep thematic analysis."
        ),
    }

    return f"""You are a Kannada literature teacher creating an exam question paper.
Generate quiz questions based on the given Kannada poem.

{_json_rules(language)}

Difficulty level: {difficulty.upper()} — {difficulty_guide.get(difficulty, "")}
Number of MCQ questions to generate: {num_questions}
Number of True/False questions to generate: 3 (always generate exactly 3)

Return this exact JSON structure:
{{
    "poem_summary": "A 2-3 sentence summary of the poem to help students answer questions.",
    "difficulty": "{difficulty}",
    "mcq_questions": [
        {{
            "question": "Clear question about the poem",
            "option_a": "First option",
            "option_b": "Second option",
            "option_c": "Third option",
            "option_d": "Fourth option",
            "correct_answer": "A",
            "explanation": "Why this answer is correct in 1-2 sentences."
        }}
    ],
    "tf_questions": [
        {{
            "statement": "A statement about the poem that is either true or false",
            "answer": true,
            "explanation": "Why this statement is true or false."
        }}
    ]
}}

IMPORTANT:
- Generate EXACTLY {num_questions} MCQ questions in the mcq_questions array
- Generate EXACTLY 3 True/False questions in the tf_questions array
- Make sure correct_answer is exactly one of: "A", "B", "C", or "D"
- Make sure answer in tf_questions is exactly true or false (boolean, not string)
- All questions must be directly based on the provided poem

Generate quiz questions for this Kannada poem:
\"\"\"{poem_text}\"\"\""""


def get_dialogue_prompt(
    poem_text: str,
    language: str,
    num_characters: int
) -> str:
    """
    FEATURE: Poem → Drama / Dialogue
    Converts a poem into a dramatic dialogue/script between characters.
    """
    character_note = {
        2: "Create exactly 2 characters who represent contrasting perspectives from the poem.",
        3: "Create exactly 3 characters — one who embodies the poem's main idea, one who questions it, and one who observes.",
        4: "Create exactly 4 characters representing different aspects of the poem's themes.",
    }

    return f"""You are a Kannada playwright and literature expert.
Convert the given Kannada poem into a dramatic dialogue script.

{_json_rules(language)}

{character_note.get(num_characters, character_note[2])}

Return this exact JSON structure:
{{
    "characters": "Introduce each character. Format:\\nCharacter 1 - [Name]: [Age, background, what they represent in context of the poem]\\nCharacter 2 - [Name]: [Age, background, what they represent]\\n(repeat for each character)",
    "setting": "Describe the scene where this dialogue takes place. Time period, location, atmosphere, and any important props or elements. 2-3 sentences.",
    "dialogue": "The complete dialogue script. Format:\\n[CHARACTER NAME]: [their dialogue line]\\n[OTHER CHARACTER]: [response]\\nContinue naturally for 15-25 exchanges. The dialogue should organically express the themes and emotions of the original poem.",
    "stage_notes": "Director's notes for performing this scene. How should each character speak? What emotions should they convey? Any important actions or movements? 3-4 sentences.",
    "theme": "The central theme or message expressed through this dialogue in 1-2 sentences."
}}

Convert this Kannada poem into a dramatic dialogue:
\"\"\"{poem_text}\"\"\""""


def get_generate_poem_prompt(
    poet_name: str,
    topic: str,
    language: str,
    length: str
) -> str:
    """
    FEATURE: Write Like Poet (Style Imitation)
    Generates a new poem on a given topic in the style of a Kannada poet.
    """
    length_guide = {
        "short":  "4 to 8 lines",
        "medium": "8 to 16 lines",
        "long":   "16 to 24 lines",
    }

    return f"""You are a creative Kannada poetry generator with deep knowledge of
Kannada literary traditions and individual poet styles.

{_json_rules(language)}

Generate a NEW original poem on the given topic, written in the distinctive
style of the specified Kannada poet. Study and imitate their:
- Vocabulary and word choices (classical vs colloquial)
- Rhythm and metre patterns
- Recurring themes and imagery
- Emotional tone and philosophical perspective
- Literary devices they commonly use

Poem length: {length_guide.get(length, "4 to 8 lines")}

Return this exact JSON structure:
{{
    "poem": "The complete newly generated poem in the style of {poet_name}. Write it in Kannada script if language=kn, or in English if language=en. Preserve the poet's characteristic style throughout.",
    "style_notes": "Explain what specific stylistic elements from {poet_name}'s writing you used in this poem. List 3-4 specific techniques: vocabulary choices, imagery patterns, structural elements, thematic approaches.",
    "poet_profile": "Brief 2-3 sentence reminder of {poet_name}'s actual writing style so the reader can appreciate how the generated poem reflects it.",
    "translation": "If the poem was written in Kannada, provide a faithful English translation here. If written in English, provide a Kannada transliteration here."
}}

Generate a {length} poem in the style of {poet_name} on this topic: \"{topic}\""""


# ─────────────────────────────────────────────────────────────
# GROUP C — NEW PROMPT FUNCTIONS
# Add these to the bottom of poetry_prompts.py
# ─────────────────────────────────────────────────────────────

def get_difficulty_prompt(poem_text: str, language: str) -> str:
    """
    FEATURE: Difficulty Scorer
    AI rates how hard a poem is to understand on a scale of 1-10,
    and gives a label of Easy / Medium / Hard with reasoning.

    Scoring criteria:
        Vocabulary complexity  — archaic, classical, or rare words
        Grammatical complexity — sentence structure, inversions
        Cultural references    — historical, mythological, regional
        Conceptual depth       — abstract vs concrete ideas
        Metre and rhythm       — classical forms vs free verse
    """
    return f"""You are a Kannada literature teacher who evaluates the difficulty
of poems for students ranging from beginners to advanced learners.

{_json_rules(language)}

Rate the difficulty of the given Kannada poem on these criteria:
1. Vocabulary (1-10): Are the words simple everyday words or rare/archaic?
2. Grammar (1-10): Is the sentence structure straightforward or complex?
3. Cultural references (1-10): Does it require deep cultural knowledge to understand?
4. Conceptual depth (1-10): Are the ideas concrete or highly abstract/philosophical?
5. Overall (1-10): Combined difficulty score

Return this exact JSON structure:
{{
    "level": "Easy OR Medium OR Hard — pick exactly one based on overall score (1-4=Easy, 5-7=Medium, 8-10=Hard)",
    "score": 6,
    "reasoning": "Explain in 3-4 sentences why you gave this difficulty rating. Mention specific words, concepts, or structures that contribute to the difficulty.",
    "hard_words": "List the most difficult words in the poem that a beginner would struggle with. Format: word1 = why it is hard, word2 = why it is hard. Leave empty string if poem is easy.",
    "suggestions": "What should a student know or study BEFORE reading this poem to understand it better? Give 2-3 specific suggestions (e.g. learn about a historical period, understand a philosophical concept, know a literary device)."
}}

IMPORTANT: The score field must be an integer between 1 and 10, not a string.

Rate the difficulty of this Kannada poem:
\"\"\"{poem_text}\"\"\""""


def get_transliterate_prompt(
    text: str,
    direction: str,
    style: str
) -> str:
    """
    FEATURE: Transliteration
    Converts between Kannada script and Roman script.

    Directions:
        kn_to_roman  → Kannada (ಕನ್ನಡ) to Roman (Kannada)
        roman_to_kn  → Roman to Kannada script

    Styles:
        readable  → easy phonetic for general readers (e.g. "namaskara")
        iast      → scholarly International Alphabet of Sanskrit Transliteration
    """
    if direction == "kn_to_roman":
        direction_instruction = (
            "Convert the given Kannada script text into Roman script transliteration. "
            "Preserve every word and line break from the original."
        )
    else:
        direction_instruction = (
            "Convert the given Roman transliteration back into Kannada script. "
            "Preserve every word and line break from the original."
        )

    style_instruction = (
        "Use simple, readable phonetic transliteration that any English speaker "
        "can attempt to pronounce. Prioritize readability over scholarly accuracy. "
        "Example: ಕನ್ನಡ → Kannada, ನಮಸ್ಕಾರ → Namaskara"
        if style == "readable"
        else
        "Use IAST (International Alphabet of Sanskrit Transliteration) — the "
        "scholarly standard. Use diacritical marks for accuracy. "
        "Example: ಕನ್ನಡ → Kannaḍa, ಅ → a, ಆ → ā, ಇ → i, ಈ → ī"
    )

    return f"""You are a Kannada linguistics expert specializing in script conversion
and transliteration between Kannada and Roman scripts.

{_json_rules("en")}

Task: {direction_instruction}
Style: {style_instruction}

Return this exact JSON structure:
{{
    "original": "The original input text exactly as provided",
    "transliterated": "The complete transliterated output. Preserve all line breaks using \\n. Every single word must be transliterated — do not skip any.",
    "direction": "{direction}",
    "pronunciation_guide": "For kn_to_roman: Explain how to pronounce 3-4 of the most unusual or tricky sounds in this text for an English speaker. For roman_to_kn: Explain what Kannada sounds the key letters represent. Keep it practical and under 80 words."
}}

Text to transliterate:
\"\"\"{text}\"\"\""""
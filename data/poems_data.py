"""
Kavya-Kanaja Poems Data Store.

This is the single source of truth for all poem data.
In a future version, this can be replaced with a database
(PostgreSQL, MongoDB) without changing any route or service code.

Structure:
    Each poem is a dict with:
    - id           : unique integer
    - title_en     : English title
    - title_kn     : Kannada title
    - poet         : poet's name
    - text         : full poem text in Kannada
    - category     : thematic category
    - difficulty   : easy / medium / hard
    - is_featured  : bool — used for daily poem rotation
    - tags         : list of searchable tags
    - era          : literary era the poem belongs to
"""

from datetime import date

# ── Full poem dataset ──────────────────────────────────────────────────────
POEMS = [
    {
        "id": 1,
        "title_en": "Manku Thimmana Kagga",
        "title_kn": "ಮಂಕುತಿಮ್ಮನ ಕಗ್ಗ",
        "poet": "D.V. Gundappa",
        "text": (
            "ಕತ್ತಲೆಯ ನಡುವೆ ಒಂದು ಕಿರಣ ಮೂಡಿತು,\n"
            "ಬಾಳಿನ ಬೆಳಕ ತೋರಿತು।\n"
            "ಎದೆಯ ತುಂಬ ಭರವಸೆ ತುಂಬಿತು,\n"
            "ಜೀವನ ಸಾರ್ಥಕ ಆಯಿತು॥"
        ),
        "category": "Philosophy",
        "difficulty": "medium",
        "is_featured": True,
        "tags": ["life", "hope", "light", "philosophy", "DVG"],
        "era": "Navodaya",
    },
    {
        "id": 2,
        "title_en": "Nature's Beauty",
        "title_kn": "ಪ್ರಕೃತಿಯ ಸೌಂದರ್ಯ",
        "poet": "Kuvempu",
        "text": (
            "ಹಸಿರು ಕಾಡಿನ ನಡುವೆ ಹಳ್ಳ ಹರಿಯಿತು,\n"
            "ಪಕ್ಷಿಗಳ ಹಾಡು ಕಿವಿಗೆ ತಾಗಿತು।\n"
            "ಗಾಳಿ ತಂಗಾಳಿ ಮನಸು ತಣಿಸಿತು,\n"
            "ಪ್ರಕೃತಿ ತಾಯಿ ಮಡಿಲಲ್ಲಿ ಮಲಗಿತು॥"
        ),
        "category": "Nature",
        "difficulty": "easy",
        "is_featured": False,
        "tags": ["nature", "birds", "forest", "peace", "Kuvempu"],
        "era": "Navodaya",
    },
    {
        "id": 3,
        "title_en": "Mother's Love",
        "title_kn": "ತಾಯಿಯ ಪ್ರೀತಿ",
        "poet": "Belagere Krishnasharma",
        "text": (
            "ತಾಯಿ ಪ್ರೀತಿ ಅಗಾಧ ಸಾಗರ,\n"
            "ಮಗುವ ನೋವು ಕಡಿಮೆ ಮಾಡುವ।\n"
            "ಕಷ್ಟದಲ್ಲಿ ಕೈ ಹಿಡಿದು ನಡೆಸುವ,\n"
            "ದೇವರ ರೂಪ ತಾಯಿ ಮಮತೆ॥"
        ),
        "category": "Family",
        "difficulty": "easy",
        "is_featured": False,
        "tags": ["mother", "love", "family", "devotion"],
        "era": "Modern",
    },
    {
        "id": 4,
        "title_en": "Motherland Karnataka",
        "title_kn": "ಕನ್ನಡ ನಾಡು",
        "poet": "Rashtrakavi Govind Pai",
        "text": (
            "ಕನ್ನಡ ನಾಡು ನಮ್ಮ ನಾಡು,\n"
            "ಕನ್ನಡ ತಾಯಿ ನಮ್ಮ ತಾಯಿ।\n"
            "ಇಲ್ಲಿನ ಮಣ್ಣು ಹೊನ್ನು ಮಣ್ಣು,\n"
            "ಕನ್ನಡಿಗರಾಗಿ ಬಾಳೋಣ ತಾಣ॥"
        ),
        "category": "Patriotic",
        "difficulty": "easy",
        "is_featured": False,
        "tags": ["Karnataka", "patriotic", "Kannada", "pride"],
        "era": "Navodaya",
    },
    {
        "id": 5,
        "title_en": "The Wandering Mind",
        "title_kn": "ಅಲೆಮಾರಿ ಮನಸು",
        "poet": "Kuvempu",
        "text": (
            "ಎಲ್ಲಿಗೆ ಹೋಗುವೆ ಮನವೆ ನೀನು,\n"
            "ಆಕಾಶದಾಚೆ ತಾರೆಗಳ ಕೂಡ।\n"
            "ನೆಲದ ಮೇಲೆ ನಿಲ್ಲಲಾರೆ,\n"
            "ಕನಸಿನ ದೋಣಿ ತೇಲುತಿಹೆ ಸದಾ॥"
        ),
        "category": "Philosophy",
        "difficulty": "medium",
        "is_featured": False,
        "tags": ["mind", "dreams", "wandering", "sky", "Kuvempu"],
        "era": "Navodaya",
    },
    {
        "id": 6,
        "title_en": "Rain Song",
        "title_kn": "ಮಳೆಯ ಗೀತೆ",
        "poet": "G.S. Shivarudrappa",
        "text": (
            "ಮಳೆ ಬಾ ಮಳೆ ಬಾ ಜೋರಾಗಿ ಬಾ,\n"
            "ಬಾನಿಂದ ಇಳಿದು ನೆಲ ತಣಿಸು ಬಾ।\n"
            "ಒಣಗಿದ ಭೂಮಿ ಹಸಿರಾಗಲಿ,\n"
            "ರೈತನ ಮನದ ಆಸೆ ಈಡೇರಲಿ॥"
        ),
        "category": "Nature",
        "difficulty": "easy",
        "is_featured": False,
        "tags": ["rain", "nature", "farmer", "hope", "seasons"],
        "era": "Navya",
    },
    {
        "id": 7,
        "title_en": "The Lamp of Knowledge",
        "title_kn": "ಜ್ಞಾನದ ದೀಪ",
        "poet": "D.V. Gundappa",
        "text": (
            "ಜ್ಞಾನದ ದೀಪ ಬೆಳಗಿಸು ಮನದಲ್ಲಿ,\n"
            "ಅಜ್ಞಾನದ ಕತ್ತಲ ಓಡಿಸು ದೂರ।\n"
            "ವಿದ್ಯೆಯ ಬೆಳಕಿನ ಹಾದಿಯಲ್ಲಿ,\n"
            "ಜೀವನ ಪಥ ಸರಳವಾಗಲಿ ಸದಾ॥"
        ),
        "category": "Education",
        "difficulty": "medium",
        "is_featured": False,
        "tags": ["knowledge", "education", "light", "wisdom", "DVG"],
        "era": "Navodaya",
    },
    {
        "id": 8,
        "title_en": "River of Time",
        "title_kn": "ಕಾಲದ ನದಿ",
        "poet": "Adiga",
        "text": (
            "ಕಾಲ ನದಿ ಹರಿಯುತಿದೆ ನಿರಂತರ,\n"
            "ನಿಲ್ಲದು ಯಾರಿಗೂ ಕಾಯದು ಎಂದಿಗೂ।\n"
            "ಇಂದನ್ನು ಬಾಳು ಪೂರ್ಣವಾಗಿ,\n"
            "ನಾಳೆಯ ಚಿಂತೆ ಬೇಡ ವ್ಯರ್ಥವಾಗಿ॥"
        ),
        "category": "Philosophy",
        "difficulty": "hard",
        "is_featured": False,
        "tags": ["time", "philosophy", "life", "present", "Navya"],
        "era": "Navya",
    },
]

# ── Helper functions used by routes/poems.py ───────────────────────────────

def get_all_poems(
    search: str = "",
    category: str = "",
    difficulty: str = "",
    poet: str = "",
    page: int = 1,
    page_size: int = 10,
) -> dict:
    """
    Returns a filtered, paginated list of poems.

    Args:
        search     : search string — matches title (en/kn), poet, tags
        category   : filter by category (exact match, case-insensitive)
        difficulty : filter by difficulty (easy/medium/hard)
        poet       : filter by poet name (partial match)
        page       : page number (1-based)
        page_size  : number of poems per page (max 20)

    Returns:
        dict with poems list, total count, page info
    """
    results = POEMS.copy()

    # ── Filter: search ────────────────────────────────────────────────────
    if search:
        q = search.lower()
        results = [
            p for p in results
            if q in p["title_en"].lower()
            or q in p["title_kn"]
            or q in p["poet"].lower()
            or any(q in tag.lower() for tag in p["tags"])
        ]

    # ── Filter: category ──────────────────────────────────────────────────
    if category:
        results = [
            p for p in results
            if p["category"].lower() == category.lower()
        ]

    # ── Filter: difficulty ────────────────────────────────────────────────
    if difficulty:
        results = [
            p for p in results
            if p["difficulty"].lower() == difficulty.lower()
        ]

    # ── Filter: poet ──────────────────────────────────────────────────────
    if poet:
        results = [
            p for p in results
            if poet.lower() in p["poet"].lower()
        ]

    # ── Pagination ────────────────────────────────────────────────────────
    total = len(results)
    page_size = min(page_size, 20)      # cap at 20 per page
    start = (page - 1) * page_size
    end = start + page_size
    paginated = results[start:end]

    return {
        "poems": paginated,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": max(1, (total + page_size - 1) // page_size),
        "has_next": end < total,
        "has_prev": page > 1,
    }


def get_poem_by_id(poem_id: int) -> dict | None:
    """Returns a single poem by ID, or None if not found."""
    return next((p for p in POEMS if p["id"] == poem_id), None)


def get_daily_poem() -> dict:
    """
    Returns today's featured poem using deterministic date-based rotation.

    Logic:
    - Get all featured poems first
    - If none are featured, use entire list
    - Use today's date as a seed to pick a poem
    - Same poem all day, changes at midnight — no DB needed
    """
    featured = [p for p in POEMS if p.get("is_featured")]
    pool = featured if featured else POEMS

    # Use day-of-year as index — deterministic, changes daily
    day_of_year = date.today().timetuple().tm_yday
    index = day_of_year % len(pool)
    return pool[index]


def get_all_categories() -> list[str]:
    """Returns sorted list of unique categories."""
    return sorted(set(p["category"] for p in POEMS))


def get_all_poets() -> list[str]:
    """Returns sorted list of unique poet names."""
    return sorted(set(p["poet"] for p in POEMS))


def get_related_poems(poem_id: int, limit: int = 3) -> list[dict]:
    """
    Returns related poems based on shared category and tags.
    Excludes the current poem from results.

    Scoring:
        +2 points for same category
        +1 point for each shared tag
    Sorted by score descending.
    """
    current = get_poem_by_id(poem_id)
    if not current:
        return []

    scored = []
    for poem in POEMS:
        if poem["id"] == poem_id:
            continue
        score = 0
        if poem["category"] == current["category"]:
            score += 2
        shared_tags = set(poem["tags"]) & set(current["tags"])
        score += len(shared_tags)
        if score > 0:
            scored.append((score, poem))

    # Sort by score descending, return top `limit`
    scored.sort(key=lambda x: x[0], reverse=True)
    return [poem for _, poem in scored[:limit]]
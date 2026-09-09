from rapidfuzz import fuzz

from src.normalization import normalize_title


def calculate_similarity(title1: str, title2: str) -> float:
    """
    Calculate a similarity percentage between two titles.

    Uses character-level and token-order similarity so that
    minor spelling and word-order variations are detected.
    """

    normalized1 = normalize_title(title1)
    normalized2 = normalize_title(title2)

    if not normalized1 or not normalized2:
        return 0.0

    character_score = fuzz.ratio(normalized1, normalized2)
    token_score = fuzz.token_sort_ratio(normalized1, normalized2)

    combined_score = (
        character_score * 0.6
        + token_score * 0.4
    )

    return round(combined_score, 2)

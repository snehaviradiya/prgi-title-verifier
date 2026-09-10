from src.normalization import normalize_title


# Common words/phrases that have equivalent meanings.
# This is intentionally small for the MVP and can be expanded later.
SEMANTIC_GROUPS = {
    "daily": {
        "daily",
        "pratidin",
        "dainik",
        "roj",
    },
    "evening": {
        "evening",
        "sandhya",
        "sham",
        "shaam",
    },
    "morning": {
        "morning",
        "subah",
        "prabhat",
    },
    "news": {
        "news",
        "samachar",
        "khabar",
        "akhbar",
    },
    "india": {
        "india",
        "bharat",
    },
}


def semantic_token(word: str) -> str:
    """
    Convert a word into its shared semantic group.
    """

    for group, words in SEMANTIC_GROUPS.items():
        if word in words:
            return group

    return word


def semantic_normalize(title: str) -> str:
    """
    Convert a title into a language-independent representation.
    """

    normalized = normalize_title(title)

    tokens = [
        semantic_token(word)
        for word in normalized.split()
    ]

    return " ".join(tokens)


def semantic_similarity(title1: str, title2: str) -> float:
    """
    Calculate a simple semantic similarity percentage.

    This MVP compares the normalized semantic token sets.
    """

    tokens1 = set(semantic_normalize(title1).split())
    tokens2 = set(semantic_normalize(title2).split())

    if not tokens1 or not tokens2:
        return 0.0

    intersection = tokens1.intersection(tokens2)
    union = tokens1.union(tokens2)

    return round((len(intersection) / len(union)) * 100, 2)


def find_semantic_match(title1: str, title2: str) -> bool:
    return semantic_similarity(title1, title2) >= 80


if __name__ == "__main__":
    examples = [
        ("Daily Evening", "Pratidin Sandhya"),
        ("Morning News", "Prabhat Samachar"),
        ("India News", "Bharat Samachar"),
        ("India Today", "Completely Different"),
    ]

    for first, second in examples:
        print(
            f"{first} <-> {second}: "
            f"{semantic_normalize(first)} / "
            f"{semantic_normalize(second)} "
            f"-> {semantic_similarity(first, second)}%"
        )
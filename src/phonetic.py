from metaphone import doublemetaphone

from src.normalization import normalize_title


def phonetic_key(title: str) -> str:
    """
    Generate a phonetic key for a title.

    Double Metaphone helps identify titles that sound
    similar despite spelling differences.
    """

    normalized = normalize_title(title)

    if not normalized:
        return ""

    words = normalized.split()

    keys = []

    for word in words:
        primary, secondary = doublemetaphone(word)

        if primary:
            keys.append(primary)
        elif secondary:
            keys.append(secondary)

    return " ".join(keys)


def phonetic_similarity(title1: str, title2: str) -> float:
    """
    Return a simple phonetic similarity percentage.

    100 means the generated phonetic representations match.
    """

    key1 = phonetic_key(title1)
    key2 = phonetic_key(title2)

    if not key1 or not key2:
        return 0.0

    if key1 == key2:
        return 100.0

    return 0.0


if __name__ == "__main__":
    examples = [
        ("Hindu", "Hindoo"),
        ("India", "Indya"),
        ("Namaskar", "Namaskaar"),
    ]

    for first, second in examples:
        print(
            f"{first} vs {second}: "
            f"{phonetic_key(first)} / {phonetic_key(second)} "
            f"-> {phonetic_similarity(first, second)}%"
        )
RESTRICTED_WORDS = {
    "police",
    "crime",
    "corruption",
    "cbi",
    "cid",
    "army",
}


def find_restricted_words(title: str) -> list[str]:
    words = title.lower().split()

    found = []

    for word in words:
        if word in RESTRICTED_WORDS:
            found.append(word)

    return found


def validate_restricted_words(title: str) -> dict:
    restricted_words = find_restricted_words(title)

    return {
        "valid": len(restricted_words) == 0,
        "restricted_words": restricted_words,
    }
PREFIXES = [
    "the",
    "new",
    "daily",
    "weekly",
    "monthly",
]

SUFFIXES = [
    "news",
    "times",
    "today",
    "india",
    "express",
]

RESTRICTED_WORDS = {
    "police",
    "crime",
    "corruption",
    "cbi",
    "cid",
    "army",
}


def extract_prefix(title: str) -> str:
    words = title.lower().strip().split()

    if not words:
        return ""

    if words[0] in PREFIXES:
        return words[0]

    return ""


def extract_suffix(title: str) -> str:
    words = title.lower().strip().split()

    if not words:
        return ""

    if words[-1] in SUFFIXES:
        return words[-1]

    return ""


def check_prefix_suffix(title: str) -> dict:
    return {
        "prefix": extract_prefix(title),
        "suffix": extract_suffix(title),
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
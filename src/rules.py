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
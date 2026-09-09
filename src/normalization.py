import re
import unicodedata


def normalize_title(title: str) -> str:
    """
    Normalize a title for comparison.

    Steps:
    - Convert Unicode characters to a standard form
    - Convert to lowercase
    - Remove punctuation
    - Normalize whitespace
    """

    if not title:
        return ""

    # Unicode normalization
    title = unicodedata.normalize("NFKC", title)

    # Lowercase
    title = title.lower()

    # Replace punctuation/special characters with spaces
    title = re.sub(r"[^\w\s]", " ", title, flags=re.UNICODE)

    # Normalize whitespace
    title = re.sub(r"\s+", " ", title)

    return title.strip()


if __name__ == "__main__":
    examples = [
        "Namaskar",
        "NAMASKAR",
        "Namaskar!",
        "  Namaskar  ",
        "Namas-kar",
        "India   Today",
    ]

    for example in examples:
        print(f"{example!r} -> {normalize_title(example)!r}")
from src.database import get_connection
from src.normalization import normalize_title


def get_title_words(title: str) -> set[str]:
    normalized = normalize_title(title)

    return {
        word
        for word in normalized.split()
        if len(word) > 2
    }


def find_title_combinations(title: str) -> list[dict]:
    """
    Detect whether a proposed title appears to combine
    significant words from multiple existing titles.
    """

    proposed_words = get_title_words(title)

    if not proposed_words:
        return []

    connection = get_connection()

    rows = connection.execute(
        """
        SELECT id, title, normalized_title
        FROM titles
        """
    ).fetchall()

    connection.close()

    matches = []

    for row in rows:
        existing_words = get_title_words(row[2])
        overlap = proposed_words.intersection(existing_words)

        if overlap:
            matches.append(
                {
                    "id": row[0],
                    "title": row[1],
                    "overlap": sorted(overlap),
                }
            )

    return matches


def detect_combination(title: str) -> dict:
    matches = find_title_combinations(title)

    unique_titles = {
        match["title"]
        for match in matches
    }

    return {
        "detected": len(unique_titles) >= 2,
        "matching_titles": sorted(unique_titles),
    }


if __name__ == "__main__":
    result = detect_combination("Hindu Indian Express")

    print("Combination detected:", result["detected"])
    print("Matching titles:")

    for title in result["matching_titles"]:
        print(f"- {title}")
        
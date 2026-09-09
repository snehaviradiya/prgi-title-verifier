from src.database import get_connection
from src.normalization import normalize_title


PERIODICITY_WORDS = {
    "daily",
    "weekly",
    "monthly",
    "fortnightly",
    "quarterly",
}


def remove_periodicity(title: str) -> str:
    """
    Remove recognized periodicity words from a title.
    """

    words = normalize_title(title).split()

    remaining = [
        word
        for word in words
        if word not in PERIODICITY_WORDS
    ]

    return " ".join(remaining)


def find_periodicity_matches(title: str) -> list[dict]:
    """
    Check whether removing a periodicity word makes the
    proposed title match an existing title.
    """

    normalized = normalize_title(title)
    base_title = remove_periodicity(title)

    if not normalized or base_title == normalized:
        return []

    connection = get_connection()

    rows = connection.execute(
        """
        SELECT id, title, normalized_title
        FROM titles
        WHERE normalized_title = ?
        """,
        (base_title,),
    ).fetchall()

    connection.close()

    return [
        {
            "id": row[0],
            "title": row[1],
        }
        for row in rows
    ]


def detect_periodicity_modification(title: str) -> dict:
    matches = find_periodicity_matches(title)

    return {
        "detected": len(matches) > 0,
        "matching_titles": [
            match["title"]
            for match in matches
        ],
    }


if __name__ == "__main__":
    examples = [
        "Daily India Today",
        "Weekly The Hindu",
        "Monthly Indian Express",
        "India Today",
    ]

    for example in examples:
        result = detect_periodicity_modification(example)

        print(
            f"{example}: "
            f"{result['detected']} "
            f"{result['matching_titles']}"
        )
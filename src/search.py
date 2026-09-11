from src.database import get_connection
from src.normalization import normalize_title
from src.phonetic import phonetic_key
from src.similarity import calculate_similarity


def search_candidates(title: str, limit: int = 20):
    """
    Find potentially similar existing titles and
    pending applications.
    """

    normalized = normalize_title(title)
    phonetic = phonetic_key(title)

    if not normalized:
        return []

    connection = get_connection()

    title_rows = connection.execute(
        """
        SELECT id, title, normalized_title, phonetic_key, source
        FROM titles
        WHERE normalized_title LIKE ?
           OR phonetic_key LIKE ?
        LIMIT ?
        """,
        (
            f"%{normalized}%",
            f"%{phonetic}%",
            limit,
        ),
    ).fetchall()

    application_rows = connection.execute(
        """
        SELECT id, title, normalized_title, phonetic_key
        FROM applications
        WHERE status = 'PENDING'
          AND (
              normalized_title LIKE ?
              OR phonetic_key LIKE ?
          )
        LIMIT ?
        """,
        (
            f"%{normalized}%",
            f"%{phonetic}%",
            limit,
        ),
    ).fetchall()

    connection.close()

    results = []

    for row in title_rows:
        similarity = calculate_similarity(
            normalized,
            row[2],
        )

        results.append(
            {
                "id": row[0],
                "title": row[1],
                "similarity": similarity,
                "source": row[4],
                "type": "existing",
            }
        )

    for row in application_rows:
        similarity = calculate_similarity(
            normalized,
            row[2],
        )

        results.append(
            {
                "id": row[0],
                "title": row[1],
                "similarity": similarity,
                "source": "Pending Application",
                "type": "application",
            }
        )

    results.sort(
        key=lambda item: item["similarity"],
        reverse=True,
    )

    return results[:limit]


if __name__ == "__main__":
    results = search_candidates("India Today")

    for result in results:
        print(
            f"{result['title']}: "
            f"{result['similarity']}% "
            f"({result['type']})"
        )
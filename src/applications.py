from src.database import get_connection
from src.normalization import normalize_title
from src.phonetic import phonetic_key


def create_application(
    title: str,
    status: str = "PENDING",
    similarity_score: float = 0.0,
    rejection_reason: str = "",
) -> int:
    """
    Store a new title application.
    """

    normalized_title = normalize_title(title)
    title_phonetic_key = phonetic_key(title)

    connection = get_connection()

    cursor = connection.execute(
        """
        INSERT INTO applications (
            title,
            normalized_title,
            phonetic_key,
            status,
            similarity_score,
            rejection_reason
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            title,
            normalized_title,
            title_phonetic_key,
            status,
            similarity_score,
            rejection_reason,
        ),
    )

    application_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return application_id


def get_applications() -> list[dict]:
    """
    Return all submitted applications.
    """

    connection = get_connection()

    rows = connection.execute(
        """
        SELECT
            id,
            title,
            status,
            similarity_score,
            rejection_reason,
            created_at
        FROM applications
        ORDER BY created_at DESC
        """
    ).fetchall()

    connection.close()

    return [
        {
            "id": row[0],
            "title": row[1],
            "status": row[2],
            "similarity_score": row[3],
            "rejection_reason": row[4],
            "created_at": row[5],
        }
        for row in rows
    ]


if __name__ == "__main__":
    application_id = create_application(
        "Example New Newspaper",
    )

    print(
        f"Application created with ID: "
        f"{application_id}"
    )

    for application in get_applications():
        print(application)
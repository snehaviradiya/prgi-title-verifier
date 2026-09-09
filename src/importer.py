import csv

from src.database import get_connection
from src.normalization import normalize_title
from src.phonetic import phonetic_key


def import_titles(file_path):
    connection = get_connection()

    with open(file_path, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        count = 0

        for row in reader:
            title = row["title"].strip()
            source = row.get("source", "Unknown").strip()

            if not title:
                continue

            normalized_title = normalize_title(title)
            title_phonetic_key = phonetic_key(title)

            connection.execute(
                """
                INSERT INTO titles (
                    title,
                    normalized_title,
                    phonetic_key,
                    source
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    title,
                    normalized_title,
                    title_phonetic_key,
                    source,
                ),
            )

            count += 1

    connection.commit()
    connection.close()

    return count


if __name__ == "__main__":
    count = import_titles("data/titles.csv")
    print(f"Imported {count} titles.")
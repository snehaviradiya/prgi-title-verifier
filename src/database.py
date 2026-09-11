import sqlite3
from pathlib import Path


DATABASE_PATH = Path("database/titles.db")


def get_connection():
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DATABASE_PATH)


def add_application_phonetic_column(connection):
    columns = connection.execute(
        "PRAGMA table_info(applications)"
    ).fetchall()

    column_names = {
        column[1]
        for column in columns
    }

    if "phonetic_key" not in column_names:
        connection.execute("""
            ALTER TABLE applications
            ADD COLUMN phonetic_key TEXT
        """)


def initialize_database():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS titles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            normalized_title TEXT,
            phonetic_key TEXT,
            source TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.execute("""
        CREATE INDEX IF NOT EXISTS idx_normalized_title
        ON titles(normalized_title)
    """)

    connection.execute("""
        CREATE INDEX IF NOT EXISTS idx_phonetic_key
        ON titles(phonetic_key)
    """)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            normalized_title TEXT,
            status TEXT NOT NULL,
            similarity_score REAL,
            rejection_reason TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    add_application_phonetic_column(connection)

    connection.execute("""
        CREATE INDEX IF NOT EXISTS idx_application_title
        ON applications(normalized_title)
    """)

    connection.execute("""
        CREATE INDEX IF NOT EXISTS idx_application_status
        ON applications(status)
    """)

    connection.execute("""
        CREATE INDEX IF NOT EXISTS idx_application_phonetic
        ON applications(phonetic_key)
    """)

    connection.commit()
    connection.close()


if __name__ == "__main__":
    initialize_database()
    print("Database initialized successfully.")
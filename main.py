from src.database import initialize_database


def main():
    initialize_database()

    print("=" * 45)
    print("       PRGI TITLE VERIFICATION SYSTEM")
    print("=" * 45)
    print()
    print("1. Verify New Title")
    print("2. View Applications")
    print("3. Exit")


if __name__ == "__main__":
    main()
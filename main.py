from src.applications import get_applications
from src.database import initialize_database
from src.verifier import verify_title


def print_verification_result(result):
    print()
    print("=" * 55)
    print(f"Title: {result['title']}")
    print(f"Decision: {result['decision']}")
    print(f"Similarity: {result['similarity_score']}%")
    print(
        f"Acceptance probability: "
        f"{result['acceptance_probability']}%"
    )

    if result["best_match"]:
        print(
            f"Best match: "
            f"{result['best_match']['title']} "
            f"({result['best_match']['score']}%)"
        )

    if result["rejection_reasons"]:
        print()
        print("Reasons:")

        for reason in result["rejection_reasons"]:
            print(f"- {reason}")

    print("=" * 55)


def verify_new_title():
    title = input("\nEnter title to verify: ").strip()

    if not title:
        print("Title cannot be empty.")
        return

    result = verify_title(title)

    print_verification_result(result)


def view_applications():
    applications = get_applications()

    print()
    print("=" * 55)
    print("APPLICATIONS")
    print("=" * 55)

    if not applications:
        print("No applications found.")
        return

    for application in applications:
        print(
            f"\nID: {application['id']}"
        )
        print(
            f"Title: {application['title']}"
        )
        print(
            f"Status: {application['status']}"
        )
        print(
            f"Similarity: "
            f"{application['similarity_score']}%"
        )
        print(
            f"Created: {application['created_at']}"
        )


def main():
    initialize_database()

    while True:
        print()
        print("=" * 55)
        print("       PRGI TITLE VERIFICATION SYSTEM")
        print("=" * 55)
        print()
        print("1. Verify New Title")
        print("2. View Applications")
        print("3. Exit")

        choice = input("\nSelect an option: ").strip()

        if choice == "1":
            verify_new_title()

        elif choice == "2":
            view_applications()

        elif choice == "3":
            print("\nGoodbye.")
            break

        else:
            print("\nInvalid option. Please choose 1, 2, or 3.")


if __name__ == "__main__":
    main()